// utils/simd_ops.rs - SIMD 优化的数学操作
#![allow(dead_code)]
//
// 使用编译器友好的代码结构启用自动向量化
// 遵循 KISS 原则：利用编译器优化而非手写 SIMD

/// SIMD 友好的向量加法
///
/// 编译器会自动向量化简单的 for 循环
#[inline]
pub fn add_vectors(a: &[f64], b: &[f64]) -> Vec<f64> {
    debug_assert_eq!(a.len(), b.len(), "Vector lengths must match");
    a.iter().zip(b.iter()).map(|(&x, &y)| x + y).collect()
}

/// SIMD 友好的向量减法
#[inline]
pub fn sub_vectors(a: &[f64], b: &[f64]) -> Vec<f64> {
    debug_assert_eq!(a.len(), b.len(), "Vector lengths must match");
    a.iter().zip(b.iter()).map(|(&x, &y)| x - y).collect()
}

/// SIMD 友好的向量乘法
#[inline]
pub fn mul_vectors(a: &[f64], b: &[f64]) -> Vec<f64> {
    debug_assert_eq!(a.len(), b.len(), "Vector lengths must match");
    a.iter().zip(b.iter()).map(|(&x, &y)| x * y).collect()
}

/// SIMD 友好的向量除法
#[inline]
pub fn div_vectors(a: &[f64], b: &[f64]) -> Vec<f64> {
    debug_assert_eq!(a.len(), b.len(), "Vector lengths must match");
    a.iter()
        .zip(b.iter())
        .map(|(&x, &y)| if y != 0.0 { x / y } else { f64::NAN })
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
#[inline]
pub fn dot_product(a: &[f64], b: &[f64]) -> f64 {
    debug_assert_eq!(a.len(), b.len(), "Vector lengths must match");

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
        return vec![f64::NAN; n];
    }

    let mut result = vec![f64::NAN; n];
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
        return vec![f64::NAN; n];
    }

    let alpha = 2.0 / (period as f64 + 1.0);
    let one_minus_alpha = 1.0 - alpha;

    let mut result = vec![f64::NAN; n];

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
    let variance: f64 = values.iter().map(|&x| (x - mean).powi(2)).sum::<f64>() / values.len() as f64;
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
