# Haze项目错误处理策略文档

## 文档版本
- **版本**: 1.0
- **创建日期**: 2025-12-26
- **作者**: Haze Architecture Team
- **状态**: DRAFT

---

## 执行摘要

本文档定义Haze技术分析库的统一错误处理策略，解决当前存在的三种错误处理模式共存问题：
1. NaN静默失败（主要在早期实现中）
2. HazeError枚举返回（标准模式，已在momentum.rs等新模块采用）
3. 未使用的validation模块（marked `#[allow(dead_code)]`）

**核心决策**：采用`HazeResult<T>`作为主要错误处理机制，保留NaN仅用于数学上合理的缺失值场景。

---

## 1. 问题现状分析

### 1.1 现有错误处理模式

#### 模式A：NaN静默失败
**位置**: 早期指标实现（部分）
```rust
// 示例：早期简单返回Vec<f64>的函数
pub fn legacy_indicator(values: &[f64], period: usize) -> Vec<f64> {
    let n = values.len();
    let mut result = vec![f64::NAN; n];

    if n < period {
        return result;  // ❌ 静默失败，调用者无法区分错误和正常warmup
    }

    // ... 计算逻辑
    result
}
```

**问题**：
- 调用者无法区分"输入错误"和"warmup期NaN"
- 边界条件错误被掩盖（如period=0, empty input）
- 违反Rust的错误处理最佳实践

#### 模式B：HazeError枚举返回（✅ 推荐）
**位置**: momentum.rs, volatility.rs, trend.rs等新模块
```rust
// 示例：标准HazeResult模式
pub fn rsi(close: &[f64], period: usize) -> HazeResult<Vec<f64>> {
    validate_not_empty(close, "close")?;
    let n = close.len();

    if period == 0 {
        return Err(HazeError::InvalidPeriod {
            period,
            data_len: n,
        });
    }
    if period >= n {
        return Err(HazeError::InsufficientData {
            required: period + 1,
            actual: n,
        });
    }

    let mut result = init_result!(n);  // vec![f64::NAN; n]

    // ... 计算逻辑，warmup期保持NaN
    Ok(result)
}
```

**优势**：
- 明确区分错误和正常NaN
- 错误信息清晰（包含上下文参数）
- 支持`?`操作符链式传播
- Python FFI友好（通过PyO3自动转换为ValueError）

#### 模式C：未使用的validation模块
**位置**: src/errors.rs (lines 71-157)
```rust
#[allow(dead_code)]
pub mod validation {
    // 已实现但被标记为dead_code的验证函数
    pub fn validate_period(...) -> HazeResult<()> { ... }
    pub fn validate_not_empty(...) -> HazeResult<()> { ... }
    // ...
}
```

**问题**：
- 已实现完善的验证工具，但被误标记为dead_code
- 实际上momentum.rs等模块正在使用（use crate::errors::validation::*）
- 需要移除`#[allow(dead_code)]`标记

### 1.2 统计数据

```
NaN使用频率统计（grep结果）:
- sfg_signals.rs: 2次
- ichimoku.rs: 12次
- volume.rs: 20次
- candlestick.rs: 3次
- sfg.rs: 29次
- overlap.rs: 4次
- harmonics.rs: 1次
- pandas_ta.rs: 28次
- momentum.rs: 25次
- volatility.rs: 26次
- cycle.rs: 5次
- trend.rs: 37次
- pivots.rs: 2次

总计: 204次NaN使用（跨15个文件）

验证函数使用:
- validate_not_empty: 已在momentum.rs等模块广泛使用
- validate_period: 已在stochastic, cci等函数使用
- validate_same_length: 已在多输入指标使用
```

---

## 2. 统一错误处理策略

### 2.1 核心原则

#### 原则1：错误 vs 缺失值的语义区分

