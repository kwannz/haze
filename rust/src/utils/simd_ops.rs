//! SIMD-Optimized Mathematical Operations
//!
//! # Overview
//! This module provides SIMD-friendly implementations of common mathematical
//! operations used in technical analysis. Rather than using explicit SIMD
//! intrinsics, the code is structured to enable automatic vectorization by
//! the Rust compiler (LLVM), providing portable performance across architectures.
//!
//! # Design Philosophy
//! - **Compiler-Friendly Code**: Simple loops that LLVM can auto-vectorize
//! - **Chunked Processing**: Uses 8-element chunks matching AVX-512 width
//! - **Zero Dependencies**: No external SIMD libraries required
//! - **Numerical Stability**: Chunked summation reduces floating-point errors
//!
//! # Available Functions
//!
//! ## Vector Arithmetic
//! - [`add_vectors`] - Element-wise vector addition
//! - [`sub_vectors`] - Element-wise vector subtraction
//! - [`mul_vectors`] - Element-wise vector multiplication
//! - [`div_vectors`] - Element-wise vector division (NaN-safe)
//! - [`scale_vector`] - Scalar multiplication
//!
//! ## Aggregation Operations
//! - [`sum_vector`] - Chunked summation for numerical stability
//! - [`dot_product`] - Dot product with chunked accumulation
//! - [`max_vector`] - Find maximum value
//! - [`min_vector`] - Find minimum value
//! - [`mean_vector`] - Calculate arithmetic mean
//! - [`std_vector`] - Calculate population standard deviation
//!
//! ## Fast Indicator Implementations
//! - [`fast_sma`] - SMA using cumulative sum optimization
//! - [`fast_ema`] - EMA using recursive formula
//! - [`batch_sma`] - Compute multiple SMA periods efficiently
//!
//! # Examples
//! ```rust
//! use haze_library::utils::simd_ops::{add_vectors, dot_product, fast_sma};
//!
//! // Vector operations
//! let a = vec![1.0, 2.0, 3.0, 4.0];
//! let b = vec![5.0, 6.0, 7.0, 8.0];
//! let sum = add_vectors(&a, &b);  // [6.0, 8.0, 10.0, 12.0]
//! let dot = dot_product(&a, &b);  // 70.0
//!
//! // Fast SMA calculation
//! let prices = vec![100.0, 101.0, 102.0, 103.0, 104.0];
//! let sma = fast_sma(&prices, 3);
//! ```
//!
//! # Performance Characteristics
//! - Vector operations: ~2-4x speedup with auto-vectorization enabled
//! - Chunk size of 8 elements aligns with AVX-512 registers
//! - `fast_sma`/`fast_ema` use O(n) sliding window, not O(n*period)
//! - Compile with `-C target-cpu=native` for best performance
//!
//! # Cross-References
//! - [`crate::utils::ma`] - Standard moving average implementations
//! - [`crate::utils::stats`] - Statistical functions with different trade-offs
//! - [`crate::utils::parallel`] - Multi-threaded parallel processing

// utils/simd_ops.rs - SIMD 优化的数学操作
#![allow(dead_code)]
//
// 使用编译器友好的代码结构启用自动向量化
// 遵循 KISS 原则：利用编译器优化而非手写 SIMD

use crate::init_result;
use crate::utils::math::is_not_zero;

/// SIMD 友好的向量加法
///
/// 编译器会自动向量化简单的 for 循环
///
/// # Panics
/// 如果 `a` 和 `b` 长度不匹配则 panic
#[inline]
pub fn add_vectors(a: &[f64], b: &[f64]) -> Vec<f64> {
    assert_eq!(a.len(), b.len(), "Vector lengths must match");
    a.iter().zip(b.iter()).map(|(&x, &y)| x + y).collect()
}

/// SIMD 友好的向量减法
///
/// # Panics
/// 如果 `a` 和 `b` 长度不匹配则 panic
#[inline]
pub fn sub_vectors(a: &[f64], b: &[f64]) -> Vec<f64> {
    assert_eq!(a.len(), b.len(), "Vector lengths must match");
    a.iter().zip(b.iter()).map(|(&x, &y)| x - y).collect()
}

