# Types & Error Handling / 数据类型与错误处理

核心类型系统和错误处理机制是 Haze-Library 的基石，定义了数据结构、类型别名和统一的错误处理策略。遵循 **Fail-Fast** 原则，确保所有错误在入口处被捕获。

---

## 📋 模块概览 / Module Overview

**文件位置**:
- `rust/src/types.rs` - 数据类型定义
- `rust/src/errors.rs` - 错误类型与验证

**核心职责**:
1. **数据抽象**: Candle（K线）、IndicatorResult（指标结果）
2. **类型安全**: 复杂返回值的类型别名（SuperTrendResult, TradingSignals 等）
3. **错误语义**: HazeError 枚举，7 种明确错误类型
4. **输入验证**: validate_period, validate_not_empty 等验证函数
5. **Python 互操作**: PyO3 绑定（#[pyclass], #[pymethods]）

---

## 🎯 核心数据类型 / Core Data Types

### `Candle` - OHLCV Candlestick / K线数据

**结构定义**:
```rust
#[cfg(feature = "python")]
#[pyclass]
#[derive(Debug, Clone, Copy, Serialize, Deserialize)]
pub struct Candle {
    #[pyo3(get, set)]
    pub timestamp: i64,  // Unix 毫秒时间戳
    #[pyo3(get, set)]
    pub open: f64,
    #[pyo3(get, set)]
    pub high: f64,
    #[pyo3(get, set)]
    pub low: f64,
    #[pyo3(get, set)]
    pub close: f64,
    #[pyo3(get, set)]
    pub volume: f64,
}
```

**字段说明**:
- `timestamp: i64` - Unix 时间戳（毫秒）
  - 示例：`1704067200000` → 2024-01-01 00:00:00 UTC
- `open: f64` - 开盘价
- `high: f64` - 最高价
- `low: f64` - 最低价
- `close: f64` - 收盘价
- `volume: f64` - 成交量

**不变量约束** (OHLC Logic):
```text
high >= max(open, close)
low <= min(open, close)
```

**Rust 示例**:
```rust
use haze_library::types::Candle;

let candle = Candle::new(
    1704067200000,  // timestamp
    100.0,          // open
    102.0,          // high
    99.0,           // low
    101.0,          // close
    10000.0,        // volume
);

// 访问字段
println!("Close: {}", candle.close);

// 计算派生价格
let typical = candle.typical_price();  // (H + L + C) / 3
let median = candle.median_price();    // (H + L) / 2
let weighted = candle.weighted_close(); // (H + L + 2C) / 4
```

**Python 示例**:
```python
from haze_library import Candle

# 创建 Candle
candle = Candle(
    timestamp=1704067200000,
    open=100.0,
    high=102.0,
    low=99.0,
    close=101.0,
    volume=10000.0
)

# 访问字段（PyO3 自动 getter/setter）
print(f"Close: {candle.close}")

# 计算派生价格
print(f"Typical Price: {candle.typical_price}")
print(f"Median Price: {candle.median_price}")
print(f"Weighted Close: {candle.weighted_close}")

# 转换为字典
candle_dict = candle.to_dict()
# {'timestamp': 1704067200000.0, 'open': 100.0, ...}

# 字符串表示
print(candle)
# Candle(O:100.00, H:102.00, L:99.00, C:101.00, V:10000.00)
```

**派生价格方法**:

| 方法 | 公式 | 用途 |
|------|------|------|
| `typical_price()` | (H + L + C) / 3 | Typical Price, MFI 基础 |
| `median_price()` | (H + L) / 2 | Median Price, 对称指标 |
| `weighted_close()` | (H + L + 2C) / 4 | Weighted Close, 强调收盘价 |

**辅助函数**:

#### `candles_to_vectors` - 拆分为 OHLCV 向量

```rust
pub fn candles_to_vectors(
    candles: &[Candle],
) -> (Vec<f64>, Vec<f64>, Vec<f64>, Vec<f64>, Vec<f64>)
```

