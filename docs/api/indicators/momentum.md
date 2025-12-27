# 动量指标模块 (Momentum Indicators)

**模块路径**: `haze_library::indicators::momentum`
**函数数量**: 14 个
**Rust 源文件**: `rust/src/indicators/momentum.rs` (1,585 行)

---

## 📋 目录

| 指标 | Python 函数 | Rust 函数 | 类型 |
|------|------------|-----------|------|
| [RSI](#rsi) | `py_rsi` | `rsi` | 核心 ⭐ |
| [MACD](#macd) | `py_macd` | `macd` | 核心 ⭐ |
| [Stochastic](#stochastic) | `py_stochastic` | `stochastic` | 核心 ⭐ |
| [Stochastic RSI](#stochrsi) | `py_stoch_rsi` | `stochrsi` | 常用 |
| [CCI](#cci) | `py_cci` | `cci` | 常用 |
| [Williams %R](#williams_r) | `py_williams_r` | `williams_r` | 常用 |
| [Awesome Oscillator](#awesome_oscillator) | `py_awesome_oscillator` | `awesome_oscillator` | 常用 |
| [Fisher Transform](#fisher_transform) | `py_fisher_transform` | `fisher_transform` | 常用 |
| [KDJ](#kdj) | `py_kdj` | `kdj` | 专业 |
| [TSI](#tsi) | `py_tsi` | `tsi` | 专业 |
| [Ultimate Oscillator](#ultimate_oscillator) | `py_ultimate_oscillator` | `ultimate_oscillator` | 专业 |
| [APO](#apo) | `py_apo` | `apo` | 简化 |
| [PPO](#ppo) | `py_ppo` | `ppo` | 简化 |
| [CMO](#cmo) | `py_cmo` | `cmo` | 简化 |

---

## 模块概述

动量指标用于测量价格变化的速度和幅度，帮助识别：
- **超买/超卖状态**：RSI, Stochastic, Williams %R
- **趋势强度**：MACD, TSI, Ultimate Oscillator
- **潜在反转点**：Fisher Transform, Awesome Oscillator

### 性能特征
- **时间复杂度**: 所有指标均为 O(n)
- **空间复杂度**: O(n) 用于中间计算
- **优化技术**: Wilder's smoothing, 单次遍历, Monotonic deque

### 错误处理
所有函数返回 `HazeResult<T>`，可能的错误：
- `HazeError::EmptyInput` - 输入数组为空
- `HazeError::InvalidPeriod` - 周期参数无效 (period = 0 或 period > data_len)
- `HazeError::InsufficientData` - 数据长度不足
- `HazeError::LengthMismatch` - 多数组长度不一致

---

## 核心指标详解

<a name="rsi"></a>
### 1. RSI - 相对强弱指标

#### 函数签名

```rust
pub fn rsi(close: &[f64], period: usize) -> HazeResult<Vec<f64>>
```

```python
def py_rsi(close: List[float], period: int = 14) -> List[float]
```

#### 描述

RSI (Relative Strength Index) 是一个动量震荡指标，测量价格变化的速度和幅度。取值范围 0-100，通常 >70 表示超买，<30 表示超卖。

#### 算法

```text
1. 计算价格变化: change[i] = close[i] - close[i-1]
2. 分离涨跌:
   gain[i] = max(change[i], 0)
   loss[i] = max(-change[i], 0)
3. 初始平均值 (简单平均):
   avg_gain = SMA(gain[1..=period])
   avg_loss = SMA(loss[1..=period])
4. Wilder's 平滑 (指数平滑):
   avg_gain[i] = (avg_gain[i-1] × (period-1) + gain[i]) / period
   avg_loss[i] = (avg_loss[i-1] × (period-1) + loss[i]) / period
5. 相对强度:
   RS = avg_gain / avg_loss
6. RSI 计算:
   RSI = 100 - (100 / (1 + RS))

特殊情况:
- avg_loss = 0 且 avg_gain > 0: RSI = 100
- 两者均为 0: RSI = 0
```

#### 参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `close` | `&[f64]` / `List[float]` | - | 收盘价序列 |
| `period` | `usize` / `int` | 14 | 回看周期（通常 14） |

#### 返回值

- **Rust**: `HazeResult<Vec<f64>>` - RSI 值序列 (0-100)
- **Python**: `List[float]` - RSI 值序列

**Warmup 期**: 前 `period` 个值为 `NaN`，有效值从 `index = period` 开始

#### 错误场景

- `EmptyInput`: close 为空
- `InvalidPeriod`: period = 0
- `InsufficientData`: period >= len(close)

#### 性能

- **时间复杂度**: O(n) 单次遍历
- **空间复杂度**: O(n) gain/loss 数组
- **优化**: Wilder's smoothing 避免重复计算

#### Rust 示例

```rust
use haze_library::indicators::momentum::rsi;

let close = vec![
    44.0, 44.25, 44.5, 44.0, 43.75, 44.0, 44.25, 44.5,
    44.75, 45.0, 45.25, 45.0, 44.75, 45.0, 45.25, 45.5, 46.0
];

let rsi_values = rsi(&close, 14)?;

// 前 14 个值为 NaN
assert!(rsi_values[0].is_nan());
assert!(rsi_values[13].is_nan());

// 第 15 个值开始有效
let rsi_14 = rsi_values[14];
assert!(!rsi_14.is_nan());
assert!(rsi_14 >= 0.0 && rsi_14 <= 100.0);

// 交易信号
if rsi_14 > 70.0 {
    println!("超买信号");
} else if rsi_14 < 30.0 {
    println!("超卖信号");
}
```

#### Python 示例

```python
import haze_library as haze
import pandas as pd

# 方式 1: 直接调用
close = [44.0, 44.25, 44.5, 44.0, 43.75, 44.0, 44.25, 44.5,
         44.75, 45.0, 45.25, 45.0, 44.75, 45.0, 45.25, 45.5, 46.0]

rsi = haze.py_rsi(close, period=14)
print(f"RSI (第15个值): {rsi[14]:.2f}")

# 方式 2: DataFrame accessor (推荐)
df = pd.DataFrame({'close': close})
df['rsi_14'] = df.haze.rsi(14)
df['signal'] = df['rsi_14'].apply(
    lambda x: 'Overbought' if x > 70 else ('Oversold' if x < 30 else 'Neutral')
)

# 方式 3: Series accessor
rsi_series = df['close'].haze.rsi(14)
```

#### 交易解读

| RSI 值 | 状态 | 交易信号 |
|--------|------|---------|
| 70-100 | 超买 | 考虑卖出 |
| 30-70 | 中性 | 持有/观望 |
| 0-30 | 超卖 | 考虑买入 |

**背离信号**:
- **看涨背离**: 价格创新低，RSI 未创新低 → 买入信号
- **看跌背离**: 价格创新高，RSI 未创新高 → 卖出信号

#### 相关函数

- [`stochrsi`](#stochrsi) - Stochastic RSI (RSI 的随机指标版本)
- [`cmo`](#cmo) - Chande Momentum Oscillator (类似概念，不同归一化)
- [`williams_r`](#williams_r) - Williams %R (另一种超买/超卖指标)

#### 参考资料

- Wilder, J. W. (1978). *New Concepts in Technical Trading Systems*
- 标准周期: 14 (日线图), 可根据时间框架调整

---

<a name="macd"></a>
### 2. MACD - 指数平滑异同移动平均线

#### 函数签名

```rust
pub fn macd(
    close: &[f64],
    fast_period: usize,
    slow_period: usize,
    signal_period: usize
) -> HazeResult<(Vec<f64>, Vec<f64>, Vec<f64>)>
```

```python
def py_macd(
    close: List[float],
    fast: int = 12,
    slow: int = 26,
    signal: int = 9
) -> Tuple[List[float], List[float], List[float]]
```

#### 描述

MACD 是一个趋势跟随动量指标，显示两个移动平均线之间的关系。由三部分组成：MACD 线、信号线和柱状图。广泛用于识别趋势方向、强度和潜在反转点。

#### 算法

```text
1. MACD 线 = EMA(close, fast_period) - EMA(close, slow_period)
2. 信号线 = EMA(MACD 线, signal_period)
3. 柱状图 = MACD 线 - 信号线

交易信号:
- 看涨: MACD 向上穿越信号线 (柱状图 > 0)
- 看跌: MACD 向下穿越信号线 (柱状图 < 0)
- 背离: 价格和 MACD 反向运动
```

**实现细节** (遵循 TA-Lib 约定):
- 快速 EMA 在 `slow_period - 1` 处重新播种以对齐
- MACD 线在 `lookback` 前的值设为 NaN
- Lookback 周期 = `slow_period + signal_period - 2`

#### 参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `close` | `&[f64]` / `List[float]` | - | 收盘价序列 |
| `fast_period` | `usize` / `int` | 12 | 快速 EMA 周期 |
| `slow_period` | `usize` / `int` | 26 | 慢速 EMA 周期 |
| `signal_period` | `usize` / `int` | 9 | 信号线 EMA 周期 |

#### 返回值

- **Rust**: `HazeResult<(Vec<f64>, Vec<f64>, Vec<f64>)>`
- **Python**: `Tuple[List[float], List[float], List[float]]`

返回三个向量：
1. **MACD 线**: 快慢 EMA 之差
2. **信号线**: MACD 线的 EMA
3. **柱状图**: MACD 线与信号线之差

所有向量长度与输入相同，前 `lookback` 个值为 NaN。

#### 错误场景

- `EmptyInput`: close 为空
- `InvalidPeriod`: 任意周期参数为 0
- `InvalidPeriod`: fast_period 约束违反
- `InsufficientData`: slow_period > data 长度
- `InsufficientData`: lookback >= data 长度

#### 性能

- **时间复杂度**: O(n)
- **空间复杂度**: O(n) EMA 中间计算
- **优化**: 高效单次遍历 EMA + 种子索引

#### Rust 示例

```rust
use haze_library::indicators::momentum::macd;

let close = vec![
    100.0, 101.0, 102.0, 103.0, 104.0, 105.0, 104.5, 104.0,
    105.0, 106.0, 107.0, 108.0, 109.0, 110.0, 111.0, 112.0,
    113.0, 114.0, 115.0, 116.0, 117.0, 118.0, 119.0, 120.0,
    121.0, 122.0, 123.0, 124.0, 125.0, 126.0, 127.0, 128.0,
    129.0, 130.0, 131.0
];

// 标准 MACD 12/26/9 设置
let (macd_line, signal, histogram) = macd(&close, 12, 26, 9)?;

assert_eq!(macd_line.len(), close.len());
assert_eq!(signal.len(), close.len());
assert_eq!(histogram.len(), close.len());

// 检查看涨交叉 (柱状图转正)
let lookback = 26 + 9 - 2; // 33
if close.len() > lookback {
    let hist = histogram[lookback];
    if hist > 0.0 {
        println!("看涨信号：MACD 上穿信号线");
    } else if hist < 0.0 {
        println!("看跌信号：MACD 下穿信号线");
    }
}
```

#### Python 示例

```python
import haze_library as haze
import pandas as pd
import numpy as np

close = [100.0, 101.0, 102.0, 103.0, 104.0, 105.0, 104.5, 104.0,
         105.0, 106.0, 107.0, 108.0, 109.0, 110.0, 111.0, 112.0,
         113.0, 114.0, 115.0, 116.0, 117.0, 118.0, 119.0, 120.0,
         121.0, 122.0, 123.0, 124.0, 125.0, 126.0, 127.0, 128.0,
         129.0, 130.0, 131.0]

# 方式 1: 直接调用
macd_line, signal_line, histogram = haze.py_macd(close, fast=12, slow=26, signal=9)

# 方式 2: DataFrame accessor
df = pd.DataFrame({'close': close})
macd_result = df.haze.macd(fast=12, slow=26, signal=9)
df[['macd', 'signal', 'histogram']] = pd.DataFrame(macd_result).T

# 识别交叉信号
df['prev_hist'] = df['histogram'].shift(1)
df['cross_up'] = (df['histogram'] > 0) & (df['prev_hist'] <= 0)
df['cross_down'] = (df['histogram'] < 0) & (df['prev_hist'] >= 0)

# 可视化
import matplotlib.pyplot as plt
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

# 价格图
ax1.plot(df.index, df['close'], label='Close Price')
ax1.set_ylabel('Price')
ax1.legend()
ax1.grid(True)

# MACD 图
ax2.plot(df.index, df['macd'], label='MACD', color='blue')
ax2.plot(df.index, df['signal'], label='Signal', color='red')
ax2.bar(df.index, df['histogram'], label='Histogram', color='gray', alpha=0.3)
ax2.axhline(0, color='black', linewidth=0.5)
ax2.set_ylabel('MACD')
ax2.set_xlabel('Index')
ax2.legend()
ax2.grid(True)

plt.tight_layout()
plt.show()
```

#### 交易解读

| 信号类型 | 条件 | 交易动作 |
|---------|------|---------|
| **看涨交叉** | MACD 上穿信号线 (histogram 转正) | 买入信号 |
| **看跌交叉** | MACD 下穿信号线 (histogram 转负) | 卖出信号 |
| **零线交叉** | MACD 穿越零线 | 趋势变化 |
| **背离** | 价格与 MACD 反向 | 动量减弱/增强 |

**中心线解读**:
- MACD > 0: 看涨偏向 (快速 EMA > 慢速 EMA)
- MACD < 0: 看跌偏向 (快速 EMA < 慢速 EMA)

#### 相关函数

- [`apo`](#apo) - 绝对价格振荡器 (MACD 无信号线版本)
- [`ppo`](#ppo) - 百分比价格振荡器 (MACD 百分比版本)
- [`ema`](../utils/moving_averages.md#ema) - 指数移动平均 (MACD 基础)

#### 参考资料

- Gerald Appel (1979). *The Moving Average Convergence-Divergence Method*
- 标准参数: 12/26/9 (日线图)
- TA-Lib 兼容实现

---

<a name="stochastic"></a>
### 3. Stochastic - 随机指标

#### 函数签名

```rust
pub fn stochastic(
    high: &[f64],
    low: &[f64],
    close: &[f64],
    k_period: usize,
    d_period: usize
) -> HazeResult<(Vec<f64>, Vec<f64>)>
```

```python
def py_stochastic(
    high: List[float],
    low: List[float],
    close: List[float],
    k_period: int = 14,
    d_period: int = 3
) -> Tuple[List[float], List[float]]
```

#### 描述

随机指标是一个动量震荡指标，比较特定收盘价与一定周期内的价格范围。通过 %K 和 %D 两条线显示价格在区间内的相对位置，范围 0-100。

#### 算法

```text
1. %K 线 (快速随机):
   %K[i] = 100 × (Close[i] - Low_min) / (High_max - Low_min)
   其中:
   Low_min = min(Low[i-k_period+1 ... i])
   High_max = max(High[i-k_period+1 ... i])

2. %D 线 (慢速随机, %K 的 SMA):
   %D[i] = SMA(%K, d_period)

交易信号:
- 超买: %K > 80
- 超卖: %K < 20
- 看涨: %K 上穿 %D
- 看跌: %K 下穿 %D
```

#### 参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `high` | `&[f64]` / `List[float]` | - | 最高价序列 |
| `low` | `&[f64]` / `List[float]` | - | 最低价序列 |
| `close` | `&[f64]` / `List[float]` | - | 收盘价序列 |
| `k_period` | `usize` / `int` | 14 | %K 线周期 |
| `d_period` | `usize` / `int` | 3 | %D 线周期 (SMA 平滑) |

#### 返回值

- **Rust**: `HazeResult<(Vec<f64>, Vec<f64>)>`
- **Python**: `Tuple[List[float], List[float]]`

返回两个向量：
1. **%K 线**: 快速随机指标 (0-100)
2. **%D 线**: %K 的平滑线 (0-100)

#### 性能

- **时间复杂度**: O(n) 使用 Monotonic deque 优化 rolling max/min
- **空间复杂度**: O(k_period) deque 空间

#### Rust 示例

```rust
use haze_library::indicators::momentum::stochastic;

let high = vec![110.0, 112.0, 115.0, 114.0, 113.0, 116.0, 118.0, 120.0,
                119.0, 121.0, 123.0, 122.0, 124.0, 125.0, 127.0];
let low =  vec![105.0, 107.0, 110.0, 109.0, 108.0, 111.0, 113.0, 115.0,
                114.0, 116.0, 118.0, 117.0, 119.0, 120.0, 122.0];
let close = vec![108.0, 110.0, 113.0, 112.0, 111.0, 114.0, 116.0, 118.0,
                 117.0, 119.0, 121.0, 120.0, 122.0, 123.0, 125.0];

let (k_line, d_line) = stochastic(&high, &low, &close, 14, 3)?;

// 交易信号
let last_k = k_line[k_line.len() - 1];
let last_d = d_line[d_line.len() - 1];

if last_k > 80.0 {
    println!("超买区域");
} else if last_k < 20.0 {
    println!("超卖区域");
}

if last_k > last_d {
    println!("看涨信号：%K 在 %D 上方");
}
```

#### Python 示例

```python
import haze_library as haze
import pandas as pd

high = [110.0, 112.0, 115.0, 114.0, 113.0, 116.0, 118.0, 120.0,
        119.0, 121.0, 123.0, 122.0, 124.0, 125.0, 127.0]
low =  [105.0, 107.0, 110.0, 109.0, 108.0, 111.0, 113.0, 115.0,
        114.0, 116.0, 118.0, 117.0, 119.0, 120.0, 122.0]
close = [108.0, 110.0, 113.0, 112.0, 111.0, 114.0, 116.0, 118.0,
         117.0, 119.0, 121.0, 120.0, 122.0, 123.0, 125.0]

# 计算随机指标
k_line, d_line = haze.py_stochastic(high, low, close, k_period=14, d_period=3)

# DataFrame 集成
df = pd.DataFrame({'high': high, 'low': low, 'close': close})
df['stoch_k'], df['stoch_d'] = haze.py_stochastic(
    df['high'].values, df['low'].values, df['close'].values, 14, 3
)

# 识别交叉
df['k_cross_d'] = (df['stoch_k'] > df['stoch_d']) & \
                  (df['stoch_k'].shift(1) <= df['stoch_d'].shift(1))
```

#### 交易解读

| 区域 | 范围 | 信号 |
|------|------|------|
| 超买 | %K > 80 | 考虑卖出 |
| 中性 | 20 < %K < 80 | 观望 |
| 超卖 | %K < 20 | 考虑买入 |

**交叉信号**:
- **金叉**: %K 上穿 %D → 买入
- **死叉**: %K 下穿 %D → 卖出

#### 相关函数

- [`stochrsi`](#stochrsi) - Stochastic RSI (将 Stochastic 应用于 RSI)
- [`kdj`](#kdj) - KDJ 指标 (Stochastic 扩展，增加 J 线)
- [`williams_r`](#williams_r) - Williams %R (类似原理)

---

## 常用指标

<a name="stochrsi"></a>
### 4. Stochastic RSI

#### 函数签名
```rust
pub fn stochrsi(
    close: &[f64],
    rsi_period: usize,
    stoch_period: usize,
    k_period: usize,
    d_period: usize
) -> HazeResult<(Vec<f64>, Vec<f64>)>
```

#### 描述
Stochastic RSI 将 Stochastic 公式应用于 RSI 值，创建更敏感的振荡器。返回 %K 和 %D 两条线。

#### 典型调用
```python
k, d = haze.py_stoch_rsi(close, rsi_period=14, stoch_period=14, k_period=3, d_period=3)
```

---

<a name="cci"></a>
### 5. CCI - 商品通道指数

#### 函数签名
```rust
pub fn cci(high: &[f64], low: &[f64], close: &[f64], period: usize) -> HazeResult<Vec<f64>>
```

#### 描述
CCI 测量价格相对于统计平均值的偏离程度。取值无界限，但通常在 -100 到 +100 之间。

#### 算法
```text
1. TP[i] = (High[i] + Low[i] + Close[i]) / 3  # 典型价格
2. SMA_TP = SMA(TP, period)
3. Mean Deviation = SMA(|TP - SMA_TP|, period)
4. CCI = (TP - SMA_TP) / (0.015 × Mean Deviation)
```

#### 典型调用
```python
cci = haze.py_cci(high, low, close, period=20)

# 信号:
# CCI > 100: 超买
# CCI < -100: 超卖
```

---

<a name="williams_r"></a>
### 6. Williams %R

#### 函数签名
```rust
pub fn williams_r(high: &[f64], low: &[f64], close: &[f64], period: usize) -> HazeResult<Vec<f64>>
```

#### 描述
Williams %R 是一个动量指标，范围 -100 到 0。与 Stochastic 相似但反向。

#### 算法
```text
%R = -100 × (High_max - Close) / (High_max - Low_min)

其中:
High_max = max(High[i-period+1 ... i])
Low_min = min(Low[i-period+1 ... i])
```

#### 典型调用
```python
williams = haze.py_williams_r(high, low, close, period=14)

# 信号:
# %R > -20: 超买
# %R < -80: 超卖
```

---

<a name="awesome_oscillator"></a>
### 7. Awesome Oscillator

#### 函数签名
```rust
pub fn awesome_oscillator(
    high: &[f64],
    low: &[f64],
    fast_period: usize,
    slow_period: usize
) -> HazeResult<Vec<f64>>
```

#### 描述
Awesome Oscillator 通过中位价的移动平均差异来衡量市场动量。

#### 算法
```text
1. Median Price = (High + Low) / 2
2. AO = SMA(Median, fast) - SMA(Median, slow)
```

#### 典型调用
```python
ao = haze.py_awesome_oscillator(high, low, fast=5, slow=34)

# 信号:
# AO > 0: 看涨
# AO < 0: 看跌
# AO 上升: 动量增强
```

---

<a name="fisher_transform"></a>
### 8. Fisher Transform

#### 函数签名
```rust
pub fn fisher_transform(
    high: &[f64],
    low: &[f64],
    period: usize
) -> HazeResult<(Vec<f64>, Vec<f64>)>
```

#### 描述
Fisher Transform 将价格转换为接近高斯正态分布，使转折点更明显。返回 Fisher 线和信号线。

#### 算法
```text
1. Value = 0.5 × ln((1 + X) / (1 - X))
   其中 X = (Price - Min) / (Max - Min) × 2 - 1
2. Fisher = α × Value + (1 - α) × Fisher[i-1]
3. Signal = Fisher[i-1]
```

#### 典型调用
```python
fisher, signal = haze.py_fisher_transform(high, low, period=10)

# 信号:
# Fisher 上穿 Signal: 买入
# Fisher 下穿 Signal: 卖出
```

---

## 专业指标

<a name="kdj"></a>
### 9. KDJ

#### 函数签名
```rust
pub fn kdj(
    high: &[f64],
    low: &[f64],
    close: &[f64],
    k_period: usize,
    d_period: usize
) -> HazeResult<(Vec<f64>, Vec<f64>, Vec<f64>)>
```

#### 描述
KDJ 是 Stochastic 的扩展，增加了 J 线 (J = 3K - 2D)，提供更敏感的信号。

#### 典型调用
```python
k, d, j = haze.py_kdj(high, low, close, k_period=9, d_period=3)
```

---

<a name="tsi"></a>
### 10. TSI - 真实强度指数

#### 函数签名
```rust
pub fn tsi(
    close: &[f64],
    long_period: usize,
    short_period: usize,
    signal_period: usize
) -> HazeResult<(Vec<f64>, Vec<f64>)>
```

#### 描述
TSI 使用双重平滑的动量来减少噪音并识别趋势方向。

#### 典型调用
```python
tsi, signal = haze.py_tsi(close, long_period=25, short_period=13, signal_period=13)
```

---

<a name="ultimate_oscillator"></a>
### 11. Ultimate Oscillator - 终极振荡器

#### 函数签名
```rust
pub fn ultimate_oscillator(
    high: &[f64],
    low: &[f64],
    close: &[f64],
    period1: usize,
    period2: usize,
    period3: usize
) -> HazeResult<Vec<f64>>
```

#### 描述
终极振荡器结合三个不同时间框架的加权动量，减少虚假信号。

#### 典型调用
```python
uo = haze.py_ultimate_oscillator(high, low, close, period1=7, period2=14, period3=28)
```

---

## 简化指标

<a name="apo"></a>
### 12. APO - 绝对价格振荡器

#### 函数签名
```rust
pub fn apo(close: &[f64], fast_period: usize, slow_period: usize) -> HazeResult<Vec<f64>>
```

#### 描述
APO 是 MACD 的简化版本，仅计算快慢 EMA 之差，无信号线。

#### 典型调用
```python
apo = haze.py_apo(close, fast_period=12, slow_period=26)
```

---

<a name="ppo"></a>
### 13. PPO - 百分比价格振荡器

#### 函数签名
```rust
pub fn ppo(close: &[f64], fast_period: usize, slow_period: usize) -> HazeResult<Vec<f64>>
```

#### 描述
PPO 是 MACD 的百分比版本，将差值表示为慢速 EMA 的百分比。

#### 算法
```text
PPO = 100 × (EMA(fast) - EMA(slow)) / EMA(slow)
```

#### 典型调用
```python
ppo = haze.py_ppo(close, fast_period=12, slow_period=26)
```

---

<a name="cmo"></a>
### 14. CMO - 钱德动量振荡器

#### 函数签名
```rust
pub fn cmo(close: &[f64], period: usize) -> HazeResult<Vec<f64>>
```

#### 描述
CMO 归一化动量指标，范围 -100 到 +100。

#### 算法
```text
CMO = 100 × (Sum(Gains) - Sum(Losses)) / (Sum(Gains) + Sum(Losses))
```

#### 典型调用
```python
cmo = haze.py_cmo(close, period=14)

# 信号:
# CMO > 50: 超买
# CMO < -50: 超卖
```

---

## 通用调用模式

### Python 批量计算示例

```python
import haze_library as haze
import pandas as pd

# 加载数据
df = pd.read_csv('price_data.csv')

# 使用 DataFrame accessor 计算多个指标
df['rsi_14'] = df.haze.rsi(14)
df['macd'], df['signal'], df['hist'] = haze.py_macd(df['close'].values, 12, 26, 9)
df['stoch_k'], df['stoch_d'] = haze.py_stochastic(
    df['high'].values, df['low'].values, df['close'].values, 14, 3
)
df['cci_20'] = haze.py_cci(df['high'].values, df['low'].values, df['close'].values, 20)

# 生成综合交易信号
df['signal_composite'] = (
    (df['rsi_14'] < 30).astype(int) +           # RSI 超卖
    (df['hist'] > 0).astype(int) +              # MACD 看涨
    (df['stoch_k'] > df['stoch_d']).astype(int) # Stochastic 金叉
)

# signal_composite >= 2 为强买入信号
```

### Rust 批量计算示例

```rust
use haze_library::indicators::momentum::*;

// 批量计算多个动量指标
let rsi_values = rsi(&close, 14)?;
let (macd_line, signal, histogram) = macd(&close, 12, 26, 9)?;
let (k_line, d_line) = stochastic(&high, &low, &close, 14, 3)?;
let cci_values = cci(&high, &low, &close, 20)?;

// 综合分析
for i in 35..close.len() {
    let mut signals = 0;

    if rsi_values[i] < 30.0 { signals += 1; }
    if histogram[i] > 0.0 { signals += 1; }
    if k_line[i] > d_line[i] { signals += 1; }

    if signals >= 2 {
        println!("强买入信号 at index {}", i);
    }
}
```

---

## 参考资料

### 书籍
- Wilder, J. W. (1978). *New Concepts in Technical Trading Systems* (RSI, ATR)
- Appel, G. (1979). *The Moving Average Convergence-Divergence Method* (MACD)
- Lane, G. C. (1984). *Lane's Stochastics* (Stochastic Oscillator)

### 在线资源
- [Investopedia - Momentum Indicators](https://www.investopedia.com/terms/m/momentum.asp)
- [TradingView - Technical Indicators](https://www.tradingview.com/scripts/)
- [TA-Lib Documentation](https://ta-lib.org/)

---

**文档更新**: 2025-12-27
**下一篇**: [波动率指标 (Volatility)](volatility.md)