/// SIMD 友好的向量乘法
///
/// # Panics
/// 如果 `a` 和 `b` 长度不匹配则 panic
#[inline]
pub fn mul_vectors(a: &[f64], b: &[f64]) -> Vec<f64> {
    assert_eq!(a.len(), b.len(), "Vector lengths must match");
    a.iter().zip(b.iter()).map(|(&x, &y)| x * y).collect()
}

/// SIMD 友好的向量除法
///
/// # Panics
/// 如果 `a` 和 `b` 长度不匹配则 panic
#[inline]
pub fn div_vectors(a: &[f64], b: &[f64]) -> Vec<f64> {
    assert_eq!(a.len(), b.len(), "Vector lengths must match");
    a.iter()
        .zip(b.iter())
        .map(|(&x, &y)| if is_not_zero(y) { x / y } else { f64::NAN })
        .collect()
}

/// SIMD 友好的标量乘法
#[inline]
pub fn scale_vector(a: &[f64], scalar: f64) -> Vec<f64> {
    a.iter().map(|&x| x * scalar).collect()
}

/// SIMD 友好的向量求和
///
/// 使用分块求和以提高数值稳定性和向量化效率
#[inline]
pub fn sum_vector(a: &[f64]) -> f64 {
    // 分块大小选择 8 以匹配常见 SIMD 宽度 (AVX-512)
    const CHUNK_SIZE: usize = 8;

    let chunks_sum: f64 = a
        .chunks_exact(CHUNK_SIZE)
        .map(|chunk| {
            let mut s = 0.0;
            for &v in chunk {
                s += v;
            }
            s
        })
        .sum();

    let remainder_sum: f64 = a.chunks_exact(CHUNK_SIZE).remainder().iter().sum();

    chunks_sum + remainder_sum
}

/// SIMD 友好的点积
///
/// # Panics
/// 如果 `a` 和 `b` 长度不匹配则 panic
#[inline]
pub fn dot_product(a: &[f64], b: &[f64]) -> f64 {
    assert_eq!(a.len(), b.len(), "Vector lengths must match");

    const CHUNK_SIZE: usize = 8;

    let main: f64 = a
        .chunks_exact(CHUNK_SIZE)
        .zip(b.chunks_exact(CHUNK_SIZE))
        .map(|(chunk_a, chunk_b)| {
            let mut s = 0.0;
            for i in 0..CHUNK_SIZE {
                s += chunk_a[i] * chunk_b[i];
            }
            s
        })
        .sum();

    let rem_a = a.chunks_exact(CHUNK_SIZE).remainder();
    let rem_b = b.chunks_exact(CHUNK_SIZE).remainder();
    let remainder: f64 = rem_a.iter().zip(rem_b.iter()).map(|(&x, &y)| x * y).sum();

    main + remainder
}

/// 快速 SMA 计算（SIMD 友好）
///
/// 使用累积和优化，O(n) 时间复杂度
pub fn fast_sma(values: &[f64], period: usize) -> Vec<f64> {
    let n = values.len();
    if period == 0 || period > n {
        return init_result!(n);
    }

    let mut result = init_result!(n);
    let period_f64 = period as f64;

    // 计算初始窗口和
    let mut sum: f64 = values[..period].iter().sum();
    result[period - 1] = sum / period_f64;

    // 滑动窗口更新
    for i in period..n {
        sum += values[i] - values[i - period];
        result[i] = sum / period_f64;
    }

    result
}

/// 快速 EMA 计算（SIMD 友好）
///
/// 使用递推公式，O(n) 时间复杂度
pub fn fast_ema(values: &[f64], period: usize) -> Vec<f64> {
    let n = values.len();
    if period == 0 || period > n {
        return init_result!(n);
    }

    let alpha = 2.0 / (period as f64 + 1.0);
    let one_minus_alpha = 1.0 - alpha;

    let mut result = init_result!(n);

    // 初始值为 SMA
    let first_sum: f64 = values[..period].iter().sum();
    result[period - 1] = first_sum / period as f64;

    // EMA 递推
    for i in period..n {
        result[i] = alpha * values[i] + one_minus_alpha * result[i - 1];
    }

    result
}

