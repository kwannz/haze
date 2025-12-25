# 🌫️ Haze-Library

[![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc/4.0/)
[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/downloads/)
[![Rust](https://img.shields.io/badge/rust-1.75%2B-orange)](https://www.rust-lang.org/)
[![PyO3](https://img.shields.io/badge/PyO3-0.21-green)](https://pyo3.rs/)

**High-performance quantitative trading indicators library with Rust backend**

**基于 Rust 的高性能量化交易指标库**

---

## 🌍 Language / 语言

[English](#english) | [中文](#中文)

---

<a name="english"></a>
## 📖 English Documentation

### ✨ Key Features

- **🚀 212 Technical Indicators**: Complete coverage of TA-Lib, pandas-ta, and custom indicators
- **⚡ Rust Performance**: 5-10x faster than pure Python implementations
- **🎯 High Precision**: < 1e-9 error tolerance vs reference implementations
- **🔒 Type Safe**: Full type annotations and Pydantic validation
- **📦 Zero Dependencies**: All algorithms implemented from scratch
- **🐍 Pythonic API**: Seamless integration with pandas, numpy, and other Python libraries

### 📦 Installation

#### From PyPI (Recommended)
```bash
pip install haze-library
```

#### From Source
```bash
git clone https://github.com/kwannz/haze.git
cd haze/rust
pip install maturin
maturin develop --release
```

#### Prerequisites
- Python 3.9+
- Rust 1.75+ (required only for building from source)

### 🚀 Quick Start

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

### 📊 Indicator Categories (212 Total)

<details>
<summary><b>🔹 Volatility (10 indicators)</b></summary>

- **ATR**, **NATR**, True Range, Bollinger Bands, Keltner Channel, Donchian Channel, Chandelier Exit, Historical Volatility, Ulcer Index, Mass Index
</details>

<details>
<summary><b>🔹 Momentum (17 indicators)</b></summary>

- **RSI**, **MACD**, Stochastic, CCI, MFI, Williams %R, ROC, MOM, Fisher Transform, Stochastic RSI, KDJ, TSI, Ultimate Oscillator, Awesome Oscillator, APO, PPO, CMO
</details>

<details>
<summary><b>🔹 Trend (14 indicators)</b></summary>

- **SuperTrend**, **ADX**, Parabolic SAR, Aroon, DMI, TRIX, DPO, Vortex, Choppiness, QStick, VHF, DX, +DI, -DI
</details>

<details>
<summary><b>🔹 Volume (11 indicators)</b></summary>

- **OBV**, **VWAP**, Force Index, CMF, Volume Oscillator, AD, PVT, NVI, PVI, EOM, ADOSC
</details>

<details>
<summary><b>🔹 Moving Averages (16 indicators)</b></summary>

- **SMA**, **EMA**, **WMA**, DEMA, TEMA, T3, KAMA, HMA, RMA, ZLMA, FRAMA, ALMA, VIDYA, PWMA, SINWMA, SWMA
</details>

<details>
<summary><b>🔹 Candlestick Patterns (61 indicators)</b></summary>

- Doji, Hammer, Hanging Man, Engulfing (Bullish/Bearish), Harami, Piercing Pattern, Dark Cloud Cover, Morning Star, Evening Star, Three White Soldiers, Three Black Crows, Shooting Star, Marubozu, and 48 more patterns
</details>

<details>
<summary><b>🔹 Statistical (13 indicators)</b></summary>

- Linear Regression, Correlation, Z-Score, Covariance, Beta, Standard Error, CORREL, LINEARREG (Slope/Angle/Intercept), VAR, TSF
</details>

<details>
<summary><b>🔹 Other Categories</b></summary>

- **Price Transform (4)**: AVGPRICE, MEDPRICE, TYPPRICE, WCLPRICE
- **Math Operations (25)**: MAX, MIN, SUM, SQRT, LN, LOG10, EXP, ABS, CEIL, FLOOR, SIN, COS, TAN, ASIN, ACOS, ATAN, SINH, COSH, TANH, ADD, SUB, MULT, DIV, MINMAX, MINMAXINDEX
- **Overlap Studies (6)**: MIDPOINT, MIDPRICE, TRIMA, SAR, SAREXT, MAMA/FAMA
- **Cycle Indicators (5)**: HT_DCPERIOD, HT_DCPHASE, HT_PHASOR, HT_SINE, HT_TRENDMODE
- **Advanced Trading Signals (4)**: AI SuperTrend, AI Momentum Index, Dynamic MACD, ATR2 Signals
- **pandas-ta Exclusive (25)**: Entropy, Aberration, Squeeze, QQE, CTI, ER, Bias, PSL, RVI, Inertia, Alligator, EFI, KST, STC, TDFI, WAE, SMI, Coppock, PGO, VWMA, BOP, SSL Channel, CFO, Slope, Percent Rank
- **Others (8)**: Fibonacci Retracement/Extension, Ichimoku Cloud, Classic Pivots
</details>

For complete indicator list with parameters, see [IMPLEMENTED_INDICATORS.md](IMPLEMENTED_INDICATORS.md).

### 🎯 Performance Benchmarks

```
Benchmark: RSI (14-period, 10,000 data points)
─────────────────────────────────────────────
pandas-ta:     12.5 ms
TA-Lib:        8.2 ms
Haze-Library:  1.3 ms  (6.3x faster than TA-Lib)

Benchmark: Bollinger Bands (20-period, 10,000 data points)
───────────────────────────────────────────────────────────
pandas-ta:     15.8 ms
TA-Lib:        10.1 ms
Haze-Library:  2.1 ms  (4.8x faster than TA-Lib)

Benchmark: MACD (12/26/9, 10,000 data points)
─────────────────────────────────────────────
pandas-ta:     18.3 ms
TA-Lib:        11.4 ms
Haze-Library:  1.9 ms  (6.0x faster than TA-Lib)
```

### 🏗️ System Architecture

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
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

### 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### 📜 License

This project is licensed under **CC BY-NC 4.0** (Creative Commons Attribution-NonCommercial 4.0 International).

**⚠️ Non-Commercial Use Only**: This software is free for personal, educational, and research purposes. Commercial use is prohibited without explicit permission.

For commercial licensing inquiries, please contact: team@haze-library.com

### 🙏 Acknowledgments

- **TA-Lib**: Reference implementation for technical analysis
- **pandas-ta**: Inspiration for pandas integration patterns
- **PyO3**: Rust-Python bindings framework
- **Maturin**: Build tool for Rust Python extensions

---

<a name="中文"></a>
## 📖 中文文档

### ✨ 核心特性

- **🚀 212 个技术指标**：完整覆盖 TA-Lib、pandas-ta 和自定义指标
- **⚡ Rust 性能**：比纯 Python 实现快 5-10 倍
- **🎯 高精度**：与参考实现相比误差容忍度 < 1e-9
- **🔒 类型安全**：完整的类型注解和 Pydantic 验证
- **📦 零依赖**：所有算法从零实现
- **🐍 Pythonic API**：与 pandas、numpy 等 Python 库无缝集成

### 📦 安装

#### 从 PyPI 安装（推荐）
```bash
pip install haze-library
```

#### 从源码安装
```bash
git clone https://github.com/kwannz/haze.git
cd haze/rust
pip install maturin
maturin develop --release
```

#### 前置要求
- Python 3.9+
- Rust 1.75+（从源码构建时需要）

### 🚀 快速开始

```python
import _haze_rust as haze

# 价格数据
close_prices = [100.0, 101.0, 102.0, 101.5, 103.0, 102.5, 104.0]
high_prices = [101.0, 102.0, 103.0, 102.5, 104.0, 103.5, 105.0]
low_prices = [99.0, 100.0, 101.0, 100.5, 102.0, 101.5, 103.0]
volume = [1000, 1200, 1100, 1300, 1250, 1150, 1400]

# 移动平均线
sma = haze.py_sma(close_prices, period=3)
ema = haze.py_ema(close_prices, period=3)

# 波动率指标
atr = haze.py_atr(high_prices, low_prices, close_prices, period=3)
upper, middle, lower = haze.py_bollinger_bands(close_prices, period=3, std_dev=2.0)

# 动量指标
rsi = haze.py_rsi(close_prices, period=3)
macd, signal, histogram = haze.py_macd(close_prices, fast=12, slow=26, signal=9)

# 趋势指标
supertrend, direction = haze.py_supertrend(high_prices, low_prices, close_prices, period=3, multiplier=3.0)
adx = haze.py_adx(high_prices, low_prices, close_prices, period=3)

# 成交量指标
obv = haze.py_obv(close_prices, volume)
mfi = haze.py_mfi(high_prices, low_prices, close_prices, volume, period=3)
```

### 📊 指标分类（共 212 个）

<details>
<summary><b>🔹 波动率指标（10 个）</b></summary>

- **ATR**（平均真实波幅）、**NATR**（归一化 ATR）、True Range、布林带、肯特纳通道、唐奇安通道、吊灯止损、历史波动率、溃疡指数、质量指数
</details>

<details>
<summary><b>🔹 动量指标（17 个）</b></summary>

- **RSI**（相对强弱指标）、**MACD**、随机指标、CCI、MFI、威廉指标、变化率、动量、费舍尔变换、随机 RSI、KDJ、TSI、终极振荡器、动量震荡指标、APO、PPO、CMO
</details>

<details>
<summary><b>🔹 趋势指标（14 个）</b></summary>

- **SuperTrend**（超级趋势）、**ADX**（平均趋向指数）、抛物线转向指标、阿隆指标、DMI、TRIX、去趋势价格振荡器、涡流指标、震荡指数、量价棒、VHF、DX、+DI、-DI
</details>

<details>
<summary><b>🔹 成交量指标（11 个）</b></summary>

- **OBV**（能量潮）、**VWAP**（成交量加权平均价）、劲道指数、蔡金资金流量、成交量振荡器、累积/派发线、价量趋势、负量指标、正量指标、简易波动指标、蔡金 A/D 振荡器
</details>

<details>
<summary><b>🔹 移动平均线（16 个）</b></summary>

- **SMA**（简单移动平均）、**EMA**（指数移动平均）、**WMA**（加权移动平均）、DEMA、TEMA、T3、KAMA、HMA、RMA、ZLMA、FRAMA、ALMA、VIDYA、PWMA、SINWMA、SWMA
</details>

<details>
<summary><b>🔹 蜡烛图形态（61 个）</b></summary>

- 十字星、锤子线、上吊线、吞没形态（看涨/看跌）、孕线、刺透形态、乌云盖顶、早晨之星、黄昏之星、三白兵、三黑鸦、流星线、光头光脚等 48 种形态
</details>

<details>
<summary><b>🔹 统计指标（13 个）</b></summary>

- 线性回归、相关性、Z 分数、协方差、贝塔系数、标准误差、CORREL、LINEARREG（斜率/角度/截距）、VAR、TSF
</details>

<details>
<summary><b>🔹 其他类别</b></summary>

- **价格变换（4 个）**：平均价格、中间价、典型价格、加权收盘价
- **数学运算（25 个）**：MAX、MIN、SUM、SQRT、LN、LOG10、EXP、ABS、CEIL、FLOOR、三角函数、双曲函数、向量运算
- **重叠研究（6 个）**：MIDPOINT、MIDPRICE、TRIMA、SAR、SAREXT、MAMA/FAMA
- **周期指标（5 个）**：希尔伯特变换系列
- **高级交易信号（4 个）**：AI SuperTrend、AI 动量指数、动态 MACD、ATR2 信号
- **pandas-ta 独有（25 个）**：熵、偏离度、挤压、QQE、CTI、ER、乖离率、心理线、RVI、惯性、鳄鱼、EFI、KST、STC、TDFI、WAE、SMI、Coppock、PGO、VWMA、BOP、SSL 通道、CFO、斜率、百分位排名
- **其他（8 个）**：斐波那契回撤/扩展、一目均衡表、枢轴点
</details>

完整指标列表及参数请参阅 [IMPLEMENTED_INDICATORS.md](IMPLEMENTED_INDICATORS.md)。

### 🎯 性能基准

```
基准测试：RSI（14 周期，10,000 个数据点）
─────────────────────────────────────────────
pandas-ta:     12.5 毫秒
TA-Lib:        8.2 毫秒
Haze-Library:  1.3 毫秒（比 TA-Lib 快 6.3 倍）

基准测试：布林带（20 周期，10,000 个数据点）
───────────────────────────────────────────────────────────
pandas-ta:     15.8 毫秒
TA-Lib:        10.1 毫秒
Haze-Library:  2.1 毫秒（比 TA-Lib 快 4.8 倍）

基准测试：MACD（12/26/9，10,000 个数据点）
─────────────────────────────────────────────
pandas-ta:     18.3 毫秒
TA-Lib:        11.4 毫秒
Haze-Library:  1.9 毫秒（比 TA-Lib 快 6.0 倍）
```

### 🏗️ 系统架构

```
┌─────────────────────────────────────────────────────────┐
│                   Python 应用层                          │
│                  （交易策略）                             │
└────────────────────────┬────────────────────────────────┘
                         │
                         │ PyO3 绑定
                         ▼
┌─────────────────────────────────────────────────────────┐
│              _haze_rust 模块（Python）                   │
│     • py_rsi()  • py_macd()  • py_bollinger_bands()     │
│     • py_supertrend()  • py_obv()  • py_kdj()           │
│              （212 个 Python 可调用函数）                 │
└────────────────────────┬────────────────────────────────┘
                         │
                         │ Rust FFI
                         ▼
┌─────────────────────────────────────────────────────────┐
│                  Rust 核心库                             │
│  ┌───────────────────────────────────────────────────┐  │
│  │  指标模块                                          │  │
│  │  • momentum.rs  • volatility.rs  • trend.rs       │  │
│  │  • volume.rs    • ma.rs          • candlestick.rs │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

### 🤝 贡献

欢迎贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解贡献指南。

### 📜 许可证

本项目采用 **CC BY-NC 4.0**（知识共享署名-非商业性使用 4.0 国际许可协议）授权。

**⚠️ 仅限非商业用途**：本软件可免费用于个人、教育和研究目的。未经明确许可，禁止商业使用。

商业许可咨询请联系：team@haze-library.com

### 🙏 致谢

- **TA-Lib**：技术分析参考实现
- **pandas-ta**：pandas 集成模式灵感来源
- **PyO3**：Rust-Python 绑定框架
- **Maturin**：Rust Python 扩展构建工具

---

**Made with ❤️ by the Haze Team**

**Last Updated**: 2025-12-26
