# Haze-Library

High-performance quantitative trading indicators library with Rust backend.

## Features

- **30+ Technical Indicators**: ATR, RSI, MACD, Bollinger Bands, SuperTrend, ADX, etc.
- **Rust Core**: 5-10x faster than pure Python implementations
- **Zero Dependencies**: All algorithms implemented from scratch
- **Type Safe**: Full type annotations and validation

## Installation

```bash
pip install haze-library
```

## Quick Start

```python
import _haze_rust as haze

# Calculate RSI
close_prices = [100.0, 101.0, 102.0, ...]
rsi = haze.py_rsi(close_prices, period=14)

# Calculate MACD
macd, signal, histogram = haze.py_macd(close_prices)

# Calculate Bollinger Bands
upper, middle, lower = haze.py_bollinger_bands(close_prices, period=20, std_multiplier=2.0)
```

## Indicators

### Volatility
- ATR, NATR, True Range
- Bollinger Bands
- Keltner Channel
- Donchian Channel

### Momentum
- RSI, StochRSI
- MACD
- Stochastic Oscillator
- CCI, Williams %R
- Fisher Transform
- Awesome Oscillator

### Trend
- SuperTrend
- ADX
- Aroon
- Parabolic SAR

### Volume
- OBV, VWAP
- MFI, CMF
- Volume Profile

### Moving Averages
- SMA, EMA, WMA, RMA
- HMA, DEMA, TEMA

## License

MIT