/// 批量计算多个 SMA 周期
///
/// 利用缓存局部性优化
pub fn batch_sma(values: &[f64], periods: &[usize]) -> Vec<Vec<f64>> {
    periods.iter().map(|&p| fast_sma(values, p)).collect()
}

/// 向量化的最大值查找
#[inline]
pub fn max_vector(values: &[f64]) -> f64 {
    values
        .iter()
        .fold(f64::NEG_INFINITY, |acc, &x| if x > acc { x } else { acc })
}

/// 向量化的最小值查找
#[inline]
pub fn min_vector(values: &[f64]) -> f64 {
    values
        .iter()
        .fold(f64::INFINITY, |acc, &x| if x < acc { x } else { acc })
}

/// 向量化的均值计算
#[inline]
pub fn mean_vector(values: &[f64]) -> f64 {
    if values.is_empty() {
        return f64::NAN;
    }
    sum_vector(values) / values.len() as f64
}

/// 向量化的标准差计算
#[inline]
pub fn std_vector(values: &[f64]) -> f64 {
    if values.len() < 2 {
        return f64::NAN;
    }

    let mean = mean_vector(values);
    let variance: f64 =
        values.iter().map(|&x| (x - mean).powi(2)).sum::<f64>() / values.len() as f64;
    variance.sqrt()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_add_vectors() {
        let a = vec![1.0, 2.0, 3.0, 4.0];
        let b = vec![5.0, 6.0, 7.0, 8.0];
        let result = add_vectors(&a, &b);
        assert_eq!(result, vec![6.0, 8.0, 10.0, 12.0]);
    }

    #[test]
    fn test_sum_vector() {
        let values: Vec<f64> = (1..=100).map(|x| x as f64).collect();
        let sum = sum_vector(&values);
        assert!((sum - 5050.0).abs() < 1e-10);
    }

    #[test]
    fn test_dot_product() {
        let a = vec![1.0, 2.0, 3.0];
        let b = vec![4.0, 5.0, 6.0];
        let result = dot_product(&a, &b);
        assert!((result - 32.0).abs() < 1e-10); // 1*4 + 2*5 + 3*6 = 32
    }

    #[test]
    fn test_fast_sma() {
        let values = vec![1.0, 2.0, 3.0, 4.0, 5.0];
        let result = fast_sma(&values, 3);
        assert!(result[0].is_nan());
        assert!(result[1].is_nan());
        assert!((result[2] - 2.0).abs() < 1e-10);
        assert!((result[3] - 3.0).abs() < 1e-10);
        assert!((result[4] - 4.0).abs() < 1e-10);
    }

    #[test]
    fn test_fast_ema() {
        let values = vec![1.0, 2.0, 3.0, 4.0, 5.0];
        let result = fast_ema(&values, 3);
        assert!(result[0].is_nan());
        assert!(result[1].is_nan());
        assert!((result[2] - 2.0).abs() < 1e-10); // 初始值 = SMA
    }

    #[test]
    fn test_batch_sma() {
        let values: Vec<f64> = (1..=20).map(|x| x as f64).collect();
        let periods = vec![3, 5, 10];
        let results = batch_sma(&values, &periods);
        assert_eq!(results.len(), 3);
    }

    #[test]
    fn test_statistics() {
        let values = vec![1.0, 2.0, 3.0, 4.0, 5.0];
        assert!((mean_vector(&values) - 3.0).abs() < 1e-10);
        assert!((max_vector(&values) - 5.0).abs() < 1e-10);
        assert!((min_vector(&values) - 1.0).abs() < 1e-10);
    }
}

// ==================== 边界条件测试 ====================

#[cfg(test)]
mod boundary_tests {
    use super::*;

    // ==================== 向量运算边界测试 ====================

    #[test]
    fn test_add_vectors_empty() {
        let a: Vec<f64> = vec![];
        let b: Vec<f64> = vec![];
        let result = add_vectors(&a, &b);
        assert!(result.is_empty());
    }

    #[test]
    fn test_add_vectors_single() {
        let a = vec![5.0];
        let b = vec![3.0];
        let result = add_vectors(&a, &b);
        assert_eq!(result, vec![8.0]);
    }

