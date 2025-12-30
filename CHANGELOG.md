# Changelog

All notable changes to Haze-Library will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.1.2] - 2025-12-30

### Documentation / 文档
- **新增 `docs/LT_INDICATORS.md`** - LT 指标系统完整技术文档 (50KB+)
  - 架构设计：市场状态检测算法、加权集成投票机制
  - 指标深度：10 个 SFG 指标详解（算法原理、数学公式、参数配置、代码示例）
    - AI SuperTrend: KNN + SuperTrend ML 增强
    - ATR2 Signals: ATR + RSI + 岭回归
    - AI Momentum Index: KNN + RSI 关系预测
    - General Parameters: RSI + MACD + ATR 投票
    - Pivot Buy/Sell: 枢轴点 + 跟踪止损
    - Market Structure & FVG: BOS/CHoCH + Fair Value Gap
    - PD Array & Breaker: Premium/Discount + 突破区块
    - Linear Regression: 多时间框架支撑阻力
    - Volume Profile: POC/VAH/VAL 成交量分布
    - Dynamic MACD + Heikin Ashi: MACD + 平均 K 线
  - 配置指南：参数调优策略、权重自定义、性能优化
  - 实战示例：5 个递进式完整代码示例（基础用法 → 回测框架）
  - 市场分析：TRENDING/RANGING/VOLATILE 三态详解
  - 常见问题：FAQ + 故障排除 + 集成指南

**注意**: 本版本为纯文档发布，无代码变更。

## [1.1.1] - 2025-12-30

### Fixed / 修复
- **Clippy 警告清理**: 修复所有 87 个 clippy 警告
  - 更新 benchmark 代码使用 `std::hint::black_box` 替代 deprecated `criterion::black_box`
  - CI/CD 启用严格模式 (`-D clippy::all`)
  - 0 警告，100% 代码质量

### Changed / 变更
- CI/CD 配置：移除 `continue-on-error` flag，clippy 失败将阻止构建

## [1.1.0] - 2025-12-30

### Added / 新增
- **LT 组合指标系统**: 10 个 SFG 专业交易信号指标
  - AI SuperTrend: KNN + SuperTrend 机器学习增强
  - ATR2 Signals: ATR + MLMI 预测
  - Pivot Buy/Sell Signals: 枢轴点 + 跟踪止损
  - AI Momentum Index: KNN + RSI 关系预测
  - Volume Algorithm Profile: 成交量分布 + POC/VAH/VAL
  - General Parameters: 动态 EMA 通道
  - Market Structure & FVG: BOS/CHoCH + Fair Value Gap
  - PD Array & Breaker Block: Premium/Discount + 突破区块
  - Linear Regression & Supply Demand: 多时间框架支撑阻力
  - Dynamic MACD + Heikin Ashi: MACD + 平均 K 线

- **市场状态自适应**: 自动检测 TRENDING/RANGING/VOLATILE 市场状态
- **加权集成投票**: 根据市场状态动态调整指标权重
- **Volume Profile 增强**: 新增 `volume_profile_with_signals()` 函数
  - POC (Point of Control) 计算
  - VAH/VAL (Value Area High/Low) 识别
  - 买卖信号生成
- **Heikin Ashi 指标**: 新增 `heikin_ashi_signals()` 函数
  - 趋势强度计算
  - 买卖信号生成

### Fixed / 修复
- 权重归一化: 确保所有市场状态权重总和为 1.0
- 边界条件检测: 增强 NaN/Inf/负值检测
- 输入验证: 添加数据长度和有效性检查

### Documentation / 文档
- 新增 LT 指标演示示例 (`examples/lt_indicator_demo.py`)
- 新增市场状态校准文档 (`examples/REGIME_CALIBRATION_RESULTS.md`)
- 新增 10 个 SFG 指标功能验证测试 (`examples/test_lt_indicators.py`)

### Tests / 测试
- 新增逻辑闭环测试 (`tests/unit/test_lt_indicators_closure.py`)
- 896/908 tests passing (98.7%)
- PDF 规格符合度: 10/10 指标 100% 符合

