# SFG - Signal Force Generator (智能信号生成器)

**模块路径**: `haze_library::indicators::sfg`
**Rust 源文件**: `rust/src/indicators/sfg.rs`, `sfg_utils.rs`, `sfg_signals.rs`
**Python 模块**: `haze_library.np_ta`, `haze_library` (直接导入)

---

## 概述

SFG (Signal Force Generator) 是 haze-library 的核心交易信号系统，提供 4 大 ML 增强指标体系和高级市场结构分析工具。

### 核心特性

- **ML 增强**: 使用 linfa 库（线性回归/岭回归）替代传统 KNN，性能提升 42-68%
- **自适应参数**: 动态调整阈值，适应不同市场环境
- **完整信号输出**: 包含买卖信号、止损、止盈
- **高级市场结构**: FVG、Order Block、背离检测等 ICT 概念

### 性能特征

| 指标 | 时间复杂度 | 空间复杂度 | 备注 |
|------|-----------|-----------|------|
| ai_supertrend_ml | O(n) | O(n) | 含 ML 训练开销 |
| atr2_signals_ml | O(n) | O(n) | 岭回归自适应阈值 |
| ai_momentum_index_ml | O(n) | O(n) | 动量预测 |
| general_parameters_signals | O(n) | O(n) | EMA 通道 + 网格 |

---

## 目录

| 函数 | 类型 | 说明 |
|------|------|------|
| `ai_supertrend_ml` | 趋势跟踪 | ML 增强的 SuperTrend，提供趋势方向和信号 |
| `atr2_signals_ml` | 动量信号 | ATR + RSI 动态阈值信号生成器 |
| `ai_momentum_index_ml` | 动量指标 | ML 预测动量，检测超买超卖 |
| `general_parameters_signals` | 网格交易 | EMA 通道 + 网格入场信号 |

---

## 核心函数详解

### 1. ai_supertrend_ml - ML 增强的 SuperTrend

#### 函数签名

**Rust:**
```rust
pub fn ai_supertrend_ml(
    high: &[f64],
    low: &[f64],
    close: &[f64],
    st_length: usize,
    st_multiplier: f64,
    model_type: &str,
    lookback: usize,
    train_window: usize,
) -> HazeResult<AISuperTrendResult>
```

**Python:**
```python
def ai_supertrend_ml(
    high: ArrayLike,
    low: ArrayLike,
    close: ArrayLike,
    st_length: int = 10,
    st_multiplier: float = 3.0,
    model_type: str = "linreg",
    lookback: int = 10,
    train_window: int = 200,
) -> Tuple[np.ndarray, ...]  # 6 个数组
```

#### 参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| high | ArrayLike | - | 最高价序列 |
| low | ArrayLike | - | 最低价序列 |
| close | ArrayLike | - | 收盘价序列 |
| st_length | int | 10 | ATR 计算周期 |
| st_multiplier | float | 3.0 | ATR 乘数 |
| model_type | str | "linreg" | ML 模型: "linreg" 或 "ridge" |
| lookback | int | 10 | ML 特征回溯期 |
| train_window | int | 200 | ML 训练窗口大小 |

#### 返回值

返回 6 个 numpy 数组的元组:

| 索引 | 名称 | 说明 |
|------|------|------|
| 0 | supertrend | SuperTrend 值 |
| 1 | direction | 趋势方向 (1.0=看涨, -1.0=看跌) |
| 2 | buy_signals | 买入信号 (1.0=信号, 0.0=无) |
| 3 | sell_signals | 卖出信号 (1.0=信号, 0.0=无) |
| 4 | stop_loss | 动态止损价位 |
| 5 | take_profit | 动态止盈价位 |

#### Python 示例

```python
import numpy as np
from haze_library import np_ta

# 使用 NumPy 兼容层
supertrend, direction, buy, sell, sl, tp = np_ta.ai_supertrend_ml(
    high, low, close,
    st_length=10,
    st_multiplier=3.0,
    model_type="linreg"
)

# 使用 DataFrame accessor
import pandas as pd
import haze_library

df = pd.read_csv('ohlcv.csv')
result = df.haze.ai_supertrend_ml(
    st_length=10,
    st_multiplier=3.0,
    model_type="linreg"
)
```

#### 交易应用

- **趋势跟踪**: direction > 0 时持有多头，< 0 时持有空头
- **入场信号**: buy_signals/sell_signals 为 1 时入场
- **风险管理**: 使用 stop_loss 和 take_profit 设置订单

---

### 2. atr2_signals_ml - ATR 动态阈值信号

