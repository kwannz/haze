#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
import tarfile
import zipfile
from pathlib import Path


def _toml_load(path: Path) -> dict:
    try:
        import tomllib  # py>=3.11
    except ModuleNotFoundError:  # pragma: no cover
        import tomli as tomllib  # type: ignore[no-redef]

    with path.open("rb") as f:
        return tomllib.load(f)


def _read_pyproject_version(path: Path) -> str:
    data = _toml_load(path)
    return str(data["project"]["version"])


def _read_cargo_version(path: Path) -> str:
    data = _toml_load(path)
    return str(data["package"]["version"])


def _read_python_dunder_version(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    m = re.search(r"""__version__\s*=\s*["']([^"']+)["']""", text)
    if not m:
        raise ValueError(f"Could not find __version__ in {path}")
    return m.group(1)


def _wheel_matches(name: str, required_tokens: list[str]) -> bool:
    lower = name.lower()
    return all(token.lower() in lower for token in required_tokens)


def _parse_wheel_tags(filename: str) -> tuple[str, str, str]:
    """
    Parse the (python_tag, abi_tag, platform_tag) from a wheel filename.

    Wheel format: {distribution}-{version}-{python tag}-{abi tag}-{platform tag}.whl
    """

    if not filename.endswith(".whl"):
        raise ValueError(f"Not a wheel file: {filename}")

    stem = filename[:-4]
    parts = stem.split("-")
    if len(parts) < 5:
        raise ValueError(f"Unrecognized wheel filename format: {filename}")

    python_tag = parts[-3]
    abi_tag = parts[-2]
    platform_tag = parts[-1]
    return python_tag, abi_tag, platform_tag


def _expected_ext_tag_patterns(python_tag: str) -> list[str]:
    """
    Return substrings expected to appear in the compiled extension filename.

    Examples:
    - wheel python_tag=cp39 => extension may include 'cp39' (Windows) or 'cpython-39' (mac/linux)
    - wheel python_tag=cp310 => extension may include 'cp310' or 'cpython-310'
    """

    m = re.match(r"^cp(?P<digits>\\d+)$", python_tag)
    if not m:
        return []

    digits = m.group("digits")
    return [python_tag.lower(), f"cpython-{digits}".lower()]


def _check_wheel_contents(wheel: Path, *, errors: list[str]) -> None:
    try:
        python_tag, _, _ = _parse_wheel_tags(wheel.name)
    except ValueError as e:
        errors.append(str(e))
        return
    expected_patterns = _expected_ext_tag_patterns(python_tag)

    try:
        with zipfile.ZipFile(wheel) as zf:
            names = zf.namelist()
    except Exception as e:  # pragma: no cover
        errors.append(f"Could not read wheel {wheel.name}: {e}")
        return

    # Basic sanity: ensure pure-Python package files exist
    if "haze_library/__init__.py" not in names:
        errors.append(f"Wheel missing haze_library/__init__.py: {wheel.name}")

    # Validate compiled extension presence and python-tag consistency.
    ext_candidates = [
        n
        for n in names
        if n.startswith("haze_library/haze_library")
        and (n.endswith(".so") or n.endswith(".pyd"))
    ]

    if len(ext_candidates) != 1:
        errors.append(
            f"Wheel extension count mismatch: {wheel.name} has {len(ext_candidates)} "
            f"(candidates={ext_candidates})"
        )
        return

    ext_name = Path(ext_candidates[0]).name.lower()
    if expected_patterns and not any(p in ext_name for p in expected_patterns):
        errors.append(
            f"Wheel extension tag mismatch: {wheel.name} contains {ext_name} "
            f"(expected python tag {python_tag})"
        )


def _check_sdist_contents(sdist: Path, *, errors: list[str]) -> None:
    try:
        with tarfile.open(sdist, mode="r:gz") as tf:
            member_names = [m.name for m in tf.getmembers()]
    except Exception as e:  # pragma: no cover
        errors.append(f"Could not read sdist {sdist.name}: {e}")
        return

    banned_suffixes = (".so", ".pyd", ".dll", ".dylib")
    banned = [n for n in member_names if n.lower().endswith(banned_suffixes)]
    if banned:
        errors.append(f"sdist contains binary artifacts: {sdist.name} (files={banned})")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Release preflight: version sync + dist artifact validation."
    )
    parser.add_argument("--repo-root", default=".", help="Repo root (default: .)")
    parser.add_argument("--dist-dir", default="dist", help="Dist dir (default: dist)")
    parser.add_argument(
        "--expected-version",
        required=True,
        help="Expected version (e.g. 0.1.2, without leading 'v')",
    )
    parser.add_argument(
        "--require-full-matrix",
        action="store_true",
        help="Require full wheel matrix coverage for all configured Python versions/platforms.",
    )

    args = parser.parse_args()

    expected = str(args.expected_version).lstrip("v")
    repo_root = Path(args.repo_root).resolve()
    dist_dir = Path(args.dist_dir).resolve()

    errors: list[str] = []

    # ---------------------------------------------------------------------
    # Version sync
    # ---------------------------------------------------------------------
    pyproject = repo_root / "pyproject.toml"
    cargo = repo_root / "rust" / "Cargo.toml"
    init_py = repo_root / "src" / "haze_library" / "__init__.py"
    rust_pyproject = repo_root / "rust" / "pyproject.toml"

    pyproject_version = _read_pyproject_version(pyproject)
    cargo_version = _read_cargo_version(cargo)
    init_version = _read_python_dunder_version(init_py)

    versions = [
        ("pyproject.toml", pyproject_version),
        ("rust/Cargo.toml", cargo_version),
        ("src/haze_library/__init__.py", init_version),
    ]

    if rust_pyproject.exists():
        versions.append(("rust/pyproject.toml", _read_pyproject_version(rust_pyproject)))

    for label, version in versions:
        if version != expected:
            errors.append(f"Version mismatch: {label}={version} expected={expected}")

    # Prevent accidental inclusion of built extension artifacts in the Python source tree.
    src_dir = repo_root / "src"
    if src_dir.exists():
        banned_suffixes = (".so", ".pyd", ".dll", ".dylib")
        binaries = [
            p
            for p in src_dir.rglob("*")
            if p.is_file() and p.suffix.lower() in banned_suffixes
        ]
        if binaries:
            rel = [str(p.relative_to(repo_root)) for p in sorted(binaries)]
            errors.append(f"Binary artifacts found under src/: {rel}")

    # ---------------------------------------------------------------------
    # Dist artifacts
    # ---------------------------------------------------------------------
    if not dist_dir.exists():
        errors.append(f"Missing dist directory: {dist_dir}")
    else:
        wheels = sorted(dist_dir.glob("*.whl"))
        sdists = sorted(dist_dir.glob("*.tar.gz"))

        if not wheels:
            errors.append("No wheels found in dist/")
        if not sdists:
            errors.append("No sdists (.tar.gz) found in dist/")

        for w in wheels:
            if expected not in w.name:
                errors.append(f"Wheel version mismatch: {w.name} (expected {expected})")

        if sdists and not any(expected in s.name for s in sdists):
            errors.append(
                f"sdist version mismatch: {[s.name for s in sdists]} (expected {expected})"
            )

        for w in wheels:
            _check_wheel_contents(w, errors=errors)

        for s in sdists:
            _check_sdist_contents(s, errors=errors)

        # -----------------------------------------------------------------
        # Wheel matrix coverage (strict gate for releases)
        # -----------------------------------------------------------------
        if args.require_full_matrix and wheels:
            python_tags = {
                "3.14": "cp314",
            }

            targets: dict[str, list[str]] = {
                "linux-x86_64": ["manylinux", "x86_64"],
                "linux-aarch64": ["manylinux", "aarch64"],
                "macos-x86_64": ["macosx", "x86_64"],
                "macos-arm64": ["macosx", "arm64"],
                "windows-amd64": ["win_amd64"],
            }

            for py_ver, cp_tag in python_tags.items():
                for target_name, tokens in targets.items():
                    required = [cp_tag, *tokens]
                    matches = [w for w in wheels if _wheel_matches(w.name, required)]
                    if not matches:
                        errors.append(
                            f"Missing wheel: {target_name} py{py_ver} (tokens={required})"
                        )

    # ---------------------------------------------------------------------
    # Report
    # ---------------------------------------------------------------------
    if errors:
        print("RELEASE PREFLIGHT FAILED\n", file=sys.stderr)
        for e in errors:
            print(f"- {e}", file=sys.stderr)
        return 2

    print("Release preflight OK")
    print(f"- version: {expected}")
    print(f"- dist: {dist_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
