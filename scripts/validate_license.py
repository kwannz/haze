#!/usr/bin/env python3
"""
Validate license consistency across all project files.
"""

import sys
from pathlib import Path


def check_license_file(project_root: Path) -> bool:
    """Check LICENSE file contains Proprietary text."""
    license_file = project_root / "LICENSE"
    if not license_file.exists():
        print("❌ LICENSE file not found")
        return False

    content = license_file.read_text()
    if "PROPRIETARY LICENSE" not in content and "ALL RIGHTS RESERVED" not in content:
        print("❌ LICENSE file does not contain proprietary license text")
        return False

    print("✓ LICENSE file: Proprietary")
    return True


def check_cargo_toml(project_root: Path) -> bool:
    """Check Cargo.toml has correct license."""
    cargo_file = project_root / "rust" / "Cargo.toml"
    if not cargo_file.exists():
        print("❌ rust/Cargo.toml not found")
        return False

    content = cargo_file.read_text()
    if 'license = "Proprietary"' not in content:
        print("❌ rust/Cargo.toml: License not set to Proprietary")
        return False

    print("✓ rust/Cargo.toml: Proprietary")
    return True


def check_rust_pyproject_toml(project_root: Path) -> bool:
    """Check rust/pyproject.toml has correct license."""
    pyproject_file = project_root / "rust" / "pyproject.toml"
    if not pyproject_file.exists():
        print("❌ rust/pyproject.toml not found")
        return False

    content = pyproject_file.read_text()
    if 'license = { text = "Proprietary" }' not in content:
        print("❌ rust/pyproject.toml: License not set to Proprietary")
        return False

    print("✓ rust/pyproject.toml: Proprietary")
    return True


def check_pyproject_toml(project_root: Path) -> bool:
    """Check pyproject.toml has correct license classifier."""
    pyproject_file = project_root / "pyproject.toml"
    if not pyproject_file.exists():
        print("❌ pyproject.toml not found")
        return False

    content = pyproject_file.read_text()
    if "License :: Other/Proprietary License" not in content:
        print("❌ pyproject.toml: Missing proprietary license classifier")
        return False

    print("✓ pyproject.toml: Proprietary classifier")
    return True


def check_readme(project_root: Path) -> bool:
    """Check README.md has correct license section."""
    readme_file = project_root / "README.md"
    if not readme_file.exists():
        print("❌ README.md not found")
        return False

    content = readme_file.read_text()

    # Check for proprietary badge
    if "License-Proprietary" not in content:
        print("❌ README.md: License badge not updated to Proprietary")
        return False

    # Check for proprietary section (either Chinese or English)
    if "专有软件" not in content and "proprietary software" not in content.lower():
        print("❌ README.md: License section not updated to Proprietary")
        return False

    # Make sure CC BY-NC is not present
    if "CC BY-NC" in content or "CC-BY-NC" in content:
        print("❌ README.md: Old CC BY-NC license text still present")
        return False

    print("✓ README.md: Proprietary license badge and section")
    return True


def main():
    project_root = Path(__file__).parent.parent

    print("=" * 60)
    print("License Consistency Check")
    print("=" * 60)
    print()

    checks = [
        check_license_file(project_root),
        check_cargo_toml(project_root),
        check_rust_pyproject_toml(project_root),
        check_pyproject_toml(project_root),
        check_readme(project_root),
    ]

    print()
    print("=" * 60)

    if all(checks):
        print("✅ All license checks passed!")
        print("=" * 60)
        return 0
    else:
        print("❌ Some license checks failed!")
        print("=" * 60)
        print("\nPlease update the license information in the failed files.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