#### 函数签名

**Python:**
```python
def atr2_signals_ml(
    high: ArrayLike,
    low: ArrayLike,
    close: ArrayLike,
    volume: ArrayLike,
    rsi_period: int = 14,
    atr_period: int = 14,
    ridge_alpha: float = 1.0,
    momentum_window: int = 10,
) -> Tuple[np.ndarray, ...]  # 6 个数组
```

#### 参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| high | ArrayLike | - | 最高价序列 |
| low | ArrayLike | - | 最低价序列 |
| close | ArrayLike | - | 收盘价序列 |
| volume | ArrayLike | - | 成交量序列 |
| rsi_period | int | 14 | RSI 计算周期 |
| atr_period | int | 14 | ATR 计算周期 |
| ridge_alpha | float | 1.0 | 岭回归正则化参数 |
| momentum_window | int | 10 | 动量计算窗口 |

#### 返回值

返回 6 个 numpy 数组的元组:

| 索引 | 名称 | 说明 |
|------|------|------|
| 0 | rsi | RSI 值 |
| 1 | buy_signals | 买入信号 |
| 2 | sell_signals | 卖出信号 |
| 3 | signal_strength | 信号强度 (0.0-1.0) |
| 4 | stop_loss | 动态止损价位 |
| 5 | take_profit | 动态止盈价位 |

#### Python 示例

```python
from haze_library import np_ta

rsi, buy, sell, strength, sl, tp = np_ta.atr2_signals_ml(
    high, low, close, volume,
    rsi_period=14,
    atr_period=14
)

# 只在信号强度 > 0.7 时入场
strong_buy = (buy == 1) & (strength > 0.7)
strong_sell = (sell == 1) & (strength > 0.7)
```

---

### 3. ai_momentum_index_ml - ML 动量指标

#### 函数签名

**Python:**
```python
def ai_momentum_index_ml(
    close: ArrayLike,
    rsi_period: int = 14,
    smooth_period: int = 3,
    use_polynomial: bool = False,
    lookback: int = 5,
    train_window: int = 200,
) -> Tuple[np.ndarray, ...]  # 6 个数组
```

#### 参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| close | ArrayLike | - | 收盘价序列 |
| rsi_period | int | 14 | RSI 计算周期 |
| smooth_period | int | 3 | 平滑周期 |
| use_polynomial | bool | False | 是否使用多项式特征 |
| lookback | int | 5 | ML 特征回溯期 |
| train_window | int | 200 | ML 训练窗口 |

#### 返回值

返回 6 个 numpy 数组的元组:

| 索引 | 名称 | 说明 |
|------|------|------|
| 0 | rsi | RSI 值 |
| 1 | predicted_momentum | 预测动量值 |
| 2 | zero_cross_buy | 零线向上穿越 (买入信号) |
| 3 | zero_cross_sell | 零线向下穿越 (卖出信号) |
| 4 | overbought | 超买信号 |
| 5 | oversold | 超卖信号 |

#### Python 示例

```python
from haze_library import np_ta

rsi, momentum, buy, sell, overbought, oversold = np_ta.ai_momentum_index_ml(
    close,
    rsi_period=14,
    smooth_period=3
)

# 结合超买超卖使用
# 超卖区域 + 动量向上穿越零线 = 强买入信号
strong_buy = (oversold == 1) & (buy == 1)
```

---

### 4. general_parameters_signals - EMA 通道网格信号

#### 函数签名

**Python:**
```python
def general_parameters_signals(
    high: ArrayLike,
    low: ArrayLike,
    close: ArrayLike,
    ema_fast: int = 20,
    ema_slow: int = 50,
    atr_period: int = 14,
    grid_multiplier: float = 1.0,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]
```

#### 参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| high | ArrayLike | - | 最高价序列 |
| low | ArrayLike | - | 最低价序列 |
| close | ArrayLike | - | 收盘价序列 |
| ema_fast | int | 20 | 快速 EMA 周期 |
| ema_slow | int | 50 | 慢速 EMA 周期 |
| atr_period | int | 14 | ATR 计算周期 |
| grid_multiplier | float | 1.0 | 网格间距乘数 |

#### 返回值

返回 4 个 numpy 数组的元组:

| 索引 | 名称 | 说明 |
|------|------|------|
| 0 | buy_signals | 买入信号 |
| 1 | sell_signals | 卖出信号 |
| 2 | stop_loss | 动态止损价位 |
| 3 | take_profit | 动态止盈价位 |

#### Python 示例

