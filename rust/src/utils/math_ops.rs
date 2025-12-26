//! Mathematical Operations Module
//!
//! # Overview
//! This module provides vectorized mathematical operations compatible with
//! TA-Lib's Math Operators. All functions operate element-wise on price
//! vectors and support rolling window calculations where applicable.
//!
//! # Available Functions
//!
//! ## Rolling Window Operations
//! - [`max`] - Highest value over a specified period
//! - [`min`] - Lowest value over a specified period
//! - [`sum`] - Summation over a specified period
//! - [`minmax`] - Both min and max in single call
//! - [`minmaxindex`] - Indices of min and max values
//!
//! ## Arithmetic Operations
//! - [`add`] - Element-wise vector addition
//! - [`sub`] - Element-wise vector subtraction
//! - [`mult`] - Element-wise vector multiplication
//! - [`div`] - Element-wise vector division (NaN-safe)
//!
//! ## Unary Math Functions
//! - [`sqrt`] - Square root
//! - [`ln`] - Natural logarithm
//! - [`log10`] - Base-10 logarithm
//! - [`exp`] - Exponential (e^x)
//! - [`abs`] - Absolute value
//! - [`ceil`] - Ceiling (round up)
//! - [`floor`] - Floor (round down)
//!
//! ## Trigonometric Functions
//! - [`sin`], [`cos`], [`tan`] - Standard trig (radians)
//! - [`asin`], [`acos`], [`atan`] - Inverse trig (returns radians)
//! - [`sinh`], [`cosh`], [`tanh`] - Hyperbolic functions
//!
//! # Examples
//! ```rust
//! use haze_library::utils::math_ops::{add, sqrt, max};
//!
//! let a = vec![1.0, 4.0, 9.0, 16.0];
//! let b = vec![1.0, 1.0, 1.0, 1.0];
//!
//! let sum = add(&a, &b);        // [2.0, 5.0, 10.0, 17.0]
//! let roots = sqrt(&a);         // [1.0, 2.0, 3.0, 4.0]
//! let rolling_max = max(&a, 2); // [NaN, 4.0, 9.0, 16.0]
//! ```
//!
//! # Performance Characteristics
//! - Unary operations: O(n) with iterator-based implementation
//! - Rolling window operations: O(n) using efficient algorithms from stats module
//! - Division handles zero divisors gracefully (returns NaN)
//!
//! # Cross-References
//! - [`crate::utils::stats`] - Statistical functions (rolling_max, rolling_min, etc.)
//! - [`crate::utils::simd_ops`] - SIMD-optimized vector operations

#![allow(dead_code)]

use crate::init_result;
use crate::utils::math::is_not_zero;

/// MAX - Highest value over a specified period
///
/// 滚动窗口最大值
///
/// # 参数
/// - `values`: 输入序列
/// - `period`: 周期
///
/// # 返回
/// - 最大值序列（前 period-1 个值为 NaN）
pub fn max(values: &[f64], period: usize) -> Vec<f64> {
    crate::utils::rolling_max(values, period)
}

/// MIN - Lowest value over a specified period
///
/// 滚动窗口最小值
///
/// # 参数
/// - `values`: 输入序列
/// - `period`: 周期
///
/// # 返回
/// - 最小值序列（前 period-1 个值为 NaN）
pub fn min(values: &[f64], period: usize) -> Vec<f64> {
    crate::utils::rolling_min(values, period)
}

/// SUM - Summation over a specified period
///
/// 滚动窗口求和
///
/// # 参数
/// - `values`: 输入序列
/// - `period`: 周期
///
/// # 返回
/// - 求和序列（前 period-1 个值为 NaN）
pub fn sum(values: &[f64], period: usize) -> Vec<f64> {
    crate::utils::rolling_sum(values, period)
}

/// SQRT - Vector Square Root
///
/// 向量平方根（逐元素）
///
/// # 参数
/// - `values`: 输入序列
///
/// # 返回
/// - 平方根序列
pub fn sqrt(values: &[f64]) -> Vec<f64> {
    values.iter().map(|&x| x.sqrt()).collect()
}