| 场景 | 处理方式 | 理由 |
|------|---------|------|
| 输入参数无效（period=0） | `Err(HazeError::InvalidPeriod)` | 这是程序错误，应立即中断 |
| 数据不足（len<period） | `Err(HazeError::InsufficientData)` | 无法计算有效值，应立即中断 |
| 数组长度不匹配 | `Err(HazeError::LengthMismatch)` | 输入不一致，应立即中断 |
| Warmup期数据点 | 返回`Ok(vec![NaN, NaN, ..., valid]）` | 这是正常输出，前N个值为NaN |
| 计算中遇到除零 | 结果数组该位置为NaN | 数学上合理的缺失值 |
| 数值溢出/无效 | 结果数组该位置为NaN | 局部计算失败，不影响其他点 |

**决策树**：
```
输入验证问题（参数/数据）？
├─ 是 → Err(HazeError::*)
└─ 否 → 计算能否产生部分有效结果？
    ├─ 是 → Ok(Vec<f64>) with NaN for invalid points
    └─ 否 → Err(HazeError::InsufficientData)
```

#### 原则2：Fail-Fast原则
**在函数入口处完成所有输入验证**，避免在计算中途返回错误。

```rust
pub fn indicator(close: &[f64], period: usize) -> HazeResult<Vec<f64>> {
    // ✅ 第一步：全部输入验证（Fail-Fast）
    validate_not_empty(close, "close")?;
    validate_period(period, close.len())?;

    // ✅ 第二步：计算逻辑（不再返回错误）
    let mut result = init_result!(close.len());
    for i in (period - 1)..close.len() {
        result[i] = compute(close, i, period);  // 内部可产生NaN，但不返回Err
    }

    Ok(result)
}
```

#### 原则3：上下文丰富的错误信息
所有错误必须携带足够的诊断信息：

```rust
// ✅ 良好：包含期望值和实际值
Err(HazeError::InvalidPeriod { period: 0, data_len: 100 })

// ❌ 不良：仅返回错误类型
Err(HazeError::InvalidInput)
```

### 2.2 标准错误类型映射

| 错误场景 | HazeError类型 | 示例 |
|---------|--------------|------|
| 空输入数组 | `EmptyInput` | `close = []` |
| 周期参数无效 | `InvalidPeriod` | `period = 0` 或 `period > len` |
| 数据长度不足 | `InsufficientData` | `len < required_min_length` |
| 数组长度不匹配 | `LengthMismatch` | `high.len() != low.len()` |
| 参数超出范围 | `ParameterOutOfRange` | `multiplier < 0.0` |
| 包含无效值 | `InvalidValue` | `close[10] = Infinity` (如需检查) |

### 2.3 NaN的合理使用场景

**✅ 允许场景**：

1. **Warmup期**（最常见）
```rust
let mut result = init_result!(n);  // 初始化为全NaN
for i in (period - 1)..n {
    result[i] = calculate(...);    // 仅填充有效区间
}
Ok(result)  // 返回包含NaN的结果是正常的
```

2. **局部计算失败**（数学合理）
```rust
// 示例：除零保护
let rsi_value = if loss == 0.0 {
    if gain == 0.0 { 0.0 } else { 100.0 }
} else {
    let rs = gain / loss;
    100.0 - (100.0 / (1.0 + rs))
};

// 示例：范围保护
let range = highest - lowest;
let normalized = if range == 0.0 {
    50.0  // 或 f64::NAN，根据语义决定
} else {
    (close - lowest) / range * 100.0
};
```

3. **滚动窗口起始**
```rust
// rolling_max/rolling_min在前period-1个位置返回NaN是合理的
let rolling_max_values = rolling_max(high, period);  // 前period-1个为NaN
```

**❌ 禁止场景**：

1. **输入验证失败后返回NaN数组**
```rust
// ❌ 错误示例
pub fn bad_indicator(values: &[f64], period: usize) -> Vec<f64> {
    if period == 0 {
        return vec![f64::NAN; values.len()];  // 应该返回Err
    }
    // ...
}
```

2. **用NaN掩盖程序逻辑错误**
```rust
// ❌ 错误示例
let result = if index >= values.len() {
    f64::NAN  // 应该是panic!或Err，这是逻辑bug
} else {
    values[index]
};
```

---

## 3. Python FFI层错误处理

### 3.1 自动转换机制

PyO3已自动实现`HazeError → PyErr`转换：

