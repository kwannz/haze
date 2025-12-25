// utils/stats.rs - 统计工具函数
#![allow(dead_code)]

use std::collections::VecDeque;

/// 标准差（样本标准差，使用 n-1 作为分母）
///
/// # 参数
/// - `values`: 输入序列
/// - `period`: 周期
///
/// # 返回
/// - 与输入等长的向量，前 period-1 个值为 NaN
pub fn stdev(values: &[f64], period: usize) -> Vec<f64> {
    if period < 2 || period > values.len() {
        return vec![f64::NAN; values.len()];
    }

    let mut result = vec![f64::NAN; values.len()];

    for i in (period - 1)..values.len() {
        let window = &values[i + 1 - period..=i];
        let mean: f64 = window.iter().sum::<f64>() / period as f64;
        let variance: f64 = window
            .iter()
            .map(|&x| (x - mean).powi(2))
            .sum::<f64>()
            / (period - 1) as f64;
        result[i] = variance.sqrt();
    }

    result
}

/// 最大值（滚动窗口）
///
/// # 参数
/// - `values`: 输入序列
/// - `period`: 周期
///
/// # 返回
/// - 与输入等长的向量，前 period-1 个值为 NaN
pub fn rolling_max(values: &[f64], period: usize) -> Vec<f64> {
    if period == 0 || period > values.len() {
        return vec![f64::NAN; values.len()];
    }

    let mut result = vec![f64::NAN; values.len()];
    let mut deque: VecDeque<usize> = VecDeque::new();
    let mut nan_count = 0usize;

    for i in 0..values.len() {
        if values[i].is_nan() {
            nan_count += 1;
        }

        if i >= period {
            let out_idx = i - period;
            if values[out_idx].is_nan() {
                nan_count -= 1;
            }
            if deque.front() == Some(&out_idx) {
                deque.pop_front();
            }
        }

        if !values[i].is_nan() {
            while let Some(&back) = deque.back() {
                if values[back] <= values[i] {
                    deque.pop_back();
                } else {
                    break;
                }
            }
            deque.push_back(i);
        }

        if i + 1 >= period {
            result[i] = if nan_count > 0 {
                f64::NAN
            } else {
                debug_assert!(!deque.is_empty());
                values[*deque.front().unwrap()]
            };
        }
    }

    result
}

/// 最小值（滚动窗口）
///
/// # 参数
/// - `values`: 输入序列
/// - `period`: 周期
///
/// # 返回
/// - 与输入等长的向量，前 period-1 个值为 NaN
pub fn rolling_min(values: &[f64], period: usize) -> Vec<f64> {
    if period == 0 || period > values.len() {
        return vec![f64::NAN; values.len()];
    }

    let mut result = vec![f64::NAN; values.len()];
    let mut deque: VecDeque<usize> = VecDeque::new();
    let mut nan_count = 0usize;

    for i in 0..values.len() {
        if values[i].is_nan() {
            nan_count += 1;
        }

        if i >= period {
            let out_idx = i - period;
            if values[out_idx].is_nan() {
                nan_count -= 1;
            }
            if deque.front() == Some(&out_idx) {
                deque.pop_front();
            }
        }

        if !values[i].is_nan() {
            while let Some(&back) = deque.back() {
                if values[back] >= values[i] {
                    deque.pop_back();
                } else {
                    break;
                }
            }
            deque.push_back(i);
        }

        if i + 1 >= period {
            result[i] = if nan_count > 0 {
                f64::NAN
            } else {
                debug_assert!(!deque.is_empty());
                values[*deque.front().unwrap()]
            };
        }
    }

    result
}

/// 求和（滚动窗口）
pub fn rolling_sum(values: &[f64], period: usize) -> Vec<f64> {
    if period == 0 || period > values.len() {
        return vec![f64::NAN; values.len()];
    }

    let mut result = vec![f64::NAN; values.len()];

    // 第一个窗口
    let first_sum: f64 = values[..period].iter().sum();
    result[period - 1] = first_sum;

    // 滚动计算（优化：增量更新）
    for i in period..values.len() {
        result[i] = result[i - 1] + values[i] - values[i - period];
    }

    result
}

