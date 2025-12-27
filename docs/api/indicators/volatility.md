# Volatility Indicators (波动率指标)

**模块路径**: `haze_library::indicators::volatility`

## 概述

波动率指标模块提供基于价格变动幅度的技术分析工具,用于测量市场在一定时期内的价格波动程度。波动率指标对风险管理、仓位调整和识别潜在突破条件至关重要。

**核心特性**:
- 10 个专业波动率指标
- O(n) 时间复杂度,高效滚动计算
- 完整的错误处理与参数验证
- 符合 TA-Lib 计算标准

**统一错误处理**:
所有函数返回 `HazeResult<T>`,可能的错误类型:
- `HazeError::EmptyInput` - 输入数组为空
- `HazeError::LengthMismatch` - 输入数组长度不一致
- `HazeError::InvalidPeriod` - 周期参数为 0 或超过数据长度
- `HazeError::InsufficientData` - 数据长度不足
- `HazeError::ParameterOutOfRange` - 参数值超出有效范围

---

## 目录

### 核心波动率指标 (完整文档)
1. [ATR - Average True Range (平均真实波幅)](#1-atr---average-true-range)
2. [Bollinger Bands (布林带)](#2-bollinger-bands)
3. [Keltner Channel (肯特纳通道)](#3-keltner-channel)

### 常用波动率指标 (标准文档)
4. [True Range (真实波幅)](#4-true-range)
5. [NATR - Normalized ATR (归一化 ATR)](#5-natr---normalized-atr)
6. [Donchian Channel (唐奇安通道)](#6-donchian-channel)
7. [Chandelier Exit (吊灯止损)](#7-chandelier-exit)

### 专业波动率指标 (简化文档)
8. [Historical Volatility (历史波动率)](#8-historical-volatility)
9. [Ulcer Index (溃疡指数)](#9-ulcer-index)
10. [Mass Index (质量指数)](#10-mass-index)

---

# 核心波动率指标

## 1. ATR - Average True Range

**函数签名**: `atr(high: &[f64], low: &[f64], close: &[f64], period: usize) -> HazeResult<Vec<f64>>`

**模块**: `indicators::volatility`

### 描述

平均真实波幅 (ATR) 是由 J. Welles Wilder Jr. 开发的技术分析波动率指标,通过分解资产价格在给定时期内的完整波动范围来衡量市场波动性。ATR 广泛用于仓位调整、止损设置和基于波动率的交易策略。

### 算法

```text
1. 计算真实波幅 (True Range):
   TR = MAX(high - low, |high - prev_close|, |low - prev_close|)

2. 初始 ATR (第 n 个周期):
   ATR[n] = SMA(TR[1..=n])

3. 后续 ATR 值 (Wilder 平滑法/RMA):
   ATR[i] = (ATR[i-1] * (period-1) + TR[i]) / period

   注意: 使用 Wilder 平滑法,类似于指数移动平均,
   但 α = 1/period 而非 2/(period+1)
```

### 参数

| 参数 | 类型 | 说明 | 典型值 |
|------|------|------|--------|
| `high` | `&[f64]` | 最高价序列 | - |
| `low` | `&[f64]` | 最低价序列 | - |
| `close` | `&[f64]` | 收盘价序列 | - |
| `period` | `usize` | ATR 平滑周期 | 14 |

### 返回值

- `Ok(Vec<f64>)`: ATR 值向量
  - 长度与输入相同
  - 前 `period` 个值为 NaN (warmup 期)
  - 有效值从 `index = period` 开始
- `Err(HazeError)`: 参数错误或数据不足

### 性能

- **时间复杂度**: O(n)
- **空间复杂度**: O(n) 用于 TR 和结果向量
- **算法**: 单次遍历,增量 Wilder 平滑

### Rust 示例

```rust
use haze_library::indicators::volatility::atr;

let high = vec![102.0, 105.0, 104.0, 106.0, 108.0, 110.0, 112.0, 114.0,
                116.0, 118.0, 120.0, 122.0, 124.0, 126.0, 128.0];
let low = vec![99.0, 101.0, 100.0, 102.0, 104.0, 106.0, 108.0, 110.0,
               112.0, 114.0, 116.0, 118.0, 120.0, 122.0, 124.0];
let close = vec![101.0, 103.0, 102.0, 105.0, 107.0, 109.0, 111.0, 113.0,
                 115.0, 117.0, 119.0, 121.0, 123.0, 125.0, 127.0];

// 计算 14 周期 ATR
let atr_values = atr(&high, &low, &close, 14).unwrap();

// 前 14 个值为 NaN (warmup 期)
assert!(atr_values[13].is_nan());

// 第一个有效 ATR 在索引 14
assert!(!atr_values[14].is_nan());
assert!(atr_values[14] > 0.0);
```

### Python 示例

```python
import haze_library as haze
import pandas as pd

# 方法 1: 直接函数调用
high = [102.0, 105.0, 104.0, 106.0, 108.0, 110.0, 112.0, 114.0,
        116.0, 118.0, 120.0, 122.0, 124.0, 126.0, 128.0]
low = [99.0, 101.0, 100.0, 102.0, 104.0, 106.0, 108.0, 110.0,
       112.0, 114.0, 116.0, 118.0, 120.0, 122.0, 124.0]
close = [101.0, 103.0, 102.0, 105.0, 107.0, 109.0, 111.0, 113.0,
         115.0, 117.0, 119.0, 121.0, 123.0, 125.0, 127.0]

atr_values = haze.py_atr(high, low, close, period=14)

# 方法 2: DataFrame Accessor (推荐)
df = pd.DataFrame({'high': high, 'low': low, 'close': close})
df['atr_14'] = df.haze.atr(14)

# 方法 3: 风险调整仓位
df['position_size'] = 1000.0 / df['atr_14']  # 每笔风险固定 1000
```

### 交易应用

| 应用场景 | 策略说明 | 参数建议 |
|----------|----------|----------|
| **波动率测量** | ATR 越高 = 波动性越大 | period=14 |
| **仓位调整** | 风险固定为 ATR 的倍数 | risk = 2 * ATR |
| **止损设置** | 入场点 ± 2-3 倍 ATR | stop = 2.5 * ATR |
| **突破确认** | ATR 上升确认突破强度 | 突破时 ATR > MA(ATR) |
| **跟踪止损** | 用于 Chandelier Exit 等系统 | 见 chandelier_exit |

**典型信号解读**:
```python
# ATR 绝对值用于波动率判断
if atr_current > atr_ma:
    print("波动率扩张 - 可能出现大幅波动")
else:
    print("波动率收缩 - 市场可能处于整理期")

# ATR 相对变化率
atr_change_pct = (atr_current - atr_prev) / atr_prev * 100
if atr_change_pct > 20:
    print("波动率急剧上升 - 警惕风险")
```

### 实现注意事项

- 遵循 TA-Lib 约定:
  - TR[0] 在 ATR 计算中被忽略
  - 初始 ATR 使用 TR[1..=period] 的简单平均
  - 后续值使用 Wilder 平滑 (RMA)
- ATR 是绝对值指标,需结合价格水平解读
- 高价股票的 ATR 自然高于低价股票
- 使用 NATR (归一化 ATR) 可跨标的比较

### 相关函数

- [`true_range`](#4-true-range) - 底层 TR 计算
- [`natr`](#5-natr---normalized-atr) - 归一化 ATR (百分比形式)
- [`chandelier_exit`](#7-chandelier-exit) - 基于 ATR 的跟踪止损
- [`keltner_channel`](#3-keltner-channel) - 基于 ATR 的波动率通道

### 参考文献

- Wilder, J. W. (1978). *New Concepts in Technical Trading Systems*
- 标准周期: 14 (可根据时间框架调整)

---

## 2. Bollinger Bands

**函数签名**: `bollinger_bands(close: &[f64], period: usize, std_multiplier: f64) -> HazeResult<(Vec<f64>, Vec<f64>, Vec<f64>)>`

**模块**: `indicators::volatility`

### 描述

布林带 (Bollinger Bands) 是由 John Bollinger 开发的波动率指标,由中轨 (SMA) 和距离中轨指定标准差倍数的上下轨组成。用于识别超买/超卖状态、波动率扩张/收缩和潜在反转点。

### 算法

```text
1. 中轨 (Middle Band / BASIS):
   MB = SMA(close, period)

2. 标准差:
   σ = StdDev(close, period)    [总体标准差]

3. 上轨 (Upper Band):
   UB = MB + (σ * std_multiplier)

4. 下轨 (Lower Band):
   LB = MB - (σ * std_multiplier)

典型设置:
- 周期: 20
- 倍数: 2.0 (覆盖约 95% 的价格行为)
```

### 参数

| 参数 | 类型 | 说明 | 典型值 |
|------|------|------|--------|
| `close` | `&[f64]` | 收盘价序列 | - |
| `period` | `usize` | 中轨 SMA 周期 | 20 |
| `std_multiplier` | `f64` | 标准差倍数 | 2.0 |

### 返回值

- `Ok((upper, middle, lower))`: 三个向量的元组
  - `upper`: 上轨 (Upper Band)
  - `middle`: 中轨 (SMA)
  - `lower`: 下轨 (Lower Band)
  - 所有向量长度与输入相同
  - 前 `period - 1` 个值为 NaN
- `Err(HazeError)`: 参数错误

### 性能

- **时间复杂度**: O(n)
- **空间复杂度**: O(n)
- **算法**: 高效滚动统计计算 (Welford 算法)

### Rust 示例

```rust
use haze_library::indicators::volatility::bollinger_bands;

let close = vec![
    100.0, 101.0, 102.0, 103.0, 104.0, 105.0, 104.5, 104.0,
    105.0, 106.0, 107.0, 108.0, 109.0, 110.0, 111.0, 112.0,
    113.0, 114.0, 115.0, 116.0, 117.0
];

// 标准布林带 (20 周期, 2 倍标准差)
let (upper, middle, lower) = bollinger_bands(&close, 20, 2.0).unwrap();

// 检查轨道值
assert!((middle[19] - 107.475).abs() < 1e-10);  // 前 20 个值的 SMA
assert!(upper[19] > middle[19]);
assert!(lower[19] < middle[19]);

// 检测 Bollinger Squeeze (轨道收窄)
let bandwidth = (upper[19] - lower[19]) / middle[19];
if bandwidth < 0.05 {  // 小于 5%
    println!("Bollinger Squeeze 检测到 - 波动率收缩");
}
```

### Python 示例

```python
import haze_library as haze
import pandas as pd
import numpy as np

# 方法 1: 直接函数调用
close = [100.0, 101.0, 102.0, 103.0, 104.0, 105.0, 104.5, 104.0,
         105.0, 106.0, 107.0, 108.0, 109.0, 110.0, 111.0, 112.0,
         113.0, 114.0, 115.0, 116.0, 117.0]

upper, middle, lower = haze.py_bollinger_bands(close, period=20, std_multiplier=2.0)

# 方法 2: DataFrame Accessor (推荐)
df = pd.DataFrame({'close': close})
df['bb_upper'], df['bb_middle'], df['bb_lower'] = df.haze.bollinger_bands(20, 2.0)

# 方法 3: 计算 %B 指标
df['percent_b'] = (df['close'] - df['bb_lower']) / (df['bb_upper'] - df['bb_lower'])

# 方法 4: 计算带宽 (BandWidth)
df['bandwidth'] = (df['bb_upper'] - df['bb_lower']) / df['bb_middle'] * 100

# 方法 5: 识别 Bollinger Squeeze
df['squeeze'] = df['bandwidth'] < 5  # 带宽 < 5% 视为 Squeeze
```

### 交易策略

#### 1. Bollinger Bounce (布林反弹)
```python
# 适用于震荡市场
if close < lower_band:
    signal = "买入 - 价格触及下轨"
elif close > upper_band:
    signal = "卖出 - 价格触及上轨"
```

#### 2. Bollinger Squeeze (布林挤压)
```python
# 窄带预示大波动即将来临
bandwidth = (upper - lower) / middle
if bandwidth < historical_low:
    print("Bollinger Squeeze - 低波动率,准备突破")
    # 突破方向由首次触及的轨道决定
```

#### 3. Band Walk (沿轨行走)
```python
# 强趋势市场
if close >= upper_band:
    print("强劲上升趋势 - 价格持续触及上轨")
    # 保持多头直到轨道明显扩宽
elif close <= lower_band:
    print("强劲下降趋势 - 价格持续触及下轨")
```

#### 4. %B 指标
```python
percent_b = (close - lower) / (upper - lower)

if percent_b > 1.0:
    print("价格在上轨之上 - 超买")
elif percent_b < 0.0:
    print("价格在下轨之下 - 超卖")
elif 0.45 <= percent_b <= 0.55:
    print("价格接近中轨 - 中性")
```

### 交易信号表

| %B 值 | 位置 | 解读 | 信号强度 |
|-------|------|------|----------|
| > 1.0 | 上轨之上 | 极度超买 | ⚠️⚠️⚠️ |
| 0.8 - 1.0 | 上轨附近 | 超买 | ⚠️⚠️ |
| 0.5 | 中轨 | 中性 | - |
| 0.0 - 0.2 | 下轨附近 | 超卖 | 📈📈 |
| < 0.0 | 下轨之下 | 极度超卖 | 📈📈📈 |

| 带宽变化 | 波动率状态 | 交易含义 |
|----------|------------|----------|
| 带宽 < 5% | 极度收窄 | Squeeze - 大波动即将来临 |
| 带宽扩张 | 波动率上升 | 趋势可能形成或加速 |
| 带宽收缩 | 波动率下降 | 市场整理,等待方向 |

### 实现注意事项

- 使用总体标准差 (除以 n,非 n-1)
- 符合 TA-Lib 计算标准
- 轨道在波动率扩张时变宽
- 轨道在波动率收缩时变窄
- 在正态分布假设下,覆盖约 95% 的价格行为

### 相关函数

- [`keltner_channel`](#3-keltner-channel) - 使用 ATR 替代 StdDev 的类似概念
- [`donchian_channel`](#6-donchian-channel) - 使用最高/最低价的价格通道
- `sma` - 简单移动平均 (中轨基础)
- `stdev_population` - 总体标准差计算

### 参考文献

- Bollinger, J. (2001). *Bollinger on Bollinger Bands*
- 标准参数: 20 周期 SMA, 2.0 倍标准差
- 正态分布下覆盖约 95% 的价格行为

---

## 3. Keltner Channel

**函数签名**: `keltner_channel(high: &[f64], low: &[f64], close: &[f64], period: usize, atr_period: usize, multiplier: f64) -> HazeResult<(Vec<f64>, Vec<f64>, Vec<f64>)>`

**模块**: `indicators::volatility`

### 描述

肯特纳通道 (Keltner Channel) 是基于波动率的包络线指标,使用 EMA 作为中线,ATR 计算轨道宽度。

### 算法

```text
中线 (Middle Line) = EMA(close, period)
上线 (Upper Line)  = 中线 + (ATR * multiplier)
下线 (Lower Line)  = 中线 - (ATR * multiplier)
```

### 参数

| 参数 | 类型 | 说明 | 典型值 |
|------|------|------|--------|
| `high` | `&[f64]` | 最高价序列 | - |
| `low` | `&[f64]` | 最低价序列 | - |
| `close` | `&[f64]` | 收盘价序列 | - |
| `period` | `usize` | 中线 EMA 周期 | 20 |
| `atr_period` | `usize` | 轨道宽度 ATR 周期 | 10 |
| `multiplier` | `f64` | ATR 倍数 | 2.0 |

### 返回值

- `Ok((upper, middle, lower))`: 三个通道值向量
- `Err(HazeError)`: 参数错误或数据不足

### 性能

- **时间复杂度**: O(n)
- **算法**: EMA + ATR 组合计算

### Rust 示例

```rust
use haze_library::indicators::volatility::keltner_channel;

let high = vec![102.0, 105.0, 104.0, 106.0, 108.0, 110.0];
let low = vec![99.0, 101.0, 100.0, 102.0, 104.0, 106.0];
let close = vec![101.0, 103.0, 102.0, 105.0, 107.0, 109.0];

let (upper, middle, lower) = keltner_channel(
    &high, &low, &close,
    3,    // EMA 周期
    3,    // ATR 周期
    2.0   // 倍数
).unwrap();
```

### Python 示例

```python
import haze_library as haze
import pandas as pd

# 方法 1: 直接调用
high = [102.0, 105.0, 104.0, 106.0, 108.0, 110.0]
low = [99.0, 101.0, 100.0, 102.0, 104.0, 106.0]
close = [101.0, 103.0, 102.0, 105.0, 107.0, 109.0]

upper, middle, lower = haze.py_keltner_channel(
    high, low, close,
    period=20,
    atr_period=10,
    multiplier=2.0
)

# 方法 2: DataFrame Accessor
df = pd.DataFrame({'high': high, 'low': low, 'close': close})
df['kc_upper'], df['kc_middle'], df['kc_lower'] = df.haze.keltner_channel(20, 10, 2.0)

# 突破信号
df['breakout'] = df['close'] > df['kc_upper']
```

### 交易应用

| 应用场景 | 策略说明 |
|----------|----------|
| **趋势跟踪** | 价格在上轨之上 = 上升趋势 |
| **突破交易** | 价格突破通道 = 趋势可能形成 |
| **超买超卖** | 价格远离中线 = 回归机会 |
| **与布林带组合** | KC 窄于 BB = Squeeze 信号 |

**典型信号**:
```python
if close > upper:
    print("上升趋势 - 考虑持有或加仓")
elif close < lower:
    print("下降趋势 - 考虑减仓或做空")
else:
    print("震荡区间 - 等待突破")
```

### 实现注意事项

- 使用 EMA 而非 SMA 作为中线 (比布林带更敏感)
- ATR 基于真实波幅,比标准差更稳定
- 适合趋势跟踪策略
- multiplier=1.5 适合短期,2.0-2.5 适合中期

### 相关函数

- [`bollinger_bands`](#2-bollinger-bands) - 使用 StdDev 的类似指标
- [`atr`](#1-atr---average-true-range) - 轨道宽度计算基础
- `ema` - 中线计算

---

# 常用波动率指标

## 4. True Range

**函数签名**: `true_range(high: &[f64], low: &[f64], close: &[f64], drift: usize) -> HazeResult<Vec<f64>>`

**模块**: `indicators::volatility`

### 描述

真实波幅 (True Range) 计算三者中的最大值:
- 当日最高价 - 当日最低价
- |当日最高价 - 前一日收盘价|
- |当日最低价 - 前一日收盘价|

### 算法

```text
TR = MAX(high - low, ABS(high - prev_close), ABS(low - prev_close))
```

### 参数

- `high`: 最高价序列
- `low`: 最低价序列
- `close`: 收盘价序列
- `drift`: 回溯周期 (通常为 1)

### 返回值

- `Ok(Vec<f64>)`: TR 值,前 `drift` 个值为 NaN
- `Err(HazeError)`: 参数错误

### Rust/Python 示例

```rust
use haze_library::indicators::volatility::true_range;

let high = vec![102.0, 105.0, 104.0];
let low = vec![99.0, 101.0, 100.0];
let close = vec![101.0, 103.0, 102.0];

let tr = true_range(&high, &low, &close, 1).unwrap();
assert!(tr[0].is_nan()); // 无前一日收盘价
assert_eq!(tr[1], 4.0);  // MAX(4, 4, 0) = 4.0
```

```python
import haze_library as haze

high = [102.0, 105.0, 104.0]
low = [99.0, 101.0, 100.0]
close = [101.0, 103.0, 102.0]

tr = haze.py_true_range(high, low, close, drift=1)
```

### 应用

- ATR 计算的基础
- 日内波动范围测量
- 跳空缺口检测

---

## 5. NATR - Normalized ATR

**函数签名**: `natr(high: &[f64], low: &[f64], close: &[f64], period: usize) -> HazeResult<Vec<f64>>`

**模块**: `indicators::volatility`

### 描述

归一化平均真实波幅 (NATR) 将 ATR 表示为收盘价的百分比,使其可在不同价格水平和标的间进行比较。

### 算法

```text
NATR = (ATR / close) * 100
```

### 参数

- `high`: 最高价序列
- `low`: 最低价序列
- `close`: 收盘价序列
- `period`: ATR 周期 (通常 14)

### 返回值

- `Ok(Vec<f64>)`: NATR 值 (百分比形式)
- `Err(HazeError)`: 参数错误

### Rust/Python 示例

```rust
use haze_library::indicators::volatility::natr;

let high = vec![102.0, 105.0, 104.0, 106.0, 108.0];
let low = vec![99.0, 101.0, 100.0, 102.0, 104.0];
let close = vec![101.0, 103.0, 102.0, 105.0, 107.0];

let natr_values = natr(&high, &low, &close, 3).unwrap();
// NATR 以百分比表示 (例如 3.5 表示 3.5%)
```

```python
import haze_library as haze
import pandas as pd

df = pd.DataFrame({'high': high, 'low': low, 'close': close})
df['natr_14'] = df.haze.natr(14)

# 跨标的比较波动率
df['volatility_rank'] = df['natr_14'].rank(pct=True)
```

### 应用

- 跨标的波动率比较
- 标准化风险测量
- 相对波动率排名

---

## 6. Donchian Channel

**函数签名**: `donchian_channel(high: &[f64], low: &[f64], period: usize) -> HazeResult<(Vec<f64>, Vec<f64>, Vec<f64>)>`

**模块**: `indicators::volatility`

### 描述

唐奇安通道 (Donchian Channel) 显示指定周期内的最高价和最低价,形成价格通道。

### 算法

```text
上轨 (Upper Band)  = MAX(high, period)
下轨 (Lower Band)  = MIN(low, period)
中轨 (Middle Band) = (上轨 + 下轨) / 2
```

### 参数

- `high`: 最高价序列
- `low`: 最低价序列
- `period`: 回溯周期 (通常 20)

### 返回值

- `Ok((upper, middle, lower))`: 三个通道值向量
- `Err(HazeError)`: 参数错误

### Rust/Python 示例

```rust
use haze_library::indicators::volatility::donchian_channel;

let high = vec![102.0, 105.0, 104.0, 106.0, 103.0];
let low = vec![99.0, 101.0, 100.0, 102.0, 98.0];

let (upper, middle, lower) = donchian_channel(&high, &low, 3).unwrap();
assert_eq!(upper[2], 105.0);  // 前 3 个最高价的 MAX
assert_eq!(lower[2], 99.0);   // 前 3 个最低价的 MIN
assert_eq!(middle[2], 102.0); // (105 + 99) / 2
```

```python
import haze_library as haze
import pandas as pd

df = pd.DataFrame({'high': high, 'low': low})
df['dc_upper'], df['dc_middle'], df['dc_lower'] = df.haze.donchian_channel(20)

# 突破策略
df['long_signal'] = df['close'] > df['dc_upper'].shift(1)
df['short_signal'] = df['close'] < df['dc_lower'].shift(1)
```

### 应用

- 海龟交易法则核心指标
- 突破交易系统
- 支撑/阻力位识别
- 趋势跟踪

---

## 7. Chandelier Exit

**函数签名**: `chandelier_exit(high: &[f64], low: &[f64], close: &[f64], period: usize, atr_period: usize, multiplier: f64) -> HazeResult<(Vec<f64>, Vec<f64>)>`

**模块**: `indicators::volatility`

### 描述

吊灯止损 (Chandelier Exit) 是基于波动率的跟踪止损系统,使用 ATR 为多头和空头仓位设置退出水平。

### 算法

```text
多头止损 (Long Exit)  = MAX(high, period) - ATR(atr_period) * multiplier
空头止损 (Short Exit) = MIN(low, period) + ATR(atr_period) * multiplier
```

### 参数

- `high`: 最高价序列
- `low`: 最低价序列
- `close`: 收盘价序列
- `period`: 最高价/最低价回溯周期 (通常 22)
- `atr_period`: ATR 周期 (通常 22)
- `multiplier`: ATR 倍数 (通常 3.0)

### 返回值

- `Ok((long_exit, short_exit))`: 两个止损水平向量
- `Err(HazeError)`: 参数错误

### Rust/Python 示例

```rust
use haze_library::indicators::volatility::chandelier_exit;

let high = vec![102.0, 105.0, 104.0, 106.0, 108.0, 110.0];
let low = vec![99.0, 101.0, 100.0, 102.0, 104.0, 106.0];
let close = vec![101.0, 103.0, 102.0, 105.0, 107.0, 109.0];

let (long_exit, short_exit) = chandelier_exit(
    &high, &low, &close,
    3,    // 周期
    3,    // ATR 周期
    3.0   // 倍数
).unwrap();
```

```python
import haze_library as haze
import pandas as pd

df = pd.DataFrame({'high': high, 'low': low, 'close': close})
df['long_stop'], df['short_stop'] = df.haze.chandelier_exit(22, 22, 3.0)

# 动态止损管理
df['stop_loss'] = df.apply(
    lambda x: x['long_stop'] if x['position'] > 0 else x['short_stop'],
    axis=1
)
```

### 应用

- 趋势跟踪止损
- 动态风险管理
- 自适应波动率止损
- 与 SuperTrend 配合使用

---

# 专业波动率指标

## 8. Historical Volatility

**函数签名**: `historical_volatility(close: &[f64], period: usize) -> HazeResult<Vec<f64>>`

**算法**: `HV = StdDev(log_returns, period) * sqrt(period) * 100`

**典型参数**: period=20

**应用**: 期权定价、风险评估、波动率交易

---

## 9. Ulcer Index

**函数签名**: `ulcer_index(close: &[f64], period: usize) -> HazeResult<Vec<f64>>`

**算法**:
```text
drawdown[i] = ((close[i] - max_close) / max_close) * 100
Ulcer Index = sqrt(mean(drawdown^2))
```

**典型参数**: period=14

**应用**: 下行风险测量、回撤深度和持续时间评估

---

## 10. Mass Index

**函数签名**: `mass_index(high: &[f64], low: &[f64], period: usize, ema_period: usize) -> HazeResult<Vec<f64>>`

**算法**:
```text
Range = high - low
EMA1  = EMA(Range, ema_period)
EMA2  = EMA(EMA1, ema_period)
Ratio = EMA1 / EMA2
Mass Index = Sum(Ratio, period)
```

**典型参数**: period=25, ema_period=9

**反转信号**: Mass Index 升至 27 以上后跌破 26.5 为"反转凸起"

**应用**: 趋势反转识别、波动率区间扩张检测

---

## 通用使用模式

### 批量计算多个波动率指标

```python
import haze_library as haze
import pandas as pd

# 加载 OHLCV 数据
df = pd.DataFrame({
    'high': high_data,
    'low': low_data,
    'close': close_data
})

# 方法 1: 使用 DataFrame Accessor 批量计算
df['atr_14'] = df.haze.atr(14)
df['natr_14'] = df.haze.natr(14)
df['bb_upper'], df['bb_middle'], df['bb_lower'] = df.haze.bollinger_bands(20, 2.0)
df['kc_upper'], df['kc_middle'], df['kc_lower'] = df.haze.keltner_channel(20, 10, 2.0)
df['dc_upper'], df['dc_middle'], df['dc_lower'] = df.haze.donchian_channel(20)

# 方法 2: 批量比较波动率指标
volatility_metrics = {
    'atr': df.haze.atr(14),
    'natr': df.haze.natr(14),
    'hv': haze.py_historical_volatility(df['close'].tolist(), 20),
    'ulcer': haze.py_ulcer_index(df['close'].tolist(), 14)
}
vol_df = pd.DataFrame(volatility_metrics)

# 方法 3: 波动率排名
df['vol_percentile'] = df['atr_14'].rolling(100).apply(
    lambda x: (x.iloc[-1] > x).sum() / len(x)
)
```

### Squeeze 检测 (Bollinger + Keltner)

```python
# Bollinger Squeeze 检测
df['bb_upper'], df['bb_middle'], df['bb_lower'] = df.haze.bollinger_bands(20, 2.0)
df['kc_upper'], df['kc_middle'], df['kc_lower'] = df.haze.keltner_channel(20, 10, 1.5)

# Squeeze 条件: Bollinger 完全在 Keltner 内部
df['squeeze'] = (df['bb_upper'] < df['kc_upper']) & (df['bb_lower'] > df['kc_lower'])
df['squeeze_release'] = df['squeeze'].shift(1) & ~df['squeeze']

# 突破方向
df.loc[df['squeeze_release'], 'breakout_direction'] = df['close'] > df['bb_middle']
```

### 动态止损系统

```python
# 结合 ATR 和 Chandelier Exit
df['atr_14'] = df.haze.atr(14)
df['long_stop'], df['short_stop'] = df.haze.chandelier_exit(22, 22, 3.0)

# 自适应止损距离
df['stop_distance'] = 2.5 * df['atr_14']
df['dynamic_long_stop'] = df['close'] - df['stop_distance']
df['dynamic_short_stop'] = df['close'] + df['stop_distance']

# 选择更保守的止损
df['final_long_stop'] = df[['long_stop', 'dynamic_long_stop']].min(axis=1)
df['final_short_stop'] = df[['short_stop', 'dynamic_short_stop']].max(axis=1)
```

---

## 性能对比

| 指标 | 时间复杂度 | 主要算法 | 适用场景 |
|------|------------|----------|----------|
| ATR | O(n) | Wilder 平滑 | 通用波动率测量 |
| Bollinger Bands | O(n) | Welford 算法 | 震荡市场,均值回归 |
| Keltner Channel | O(n) | EMA + ATR | 趋势跟踪 |
| Donchian Channel | O(n) | 单调队列 | 突破交易 |
| Chandelier Exit | O(n) | 滚动极值 + ATR | 趋势止损 |
| Historical Volatility | O(n) | 对数收益率 StdDev | 期权定价 |
| Ulcer Index | O(n) | 回撤平方根 | 下行风险 |
| Mass Index | O(n) | 双重 EMA | 反转识别 |

---

## 设计原则

本模块严格遵循 Haze-Library 核心设计哲学:

- **KISS 原则**: 每个函数职责单一,算法清晰
- **YAGNI 原则**: 仅实现必要功能,避免过度工程化
- **SOLID 原则**: 模块化设计,便于扩展
- **数值稳定性**: 使用 Welford 算法、Kahan 求和保证精度
- **性能优先**: O(n) 复杂度,单次遍历,低内存分配

---

## 相关文档

- [Momentum Indicators (动量指标)](./momentum.md)
- [Trend Indicators (趋势指标)](./trend.md)
- [Architecture Overview (架构总览)](../../ARCHITECTURE.md)
- [Error Handling Strategy (错误处理策略)](../../ERROR_HANDLING_STRATEGY.md)
