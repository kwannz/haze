# Trend Indicators (趋势指标)

**模块路径**: `haze_library::indicators::trend`

## 概述

趋势指标模块提供识别价格趋势方向和强度的技术分析工具。这些指标帮助交易者判断是否顺势交易、识别趋势反转,并测量趋势动量。

**核心特性**:
- 13 个专业趋势分析指标
- O(n) 时间复杂度,高效状态追踪
- 完整的错误处理与参数验证
- 符合 TA-Lib 与 TradingView 计算标准

**统一错误处理**:
所有函数返回 `HazeResult<T>`,可能的错误类型:
- `HazeError::EmptyInput` - 输入数组为空
- `HazeError::LengthMismatch` - 输入数组长度不一致
- `HazeError::InvalidPeriod` - 周期参数无效
- `HazeError::InsufficientData` - 数据长度不足
- `HazeError::InvalidValue` - 参数值非法

**趋势信号解读**:
- ADX > 25: 强趋势; ADX < 20: 弱趋势或震荡
- SuperTrend direction: 1.0 = 上升趋势, -1.0 = 下降趋势
- PSAR trend: 1.0 = 看涨, -1.0 = 看跌
- Choppiness > 61.8: 震荡; < 38.2: 趋势

---

## 目录

### 核心趋势指标 (完整文档)
1. [SuperTrend (超级趋势)](#1-supertrend)
2. [ADX - Average Directional Index (平均趋向指标)](#2-adx---average-directional-index)
3. [PSAR - Parabolic SAR (抛物线转向)](#3-psar---parabolic-sar)

### 常用趋势指标 (标准文档)
4. [Aroon Indicator (阿隆指标)](#4-aroon-indicator)
5. [DX - Directional Movement Index (方向性移动指数)](#5-dx---directional-movement-index)
6. [+DI / -DI (正负方向指标)](#6-di--di)
7. [Vortex Indicator (涡旋指标)](#7-vortex-indicator)

### 专业趋势指标 (简化文档)
8. [Choppiness Index (震荡指数)](#8-choppiness-index)
9. [QStick (买卖压力指标)](#9-qstick)
10. [VHF - Vertical Horizontal Filter (垂直水平过滤器)](#10-vhf---vertical-horizontal-filter)
11. [TRIX - Triple Exponential Average (三重指数平滑)](#11-trix---triple-exponential-average)
12. [DPO - Detrended Price Oscillator (去趋势价格振荡器)](#12-dpo---detrended-price-oscillator)

---

# 核心趋势指标

## 1. SuperTrend

**函数签名**: `supertrend(high: &[f64], low: &[f64], close: &[f64], period: usize, multiplier: f64) -> HazeResult<(Vec<f64>, Vec<f64>, Vec<f64>, Vec<f64>)>`

**模块**: `indicators::trend`

### 描述

SuperTrend (超级趋势) 是基于 ATR 的动态支撑/阻力指标,提供清晰的趋势方向信号和动态止损位。广泛用于趋势跟踪策略和风险管理。

### 算法

```text
1. 计算基础带:
   HL2 = (High + Low) / 2
   Basic Upper Band = HL2 + (multiplier × ATR)
   Basic Lower Band = HL2 - (multiplier × ATR)

2. 状态机追踪 (带收敛规则):
   - Upper Band: 只能向下收敛 (取 min(current, previous))
   - Lower Band: 只能向上收敛 (取 max(current, previous))

3. 趋势判定:
   - 当 Close > Upper Band → 转为下降趋势 (-1)
   - 当 Close < Lower Band → 转为上升趋势 (1)

4. SuperTrend 线:
   - 上升趋势 (direction = 1): SuperTrend = Lower Band
   - 下降趋势 (direction = -1): SuperTrend = Upper Band
```

### 参数

| 参数 | 类型 | 说明 | 典型值 |
|------|------|------|--------|
| `high` | `&[f64]` | 最高价序列 | - |
| `low` | `&[f64]` | 最低价序列 | - |
| `close` | `&[f64]` | 收盘价序列 | - |
| `period` | `usize` | ATR 周期 | 7 或 10 |
| `multiplier` | `f64` | ATR 倍数 | 3.0 |

### 返回值

- `Ok((supertrend, direction, upper, lower))`: 四个向量的元组
  - `supertrend`: SuperTrend 线 (支撑/阻力位)
  - `direction`: 趋势方向 (1.0 = 上升, -1.0 = 下降)
  - `upper`: 上轨
  - `lower`: 下轨
  - 所有向量长度与输入相同
  - 前 `period` 个值为 NaN (warmup 期)
- `Err(HazeError)`: 参数错误或数据不足

### 性能

- **时间复杂度**: O(n)
- **算法**: ATR 计算 + 状态机追踪

### Rust 示例

```rust
use haze_library::indicators::trend::supertrend;

let high = vec![102.0, 105.0, 104.0, 106.0, 108.0, 107.0, 109.0, 111.0];
let low = vec![99.0, 101.0, 100.0, 102.0, 104.0, 103.0, 105.0, 107.0];
let close = vec![101.0, 103.0, 102.0, 105.0, 107.0, 106.0, 108.0, 110.0];

// 计算 SuperTrend (7 周期 ATR, 3.0 倍数)
let (st_line, direction, upper, lower) = supertrend(
    &high, &low, &close,
    7,    // ATR 周期
    3.0   // ATR 倍数
).unwrap();

// 趋势判断
for i in 7..st_line.len() {
    if direction[i] == 1.0 {
        println!("[{}] 上升趋势 - 支撑位: {:.2}", i, st_line[i]);
    } else {
        println!("[{}] 下降趋势 - 阻力位: {:.2}", i, st_line[i]);
    }
}
```

### Python 示例

```python
import haze_library as haze
import pandas as pd
import numpy as np

# 方法 1: 直接函数调用
high = [102.0, 105.0, 104.0, 106.0, 108.0, 107.0, 109.0, 111.0]
low = [99.0, 101.0, 100.0, 102.0, 104.0, 103.0, 105.0, 107.0]
close = [101.0, 103.0, 102.0, 105.0, 107.0, 106.0, 108.0, 110.0]

st_line, direction, upper, lower = haze.py_supertrend(
    high, low, close,
    period=7,
    multiplier=3.0
)

# 方法 2: DataFrame Accessor (推荐)
df = pd.DataFrame({'high': high, 'low': low, 'close': close})
df['st'], df['st_dir'], df['st_upper'], df['st_lower'] = df.haze.supertrend(7, 3.0)

# 方法 3: 趋势信号生成
df['long_signal'] = (df['st_dir'] == 1) & (df['st_dir'].shift(1) == -1)
df['short_signal'] = (df['st_dir'] == -1) & (df['st_dir'].shift(1) == 1)

# 方法 4: 动态止损
df['stop_loss'] = np.where(
    df['st_dir'] == 1,
    df['st_lower'],  # 多头: 使用下轨作为止损
    df['st_upper']   # 空头: 使用上轨作为止损
)
```

### 交易策略

#### 1. 趋势跟踪
```python
# 基础信号
if direction_current == 1 and direction_prev == -1:
    print("做多信号 - 趋势反转向上")
elif direction_current == -1 and direction_prev == 1:
    print("做空信号 - 趋势反转向下")

# 趋势持续
if direction_current == 1:
    print(f"持有多头 - 支撑位: {st_line}")
else:
    print(f"持有空头 - 阻力位: {st_line}")
```

#### 2. 动态止损系统
```python
# SuperTrend 作为跟踪止损
position = 1  # 1 = 多头, -1 = 空头

if position > 0:
    stop_loss = st_lower  # 多头使用下轨
    if close < stop_loss:
        print("多头止损触发")
else:
    stop_loss = st_upper  # 空头使用上轨
    if close > stop_loss:
        print("空头止损触发")
```

#### 3. 多周期确认
```python
# 结合两个周期
st_fast = haze.py_supertrend(high, low, close, 5, 2.0)
st_slow = haze.py_supertrend(high, low, close, 10, 3.0)

if st_fast[1] == 1 and st_slow[1] == 1:
    print("强势上升趋势 - 快慢周期均确认")
elif st_fast[1] == -1 and st_slow[1] == -1:
    print("强势下降趋势 - 快慢周期均确认")
else:
    print("趋势不明确 - 观望")
```

### 交易信号表

| 信号类型 | 条件 | 解读 | 操作建议 |
|----------|------|------|----------|
| **多头反转** | direction: -1 → 1 | 下降趋势转为上升趋势 | 开多 / 平空 |
| **空头反转** | direction: 1 → -1 | 上升趋势转为下降趋势 | 开空 / 平多 |
| **趋势持续** | direction 保持不变 | 趋势延续 | 持仓,使用 ST 线止损 |
| **价格回测** | close 接近 st_line | 支撑/阻力测试 | 加仓机会 |

| 参数组合 | 灵敏度 | 适用场景 | 假信号风险 |
|----------|--------|----------|------------|
| (7, 3.0) | 标准 | 日线趋势跟踪 | 中等 |
| (10, 3.0) | 较低 | 强趋势过滤 | 低 |
| (5, 2.0) | 高 | 短期波段 | 高 |
| (14, 4.0) | 极低 | 长期趋势 | 极低 |

### 实现注意事项

- 使用 TA-Lib 兼容的 ATR 计算 (首个有效值在 index=period)
- 带收敛规则防止异常波动: Upper 只降不升, Lower 只升不降
- 初始趋势判定: close > HL2 → 上升趋势,否则下降趋势
- SuperTrend 线在上升趋势时为下轨,下降趋势时为上轨

### 相关函数

- [`atr`](../volatility/README.md#atr) - 底层 ATR 计算
- [`chandelier_exit`](../volatility/README.md#chandelier-exit) - 类似的 ATR 止损系统
- [`psar`](#3-psar---parabolic-sar) - 另一种趋势跟踪指标

### 参考文献

- Olivier Seban (2008). *SuperTrend Indicator*
- 标准参数: period=7/10, multiplier=3.0
- 在 TradingView 和 Zerodha 中广泛使用

---

## 2. ADX - Average Directional Index

**函数签名**: `adx(high: &[f64], low: &[f64], close: &[f64], period: usize) -> HazeResult<(Vec<f64>, Vec<f64>, Vec<f64>)>`

**模块**: `indicators::trend`

### 描述

平均趋向指标 (ADX) 由 J. Welles Wilder Jr. 开发,衡量趋势强度 (0-100),不指示方向。配合 +DI 和 -DI 判断趋势方向和强度。

### 算法

```text
1. 计算方向移动 (Directional Movement):
   +DM = max(High - Prev_High, 0)  当 +DM > -DM
   -DM = max(Prev_Low - Low, 0)    当 -DM > +DM
   (如果一方占优,另一方归零)

2. 计算方向指标 (Directional Indicators):
   +DI = 100 × RMA(+DM, period) / ATR
   -DI = 100 × RMA(-DM, period) / ATR

3. 计算方向性指数 (Directional Index):
   DX = 100 × |(+DI - -DI)| / (+DI + -DI)

4. 计算 ADX:
   ADX = RMA(DX, period)

RMA = Wilder's smoothing (与 EMA 类似,但 α = 1/period)
```

### 参数

| 参数 | 类型 | 说明 | 典型值 |
|------|------|------|--------|
| `high` | `&[f64]` | 最高价序列 | - |
| `low` | `&[f64]` | 最低价序列 | - |
| `close` | `&[f64]` | 收盘价序列 | - |
| `period` | `usize` | 平滑周期 | 14 |

### 返回值

- `Ok((adx, plus_di, minus_di))`: 三个向量的元组
  - `adx`: ADX 值 (0-100,趋势强度)
  - `plus_di`: +DI (上升趋势强度)
  - `minus_di`: -DI (下降趋势强度)
- `Err(HazeError)`: 参数错误

### 性能

- **时间复杂度**: O(n)
- **算法**: RMA 平滑,单次遍历

### Rust/Python 示例

```rust
use haze_library::indicators::trend::adx;

let high = vec![110.0, 111.0, 112.0, 113.0, 114.0, 115.0, 116.0, 117.0];
let low = vec![100.0, 101.0, 102.0, 103.0, 104.0, 105.0, 106.0, 107.0];
let close = vec![105.0, 106.0, 107.0, 108.0, 109.0, 110.0, 111.0, 112.0];

let (adx_values, plus_di, minus_di) = adx(&high, &low, &close, 14).unwrap();

// 趋势强度判断
for i in 14..adx_values.len() {
    if adx_values[i] > 25.0 {
        println!("[{}] 强趋势: ADX={:.2}", i, adx_values[i]);
        if plus_di[i] > minus_di[i] {
            println!("  方向: 上升 (+DI={:.2} > -DI={:.2})", plus_di[i], minus_di[i]);
        } else {
            println!("  方向: 下降 (-DI={:.2} > +DI={:.2})", minus_di[i], plus_di[i]);
        }
    } else {
        println!("[{}] 弱趋势/震荡: ADX={:.2}", i, adx_values[i]);
    }
}
```

```python
import haze_library as haze
import pandas as pd

df = pd.DataFrame({'high': high, 'low': low, 'close': close})
df['adx'], df['plus_di'], df['minus_di'] = df.haze.adx(14)

# 趋势分类
df['trend_strength'] = pd.cut(
    df['adx'],
    bins=[0, 20, 25, 50, 100],
    labels=['无趋势', '弱趋势', '中等趋势', '强趋势']
)

# 趋势方向
df['trend_direction'] = df.apply(
    lambda x: '上升' if x['plus_di'] > x['minus_di'] else '下降',
    axis=1
)

# ADX 交叉信号
df['di_crossover'] = (
    (df['plus_di'] > df['minus_di']) &
    (df['plus_di'].shift(1) <= df['minus_di'].shift(1))
)
```

### 交易策略

#### ADX 趋势强度判定

| ADX 值 | 趋势强度 | 交易策略 |
|--------|----------|----------|
| 0-20 | 无趋势/震荡 | 区间交易,避免趋势策略 |
| 20-25 | 弱趋势 | 谨慎顺势,等待确认 |
| 25-50 | 强趋势 | 趋势跟踪,持仓 |
| 50-100 | 极强趋势 | 重仓趋势交易 |

#### 综合信号

```python
# 强势上升信号
if adx > 25 and plus_di > minus_di and plus_di > 20:
    print("强势上升趋势 - 做多")

# 强势下降信号
elif adx > 25 and minus_di > plus_di and minus_di > 20:
    print("强势下降趋势 - 做空")

# DI 交叉
elif plus_di > minus_di and adx > 20:
    print("+DI 上穿 -DI - 趋势转为上升")
elif minus_di > plus_di and adx > 20:
    print("-DI 上穿 +DI - 趋势转为下降")

# 震荡市场
elif adx < 20:
    print("震荡市场 - 区间交易或观望")
```

### 实现注意事项

- ADX 是滞后指标,不预测未来只确认当前
- ADX 上升不代表价格上升,只代表趋势加强
- DI 交叉早于 ADX 反应,可提前入场
- 结合其他指标确认方向 (如 SuperTrend, MA)

### 相关函数

- [`dx`](#5-dx---directional-movement-index) - ADX 的基础指标 (未平滑)
- [`plus_di`](#6-di--di) - +DI 单独计算
- [`minus_di`](#6-di--di) - -DI 单独计算

### 参考文献

- Wilder, J. W. (1978). *New Concepts in Technical Trading Systems*
- 标准周期: 14

---

## 3. PSAR - Parabolic SAR

**函数签名**: `psar(high: &[f64], low: &[f64], close: &[f64], af_init: f64, af_increment: f64, af_max: f64) -> HazeResult<(Vec<f64>, Vec<f64>)>`

**模块**: `indicators::trend`

### 描述

抛物线转向 (Parabolic SAR) 由 J. Welles Wilder Jr. 开发,提供动态跟踪止损位和趋势反转信号。SAR 点在价格上方表示下降趋势,下方表示上升趋势。

### 算法

```text
1. 初始化:
   - 趋势方向: close[1] > close[0] → 上升, 否则下降
   - SAR[0]: 上升时 = low[0], 下降时 = high[0]
   - EP (极值点): 上升时 = high[1], 下降时 = low[1]
   - AF (加速因子) = af_init (通常 0.02)

2. 每个周期更新:
   SAR[i] = SAR[i-1] + AF × (EP - SAR[i-1])

3. SAR 约束 (防止穿越价格):
   上升趋势: SAR = min(SAR, low[i-1], low[i-2])
   下降趋势: SAR = max(SAR, high[i-1], high[i-2])

4. 趋势反转检测:
   上升趋势: 若 low[i] < SAR → 反转为下降
   下降趋势: 若 high[i] > SAR → 反转为上升

5. 反转时:
   - SAR = 上一个极值点 EP
   - EP = 当前 high (上升) 或 low (下降)
   - AF = af_init (重置)

6. 无反转时更新 EP 和 AF:
   - 若创新高/低: EP = 新极值, AF = min(AF + af_increment, af_max)
```

### 参数

| 参数 | 类型 | 说明 | 典型值 |
|------|------|------|--------|
| `high` | `&[f64]` | 最高价序列 | - |
| `low` | `&[f64]` | 最低价序列 | - |
| `close` | `&[f64]` | 收盘价序列 | - |
| `af_init` | `f64` | 初始加速因子 | 0.02 |
| `af_increment` | `f64` | AF 增量 | 0.02 |
| `af_max` | `f64` | 最大 AF | 0.2 |

### 返回值

- `Ok((psar, trend))`: 两个向量的元组
  - `psar`: SAR 值 (止损位)
  - `trend`: 趋势方向 (1.0 = 上升, -1.0 = 下降)
- `Err(HazeError)`: 参数错误

### 性能

- **时间复杂度**: O(n)
- **算法**: 迭代更新极值点和加速因子

### Rust/Python 示例

```rust
use haze_library::indicators::trend::psar;

let high = vec![102.0, 105.0, 104.0, 106.0, 108.0];
let low = vec![99.0, 101.0, 100.0, 102.0, 104.0];
let close = vec![101.0, 103.0, 102.0, 105.0, 107.0];

let (psar_values, trend) = psar(
    &high, &low, &close,
    0.02,  // 初始 AF
    0.02,  // AF 增量
    0.2    // 最大 AF
).unwrap();

// 趋势信号
for i in 1..psar_values.len() {
    if trend[i] == 1.0 && trend[i-1] == -1.0 {
        println!("[{}] 多头信号 - SAR: {:.2}", i, psar_values[i]);
    } else if trend[i] == -1.0 && trend[i-1] == 1.0 {
        println!("[{}] 空头信号 - SAR: {:.2}", i, psar_values[i]);
    }
}
```

```python
import haze_library as haze
import pandas as pd

df = pd.DataFrame({'high': high, 'low': low, 'close': close})
df['psar'], df['psar_trend'] = df.haze.psar(0.02, 0.02, 0.2)

# 反转信号
df['long_entry'] = (df['psar_trend'] == 1) & (df['psar_trend'].shift(1) == -1)
df['short_entry'] = (df['psar_trend'] == -1) & (df['psar_trend'].shift(1) == 1)

# 动态止损
df['stop_loss'] = df['psar']  # SAR 即为止损位

# 可视化
import matplotlib.pyplot as plt
plt.figure(figsize=(12, 6))
plt.plot(df['close'], label='Close', linewidth=2)
plt.scatter(df.index[df['psar_trend'] == 1], df['psar'][df['psar_trend'] == 1],
            color='green', marker='^', label='Bullish SAR')
plt.scatter(df.index[df['psar_trend'] == -1], df['psar'][df['psar_trend'] == -1],
            color='red', marker='v', label='Bearish SAR')
plt.legend()
plt.show()
```

### 交易策略

```python
# PSAR 趋势跟踪
if psar_trend == 1:
    print(f"多头趋势 - 止损位: {psar:.2f}")
    if close < psar:
        print("止损触发 - 平多")
elif psar_trend == -1:
    print(f"空头趋势 - 止损位: {psar:.2f}")
    if close > psar:
        print("止损触发 - 平空")

# 趋势反转
if psar_trend == 1 and psar_trend_prev == -1:
    print("反转信号 - 开多 / 平空")
elif psar_trend == -1 and psar_trend_prev == 1:
    print("反转信号 - 开空 / 平多")
```

### 参数调优

| 参数组合 | 灵敏度 | 适用场景 | 特点 |
|----------|--------|----------|------|
| (0.02, 0.02, 0.2) | 标准 | 通用趋势跟踪 | Wilder 原始参数 |
| (0.01, 0.01, 0.1) | 低 | 长期趋势 | 止损宽松,假信号少 |
| (0.03, 0.03, 0.3) | 高 | 短期波段 | 止损紧密,假信号多 |

### 实现注意事项

- SAR 不穿越前两根 K 线的 high/low (防止异常跳变)
- 反转时 SAR 跳跃到对侧极值点
- AF 在创新高/低时递增,反转时重置
- PSAR 在震荡市场频繁反转,适合趋势市场

### 相关函数

- [`supertrend`](#1-supertrend) - 另一种 ATR-based 趋势系统
- [`chandelier_exit`](../volatility/README.md#chandelier-exit) - ATR 跟踪止损

### 参考文献

- Wilder, J. W. (1978). *New Concepts in Technical Trading Systems*
- 标准参数: af_init=0.02, af_increment=0.02, af_max=0.2

---

# 常用趋势指标

## 4. Aroon Indicator

**函数签名**: `aroon(high: &[f64], low: &[f64], period: usize) -> HazeResult<(Vec<f64>, Vec<f64>, Vec<f64>)>`

**模块**: `indicators::trend`

### 描述

阿隆指标 (Aroon) 基于时间衡量趋势,通过计算距离最高/最低点的时间间隔来识别趋势强度和方向。

### 算法

```text
Aroon Up = ((period - bars_since_highest_high) / period) × 100
Aroon Down = ((period - bars_since_lowest_low) / period) × 100
Aroon Oscillator = Aroon Up - Aroon Down
```

### 参数

- `high`: 最高价序列
- `low`: 最低价序列
- `period`: 周期 (通常 25)

### 返回值

- `Ok((aroon_up, aroon_down, aroon_oscillator))`: 三个向量 (0-100 范围)

### Rust/Python 示例

```rust
use haze_library::indicators::trend::aroon;

let high = vec![110.0, 111.0, 112.0, 113.0, 114.0, 113.0, 112.0, 111.0];
let low = vec![100.0, 101.0, 102.0, 103.0, 104.0, 103.0, 102.0, 101.0];

let (aroon_up, aroon_down, aroon_osc) = aroon(&high, &low, 5).unwrap();
```

```python
df['aroon_up'], df['aroon_down'], df['aroon_osc'] = df.haze.aroon(25)

# 信号
df['strong_uptrend'] = (df['aroon_up'] > 70) & (df['aroon_down'] < 30)
df['strong_downtrend'] = (df['aroon_down'] > 70) & (df['aroon_up'] < 30)
```

### 交易信号

| 条件 | 解读 |
|------|------|
| Aroon Up > 70, Down < 30 | 强上升趋势 |
| Aroon Down > 70, Up < 30 | 强下降趋势 |
| Aroon Up/Down 都 < 50 | 震荡/整理 |
| Aroon Up 上穿 Down | 趋势转为上升 |

---

## 5. DX - Directional Movement Index

**函数签名**: `dx(high: &[f64], low: &[f64], close: &[f64], period: usize) -> HazeResult<Vec<f64>>`

**描述**: ADX 的基础指标,衡量趋势强度但无平滑

**算法**: `DX = 100 × |(+DI - -DI)| / (+DI + -DI)`

**返回值**: `Ok(Vec<f64>)` - DX 值 (0-100)

---

## 6. +DI / -DI

**函数签名**:
- `plus_di(high: &[f64], low: &[f64], close: &[f64], period: usize) -> HazeResult<Vec<f64>>`
- `minus_di(high: &[f64], low: &[f64], close: &[f64], period: usize) -> HazeResult<Vec<f64>>`

**描述**:
- `+DI`: 正向指标,衡量上升趋势强度
- `-DI`: 负向指标,衡量下降趋势强度

**算法**:
```text
+DI = 100 × RMA(+DM, period) / ATR
-DI = 100 × RMA(-DM, period) / ATR
```

**应用**:
- +DI > -DI: 上升趋势占优
- -DI > +DI: 下降趋势占优
- DI 交叉: 趋势反转信号

---

## 7. Vortex Indicator

**函数签名**: `vortex(high: &[f64], low: &[f64], close: &[f64], period: usize) -> HazeResult<(Vec<f64>, Vec<f64>)>`

**描述**: 涡旋指标,识别趋势的开始和持续性

**算法**:
```text
VM+ = |High[i] - Low[i-1]|
VM- = |Low[i] - High[i-1]|
TR = Max(High - Low, |High - Prev_Close|, |Low - Prev_Close|)

VI+ = Sum(VM+, period) / Sum(TR, period)
VI- = Sum(VM-, period) / Sum(TR, period)
```

**信号**:
- VI+ > VI-: 上升趋势
- VI- > VI+: 下降趋势
- VI+/VI- 交叉: 趋势反转

**Python 示例**:
```python
df['vi_plus'], df['vi_minus'] = df.haze.vortex(14)
df['vortex_signal'] = df['vi_plus'] > df['vi_minus']
```

---

# 专业趋势指标

## 8. Choppiness Index

**函数签名**: `choppiness_index(high: &[f64], low: &[f64], close: &[f64], period: usize) -> HazeResult<Vec<f64>>`

**算法**: `CHOP = 100 × log10(Sum(TR, period) / (Max(High) - Min(Low))) / log10(period)`

**典型参数**: period=14

**解读**:
- CHOP > 61.8: 震荡/横盘市场
- CHOP < 38.2: 趋势市场
- 不指示方向,仅判断市场状态

---

## 9. QStick

**函数签名**: `qstick(open: &[f64], close: &[f64], period: usize) -> HazeResult<Vec<f64>>`

**算法**: `QStick = EMA(Close - Open, period)`

**典型参数**: period=14

**信号**:
- QStick > 0: 买盘压力 (收盘价 > 开盘价)
- QStick < 0: 卖盘压力 (收盘价 < 开盘价)

---

## 10. VHF - Vertical Horizontal Filter

**函数签名**: `vhf(close: &[f64], period: usize) -> HazeResult<Vec<f64>>`

**算法**: `VHF = |Max(Close) - Min(Close)| / Sum(|Close[i] - Close[i-1]|, period)`

**典型参数**: period=28

**解读**:
- VHF 高值: 趋势市场 (价格单向移动)
- VHF 低值: 震荡市场 (价格来回波动)

---

## 11. TRIX - Triple Exponential Average

**函数签名**: `trix(close: &[f64], period: usize) -> HazeResult<Vec<f64>>`

**算法**:
```text
EMA1 = EMA(Close, period)
EMA2 = EMA(EMA1, period)
EMA3 = EMA(EMA2, period)
TRIX = (EMA3[i] - EMA3[i-1]) / EMA3[i-1] × 100
```

**典型参数**: period=14

**应用**: 过滤噪音,识别长期趋势变化率

---

## 12. DPO - Detrended Price Oscillator

**函数签名**: `dpo(close: &[f64], period: usize) -> HazeResult<Vec<f64>>`

**算法**:
```text
shift = period / 2 + 1
DPO = Close[i] - SMA(Close, period)[i - shift]
```

**典型参数**: period=20

**应用**: 去除趋势,识别周期性循环

---

## 通用使用模式

### 多指标趋势确认

```python
import haze_library as haze
import pandas as pd

df = pd.DataFrame({'high': high, 'low': low, 'close': close})

# 批量计算趋势指标
df['st'], df['st_dir'], _, _ = df.haze.supertrend(7, 3.0)
df['adx'], df['plus_di'], df['minus_di'] = df.haze.adx(14)
df['psar'], df['psar_trend'] = df.haze.psar(0.02, 0.02, 0.2)
df['aroon_up'], df['aroon_down'], df['aroon_osc'] = df.haze.aroon(25)
df['chop'] = haze.py_choppiness_index(df['high'].tolist(), df['low'].tolist(),
                                       df['close'].tolist(), 14)

# 趋势强度评分
def trend_score(row):
    score = 0
    # SuperTrend 确认
    if row['st_dir'] == 1:
        score += 2
    # ADX 强趋势
    if row['adx'] > 25:
        score += 2
    # DI 确认
    if row['plus_di'] > row['minus_di']:
        score += 1
    # PSAR 确认
    if row['psar_trend'] == 1:
        score += 1
    # Aroon 确认
    if row['aroon_up'] > 70 and row['aroon_down'] < 30:
        score += 1
    # Choppiness 过滤
    if row['chop'] < 38.2:
        score += 1
    return score

df['trend_score'] = df.apply(trend_score, axis=1)

# 综合信号
df['strong_uptrend'] = df['trend_score'] >= 6  # 8 分制, 6 分以上为强趋势
```

### 趋势 vs 震荡市场识别

```python
# 方法 1: ADX + Choppiness
df['is_trending'] = (df['adx'] > 25) & (df['chop'] < 50)
df['is_ranging'] = (df['adx'] < 20) | (df['chop'] > 61.8)

# 方法 2: VHF + DI 差值
df['vhf'] = haze.py_vhf(df['close'].tolist(), 28)
df['di_diff'] = abs(df['plus_di'] - df['minus_di'])
df['is_trending'] = (df['vhf'] > 0.4) | (df['di_diff'] > 20)

# 策略切换
df['strategy'] = df['is_trending'].apply(
    lambda x: '趋势跟踪' if x else '区间交易'
)
```

### 动态止损组合

```python
# 结合 SuperTrend 和 PSAR
df['st_stop'] = df.apply(
    lambda x: x['st_lower'] if x['st_dir'] == 1 else x['st_upper'],
    axis=1
)

# 使用更保守的止损
df['combined_stop'] = df.apply(
    lambda x: min(x['st_stop'], x['psar']) if x['st_dir'] == 1
              else max(x['st_stop'], x['psar']),
    axis=1
)
```

---

## 性能对比

| 指标 | 时间复杂度 | 主要算法 | 适用场景 |
|------|------------|----------|----------|
| SuperTrend | O(n) | ATR + 状态机 | 通用趋势跟踪 |
| ADX | O(n) | RMA 平滑 | 趋势强度确认 |
| PSAR | O(n) | 迭代加速因子 | 动态止损 |
| Aroon | O(n) | 时间距离计算 | 新趋势识别 |
| Vortex | O(n) | 滚动求和 | 趋势开始检测 |
| Choppiness | O(n) | 对数计算 | 趋势/震荡判别 |
| VHF | O(n) | 价格变化累积 | 市场状态分类 |

---

## 设计原则

本模块严格遵循 Haze-Library 核心设计哲学:

- **KISS 原则**: 每个函数职责单一,算法清晰
- **YAGNI 原则**: 仅实现必要功能,避免过度工程化
- **SOLID 原则**: 模块化设计,便于扩展
- **数值稳定性**: 使用 RMA 平滑、状态机追踪保证精度
- **性能优先**: O(n) 复杂度,单次遍历,低内存分配

---

## 相关文档

- [Momentum Indicators (动量指标)](./momentum.md)
- [Volatility Indicators (波动率指标)](./volatility.md)
- [Architecture Overview (架构总览)](../../ARCHITECTURE.md)
- [Error Handling Strategy (错误处理策略)](../../ERROR_HANDLING_STRATEGY.md)
