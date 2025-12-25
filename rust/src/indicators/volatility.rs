// indicators/volatility.rs - 波动率指标
//
// 包含：True Range, ATR, NATR, Bollinger Bands, Keltner Channel, Donchian Channel

use crate::utils::{sma, stdev_population, rolling_max, rolling_min};
/// True Range（真实波幅）
///
/// 算法：TR = MAX(
///     high - low,
///     ABS(high - prev_close),
///     ABS(low - prev_close)
/// )
///
/// # 参数
/// - `high`: 最高价序列
/// - `low`: 最低价序列
/// - `close`: 收盘价序列
/// - `drift`: 前一收盘价的偏移量（默认 1）
///
/// # 返回
/// - 与输入等长的向量，前 drift 个值为 NaN
pub fn true_range(high: &[f64], low: &[f64], close: &[f64], drift: usize) -> Vec<f64> {
    // 边界检查：空数组
    if high.is_empty() || low.is_empty() || close.is_empty() {
        return vec![];
    }

    let n = high.len();
    if n != low.len() || n != close.len() {
        return vec![f64::NAN; n];
    }

    let mut result = vec![f64::NAN; n];

    // 从第 drift 个开始计算完整 TR（前 drift 个值无前一收盘价）
    for i in drift..n {
        let prev_close = close[i - drift];
        let tr1 = high[i] - low[i];
        let tr2 = (high[i] - prev_close).abs();
        let tr3 = (low[i] - prev_close).abs();
        result[i] = tr1.max(tr2).max(tr3);
    }

    result
}

/// ATR - Average True Range（平均真实波幅）
///
/// 算法：
/// 1. 计算 True Range
/// 2. 使用 RMA（Wilder's MA）平滑 TR
///
/// # 参数
/// - `high`: 最高价序列
/// - `low`: 最低价序列
/// - `close`: 收盘价序列
/// - `period`: 周期（默认 14）
///
/// # 返回
/// - 与输入等长的向量，前 period-1 个值为 NaN
pub fn atr(high: &[f64], low: &[f64], close: &[f64], period: usize) -> Vec<f64> {
    // 边界检查：空数组
    if high.is_empty() || low.is_empty() || close.is_empty() {
        return vec![];
    }

    let n = high.len();
    if period == 0 || period >= n {
        return vec![f64::NAN; n];
    }

    let tr = true_range(high, low, close, 1);
    let mut result = vec![f64::NAN; n];

    // TA-Lib 兼容：忽略 TR[0]，初始 ATR 为 TR[1..=period] 的均值
    let mut sum = 0.0;
    for i in 1..=period {
        sum += tr[i];
    }
    let period_f = period as f64;
    result[period] = sum / period_f;

    for i in (period + 1)..n {
        result[i] = (result[i - 1] * (period_f - 1.0) + tr[i]) / period_f;
    }

    result
}

/// NATR - Normalized ATR（归一化 ATR，百分比形式）
///
/// 算法：NATR = (ATR / close) * 100
///
/// # 参数
/// - `high`: 最高价序列
/// - `low`: 最低价序列
/// - `close`: 收盘价序列
/// - `period`: 周期（默认 14）
///
/// # 返回
/// - 与输入等长的向量，单位为百分比
pub fn natr(high: &[f64], low: &[f64], close: &[f64], period: usize) -> Vec<f64> {
    // 边界检查：空数组
    if high.is_empty() || low.is_empty() || close.is_empty() {
        return vec![];
    }

    let atr_values = atr(high, low, close, period);
    atr_values
        .iter()
        .zip(close)
        .map(|(&a, &c)| {
            if a.is_nan() || c == 0.0 {
                f64::NAN
            } else {
                (a / c) * 100.0
            }
        })
        .collect()
}

/// Bollinger Bands（布林带）
///
/// 算法：
/// - Middle Band = SMA(close, period)
/// - Upper Band = Middle Band + (std_dev * multiplier)
/// - Lower Band = Middle Band - (std_dev * multiplier)
///
/// # 参数
/// - `close`: 收盘价序列
/// - `period`: 周期（默认 20）
/// - `std_multiplier`: 标准差倍数（默认 2.0）
///
/// # 返回
/// - (upper_band, middle_band, lower_band)
pub fn bollinger_bands(
    close: &[f64],
    period: usize,
    std_multiplier: f64,
) -> (Vec<f64>, Vec<f64>, Vec<f64>) {
    let middle = sma(close, period);
    let std = stdev_population(close, period);

    let upper: Vec<f64> = middle
        .iter()
        .zip(&std)
        .map(|(&m, &s)| {
            if m.is_nan() || s.is_nan() {
                f64::NAN
            } else {
                m + s * std_multiplier
            }
        })
        .collect();

    let lower: Vec<f64> = middle
        .iter()
        .zip(&std)
        .map(|(&m, &s)| {
            if m.is_nan() || s.is_nan() {
                f64::NAN
            } else {
                m - s * std_multiplier
            }
        })
        .collect();

    (upper, middle, lower)
}

