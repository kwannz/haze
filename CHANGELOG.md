# Changelog

All notable changes to Haze-Library will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive README.md with badges, architecture diagram, and full feature list
- CONTRIBUTING.md with detailed contribution guidelines
- MANIFEST.in for proper Python packaging
- .gitignore for clean repository

## [0.1.2] - 2025-12-26

### Added - Python FFI Documentation 📚

#### NumPy-Style Docstrings (49 functions, 47% coverage)

**English**:
Comprehensive docstrings with `#[pyo3(text_signature = "...")]` annotations for IDE autocomplete:

- **Momentum Indicators (9)**: TSI, Ultimate Oscillator, MOM, ROC, KDJ, APO, PPO, CMO
- **Trend Indicators (7)**: Vortex, Choppiness, Qstick, VHF, DX, +DI, -DI
- **Overlap/Moving Averages (6)**: T3, KAMA, TRIMA, Midpoint, Midprice, SAR
- **Candlestick Patterns (13)**: Hammer, Inverted Hammer, Hanging Man, Bullish/Bearish Engulfing, Bullish/Bearish Harami, Piercing Pattern, Dark Cloud Cover, Morning Star, Evening Star, Three White Soldiers, Three Black Crows
- **Statistical Indicators (7)**: Linear Regression, Correlation, Z-Score, Covariance, Beta, Standard Error
- **Price Transforms (3)**: AvgPrice, MedPrice, TypPrice
- **Pandas-TA Exclusives (5)**: Entropy, Aberration, Squeeze, QQE, CTI

**中文**:
完整的 NumPy 风格文档字符串，支持 `#[pyo3(text_signature = "...")]` IDE 自动补全：

- **动量指标（9 个）**：TSI、终极振荡器、MOM、ROC、KDJ、APO、PPO、CMO
- **趋势指标（7 个）**：涡流、震荡指数、量价棒、VHF、DX、+DI、-DI
- **移动平均线（6 个）**：T3、KAMA、TRIMA、中点、中价、SAR
- **蜡烛图形态（13 个）**：锤子线、倒锤子线、上吊线、看涨/看跌吞没、看涨/看跌孕线、刺透形态、乌云盖顶、早晨之星、黄昏之星、三白兵、三黑鸦
- **统计指标（7 个）**：线性回归、相关性、Z分数、协方差、贝塔系数、标准误差
- **价格变换（3 个）**：平均价格、中间价格、典型价格
- **Pandas-TA 独有（5 个）**：熵、偏离度、挤压、QQE、CTI

### Improved

**Code Quality / 代码质量**:
- Unified error handling with `ok_or_nan!` macro (reduced ~150 lines duplication)
- 统一错误处理宏 `ok_or_nan!`（减少约 150 行重复代码）

**Test Coverage / 测试覆盖率**:
- 759 tests passing (streaming.rs 90%, simd_ops.rs 90%)
- 759 个测试通过（streaming.rs 90%, simd_ops.rs 90%）

---

## [0.1.1] - 2025-12-26

### Added - Harmonic Patterns 🎵

#### Batch 11: Harmonic Pattern Indicators (212 → 215)
- **Harmonic Pattern Detection (3)**:
  - `py_harmonics`: Time-series signal output (signals, prz_upper, prz_lower, probability)
  - `py_harmonics_patterns`: Detailed pattern objects with PyHarmonicPattern class
  - `py_harmonics_prz`: PRZ (Potential Reversal Zone) calculation

- **Supported Harmonic Patterns (9 types)**:
  - Gartley (伽利形态)
  - Bat (蝙蝠形态)
  - Butterfly (蝴蝶形态)
  - Crab (螃蟹形态)
  - Deep Crab (深蟹形态)
  - Shark (鲨鱼形态)
  - Cypher (赛弗形态)
  - Three Drive (三驱形态)
  - Alt Bat (变体蝙蝠)

- **Features**:
  - XABCD swing point detection with configurable left/right bars
  - Fibonacci ratio validation per pattern type
  - PRZ zone calculation (confluence of multiple Fib projections)
  - Completion probability estimation
  - Target price and stop-loss calculation
  - Forming pattern detection (incomplete XABC patterns)
  - Bilingual support (English + Chinese pattern names)

### Fixed
- Empty data crash in harmonics.rs with bounds checking

---

## [0.1.0] - 2025-12-25

### Added - Implementation Complete (212/212 Indicators) 🎉

#### Batch 10: Final Indicators (200 → 212)
- **High-Level Moving Averages (5)**:
  - `py_alma`: Arnaud Legoux Moving Average (Gaussian weighting)
  - `py_vidya`: Variable Index Dynamic Average (volatility-adaptive)
  - `py_pwma`: Pascal's Weighted Moving Average (combinatorial weights)
  - `py_sinwma`: Sine Weighted Moving Average (sinusoidal weights)
  - `py_swma`: Symmetric Weighted Moving Average (symmetric triangle weights)

- **pandas-ta Exclusive Indicators - Batch 3 (5)**:
  - `py_bop`: Balance of Power (-1 to 1)
  - `py_ssl_channel`: SSL Channel (returns ssl_up, ssl_down)
  - `py_cfo`: Chande Forecast Oscillator
  - `py_slope`: Linear Slope Indicator
  - `py_percent_rank`: Percentile Rank (0-100)

- **Supplementary Indicators (2)**:
  - `py_natr`: Normalized ATR (percentage form)
  - `py_fisher_transform`: Fisher Transform (returns fisher, signal)

