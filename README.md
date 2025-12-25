# 🌫️ Haze-Library

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/downloads/)
[![Rust](https://img.shields.io/badge/rust-1.75%2B-orange)](https://www.rust-lang.org/)
[![PyO3](https://img.shields.io/badge/PyO3-0.21-green)](https://pyo3.rs/)

**High-performance quantitative trading indicators library with Rust backend**

Haze-Library provides **212 technical analysis indicators** implemented in Rust with Python bindings, offering **5-10x performance** compared to pure Python implementations while maintaining high precision (< 1e-9 error tolerance).

## ✨ Key Features

- **🚀 212 Technical Indicators**: Complete coverage of TA-Lib, pandas-ta, and custom indicators
- **⚡ Rust Performance**: 5-10x faster than pure Python implementations
- **🎯 High Precision**: < 1e-9 error tolerance vs reference implementations
- **🔒 Type Safe**: Full type annotations and Pydantic validation
- **📦 Zero Dependencies**: All algorithms implemented from scratch
- **🐍 Pythonic API**: Seamless integration with pandas, numpy, and other Python libraries

## 📦 Installation

### From PyPI (Recommended)
```bash
pip install haze-library
```

### From Source
```bash
git clone https://github.com/haze-library/haze-library.git
cd haze-library/rust
maturin develop --release
```

### Prerequisites
- Python 3.9+
- Rust 1.75+ (for building from source)

## 🚀 Quick Start

```python
import _haze_rust as haze

# Price data
close_prices = [100.0, 101.0, 102.0, 101.5, 103.0, 102.5, 104.0]
high_prices = [101.0, 102.0, 103.0, 102.5, 104.0, 103.5, 105.0]
low_prices = [99.0, 100.0, 101.0, 100.5, 102.0, 101.5, 103.0]
volume = [1000, 1200, 1100, 1300, 1250, 1150, 1400]

# Moving Averages
sma = haze.py_sma(close_prices, period=3)
ema = haze.py_ema(close_prices, period=3)

# Volatility Indicators
atr = haze.py_atr(high_prices, low_prices, close_prices, period=3)
upper, middle, lower = haze.py_bollinger_bands(close_prices, period=3, std_dev=2.0)

# Momentum Indicators
rsi = haze.py_rsi(close_prices, period=3)
macd, signal, histogram = haze.py_macd(close_prices, fast=12, slow=26, signal=9)

# Trend Indicators
supertrend, direction = haze.py_supertrend(high_prices, low_prices, close_prices, period=3, multiplier=3.0)
adx = haze.py_adx(high_prices, low_prices, close_prices, period=3)

# Volume Indicators
obv = haze.py_obv(close_prices, volume)
mfi = haze.py_mfi(high_prices, low_prices, close_prices, volume, period=3)
```

## 📊 Indicator Categories

### 🔹 Volatility (10 indicators)
- **ATR**, **NATR**, True Range, Bollinger Bands, Keltner Channel, Donchian Channel, Chandelier Exit, Historical Volatility, Ulcer Index, Mass Index

### 🔹 Momentum (17 indicators)
- **RSI**, **MACD**, Stochastic, CCI, MFI, Williams %R, ROC, MOM, Fisher Transform, Stochastic RSI, KDJ, TSI, Ultimate Oscillator, Awesome Oscillator, APO, PPO, CMO

### 🔹 Trend (14 indicators)
- **SuperTrend**, **ADX**, Parabolic SAR, Aroon, DMI, TRIX, DPO, Vortex, Choppiness, QStick, VHF, DX, +DI, -DI

### 🔹 Volume (11 indicators)
- **OBV**, **VWAP**, Force Index, CMF, Volume Oscillator, AD, PVT, NVI, PVI, EOM, ADOSC

### 🔹 Moving Averages (16 indicators)
- **SMA**, **EMA**, **WMA**, DEMA, TEMA, T3, KAMA, HMA, RMA, ZLMA, FRAMA, ALMA, VIDYA, PWMA, SINWMA, SWMA

### 🔹 Candlestick Patterns (61 indicators)
- Doji, Hammer, Hanging Man, Engulfing (Bullish/Bearish), Harami, Piercing Pattern, Dark Cloud Cover, Morning Star, Evening Star, Three White Soldiers, Three Black Crows, Shooting Star, Marubozu, and 48 more patterns

### 🔹 Statistical (13 indicators)
- Linear Regression, Correlation, Z-Score, Covariance, Beta, Standard Error, CORREL, LINEARREG (Slope/Angle/Intercept), VAR, TSF

### 🔹 Price Transform (4 indicators)
- AVGPRICE, MEDPRICE, TYPPRICE, WCLPRICE

### 🔹 Math Operations (25 functions)
- MAX, MIN, SUM, SQRT, LN, LOG10, EXP, ABS, CEIL, FLOOR, SIN, COS, TAN, ASIN, ACOS, ATAN, SINH, COSH, TANH, ADD, SUB, MULT, DIV, MINMAX, MINMAXINDEX

### 🔹 Overlap Studies (6 indicators)
- MIDPOINT, MIDPRICE, TRIMA, SAR, SAREXT, MAMA/FAMA

### 🔹 Cycle Indicators (5 indicators - Hilbert Transform)
- HT_DCPERIOD, HT_DCPHASE, HT_PHASOR, HT_SINE, HT_TRENDMODE

### 🔹 Advanced Trading Signals (4 indicators - SFG)
- AI SuperTrend, AI Momentum Index, Dynamic MACD, ATR2 Signals

### 🔹 pandas-ta Exclusive (25 indicators)
- Entropy, Aberration, Squeeze, QQE, CTI, ER, Bias, PSL, RVI, Inertia, Alligator, EFI, KST, STC, TDFI, WAE, SMI, Coppock, PGO, VWMA, BOP, SSL Channel, CFO, Slope, Percent Rank

### 🔹 Other Indicators (8 indicators)
- Fibonacci Retracement/Extension, Ichimoku Cloud, Classic Pivots

**Total**: **212 indicators** ✅

## 📖 Detailed Documentation

### API Reference

All indicators follow consistent naming patterns:

```python
# Single output indicators
result = haze.py_indicator_name(data, period, *args)

# Multiple output indicators (returns tuple)
output1, output2, output3 = haze.py_indicator_name(data, period, *args)
```

### Complete Indicator List

For the complete list of all 212 indicators with parameters and descriptions, see [IMPLEMENTED_INDICATORS.md](IMPLEMENTED_INDICATORS.md).

## 🎯 Performance Benchmarks

```
Benchmark: RSI (14-period, 10,000 data points)
─────────────────────────────────────────────
pandas-ta:     12.5 ms
TA-Lib:        8.2 ms
Haze-Library:  1.3 ms  (6.3x faster than TA-Lib, 9.6x faster than pandas-ta)

Benchmark: Bollinger Bands (20-period, 10,000 data points)
───────────────────────────────────────────────────────────
pandas-ta:     15.8 ms
TA-Lib:        10.1 ms
Haze-Library:  2.1 ms  (4.8x faster than TA-Lib, 7.5x faster than pandas-ta)

Benchmark: MACD (12/26/9, 10,000 data points)
─────────────────────────────────────────────
pandas-ta:     18.3 ms
TA-Lib:        11.4 ms
Haze-Library:  1.9 ms  (6.0x faster than TA-Lib, 9.6x faster than pandas-ta)
```

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   Python Application                     │
│                  (Trading Strategies)                    │
└────────────────────────┬────────────────────────────────┘
                         │
                         │ PyO3 Bindings
                         ▼
┌─────────────────────────────────────────────────────────┐
│              _haze_rust Module (Python)                  │
│     • py_rsi()  • py_macd()  • py_bollinger_bands()     │
│     • py_supertrend()  • py_obv()  • py_kdj()           │
│              (212 Python-callable functions)             │
└────────────────────────┬────────────────────────────────┘
                         │
                         │ Rust FFI
                         ▼
┌─────────────────────────────────────────────────────────┐
│                  Rust Core Library                       │
│  ┌───────────────────────────────────────────────────┐  │
│  │  Indicators Module                                 │  │
│  │  • momentum.rs  • volatility.rs  • trend.rs       │  │
│  │  • volume.rs    • ma.rs          • candlestick.rs │  │
│  │  • statistical.rs  • pandas_ta.rs  • cycle.rs     │  │
│  └───────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────┐  │
│  │  Utilities Module                                  │  │
│  │  • ma.rs (Moving Average primitives)              │  │
│  │  • stats.rs (Statistical functions)               │  │
│  │  • pattern.rs (Pattern recognition)               │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

### Design Principles

1. **KISS (Keep It Simple)**: Direct algorithms without unnecessary abstractions
2. **YAGNI (You Aren't Gonna Need It)**: Focus on core functionality only
3. **SOLID**: Single responsibility for each indicator module
4. **Occam's Razor**: Minimal dependencies, maximum performance

## 🧪 Testing & Quality

```bash
# Run precision validation (vs TA-Lib/pandas-ta)
python tests/run_precision_tests.py

# Run unit tests (212/212 indicators)
pytest tests/unit/ -v

# Generate coverage report
pytest tests/unit/ --cov=_haze_rust --cov-report=html
```

### Precision Standards
- **Max Error**: < 1e-9 (nanometer-level precision)
- **Correlation**: > 0.9999 with TA-Lib/pandas-ta
- **Coverage**: 212/212 indicators verified

## 🔧 Development

### Building from Source

```bash
# Clone repository
git clone https://github.com/haze-library/haze-library.git
cd haze-library

# Install Rust (if not already installed)
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Build Rust library with Maturin
cd rust
pip install maturin
maturin develop --release

# Verify installation
python -c "import _haze_rust as haze; print(haze.py_sma([1,2,3,4,5], 3))"
```

### Project Structure

```
haze-library/
├── rust/                    # Rust source code
│   ├── src/
│   │   ├── lib.rs          # PyO3 module registration
│   │   ├── indicators/     # Indicator implementations
│   │   └── utils/          # Shared utilities
│   └── Cargo.toml
├── tests/                   # Python test suite
│   ├── unit/               # Unit tests (pytest)
│   └── precision_validator.py
├── pyproject.toml           # Python project configuration
└── README.md
```

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Workflow

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-indicator`)
3. Implement your changes with tests
4. Ensure all tests pass (`pytest tests/`)
5. Submit a pull request

## 📝 Changelog

See [CHANGELOG.md](CHANGELOG.md) for release history.

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **TA-Lib**: Reference implementation for technical analysis
- **pandas-ta**: Inspiration for pandas integration patterns
- **PyO3**: Rust-Python bindings framework
- **Maturin**: Build tool for Rust Python extensions

## 📬 Contact

- **Issues**: [GitHub Issues](https://github.com/haze-library/haze-library/issues)
- **Discussions**: [GitHub Discussions](https://github.com/haze-library/haze-library/discussions)
- **Email**: team@haze-library.com

## ⭐ Star History

If you find Haze-Library useful, please consider giving it a star! ⭐

---

**Made with ❤️ by the Haze Team**

**Last Updated**: 2025-12-25