/// 百分位数（滚动窗口）
///
/// # 参数
/// - `values`: 输入序列
/// - `period`: 周期
/// - `percentile`: 百分位（0.0 - 1.0），如 0.5 表示中位数
///
/// # 返回
/// - 与输入等长的向量
pub fn rolling_percentile(values: &[f64], period: usize, percentile: f64) -> Vec<f64> {
    if period == 0 || period > values.len() || percentile < 0.0 || percentile > 1.0 {
        return vec![f64::NAN; values.len()];
    }

    let mut result = vec![f64::NAN; values.len()];

    for i in (period - 1)..values.len() {
        let mut window: Vec<f64> = values[i + 1 - period..=i].to_vec();
        window.sort_by(|a, b| a.partial_cmp(b).unwrap());

        let index = (percentile * (period - 1) as f64).round() as usize;
        result[i] = window[index];
    }

    result
}

/// 变化率（Rate of Change）
///
/// # 参数
/// - `values`: 输入序列
/// - `period`: 周期
///
/// # 返回
/// - ROC[i] = (values[i] / values[i-period] - 1) * 100
pub fn roc(values: &[f64], period: usize) -> Vec<f64> {
    if period == 0 || period >= values.len() {
        return vec![f64::NAN; values.len()];
    }

    let mut result = vec![f64::NAN; values.len()];

    for i in period..values.len() {
        if values[i - period] != 0.0 {
            result[i] = ((values[i] / values[i - period]) - 1.0) * 100.0;
        }
    }

    result
}

/// 动量（Momentum）
///
/// # 参数
/// - `values`: 输入序列
/// - `period`: 周期
///
/// # 返回
/// - MOM[i] = values[i] - values[i-period]
pub fn momentum(values: &[f64], period: usize) -> Vec<f64> {
    if period == 0 || period >= values.len() {
        return vec![f64::NAN; values.len()];
    }

    let mut result = vec![f64::NAN; values.len()];

    for i in period..values.len() {
        result[i] = values[i] - values[i - period];
    }

    result
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_stdev() {
        let values = vec![1.0, 2.0, 3.0, 4.0, 5.0];
        let result = stdev(&values, 3);
        assert!(result[0].is_nan());
        assert!(result[1].is_nan());
        // stdev([1,2,3]) = sqrt(((1-2)^2 + (2-2)^2 + (3-2)^2) / 2) = 1.0
        assert!((result[2] - 1.0).abs() < 1e-10);
    }

    #[test]
    fn test_rolling_max() {
        let values = vec![1.0, 3.0, 2.0, 5.0, 4.0];
        let result = rolling_max(&values, 3);
        assert!(result[0].is_nan());
        assert!(result[1].is_nan());
        assert_eq!(result[2], 3.0);  // max([1,3,2])
        assert_eq!(result[3], 5.0);  // max([3,2,5])
        assert_eq!(result[4], 5.0);  // max([2,5,4])
    }

    #[test]
    fn test_rolling_max_min_with_nan() {
        let values = vec![1.0, f64::NAN, 2.0, 3.0];
        let max_result = rolling_max(&values, 2);
        let min_result = rolling_min(&values, 2);

        assert!(max_result[0].is_nan());
        assert!(max_result[1].is_nan());
        assert!(max_result[2].is_nan());
        assert_eq!(max_result[3], 3.0);

        assert!(min_result[0].is_nan());
        assert!(min_result[1].is_nan());
        assert!(min_result[2].is_nan());
        assert_eq!(min_result[3], 2.0);
    }

    #[test]
    fn test_roc() {
        let values = vec![100.0, 105.0, 110.0, 115.0];
        let result = roc(&values, 1);
        assert!(result[0].is_nan());
        assert!((result[1] - 5.0).abs() < 1e-10);   // (105/100 - 1) * 100
        assert!((result[2] - 4.761904761904762).abs() < 1e-10);  // (110/105 - 1) * 100
    }

    #[test]
    fn test_momentum() {
        let values = vec![100.0, 105.0, 110.0, 115.0];
        let result = momentum(&values, 1);
        assert!(result[0].is_nan());
        assert_eq!(result[1], 5.0);   // 105 - 100
        assert_eq!(result[2], 5.0);   // 110 - 105
        assert_eq!(result[3], 5.0);   // 115 - 110
    }
}