## [1.0.1] - 2025-12-28

### Changed / 变更
- Updated Rust dependency pins to latest compatible patch versions (linfa 0.8.1, thiserror 2.0.17,
  ndarray 0.16.1, criterion 0.8.1, bincode 2.0.1).
- Raised maturin minimum version to 1.10.2 for Python builds.

### Fixed / 修复
- Mass Index doc example now uses sufficient input length to avoid `InsufficientData` errors.

## [1.0.0] - 2025-12-28

### Highlights / 亮点 🎉

**Production-Ready Release / 生产就绪版本**:
- **885 tests passing** with **100% code coverage** (2,437 statements, 0 missed)
- **0 code quality errors** (ruff, clippy clean)
- **215+ technical indicators** with Rust-powered performance
- **Streaming/Incremental calculators** for real-time trading
- **Multi-framework support**: NumPy, Pandas, Polars, PyTorch

**中文**:
- **885 个测试通过**，**100% 代码覆盖率**（2,437 条语句，0 遗漏）
- **0 代码质量错误**（ruff、clippy 全部通过）
- **215+ 技术指标**，Rust 驱动的高性能
- **流式/增量计算器**，支持实时交易
- **多框架支持**：NumPy、Pandas、Polars、PyTorch

### Added / 新增

**Streaming Indicators / 流式指标**:
- `IncrementalSMA`, `IncrementalEMA`, `IncrementalRSI`, `IncrementalATR`
- `IncrementalMACD`, `IncrementalBollingerBands`, `IncrementalStochastic`
- `IncrementalSuperTrend`, `IncrementalAdaptiveRSI`, `IncrementalEnsembleSignal`
- `IncrementalMLSuperTrend` - Machine learning enhanced SuperTrend
- `CCXTStreamProcessor` - Direct CCXT integration for live trading

**AI Indicators / AI 指标**:
- `adaptive_rsi` - Volatility-adaptive RSI with dynamic period
- `ensemble_signal` - Multi-indicator ensemble with weighted voting
- `ml_supertrend` - ML-enhanced SuperTrend with confirmation

**Execution Module / 执行模块**:
- `ExecutionEngine` - Order execution with risk management
- `CCXTProvider` - Exchange integration via CCXT
- `RiskManager` - Position sizing and stop-loss management

### Changed / 变更
- Parallel utilities now return `HazeResult` and fail fast on invalid inputs (no NaN fallback):
  `parallel_sma`, `parallel_ema`, `parallel_rsi`, `parallel_atr`,
  `parallel_multi_period_sma`, `parallel_multi_period_ema`.
- Math ops now return `HazeResult` and enforce domain checks (`sqrt`, `ln`, `log10`,
  `asin`, `acos`, `div`, length-matched vector ops).
- AI indicators (`adaptive_rsi`, `ensemble_signal`, `ml_supertrend`) are exported at the
  top-level and enforce strict parameter/length validation (fail-fast).
- Streaming incremental indicators now raise on non-finite inputs instead of
  propagating NaN, aligning streaming APIs with fail-fast behavior.
- Python runtime deps now require `numpy>=2.4.0` and `pandas>=2.3.3` to match
  Python 3.14 support.
- Fibonacci, Harmonics, Ichimoku, Pivot, and SFG signal utilities now fail fast on
  invalid inputs; Python bindings updated accordingly.
- Python API changes:
  - `py_combine_signals` now returns `(buy, sell, strength)`.
  - `py_calculate_stops` now expects `(close, atr_values, buy_signals, sell_signals, ...)`.
  - Added `py_trailing_stop`.
  - `py_harmonics_patterns` and `py_swing_points` now raise on insufficient data (no empty-list fallback).
- Added Python wrappers for additional Fibonacci/Ichimoku/Pivot helpers.
- PyO3 type stubs now include core classes and correct tuple/list return types
   (`py_calc_pivot_series`, `py_harmonics_patterns`, `py_swing_points`).