**用途**: 将 `Vec<Candle>` 转换为 5 个独立向量（O, H, L, C, V）

**示例**:
```rust
use haze_library::types::{Candle, candles_to_vectors};

let candles = vec![
    Candle::new(0, 100.0, 102.0, 99.0, 101.0, 1000.0),
    Candle::new(1, 101.0, 103.0, 100.0, 102.0, 1100.0),
];

let (open, high, low, close, volume) = candles_to_vectors(&candles);

// open = [100.0, 101.0]
// high = [102.0, 103.0]
// close = [101.0, 102.0]

// 传递给指标函数
let rsi = haze::indicators::momentum::rsi(&close, 14)?;
```

---

#### `validate_ohlc` - 验证 OHLC 逻辑

```rust
pub fn validate_ohlc(candles: &[Candle]) -> Result<(), String>
```

**验证规则**:
1. `high >= max(open, close)` - 最高价不能低于开盘/收盘价
2. `low <= min(open, close)` - 最低价不能高于开盘/收盘价

**示例**:
```rust
use haze_library::types::{Candle, validate_ohlc};

// ✅ 有效数据
let valid_candles = vec![
    Candle::new(0, 100.0, 102.0, 99.0, 101.0, 1000.0),
];
assert!(validate_ohlc(&valid_candles).is_ok());

// ❌ 无效数据（high < close）
let invalid_candles = vec![
    Candle::new(0, 100.0, 99.0, 98.0, 101.0, 1000.0),
];
match validate_ohlc(&invalid_candles) {
    Err(msg) => println!("验证失败: {}", msg),
    // "Candle 0 违反 OHLC 逻辑: high < max(open, close)"
    Ok(_) => {}
}
```

**应用场景**:
- 数据清洗：过滤交易所错误数据
- 回测验证：确保历史数据质量
- 实时监控：检测异常 tick 数据

---

### `IndicatorResult` - 单序列指标结果

**结构定义**:
```rust
#[cfg(feature = "python")]
#[pyclass]
#[derive(Debug, Clone)]
pub struct IndicatorResult {
    #[pyo3(get)]
    pub name: String,
    #[pyo3(get)]
    pub values: Vec<f64>,
    #[pyo3(get)]
    pub metadata: HashMap<String, String>,
}
```

**字段说明**:
- `name: String` - 指标名称（如 "RSI", "SMA"）
- `values: Vec<f64>` - 指标值序列
- `metadata: HashMap<String, String>` - 元数据（参数、版本等）

**Rust 示例**:
```rust
use haze_library::types::IndicatorResult;

let mut result = IndicatorResult::new("SMA".to_string(), sma_values);

// 添加元数据
result.add_metadata("period".to_string(), "20".to_string());
result.add_metadata("version".to_string(), "0.4.0".to_string());

println!("Indicator: {}, Length: {}", result.name, result.len());
```

**Python 示例**:
```python
from haze_library import IndicatorResult

result = IndicatorResult("SMA", sma_values)
result.add_metadata("period", "20")

print(f"Length: {result.len()}")
print(f"Metadata: {result.metadata}")
```

---

### `MultiIndicatorResult` - 多序列指标结果

**结构定义**:
```rust
#[cfg(feature = "python")]
#[pyclass]
#[derive(Debug, Clone)]
pub struct MultiIndicatorResult {
    #[pyo3(get)]
    pub name: String,
    #[pyo3(get)]
    pub series: HashMap<String, Vec<f64>>,
    #[pyo3(get)]
    pub metadata: HashMap<String, String>,
}
```

**用途**: 返回多条线的指标（如 MACD = macd + signal + histogram）