```rust
// errors.rs (已实现)
#[cfg(feature = "python")]
impl From<HazeError> for PyErr {
    fn from(err: HazeError) -> PyErr {
        PyValueError::new_err(err.to_string())
    }
}
```

**Python侧接收**：
```python
import haze_library as haze

try:
    result = haze.py_rsi([], period=14)
except ValueError as e:
    print(e)  # "Empty input: close cannot be empty"
```

### 3.2 PyO3包装器标准模板

**✅ 推荐模式**：
```rust
#[pyfunction]
#[pyo3(name = "py_indicator")]
fn py_indicator(
    close: Vec<f64>,
    period: usize,
) -> PyResult<Vec<f64>> {
    // 直接调用Rust函数，?自动转换HazeError→PyErr
    Ok(indicators::your_module::indicator(&close, period)?)
}
```

**关键点**：
1. 使用`PyResult<T>`作为返回类型
2. 使用`?`传播HazeError（自动转换为PyErr）
3. 无需手写错误转换代码

### 3.3 Python文档字符串

```rust
/// py_rsi - Relative Strength Index
///
/// Args:
///     close (List[float]): Closing prices
///     period (int): RSI period (default: 14)
///
/// Returns:
///     List[float]: RSI values (0-100), NaN for warmup period
///
/// Raises:
///     ValueError: If close is empty
///     ValueError: If period is 0 or exceeds data length
///
/// Example:
///     >>> import haze_library as haze
///     >>> close = [44.0, 44.25, 44.5, ...]
///     >>> rsi = haze.py_rsi(close, period=14)
#[pyfunction]
#[pyo3(name = "py_rsi")]
fn py_rsi(close: Vec<f64>, period: usize) -> PyResult<Vec<f64>> {
    Ok(indicators::momentum::rsi(&close, period)?)
}
```

---

## 4. 迁移指南

### 4.1 迁移优先级

**第一阶段：高优先级模块（已迁移✅）**
- ✅ momentum.rs - 已完全采用HazeResult
- ✅ volatility.rs - 已完全采用HazeResult
- ✅ trend.rs - 已完全采用HazeResult

**第二阶段：中优先级模块（需迁移）**
- 🔄 overlap.rs - 基础MA函数，使用频繁
- 🔄 volume.rs - 20次NaN使用，需审查
- 🔄 candlestick.rs - 模式识别，错误处理简单

**第三阶段：低优先级模块（谨慎迁移）**
- ⚠️ sfg.rs / sfg_signals.rs - 复杂SFG算法，需彻底测试
- ⚠️ pandas_ta.rs - 兼容层，可能需要特殊处理
- ⚠️ harmonics.rs - 复杂图形识别，边界情况多

### 4.2 迁移步骤（模板）

#### Step 1: 识别需要迁移的函数
```bash
# 查找未使用HazeResult的公开函数
rg "^pub fn \w+.*-> Vec<f64>" haze/rust/src/indicators/
```

#### Step 2: 重构函数签名
```rust
// Before
pub fn indicator(values: &[f64], period: usize) -> Vec<f64> {
    // ...
}

// After
pub fn indicator(values: &[f64], period: usize) -> HazeResult<Vec<f64>> {
    // ...
}
```

#### Step 3: 添加输入验证
```rust
pub fn indicator(values: &[f64], period: usize) -> HazeResult<Vec<f64>> {
    // 添加验证
    validate_not_empty(values, "values")?;
    validate_period(period, values.len())?;

    // 原有逻辑
    let mut result = init_result!(values.len());
    // ...
    Ok(result)  // 包装返回值
}
```

#### Step 4: 更新调用链
```rust
// 如果函数被其他Rust函数调用
pub fn composite_indicator(values: &[f64]) -> HazeResult<Vec<f64>> {
    let sma_vals = sma(values, 10)?;  // 添加?传播错误
    let ema_vals = ema(values, 20)?;

    // ...
    Ok(result)
}
```

#### Step 5: 更新PyO3包装器
```rust
// 在lib.rs中
#[pyfunction]
#[pyo3(name = "py_indicator")]
fn py_indicator(values: Vec<f64>, period: usize) -> PyResult<Vec<f64>> {
    Ok(indicators::your_module::indicator(&values, period)?)
    // 从 Ok(indicator(&values, period)) 改为添加 ?
}
```