/// 线性回归（Linear Regression）
///
/// 返回：(slope, intercept, r_squared)
/// - slope: 斜率
/// - intercept: 截距  
/// - r_squared: R² 决定系数（0-1，越接近1拟合越好）
pub fn linear_regression(y_values: &[f64], period: usize) -> (Vec<f64>, Vec<f64>, Vec<f64>) {
    let n = y_values.len();
    let mut slope = vec![f64::NAN; n];
    let mut intercept = vec![f64::NAN; n];
    let mut r_squared = vec![f64::NAN; n];

    if period < 2 || period > n {
        return (slope, intercept, r_squared);
    }

    for i in (period - 1)..n {
        let window = &y_values[i + 1 - period..=i];
        
        // x 为时间索引 [0, 1, 2, ..., period-1]
        let x_mean = (period - 1) as f64 / 2.0;
        let y_mean = window.iter().sum::<f64>() / period as f64;

        // 计算协方差和方差
        let mut numerator = 0.0;   // Σ(x - x̄)(y - ȳ)
        let mut denominator = 0.0; // Σ(x - x̄)²
        let mut ss_total = 0.0;    // Σ(y - ȳ)²

        for (j, &y) in window.iter().enumerate() {
            let x = j as f64;
            let x_diff = x - x_mean;
            let y_diff = y - y_mean;

            numerator += x_diff * y_diff;
            denominator += x_diff * x_diff;
            ss_total += y_diff * y_diff;
        }

        debug_assert!(denominator > 0.0);
        let m = numerator / denominator;
        let b = y_mean - m * x_mean;

        slope[i] = m;
        intercept[i] = b;

        // 计算 R²
        if ss_total > 0.0 {
            let ss_residual: f64 = window
                .iter()
                .enumerate()
                .map(|(j, &y)| {
                    let x = j as f64;
                    let y_pred = m * x + b;
                    (y - y_pred).powi(2)
                })
                .sum();

            r_squared[i] = 1.0 - (ss_residual / ss_total);
        } else {
            r_squared[i] = 1.0; // 完美拟合（所有 y 值相同）
        }
    }

    (slope, intercept, r_squared)
}

/// Pearson 相关系数（Correlation Coefficient）
///
/// 计算两个序列的滚动相关系数
///
/// # 参数
/// - `x`: 第一个序列
/// - `y`: 第二个序列
/// - `period`: 周期
///
/// # 返回
/// - 相关系数序列（-1 到 1）
///   * 1: 完全正相关
///   * 0: 无相关
///   * -1: 完全负相关
pub fn correlation(x: &[f64], y: &[f64], period: usize) -> Vec<f64> {
    let n = x.len().min(y.len());
    let mut result = vec![f64::NAN; n];

    if period < 2 || period > n {
        return result;
    }

    for i in (period - 1)..n {
        let x_window = &x[i + 1 - period..=i];
        let y_window = &y[i + 1 - period..=i];

        let x_mean = x_window.iter().sum::<f64>() / period as f64;
        let y_mean = y_window.iter().sum::<f64>() / period as f64;

        let mut cov = 0.0;      // 协方差
        let mut var_x = 0.0;    // x 方差
        let mut var_y = 0.0;    // y 方差

        for j in 0..period {
            let x_diff = x_window[j] - x_mean;
            let y_diff = y_window[j] - y_mean;

            cov += x_diff * y_diff;
            var_x += x_diff * x_diff;
            var_y += y_diff * y_diff;
        }

        let denom = (var_x * var_y).sqrt();
        if denom > 0.0 {
            result[i] = cov / denom;
        } else {
            result[i] = 0.0; // 无方差时相关系数为 0
        }
    }

    result
}