**Rust 示例**:
```rust
use haze_library::types::MultiIndicatorResult;

let mut macd_result = MultiIndicatorResult::new("MACD".to_string());

macd_result.add_series("macd".to_string(), macd_line);
macd_result.add_series("signal".to_string(), signal_line);
macd_result.add_series("histogram".to_string(), histogram);

macd_result.add_metadata("fast".to_string(), "12".to_string());
macd_result.add_metadata("slow".to_string(), "26".to_string());
```

**Python 示例**:
```python
result = MultiIndicatorResult("MACD")
result.add_series("macd", macd_line)
result.add_series("signal", signal_line)
result.add_series("histogram", histogram)

# 访问各条线
macd = result.series["macd"]
signal = result.series["signal"]
```

---

## 🔗 类型别名 / Type Aliases

为复杂返回值提供语义化别名，提升代码可读性。

### SuperTrend 相关

```rust
/// SuperTrend 指标结果
pub type SuperTrendResult<T> = HazeResult<(T, T, T, T)>;
// 返回：(supertrend_line, direction, upper_band, lower_band)

/// SuperTrend 切片（零拷贝）
pub type SuperTrendSlices<'a> = HazeResult<(&'a [f64], &'a [f64], &'a [f64], &'a [f64])>;

/// SuperTrend Python FFI（拥有所有权）
#[cfg(feature = "python")]
pub type SuperTrendVecs = PyResult<(Vec<f64>, Vec<f64>, Vec<f64>, Vec<f64>)>;
```

**使用示例**:
```rust
use haze_library::types::SuperTrendResult;

fn supertrend(/* ... */) -> SuperTrendResult<Vec<f64>> {
    // ...
    Ok((line, direction, upper, lower))
}
```

---

### 交易信号相关

```rust
/// 交易信号 + 止损/止盈
pub type TradingSignals = HazeResult<(Vec<f64>, Vec<f64>, Vec<f64>, Vec<f64>)>;
// 返回：(buy_signals, sell_signals, stop_loss, take_profit)

/// 区域信号 + 边界
pub type ZoneSignals = HazeResult<(Vec<f64>, Vec<f64>, Vec<f64>, Vec<f64>)>;
// 返回：(bullish_zone, bearish_zone, upper_bound, lower_bound)

/// 谐波形态信号 + PRZ + 概率
pub type HarmonicSignals = HazeResult<(Vec<f64>, Vec<f64>, Vec<f64>, Vec<f64>)>;
// 返回：(signals, prz_upper, prz_lower, probability)
```

**应用示例**:
```rust
use haze_library::types::TradingSignals;

fn generate_signals(/* ... */) -> TradingSignals {
    let buy_signals = vec![1.0, 0.0, 0.0, 1.0];
    let sell_signals = vec![0.0, 0.0, 1.0, 0.0];
    let stop_loss = vec![95.0, f64::NAN, 98.0, 94.0];
    let take_profit = vec![105.0, f64::NAN, 102.0, 106.0];

    Ok((buy_signals, sell_signals, stop_loss, take_profit))
}
```

---

## ⚠️ 错误处理系统 / Error Handling System

### `HazeError` - 错误枚举

**定义**:
```rust
use thiserror::Error;

#[derive(Error, Debug, Clone, PartialEq)]
pub enum HazeError {
    #[error("输入数据为空: {field}")]
    EmptyInput { field: String },

    #[error("参数无效: {message}")]
    InvalidParameter { message: String },

    #[error("周期参数无效: period={period}, data_len={data_len}")]
    InvalidPeriod { period: usize, data_len: usize },

    #[error("数据长度不匹配: {message}")]
    LengthMismatch { message: String },

    #[error("数值范围错误: {param}={value}, 期望范围 [{min}, {max}]")]
    OutOfRange {
        param: String,
        value: f64,
        min: f64,
        max: f64,
    },

    #[error("计算失败: {reason}")]
    ComputationError { reason: String },

    #[error("非有限值: {message}")]
    InvalidValue { message: String },
}
```

**错误类型详解**:

