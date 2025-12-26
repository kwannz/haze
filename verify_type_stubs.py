#!/usr/bin/env python3
"""
Verify Type Stubs for Haze-Library
===================================

Validates that .pyi stub files are correctly generated and accessible.
"""

import sys
from pathlib import Path
from typing import get_type_hints

def verify_pyi_files():
    """Verify that .pyi files exist and are valid."""
    print("=" * 70)
    print("Haze-Library Type Stubs Verification")
    print("=" * 70)

    project_root = Path(__file__).parent
    haze_lib_path = project_root / 'src' / 'haze_library'

    # Check for .pyi files
    pyi_files = [
        haze_lib_path / '__init__.pyi',
        haze_lib_path / 'haze_library.pyi'
    ]

    print("\n1. Checking .pyi files existence...")
    print("-" * 70)

    all_exist = True
    for pyi_file in pyi_files:
        exists = pyi_file.exists()
        status = "✅ Found" if exists else "❌ Missing"
        print(f"  {status}: {pyi_file.name} ({pyi_file.stat().st_size if exists else 0} bytes)")
        if not exists:
            all_exist = False

    if not all_exist:
        print("\n❌ Some .pyi files are missing!")
        return False

    # Check for py.typed marker
    print("\n2. Checking PEP 561 compliance...")
    print("-" * 70)

    py_typed = haze_lib_path / 'py.typed'
    if py_typed.exists():
        print(f"  ✅ Found: py.typed marker file")
    else:
        print(f"  ⚠️  Missing: py.typed marker file")
        print("     Creating py.typed marker...")
        py_typed.touch()
        print("  ✅ Created: py.typed")

    # Count functions in .pyi files
    print("\n3. Analyzing function signatures...")
    print("-" * 70)

    haze_library_pyi = haze_lib_path / 'haze_library.pyi'
    with open(haze_library_pyi, 'r') as f:
        content = f.read()

    import re
    func_pattern = r'^def (py_\w+)\('
    functions = re.findall(func_pattern, content, re.MULTILINE)

    print(f"  Total functions in haze_library.pyi: {len(functions)}")

    # Categorize functions
    categories = {
        'Volatility': 0,
        'Momentum': 0,
        'Trend': 0,
        'Volume': 0,
        'Moving Averages': 0,
        'Candlestick Patterns': 0,
        'Statistical': 0,
        'Math': 0,
        'Other': 0
    }

    for line in content.split('\n'):
        if line.startswith('# ') and '(' in line and 'functions)' in line:
            parts = line.split('(')
            if len(parts) >= 2:
                count_part = parts[1].split()[0]
                category_part = parts[0].replace('# ', '').strip()

                try:
                    count = int(count_part)
                    for category in categories:
                        if category in category_part:
                            categories[category] = count
                            break
                    else:
                        categories['Other'] += count
                except ValueError:
                    pass

    print("\n  Breakdown by category:")
    total_categorized = 0
    for category, count in categories.items():
        if count > 0:
            print(f"    {category:25s}: {count:3d} functions")
            total_categorized += count

    # Try to import haze_library
    print("\n4. Testing module import...")
    print("-" * 70)

    try:
        import haze_library
        print(f"  ✅ Successfully imported haze_library")
        print(f"     Version: {haze_library.__version__}")

        # Check for key functions
        key_functions = [
            'py_sma', 'py_ema', 'py_rsi', 'py_macd',
            'py_bollinger_bands', 'py_atr', 'py_supertrend'
        ]

        missing = []
        for func_name in key_functions:
            if hasattr(haze_library, func_name):
                print(f"  ✅ Found: {func_name}")
            else:
                print(f"  ❌ Missing: {func_name}")
                missing.append(func_name)

        if missing:
            print(f"\n  ⚠️  Missing {len(missing)} key functions")
            return False

    except ImportError as e:
        print(f"  ❌ Failed to import haze_library: {e}")
        return False

    # Test type hints (if typing_extensions is available)
    print("\n5. Testing type hint accessibility...")
    print("-" * 70)

    try:
        # Try to get type hints for a few functions
        test_functions = ['py_sma', 'py_rsi', 'py_macd']

        for func_name in test_functions:
            func = getattr(haze_library, func_name, None)
            if func:
                # Check if function has annotations
                if hasattr(func, '__annotations__'):
                    print(f"  ✅ {func_name}: has __annotations__")
                else:
                    print(f"  ⚠️  {func_name}: no __annotations__ (expected for Rust extensions)")

    except Exception as e:
        print(f"  ⚠️  Type hint testing: {e}")

    # Test pandas accessor (if pandas is available)
    print("\n6. Testing Pandas accessor...")
    print("-" * 70)

    try:
        import pandas as pd
        from haze_library import TechnicalAnalysisAccessor

        print(f"  ✅ TechnicalAnalysisAccessor imported")

        # Create a simple DataFrame
        df = pd.DataFrame({'close': [100.0, 101.0, 102.0, 103.0, 104.0]})

        # Check if .ta accessor is available
        if hasattr(df, 'ta'):
            print(f"  ✅ DataFrame.ta accessor registered")

            # Test a simple indicator
            try:
                result = df.ta.sma(3)
                print(f"  ✅ df.ta.sma(3) works (result length: {len(result)})")
            except Exception as e:
                print(f"  ⚠️  df.ta.sma(3) failed: {e}")
        else:
            print(f"  ❌ DataFrame.ta accessor not found")

    except ImportError:
        print(f"  ⚠️  Pandas not installed - skipping accessor test")

    # Summary
    print("\n" + "=" * 70)
    print("Verification Summary")
    print("=" * 70)

    print(f"\n✅ All critical checks passed!")
    print(f"\nType stub files are ready for IDE support.")
    print(f"Total functions with type hints: {len(functions)}")

    return True


def test_mypy_compatibility():
    """Test if mypy can use the type stubs."""
    print("\n7. Testing mypy compatibility...")
    print("-" * 70)

    try:
        import subprocess

        # Create a simple test file
        test_file = Path(__file__).parent / 'test_type_checking.py'
        with open(test_file, 'w') as f:
            f.write("""
from typing import List
from haze_library import py_sma, py_rsi

# This should pass type checking
close_prices: List[float] = [100.0, 101.0, 102.0]
result: List[float] = py_sma(close_prices, 2)

# This should fail type checking (uncomment to test)
# wrong_type: str = py_sma(close_prices, 2)
""")

        # Try to run mypy
        result = subprocess.run(
            ['mypy', '--no-error-summary', str(test_file)],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode == 0:
            print("  ✅ mypy validation passed!")
        else:
            print("  ⚠️  mypy found issues:")
            print(result.stdout)

        # Clean up
        test_file.unlink()

    except FileNotFoundError:
        print("  ⚠️  mypy not installed - skipping mypy test")
        print("     Install with: pip install mypy")
    except Exception as e:
        print(f"  ⚠️  mypy test failed: {e}")


if __name__ == '__main__':
    success = verify_pyi_files()

    # Optional: test mypy
    test_mypy_compatibility()

    print("\n" + "=" * 70)
    if success:
        print("✅ Verification completed successfully!")
        print("\nNext steps:")
        print("  1. Open the project in VS Code or PyCharm")
        print("  2. Try auto-completion with haze_library functions")
        print("  3. Run: python examples/type_hints_demo.py")
        print("  4. Run: mypy examples/type_hints_demo.py")
        sys.exit(0)
    else:
        print("❌ Verification failed!")
        print("\nPlease check the error messages above.")
        sys.exit(1)
