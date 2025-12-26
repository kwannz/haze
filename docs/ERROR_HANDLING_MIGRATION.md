# Error Handling Migration Guide

**Version**: 1.0
**Date**: 2025-12-26
**Status**: Current implementation - No breaking changes

## Overview

This document describes the error handling strategy in Haze-Library and provides guidance for users working with the library. **Note: The current implementation already includes proper error handling - this is a documentation update, not a breaking change.**

## Current Error Handling Architecture

### Rust Layer (Internal)

The Rust core uses a unified error handling approach:

```rust
// Error types defined in errors.rs
pub enum HazeError {
    InsufficientData { required: usize, actual: usize },
    InvalidPeriod { period: usize, data_len: usize },
    LengthMismatch { name1: &'static str, len1: usize, name2: &'static str, len2: usize },
    InvalidValue { index: usize, message: String },
    EmptyInput { name: &'static str },
    ParameterOutOfRange { name: &'static str, value: f64, min: f64, max: f64 },
    ModelError(String),
    IoError(#[from] std::io::Error),
}

pub type HazeResult<T> = Result<T, HazeError>;
```

### Python Layer (API)

All errors from Rust are automatically converted to Python `ValueError` via PyO3:

```rust
// Automatic conversion in errors.rs
impl From<HazeError> for PyErr {
    fn from(err: HazeError) -> PyErr {
        PyValueError::new_err(err.to_string())
    }
}
```

This means all indicator functions in Python can raise `ValueError` with descriptive error messages.

## Error Handling Patterns

### When Errors Are Raised

Haze-Library raises `ValueError` in the following situations:

1. **Invalid Period**
   - Period is 0
   - Period is larger than the data length
   - Example: `haze.py_rsi([100, 101, 102], period=14)`

2. **Mismatched Array Lengths**
   - When multi-array indicators receive arrays of different lengths
   - Example: `haze.py_atr(high=[101, 102], low=[99], close=[100, 101], period=2)`

3. **Empty Input**
   - When empty arrays are provided
   - Example: `haze.py_rsi([], period=14)`

4. **Parameter Out of Range**
   - When parameters exceed valid ranges
   - Example: `haze.py_bollinger_bands(prices, period=20, std_dev=-1.0)`

5. **Insufficient Data**
   - When data length is less than required minimum
   - Example: Some indicators need minimum data points for calculation

### When NaN is Returned (Not an Error)

Some values are `NaN` by design - this is **not an error**:

1. **Warmup Period**
   - The first `period - 1` values are NaN because there's insufficient historical data
   - Example: RSI(14) will have NaN for the first 13 values
   - **This is expected behavior**, not an error

2. **Division by Zero in Calculations**
   - When denominator becomes zero in valid calculations
   - Example: Some oscillators may have NaN during flat markets
   - **This is valid mathematical behavior**, not an error

## Migration Guide

### No Code Changes Required

**Good news**: If your code already handles standard Python exceptions, no changes are needed. The error handling has been in place since the beginning.

### Recommended Best Practices

#### 1. Basic Error Handling

```python
import haze_library as haze

try:
    rsi = haze.py_rsi(prices, period=14)
except ValueError as e:
    print(f"Failed to calculate RSI: {e}")
    # Handle error appropriately
```

#### 2. Validate Before Calling

```python
def calculate_indicator_safe(prices, period=14):
    """Calculate indicator with validation."""
    # Pre-validate inputs
    if not prices:
        print("Error: Empty price data")
        return None

    if period > len(prices):
        print(f"Warning: Adjusting period from {period} to {len(prices)}")
        period = len(prices)

    try:
        return haze.py_rsi(prices, period=period)
    except ValueError as e:
        print(f"Error: {e}")
        return None
```

#### 3. Defensive Programming

```python
def safe_calculate_indicators(df):
    """Calculate multiple indicators with error handling."""
    indicators = {}

    # RSI
    try:
        indicators['rsi'] = haze.py_rsi(df['close'].tolist(), period=14)
    except ValueError as e:
        print(f"RSI calculation failed: {e}")
        indicators['rsi'] = [float('nan')] * len(df)

    # MACD
    try:
        macd, signal, hist = haze.py_macd(
            df['close'].tolist(),
            fast=12,
            slow=26,
            signal=9
        )
        indicators['macd'] = macd
        indicators['macd_signal'] = signal
        indicators['macd_hist'] = hist
    except ValueError as e:
        print(f"MACD calculation failed: {e}")
        nan_array = [float('nan')] * len(df)
        indicators['macd'] = nan_array
        indicators['macd_signal'] = nan_array
        indicators['macd_hist'] = nan_array

    return indicators
```