#### Step 6: 更新测试
```rust
#[test]
fn test_indicator_empty_input() {
    let result = indicator(&[], 10);
    assert!(matches!(result, Err(HazeError::EmptyInput { .. })));
}

#[test]
fn test_indicator_invalid_period() {
    let values = vec![1.0, 2.0, 3.0];
    let result = indicator(&values, 0);
    assert!(matches!(result, Err(HazeError::InvalidPeriod { .. })));
}

#[test]
fn test_indicator_valid() {
    let values = vec![1.0, 2.0, 3.0, 4.0, 5.0];
    let result = indicator(&values, 3).unwrap();

    // Warmup期为NaN
    assert!(result[0].is_nan());
    assert!(result[1].is_nan());

    // 有效值检查
    assert!(!result[2].is_nan());
}
```

### 4.3 向后兼容性考虑

**Rust API**：
- ✅ 破坏性变更可接受（v1.0之前）
- 通过返回类型变更，编译器强制调用者处理错误

**Python API**：
- ✅ 异常抛出是增强行为
- 旧代码：未处理错误时程序崩溃（更早发现问题）
- 新代码：可通过try-except优雅处理

```python
# 向后兼容：旧代码仍能运行（但会在错误输入时抛出异常）
rsi_values = haze.py_rsi(close, 14)  # 可能抛出ValueError

# 新代码：显式处理错误
try:
    rsi_values = haze.py_rsi(close, 14)
except ValueError as e:
    print(f"计算失败: {e}")
    rsi_values = [float('nan')] * len(close)
```

---

## 5. 新指标开发规范

### 5.1 强制要求

开发新指标时，必须遵循以下规范：

#### 5.1.1 函数签名
```rust
/// [Indicator Name] - Brief description
///
/// # Parameters
/// - `param1`: Description
/// - `param2`: Description
///
/// # Returns
/// - `Ok(Vec<f64>)`: Indicator values with NaN for warmup period
///
/// # Errors
/// - `HazeError::EmptyInput`: If input is empty
/// - `HazeError::InvalidPeriod`: If period is invalid
/// - `HazeError::InsufficientData`: If data length < required
///
/// # Example
/// ```rust
/// let result = indicator(&values, period)?;
/// assert!(result[0].is_nan());  // Warmup period
/// ```
pub fn indicator(
    values: &[f64],
    period: usize,
) -> HazeResult<Vec<f64>> {
    // Implementation
}
```

#### 5.1.2 输入验证顺序
```rust
pub fn indicator(...) -> HazeResult<Vec<f64>> {
    // 1. 空值检查（最基础）
    validate_not_empty(values, "values")?;

    // 2. 参数范围检查
    if period == 0 {
        return Err(HazeError::InvalidPeriod {
            period,
            data_len: values.len()
        });
    }

    // 3. 参数有效性检查
    if multiplier < 0.0 {
        return Err(HazeError::ParameterOutOfRange {
            name: "multiplier",
            value: multiplier,
            min: 0.0,
            max: f64::INFINITY,
        });
    }

    // 4. 数据充足性检查
    validate_min_length(values, period)?;

    // 5. 多输入长度一致性检查（如适用）
    validate_same_length(high, "high", low, "low")?;

    // 6. 开始计算
    let mut result = init_result!(values.len());
    // ...
    Ok(result)
}
```

#### 5.1.3 必需的测试用例
```rust
#[cfg(test)]
mod tests {
    use super::*;

    // ✅ 必需：空输入测试
    #[test]
    fn test_indicator_empty_input() {
        let result = indicator(&[], 10);
        assert!(matches!(result, Err(HazeError::EmptyInput { .. })));
    }

    // ✅ 必需：无效周期测试
    #[test]
    fn test_indicator_invalid_period() {
        let values = vec![1.0, 2.0, 3.0];
        assert!(matches!(
            indicator(&values, 0),
            Err(HazeError::InvalidPeriod { .. })
        ));
    }

