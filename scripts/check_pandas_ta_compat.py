#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Iterable, Optional, Tuple


def _import_pandas_ta(repo_root: Path) -> Tuple[object, bool]:
    tests_dir = repo_root / "tests"
    sys.path.insert(0, str(tests_dir))
    try:
        from pandas_ta_compat import import_pandas_ta  # type: ignore[import-not-found]
    except Exception as e:  # pragma: no cover
        raise RuntimeError(f"Could not import tests helper pandas_ta_compat: {e}") from e

    module, stubbed = import_pandas_ta()
    if module is None:
        raise RuntimeError(
            "pandas-ta is not installed or failed to import; "
            "install it first (e.g. `pip install pandas-ta --no-deps` then `pip install numpy pandas tqdm`)."
        )
    return module, stubbed


def _iter_category_items(category: object) -> Iterable[Tuple[str, object]]:
    if hasattr(category, "items") and callable(getattr(category, "items")):
        return category.items()  # type: ignore[no-any-return]
    data = getattr(category, "__dict__", {})
    if isinstance(data, dict):
        return data.items()
    return ()


def _extract_pandas_ta_indicator_names() -> set[str]:
    try:
        import pandas_ta.maps as maps  # type: ignore[import-not-found]
    except Exception as e:
        raise RuntimeError(f"Could not import pandas_ta.maps: {e}") from e

    category = getattr(maps, "Category", None)
    if category is None:
        raise RuntimeError("pandas_ta.maps.Category not found (unexpected pandas-ta layout)")

    names: set[str] = set()
    for key, value in _iter_category_items(category):
        if not isinstance(key, str) or key.startswith("_"):
            continue
        if isinstance(value, (list, tuple, set)):
            for item in value:
                if isinstance(item, str):
                    names.add(item)
    return names


def _extract_rust_compat_symbols(path: Path) -> set[str]:
    text = path.read_text(encoding="utf-8")
    return set(re.findall(r"\bp::([A-Za-z0-9_]+)\b", text))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check that Rust pandas_ta_compat symbols match pandas-ta Category map."
    )
    parser.add_argument("--repo-root", default=".", help="Repo root (default: .)")
    parser.add_argument(
        "--rust-test-file",
        default="rust/tests/pandas_ta_compat_symbols.rs",
        help="Path to rust compat symbol test file.",
    )
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    rust_test_file = (repo_root / args.rust_test_file).resolve()

    if not rust_test_file.exists():
        print(f"Missing rust test file: {rust_test_file}", file=sys.stderr)
        return 2

    try:
        pta, stubbed = _import_pandas_ta(repo_root)
    except RuntimeError as e:
        print(str(e), file=sys.stderr)
        return 2

    version = getattr(pta, "__version__", "unknown")
    expected = _extract_pandas_ta_indicator_names()
    actual = _extract_rust_compat_symbols(rust_test_file)

    missing = sorted(expected - actual)
    extra = sorted(actual - expected)

    if missing or extra:
        print("PANDAS-TA COMPAT CHECK FAILED\n", file=sys.stderr)
        print(f"- pandas-ta version: {version}", file=sys.stderr)
        if stubbed:
            print("- pandas-ta import: using numba stub", file=sys.stderr)
        if missing:
            print(f"- Missing in rust compat test ({len(missing)}): {missing}", file=sys.stderr)
        if extra:
            print(f"- Extra in rust compat test ({len(extra)}): {extra}", file=sys.stderr)
        return 2

    print("pandas-ta compat check OK")
    print(f"- pandas-ta version: {version}")
    print(f"- indicators: {len(expected)}")
    if stubbed:
        print("- pandas-ta import: using numba stub")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
