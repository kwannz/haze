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
pytest tests/ --cov=_haze_rust --cov-report=html

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
/// YOUR_INDICATOR - Brief description
///
/// # Parameters
/// - `values`: Input price data
/// - `period`: Lookback period
///
/// # Returns
/// - `Vec<f64>`: Indicator values (NaN for initial period)
///
/// # Example
/// ```
/// let close = vec![10.0, 11.0, 12.0, 13.0, 14.0];
/// let result = your_indicator(&close, 3);
/// ```
pub fn your_indicator(values: &[f64], period: usize) -> Vec<f64> {
    let n = values.len();
    let mut result = vec![f64::NAN; n];

    if n < period {
        return result;
    }

    // Your algorithm implementation here
    for i in (period - 1)..n {
        // Calculate indicator value
        result[i] = 0.0; // Replace with actual calculation
    }

    result
}
```

#### 2. Add PyO3 Wrapper

File: `rust/src/lib.rs`

```rust
#[pyfunction]
#[pyo3(name = "py_your_indicator")]
fn py_your_indicator(values: Vec<f64>, period: usize) -> PyResult<Vec<f64>> {
    Ok(indicators::your_category::your_indicator(&values, period))
}

// Register in #[pymodule] fn _haze_rust
m.add_function(wrap_pyfunction!(py_your_indicator, m)?)?;
```

#### 3. Add Unit Test

File: `tests/unit/test_YOUR_CATEGORY.py`

```python
import pytest
import numpy as np
import _haze_rust as haze

class TestYourIndicator:
    """Unit tests for YOUR_INDICATOR"""

    def test_basic_calculation(self, simple_prices):
        """Test basic calculation with hand-calculated values"""
        result = haze.py_your_indicator(simple_prices, period=3)

        # Verify NaN for initial period
        assert np.isnan(result[0])
        assert np.isnan(result[1])

        # Verify calculated values (hand-calculated)
        assert abs(result[2] - EXPECTED_VALUE) < 1e-10

    def test_edge_cases(self):
        """Test edge cases"""
        # Empty array
        result = haze.py_your_indicator([], period=3)
        assert len(result) == 0

        # Insufficient data
        result = haze.py_your_indicator([10.0, 11.0], period=3)
        assert all(np.isnan(result))

    def test_different_periods(self, simple_prices):
        """Test with different period parameters"""
        result_p2 = haze.py_your_indicator(simple_prices, period=2)
        result_p5 = haze.py_your_indicator(simple_prices, period=5)

        # Verify period-specific behavior
        assert not np.isnan(result_p2[1])
        assert np.isnan(result_p5[4])
```

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
- **Command**: `pytest tests/unit/ --cov=_haze_rust --cov-report=html`

### Precision Validation

For new indicators, optionally add precision validation against TA-Lib or pandas-ta:

```bash
python tests/run_precision_tests.py
```

**Expected**:
- Max Error < 1e-9
- Correlation > 0.9999

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

3. **Format code**:
   ```bash
   cd rust
   cargo fmt
   cargo clippy
   cd ..
   black tests/
   ```

4. **Update documentation**:
   - README.md (if adding new indicator)
   - IMPLEMENTED_INDICATORS.md
   - CHANGELOG.md (under "Unreleased")

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
     - Any breaking changes?

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