| 错误类型 | 触发条件 | 示例 | 恢复建议 |
|---------|---------|------|---------|
| **EmptyInput** | 输入为空数组 | `sma(&[], 10)` | 检查数据源 |
| **InvalidParameter** | 参数语义错误 | `ema(&data, alpha=-0.5)` | 修正参数值 |
| **InvalidPeriod** | period = 0 或 > 数据长度 | `sma(&[1,2,3], 0)` | 调整 period |
| **LengthMismatch** | 多序列长度不一致 | `correlation(&[1,2], &[1,2,3], 2)` | 对齐数据 |
| **OutOfRange** | 参数超出有效范围 | `roc(&data, -10)` | 使用有效范围 |
| **ComputationError** | 计算失败（如除零） | `stdev(&[5.0; 100], 100)` | 检查数据有效性 |
| **InvalidValue** | 输入包含 NaN/Inf | `sma(&[1.0, f64::NAN], 2)` | 过滤非有限值 |

**Python 错误映射**:
```python
# Rust HazeError → Python ValueError
try:
    result = haze.py_sma([], 10)
except ValueError as e:
    print(f"Error: {e}")
    # "输入数据为空: values"
```

---

### `HazeResult<T>` - 结果类型

**定义**:
```rust
pub type HazeResult<T> = Result<T, HazeError>;
```

**用途**: 统一的返回类型，强制错误处理

**示例**:
```rust
use haze_library::errors::HazeResult;

fn my_indicator(data: &[f64], period: usize) -> HazeResult<Vec<f64>> {
    // 验证输入
    if data.is_empty() {
        return Err(HazeError::EmptyInput {
            field: "data".to_string()
        });
    }

    // 计算逻辑
    let result = vec![/* ... */];
    Ok(result)
}

// 调用方必须处理错误
match my_indicator(&data, 20) {
    Ok(values) => process_values(values),
    Err(e) => eprintln!("指标计算失败: {}", e),
}
```

---

### 验证函数 / Validation Functions

**模块**: `errors::validation`

#### `validate_not_empty` - 验证非空

```rust
pub fn validate_not_empty(values: &[f64], field: &str) -> HazeResult<()>
```

**示例**:
```rust
use haze_library::errors::validation::validate_not_empty;

validate_not_empty(&close_prices, "close")?;
// 如果为空，返回 Err(HazeError::EmptyInput { field: "close" })
```

---

#### `validate_period` - 验证周期参数

```rust
pub fn validate_period(period: usize, data_len: usize) -> HazeResult<()>
```

**验证规则**:
- `period > 0`
- `period <= data_len`

**示例**:
```rust
use haze_library::errors::validation::validate_period;

validate_period(20, close_prices.len())?;
// 如果 period = 0 或 > data_len，返回 InvalidPeriod
```

---

#### `validate_range` - 验证范围

```rust
pub fn validate_range(
    param: &str,
    value: f64,
    min: f64,
    max: f64,
) -> HazeResult<()>
```

**示例**:
```rust
use haze_library::errors::validation::validate_range;

validate_range("alpha", 0.5, 0.0, 1.0)?;
// 如果 alpha < 0 或 > 1，返回 OutOfRange
```

---

#### `validate_lengths_match` - 验证长度一致

```rust
pub fn validate_lengths_match(arrays: &[(&[f64], &str)]) -> HazeResult<()>
```

**示例**:
```rust
use haze_library::errors::validation::validate_lengths_match;

validate_lengths_match(&[
    (&high, "high"),
    (&low, "low"),
    (&close, "close"),
])?;
// 如果长度不一致，返回 LengthMismatch
```

---

#### `validate_all_finite` - 验证所有值有限

```rust
pub fn validate_all_finite(values: &[f64], field: &str) -> HazeResult<()>
```

**验证**: 所有值不是 NaN 且不是 Infinity