    // ✅ 必需：数据不足测试
    #[test]
    fn test_indicator_insufficient_data() {
        let values = vec![1.0, 2.0];
        assert!(matches!(
            indicator(&values, 10),
            Err(HazeError::InsufficientData { .. })
        ));
    }

    // ✅ 必需：基本计算测试
    #[test]
    fn test_indicator_basic_calculation() {
        let values = vec![1.0, 2.0, 3.0, 4.0, 5.0];
        let result = indicator(&values, 3).unwrap();

        // 验证warmup期
        assert!(result[0].is_nan());
        assert!(result[1].is_nan());

        // 验证有效值
        assert!(!result[2].is_nan());
        assert_eq!(result[2], EXPECTED_VALUE);
    }

    // ✅ 推荐：边界值测试
    #[test]
    fn test_indicator_edge_cases() {
        // period = len
        let values = vec![1.0, 2.0, 3.0];
        let result = indicator(&values, 3);
        // 根据实现决定是Error还是Ok
    }
}
```

### 5.2 PyO3包装器规范

```rust
/// Python wrapper for [Indicator Name]
///
/// See Rust documentation for detailed algorithm description.
#[pyfunction]
#[pyo3(
    name = "py_indicator_name",
    signature = (values, period, optional_param=default_value)
)]
fn py_indicator_name(
    values: Vec<f64>,
    period: usize,
    optional_param: Option<f64>,
) -> PyResult<Vec<f64>> {
    let param = optional_param.unwrap_or(DEFAULT_VALUE);
    Ok(indicators::module::indicator_name(&values, period, param)?)
}

// 在pymodule中注册
#[pymodule]
fn haze_library(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(py_indicator_name, m)?)?;
    Ok(())
}
```

---

## 6. 验证模块使用指南

### 6.1 移除dead_code标记

**Action Required**:
```rust
// src/errors.rs

// ❌ 当前状态
#[allow(dead_code)]
pub mod validation {
    // ...
}

// ✅ 修改为
pub mod validation {
    // 这些函数实际上被广泛使用，不应标记为dead_code
}
```

### 6.2 标准验证函数

| 函数 | 用途 | 示例 |
|------|------|------|
| `validate_not_empty` | 检查数组非空 | `validate_not_empty(close, "close")?;` |
| `validate_period` | 检查周期有效性 | `validate_period(period, data.len())?;` |
| `validate_same_length` | 检查两数组等长 | `validate_same_length(high, "high", low, "low")?;` |
| `validate_lengths_match` | 检查多数组等长 | `validate_lengths_match(&[(h, "h"), (l, "l"), (c, "c")])?;` |
| `validate_min_length` | 检查最小长度 | `validate_min_length(data, required)?;` |
| `validate_range` | 检查参数范围 | `validate_range("alpha", 0.5, 0.0, 1.0)?;` |

### 6.3 验证函数使用示例

```rust
use crate::errors::validation::*;

