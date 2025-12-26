# Haze错误处理策略 - 执行摘要

## 核心决策

采用**HazeResult<T>**作为标准错误处理机制，保留NaN仅用于数学上合理的缺失值场景。

## 决策树

```
输入验证问题（参数/数据）？
├─ 是 → Err(HazeError::*)
└─ 否 → 计算能否产生部分有效结果？
    ├─ 是 → Ok(Vec<f64>) with NaN for invalid points
    └─ 否 → Err(HazeError::InsufficientData)
```

## 关键原则

### 1. 错误 vs 缺失值的语义区分

| 场景 | 处理方式 | 示例 |
|------|---------|------|
| 输入参数无效 | `Err(HazeError::InvalidPeriod)` | `period = 0` |
| 数据不足 | `Err(HazeError::InsufficientData)` | `len < period` |
| 数组长度不匹配 | `Err(HazeError::LengthMismatch)` | `high.len() != low.len()` |
| Warmup期 | `Ok(vec![NaN, ..., valid])` | 前N个值为NaN |
| 局部计算失败 | 结果数组该位置为NaN | 除零、溢出 |

### 2. Fail-Fast原则

在函数入口处完成所有输入验证，避免在计算中途返回错误。

```rust
pub fn indicator(...) -> HazeResult<Vec<f64>> {
    // ✅ 第一步：全部输入验证
    validate_not_empty(values, "values")?;
    validate_period(period, values.len())?;

    // ✅ 第二步：计算逻辑（不再返回错误）
    let mut result = init_result!(values.len());
    // ...
    Ok(result)
}
```

### 3. 上下文丰富的错误信息

```rust
// ✅ 良好：包含诊断上下文
Err(HazeError::InvalidPeriod { period: 0, data_len: 100 })

// ❌ 不良：信息不足
Err(HazeError::GenericError)
```

## 迁移优先级

### 第一阶段：已完成✅
- momentum.rs
- volatility.rs  
- trend.rs

### 第二阶段：中优先级🔄
- overlap.rs - 基础MA函数
- volume.rs - 20次NaN使用
- candlestick.rs - 模式识别

### 第三阶段：低优先级⚠️
- sfg.rs / sfg_signals.rs - 复杂算法
- pandas_ta.rs - 兼容层
- harmonics.rs - 复杂图形识别

## 标准实现模板

### 单输入指标
```rust
use crate::errors::validation::*;

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

### PyO3包装器
```rust
#[pyfunction]
fn py_indicator(values: Vec<f64>, period: usize) -> PyResult<Vec<f64>> {
    Ok(indicators::module::indicator(&values, period)?)
}
```

## 必需测试用例

```rust
#[test]
fn test_empty_input() {
    assert!(matches!(indicator(&[], 10), Err(HazeError::EmptyInput { .. })));
}

#[test]
fn test_invalid_period() {
    assert!(matches!(indicator(&[1.0], 0), Err(HazeError::InvalidPeriod { .. })));
}

#[test]
fn test_valid() {
    let result = indicator(&[1.0, 2.0, 3.0, 4.0, 5.0], 3).unwrap();
    assert!(result[0].is_nan());  // Warmup
    assert!(!result[2].is_nan()); // Valid
}
```

## Python侧测试
```python
def test_empty_input():
    with pytest.raises(ValueError, match="Empty input"):
        haze.py_indicator([], period=3)

def test_invalid_period():
    with pytest.raises(ValueError, match="Invalid period"):
        haze.py_indicator([1.0], period=0)
```

## Action Items

1. **立即执行**：
   - 移除 `errors.rs` 中 `validation` 模块的 `#[allow(dead_code)]` 标记

2. **短期（本周）**：
   - 迁移 overlap.rs 中的基础MA函数
   - 添加错误处理测试到现有测试套件

3. **中期（本月）**：
   - 完成 volume.rs 和 candlestick.rs 迁移
   - 更新所有 PyO3 包装器添加错误文档

4. **长期（下季度）**：
   - 迁移复杂模块（sfg, pandas_ta, harmonics）
   - 添加性能基准测试验证错误处理开销

## 参考文档

- **详细策略**: `docs/ERROR_HANDLING_STRATEGY.md`
- **CLAUDE.md**: 错误处理最佳实践章节
- **CONTRIBUTING.md**: 新指标开发规范
- **良好示例**: `src/indicators/momentum.rs`

## 统计数据

```
当前状态（2025-12-26）:
- NaN使用: 204次（跨15个文件）
- 已迁移模块: 3个（momentum, volatility, trend）
- 待迁移模块: 12个
- validation函数使用: 广泛（被误标记为dead_code）
```

---

**版本**: 1.0  
**创建日期**: 2025-12-26  
**状态**: APPROVED