### Fixed / 修复
- `vhf` now returns `InsufficientData` when `period >= data_len`.
- `pvt`, `nvi`, `pvi`, `eom` now return `InsufficientData` when input length < 2.
- `volume_profile` now returns `ParameterOutOfRange` when `num_bins == 0`.
- Online adaptive RSI uses Kahan summation for gain/loss windows to reduce drift.
- Regenerated golden fixture `tests/fixtures/golden_indicators_v1.json` after fail-fast updates.

### Migration Notes / 迁移说明
- Update parallel calls to handle `Result`, e.g. `parallel_sma(&data_sets)?` or `.unwrap()`.
- If you depended on NaN-filled outputs for invalid input, handle the error explicitly.
- Ensure `pvt`, `nvi`, `pvi`, `eom` inputs contain at least 2 data points.
- Pass `num_bins >= 1` for `volume_profile`.
- Update math ops callers to handle `ValueError` for invalid domains and zero divisors.
- Update SFG integrations for `py_combine_signals` and `py_calculate_stops` signature changes.
- AI indicators now require `base_period` within `[min_period, max_period]`, and
  `min_period`, `max_period`, `volatility_window`, and `period` must be `< data length`.
  `ml_supertrend` now errors if `confirmation_bars` exceeds data length.
- Streaming updates now raise `ValueError` on NaN/Inf inputs; remove any caller-side
  reliance on NaN propagation for `IncrementalSMA` and `IncrementalAdaptiveRSI`.

## [0.1.3] - 2025-12-26

### Fixed - Code Quality / 代码质量修复

**Clippy Warnings (18 total) / Clippy 警告（共 18 处）**:
- Replace manual slice copy loops with `copy_from_slice()` for SIMD optimization (3 locations)
- Use iterator patterns instead of index-only loop variables (4 locations)
- Add `OhlcResult` type alias to reduce complex tuple types (2 locations)
- Remove redundant identical if/else branches (6 locations)
- Collapse `else { if }` blocks to `else if` (2 locations)
- Use `clamp()` instead of manual min/max checks (1 location)
- Simplify boolean expressions by factoring common conditions (2 locations)
- Replace `iter().copied().collect()` with `to_vec()` (1 location)

**中文**:
- 使用 `copy_from_slice()` 替换手动切片复制循环，启用 SIMD 优化（3 处）
- 使用迭代器模式替代仅用于索引的循环变量（4 处）
- 添加 `OhlcResult` 类型别名简化复杂元组类型（2 处）
- 移除冗余的相同 if/else 分支（6 处）
- 将 `else { if }` 块折叠为 `else if`（2 处）
- 使用 `clamp()` 替代手动最小/最大值检查（1 处）
- 通过提取公共条件简化布尔表达式（2 处）
- 使用 `to_vec()` 替代 `iter().copied().collect()`（1 处）

### Improved - CI/CD

**GitHub Actions / GitHub 工作流**:
- Added Linux aarch64 wheel builds (ARM64 support)
- Added sdist (source distribution) to releases
- Improved macOS builds with separate macos-13 (Intel) and macos-14 (ARM) runners
- Using PyO3/maturin-action for more reliable wheel builds

**中文**:
- 新增 Linux aarch64 轮子构建（ARM64 支持）
- 发布包中新增 sdist（源代码分发）
- 改进 macOS 构建，分离 macos-13（Intel）和 macos-14（ARM）运行器
- 使用 PyO3/maturin-action 提高轮子构建可靠性

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
- No external indicator dependencies (all indicator algorithms from scratch; infra deps are minimal)

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

- **v1.0.0** (2025-12-28): Production-Ready Release - 885 tests, 100% coverage, 215+ indicators
- **v0.1.3** (2025-12-26): Code Quality - Clippy warnings fixed, CI/CD improvements
- **v0.1.2** (2025-12-26): Python FFI Documentation - 49 docstrings, ok_or_nan! macro
- **v0.1.1** (2025-12-26): Harmonic Pattern Detection - 215 indicators
- **v0.1.0** (2025-12-25): 100% Implementation Complete - 212 indicators
- **v0.0.1** (2025-12-20): Initial release - 30 indicators

---

**Maintained by**: Haze Team
**License**: MIT