**示例**:
```rust
use haze_library::errors::validation::validate_all_finite;

validate_all_finite(&prices, "prices")?;
// 如果包含 NaN/Inf，返回 InvalidValue
```

---

## 🛠️ 错误处理模式 / Error Handling Patterns

### 模式 1：入口验证（Fail-Fast）

**推荐**:
```rust
pub fn sma(values: &[f64], period: usize) -> HazeResult<Vec<f64>> {
    // ✅ 入口处集中验证
    validate_not_empty(values, "values")?;
    validate_period(period, values.len())?;

    // 后续计算不再返回错误
    let mut result = vec![f64::NAN; values.len()];
    for i in (period - 1)..values.len() {
        result[i] = calculate_sma(values, i, period);
    }

    Ok(result)
}
```

**反模式**:
```rust
// ❌ 计算中途返回错误（违反 Fail-Fast）
pub fn bad_sma(values: &[f64], period: usize) -> HazeResult<Vec<f64>> {
    let mut result = vec![];

    for i in 0..values.len() {
        if i < period - 1 {
            return Err(HazeError::InvalidPeriod { /* ... */ });
        }
        // ...
    }

    Ok(result)
}
```

---

### 模式 2：使用 `?` 传播错误

**推荐**:
```rust
pub fn macd(close: &[f64], /* ... */) -> HazeResult<(Vec<f64>, Vec<f64>, Vec<f64>)> {
    // ✅ 使用 ? 自动传播错误
    let fast_ema = ema(close, fast_period)?;
    let slow_ema = ema(close, slow_period)?;

    let macd_line = fast_ema.iter()
        .zip(&slow_ema)
        .map(|(f, s)| f - s)
        .collect();

    let signal_line = ema(&macd_line, signal_period)?;

    Ok((macd_line, signal_line, histogram))
}
```

**反模式**:
```rust
// ❌ unwrap 或 expect（会导致 panic）
pub fn bad_macd(close: &[f64], /* ... */) -> (Vec<f64>, Vec<f64>, Vec<f64>) {
    let fast_ema = ema(close, fast_period).unwrap();  // ❌ Panic!
    // ...
}
```

---

### 模式 3：提供上下文的错误信息

**推荐**:
```rust
// ✅ 包含诊断上下文
if alpha <= 0.0 || alpha > 1.0 {
    return Err(HazeError::OutOfRange {
        param: "alpha".to_string(),
        value: alpha,
        min: 0.0,
        max: 1.0,
    });
}
```

**反模式**:
```rust
// ❌ 缺乏上下文
if alpha <= 0.0 || alpha > 1.0 {
    return Err(HazeError::InvalidParameter {
        message: "invalid alpha".to_string()  // 太笼统
    });
}
```

---

### 模式 4：NaN 处理策略

**Warmup 期使用 NaN**:
```rust
// ✅ Warmup 期填充 NaN
let mut result = vec![f64::NAN; values.len()];

for i in (period - 1)..values.len() {
    result[i] = calculate(...);  // 仅填充有效值
}

Ok(result)
```

**输入错误使用 Error**:
```rust
// ✅ 输入包含 NaN → 返回错误
validate_all_finite(values, "values")?;

// ❌ 不推荐：用 NaN 掩盖错误
if values.iter().any(|v| v.is_nan()) {
    return Ok(vec![f64::NAN; values.len()]);  // ❌ 隐藏问题
}
```

---

## 🧪 测试示例 / Testing Examples