/// LN - Vector Natural Logarithm
///
/// 向量自然对数（逐元素）
///
/// # 参数
/// - `values`: 输入序列
///
/// # 返回
/// - 自然对数序列
pub fn ln(values: &[f64]) -> Vec<f64> {
    values.iter().map(|&x| x.ln()).collect()
}

/// LOG10 - Vector Base-10 Logarithm
///
/// 向量常用对数（逐元素）
///
/// # 参数
/// - `values`: 输入序列
///
/// # 返回
/// - 常用对数序列
pub fn log10(values: &[f64]) -> Vec<f64> {
    values.iter().map(|&x| x.log10()).collect()
}

/// EXP - Vector Exponential
///
/// 向量指数函数（e^x）
///
/// # 参数
/// - `values`: 输入序列
///
/// # 返回
/// - e^x 序列
pub fn exp(values: &[f64]) -> Vec<f64> {
    values.iter().map(|&x| x.exp()).collect()
}

/// ABS - Vector Absolute Value
///
/// 向量绝对值（逐元素）
///
/// # 参数
/// - `values`: 输入序列
///
/// # 返回
/// - 绝对值序列
pub fn abs(values: &[f64]) -> Vec<f64> {
    values.iter().map(|&x| x.abs()).collect()
}

/// CEIL - Vector Ceiling
///
/// 向量向上取整（逐元素）
///
/// # 参数
/// - `values`: 输入序列
///
/// # 返回
/// - 向上取整序列
pub fn ceil(values: &[f64]) -> Vec<f64> {
    values.iter().map(|&x| x.ceil()).collect()
}

/// FLOOR - Vector Floor
///
/// 向量向下取整（逐元素）
///
/// # 参数
/// - `values`: 输入序列
///
/// # 返回
/// - 向下取整序列
pub fn floor(values: &[f64]) -> Vec<f64> {
    values.iter().map(|&x| x.floor()).collect()
}

/// SIN - Vector Sine
///
/// 向量正弦函数（逐元素，输入为弧度）
///
/// # 参数
/// - `values`: 输入序列（弧度）
///
/// # 返回
/// - 正弦值序列
pub fn sin(values: &[f64]) -> Vec<f64> {
    values.iter().map(|&x| x.sin()).collect()
}

/// COS - Vector Cosine
///
/// 向量余弦函数（逐元素，输入为弧度）
///
/// # 参数
/// - `values`: 输入序列（弧度）
///
/// # 返回
/// - 余弦值序列
pub fn cos(values: &[f64]) -> Vec<f64> {
    values.iter().map(|&x| x.cos()).collect()
}

/// TAN - Vector Tangent
///
/// 向量正切函数（逐元素，输入为弧度）
///
/// # 参数
/// - `values`: 输入序列（弧度）
///
/// # 返回
/// - 正切值序列
pub fn tan(values: &[f64]) -> Vec<f64> {
    values.iter().map(|&x| x.tan()).collect()
}

/// ASIN - Vector Inverse Sine
///
/// 向量反正弦函数（逐元素，返回弧度）
///
/// # 参数
/// - `values`: 输入序列（-1 到 1）
///
/// # 返回
/// - 反正弦值序列（弧度）
pub fn asin(values: &[f64]) -> Vec<f64> {
    values.iter().map(|&x| x.asin()).collect()
}

/// ACOS - Vector Inverse Cosine
///
/// 向量反余弦函数（逐元素，返回弧度）
///
/// # 参数
/// - `values`: 输入序列（-1 到 1）
///
/// # 返回
/// - 反余弦值序列（弧度）
pub fn acos(values: &[f64]) -> Vec<f64> {
    values.iter().map(|&x| x.acos()).collect()
}

