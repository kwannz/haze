# Contributing to Haze-Library

Thank you for your interest in contributing to Haze-Library! This document provides guidelines and instructions for contributing.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Contributions](#making-contributions)
- [Coding Standards](#coding-standards)
- [Testing Requirements](#testing-requirements)
- [Pull Request Process](#pull-request-process)

## Code of Conduct

We are committed to providing a welcoming and inclusive environment. Please be respectful and professional in all interactions.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/haze-library.git
   cd haze-library
   ```
3. **Add upstream remote**:
   ```bash
   git remote add upstream https://github.com/haze-library/haze-library.git
   ```

## Development Setup

### Prerequisites

- Python 3.9+
- Rust 1.75+
- Maturin (`pip install maturin`)
- pytest (`pip install pytest pytest-cov`)

### Building the Library

```bash
# Navigate to Rust directory
cd rust

# Build in development mode (faster compilation)
maturin develop

# Or build in release mode (optimized)
maturin develop --release

# Return to project root
cd ..
```

### Running Tests

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=haze_library --cov-report=html

# Run precision validation
python tests/run_precision_tests.py
```

## Making Contributions

### Types of Contributions

We welcome the following types of contributions:

1. **Bug Fixes**: Fix incorrect indicator calculations or runtime errors
2. **New Indicators**: Implement additional technical analysis indicators
3. **Performance Improvements**: Optimize existing algorithms with SIMD or better algorithms
4. **Documentation**: Improve README, docstrings, or create tutorials
5. **Tests**: Add unit tests or precision validation tests

### Creating a New Indicator

If you want to add a new indicator, follow this template:

#### 1. Create Rust Implementation

File: `rust/src/indicators/YOUR_CATEGORY.rs`

```rust
use crate::errors::{HazeError, HazeResult};
use crate::errors::validation::{validate_not_empty, validate_period};
use crate::init_result;

/// YOUR_INDICATOR - Brief description
///
/// Algorithm:
/// - Step 1: Description of calculation
/// - Step 2: ...
///
/// # Parameters
/// - `values`: Input price data
/// - `period`: Lookback period
///
/// # Returns
/// - `Ok(Vec<f64>)`: Indicator values (NaN for warmup period)
///
/// # Errors
/// - `HazeError::EmptyInput`: If values is empty
/// - `HazeError::InvalidPeriod`: If period is 0 or > values.len()
/// - `HazeError::InsufficientData`: If values.len() < required minimum
///
/// # Example
/// ```rust
/// let close = vec![10.0, 11.0, 12.0, 13.0, 14.0];
/// let result = your_indicator(&close, 3)?;
/// assert!(result[0].is_nan());  // Warmup period
/// assert!(!result[2].is_nan()); // Valid value
/// ```
pub fn your_indicator(values: &[f64], period: usize) -> HazeResult<Vec<f64>> {
    // ✅ Step 1: Input validation (Fail-Fast principle)
    validate_not_empty(values, "values")?;
    validate_period(period, values.len())?;

    let n = values.len();
    let mut result = init_result!(n);

    // ✅ Step 2: Calculation logic (no more errors returned)
    for i in (period - 1)..n {
        // Calculate indicator value
        result[i] = 0.0; // Replace with actual calculation
    }

    Ok(result)
}
```

**✅ Error Handling Requirements**:
1. Use `HazeResult<T>` as return type (not `Vec<f64>`)
2. Validate all inputs at function entry using `validation` module
3. Return `Err(HazeError::*)` for invalid inputs (empty, invalid period, etc.)
4. Return `Ok(Vec<f64>)` with NaN for warmup period
5. Document all possible errors in `# Errors` section
6. See `docs/ERROR_HANDLING_STRATEGY.md` for detailed guidelines

#### 2. Add PyO3 Wrapper

File: `rust/src/lib.rs`

```rust
/// Python wrapper for YOUR_INDICATOR
///
/// Args:
///     values (List[float]): Input price data
///     period (int): Lookback period
///
/// Returns:
///     List[float]: Indicator values (NaN for warmup period)
///
/// Raises:
///     ValueError: If values is empty
///     ValueError: If period is invalid (0 or > len(values))
///
/// Example:
///     >>> import haze_library as haze
///     >>> close = [10.0, 11.0, 12.0, 13.0, 14.0]
///     >>> result = haze.py_your_indicator(close, period=3)
#[pyfunction]
#[pyo3(name = "py_your_indicator")]
fn py_your_indicator(values: Vec<f64>, period: usize) -> PyResult<Vec<f64>> {
    // ✅ Use ? to automatically convert HazeError → PyErr (ValueError)
    Ok(indicators::your_category::your_indicator(&values, period)?)
}

// Register in #[pymodule] fn haze_library
m.add_function(wrap_pyfunction!(py_your_indicator, m)?)?;
```

**✅ Key Points**:
- Use `?` operator to propagate errors (auto-converts `HazeError` → `PyErr`)
- Document error scenarios in Python docstring (`Raises` section)
- No manual error conversion needed (PyO3 handles it via `From<HazeError>`)

#### 3. Add Unit Test

File: `tests/unit/test_YOUR_CATEGORY.py`

```python
import pytest
import numpy as np
import haze_library as haze

class TestYourIndicator:
    """Unit tests for YOUR_INDICATOR"""

    # ✅ REQUIRED: Test empty input (must raise ValueError)
    def test_empty_input(self):
        """Empty input should raise ValueError"""
        with pytest.raises(ValueError, match="Empty input"):
            haze.py_your_indicator([], period=3)

    # ✅ REQUIRED: Test invalid period (must raise ValueError)
    def test_invalid_period_zero(self):
        """Period = 0 should raise ValueError"""
        values = [10.0, 11.0, 12.0]
        with pytest.raises(ValueError, match="Invalid period"):
            haze.py_your_indicator(values, period=0)

    # ✅ REQUIRED: Test insufficient data (must raise ValueError)
    def test_insufficient_data(self):
        """Data length < period should raise ValueError"""
        values = [10.0, 11.0]
        with pytest.raises(ValueError, match="Insufficient data"):
            haze.py_your_indicator(values, period=10)

    # ✅ REQUIRED: Test basic calculation
    def test_basic_calculation(self, simple_prices):
        """Test basic calculation with hand-calculated values"""
        result = haze.py_your_indicator(simple_prices, period=3)

        # Verify NaN for warmup period
        assert np.isnan(result[0])
        assert np.isnan(result[1])

        # Verify calculated values (hand-calculated)
        assert not np.isnan(result[2])
        assert abs(result[2] - EXPECTED_VALUE) < 1e-10

    # ✅ RECOMMENDED: Test different periods
    def test_different_periods(self, simple_prices):
        """Test with different period parameters"""
        result_p2 = haze.py_your_indicator(simple_prices, period=2)
        result_p5 = haze.py_your_indicator(simple_prices, period=5)

        # Verify period-specific warmup
        assert not np.isnan(result_p2[1])
        assert np.isnan(result_p5[4])
```

**✅ Testing Requirements**:
1. **MUST** test empty input (expect `ValueError`)
2. **MUST** test invalid period (expect `ValueError`)
3. **MUST** test insufficient data (expect `ValueError`)
4. **MUST** test basic calculation with known values
5. **SHOULD** test warmup period NaN behavior
6. **SHOULD** test different period values
7. Use `pytest.raises(ValueError)` for error cases

#### 4. Add Precision Validation (Optional)

File: `tests/run_precision_tests.py`

```python
# Add to appropriate validation function
validator.validate_indicator(
    name="YOUR_INDICATOR",
    haze_func=lambda: haze.py_your_indicator(df['close'].tolist(), 14),
    reference_func=lambda: talib.YOUR_INDICATOR(df['close'].values, timeperiod=14),
    test_data=df.to_dict('list'),
    params={},
    reference_lib="TA-Lib"
)
```

#### 5. Update Documentation

- Add entry to `IMPLEMENTED_INDICATORS.md`
- Update indicator count in `README.md`

## Coding Standards

### Rust Code

- **Style**: Follow `rustfmt` defaults (`cargo fmt`)
- **Linting**: No warnings from `clippy` (`cargo clippy`)
- **Naming**: `snake_case` for functions, `SCREAMING_SNAKE_CASE` for constants
- **Documentation**: Doc comments (`///`) for all public functions
- **Error Handling**: Use `Result<T, E>` for fallible operations

### Python Code

- **Style**: Follow PEP 8 (use `black` formatter)
- **Type Hints**: Use type annotations for all function signatures
- **Docstrings**: Google-style docstrings for all public functions
- **Testing**: pytest conventions

### Design Principles

Follow the principles outlined in `CLAUDE.md`:

1. **KISS (Keep It Simple)**: Avoid unnecessary complexity
2. **YAGNI (You Aren't Gonna Need It)**: Don't implement未来 features
3. **SOLID**: Single responsibility per module/function
4. **Occam's Razor**: Minimal dependencies and assumptions

## Testing Requirements

All contributions must include:

1. **Unit Tests**: Test with small datasets (5-20 points) and hand-calculated expected values
2. **Edge Cases**: Empty arrays, insufficient data, NaN handling
3. **Precision**: < 1e-10 error tolerance for basic calculations

### Test Coverage

- **Target**: > 80% code coverage
- **Command**: `pytest tests/unit/ --cov=haze_library --cov-report=html`

### Precision Validation

For new indicators, optionally add precision validation against TA-Lib or pandas-ta:

```bash
python tests/run_precision_tests.py
```

**Expected**:
- Max Error < 1e-9
- Correlation > 0.9999

## Documentation Requirements

All code contributions must include proper documentation:

### Rust Documentation

1. **Public API Documentation**: All public functions, structs, traits, and modules must have doc comments (`///`)
2. **Private Item Documentation**: Document private items when their purpose is not immediately obvious
3. **Include Examples**: Add code examples in doc comments using `# Example` sections
4. **Document Parameters**: Use `# Parameters` section to describe all function parameters
5. **Document Return Values**: Use `# Returns` section to describe return values
6. **Document Safety**: Use `# Safety` section for unsafe code
7. **Document Panics**: Use `# Panics` section if function can panic

Example:
```rust
/// Calculates the Simple Moving Average (SMA) over a specified period.
///
/// # Parameters
/// - `values`: Slice of input price data
/// - `period`: Number of periods for the moving average
///
/// # Returns
/// Vector of SMA values (NaN for initial period where data is insufficient)
///
/// # Example
/// ```
/// let prices = vec![10.0, 11.0, 12.0, 13.0, 14.0];
/// let sma = simple_moving_average(&prices, 3);
/// assert!(sma[2].is_finite());  // First valid SMA at index 2
/// ```
///
/// # Panics
/// Panics if `period` is 0.
pub fn simple_moving_average(values: &[f64], period: usize) -> Vec<f64> {
    // Implementation...
}
```

### Documentation Tools

Use the provided scripts to check documentation quality:

```bash
# Generate documentation and open in browser
./scripts/generate_docs.sh --open

# Check documentation coverage and quality
./scripts/check_docs.sh

# View documentation coverage report
cat doc-coverage-report.md
```

### Documentation Coverage Standards

- **Minimum Coverage**: All new public items must be documented
- **Coverage Target**: Maintain or improve overall documentation coverage
- **Quality**: Documentation should be clear, accurate, and helpful
- **Examples**: Include at least one example for complex functions

## Pull Request Process

### Before Submitting

1. **Update from upstream**:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Run all tests**:
   ```bash
   pytest tests/ -v
   python tests/run_precision_tests.py
   ```

3. **Check documentation**:
   ```bash
   ./scripts/check_docs.sh
   ```

4. **Format code**:
   ```bash
   cd rust
   cargo fmt
   cargo clippy
   cd ..
   black tests/
   ```

5. **Update documentation**:
   - README.md (if adding new indicator)
   - IMPLEMENTED_INDICATORS.md
   - CHANGELOG.md (under "Unreleased")
   - Add/update doc comments for new/modified code

### Submitting the PR

1. **Create a descriptive branch**:
   ```bash
   git checkout -b feature/add-awesome-indicator
   ```

2. **Commit with clear messages**:
   ```bash
   git commit -m "feat: add Awesome Indicator

   - Implement Awesome Oscillator in Rust
   - Add PyO3 wrapper py_awesome_oscillator
   - Add unit tests with hand-calculated values
   - Add precision validation vs TA-Lib
   - Add documentation with examples
   - Update IMPLEMENTED_INDICATORS.md (17 → 18 momentum indicators)
   "
   ```

3. **Push to your fork**:
   ```bash
   git push origin feature/add-awesome-indicator
   ```

4. **Open Pull Request** on GitHub with:
   - **Title**: Clear and concise (e.g., "Add Awesome Oscillator indicator")
   - **Description**:
     - What does this PR do?
     - Why is this change needed?
     - How was it tested?
     - Documentation coverage status
     - Any breaking changes?

### PR Checklist

Before submitting your PR, ensure you have completed the following:

- [ ] All tests pass (`pytest tests/ -v`)
- [ ] Code is formatted (`cargo fmt`, `black tests/`)
- [ ] No clippy warnings (`cargo clippy`)
- [ ] Documentation is complete (all public items documented)
- [ ] Documentation quality check passes (`./scripts/check_docs.sh`)
- [ ] Examples included in doc comments
- [ ] CHANGELOG.md updated
- [ ] README.md updated (if adding new features)
- [ ] No decrease in documentation coverage

### PR Review Process

1. Automated checks will run (future: CI/CD)
2. Maintainers will review code quality and test coverage
3. Address review comments
4. Once approved, maintainers will merge

## Questions?

- **Issues**: [GitHub Issues](https://github.com/haze-library/haze-library/issues)
- **Discussions**: [GitHub Discussions](https://github.com/haze-library/haze-library/discussions)
- **Email**: team@haze-library.com

Thank you for contributing to Haze-Library! 🎉