pub fn complex_indicator(
    high: &[f64],
    low: &[f64],
    close: &[f64],
    period: usize,
    multiplier: f64,
) -> HazeResult<Vec<f64>> {
    // 组合使用多个验证函数
    validate_not_empty(high, "high")?;
    validate_lengths_match(&[
        (high, "high"),
        (low, "low"),
        (close, "close"),
    ])?;
    validate_period(period, high.len())?;
    validate_range("multiplier", multiplier, 0.0, 10.0)?;

    // 继续计算...
    Ok(result)
}
```

---

## 7. 错误处理最佳实践

### 7.1 DO's ✅

1. **使用HazeResult作为返回类型**
   ```rust
   pub fn indicator(...) -> HazeResult<Vec<f64>> { ... }
   ```

2. **在函数入口处完成所有验证**
   ```rust
   // ✅ 入口处集中验证
   validate_not_empty(values, "values")?;
   validate_period(period, values.len())?;

   // ✅ 之后的逻辑不再返回错误
   let mut result = init_result!(values.len());
   ```

3. **为错误提供丰富上下文**
   ```rust
   Err(HazeError::InvalidPeriod {
       period: user_period,
       data_len: values.len()
   })
   ```

4. **Warmup期使用NaN**
   ```rust
   let mut result = init_result!(n);  // 前period-1个为NaN
   for i in (period - 1)..n {
       result[i] = calculate(...);
   }
   Ok(result)
   ```

5. **使用init_result!宏统一初始化**
   ```rust
   let mut result = init_result!(n);  // 等价于 vec![f64::NAN; n]
   ```

### 7.2 DON'Ts ❌

1. **不要用NaN掩盖输入错误**
   ```rust
   // ❌ 错误
   if period == 0 {
       return vec![f64::NAN; n];
   }

   // ✅ 正确
   if period == 0 {
       return Err(HazeError::InvalidPeriod { period, data_len: n });
   }
   ```

2. **不要吞噬错误**
   ```rust
   // ❌ 错误
   let sub_result = sub_indicator(values, period).unwrap_or_else(|_| vec![]);

   // ✅ 正确
   let sub_result = sub_indicator(values, period)?;  // 传播错误
   ```

3. **不要在计算中途返回错误**
   ```rust
   // ❌ 错误：在循环中返回错误
   for i in 0..n {
       if values[i] < 0.0 {
           return Err(HazeError::InvalidValue { ... });
       }
   }

   // ✅ 正确：在入口处验证或局部使用NaN
   validate_all_positive(values)?;  // 或
   result[i] = if values[i] < 0.0 { f64::NAN } else { compute(...) };
   ```

4. **不要创建过于通用的错误**
   ```rust
   // ❌ 错误
   Err(HazeError::GenericError("something wrong".to_string()))

   // ✅ 正确
   Err(HazeError::InvalidPeriod { period, data_len })
   ```

### 7.3 性能考虑

1. **验证函数开销**
   - 输入验证的成本为O(1)（仅检查长度/参数）
   - 相比计算逻辑（通常O(n)或O(n·period)），验证开销可忽略

2. **NaN传播**
   - NaN的算术运算天然传播（NaN + x = NaN）
   - 无需显式检查每个中间值

3. **错误路径优化**
   - 使用`#[cold]`标记错误处理分支（未来优化）
   ```rust
   #[cold]
   fn handle_invalid_period(period: usize, len: usize) -> HazeError {
       HazeError::InvalidPeriod { period, data_len: len }
   }
   ```

---

## 8. 附录

### 8.1 完整的HazeError枚举

```rust
// src/errors.rs (已实现)

#[derive(Debug, Error)]
pub enum HazeError {
    #[error("Insufficient data: need at least {required} elements, got {actual}")]
    InsufficientData { required: usize, actual: usize },

    #[error("Invalid period: {period} (must be > 0 and <= data length {data_len})")]
    InvalidPeriod { period: usize, data_len: usize },

    #[error("Length mismatch: {name1}={len1}, {name2}={len2}")]
    LengthMismatch {
        name1: &'static str,
        len1: usize,
        name2: &'static str,
        len2: usize,
    },

    #[error("Invalid value at index {index}: {message}")]
    InvalidValue { index: usize, message: String },

    #[error("Empty input: {name} cannot be empty")]
    EmptyInput { name: &'static str },

    #[error("Parameter {name} out of range: {value} (valid range: {min}..{max})")]
    ParameterOutOfRange {
        name: &'static str,
        value: f64,
        min: f64,
        max: f64,
    },

    #[error("Model error: {0}")]
    ModelError(String),

    #[error("IO error: {0}")]
    IoError(#[from] std::io::Error),
}

pub type HazeResult<T> = Result<T, HazeError>;
```

### 8.2 迁移检查清单

针对每个待迁移函数，完成以下检查：

- [ ] 函数签名已更新为 `-> HazeResult<T>`
- [ ] 添加了输入验证（空值、周期、长度）
- [ ] 移除了静默失败的返回路径
- [ ] Warmup期正确使用NaN
- [ ] 更新了所有调用该函数的代码（添加`?`）
- [ ] 更新了PyO3包装器
- [ ] 添加了错误处理测试用例
- [ ] 更新了文档字符串（Errors章节）
- [ ] 通过了`cargo test`和`pytest`

### 8.3 常见错误处理模式速查