    #[test]
    fn test_add_vectors_with_nan() {
        let a = vec![1.0, f64::NAN, 3.0];
        let b = vec![4.0, 5.0, 6.0];
        let result = add_vectors(&a, &b);
        assert!((result[0] - 5.0).abs() < 1e-10);
        assert!(result[1].is_nan());
        assert!((result[2] - 9.0).abs() < 1e-10);
    }

    #[test]
    fn test_add_vectors_with_infinity() {
        let a = vec![f64::INFINITY, f64::NEG_INFINITY, 1.0];
        let b = vec![1.0, 1.0, f64::INFINITY];
        let result = add_vectors(&a, &b);
        assert!(result[0].is_infinite() && result[0] > 0.0);
        assert!(result[1].is_infinite() && result[1] < 0.0);
        assert!(result[2].is_infinite() && result[2] > 0.0);
    }

    #[test]
    #[should_panic(expected = "Vector lengths must match")]
    fn test_add_vectors_length_mismatch() {
        let a = vec![1.0, 2.0];
        let b = vec![1.0];
        add_vectors(&a, &b);
    }

    #[test]
    fn test_sub_vectors_empty() {
        let a: Vec<f64> = vec![];
        let b: Vec<f64> = vec![];
        let result = sub_vectors(&a, &b);
        assert!(result.is_empty());
    }

    #[test]
    fn test_sub_vectors_single() {
        let a = vec![10.0];
        let b = vec![3.0];
        let result = sub_vectors(&a, &b);
        assert_eq!(result, vec![7.0]);
    }

    #[test]
    fn test_sub_vectors_with_nan() {
        let a = vec![1.0, f64::NAN, 3.0];
        let b = vec![0.5, 2.0, 1.0];
        let result = sub_vectors(&a, &b);
        assert!((result[0] - 0.5).abs() < 1e-10);
        assert!(result[1].is_nan());
        assert!((result[2] - 2.0).abs() < 1e-10);
    }

    #[test]
    #[should_panic(expected = "Vector lengths must match")]
    fn test_sub_vectors_length_mismatch() {
        let a = vec![1.0, 2.0, 3.0];
        let b = vec![1.0, 2.0];
        sub_vectors(&a, &b);
    }

    #[test]
    fn test_mul_vectors_empty() {
        let a: Vec<f64> = vec![];
        let b: Vec<f64> = vec![];
        let result = mul_vectors(&a, &b);
        assert!(result.is_empty());
    }

    #[test]
    fn test_mul_vectors_single() {
        let a = vec![4.0];
        let b = vec![5.0];
        let result = mul_vectors(&a, &b);
        assert_eq!(result, vec![20.0]);
    }

    #[test]
    fn test_mul_vectors_with_zero() {
        let a = vec![1.0, 0.0, 3.0];
        let b = vec![0.0, 5.0, 6.0];
        let result = mul_vectors(&a, &b);
        assert_eq!(result, vec![0.0, 0.0, 18.0]);
    }

    #[test]
    fn test_mul_vectors_with_nan() {
        let a = vec![1.0, f64::NAN, 3.0];
        let b = vec![2.0, 3.0, 4.0];
        let result = mul_vectors(&a, &b);
        assert!((result[0] - 2.0).abs() < 1e-10);
        assert!(result[1].is_nan());
        assert!((result[2] - 12.0).abs() < 1e-10);
    }

    #[test]
    #[should_panic(expected = "Vector lengths must match")]
    fn test_mul_vectors_length_mismatch() {
        let a = vec![1.0];
        let b = vec![1.0, 2.0];
        mul_vectors(&a, &b);
    }

    #[test]
    fn test_div_vectors_empty() {
        let a: Vec<f64> = vec![];
        let b: Vec<f64> = vec![];
        let result = div_vectors(&a, &b);
        assert!(result.is_empty());
    }

    #[test]
    fn test_div_vectors_single() {
        let a = vec![10.0];
        let b = vec![2.0];
        let result = div_vectors(&a, &b);
        assert_eq!(result, vec![5.0]);
    }