/// ATAN - Vector Inverse Tangent
///
/// 向量反正切函数（逐元素，返回弧度）
///
/// # 参数
/// - `values`: 输入序列
///
/// # 返回
/// - 反正切值序列（弧度，-π/2 到 π/2）
pub fn atan(values: &[f64]) -> Vec<f64> {
    values.iter().map(|&x| x.atan()).collect()
}

/// SINH - Vector Hyperbolic Sine
///
/// 向量双曲正弦函数（逐元素）
///
/// # 参数
/// - `values`: 输入序列
///
/// # 返回
/// - 双曲正弦值序列
pub fn sinh(values: &[f64]) -> Vec<f64> {
    values.iter().map(|&x| x.sinh()).collect()
}

/// COSH - Vector Hyperbolic Cosine
///
/// 向量双曲余弦函数（逐元素）
///
/// # 参数
/// - `values`: 输入序列
///
/// # 返回
/// - 双曲余弦值序列
pub fn cosh(values: &[f64]) -> Vec<f64> {
    values.iter().map(|&x| x.cosh()).collect()
}

/// TANH - Vector Hyperbolic Tangent
///
/// 向量双曲正切函数（逐元素）
///
/// # 参数
/// - `values`: 输入序列
///
/// # 返回
/// - 双曲正切值序列
pub fn tanh(values: &[f64]) -> Vec<f64> {
    values.iter().map(|&x| x.tanh()).collect()
}

/// ADD - Vector Addition
///
/// 向量加法（逐元素）
///
/// # 参数
/// - `values1`: 第一个输入序列
/// - `values2`: 第二个输入序列
///
/// # 返回
/// - 和序列
pub fn add(values1: &[f64], values2: &[f64]) -> Vec<f64> {
    let n = values1.len().min(values2.len());
    let mut result = Vec::with_capacity(n);

    for i in 0..n {
        result.push(values1[i] + values2[i]);
    }

    result
}

/// SUB - Vector Subtraction
///
/// 向量减法（逐元素）
///
/// # 参数
/// - `values1`: 第一个输入序列
/// - `values2`: 第二个输入序列
///
/// # 返回
/// - 差序列
pub fn sub(values1: &[f64], values2: &[f64]) -> Vec<f64> {
    let n = values1.len().min(values2.len());
    let mut result = Vec::with_capacity(n);

    for i in 0..n {
        result.push(values1[i] - values2[i]);
    }

    result
}

/// MULT - Vector Multiplication
///
/// 向量乘法（逐元素）
///
/// # 参数
/// - `values1`: 第一个输入序列
/// - `values2`: 第二个输入序列
///
/// # 返回
/// - 积序列
pub fn mult(values1: &[f64], values2: &[f64]) -> Vec<f64> {
    let n = values1.len().min(values2.len());
    let mut result = Vec::with_capacity(n);

    for i in 0..n {
        result.push(values1[i] * values2[i]);
    }

    result
}

/// DIV - Vector Division
///
/// 向量除法（逐元素）
///
/// # 参数
/// - `values1`: 第一个输入序列（被除数）
/// - `values2`: 第二个输入序列（除数）
///
/// # 返回
/// - 商序列（除数为 0 时返回 NaN）
pub fn div(values1: &[f64], values2: &[f64]) -> Vec<f64> {
    let n = values1.len().min(values2.len());
    let mut result = Vec::with_capacity(n);

    for i in 0..n {
        if is_not_zero(values2[i]) {
            result.push(values1[i] / values2[i]);
        } else {
            result.push(f64::NAN);
        }
    }

    result
}

/// MINMAX - Lowest and Highest values over a specified period
///
/// 返回滚动窗口的最小值和最大值
///
/// # 参数
/// - `values`: 输入序列
/// - `period`: 周期
///
/// # 返回
/// - (min_values, max_values) 元组
pub fn minmax(values: &[f64], period: usize) -> (Vec<f64>, Vec<f64>) {
    let min_values = min(values, period);
    let max_values = max(values, period);
    (min_values, max_values)
}