```python
from haze_library import np_ta

buy, sell, sl, tp = np_ta.general_parameters_signals(
    high, low, close,
    ema_fast=20,
    ema_slow=50,
    grid_multiplier=1.5  # 更宽的网格间距
)
```

---

## 高级市场结构工具 (sfg_utils)

SFG 还提供以下高级市场结构分析函数（通过直接导入使用）：

| 函数 | 说明 |
|------|------|
| `detect_fvg` | Fair Value Gap 检测 |
| `detect_order_block` | Order Block 识别 (ICT 概念) |
| `detect_breaker_block` | Breaker Block 检测 |
| `detect_divergence` | 背离检测（常规/隐藏） |
| `pd_array` | 溢价/折扣数组计算 |
| `detect_supply_demand_zones` | 供需区域识别 |
| `linear_regression_channel` | 线性回归通道 |
| `volume_filter` | 成交量过滤器 |

### 示例：背离检测

```python
from haze_library import detect_divergence

# 检测价格与 RSI 之间的背离
div_type, strength = detect_divergence(
    price=close,
    indicator=rsi,
    lookback=20,
    threshold=0.02
)

# div_type: 0=无, 1=常规看涨, 2=常规看跌, 3=隐藏看涨, 4=隐藏看跌
```

---

## 信号组合 (sfg_signals)

`sfg_signals` 模块提供信号组合和风险管理工具：

| 组件 | 说明 |
|------|------|
| `SFGSignal` | 统一信号输出结构 |
| `combine_signals` | 多信号源加权组合 |
| `calculate_stops` | 止损止盈计算 |
| `trailing_stop` | 追踪止损 |

---

## 错误处理

所有 SFG 函数使用 `HazeResult<T>` 处理错误，可能抛出以下异常：

| 异常 | 说明 |
|------|------|
| `InsufficientDataError` | 数据量不足（< train_window + lookback） |
| `InvalidPeriodError` | 周期参数无效 (≤ 0) |
| `InvalidParameterError` | 参数无效 (NaN/Inf) |

---

## 最小数据要求

| 函数 | 最小数据量 |
|------|-----------|
| ai_supertrend_ml | train_window + lookback (默认 210) |
| atr2_signals_ml | 200 + momentum_window (默认 210) |
| ai_momentum_index_ml | train_window + lookback (默认 205) |
| general_parameters_signals | max(ema_fast, ema_slow) + atr_period |

---

## 流式计算 (Streaming)

SFG 支持增量/流式计算，适用于实时交易场景：

### IncrementalAISuperTrend

```python
from haze_library.streaming import IncrementalAISuperTrend, CCXTStreamProcessor

# 创建流式计算器
ind = IncrementalAISuperTrend(
    st_length=10,
    st_multiplier=3.0,
    lookback=10,
    train_window=200,
)

# 逐条更新
for candle in realtime_feed:
    result = ind.update(candle['high'], candle['low'], candle['close'])

    if result['buy_signal']:
        print(f"Buy @ {candle['close']}, SL: {result['stop_loss']}, TP: {result['take_profit']}")
    elif result['sell_signal']:
        print(f"Sell @ {candle['close']}, SL: {result['stop_loss']}, TP: {result['take_profit']}")
```

### 返回值字段

| 字段 | 类型 | 说明 |
|------|------|------|
| supertrend | float | SuperTrend 线值 |
| direction | int | 趋势方向 (-1/0/1) |
| trend_offset | float | ML 预测的趋势偏移 |
| buy_signal | bool | 买入信号 |
| sell_signal | bool | 卖出信号 |
| stop_loss | float | 建议止损价位 |
| take_profit | float | 建议止盈价位 |

### CCXTStreamProcessor 集成

```python
from haze_library.streaming import CCXTStreamProcessor, IncrementalAISuperTrend

proc = CCXTStreamProcessor()
proc.add_indicator("ai_st", IncrementalAISuperTrend(st_length=10))

# 处理 CCXT 格式 K 线
for candle in exchange.watch_ohlcv('BTC/USDT', '1m'):
    results = proc.process_candle(candle)
    ai_st_result = results['ai_st']
    # ...
```

---

## 参考资料

- [SuperTrend Indicator](https://www.tradingview.com/support/solutions/43000672285-supertrend/)
- [ATR - Average True Range](https://www.investopedia.com/terms/a/atr.asp)
- [RSI - Relative Strength Index](https://www.investopedia.com/terms/r/rsi.asp)
- [ICT Trading Concepts](https://www.ictconcepts.com/)