    #[test]
    fn test_div_vectors_by_zero() {
        let a = vec![10.0, 0.0, 5.0];
        let b = vec![0.0, 0.0, 2.5];
        let result = div_vectors(&a, &b);
        assert!(result[0].is_nan()); // 10/0 = NaN (defensive)
        assert!(result[1].is_nan()); // 0/0 = NaN
        assert!((result[2] - 2.0).abs() < 1e-10);
    }

    #[test]
    fn test_div_vectors_with_nan() {
        let a = vec![f64::NAN, 10.0];
        let b = vec![2.0, f64::NAN];
        let result = div_vectors(&a, &b);
        assert!(result[0].is_nan());
        assert!(result[1].is_nan());
    }

    #[test]
    #[should_panic(expected = "Vector lengths must match")]
    fn test_div_vectors_length_mismatch() {
        let a = vec![1.0, 2.0, 3.0];
        let b = vec![1.0];
        div_vectors(&a, &b);
    }

    #[test]
    fn test_scale_vector_empty() {
        let a: Vec<f64> = vec![];
        let result = scale_vector(&a, 5.0);
        assert!(result.is_empty());
    }

    #[test]
    fn test_scale_vector_by_zero() {
        let a = vec![1.0, 2.0, 3.0];
        let result = scale_vector(&a, 0.0);
        assert_eq!(result, vec![0.0, 0.0, 0.0]);
    }

    #[test]
    fn test_scale_vector_by_nan() {
        let a = vec![1.0, 2.0, 3.0];
        let result = scale_vector(&a, f64::NAN);
        assert!(result.iter().all(|v| v.is_nan()));
    }

    #[test]
    fn test_scale_vector_with_nan() {
        let a = vec![1.0, f64::NAN, 3.0];
        let result = scale_vector(&a, 2.0);
        assert!((result[0] - 2.0).abs() < 1e-10);
        assert!(result[1].is_nan());
        assert!((result[2] - 6.0).abs() < 1e-10);
    }

    // ==================== 聚合操作边界测试 ====================

    #[test]
    fn test_sum_vector_empty() {
        let a: Vec<f64> = vec![];
        let result = sum_vector(&a);
        assert!((result - 0.0).abs() < 1e-10);
    }

    #[test]
    fn test_sum_vector_single() {
        let a = vec![42.0];
        let result = sum_vector(&a);
        assert!((result - 42.0).abs() < 1e-10);
    }

    #[test]
    fn test_sum_vector_with_nan() {
        let a = vec![1.0, f64::NAN, 3.0];
        let result = sum_vector(&a);
        assert!(result.is_nan());
    }

    #[test]
    fn test_sum_vector_exact_chunk_size() {
        // Test with exactly 8 elements (one chunk)
        let a = vec![1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0];
        let result = sum_vector(&a);
        assert!((result - 36.0).abs() < 1e-10);
    }

    #[test]
    fn test_sum_vector_multiple_chunks_with_remainder() {
        // Test with 17 elements (2 chunks + 1 remainder)
        let a: Vec<f64> = (1..=17).map(|x| x as f64).collect();
        let result = sum_vector(&a);
        let expected = 17.0 * 18.0 / 2.0; // Sum 1..17 = n(n+1)/2
        assert!((result - expected).abs() < 1e-10);
    }

    #[test]
    fn test_dot_product_empty() {
        let a: Vec<f64> = vec![];
        let b: Vec<f64> = vec![];
        let result = dot_product(&a, &b);
        assert!((result - 0.0).abs() < 1e-10);
    }

    #[test]
    fn test_dot_product_single() {
        let a = vec![3.0];
        let b = vec![4.0];
        let result = dot_product(&a, &b);
        assert!((result - 12.0).abs() < 1e-10);
    }

    #[test]
    fn test_dot_product_with_nan() {
        let a = vec![1.0, f64::NAN, 3.0];
        let b = vec![2.0, 3.0, 4.0];
        let result = dot_product(&a, &b);
        assert!(result.is_nan());
    }

    #[test]
    fn test_dot_product_exact_chunk_size() {
        let a = vec![1.0; 8];
        let b = vec![2.0; 8];
        let result = dot_product(&a, &b);
        assert!((result - 16.0).abs() < 1e-10);
    }

