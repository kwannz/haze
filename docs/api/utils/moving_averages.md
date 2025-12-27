# Moving Averages Module / 移动平均工具模块

**模块路径**: `utils::ma` / `haze_library.utils.ma`

**功能定位**: 提供高性能的移动平均计算函数,作为技术指标的构建基础

## 📋 函数清单 (Function Inventory)

### 核心移动平均 (Core Moving Averages)
- [`sma`](#sma---simple-moving-average-简单移动平均) - Simple Moving Average (算术平均)
- [`ema`](#ema---exponential-moving-average-指数移动平均) - Exponential Moving Average (指数加权)
- [`wma`](#wma---weighted-moving-average-加权移动平均) - Weighted Moving Average (线性加权)

### 常用移动平均 (Common Moving Averages)
- [`rma`](#rma---wilders-moving-average-威尔德移动平均) - Wilder's Moving Average (ATR/RSI 专用)
- [`dema`](#dema---double-exponential-moving-average-双重指数移动平均) - Double Exponential MA (减少延迟)
- [`tema`](#tema---triple-exponential-moving-average-三重指数移动平均) - Triple Exponential MA (进一步减少延迟)
- [`hma`](#hma---hull-moving-average-赫尔移动平均) - Hull Moving Average (低延迟平滑)
- [`vwap`](#vwap---volume-weighted-average-price-成交量加权平均价) - Volume Weighted Average Price

### 高级移动平均 (Advanced Moving Averages)
- [`zlma`](#zlma---zero-lag-moving-average-零延迟移动平均) - Zero-Lag Moving Average
- [`t3`](#t3---tillson-t3-moving-average) - Tillson T3 (6 重 EMA)
- [`kama`](#kama---kaufman-adaptive-moving-average-考夫曼自适应移动平均) - Kaufman Adaptive MA
- [`frama`](#frama---fractal-adaptive-moving-average-分形自适应移动平均) - Fractal Adaptive MA

---

## ⭐ 核心函数详细文档

### `sma` - Simple Moving Average / 简单移动平均

**函数签名**:
```rust
pub fn sma(values: &[f64], period: usize) -> HazeResult<Vec<f64>>
```

**模块**: `utils::ma`

**描述**: 计算简单移动平均,使用 Kahan 补偿求和的增量更新算法,定期重新计算以防止浮点误差累积。

**算法**:
```text
SMA[i] = sum(values[i-period+1 .. i+1]) / period

增量更新:
  new_sum = old_sum - old_value + new_value

Kahan 补偿:
  y = value - compensation
  t = sum + y
  compensation = (t - sum) - y
  sum = t

定期重新计算:
  每 1000 次迭代重新计算窗口和以重置累积误差
```

**参数**:
- `values`: `&[f64]` - 输入价格序列
- `period`: `usize` - 移动平均周期

**返回值**:
- `Ok(Vec<f64>)`: 与输入等长的向量
  - 前 `period-1` 个值为 `NaN` (warmup 期)
  - 从索引 `period-1` 开始为有效 SMA 值
- `Err(HazeError)`:
  - `EmptyInput`: 输入为空
  - `InvalidPeriod`: period 为 0 或超过数据长度

**性能**:
- 时间复杂度: O(n) 平均,定期重新计算导致最坏 O(n²/1000)
- 空间复杂度: O(n)
- 数值精度: 相对误差 < 1e-12

**Rust 示例**:
```rust
use haze_library::utils::ma::sma;

let prices = vec![100.0, 101.0, 102.0, 103.0, 104.0, 105.0];
let result = sma(&prices, 3)?;

// result = [NaN, NaN, 101.0, 102.0, 103.0, 104.0]
assert!(result[0].is_nan());
assert_eq!(result[2], 101.0);  // (100+101+102)/3
assert_eq!(result[5], 104.0);  // (103+104+105)/3
```

**Python 示例**:
```python
import haze_library as haze
import pandas as pd

# 方式 1: 直接调用
prices = [100.0, 101.0, 102.0, 103.0, 104.0, 105.0]
sma_values = haze.py_sma(prices, 3)

# 方式 2: DataFrame accessor
df = pd.DataFrame({'close': prices})
df['sma_3'] = df.haze.sma(3)

# 方式 3: 批量计算多周期
for period in [5, 10, 20, 50, 200]:
    df[f'sma_{period}'] = df.haze.sma(period)
```

**交易应用 (Trading Applications)**:

| 策略 | 信号条件 | 含义 | 应用场景 |
|------|---------|------|---------|
| **趋势识别** | Price > SMA | 多头趋势 | 顺势做多 |
| | Price < SMA | 空头趋势 | 顺势做空 |
| **Golden Cross** | SMA(50) 上穿 SMA(200) | 长期看涨 | 牛市确认 |
| **Death Cross** | SMA(50) 下穿 SMA(200) | 长期看跌 | 熊市确认 |
| **多头排列** | SMA(5) > SMA(20) > SMA(50) | 强势上涨 | 加仓做多 |
| **空头排列** | SMA(5) < SMA(20) < SMA(50) | 强势下跌 | 加仓做空 |

**常用周期参数**:
- **短期**: 5, 10 (日内交易)
- **中期**: 20, 50 (波段交易)
- **长期**: 100, 200 (趋势跟踪)
- **经典组合**: (5, 10, 20) / (50, 100, 200)

**相关函数**: [`ema`](#ema---exponential-moving-average-指数移动平均), [`wma`](#wma---weighted-moving-average-加权移动平均), [`rolling_sum`](statistics.md#rolling_sum---滚动求和)

---

### `ema` - Exponential Moving Average / 指数移动平均

**函数签名**:
```rust
pub fn ema(values: &[f64], period: usize) -> HazeResult<Vec<f64>>
```

**模块**: `utils::ma`

**描述**: 计算指数移动平均,对最近的数据赋予更高权重,响应速度快于 SMA。

**算法**:
```text
平滑因子 (Alpha):
α = 2 / (period + 1)

初始值:
EMA[0] = SMA(period)  // 使用前 period 个值的 SMA

递推公式:
EMA[i] = α × values[i] + (1 - α) × EMA[i-1]

权重衰减特性:
- 最新数据权重: α
- 前 1 期权重: (1-α) × α
- 前 2 期权重: (1-α)² × α
- ...呈指数衰减
```

**参数**:
- `values`: `&[f64]` - 输入价格序列
- `period`: `usize` - EMA 周期

**返回值**:
- `Ok(Vec<f64>)`: 与输入等长的向量,前 `period-1` 个值为 `NaN`
- `Err(HazeError)`: 同 SMA

**性能**:
- 时间复杂度: O(n)
- 空间复杂度: O(n)

**Rust 示例**:
```rust
use haze_library::utils::ma::ema;

let prices = vec![100.0, 102.0, 104.0, 106.0, 108.0];
let result = ema(&prices, 3)?;

// Alpha = 2/(3+1) = 0.5
// result[2] = SMA(100,102,104) = 102.0
// result[3] = 0.5*106 + 0.5*102 = 104.0
// result[4] = 0.5*108 + 0.5*104 = 106.0
```

**Python 示例**:
```python
import pandas as pd
import haze_library as haze

df = pd.DataFrame({'close': [100, 102, 104, 106, 108]})

# Fibonacci EMA 序列 (常用于趋势识别)
for period in [8, 13, 21, 34, 55, 89]:
    df[f'ema_{period}'] = df.haze.ema(period)

# EMA 交叉策略
df['ema_fast'] = df.haze.ema(12)
df['ema_slow'] = df.haze.ema(26)
df['signal'] = (df['ema_fast'] > df['ema_slow']).astype(int)
```

**交易应用 (Trading Applications)**:

| 策略 | 信号条件 | 含义 | 应用场景 |
|------|---------|------|---------|
| **EMA 交叉** | EMA(12) 上穿 EMA(26) | 短期转强 | MACD 基础 |
| | EMA(12) 下穿 EMA(26) | 短期转弱 | 趋势反转 |
| **价格位置** | Price > EMA(20) | 强势区域 | 回调买入 |
| | Price < EMA(20) | 弱势区域 | 反弹卖出 |
| **三重 EMA** | EMA(5) > EMA(10) > EMA(20) | 多头加速 | 追涨 |

**vs SMA 对比**:
| 特性 | EMA | SMA |
|------|-----|-----|
| **响应速度** | 快 (α=0.1~0.5) | 慢 (均匀权重) |
| **延迟** | 低 | 高 |
| **平滑度** | 中等 | 高 |
| **噪音过滤** | 弱 | 强 |
| **适用场景** | 短线、快速趋势 | 长线、稳定趋势 |

**相关函数**: [`sma`](#sma---simple-moving-average-简单移动平均), [`dema`](#dema---double-exponential-moving-average-双重指数移动平均), [`tema`](#tema---triple-exponential-moving-average-三重指数移动平均)

---

### `wma` - Weighted Moving Average / 加权移动平均

**函数签名**:
```rust
pub fn wma(values: &[f64], period: usize) -> HazeResult<Vec<f64>>
```

**模块**: `utils::ma`

**描述**: 计算加权移动平均,使用线性递增权重,最新数据权重最大。使用 O(n) 增量算法优化性能。

**算法**:
```text
权重序列: [1, 2, 3, ..., period]
权重和: weight_sum = period × (period + 1) / 2

WMA[i] = Σ(values[i-period+1+j] × (j+1)) / weight_sum
         for j in 0..period

增量更新原理:
  当窗口从 [v0, v1, ..., v_{n-1}] 滑动到 [v1, v2, ..., v_n]:
  - 所有现有值的权重都减 1 (等于减去 simple_sum)
  - 旧值 v0 (权重 1) 被移除
  - 新值 v_n (权重 period) 被添加

  new_weighted_sum = old_weighted_sum - simple_sum + period × new_value
```

**参数**:
- `values`: `&[f64]` - 输入价格序列
- `period`: `usize` - WMA 周期

**返回值**:
- `Ok(Vec<f64>)`: 与输入等长的向量,前 `period-1` 个值为 `NaN`
- `Err(HazeError)`: 同 SMA

**性能**:
- 时间复杂度: O(n) (使用增量更新优化,定期重新计算)
- 空间复杂度: O(n)

**Rust 示例**:
```rust
use haze_library::utils::ma::wma;

let prices = vec![1.0, 2.0, 3.0, 4.0, 5.0];
let result = wma(&prices, 3)?;

// 窗口 [1,2,3]: (1×1 + 2×2 + 3×3) / (1+2+3) = 14/6 = 2.333...
// 窗口 [2,3,4]: (2×1 + 3×2 + 4×3) / 6 = 20/6 = 3.333...
assert!((result[2] - 14.0/6.0).abs() < 1e-10);
```

**Python 示例**:
```python
import haze_library as haze

prices = [100.0, 101.0, 102.0, 103.0, 104.0, 105.0]
wma_values = haze.py_wma(prices, 3)

# WMA 给予最近数据更高权重,适合捕捉短期趋势变化
```

**交易应用 (Trading Applications)**:

| 特性 | 说明 |
|------|------|
| **权重分布** | 线性递增,最新数据权重是最早数据的 period 倍 |
| **响应速度** | 介于 SMA 和 EMA 之间 |
| **适用场景** | 短期趋势追踪,需要快速响应但保持一定平滑度 |

**移动平均类型对比**:

| 类型 | 权重分布 | 响应速度 | 平滑度 | 延迟 | 使用场景 |
|------|---------|---------|--------|------|---------|
| **SMA** | 均匀 | 慢 | 高 | 高 | 长期趋势 |
| **WMA** | 线性递增 | 中 | 中 | 中 | 中期趋势 |
| **EMA** | 指数衰减 | 快 | 中 | 低 | 短期趋势 |
| **HMA** | 组合优化 | 最快 | 中 | 最低 | 快速趋势 |

**相关函数**: [`sma`](#sma---simple-moving-average-简单移动平均), [`ema`](#ema---exponential-moving-average-指数移动平均), [`hma`](#hma---hull-moving-average-赫尔移动平均)

---

## 📖 常用函数标准文档

### `rma` - Wilder's Moving Average / 威尔德移动平均

**函数签名**:
```rust
pub fn rma(values: &[f64], period: usize) -> HazeResult<Vec<f64>>
```

**描述**: 威尔德平滑移动平均,等价于 `EMA(alpha=1/period)`。专用于 ATR、RSI 等威尔德指标。

**算法**:
```text
Alpha = 1 / period
RMA[0] = SMA(period)
RMA[i] = (RMA[i-1] × (period - 1) + value[i]) / period
```

**Python 示例**:
```python
import haze_library as haze

close = [100.0, 102.0, 104.0, 106.0, 108.0, 110.0]
rma_14 = haze.py_rma(close, 14)  # 用于 RSI 计算

# RMA 比 EMA 更平滑 (alpha 更小)
# EMA(14) 的 alpha = 2/15 ≈ 0.133
# RMA(14) 的 alpha = 1/14 ≈ 0.071
```

**应用**: ATR (`atr = rma(true_range, period)`), RSI (`avg_gain = rma(gains, period)`)

**相关函数**: [`ema`](#ema---exponential-moving-average-指数移动平均), [`indicators::volatility::atr`](../indicators/volatility.md#atr---average-true-range-真实波动幅度均值), [`indicators::momentum::rsi`](../indicators/momentum.md#rsi---relative-strength-index-相对强弱指数)

---

### `dema` - Double Exponential Moving Average / 双重指数移动平均

**函数签名**:
```rust
pub fn dema(values: &[f64], period: usize) -> HazeResult<Vec<f64>>
```

**描述**: 双重指数移动平均,通过双重平滑减少 EMA 的延迟。

**算法**:
```text
EMA1 = EMA(values, period)
EMA2 = EMA(EMA1, period)
DEMA = 2 × EMA1 - EMA2
```

**特点**:
- 延迟比 EMA 低约 30-40%
- 保持平滑度的同时提高响应速度
- 适合波动性适中的市场

**Python 示例**:
```python
import pandas as pd
import haze_library as haze

df = pd.DataFrame({'close': prices})
df['dema_20'] = df.haze.dema(20)
df['ema_20'] = df.haze.ema(20)

# DEMA 对趋势变化的响应速度更快
```

**相关函数**: [`ema`](#ema---exponential-moving-average-指数移动平均), [`tema`](#tema---triple-exponential-moving-average-三重指数移动平均)

---

### `tema` - Triple Exponential Moving Average / 三重指数移动平均

**函数签名**:
```rust
pub fn tema(values: &[f64], period: usize) -> HazeResult<Vec<f64>>
```

**描述**: 三重指数移动平均,进一步减少延迟。

**算法**:
```text
EMA1 = EMA(values, period)
EMA2 = EMA(EMA1, period)
EMA3 = EMA(EMA2, period)
TEMA = 3 × EMA1 - 3 × EMA2 + EMA3
```

**特点**:
- 延迟比 EMA 低约 50-60%
- 对价格变化最敏感
- 在快速变化的市场中表现最佳

**Python 示例**:
```python
df['tema_20'] = df.haze.tema(20)

# TEMA 适合捕捉快速趋势反转
df['trend_change'] = (df['tema_20'].diff() > 0).astype(int)
```

**相关函数**: [`ema`](#ema---exponential-moving-average-指数移动平均), [`dema`](#dema---double-exponential-moving-average-双重指数移动平均)

---

### `hma` - Hull Moving Average / 赫尔移动平均

**函数签名**:
```rust
pub fn hma(values: &[f64], period: usize) -> HazeResult<Vec<f64>>
```

**描述**: 赫尔移动平均,使用组合 WMA 实现低延迟和高平滑度的平衡。

**算法**:
```text
half_period = period / 2
sqrt_period = sqrt(period)

HMA = WMA(2 × WMA(half_period) - WMA(period), sqrt_period)
```

**特点**:
- 延迟最低的平滑 MA 类型
- 保持平滑的同时快速响应趋势变化
- 适合趋势追踪和突破确认

**Python 示例**:
```python
df['hma_9'] = df.haze.hma(9)  # 快速趋势
df['hma_16'] = df.haze.hma(16)  # 中期趋势

# HMA 交叉策略
df['signal'] = (df['hma_9'] > df['hma_16']).astype(int)
```

**相关函数**: [`wma`](#wma---weighted-moving-average-加权移动平均)

---

### `vwap` - Volume Weighted Average Price / 成交量加权平均价

**函数签名**:
```rust
pub fn vwap(typical_prices: &[f64], volumes: &[f64], period: usize) -> HazeResult<Vec<f64>>
```

**描述**: 成交量加权平均价,机构交易者常用的基准价格指标。

**算法**:
```text
典型价格:
typical_price = (high + low + close) / 3

累积 VWAP (period=0):
VWAP = Σ(typical_price × volume) / Σ(volume)

滚动 VWAP (period>0):
VWAP[i] = Σ(typical_price[i-period+1:i+1] × volume) / Σ(volume[i-period+1:i+1])
```

**参数**:
- `typical_prices`: `&[f64]` - 典型价格序列 (H+L+C)/3
- `volumes`: `&[f64]` - 成交量序列
- `period`: `usize` - 周期 (0 表示累积 VWAP)

**性能**: 使用 Kahan 补偿求和,定期重新计算,精度 < 1e-12

**Python 示例**:
```python
import pandas as pd
import haze_library as haze

df = pd.DataFrame({
    'high': [102, 103, 104],
    'low': [98, 99, 100],
    'close': [100, 101, 102],
    'volume': [1000, 1100, 1200]
})

# 计算典型价格
df['typical'] = (df['high'] + df['low'] + df['close']) / 3

# 累积 VWAP (从开盘到当前)
df['vwap_cumulative'] = haze.py_vwap(
    df['typical'].tolist(),
    df['volume'].tolist(),
    0  # period=0 表示累积
)

# 滚动 VWAP (20 周期)
df['vwap_20'] = haze.py_vwap(
    df['typical'].tolist(),
    df['volume'].tolist(),
    20
)
```

**交易应用 (Trading Applications)**:

| 策略 | 信号条件 | 含义 | 应用场景 |
|------|---------|------|---------|
| **价格位置** | Price > VWAP | 买方占优 | 日内多单 |
| | Price < VWAP | 卖方占优 | 日内空单 |
| **回归交易** | Price 偏离 VWAP > 2% | 极端偏离 | 均值回归 |
| **机构成本** | VWAP 作为基准 | 交易成本评估 | 大单执行 |

**相关函数**: [`sma`](#sma---simple-moving-average-简单移动平均), [`indicators::volume::vwma`](../indicators/volume.md#vwma---volume-weighted-moving-average)

---

## 📝 高级函数简化文档

### `zlma` - Zero-Lag Moving Average / 零延迟移动平均

**函数签名**: `pub fn zlma(values: &[f64], period: usize) -> HazeResult<Vec<f64>>`

**算法**:
```text
lag = (period - 1) / 2
ema_data = 2 × values - values[lag_ago]
ZLMA = EMA(ema_data, period)
```

**特点**: 通过提前补偿尝试消除 EMA 延迟,更快响应价格变化

**Python 示例**: `zlma_20 = haze.py_zlma(close, 20)`

---

### `t3` - Tillson T3 Moving Average

**函数签名**: `pub fn t3(values: &[f64], period: usize, v_factor: f64) -> HazeResult<Vec<f64>>`

**算法**: 6 重 EMA 平滑,减少噪音同时保持快速响应

**参数**:
- `period`: 周期
- `v_factor`: 平滑因子 (通常 0.7)

**Python 示例**: `t3_5 = haze.py_t3(close, 5, 0.7)`

---

### `kama` - Kaufman Adaptive Moving Average / 考夫曼自适应移动平均

**函数签名**: `pub fn kama(values: &[f64], period: usize, fast_period: usize, slow_period: usize) -> HazeResult<Vec<f64>>`

**算法**: 根据市场波动性自适应调整平滑度

**参数**:
- `period`: 效率比率周期 (默认 10)
- `fast_period`: 快速 EMA 周期 (默认 2)
- `slow_period`: 慢速 EMA 周期 (默认 30)

**Python 示例**: `kama_10 = haze.py_kama(close, 10, 2, 30)`

---

### `frama` - Fractal Adaptive Moving Average / 分形自适应移动平均

**函数签名**: `pub fn frama(values: &[f64], period: usize) -> HazeResult<Vec<f64>>`

**算法**: 基于分形维度自适应调整

**约束**: period 必须是偶数且 >= 2

**Python 示例**: `frama_16 = haze.py_frama(close, 16)`

---

## 🎯 通用使用模式 (Common Usage Patterns)

### 模式 1: 多周期移动平均组合

```python
import pandas as pd
import haze_library as haze

df = pd.DataFrame({'close': prices})

# 趋势识别层级
df['sma_5'] = df.haze.sma(5)    # 超短期
df['sma_20'] = df.haze.sma(20)   # 短期
df['sma_50'] = df.haze.sma(50)   # 中期
df['sma_200'] = df.haze.sma(200) # 长期

# 判断趋势方向
def trend_direction(row):
    if row['sma_5'] > row['sma_20'] > row['sma_50'] > row['sma_200']:
        return '强势多头'
    elif row['sma_5'] < row['sma_20'] < row['sma_50'] < row['sma_200']:
        return '强势空头'
    elif row['sma_20'] > row['sma_50']:
        return '中期多头'
    elif row['sma_20'] < row['sma_50']:
        return '中期空头'
    else:
        return '震荡'

df['trend'] = df.apply(trend_direction, axis=1)
```

### 模式 2: MA 交叉信号系统

```python
# Golden Cross / Death Cross 检测
df['ma_fast'] = df.haze.sma(50)
df['ma_slow'] = df.haze.sma(200)

df['cross_up'] = (
    (df['ma_fast'] > df['ma_slow']) &
    (df['ma_fast'].shift(1) <= df['ma_slow'].shift(1))
)
df['cross_down'] = (
    (df['ma_fast'] < df['ma_slow']) &
    (df['ma_fast'].shift(1) >= df['ma_slow'].shift(1))
)

# 生成交易信号
df['signal'] = 0
df.loc[df['cross_up'], 'signal'] = 1   # 买入
df.loc[df['cross_down'], 'signal'] = -1  # 卖出
```

### 模式 3: MA 包络线 (Envelope)

```python
# SMA 包络线 (±2%)
df['sma_20'] = df.haze.sma(20)
df['upper_band'] = df['sma_20'] * 1.02
df['lower_band'] = df['sma_20'] * 0.98

# 超买超卖信号
df['overbought'] = df['close'] > df['upper_band']
df['oversold'] = df['close'] < df['lower_band']
```

### 模式 4: 多类型 MA 对比

```python
# 同周期不同类型 MA
period = 20
df['sma'] = df.haze.sma(period)
df['ema'] = df.haze.ema(period)
df['wma'] = df.haze.wma(period)
df['hma'] = df.haze.hma(period)
df['dema'] = df.haze.dema(period)

# 响应速度对比 (价格变化后的延迟)
# HMA < DEMA < EMA < WMA < SMA
```

---

## 🔧 性能与数值精度

### Kahan 补偿求和

所有滚动窗口移动平均 (SMA, WMA, VWAP) 均使用 Kahan 补偿算法:

```rust
// Kahan 补偿求和核心逻辑
y = value - compensation;
t = sum + y;
compensation = (t - sum) - y;
sum = t;
```

**效果**:
- 相对误差 < 1e-12 (vs naive 累加的 1e-6 ~ 1e-8)
- 适用于大规模数据集 (100k+ 数据点)

### 定期重新计算

为防止长时间累积误差,每 1000 次迭代重新计算窗口和:

```rust
const RECALC_INTERVAL: usize = 1000;

if steps_since_recalc >= RECALC_INTERVAL {
    sum = kahan_sum(&values[i + 1 - period..=i]);
    compensation = 0.0;
    steps_since_recalc = 0;
}
```

### 性能基准

| 函数 | 时间复杂度 | 空间复杂度 | 100k 数据点耗时 (估算) |
|------|----------|----------|---------------------|
| **SMA** | O(n) 平均 | O(n) | ~5ms |
| **EMA** | O(n) | O(n) | ~3ms |
| **WMA** | O(n) 平均 | O(n) | ~8ms |
| **DEMA** | O(n) | O(n) | ~6ms |
| **HMA** | O(n) | O(n) | ~15ms |
| **VWAP** | O(n) 平均 | O(n) | ~6ms |

---

## 📚 相关资源

**指标模块引用**:
- [Momentum Indicators](../indicators/momentum.md) - RSI 使用 RMA
- [Volatility Indicators](../indicators/volatility.md) - ATR 使用 RMA, Bollinger Bands 使用 SMA
- [Trend Indicators](../indicators/trend.md) - SuperTrend 使用 ATR (RMA)
- [Overlap Indicators](../indicators/overlap.md) - 价格计算与 MA 组合

**工具模块**:
- [Statistics Module](statistics.md) - 滚动窗口统计函数
- [Math Module](math.md) - Kahan 求和与浮点精度
- [Streaming Module](streaming.md) - 在线 MA 计算器

**核心模块**:
- [Types & Errors](../core/types_and_errors.md) - `HazeResult`, `HazeError` 定义
- [PyO3 Bindings](../core/pyo3_bindings.md) - Python 函数包装器

---

**文档版本**: v1.0
**最后更新**: 2025-01-XX
**维护者**: Haze-Library Team
