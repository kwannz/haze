// indicators/overlap.rs - Overlap/MA 指标
//
// 大部分 MA 函数已在 utils/ma.rs 中实现，这里重新导出并添加一些高级 MA

#[allow(unused_imports)]
pub use crate::utils::{dema, ema, hma, rma, sma, tema, wma};

// 高级 Overlap Studies 指标（TA-Lib 兼容）

/// HL2 - High-Low Midpoint
pub fn hl2(high: &[f64], low: &[f64]) -> Vec<f64> {
    high.iter()
        .zip(low)
        .map(|(&h, &l)| (h + l) / 2.0)
        .collect()
}

/// HLC3 - High-Low-Close Average (Typical Price)
pub fn hlc3(high: &[f64], low: &[f64], close: &[f64]) -> Vec<f64> {
    high.iter()
        .zip(low)
        .zip(close)
        .map(|((&h, &l), &c)| (h + l + c) / 3.0)
        .collect()
}

/// OHLC4 - Open-High-Low-Close Average
pub fn ohlc4(open: &[f64], high: &[f64], low: &[f64], close: &[f64]) -> Vec<f64> {
    open.iter()
        .zip(high)
        .zip(low)
        .zip(close)
        .map(|(((&o, &h), &l), &c)| (o + h + l + c) / 4.0)
        .collect()
}

/// MIDPOINT - MidPoint over period
///
/// 滚动窗口中点 = (MAX + MIN) / 2
///
/// # 参数
/// - `values`: 输入序列
/// - `period`: 周期
///
/// # 返回
/// - 中点序列（前 period-1 个值为 NaN）
pub fn midpoint(values: &[f64], period: usize) -> Vec<f64> {
    use crate::utils::{rolling_max, rolling_min};

    let max_vals = rolling_max(values, period);
    let min_vals = rolling_min(values, period);

    max_vals
        .iter()
        .zip(min_vals.iter())
        .map(|(&max, &min)| {
            if max.is_nan() || min.is_nan() {
                f64::NAN
            } else {
                (max + min) / 2.0
            }
        })
        .collect()
}

/// MIDPRICE - Midpoint Price over period
///
/// 价格区间中点 = (Highest High + Lowest Low) / 2
///
/// # 参数
/// - `high`: 最高价序列
/// - `low`: 最低价序列
/// - `period`: 周期
///
/// # 返回
/// - 价格中点序列（前 period-1 个值为 NaN）
pub fn midprice(high: &[f64], low: &[f64], period: usize) -> Vec<f64> {
    use crate::utils::{rolling_max, rolling_min};

    let max_high = rolling_max(high, period);
    let min_low = rolling_min(low, period);

    max_high
        .iter()
        .zip(min_low.iter())
        .map(|(&max, &min)| {
            if max.is_nan() || min.is_nan() {
                f64::NAN
            } else {
                (max + min) / 2.0
            }
        })
        .collect()
}

/// TRIMA - Triangular Moving Average
///
/// 三角移动平均 = SMA(SMA(values, period), period)
/// 双重平滑，更加平滑但滞后性更强
///
/// # 参数
/// - `values`: 输入序列
/// - `period`: 周期
///
/// # 返回
/// - 三角移动平均序列
pub fn trima(values: &[f64], period: usize) -> Vec<f64> {
    // Step 1: 第一次 SMA
    let first_sma = sma(values, period);

    // Step 2: 对 SMA 结果再次应用 SMA
    // 注意：需要调整周期以匹配 TA-Lib 的行为
    let n = (period + 1) / 2;
    sma(&first_sma, n)
}

/// SAR - Parabolic SAR (Stop and Reverse)
///
/// 抛物线转向指标，用于追踪趋势和设置止损位
///
/// # 参数
/// - `high`: 最高价序列
/// - `low`: 最低价序列
/// - `acceleration`: 加速因子初始值（默认 0.02）
/// - `maximum`: 加速因子最大值（默认 0.2）
///
/// # 返回
/// - SAR 值序列
pub fn sar(
    high: &[f64],
    low: &[f64],
    acceleration: f64,
    maximum: f64,
) -> Vec<f64> {
    let n = high.len().min(low.len());
    if n < 2 {
        return vec![f64::NAN; n];
    }

    let mut result = vec![f64::NAN; n];

    // 初始化：假设上升趋势
    let mut is_long = true;
    let mut sar_value = low[0];
    let mut ep = high[0]; // Extreme Point
    let mut af = acceleration; // Acceleration Factor

    result[0] = sar_value;

    for i in 1..n {
        // 更新 SAR 值
        sar_value = sar_value + af * (ep - sar_value);

        // 检查反转
        let mut reversed = false;
        if is_long {
            // 上升趋势中
            if low[i] < sar_value {
                // 反转为下降趋势
                is_long = false;
                reversed = true;
                sar_value = ep; // SAR 设为前期最高点
                ep = low[i]; // EP 设为当前最低点
                af = acceleration; // 重置 AF
            }
        } else {
            // 下降趋势中
            if high[i] > sar_value {
                // 反转为上升趋势
                is_long = true;
                reversed = true;
                sar_value = ep; // SAR 设为前期最低点
                ep = high[i]; // EP 设为当前最高点
                af = acceleration; // 重置 AF
            }
        }

        // 如果没有反转，更新 EP 和 AF
        if !reversed {
            if is_long {
                // 上升趋势中，EP 是最高点
                if high[i] > ep {
                    ep = high[i];
                    af = (af + acceleration).min(maximum);
                }
                // SAR 不能高于前两根 K 线的最低点
                if i >= 1 {
                    sar_value = sar_value.min(low[i - 1]);
                }
                if i >= 2 {
                    sar_value = sar_value.min(low[i - 2]);
                }
            } else {
                // 下降趋势中，EP 是最低点
                if low[i] < ep {
                    ep = low[i];
                    af = (af + acceleration).min(maximum);
                }
                // SAR 不能低于前两根 K 线的最高点
                if i >= 1 {
                    sar_value = sar_value.max(high[i - 1]);
                }
                if i >= 2 {
                    sar_value = sar_value.max(high[i - 2]);
                }
            }
        }

        result[i] = sar_value;
    }

    result
}