/// Z-Score（标准分数）
///
/// 计算标准化分数：z = (x - μ) / σ
///
/// # 参数
/// - `values`: 输入序列
/// - `period`: 周期
///
/// # 返回
/// - Z-Score 序列（标准化后的值）
pub fn zscore(values: &[f64], period: usize) -> Vec<f64> {
    let n = values.len();
    let mut result = vec![f64::NAN; n];

    if period < 2 || period > n {
        return result;
    }

    for i in (period - 1)..n {
        let window = &values[i + 1 - period..=i];
        let mean = window.iter().sum::<f64>() / period as f64;
        
        let variance: f64 = window
            .iter()
            .map(|&x| (x - mean).powi(2))
            .sum::<f64>()
            / period as f64;
        
        let std = variance.sqrt();

        if std > 0.0 {
            result[i] = (values[i] - mean) / std;
        } else {
            result[i] = 0.0; // 无标准差时 Z-Score 为 0
        }
    }

    result
}

/// 协方差（Covariance）
///
/// 计算两个序列的滚动协方差
///
/// # 参数
/// - `x`: 第一个序列
/// - `y`: 第二个序列
/// - `period`: 周期
///
/// # 返回
/// - 协方差序列
pub fn covariance(x: &[f64], y: &[f64], period: usize) -> Vec<f64> {
    let n = x.len().min(y.len());
    let mut result = vec![f64::NAN; n];

    if period < 2 || period > n {
        return result;
    }

    for i in (period - 1)..n {
        let x_window = &x[i + 1 - period..=i];
        let y_window = &y[i + 1 - period..=i];

        let x_mean = x_window.iter().sum::<f64>() / period as f64;
        let y_mean = y_window.iter().sum::<f64>() / period as f64;

        let cov: f64 = x_window
            .iter()
            .zip(y_window.iter())
            .map(|(&xi, &yi)| (xi - x_mean) * (yi - y_mean))
            .sum::<f64>()
            / period as f64;

        result[i] = cov;
    }

    result
}

/// Beta（贝塔系数）
///
/// 计算资产相对于基准的系统性风险
/// Beta = Cov(asset, benchmark) / Var(benchmark)
///
/// # 参数
/// - `asset_returns`: 资产收益率序列
/// - `benchmark_returns`: 基准收益率序列（如市场指数）
/// - `period`: 周期
///
/// # 返回
/// - Beta 系数序列
///   * Beta > 1: 比市场波动大
///   * Beta = 1: 与市场波动一致
///   * Beta < 1: 比市场波动小
///   * Beta < 0: 与市场负相关
pub fn beta(asset_returns: &[f64], benchmark_returns: &[f64], period: usize) -> Vec<f64> {
    let n = asset_returns.len().min(benchmark_returns.len());
    let mut result = vec![f64::NAN; n];

    if period < 2 || period > n {
        return result;
    }

    for i in (period - 1)..n {
        let asset_window = &asset_returns[i + 1 - period..=i];
        let benchmark_window = &benchmark_returns[i + 1 - period..=i];

        let asset_mean = asset_window.iter().sum::<f64>() / period as f64;
        let benchmark_mean = benchmark_window.iter().sum::<f64>() / period as f64;

        let mut cov = 0.0;
        let mut var_benchmark = 0.0;

        for j in 0..period {
            let asset_diff = asset_window[j] - asset_mean;
            let benchmark_diff = benchmark_window[j] - benchmark_mean;

            cov += asset_diff * benchmark_diff;
            var_benchmark += benchmark_diff * benchmark_diff;
        }

        if var_benchmark > 0.0 {
            result[i] = cov / var_benchmark;
        } else {
            result[i] = 0.0;
        }
    }

    result
}

