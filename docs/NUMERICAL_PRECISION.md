# Numerical Precision in Haze

## Overview

This document explains the numerical precision considerations in Haze indicators, the challenges of floating-point arithmetic, and best practices for maintaining accuracy in quantitative trading calculations.

## Table of Contents

1. [Floating-Point Precision Fundamentals](#floating-point-precision-fundamentals)
2. [Common Numerical Challenges](#common-numerical-challenges)
3. [Haze's Mitigation Strategies](#hazes-mitigation-strategies)
4. [User Best Practices](#user-best-practices)
5. [Testing and Validation](#testing-and-validation)

---

## Floating-Point Precision Fundamentals

### IEEE 754 Double Precision (f64)

Haze uses IEEE 754 double-precision floating-point numbers (`f64` in Rust, `float` in Python):

- **Precision**: ~15-17 decimal digits
- **Range**: ±1.7 × 10^308
- **Epsilon**: ~2.22 × 10^-16 (smallest distinguishable difference)

### Key Limitations

1. **Representational Error**: Most decimal numbers cannot be exactly represented
   ```python
   # Example: 0.1 + 0.2 ≠ 0.3 in binary floating-point
   >>> 0.1 + 0.2
   0.30000000000000004
   ```

2. **Rounding Error**: Accumulates through arithmetic operations
   ```python
   # Summing many small numbers can lose precision
   >>> sum([0.1] * 10) == 1.0
   False
   ```

3. **Catastrophic Cancellation**: Subtracting nearly equal numbers loses precision
   ```python
   # Example: (a - b) when a ≈ b
   >>> a = 1.0000000001
   >>> b = 1.0000000000
   >>> (a - b) * 1e10  # Magnified error
   ```

---

## Common Numerical Challenges

### 1. Large Numbers + Small Increments

**Problem**: Adding small changes to large base values loses precision.

```python
base = 1e10  # 10 billion
increment = 1e-5  # 0.00001

# After many increments, precision is lost
result = base
for _ in range(10000):
    result += increment

# Expected: 1e10 + 0.1 = 10000000000.1
# Actual: May differ due to rounding
```

**Impact on Trading**:
- High-priced assets (e.g., Bitcoin at $40,000) with small percentage moves
- Accumulating returns over long periods

**Haze Solution**:
- Kahan summation algorithm for SMA calculations
- Compensated arithmetic to track and correct rounding errors

### 2. Catastrophic Cancellation

**Problem**: Subtracting nearly equal values amplifies relative error.

```python
# RSI calculation involves (average_gain - average_loss)
# When gains ≈ losses, precision is lost
gains = [0.01, 0.01, 0.01]  # 1% gains
losses = [0.01, 0.01, 0.01]  # 1% losses

avg_gain = sum(gains) / len(gains)
avg_loss = sum(losses) / len(losses)

# This subtraction loses precision
rs = avg_gain / avg_loss  # Should be exactly 1.0
```

**Impact on Trading**:
- RSI near 50 (balanced market)
- Momentum indicators with small net changes
- Mean reversion signals

**Haze Solution**:
- Separate tracking of positive and negative changes
- Avoid intermediate subtractions when possible
- Use ratios instead of differences where applicable

### 3. Precision Loss in Long Sequences

**Problem**: Errors accumulate over iterations.

```python
# EMA calculation: recursive formula
# ema[i] = α * price[i] + (1-α) * ema[i-1]

# After 100,000 iterations, rounding errors accumulate
data = [100 + np.sin(i * 0.01) for i in range(100000)]
ema_result = calculate_ema(data, period=20)
```

**Impact on Trading**:
- Long-running backtests (years of daily data)
- High-frequency data (millions of ticks)
- Cumulative return calculations

**Haze Solution**:
- Periodic renormalization in iterative algorithms
- Use of higher-precision intermediate calculations
- Validation against reference implementations

### 4. Division by Zero and Near-Zero

**Problem**: Standard deviation can be zero for constant prices.

```python
# Bollinger Bands with constant price
prices = [100.0] * 50  # No volatility

std_dev = np.std(prices)  # Returns 0.0
upper_band = sma + 2 * std_dev  # Fine
width = (upper_band - lower_band) / sma  # Division by zero if we're not careful
```

**Impact on Trading**:
- Low-volatility markets (e.g., stablecoins)
- After-hours trading with few transactions
- Indicators that normalize by volatility

**Haze Solution**:
- Explicit zero checks before division
- Return NaN or meaningful defaults (e.g., bands collapse to SMA)
- Configurable epsilon thresholds

---

## Haze's Mitigation Strategies

### 1. Kahan Summation Algorithm

For simple moving averages and similar calculations:

```rust
fn kahan_sum(values: &[f64]) -> f64 {
    let mut sum = 0.0;
    let mut compensation = 0.0;

    for &value in values {
        let y = value - compensation;
        let t = sum + y;
        compensation = (t - sum) - y;
        sum = t;
    }

    sum
}
```

**Benefits**:
- Reduces rounding error accumulation
- Maintains precision for large datasets
- Minimal performance overhead (~10-20% slower)

**When Applied**:
- SMA, WMA calculations
- Cumulative summations in OBV, ADL
- Any operation summing many values

### 2. Welford's Online Algorithm

For variance and standard deviation:

```rust
// Updates mean and variance in single pass
// Avoids catastrophic cancellation in var = E[X²] - E[X]²
struct WelfordAccumulator {
    count: usize,
    mean: f64,
    m2: f64,  // Sum of squared differences from mean
}
```

**Benefits**:
- Numerically stable variance calculation
- Single-pass algorithm (memory efficient)
- No catastrophic cancellation

**When Applied**:
- Bollinger Bands
- Standard Deviation
- Z-score calculations

### 3. Safe Division with Epsilon

```rust
const EPSILON: f64 = 1e-10;

fn safe_divide(numerator: f64, denominator: f64) -> f64 {
    if denominator.abs() < EPSILON {
        return f64::NAN;
    }
    numerator / denominator
}
```

**Benefits**:
- Prevents division by zero
- Returns NaN for undefined operations
- Configurable threshold

**When Applied**:
- RSI calculation (RS = avg_gain / avg_loss)
- Normalized indicators
- Ratio calculations

### 4. Interval-Based Recalculation

For long sequences, periodically reset calculations:

```rust
// For EMA, reset every N points to prevent drift
const RESET_INTERVAL: usize = 100_000;

if index % RESET_INTERVAL == 0 {
    // Recalculate from last reliable value
    ema = recalculate_ema_from_checkpoint();
}
```

**Benefits**:
- Bounds error accumulation
- Maintains long-term accuracy
- Minimal impact on results

---

## User Best Practices

### 1. Data Preprocessing

**Normalize High-Priced Assets**:
```python
# Instead of using raw BTC prices ($40,000)
prices = [40000, 40100, 40050, ...]

# Normalize to reasonable range
normalized = [p / 1000 for p in prices]  # $40-$50 range
result = haze.sma(normalized, period=20)
# Scale back if needed
result = [r * 1000 for r in result]
```

**Use Returns Instead of Prices**:
```python
# Better for long-term analysis
returns = [(p2 - p1) / p1 for p1, p2 in zip(prices[:-1], prices[1:])]
sma_returns = haze.sma(returns, period=20)
```

### 2. Choose Appropriate Periods

**Avoid Extreme Period Values**:
```python
# Too short: noisy, but precise
sma_5 = haze.sma(data, period=5)

# Too long: smooth, but accumulates error
sma_1000 = haze.sma(data, period=1000)  # May drift

# Recommended: 10-200 for most applications
sma_50 = haze.sma(data, period=50)
```

### 3. Validate Critical Calculations

**Cross-Check with Reference Implementations**:
```python
import haze_library as haze
import talib
import numpy as np

# Your critical calculation
haze_result = haze.sma(data, period=20)

# Validate against known library
talib_result = talib.SMA(np.array(data), timeperiod=20)

# Check agreement within tolerance
max_diff = np.nanmax(np.abs(haze_result - talib_result))
assert max_diff < 1e-6, f"Large discrepancy: {max_diff}"
```

### 4. Handle NaN Values Properly

**Don't Silently Drop NaNs**:
```python
# Bad: Silently removes data
clean_data = [x for x in data if not np.isnan(x)]

# Good: Understand why NaNs exist
if any(np.isnan(x) for x in data):
    print("Warning: Input contains NaN values")
    # Decide on strategy: forward-fill, drop, or interpolate

# Haze handles NaNs gracefully
result = haze.sma(data, period=20)  # Returns NaN for invalid positions
```

### 5. Monitor Precision in Production

**Add Sanity Checks**:
```python
def validate_indicator(result, expected_range):
    """Ensure indicator output is reasonable"""
    valid = [r for r in result if np.isfinite(r)]

    if not valid:
        raise ValueError("No valid indicator values")

    min_val, max_val = min(valid), max(valid)

    if not (expected_range[0] <= min_val <= expected_range[1]):
        raise ValueError(f"Min value {min_val} out of range")

    if not (expected_range[0] <= max_val <= expected_range[1]):
        raise ValueError(f"Max value {max_val} out of range")

# Example
rsi = haze.rsi(data, period=14)
validate_indicator(rsi, expected_range=(0, 100))
```

---

## Testing and Validation

### Automated Test Suite

Haze includes comprehensive numerical stability tests:

```bash
# Run Python precision tests
pytest tests/unit/test_numerical_stability.py -v

# Run Rust benchmarks
cd rust
cargo bench --bench numerical_precision
```

### Test Coverage

1. **Large Numbers + Small Increments**
   - Base: 1×10^10, Increments: ±1×10^-5
   - Validates relative error < 1×10^-8

2. **Catastrophic Cancellation**
   - Balanced gains/losses
   - RSI should remain near 50 ± 5

3. **Long Sequences**
   - 100,000 data points
   - Compares with NumPy reference

4. **NaN Propagation**
   - Mixed valid/NaN input
   - Ensures partial results remain valid

5. **Division by Zero**
   - Constant prices (zero variance)
   - Verifies safe fallback behavior

6. **Extreme Volatility**
   - Price swings up to 10×
   - Checks for overflow/underflow

### Continuous Integration

GitHub Actions automatically:
- Runs precision tests on every commit
- Compares benchmark results (alerts on >50% regression)
- Generates precision reports
- Validates against thresholds

---

## References

### Academic Papers

1. Goldberg, D. (1991). "What Every Computer Scientist Should Know About Floating-Point Arithmetic"
2. Kahan, W. (1965). "Further Remarks on Reducing Truncation Errors"
3. Welford, B.P. (1962). "Note on a Method for Calculating Corrected Sums of Squares and Products"

### Standards

- IEEE 754-2008: IEEE Standard for Floating-Point Arithmetic

### Tools

- `tests/unit/test_numerical_stability.py`: Python test suite
- `rust/benches/numerical_precision.rs`: Rust benchmarks
- `.github/workflows/precision_tests.yml`: CI/CD pipeline

---

## FAQ

### Q: Why don't my indicators match exactly between Haze and other libraries?

**A**: Small differences (< 1×10^-6) are expected due to:
- Different summation algorithms (Kahan vs naive)
- Compiler optimizations
- Order of operations

Differences > 1×10^-4 may indicate a bug—please report.

### Q: Can I use Haze for high-frequency trading (millions of data points)?

**A**: Yes, but consider:
- Batch processing (process in chunks of 100k)
- Periodic checkpointing for long-running calculations
- Monitor precision with validation suite

### Q: What if I need more precision than f64?

**A**: For extreme cases, consider:
1. **Preprocessing**: Normalize data to avoid extreme values
2. **Custom Types**: Rust supports `f128` (software emulation)
3. **Decimal Libraries**: Use `rust_decimal` for financial precision
4. **Alternative Formulation**: Sometimes a different algorithm avoids the precision issue

### Q: How do I know if my results are affected by precision issues?

**A**: Warning signs:
- Results drift over long sequences
- Indicators don't match reference implementations
- Unexpected NaN or Inf values
- Results change significantly with minor input changes

**Action**: Run `pytest tests/unit/test_numerical_stability.py` on your data

---

## Contributing

Found a precision issue? Please:

1. Create a minimal reproducible example
2. Include input data and expected output
3. Run the precision test suite
4. Open an issue with test case

See [CONTRIBUTING.md](../CONTRIBUTING.md) for details.

---

**Last Updated**: 2025-12-26
**Maintainer**: Haze Team
**License**: CC-BY-NC-4.0
