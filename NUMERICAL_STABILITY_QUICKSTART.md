# Numerical Stability Test Suite - Quick Start Guide

## Run Tests Locally

### Python Tests

```bash
# Run all numerical stability tests
pytest tests/unit/test_numerical_stability.py -v

# Run with coverage
pytest tests/unit/test_numerical_stability.py --cov=haze_library --cov-report=term

# Run specific test class
pytest tests/unit/test_numerical_stability.py::TestNumericalStability -v

# Run single test
pytest tests/unit/test_numerical_stability.py::TestNumericalStability::test_large_numbers_small_increments -v
```

### Rust Benchmarks

```bash
cd rust

# Run all precision benchmarks
cargo bench --bench numerical_precision

# Run specific benchmark
cargo bench --bench numerical_precision -- "sma_large_numbers"

# Generate detailed report
cargo bench --bench numerical_precision -- --verbose
```

## File Locations

```
haze/
├── tests/unit/
│   ├── test_numerical_stability.py              # Main test suite (16 tests)
│   └── NUMERICAL_STABILITY_README.md            # Test documentation
├── rust/benches/
│   └── numerical_precision.rs                   # Rust benchmarks (8 benchmarks)
├── .github/workflows/
│   └── precision_tests.yml                      # CI/CD pipeline
├── docs/
│   └── NUMERICAL_PRECISION.md                   # Comprehensive guide (12KB)
├── NUMERICAL_STABILITY_IMPLEMENTATION_SUMMARY.md # Implementation overview
└── NUMERICAL_STABILITY_QUICKSTART.md            # This file
```

## What Gets Tested

### Critical Edge Cases

✅ **Large Numbers**: 1×10^10 ± 1×10^-5 (precision loss)
✅ **Long Sequences**: 100,000+ data points (error accumulation)
✅ **Extreme Volatility**: 10× price swings (overflow)
✅ **Tiny Values**: ~1×10^-9 (underflow)
✅ **Division by Zero**: Constant prices (Bollinger Bands)
✅ **NaN Handling**: Invalid inputs
✅ **Catastrophic Cancellation**: Balanced gains/losses (RSI)

### Indicators Tested

- **SMA** (Simple Moving Average)
- **EMA** (Exponential Moving Average)
- **RSI** (Relative Strength Index)
- **Bollinger Bands**

## Validation Report

Generate a precision validation report:

```bash
python << 'EOF'
import numpy as np
import haze_library as haze

# Test 1: Large numbers
base = 1e10
data = [base + i * 1e-5 for i in range(10000)]
result = haze.sma(data, period=100)
valid = [r for r in result if not np.isnan(r)]
error = max(abs(r - base) / base for r in valid)
print(f"Large numbers test: {error:.2e} (target: <1e-8)")

# Test 2: Long sequence
data = [100.0 + np.sin(i * 0.01) for i in range(100000)]
result = haze.ema(data, period=20)
print(f"Long sequence test: finite={np.isfinite(result[-1])}")

# Test 3: Extreme volatility
data = [100.0] + [100.0 * (2.0 if i % 2 else 0.5)**i for i in range(1, 1000)]
result = haze.sma(data, period=50)
valid = [r for r in result if not np.isnan(r)]
print(f"Extreme volatility: all_finite={all(np.isfinite(r) for r in valid)}")
EOF
```

## CI/CD Integration

Tests run automatically on:

- ✅ Every commit to main/develop
- ✅ Pull requests
- ✅ Daily at 2 AM UTC (scheduled)
- ✅ Manual trigger via GitHub Actions

View results at: `https://github.com/kwannz/haze/actions/workflows/precision_tests.yml`

## Common Issues & Solutions

### Issue: Tests fail with "module has no attribute"

**Solution**: Rebuild the Rust extension
```bash
cd rust
maturin develop --release --features python
```

### Issue: Benchmarks don't compile

**Solution**: Ensure criterion dependency
```bash
cd rust
cargo update
cargo bench --bench numerical_precision --no-run
```

### Issue: CI/CD fails on specific platform

**Solution**: Check platform-specific precision
- Some tests may need platform-specific tolerances
- Review GitHub Actions logs for details
- Update thresholds if needed

## Expected Test Times

| Test Suite | Data Points | Time |
|------------|-------------|------|
| Small tests | < 100 | < 1ms |
| Medium tests | 10,000 | ~10ms |
| Large tests | 100,000 | ~100ms |
| XL tests | 1,000,000 | ~1s |

**Total suite**: ~5-10 seconds

## Pass Criteria

All tests should pass with:

✅ **No crashes** or exceptions
✅ **Finite results** (no NaN/Inf in valid regions)
✅ **Bounded error** (< specified tolerance)
✅ **Reproducible** (same results on repeated runs)

## Documentation

**Deep Dive**: See `docs/NUMERICAL_PRECISION.md` for:
- Floating-point fundamentals
- Common numerical challenges
- Haze's mitigation strategies
- User best practices
- Academic references

**Test Guide**: See `tests/unit/NUMERICAL_STABILITY_README.md` for:
- Detailed test descriptions
- Running specific tests
- Contributing new tests

**Implementation**: See `NUMERICAL_STABILITY_IMPLEMENTATION_SUMMARY.md` for:
- Technical details
- Validation results
- Performance metrics

## Quick Checks

### Verify Installation

```python
import haze_library as haze
print(f"Haze version: {haze.__version__ if hasattr(haze, '__version__') else 'unknown'}")
print(f"Available: sma={hasattr(haze, 'sma')}, ema={hasattr(haze, 'ema')}")
```

### Basic Precision Test

```python
import numpy as np
import haze_library as haze

# Should handle large numbers
data = [1e10 + i for i in range(100)]
result = haze.sma(data, period=10)
assert all(np.isfinite(r) for r in result if not np.isnan(r))
print("✓ Basic precision test passed")
```

## Contributing

When adding new indicators, ensure:

1. ✅ Add numerical stability tests
2. ✅ Test with extreme values
3. ✅ Verify NaN handling
4. ✅ Check division by zero
5. ✅ Benchmark performance

Example test template:

```python
def test_new_indicator_stability(self):
    """Test NEW_INDICATOR with extreme values."""
    # Large numbers
    data = [1e10 + i * 1e-5 for i in range(10000)]
    result = haze.new_indicator(data, period=100)
    valid = [r for r in result if not np.isnan(r)]
    assert len(valid) > 0, "Should have valid results"
    assert all(np.isfinite(r) for r in valid), "All should be finite"
```

## Support

- **Issues**: https://github.com/kwannz/haze/issues
- **Discussions**: https://github.com/kwannz/haze/discussions
- **Documentation**: `docs/NUMERICAL_PRECISION.md`

---

**Last Updated**: 2025-12-26
**Status**: Production Ready
**Coverage**: 16 tests, 100% pass rate
