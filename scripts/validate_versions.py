#!/usr/bin/env python3
"""
Validate version consistency across all project files.
"""

import re
import sys
from pathlib import Path


def extract_version(file_path: Path, pattern: str) -> str | None:
    """Extract version from file using regex pattern."""
    if not file_path.exists():
        return None

    content = file_path.read_text()
    match = re.search(pattern, content)
    return match.group(1) if match else None


def main():
    project_root = Path(__file__).parent.parent
    expected_version = sys.argv[1] if len(sys.argv) > 1 else None

    version_files = {
        "pyproject.toml": (
            project_root / "pyproject.toml",
            r'version\s*=\s*"([^"]+)"'
        ),
        "rust/Cargo.toml": (
            project_root / "rust" / "Cargo.toml",
            r'version\s*=\s*"([^"]+)"'
        ),
        "rust/pyproject.toml": (
            project_root / "rust" / "pyproject.toml",
            r'version\s*=\s*"([^"]+)"'
        ),
        "README.md": (
            project_root / "README.md",
            r'\*\*版本\*\*:\s*([0-9.]+)'
        ),
        "src/haze_library/__init__.py": (
            project_root / "src" / "haze_library" / "__init__.py",
            r'__version__\s*=\s*"([^"]+)"'
        ),
    }

    print("=" * 60)
    print("Version Consistency Check")
    print("=" * 60)

    versions = {}
    for name, (path, pattern) in version_files.items():
        version = extract_version(path, pattern)
        versions[name] = version
        status = "✓" if version else "✗"
        print(f"{status} {name:40} → {version or 'NOT FOUND'}")

    # Check consistency
    unique_versions = set(v for v in versions.values() if v)

    print("\n" + "=" * 60)

    if len(unique_versions) > 1:
        print(f"❌ ERROR: Version mismatch detected!")
        print(f"   Found versions: {unique_versions}")
        print("\nPlease ensure all files have the same version number.")
        return 1

    if expected_version and unique_versions != {expected_version}:
        print(f"❌ ERROR: Expected version {expected_version}, found {unique_versions}")
        print("\nPlease update version numbers to match the expected version.")
        return 1

    current_version = unique_versions.pop() if unique_versions else "UNKNOWN"
    print(f"✅ All versions consistent: {current_version}")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