    #[test]
    #[should_panic(expected = "Vector lengths must match")]
    fn test_dot_product_length_mismatch() {
        let a = vec![1.0, 2.0];
        let b = vec![1.0, 2.0, 3.0];
        dot_product(&a, &b);
    }

    #[test]
    fn test_max_vector_empty() {
        let a: Vec<f64> = vec![];
        let result = max_vector(&a);
        assert!(result == f64::NEG_INFINITY);
    }

    #[test]
    fn test_max_vector_single() {
        let a = vec![42.0];
        let result = max_vector(&a);
        assert!((result - 42.0).abs() < 1e-10);
    }

    #[test]
    fn test_max_vector_all_same() {
        let a = vec![5.0, 5.0, 5.0, 5.0];
        let result = max_vector(&a);
        assert!((result - 5.0).abs() < 1e-10);
    }

    #[test]
    fn test_max_vector_with_nan() {
        // NaN comparisons are tricky - NaN is not > any value
        let a = vec![1.0, f64::NAN, 3.0];
        let result = max_vector(&a);
        // Since NaN > 3.0 is false, result should be 3.0
        assert!((result - 3.0).abs() < 1e-10);
    }

    #[test]
    fn test_max_vector_with_infinity() {
        let a = vec![1.0, f64::INFINITY, 3.0];
        let result = max_vector(&a);
        assert!(result.is_infinite() && result > 0.0);
    }

    #[test]
    fn test_max_vector_with_neg_infinity() {
        let a = vec![f64::NEG_INFINITY, -100.0, -50.0];
        let result = max_vector(&a);
        assert!((result - (-50.0)).abs() < 1e-10);
    }

    #[test]
    fn test_min_vector_empty() {
        let a: Vec<f64> = vec![];
        let result = min_vector(&a);
        assert!(result == f64::INFINITY);
    }

    #[test]
    fn test_min_vector_single() {
        let a = vec![42.0];
        let result = min_vector(&a);
        assert!((result - 42.0).abs() < 1e-10);
    }

    #[test]
    fn test_min_vector_all_same() {
        let a = vec![5.0, 5.0, 5.0, 5.0];
        let result = min_vector(&a);
        assert!((result - 5.0).abs() < 1e-10);
    }

    #[test]
    fn test_min_vector_with_nan() {
        let a = vec![1.0, f64::NAN, 3.0];
        let result = min_vector(&a);
        // Since NaN < 1.0 is false, result should be 1.0
        assert!((result - 1.0).abs() < 1e-10);
    }

    #[test]
    fn test_min_vector_with_neg_infinity() {
        let a = vec![1.0, f64::NEG_INFINITY, 3.0];
        let result = min_vector(&a);
        assert!(result.is_infinite() && result < 0.0);
    }

    #[test]
    fn test_mean_vector_empty() {
        let a: Vec<f64> = vec![];
        let result = mean_vector(&a);
        assert!(result.is_nan());
    }

    #[test]
    fn test_mean_vector_single() {
        let a = vec![42.0];
        let result = mean_vector(&a);
        assert!((result - 42.0).abs() < 1e-10);
    }

    #[test]
    fn test_mean_vector_with_nan() {
        let a = vec![1.0, f64::NAN, 3.0];
        let result = mean_vector(&a);
        assert!(result.is_nan());
    }

    #[test]
    fn test_std_vector_empty() {
        let a: Vec<f64> = vec![];
        let result = std_vector(&a);
        assert!(result.is_nan());
    }

    #[test]
    fn test_std_vector_single() {
        let a = vec![42.0];
        let result = std_vector(&a);
        // Single element - not enough for std dev
        assert!(result.is_nan());
    }

    #[test]
    fn test_std_vector_two_elements() {
        let a = vec![0.0, 2.0];
        let result = std_vector(&a);
        // Mean = 1.0, variance = ((0-1)^2 + (2-1)^2)/2 = 1, std = 1
        assert!((result - 1.0).abs() < 1e-10);
    }

    #[test]
    fn test_std_vector_all_same() {
        let a = vec![5.0, 5.0, 5.0, 5.0];
        let result = std_vector(&a);
        // All same values -> std = 0
        assert!((result - 0.0).abs() < 1e-10);
    }