#### 单输入指标
```rust
pub fn indicator(values: &[f64], period: usize) -> HazeResult<Vec<f64>> {
    validate_not_empty(values, "values")?;
    validate_period(period, values.len())?;

    let mut result = init_result!(values.len());
    for i in (period - 1)..values.len() {
        result[i] = compute(values, i, period);
    }
    Ok(result)
}
```

#### 多输入指标（OHLC）
```rust
pub fn indicator(
    high: &[f64],
    low: &[f64],
    close: &[f64],
    period: usize,
) -> HazeResult<Vec<f64>> {
    validate_not_empty(high, "high")?;
    validate_lengths_match(&[
        (high, "high"),
        (low, "low"),
        (close, "close"),
    ])?;
    validate_period(period, high.len())?;

    let mut result = init_result!(high.len());
    // ...
    Ok(result)
}
```

#### 返回多个值
```rust
pub fn indicator(
    values: &[f64],
    period: usize,
) -> HazeResult<(Vec<f64>, Vec<f64>, Vec<f64>)> {
    validate_not_empty(values, "values")?;
    validate_period(period, values.len())?;

    let n = values.len();
    let mut line1 = init_result!(n);
    let mut line2 = init_result!(n);
    let mut line3 = init_result!(n);

    // ...
    Ok((line1, line2, line3))
}
```

#### 带可选参数
```rust
pub fn indicator(
    values: &[f64],
    period: usize,
    multiplier: Option<f64>,
) -> HazeResult<Vec<f64>> {
    let mult = multiplier.unwrap_or(2.0);  // 默认值

    validate_not_empty(values, "values")?;
    validate_period(period, values.len())?;
    validate_range("multiplier", mult, 0.0, 10.0)?;

    // ...
    Ok(result)
}
```

---

## 9. 决策记录

### 9.1 关键决策

| 决策ID | 决策内容 | 理由 |
|-------|---------|------|
| DEC-001 | 采用HazeResult<T>作为标准返回类型 | Rust最佳实践，类型安全，强制错误处理 |
| DEC-002 | 保留NaN用于Warmup期和局部计算失败 | 符合金融库惯例（TA-Lib, pandas-ta） |
| DEC-003 | 移除validation模块的dead_code标记 | 模块已被使用，标记不正确 |
| DEC-004 | 输入验证集中在函数入口 | Fail-Fast原则，提高调试效率 |
| DEC-005 | Python FFI自动转换为ValueError | 简化FFI层，符合Python异常惯例 |

### 9.2 未来考虑

1. **自定义错误类型**（v2.0考虑）
   - 可能为不同模块创建专门的错误类型
   - 例如：`VolatilityError`, `MomentumError`

2. **错误恢复策略**（v2.0考虑）
   - 提供`try_indicator`变体，返回部分结果
   - 例如：`try_rsi() -> (Vec<f64>, Vec<HazeError>)`

3. **日志记录**（未来版本）
   - 集成`tracing`库记录警告级别的问题
   - 例如：数据中包含异常值但未达到错误阈值

---

## 10. 参考资料

### 10.1 内部文档
- `haze/rust/src/errors.rs` - 错误类型定义
- `haze/rust/src/indicators/momentum.rs` - 良好实践示例
- `haze/CONTRIBUTING.md` - 贡献指南
- `haze/claude.md` - SOLID原则与设计哲学

### 10.2 外部参考
- [Rust Error Handling](https://doc.rust-lang.org/book/ch09-00-error-handling.html)
- [PyO3 Error Handling](https://pyo3.rs/latest/function/error_handling.html)
- [thiserror Documentation](https://docs.rs/thiserror/latest/thiserror/)

### 10.3 相关Issues
- GitHub Issue #XXX: "统一错误处理策略"
- GitHub Issue #YYY: "移除validation dead_code标记"

---

## 变更历史

| 版本 | 日期 | 作者 | 变更内容 |
|------|------|------|---------|
| 1.0 | 2025-12-26 | Haze Team | 初始版本，定义核心策略 |

---

**文档状态**: DRAFT
**下次审查日期**: 2025-12-31
**批准人**: [待定]