### 单元测试：验证错误处理

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_sma_empty_input() {
        let result = sma(&[], 10);
        assert!(matches!(
            result,
            Err(HazeError::EmptyInput { field }) if field == "values"
        ));
    }

    #[test]
    fn test_sma_invalid_period() {
        let values = vec![1.0, 2.0, 3.0];

        // period = 0
        assert!(matches!(
            sma(&values, 0),
            Err(HazeError::InvalidPeriod { period: 0, .. })
        ));

        // period > data_len
        assert!(matches!(
            sma(&values, 10),
            Err(HazeError::InvalidPeriod { period: 10, data_len: 3 })
        ));
    }

    #[test]
    fn test_sma_valid() {
        let values = vec![1.0, 2.0, 3.0, 4.0, 5.0];
        let result = sma(&values, 3).unwrap();

        // Warmup 期
        assert!(result[0].is_nan());
        assert!(result[1].is_nan());

        // 有效值
        assert_eq!(result[2], 2.0);  // (1+2+3)/3
        assert_eq!(result[3], 3.0);  // (2+3+4)/3
    }
}
```

---

## 📊 设计哲学 / Design Philosophy

### SOLID 原则体现

**Single Responsibility（单一职责）**:
- `types.rs` 仅负责数据结构定义
- `errors.rs` 仅负责错误类型与验证
- 每个验证函数仅验证一个条件

**Open/Closed（开闭原则）**:
- `HazeError` 枚举可扩展新错误类型（Open）
- 现有错误类型不修改（Closed）

**Dependency Inversion（依赖反转）**:
- 指标函数依赖 `HazeResult<T>` 抽象
- 不直接依赖具体错误类型

---

### KISS 原则体现

**简单的错误类型**:
- 仅 7 种错误类型（vs 复杂的错误层级）
- 每种错误有明确语义

**简单的验证策略**:
- 入口处集中验证（Fail-Fast）
- 后续计算不返回错误

---

### YAGNI 原则体现

**不实现的功能**:
- ❌ 错误恢复机制（复杂且不需要）
- ❌ 多语言错误消息（i18n）
- ❌ 错误堆栈追踪（backtrace）

**仅实现必要功能**:
- ✅ 明确的错误类型
- ✅ 输入验证
- ✅ Python 错误映射

---

## 🔗 相关模块 / Related Modules

### 使用本模块的函数

**所有指标函数** (`indicators/*`):
- 使用 `HazeResult<Vec<f64>>` 返回类型
- 使用 `validate_*` 函数进行输入验证

**工具函数** (`utils/*`):
- `ma.rs` - 使用 `HazeError::InvalidPeriod`
- `stats.rs` - 使用 `HazeError::LengthMismatch`
- `streaming.rs` - 使用 `HazeError::InvalidValue`

**Python 绑定** (`lib.rs`):
- 使用 `#[pyclass]` 暴露 `Candle`
- 使用 `From<HazeError> for PyErr` 转换错误

---

## 📝 最佳实践总结 / Best Practices Summary

### DO's ✅

1. **使用验证函数**
   ```rust
   validate_not_empty(values, "values")?;
   validate_period(period, values.len())?;
   ```

2. **Fail-Fast 验证**
   ```rust
   // 入口处全部验证完成
   validate_inputs()?;

   // 后续计算不返回错误
   let result = calculate(...);
   Ok(result)
   ```

3. **提供上下文信息**
   ```rust
   Err(HazeError::OutOfRange {
       param: "alpha".to_string(),
       value: alpha,
       min: 0.0,
       max: 1.0,
   })
   ```

### DON'Ts ❌

1. **不要用 NaN 掩盖错误**
   ```rust
   // ❌ 错误
   if period == 0 {
       return Ok(vec![f64::NAN; n]);
   }

   // ✅ 正确
   validate_period(period, n)?;
   ```

2. **不要在计算中途返回错误**
   ```rust
   // ❌ 错误
   for i in 0..n {
       if bad_condition(i) {
           return Err(...);  // 违反 Fail-Fast
       }
   }
   ```

3. **不要 unwrap 或 expect**
   ```rust
   // ❌ 错误
   let ema = ema(values, 12).unwrap();

   // ✅ 正确
   let ema = ema(values, 12)?;
   ```

---

**返回**: [API 文档首页](../README.md) | [核心模块总览](README.md)