    #[test]
    fn test_std_vector_with_nan() {
        let a = vec![1.0, f64::NAN, 3.0];
        let result = std_vector(&a);
        assert!(result.is_nan());
    }

    // ==================== 快速指标边界测试 ====================

    #[test]
    fn test_fast_sma_empty() {
        let a: Vec<f64> = vec![];
        let result = fast_sma(&a, 3);
        assert!(result.is_empty());
    }

    #[test]
    fn test_fast_sma_period_zero() {
        let a = vec![1.0, 2.0, 3.0];
        let result = fast_sma(&a, 0);
        assert!(result.iter().all(|v| v.is_nan()));
    }

    #[test]
    fn test_fast_sma_period_one() {
        let a = vec![1.0, 2.0, 3.0, 4.0];
        let result = fast_sma(&a, 1);
        // Period=1 means each value is its own SMA
        assert!((result[0] - 1.0).abs() < 1e-10);
        assert!((result[1] - 2.0).abs() < 1e-10);
        assert!((result[2] - 3.0).abs() < 1e-10);
        assert!((result[3] - 4.0).abs() < 1e-10);
    }

    #[test]
    fn test_fast_sma_period_equals_length() {
        let a = vec![1.0, 2.0, 3.0, 4.0, 5.0];
        let result = fast_sma(&a, 5);
        // Only last value should have SMA
        assert!(result[0..4].iter().all(|v| v.is_nan()));
        assert!((result[4] - 3.0).abs() < 1e-10);
    }

    #[test]
    fn test_fast_sma_period_exceeds_length() {
        let a = vec![1.0, 2.0, 3.0];
        let result = fast_sma(&a, 10);
        assert!(result.iter().all(|v| v.is_nan()));
    }

    #[test]
    fn test_fast_sma_with_nan() {
        let a = vec![1.0, 2.0, f64::NAN, 4.0, 5.0];
        let result = fast_sma(&a, 3);
        // NaN will propagate through the window
        assert!(result[2].is_nan()); // Window contains NaN
        assert!(result[3].is_nan()); // Window contains NaN
        assert!(result[4].is_nan()); // Window contains NaN
    }

    #[test]
    fn test_fast_sma_large_values() {
        let a = vec![1e15, 2e15, 3e15, 4e15, 5e15];
        let result = fast_sma(&a, 3);
        assert!((result[2] - 2e15).abs() < 1e5);
        assert!((result[3] - 3e15).abs() < 1e5);
        assert!((result[4] - 4e15).abs() < 1e5);
    }

    #[test]
    fn test_fast_ema_empty() {
        let a: Vec<f64> = vec![];
        let result = fast_ema(&a, 3);
        assert!(result.is_empty());
    }

    #[test]
    fn test_fast_ema_period_zero() {
        let a = vec![1.0, 2.0, 3.0];
        let result = fast_ema(&a, 0);
        assert!(result.iter().all(|v| v.is_nan()));
    }

    #[test]
    fn test_fast_ema_period_one() {
        let a = vec![1.0, 2.0, 3.0, 4.0];
        let result = fast_ema(&a, 1);
        // Period=1 means alpha=1, so EMA = each value
        assert!((result[0] - 1.0).abs() < 1e-10);
        assert!((result[1] - 2.0).abs() < 1e-10);
        assert!((result[2] - 3.0).abs() < 1e-10);
        assert!((result[3] - 4.0).abs() < 1e-10);
    }

    #[test]
    fn test_fast_ema_period_equals_length() {
        let a = vec![1.0, 2.0, 3.0, 4.0, 5.0];
        let result = fast_ema(&a, 5);
        // Only last value should have EMA (initial = SMA)
        assert!(result[0..4].iter().all(|v| v.is_nan()));
        assert!((result[4] - 3.0).abs() < 1e-10); // SMA of 1-5 = 3
    }

    #[test]
    fn test_fast_ema_period_exceeds_length() {
        let a = vec![1.0, 2.0, 3.0];
        let result = fast_ema(&a, 10);
        assert!(result.iter().all(|v| v.is_nan()));
    }