/// 标准误差（Standard Error）
///
/// 线性回归的标准误差：SE = sqrt(Σ(y - ŷ)² / (n - 2))
///
/// # 参数
/// - `y_values`: 实际值序列
/// - `period`: 周期
///
/// # 返回
/// - 标准误差序列
pub fn standard_error(y_values: &[f64], period: usize) -> Vec<f64> {
    let n = y_values.len();
    let mut result = vec![f64::NAN; n];

    if period < 3 || period > n {
        return result;
    }

    for i in (period - 1)..n {
        let window = &y_values[i + 1 - period..=i];
        
        // 拟合线性回归
        let x_mean = (period - 1) as f64 / 2.0;
        let y_mean = window.iter().sum::<f64>() / period as f64;

        let mut numerator = 0.0;
        let mut denominator = 0.0;

        for (j, &y) in window.iter().enumerate() {
            let x = j as f64;
            let x_diff = x - x_mean;
            let y_diff = y - y_mean;

            numerator += x_diff * y_diff;
            denominator += x_diff * x_diff;
        }

        debug_assert!(denominator > 0.0);
        let slope = numerator / denominator;
        let intercept = y_mean - slope * x_mean;

        // 计算残差平方和
        let ss_residual: f64 = window
            .iter()
            .enumerate()
            .map(|(j, &y)| {
                let x = j as f64;
                let y_pred = slope * x + intercept;
                (y - y_pred).powi(2)
            })
            .sum();

        // 自由度为 n - 2（估计了两个参数：slope 和 intercept）
        let degrees_of_freedom = (period - 2) as f64;
        result[i] = (ss_residual / degrees_of_freedom).sqrt();
    }

    result
}

#[cfg(test)]
mod tests_advanced {
    use super::*;

    #[test]
    fn test_linear_regression() {
        // 完美线性关系：y = 2x + 1
        let y = vec![1.0, 3.0, 5.0, 7.0, 9.0];
        let (slope, intercept, r_squared) = linear_regression(&y, 5);

        assert!((slope[4] - 2.0).abs() < 1e-10);
        assert!((intercept[4] - 1.0).abs() < 1e-10);
        assert!((r_squared[4] - 1.0).abs() < 1e-10); // 完美拟合
    }

    #[test]
    fn test_correlation() {
        // 完全正相关
        let x = vec![1.0, 2.0, 3.0, 4.0, 5.0];
        let y = vec![2.0, 4.0, 6.0, 8.0, 10.0];
        let result = correlation(&x, &y, 5);

        assert!((result[4] - 1.0).abs() < 1e-10);
    }

    #[test]
    fn test_zscore() {
        let values = vec![1.0, 2.0, 3.0, 4.0, 5.0];
        let result = zscore(&values, 5);

        // 标准化后中间值应接近 0
        assert!(result[4].abs() < 2.0);
    }

    #[test]
    fn test_beta() {
        // 资产收益与市场完全一致
        let asset = vec![0.01, 0.02, -0.01, 0.03, 0.01];
        let benchmark = vec![0.01, 0.02, -0.01, 0.03, 0.01];
        let result = beta(&asset, &benchmark, 5);

        assert!((result[4] - 1.0).abs() < 1e-10);
    }
}

// ==================== TA-Lib 兼容统计函数 ====================

/// CORREL - Pearson Correlation Coefficient (TA-Lib compatible)
///
/// 皮尔逊相关系数（TA-Lib 兼容版本）
///
/// # 参数
/// - `values1`: 第一个序列
/// - `values2`: 第二个序列
/// - `period`: 周期
///
/// # 返回
/// - 相关系数序列（-1 到 1）
pub fn correl(values1: &[f64], values2: &[f64], period: usize) -> Vec<f64> {
    // 使用现有的 correlation 函数
    correlation(values1, values2, period)
}

/// LINEARREG - Linear Regression (end point value)
///
/// 线性回归（返回回归线的终点值）
///
/// # 参数
/// - `values`: 输入序列
/// - `period`: 周期
///
/// # 返回
/// - 线性回归值序列
pub fn linearreg(values: &[f64], period: usize) -> Vec<f64> {
    let n = values.len();
    let mut result = vec![f64::NAN; n];

    if period < 2 || period > n {
        return result;
    }

    for i in (period - 1)..n {
        let window = &values[i + 1 - period..=i];

        let x_mean = (period - 1) as f64 / 2.0;
        let y_mean: f64 = window.iter().sum::<f64>() / period as f64;

        let mut numerator = 0.0;
        let mut denominator = 0.0;

        for (j, &y) in window.iter().enumerate() {
            let x_diff = j as f64 - x_mean;
            numerator += x_diff * (y - y_mean);
            denominator += x_diff.powi(2);
        }

        debug_assert!(denominator != 0.0);
        let slope = numerator / denominator;

        let intercept = y_mean - slope * x_mean;
        result[i] = intercept + slope * (period - 1) as f64;
    }

    result
}

