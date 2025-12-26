# Numerical Stability Test Suite

## Overview

This test suite validates the numerical precision and stability of Haze indicators under extreme conditions that could expose floating-point arithmetic issues.

## Test File

**Location**: `tests/unit/test_numerical_stability.py`

## Test Categories

### 1. Large Numbers + Small Increments (`TestNumericalStability`)

Tests indicators with large base values (e.g., 1×10^10) and tiny changes (1×10^-5).

**Challenge**: Floating-point precision loss when adding small numbers to large numbers.

**Tests**:
- `test_large_numbers_small_increments`: Validates SMA maintains precision with relative error < 1×10^-8

### 2. Catastrophic Cancellation

Tests indicators when subtracting nearly equal values.

**Challenge**: Loss of significant digits when computing differences.

**Tests**:
- `test_catastrophic_cancellation`: RSI with balanced gains/losses should remain near 50

### 3. Long Sequence Precision

Tests error accumulation over many iterations.

**Challenge**: Rounding errors compound in recursive calculations.

**Tests**:
- `test_long_sequence_precision`: EMA over 100,000 points matches NumPy reference within 1×10^-6

### 4. NaN and Infinity Handling

Tests robustness with invalid inputs.

**Challenge**: NaN can propagate through calculations, invalidating entire results.

**Tests**:
- `test_nan_propagation`: Handles NaN input gracefully
- `test_division_by_zero_safety`: Bollinger Bands with zero variance
- `test_zero_and_negative_prices`: Invalid price values

### 5. Extreme Volatility

Tests with large price swings.

**Challenge**: Overflow or underflow in calculations.

**Tests**:
- `test_extreme_volatility`: Random price multipliers up to 10×
- `test_monotonic_increase`: Strictly increasing prices
- `test_alternating_large_small`: Values alternating between 1×10^10 and 1×10^-10

### 6. Very Small Numbers

Tests near underflow threshold.

**Challenge**: Values may underflow to zero.

**Tests**:
- `test_very_small_numbers`: Prices around 1×10^-9

### 7. Edge Case Parameters (`TestEdgeCaseParameters`)

Tests boundary conditions for indicator parameters.

**Tests**:
- `test_period_one`: SMA(1) should equal input
- `test_period_equals_length`: SMA(n) with n data points
- `test_very_large_period`: Period > data length should return all NaN

### 8. Memory Efficiency (`TestMemoryEfficiency`)

Tests performance with large datasets.

**Tests**:
- `test_large_dataset_no_overflow`: 1 million data points
- `test_multiple_indicators_sequentially`: Running multiple indicators on large data

## Running the Tests

### Run All Numerical Stability Tests

```bash
pytest tests/unit/test_numerical_stability.py -v
```

### Run with Coverage

```bash
pytest tests/unit/test_numerical_stability.py --cov=haze_library --cov-report=term-missing
```

### Run Specific Test Class

```bash
pytest tests/unit/test_numerical_stability.py::TestNumericalStability -v
```

### Run Single Test

```bash
pytest tests/unit/test_numerical_stability.py::TestNumericalStability::test_large_numbers_small_increments -v
```

## Expected Results

All tests should **PASS** with these characteristics:

1. **No Crashes**: All tests complete without exceptions
2. **Finite Results**: No NaN or Inf in valid calculation regions
3. **Bounded Error**: Results match reference implementations within tolerance
4. **Consistent Behavior**: Results are reproducible across runs

## Failure Investigation

If a test fails, check:

1. **Input Data**: Verify test data generation
2. **Expected Behavior**: Confirm expected results are reasonable
3. **Implementation**: Check if indicator algorithm changed
4. **Precision Threshold**: May need adjustment for different architectures

## Continuous Integration

These tests run automatically on every commit via GitHub Actions:

- **Workflow**: `.github/workflows/precision_tests.yml`
- **Schedule**: On push, pull request, and daily at 2 AM UTC
- **Platforms**: Ubuntu and macOS
- **Python Versions**: 3.10, 3.11, 3.12

## Benchmarks

Corresponding Rust benchmarks measure performance:

**Location**: `rust/benches/numerical_precision.rs`

Run benchmarks:

```bash
cd rust
cargo bench --bench numerical_precision
```

## Related Documentation

- **Precision Guide**: `docs/NUMERICAL_PRECISION.md` - In-depth explanation of numerical issues
- **CI Configuration**: `.github/workflows/precision_tests.yml` - Automated testing setup
- **Benchmarks**: `rust/benches/numerical_precision.rs` - Performance measurements

## Contributing

When adding new indicators:

1. Add corresponding numerical stability tests
2. Test with extreme values (very large, very small, zero)
3. Verify NaN handling
4. Check for division by zero
5. Validate against reference implementation

## Test Metrics

Current test coverage:

- **Total Tests**: 16
- **Test Classes**: 4
- **Indicators Covered**: SMA, EMA, RSI, Bollinger Bands
- **Edge Cases**: 10+

## Maintenance

Review and update these tests when:

- Adding new indicators
- Changing numerical algorithms (e.g., switching to Kahan summation)
- Encountering precision issues in production
- Updating to new Python/Rust versions

---

**Last Updated**: 2025-12-26
**Maintainer**: Haze Team
**Related**: [NUMERICAL_PRECISION.md](../../docs/NUMERICAL_PRECISION.md)