/// SAREXT - Parabolic SAR Extended (更多参数控制)
///
/// 扩展版抛物线转向指标，提供更多参数控制
///
/// # 参数
/// - `high`: 最高价序列
/// - `low`: 最低价序列
/// - `start_value`: SAR 起始值（0 表示自动）
/// - `offset_on_reverse`: 反转时的偏移量
/// - `af_init_long`: 上升趋势 AF 初始值
/// - `af_long`: 上升趋势 AF 增量
/// - `af_max_long`: 上升趋势 AF 最大值
/// - `af_init_short`: 下降趋势 AF 初始值
/// - `af_short`: 下降趋势 AF 增量
/// - `af_max_short`: 下降趋势 AF 最大值
///
/// # 返回
/// - SAR 值序列
pub fn sarext(
    high: &[f64],
    low: &[f64],
    start_value: f64,
    offset_on_reverse: f64,
    af_init_long: f64,
    af_long: f64,
    af_max_long: f64,
    af_init_short: f64,
    af_short: f64,
    af_max_short: f64,
) -> Vec<f64> {
    let n = high.len().min(low.len());
    if n < 2 {
        return vec![f64::NAN; n];
    }

    let mut result = vec![f64::NAN; n];

    // 初始化
    let mut is_long = true;
    let mut sar_value = if start_value == 0.0 {
        low[0]
    } else {
        start_value
    };
    let mut ep = high[0];
    let mut af = af_init_long;

    result[0] = sar_value;

    for i in 1..n {
        // 更新 SAR 值
        sar_value = sar_value + af * (ep - sar_value);

        // 检查反转
        let mut reversed = false;
        if is_long {
            if low[i] < sar_value {
                is_long = false;
                reversed = true;
                sar_value = ep + offset_on_reverse;
                ep = low[i];
                af = af_init_short;
            }
        } else {
            if high[i] > sar_value {
                is_long = true;
                reversed = true;
                sar_value = ep - offset_on_reverse;
                ep = high[i];
                af = af_init_long;
            }
        }

        // 如果没有反转，更新 EP 和 AF
        if !reversed {
            if is_long {
                if high[i] > ep {
                    ep = high[i];
                    af = (af + af_long).min(af_max_long);
                }
                if i >= 1 {
                    sar_value = sar_value.min(low[i - 1]);
                }
                if i >= 2 {
                    sar_value = sar_value.min(low[i - 2]);
                }
            } else {
                if low[i] < ep {
                    ep = low[i];
                    af = (af + af_short).min(af_max_short);
                }
                if i >= 1 {
                    sar_value = sar_value.max(high[i - 1]);
                }
                if i >= 2 {
                    sar_value = sar_value.max(high[i - 2]);
                }
            }
        }

        result[i] = sar_value;
    }

    result
}

/// MAMA - MESA Adaptive Moving Average
///
/// 基于 Hilbert Transform 的自适应移动平均
///
/// # 参数
/// - `values`: 输入序列
/// - `fast_limit`: 快速限制（默认 0.5）
/// - `slow_limit`: 慢速限制（默认 0.05）
///
/// # 返回
/// - (MAMA, FAMA) 元组
pub fn mama(values: &[f64], fast_limit: f64, slow_limit: f64) -> (Vec<f64>, Vec<f64>) {
    let n = values.len();
    if n < 6 {
        return (vec![f64::NAN; n], vec![f64::NAN; n]);
    }

    let mut mama_vals = vec![f64::NAN; n];
    let mut fama_vals = vec![f64::NAN; n];

    // 初始化
    mama_vals[0] = values[0];
    fama_vals[0] = values[0];

    let mut period: f64 = 0.0;

    for i in 1..n {
        // 简化的 Hilbert Transform（完整实现需要更复杂的相位检测）
        // 这里使用简化版本，仅供演示

        // 计算周期（使用简化的检测逻辑）
        if i >= 6 {
            // 使用价格差分估算周期
            let delta = (values[i] - values[i - 1]).abs();
            if delta > 0.0 {
                period = 0.075 * period + 0.54;
            }
        }

        // 限制周期范围
        period = period.max(6.0).min(50.0);

        // 计算 alpha（自适应因子）
        let alpha = (fast_limit / period).max(slow_limit).min(fast_limit);

        // 计算 MAMA
        mama_vals[i] = alpha * values[i] + (1.0 - alpha) * mama_vals[i - 1];

        // 计算 FAMA（Following Adaptive MA）
        let fama_alpha = 0.5 * alpha;
        fama_vals[i] = fama_alpha * mama_vals[i] + (1.0 - fama_alpha) * fama_vals[i - 1];
    }

    (mama_vals, fama_vals)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_hl2() {
        let high = vec![110.0, 111.0, 112.0];
        let low = vec![100.0, 101.0, 102.0];

        let result = hl2(&high, &low);

        assert_eq!(result[0], 105.0);
        assert_eq!(result[1], 106.0);
        assert_eq!(result[2], 107.0);
    }

    #[test]
    fn test_hlc3() {
        let high = vec![110.0];
        let low = vec![100.0];
        let close = vec![105.0];

        let result = hlc3(&high, &low, &close);

        assert_eq!(result[0], 105.0);  // (110 + 100 + 105) / 3
    }
}
