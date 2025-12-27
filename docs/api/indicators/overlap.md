# Overlap / Moving Average Indicators (移动平均类指标)

**模块路径**: `haze_library::indicators::overlap`

## 概述

移动平均 (Overlap) 指标模块提供各类移动平均线和价格计算工具,用于平滑价格波动、识别趋势方向和动态支撑/阻力位。这些指标是技术分析的基础构建块。

**核心特性**:
- 16 个移动平均与价格计算函数
- 7 个经典 MA 从 `utils::ma` 重导出
- 9 个扩展 Overlap 函数 (价格计算、高级 MA)
- O(n) 时间复杂度,高效滚动计算
- 完整的错误处理与参数验证

**统一错误处理**:
所有函数返回 `HazeResult<T>`,可能的错误类型:
- `HazeError::EmptyInput` - 输入数组为空
- `HazeError::LengthMismatch` - 输入数组长度不一致
- `HazeError::InvalidPeriod` - 周期参数无效
- `HazeError::InsufficientData` - 数据长度不足
- `HazeError::InvalidValue` - 参数值非法

---

## 目录

### 核心移动平均 (完整文档)
1. [SMA - Simple Moving Average (简单移动平均)](#1-sma---simple-moving-average)
2. [EMA - Exponential Moving Average (指数移动平均)](#2-ema---exponential-moving-average)
3. [WMA - Weighted Moving Average (加权移动平均)](#3-wma---weighted-moving-average)

### 常用移动平均 (标准文档)
4. [DEMA - Double Exponential MA (双重指数移动平均)](#4-dema---double-exponential-ma)
5. [TEMA - Triple Exponential MA (三重指数移动平均)](#5-tema---triple-exponential-ma)
6. [HMA - Hull Moving Average (赫尔移动平均)](#6-hma---hull-moving-average)
7. [RMA - Rolling/Wilder's MA (Wilder 平滑)](#7-rma---rollingwilders-ma)

### 价格计算函数 (标准文档)
8. [HL2 - High-Low Midpoint (高低中点)](#8-hl2---high-low-midpoint)
9. [HLC3 - Typical Price (典型价格)](#9-hlc3---typical-price)
10. [OHLC4 - Four-Price Average (四价平均)](#10-ohlc4---four-price-average)
11. [MIDPOINT / MIDPRICE (滚动中点)](#11-midpoint--midprice)

### 高级移动平均 (简化文档)
12. [TRIMA - Triangular MA (三角移动平均)](#12-trima---triangular-ma)
13. [SAR - Parabolic SAR (抛物线转向)](#13-sar---parabolic-sar)
14. [SAREXT - SAR Extended (扩展 SAR)](#14-sarext---sar-extended)
15. [MAMA - MESA Adaptive MA (自适应移动平均)](#15-mama---mesa-adaptive-ma)

---

# 核心移动平均

## 1. SMA - Simple Moving Average

**函数签名**: `sma(values: &[f64], period: usize) -> HazeResult<Vec<f64>>`

**模块**: `indicators::overlap` (re-exported from `utils::ma`)

### 描述

简单移动平均 (SMA) 是最基础的移动平均线,对给定周期内的数据求算术平均值。每个数据点权重相等,计算简单但对旧数据和新数据同等对待。

### 算法

```text
SMA[i] = (values[i] + values[i-1] + ... + values[i-period+1]) / period

其中:
- 前 period-1 个值为 NaN (warmup 期)
- 第 period 个值开始为有效 SMA
```

### 参数

| 参数 | 类型 | 说明 | 典型值 |
|------|------|------|--------|
| `values` | `&[f64]` | 输入数据序列 | close 价格 |
| `period` | `usize` | 移动平均周期 | 5, 10, 20, 50, 200 |

### 返回值

- `Ok(Vec<f64>)`: SMA 值向量
  - 长度与输入相同
  - 前 `period - 1` 个值为 NaN
  - 有效值从 `index = period - 1` 开始
- `Err(HazeError)`: 参数错误

### 性能

- **时间复杂度**: O(n)
- **空间复杂度**: O(n)
- **算法**: 滚动窗口求和 (使用 Kahan 补偿求和保证精度)

### Rust 示例

```rust
use haze_library::indicators::overlap::sma;

let close = vec![100.0, 102.0, 101.0, 105.0, 107.0, 106.0, 108.0, 110.0];

// 计算 5 周期 SMA
let sma_5 = sma(&close, 5).unwrap();

// 前 4 个值为 NaN
assert!(sma_5[0].is_nan());
assert!(sma_5[3].is_nan());

// 第 5 个值开始有效
assert!(!sma_5[4].is_nan());
assert_eq!(sma_5[4], (100.0 + 102.0 + 101.0 + 105.0 + 107.0) / 5.0);
```

### Python 示例

```python
import haze_library as haze
import pandas as pd

# 方法 1: 直接函数调用
close = [100.0, 102.0, 101.0, 105.0, 107.0, 106.0, 108.0, 110.0]
sma_5 = haze.py_sma(close, period=5)

# 方法 2: DataFrame Accessor (推荐)
df = pd.DataFrame({'close': close})
df['sma_5'] = df.haze.sma(5)
df['sma_20'] = df.haze.sma(20)

# 方法 3: Series Accessor
sma_series = df['close'].haze.sma(10)

# 方法 4: 多周期分析
for period in [5, 10, 20, 50, 200]:
    df[f'sma_{period}'] = df.haze.sma(period)
```

### 交易应用

#### 1. 趋势识别
```python
# 价格 vs SMA
if close > sma:
    print("价格在均线之上 - 上升趋势")
else:
    print("价格在均线之下 - 下降趋势")

# 多周期确认
if close > sma_5 > sma_20 > sma_50:
    print("多头排列 - 强势上升趋势")
elif close < sma_5 < sma_20 < sma_50:
    print("空头排列 - 强势下降趋势")
```

#### 2. 金叉死叉
```python
# 金叉 (Golden Cross)
if sma_5 > sma_20 and sma_5_prev <= sma_20_prev:
    print("金叉 - 短期均线上穿长期均线 - 买入信号")

# 死叉 (Death Cross)
if sma_5 < sma_20 and sma_5_prev >= sma_20_prev:
    print("死叉 - 短期均线下穿长期均线 - 卖出信号")
```

#### 3. 动态支撑/阻力
```python
# SMA 作为支撑/阻力位
if close > sma_50:
    support_level = sma_50
    print(f"SMA50 作为支撑位: {support_level:.2f}")
else:
    resistance_level = sma_50
    print(f"SMA50 作为阻力位: {resistance_level:.2f}")
```

### 常用周期

| 周期 | 类型 | 应用场景 |
|------|------|----------|
| 5 | 超短期 | 日内交易,快速反应 |
| 10 | 短期 | 短期趋势,波段交易 |
| 20 | 中短期 | 布林带中轨,波段交易 |
| 50 | 中期 | 中期趋势判断 |
| 200 | 长期 | 牛熊分界,长期趋势 |

### 优缺点

**优点**:
- 计算简单,易于理解
- 平滑噪音,显示趋势
- 支撑/阻力位明确

**缺点**:
- 滞后性强 (对新数据反应慢)
- 对所有数据同等权重
- 震荡市场频繁假信号

### 相关函数

- [`ema`](#2-ema---exponential-moving-average) - 对近期数据更敏感
- [`wma`](#3-wma---weighted-moving-average) - 线性加权
- [`trima`](#12-trima---triangular-ma) - 双重平滑

---

## 2. EMA - Exponential Moving Average

**函数签名**: `ema(values: &[f64], period: usize) -> HazeResult<Vec<f64>>`

**模块**: `indicators::overlap` (re-exported from `utils::ma`)

### 描述

指数移动平均 (EMA) 对近期数据赋予更高权重,对价格变化反应更快。广泛用于 MACD、ADX、SuperTrend 等指标的基础计算。

### 算法

```text
平滑因子 (Alpha):
α = 2 / (period + 1)

初始值:
EMA[0] = values[0]  或  SMA(values[0..period])

递推公式:
EMA[i] = α × values[i] + (1 - α) × EMA[i-1]
       = values[i] × α + EMA[i-1] × (1 - α)

权重衰减:
- 最新数据权重: α
- 前一期权重: (1-α) × α
- 前两期权重: (1-α)² × α
- ...呈指数衰减
```

### 参数

- `values`: 输入数据序列
- `period`: 周期 (决定平滑因子 α)

### 返回值

- `Ok(Vec<f64>)`: EMA 值向量,第一个值使用 values[0] 初始化

### 性能

- **时间复杂度**: O(n)
- **算法**: 递推计算,单次遍历

### Rust/Python 示例

```rust
use haze_library::indicators::overlap::ema;

let close = vec![100.0, 102.0, 101.0, 105.0, 107.0, 106.0, 108.0, 110.0];
let ema_5 = ema(&close, 5).unwrap();

// EMA 从第一个值开始就有效 (无 warmup 期)
assert!(!ema_5[0].is_nan());
```

```python
import haze_library as haze
import pandas as pd

df = pd.DataFrame({'close': close})
df['ema_12'] = df.haze.ema(12)
df['ema_26'] = df.haze.ema(26)

# MACD 基础
df['macd_line'] = df['ema_12'] - df['ema_26']
df['signal_line'] = df['macd_line'].haze.ema(9)
df['macd_histogram'] = df['macd_line'] - df['signal_line']
```

### 交易应用

#### EMA vs SMA 对比
```python
df['sma_20'] = df.haze.sma(20)
df['ema_20'] = df.haze.ema(20)

# EMA 对价格变化反应更快
if ema_20 > sma_20:
    print("近期价格上涨较快")
elif ema_20 < sma_20:
    print("近期价格下跌较快")
```

#### 常用组合
```python
# 12/26 EMA (MACD 标准参数)
# 5/20/60 EMA (短中长期组合)
# 8/21 EMA (斐波那契数列)
```

### 优缺点

**优点**:
- 对近期数据更敏感
- 反应速度比 SMA 快
- 适合趋势跟踪

**缺点**:
- 震荡市场噪音较多
- 参数敏感度高
- 永远不会完全去除历史数据影响

### 相关函数

- [`sma`](#1-sma---simple-moving-average) - 简单移动平均
- [`dema`](#4-dema---double-exponential-ma) - 双重 EMA
- [`rma`](#7-rma---rollingwilders-ma) - Wilder 平滑 (类似 EMA)

---

## 3. WMA - Weighted Moving Average

**函数签名**: `wma(values: &[f64], period: usize) -> HazeResult<Vec<f64>>`

**模块**: `indicators::overlap` (re-exported from `utils::ma`)

### 描述

加权移动平均 (WMA) 对滚动窗口内的数据进行线性加权,最新数据权重最大,最旧数据权重最小。比 SMA 更敏感,但比 EMA 计算更简单。

### 算法

```text
WMA[i] = (values[i] × period + values[i-1] × (period-1) + ... + values[i-period+1] × 1)
         / (period + (period-1) + ... + 1)

分母 (权重总和):
Sum = period × (period + 1) / 2

示例 (period=3):
WMA = (values[i]×3 + values[i-1]×2 + values[i-2]×1) / (3+2+1)
    = (values[i]×3 + values[i-1]×2 + values[i-2]×1) / 6
```

### 参数

- `values`: 输入数据序列
- `period`: 周期

### 返回值

- `Ok(Vec<f64>)`: WMA 值向量,前 `period - 1` 个值为 NaN

### Rust/Python 示例

```rust
use haze_library::indicators::overlap::wma;

let close = vec![100.0, 102.0, 101.0, 105.0, 107.0];
let wma_3 = wma(&close, 3).unwrap();

// wma_3[2] = (101×3 + 102×2 + 100×1) / 6
//          = (303 + 204 + 100) / 6 = 101.17
```

```python
df['wma_10'] = df.haze.wma(10)

# 与 SMA/EMA 对比
df['sma_10'] = df.haze.sma(10)
df['ema_10'] = df.haze.ema(10)

# 反应速度: WMA > EMA > SMA
```

### 应用

- 比 SMA 对近期价格更敏感
- 比 EMA 计算更透明 (明确的线性权重)
- 适合需要中等灵敏度的场景

### 相关函数

- [`hma`](#6-hma---hull-moving-average) - Hull MA (使用 WMA 构建)

---

# 常用移动平均

## 4. DEMA - Double Exponential MA

**函数签名**: `dema(values: &[f64], period: usize) -> HazeResult<Vec<f64>>`

**描述**: 双重指数移动平均,减少 EMA 滞后性

**算法**:
```text
EMA1 = EMA(values, period)
EMA2 = EMA(EMA1, period)
DEMA = 2 × EMA1 - EMA2
```

**特点**: 比 EMA 更快响应,滞后性更低

---

## 5. TEMA - Triple Exponential MA

**函数签名**: `tema(values: &[f64], period: usize) -> HazeResult<Vec<f64>>`

**描述**: 三重指数移动平均,进一步减少滞后

**算法**:
```text
EMA1 = EMA(values, period)
EMA2 = EMA(EMA1, period)
EMA3 = EMA(EMA2, period)
TEMA = 3 × EMA1 - 3 × EMA2 + EMA3
```

**特点**: 滞后性最低,但噪音较大

---

## 6. HMA - Hull Moving Average

**函数签名**: `hma(values: &[f64], period: usize) -> HazeResult<Vec<f64>>`

**描述**: 赫尔移动平均,由 Alan Hull 开发,兼顾平滑性和响应速度

**算法**:
```text
half_period = period / 2
sqrt_period = sqrt(period)

WMA1 = WMA(values, half_period)
WMA2 = WMA(values, period)
raw_hma = 2 × WMA1 - WMA2
HMA = WMA(raw_hma, sqrt_period)
```

**特点**: 平滑且快速,适合趋势跟踪

**Python 示例**:
```python
df['hma_20'] = df.haze.hma(20)

# HMA 趋势信号
df['hma_trend'] = df['hma_20'].diff() > 0  # True = 上升, False = 下降
```

---

## 7. RMA - Rolling/Wilder's MA

**函数签名**: `rma(values: &[f64], period: usize) -> HazeResult<Vec<f64>>`

**描述**: Wilder 平滑移动平均,由 J. Welles Wilder Jr. 开发,用于 ATR、ADX、RSI 等指标

**算法**:
```text
α = 1 / period  (而非 EMA 的 2/(period+1))

RMA[0] = SMA(values[0..period])
RMA[i] = α × values[i] + (1 - α) × RMA[i-1]
```

**特点**: 比 EMA 更平滑,滞后性更强

**应用**: ATR, ADX, RSI 内部使用

---

# 价格计算函数

## 8. HL2 - High-Low Midpoint

**函数签名**: `hl2(high: &[f64], low: &[f64]) -> HazeResult<Vec<f64>>`

**算法**: `HL2 = (High + Low) / 2`

**应用**: 价格中点,用于 SuperTrend、Pivot Points

---

## 9. HLC3 - Typical Price

**函数签名**: `hlc3(high: &[f64], low: &[f64], close: &[f64]) -> HazeResult<Vec<f64>>`

**算法**: `HLC3 = (High + Low + Close) / 3`

**应用**: 典型价格,常用于成交量加权指标 (VWAP, MFI)

---

## 10. OHLC4 - Four-Price Average

**函数签名**: `ohlc4(open: &[f64], high: &[f64], low: &[f64], close: &[f64]) -> HazeResult<Vec<f64>>`

**算法**: `OHLC4 = (Open + High + Low + Close) / 4`

**应用**: 四价平均,Heikin Ashi 蜡烛图基础

---

## 11. MIDPOINT / MIDPRICE

**函数签名**:
- `midpoint(values: &[f64], period: usize) -> HazeResult<Vec<f64>>`
- `midprice(high: &[f64], low: &[f64], period: usize) -> HazeResult<Vec<f64>>`

**算法**:
```text
MIDPOINT = (MAX(values, period) + MIN(values, period)) / 2
MIDPRICE = (MAX(high, period) + MIN(low, period)) / 2
```

**应用**: 滚动窗口中点,动态支撑/阻力位

**Python 示例**:
```python
df['midprice_20'] = haze.py_midprice(
    df['high'].tolist(),
    df['low'].tolist(),
    period=20
)

# 与 Donchian Channel 中轨相同
```

---

# 高级移动平均

## 12. TRIMA - Triangular MA

**函数签名**: `trima(values: &[f64], period: usize) -> HazeResult<Vec<f64>>`

**算法**: `TRIMA = SMA(SMA(values, period), ceil(period/2))`

**特点**: 双重平滑,极度平滑但滞后性强

---

## 13. SAR - Parabolic SAR

**函数签名**: `sar(high: &[f64], low: &[f64], acceleration: f64, maximum: f64) -> HazeResult<Vec<f64>>`

**描述**: 抛物线转向指标 (简化版,仅返回 SAR 值,不含趋势方向)

**典型参数**: acceleration=0.02, maximum=0.2

**应用**: 动态止损位

**注意**: 完整的 PSAR 实现在 `trend::psar`,返回 (SAR, trend) 元组

---

## 14. SAREXT - SAR Extended

**函数签名**: `sarext(high, low, start_value, offset_on_reverse, af_init_long, af_long, af_max_long, af_init_short, af_short, af_max_short) -> HazeResult<Vec<f64>>`

**描述**: 扩展版 SAR,提供长短仓不同参数控制

**参数**:
- `start_value`: SAR 起始值 (0 = 自动)
- `offset_on_reverse`: 反转时偏移量
- `af_init_long/short`: 长/短仓初始 AF
- `af_long/short`: 长/短仓 AF 增量
- `af_max_long/short`: 长/短仓最大 AF

---

## 15. MAMA - MESA Adaptive MA

**函数签名**: `mama(values: &[f64], fast_limit: f64, slow_limit: f64) -> HazeResult<(Vec<f64>, Vec<f64>)>`

**描述**: MESA 自适应移动平均,基于 Hilbert Transform 的自适应周期检测

**典型参数**: fast_limit=0.5, slow_limit=0.05

**返回值**: `(MAMA, FAMA)` - MAMA 和 Following Adaptive MA

**特点**: 自适应周期,适应市场节奏变化

**注意**: 当前实现为简化版,完整 Hilbert Transform 实现复杂度较高

---

## 通用使用模式

### 多周期 MA 组合分析

```python
import haze_library as haze
import pandas as pd

df = pd.DataFrame({'close': close_data})

# 批量计算多周期 MA
ma_periods = {
    'sma': [5, 10, 20, 50, 200],
    'ema': [8, 13, 21, 55, 89],  # 斐波那契数列
    'hma': [9, 16, 25]
}

for ma_type, periods in ma_periods.items():
    for period in periods:
        if ma_type == 'sma':
            df[f'sma_{period}'] = df.haze.sma(period)
        elif ma_type == 'ema':
            df[f'ema_{period}'] = df.haze.ema(period)
        elif ma_type == 'hma':
            df[f'hma_{period}'] = df.haze.hma(period)

# MA 排列检测
def ma_alignment(row):
    # 多头排列: SMA5 > SMA20 > SMA50 > SMA200
    if (row['sma_5'] > row['sma_20'] > row['sma_50'] > row['sma_200']):
        return '多头排列'
    # 空头排列: SMA5 < SMA20 < SMA50 < SMA200
    elif (row['sma_5'] < row['sma_20'] < row['sma_50'] < row['sma_200']):
        return '空头排列'
    else:
        return '震荡'

df['ma_alignment'] = df.apply(ma_alignment, axis=1)
```

### 金叉死叉检测系统

```python
def detect_crossovers(df, fast_col, slow_col):
    """检测金叉和死叉"""
    df['cross_type'] = None

    # 金叉: 快线上穿慢线
    golden_cross = (
        (df[fast_col] > df[slow_col]) &
        (df[fast_col].shift(1) <= df[slow_col].shift(1))
    )
    df.loc[golden_cross, 'cross_type'] = 'Golden Cross'

    # 死叉: 快线下穿慢线
    death_cross = (
        (df[fast_col] < df[slow_col]) &
        (df[fast_col].shift(1) >= df[slow_col].shift(1))
    )
    df.loc[death_cross, 'cross_type'] = 'Death Cross'

    return df

# 应用于不同 MA 组合
df = detect_crossovers(df, 'ema_12', 'ema_26')  # MACD 金叉死叉
df = detect_crossovers(df, 'sma_50', 'sma_200')  # 经典金叉死叉
```

### MA 包络线 (Envelope)

```python
# MA 包络线: MA ± 百分比
df['sma_20'] = df.haze.sma(20)
envelope_pct = 0.025  # 2.5%

df['envelope_upper'] = df['sma_20'] * (1 + envelope_pct)
df['envelope_lower'] = df['sma_20'] * (1 - envelope_pct)

# 超买超卖信号
df['overbought'] = df['close'] > df['envelope_upper']
df['oversold'] = df['close'] < df['envelope_lower']
```

### 价格计算综合应用

```python
# 批量计算价格指标
df['hl2'] = haze.py_hl2(df['high'].tolist(), df['low'].tolist())
df['hlc3'] = haze.py_hlc3(df['high'].tolist(), df['low'].tolist(), df['close'].tolist())
df['ohlc4'] = haze.py_ohlc4(
    df['open'].tolist(), df['high'].tolist(),
    df['low'].tolist(), df['close'].tolist()
)

# 使用 HLC3 计算 MA (更平滑)
df['sma_hlc3'] = haze.py_sma(df['hlc3'].tolist(), 20)

# 对比不同价格基准
df['sma_close'] = df.haze.sma(20)
df['sma_hlc3_diff'] = df['sma_hlc3'] - df['sma_close']
```

---

## MA 类型对比

| MA 类型 | 响应速度 | 平滑度 | 滞后性 | 适用场景 |
|---------|----------|--------|--------|----------|
| **SMA** | 慢 | 高 | 高 | 长期趋势,支撑阻力 |
| **EMA** | 快 | 中 | 中 | 趋势跟踪,MACD |
| **WMA** | 中快 | 中 | 中 | 平衡速度与平滑 |
| **DEMA** | 快 | 中低 | 低 | 快速趋势反应 |
| **TEMA** | 极快 | 低 | 极低 | 超短期交易 |
| **HMA** | 快 | 中高 | 低 | 趋势识别,兼顾速度 |
| **RMA** | 慢 | 极高 | 高 | ATR/ADX 内部使用 |
| **TRIMA** | 极慢 | 极高 | 极高 | 极度平滑,过滤噪音 |

## 常用周期参数

| 时间框架 | 短期 MA | 中期 MA | 长期 MA | 应用 |
|----------|---------|---------|---------|------|
| **日内 (1m-15m)** | 9, 21 | 50, 100 | 200 | 日内波段 |
| **日线** | 5, 10, 20 | 50, 60 | 100, 200 | 波段交易 |
| **周线** | 4, 13 | 26, 52 | 104 | 中长期投资 |

---

## 性能对比

| 函数 | 时间复杂度 | 主要算法 | 精度保证 |
|------|------------|----------|----------|
| SMA | O(n) | Kahan 求和 | < 1e-9 误差 |
| EMA | O(n) | 递推 | 浮点精度 |
| WMA | O(n) | 加权求和 | Kahan 求和 |
| DEMA | O(n) | 双重 EMA | 组合误差 |
| TEMA | O(n) | 三重 EMA | 组合误差 |
| HMA | O(n) | WMA 组合 | Kahan 求和 |
| RMA | O(n) | Wilder 平滑 | 浮点精度 |

---

## 设计原则

本模块严格遵循 Haze-Library 核心设计哲学:

- **KISS 原则**: 每个 MA 函数职责单一,算法清晰
- **YAGNI 原则**: 仅实现必要的 MA 类型,避免冗余
- **SOLID 原则**: 从 utils::ma 重导出基础 MA,模块化清晰
- **数值稳定性**: SMA/WMA 使用 Kahan 求和,误差 < 1e-9
- **性能优先**: O(n) 复杂度,单次遍历,低内存分配

---

## 相关文档

- [Momentum Indicators (动量指标)](./momentum.md)
- [Volatility Indicators (波动率指标)](./volatility.md)
- [Trend Indicators (趋势指标)](./trend.md)
- [Utils: MA Module (移动平均工具)](../utils/moving_averages.md)
- [Architecture Overview (架构总览)](../../ARCHITECTURE.md)