/// MINMAXINDEX - Indexes of lowest and highest values over a specified period
///
/// 返回滚动窗口内最小值和最大值的索引
///
/// # 参数
/// - `values`: 输入序列
/// - `period`: 周期
///
/// # 返回
/// - (min_idx, max_idx) 元组（索引相对于窗口起始位置）
pub fn minmaxindex(values: &[f64], period: usize) -> (Vec<f64>, Vec<f64>) {
    let n = values.len();
    let mut min_idx = init_result!(n);
    let mut max_idx = init_result!(n);

    if period == 0 || period > n {
        return (min_idx, max_idx);
    }

    for i in (period - 1)..n {
        let window = &values[i + 1 - period..=i];

        let mut min_index = 0;
        let mut max_index = 0;
        let mut min_value = window[0];
        let mut max_value = window[0];

        for (j, &val) in window.iter().enumerate() {
            if val < min_value {
                min_value = val;
                min_index = j;
            }
            if val > max_value {
                max_value = val;
                max_index = j;
            }
        }

        min_idx[i] = min_index as f64;
        max_idx[i] = max_index as f64;
    }

    (min_idx, max_idx)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_sqrt() {
        let values = vec![4.0, 9.0, 16.0];
        let result = sqrt(&values);
        assert_eq!(result, vec![2.0, 3.0, 4.0]);
    }

    #[test]
    fn test_ln() {
        let values = vec![1.0, std::f64::consts::E, std::f64::consts::E.powi(2)];
        let result = ln(&values);
        assert!((result[0] - 0.0).abs() < 1e-10);
        assert!((result[1] - 1.0).abs() < 1e-10);
        assert!((result[2] - 2.0).abs() < 1e-10);
    }

    #[test]
    fn test_log10() {
        let values = vec![1.0, 10.0, 100.0];
        let result = log10(&values);
        assert_eq!(result, vec![0.0, 1.0, 2.0]);
    }

    #[test]
    fn test_trigonometric() {
        let values = vec![0.0, std::f64::consts::PI / 2.0];

        let sin_result = sin(&values);
        assert!((sin_result[0] - 0.0).abs() < 1e-10);
        assert!((sin_result[1] - 1.0).abs() < 1e-10);

        let cos_result = cos(&values);
        assert!((cos_result[0] - 1.0).abs() < 1e-10);
        assert!((cos_result[1] - 0.0).abs() < 1e-10);
    }

    #[test]
    fn test_add_sub_mult_div() {
        let a = vec![10.0, 20.0, 30.0];
        let b = vec![2.0, 4.0, 5.0];

        assert_eq!(add(&a, &b), vec![12.0, 24.0, 35.0]);
        assert_eq!(sub(&a, &b), vec![8.0, 16.0, 25.0]);
        assert_eq!(mult(&a, &b), vec![20.0, 80.0, 150.0]);
        assert_eq!(div(&a, &b), vec![5.0, 5.0, 6.0]);
    }

    #[test]
    fn test_minmax() {
        let values = vec![3.0, 1.0, 4.0, 1.0, 5.0];
        let (min_vals, max_vals) = minmax(&values, 3);

        assert!(min_vals[0].is_nan());
        assert!(min_vals[1].is_nan());
        assert_eq!(min_vals[2], 1.0); // min([3,1,4])
        assert_eq!(max_vals[2], 4.0); // max([3,1,4])
        assert_eq!(min_vals[4], 1.0); // min([4,1,5])
        assert_eq!(max_vals[4], 5.0); // max([4,1,5])
    }

    #[test]
    fn test_minmaxindex() {
        let values = vec![3.0, 1.0, 4.0, 1.0, 5.0];
        let (min_idx, max_idx) = minmaxindex(&values, 3);

        assert_eq!(min_idx[2], 1.0); // index of min in [3,1,4] is 1
        assert_eq!(max_idx[2], 2.0); // index of max in [3,1,4] is 2
    }
}