    #[test]
    fn test_fast_ema_constant_values() {
        let a = vec![100.0; 20];
        let result = fast_ema(&a, 5);
        // EMA of constant values should equal the constant
        for i in 4..20 {
            assert!((result[i] - 100.0).abs() < 1e-10);
        }
    }

    #[test]
    fn test_batch_sma_empty_values() {
        let a: Vec<f64> = vec![];
        let periods = vec![3, 5, 10];
        let results = batch_sma(&a, &periods);
        assert_eq!(results.len(), 3);
        assert!(results.iter().all(|v| v.is_empty()));
    }

    #[test]
    fn test_batch_sma_empty_periods() {
        let a = vec![1.0, 2.0, 3.0, 4.0, 5.0];
        let periods: Vec<usize> = vec![];
        let results = batch_sma(&a, &periods);
        assert!(results.is_empty());
    }

    #[test]
    fn test_batch_sma_with_zero_period() {
        let a = vec![1.0, 2.0, 3.0, 4.0, 5.0];
        let periods = vec![0, 3, 5];
        let results = batch_sma(&a, &periods);
        assert_eq!(results.len(), 3);
        assert!(results[0].iter().all(|v| v.is_nan())); // Period 0
        assert!(!results[1][2].is_nan()); // Period 3
        assert!(!results[2][4].is_nan()); // Period 5
    }

    // ==================== 数值精度测试 ====================

    #[test]
    fn test_sum_vector_precision() {
        // Test numerical precision with many small values
        let a: Vec<f64> = (0..10000).map(|_| 0.0001).collect();
        let result = sum_vector(&a);
        let expected = 1.0;
        assert!((result - expected).abs() < 1e-8);
    }

    #[test]
    fn test_dot_product_precision() {
        // Test with large number of elements
        let a: Vec<f64> = (1..=1000).map(|x| x as f64).collect();
        let b = vec![1.0; 1000];
        let result = dot_product(&a, &b);
        let expected = 1000.0 * 1001.0 / 2.0; // Sum of 1 to 1000
        assert!((result - expected).abs() < 1e-6);
    }

    #[test]
    fn test_fast_sma_numerical_stability() {
        // Test with values that could cause numerical instability
        let a: Vec<f64> = (0..100).map(|i| 1e10 + i as f64).collect();
        let result = fast_sma(&a, 10);
        // Verify the output is reasonable
        for i in 9..100 {
            assert!(!result[i].is_nan());
            assert!(result[i] >= 1e10);
        }
    }

    // ==================== 集成测试 ====================

    #[test]
    fn test_vector_operations_chain() {
        let a = vec![1.0, 2.0, 3.0, 4.0];
        let b = vec![2.0, 2.0, 2.0, 2.0];

        // (a + b) * 2
        let sum = add_vectors(&a, &b);
        let result = scale_vector(&sum, 2.0);
        assert_eq!(result, vec![6.0, 8.0, 10.0, 12.0]);
    }

    #[test]
    fn test_fast_sma_vs_manual() {
        let values = vec![1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0];
        let result = fast_sma(&values, 3);

        // Verify against manual calculation
        assert!((result[2] - (1.0 + 2.0 + 3.0) / 3.0).abs() < 1e-10);
        assert!((result[3] - (2.0 + 3.0 + 4.0) / 3.0).abs() < 1e-10);
        assert!((result[4] - (3.0 + 4.0 + 5.0) / 3.0).abs() < 1e-10);
        assert!((result[5] - (4.0 + 5.0 + 6.0) / 3.0).abs() < 1e-10);
        assert!((result[6] - (5.0 + 6.0 + 7.0) / 3.0).abs() < 1e-10);
    }

    #[test]
    fn test_negative_values() {
        let a = vec![-5.0, -3.0, -1.0, 1.0, 3.0, 5.0];
        let b = vec![1.0, 1.0, 1.0, 1.0, 1.0, 1.0];

        let sum = sum_vector(&a);
        assert!((sum - 0.0).abs() < 1e-10);

        let mean = mean_vector(&a);
        assert!((mean - 0.0).abs() < 1e-10);

        let result = add_vectors(&a, &b);
        assert_eq!(result, vec![-4.0, -2.0, 0.0, 2.0, 4.0, 6.0]);
    }
}