#### Batch 9: pandas-ta Exclusive - Batch 2 (190 → 200)
- **Trend Indicators (4)**:
  - `py_alligator`: Bill Williams Alligator (jaw, teeth, lips)
  - `py_kst`: Know Sure Thing (kst, signal)
  - `py_stc`: Schaff Trend Cycle (0-100)
  - `py_tdfi`: Trend Direction Force Index

- **Momentum Indicators (3)**:
  - `py_efi`: Elder's Force Index
  - `py_smi`: Stochastic Momentum Index
  - `py_coppock`: Coppock Curve (long-term trend)

- **Volatility & Price (3)**:
  - `py_wae`: Waddah Attar Explosion (explosion, dead_zone)
  - `py_pgo`: Pretty Good Oscillator
  - `py_vwma`: Volume Weighted Moving Average

#### Batch 8: pandas-ta Exclusive - Batch 1 (180 → 190)
- **Statistical Indicators (3)**:
  - `py_entropy`: Information Entropy (price uncertainty)
  - `py_cti`: Correlation Trend Indicator
  - `py_er`: Efficiency Ratio (Kaufman principle)

- **Volatility Indicators (2)**:
  - `py_aberration`: Deviation from centerline
  - `py_squeeze`: TTM Squeeze (squeeze_on, squeeze_off, momentum)

- **Momentum Indicators (3)**:
  - `py_qqe`: Quantitative Qualitative Estimation (fast_line, slow_line, signal)
  - `py_rvi`: Relative Vigor Index (rvi, signal)
  - `py_inertia`: Inertia Indicator (RVI linear regression)

- **Price Indicators (2)**:
  - `py_bias`: Bias (price deviation from MA in %)
  - `py_psl`: Psychological Line (% of up days)

#### Batch 7: TA-Lib Advanced Indicators (170 → 180)
- **Momentum (4)**: APO, PPO, CMO, T3
- **Trend (3)**: DX, PLUS_DI, MINUS_DI
- **Volume (1)**: ADOSC (Chaikin A/D Oscillator)
- **Moving Average (2)**: T3 (Tillson T3), KAMA (Kaufman Adaptive MA)

#### Batch 6: Candlestick Patterns - Final (158 → 170)
- **61 Complete TA-Lib Candlestick Patterns**: Including CONCEALING_BABY_SWALLOW, COUNTERATTACK, HIGHWAVE, HIKKAKE, HIKKAKE_MOD, LADDER_BOTTOM, MAT_HOLD, RICKSHAW_MAN, UNIQUE_3_RIVER, XSIDE_GAP_3_METHODS, CLOSING_MARUBOZU, BREAKAWAY

#### Batch 5: Cycle Indicators (143 → 158)
- **Hilbert Transform (5)**: HT_DCPERIOD, HT_DCPHASE, HT_PHASOR, HT_SINE, HT_TRENDMODE
- **Statistical (7)**: CORREL, LINEARREG, LINEARREG_SLOPE, LINEARREG_ANGLE, LINEARREG_INTERCEPT, VAR, TSF
- **Candlestick (3)**: More advanced patterns

#### Batches 1-4: Core Indicators (0 → 143)
- **Volatility (10)**: ATR, Bollinger Bands, Keltner Channel, etc.
- **Momentum (17)**: RSI, MACD, Stochastic, CCI, MFI, etc.
- **Trend (14)**: SuperTrend, ADX, Parabolic SAR, Aroon, DMI, etc.
- **Volume (11)**: OBV, VWAP, Force Index, CMF, etc.
- **Moving Averages (11)**: SMA, EMA, WMA, DEMA, TEMA, HMA, RMA, ZLMA, etc.
- **Statistical (6)**: Linear Regression, Correlation, Z-Score, Beta, etc.
- **Math Operations (25)**: MAX, MIN, SUM, SQRT, LN, LOG10, trigonometric, etc.
- **Price Transform (4)**: AVGPRICE, MEDPRICE, TYPPRICE, WCLPRICE
- **Overlap Studies (6)**: MIDPOINT, MIDPRICE, TRIMA, SAR, SAREXT, MAMA/FAMA
- **SFG Signals (4)**: AI SuperTrend, AI Momentum Index, Dynamic MACD, ATR2 Signals
- **Others (8)**: Fibonacci, Ichimoku Cloud, Pivots

### Testing
- Precision validation framework (`tests/precision_validator.py`)
- 17/212 indicators validated vs TA-Lib/pandas-ta
- Unit test framework setup (`tests/unit/conftest.py`)
- Max error < 1e-9, Correlation > 0.9999

### Performance
- 5-10x faster than pure Python implementations
- Rust-based core with PyO3 bindings
- Zero external dependencies (all algorithms from scratch)

### Documentation
- Comprehensive IMPLEMENTED_INDICATORS.md with all 212 indicators
- API documentation in README.md
- Architecture diagrams and design principles

## [0.0.1] - 2025-12-20

### Added
- Initial project structure
- Maturin build configuration
- PyO3 integration
- First batch of indicators (30)

---

## Version History

- **v0.1.2** (2025-12-26): Python FFI Documentation - 49 docstrings, ok_or_nan! macro
- **v0.1.1** (2025-12-26): Harmonic Pattern Detection - 215 indicators
- **v0.1.0** (2025-12-25): 100% Implementation Complete - 212 indicators
- **v0.0.1** (2025-12-20): Initial release - 30 indicators

---

**Maintained by**: Haze Team
**License**: MIT