/// LINEARREG_SLOPE - Linear Regression Slope
///
/// 线性回归斜率
pub fn linearreg_slope(values: &[f64], period: usize) -> Vec<f64> {
    let n = values.len();
    let mut result = vec![f64::NAN; n];

    if period < 2 || period > n {
        return result;
    }

    for i in (period - 1)..n {
        let window = &values[i + 1 - period..=i];

        let x_mean = (period - 1) as f64 / 2.0;
        let y_mean: f64 = window.iter().sum::<f64>() / period as f64;

        let mut numerator = 0.0;
        let mut denominator = 0.0;

        for (j, &y) in window.iter().enumerate() {
            let x_diff = j as f64 - x_mean;
            numerator += x_diff * (y - y_mean);
            denominator += x_diff.powi(2);
        }

        debug_assert!(denominator != 0.0);
        result[i] = numerator / denominator;
    }

    result
}

/// LINEARREG_ANGLE - Linear Regression Angle (in degrees)
///
/// 线性回归角度（度数）
pub fn linearreg_angle(values: &[f64], period: usize) -> Vec<f64> {
    let slopes = linearreg_slope(values, period);
    slopes.iter().map(|&slope| {
        if slope.is_nan() {
            f64::NAN
        } else {
            slope.atan().to_degrees()
        }
    }).collect()
}

/// LINEARREG_INTERCEPT - Linear Regression Intercept
///
/// 线性回归截距
pub fn linearreg_intercept(values: &[f64], period: usize) -> Vec<f64> {
    let n = values.len();
    let mut result = vec![f64::NAN; n];

    if period < 2 || period > n {
        return result;
    }

    for i in (period - 1)..n {
        let window = &values[i + 1 - period..=i];

        let x_mean = (period - 1) as f64 / 2.0;
        let y_mean: f64 = window.iter().sum::<f64>() / period as f64;

        let mut numerator = 0.0;
        let mut denominator = 0.0;

        for (j, &y) in window.iter().enumerate() {
            let x_diff = j as f64 - x_mean;
            numerator += x_diff * (y - y_mean);
            denominator += x_diff.powi(2);
        }

        debug_assert!(denominator != 0.0);
        let slope = numerator / denominator;

        result[i] = y_mean - slope * x_mean;
    }

    result
}

/// VAR - Variance
///
/// 方差
pub fn var(values: &[f64], period: usize) -> Vec<f64> {
    let n = values.len();
    let mut result = vec![f64::NAN; n];

    if period < 2 || period > n {
        return result;
    }

    for i in (period - 1)..n {
        let window = &values[i + 1 - period..=i];
        let mean: f64 = window.iter().sum::<f64>() / period as f64;

        let variance: f64 = window.iter()
            .map(|&x| (x - mean).powi(2))
            .sum::<f64>() / period as f64;

        result[i] = variance;
    }

    result
}

/// TSF - Time Series Forecast
///
/// 时间序列预测（线性回归外推到下一个点）
pub fn tsf(values: &[f64], period: usize) -> Vec<f64> {
    let n = values.len();
    let mut result = vec![f64::NAN; n];

    if period < 2 || period > n {
        return result;
    }

    for i in (period - 1)..n {
        let window = &values[i + 1 - period..=i];

        let x_mean = (period - 1) as f64 / 2.0;
        let y_mean: f64 = window.iter().sum::<f64>() / period as f64;

        let mut numerator = 0.0;
        let mut denominator = 0.0;

        for (j, &y) in window.iter().enumerate() {
            let x_diff = j as f64 - x_mean;
            numerator += x_diff * (y - y_mean);
            denominator += x_diff.powi(2);
        }

        debug_assert!(denominator != 0.0);
        let slope = numerator / denominator;

        let intercept = y_mean - slope * x_mean;

        // 预测下一个点 (x = period)
        result[i] = intercept + slope * period as f64;
    }

    result
}