#### 4. Real-time Streaming Error Handling

```python
from haze_library.streaming import IncrementalRSI

rsi_calc = IncrementalRSI(period=14)

for price in price_stream:
    try:
        rsi_value = rsi_calc.update(price)

        if rsi_calc.is_ready:
            print(f"RSI: {rsi_value:.2f}")
        else:
            print(f"Warming up: {rsi_calc.count}/14")

    except ValueError as e:
        print(f"Error updating RSI: {e}")
        continue  # Skip this price and continue
```

## Error Messages Reference

### Common Error Messages

| Error Message | Cause | Solution |
|--------------|-------|----------|
| `Invalid period: X (must be > 0 and <= data length Y)` | Period parameter is invalid | Use period between 1 and data length |
| `Length mismatch: high=X, low=Y` | Array lengths don't match | Ensure all OHLC arrays have same length |
| `Empty input: close cannot be empty` | Input array is empty | Provide non-empty data |
| `Insufficient data: need at least X elements, got Y` | Not enough data points | Provide more data or reduce period |
| `Parameter alpha out of range: X (valid range: 0.0..1.0)` | Parameter outside valid range | Adjust parameter to valid range |

### Interpreting Error Messages

All error messages follow a descriptive format:

```
<Error Type>: <Details>
```

Example:
```
Invalid period: 100 (must be > 0 and <= data length 50)
         ^       ^                                   ^
    Error Type   Invalid Value              Valid Range/Context
```

## Testing Your Error Handling

Use these test cases to verify your error handling:

```python
import haze_library as haze

# Test 1: Empty input
try:
    haze.py_rsi([], period=14)
    print("❌ Should have raised ValueError")
except ValueError:
    print("✅ Empty input handled correctly")

# Test 2: Invalid period
try:
    haze.py_rsi([100, 101, 102], period=14)
    print("❌ Should have raised ValueError")
except ValueError:
    print("✅ Invalid period handled correctly")

# Test 3: Mismatched lengths
try:
    haze.py_atr([101, 102], [99], [100, 101], period=2)
    print("❌ Should have raised ValueError")
except ValueError:
    print("✅ Length mismatch handled correctly")

# Test 4: Valid input (should succeed)
try:
    result = haze.py_rsi([100, 101, 102, 103, 104, 105], period=3)
    print("✅ Valid input processed correctly")
except ValueError as e:
    print(f"❌ Unexpected error: {e}")
```

## FAQ

### Q: Do I need to update my code?

**A:** No, if you're already using try-except blocks for exceptions. The error handling has been consistent since the initial release.

### Q: What changed in this update?

**A:** Only documentation. We added comprehensive error handling examples and best practices to the README and examples. The underlying behavior is unchanged.

### Q: Why do I see NaN in my results?

**A:** NaN values are expected during the "warmup period" (first `period - 1` values) and in certain edge cases during calculation. This is **not an error** - it's the correct mathematical behavior. Errors that indicate invalid input raise `ValueError` instead.

### Q: Can I disable error checking for performance?

**A:** No. Error checking is essential for data integrity and happens at the Rust level with minimal overhead. The performance impact is negligible compared to the calculation itself.

### Q: What if I want different error behavior?

**A:** You can wrap the library functions with your own error handling:

```python
def my_rsi(prices, period=14, default=None):
    """RSI wrapper that returns default on error."""
    try:
        return haze.py_rsi(prices, period=period)
    except ValueError:
        return default if default is not None else [float('nan')] * len(prices)
```

### Q: Are there any breaking changes?

**A:** No. This is a documentation update only. All existing code continues to work as before.

## Additional Resources

- **README.md**: Quick start guide with error handling examples
- **examples/ccxt_realtime_demo.py**: Real-world error handling patterns
- **src/errors.rs**: Complete error type definitions (Rust)
- **API_REFERENCE.md**: Detailed API documentation

## Support

If you encounter error messages not covered in this guide, please:

1. Check the error message details - they are designed to be self-explanatory
2. Verify your input data meets the requirements
3. Consult the API reference for parameter constraints
4. Open an issue on GitHub if you believe the error is incorrect

---

**Last Updated**: 2025-12-26
**Applies to**: Haze-Library v1.0+