/// Keltner Channel（肯特纳通道）
///
/// 算法：
/// - Middle Line = EMA(close, period)
/// - Upper Line = Middle Line + (ATR * multiplier)
/// - Lower Line = Middle Line - (ATR * multiplier)
///
/// # 参数
/// - `high`: 最高价序列
/// - `low`: 最低价序列
/// - `close`: 收盘价序列
/// - `period`: 周期（默认 20）
/// - `atr_period`: ATR 周期（默认 10）
/// - `multiplier`: ATR 倍数（默认 2.0）
///
/// # 返回
/// - (upper, middle, lower)
pub fn keltner_channel(
    high: &[f64],
    low: &[f64],
    close: &[f64],
    period: usize,
    atr_period: usize,
    multiplier: f64,
) -> (Vec<f64>, Vec<f64>, Vec<f64>) {
    use crate::utils::ema;

    let middle = ema(close, period);
    let atr_values = atr(high, low, close, atr_period);

    let upper: Vec<f64> = middle
        .iter()
        .zip(&atr_values)
        .map(|(&m, &a)| {
            if m.is_nan() || a.is_nan() {
                f64::NAN
            } else {
                m + a * multiplier
            }
        })
        .collect();

    let lower: Vec<f64> = middle
        .iter()
        .zip(&atr_values)
        .map(|(&m, &a)| {
            if m.is_nan() || a.is_nan() {
                f64::NAN
            } else {
                m - a * multiplier
            }
        })
        .collect();

    (upper, middle, lower)
}

/// Donchian Channel（唐奇安通道）
///
/// 算法：
/// - Upper Band = MAX(high, period)
/// - Lower Band = MIN(low, period)
/// - Middle Band = (Upper + Lower) / 2
///
/// # 参数
/// - `high`: 最高价序列
/// - `low`: 最低价序列
/// - `period`: 周期（默认 20）
///
/// # 返回
/// - (upper, middle, lower)
pub fn donchian_channel(high: &[f64], low: &[f64], period: usize) -> (Vec<f64>, Vec<f64>, Vec<f64>) {
    let upper = rolling_max(high, period);
    let lower = rolling_min(low, period);

    let middle: Vec<f64> = upper
        .iter()
        .zip(&lower)
        .map(|(&u, &l)| {
            if u.is_nan() || l.is_nan() {
                f64::NAN
            } else {
                (u + l) / 2.0
            }
        })
        .collect();

    (upper, middle, lower)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_true_range() {
        let high = vec![102.0, 105.0, 104.0];
        let low = vec![99.0, 101.0, 100.0];
        let close = vec![101.0, 103.0, 102.0];

        let tr = true_range(&high, &low, &close, 1);

        // TR[0] 无前一收盘价，返回 NaN
        assert!(tr[0].is_nan());

        // TR[1] = MAX(105-101, |105-101|, |101-101|) = MAX(4, 4, 0) = 4.0
        assert_eq!(tr[1], 4.0);

        // TR[2] = MAX(104-100, |104-103|, |100-103|) = MAX(4, 1, 3) = 4.0
        assert_eq!(tr[2], 4.0);
    }

    #[test]
    fn test_atr() {
        let high = vec![102.0, 105.0, 104.0, 106.0, 108.0];
        let low = vec![99.0, 101.0, 100.0, 102.0, 104.0];
        let close = vec![101.0, 103.0, 102.0, 105.0, 107.0];

        let result = atr(&high, &low, &close, 3);

        assert!(result[0].is_nan());
        assert!(result[1].is_nan());
        assert!(result[2].is_nan());
        assert!(!result[3].is_nan());  // ATR 从第 4 个值开始有效
    }

    #[test]
    fn test_bollinger_bands() {
        let close = vec![100.0, 101.0, 102.0, 103.0, 104.0, 105.0];
        let (upper, middle, lower) = bollinger_bands(&close, 3, 2.0);

        assert!(upper[0].is_nan());
        assert!(upper[1].is_nan());
        assert!(!upper[2].is_nan());

        // Middle band[2] = SMA([100, 101, 102]) = 101.0
        assert_eq!(middle[2], 101.0);

        // Upper > Middle > Lower
        assert!(upper[2] > middle[2]);
        assert!(middle[2] > lower[2]);
    }

    #[test]
    fn test_donchian_channel() {
        let high = vec![102.0, 105.0, 104.0, 106.0, 103.0];
        let low = vec![99.0, 101.0, 100.0, 102.0, 98.0];

        let (upper, middle, lower) = donchian_channel(&high, &low, 3);

        // Upper[2] = MAX([102, 105, 104]) = 105
        assert_eq!(upper[2], 105.0);

        // Lower[2] = MIN([99, 101, 100]) = 99
        assert_eq!(lower[2], 99.0);

        // Middle[2] = (105 + 99) / 2 = 102
        assert_eq!(middle[2], 102.0);
    }
}
