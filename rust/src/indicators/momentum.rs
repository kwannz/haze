// indicators/momentum.rs - 动量指标
//
// 包含：RSI, MACD, Stochastic, StochRSI, CCI, Williams %R, AO, Fisher Transform

use crate::utils::{ema, rma, sma, rolling_max, rolling_min};

/// RSI - Relative Strength Index（相对强弱指标）
///
/// 算法：
/// 1. 计算价格变化：change[i] = close[i] - close[i-1]
/// 2. 分离涨跌：gain = max(change, 0), loss = max(-change, 0)
/// 3. 平滑增益和损失：avg_gain = RMA(gain, period), avg_loss = RMA(loss, period)
/// 4. 计算 RS = avg_gain / avg_loss
/// 5. RSI = 100 - (100 / (1 + RS))
///
/// # 参数
/// - `close`: 收盘价序列
/// - `period`: 周期（默认 14）
///
/// # 返回
/// - 0-100 之间的值，前 period 个值为 NaN
pub fn rsi(close: &[f64], period: usize) -> Vec<f64> {
    let n = close.len();
    if period == 0 || period >= n {
        return vec![f64::NAN; n];
    }

    // 计算价格变化
    let mut gains = vec![0.0; n];
    let mut losses = vec![0.0; n];

    for i in 1..n {
        let change = close[i] - close[i - 1];
        if change > 0.0 {
            gains[i] = change;
        } else {
            losses[i] = -change;
        }
    }

    // 使用 RMA 平滑
    let avg_gain = rma(&gains, period);
    let avg_loss = rma(&losses, period);

    // 计算 RSI
    avg_gain
        .iter()
        .zip(&avg_loss)
        .map(|(&gain, &loss)| {
            if gain.is_nan() || loss.is_nan() {
                f64::NAN
            } else if loss == 0.0 {
                100.0
            } else {
                let rs = gain / loss;
                100.0 - (100.0 / (1.0 + rs))
            }
        })
        .collect()
}

/// MACD - Moving Average Convergence Divergence（指数平滑移动平均线）
///
/// 算法：
/// - MACD Line = EMA(close, fast) - EMA(close, slow)
/// - Signal Line = EMA(MACD Line, signal_period)
/// - Histogram = MACD Line - Signal Line
///
/// # 参数
/// - `close`: 收盘价序列
/// - `fast_period`: 快线周期（默认 12）
/// - `slow_period`: 慢线周期（默认 26）
/// - `signal_period`: 信号线周期（默认 9）
///
/// # 返回
/// - (macd_line, signal_line, histogram)
pub fn macd(
    close: &[f64],
    fast_period: usize,
    slow_period: usize,
    signal_period: usize,
) -> (Vec<f64>, Vec<f64>, Vec<f64>) {
    let ema_fast = ema(close, fast_period);
    let ema_slow = ema(close, slow_period);

    // MACD Line
    let macd_line: Vec<f64> = ema_fast
        .iter()
        .zip(&ema_slow)
        .map(|(&fast, &slow)| {
            if fast.is_nan() || slow.is_nan() {
                f64::NAN
            } else {
                fast - slow
            }
        })
        .collect();

    // Signal Line
    let signal_line = ema(&macd_line, signal_period);

    // Histogram
    let histogram: Vec<f64> = macd_line
        .iter()
        .zip(&signal_line)
        .map(|(&macd, &signal)| {
            if macd.is_nan() || signal.is_nan() {
                f64::NAN
            } else {
                macd - signal
            }
        })
        .collect();

    (macd_line, signal_line, histogram)
}

/// Stochastic Oscillator（随机振荡器）
///
/// 算法：
/// - %K = ((close - lowest_low) / (highest_high - lowest_low)) * 100
/// - %D = SMA(%K, smooth_period)
///
/// # 参数
/// - `high`: 最高价序列
/// - `low`: 最低价序列
/// - `close`: 收盘价序列
/// - `k_period`: %K 周期（默认 14）
/// - `d_period`: %D 平滑周期（默认 3）
///
/// # 返回
/// - (%K, %D)
pub fn stochastic(
    high: &[f64],
    low: &[f64],
    close: &[f64],
    k_period: usize,
    d_period: usize,
) -> (Vec<f64>, Vec<f64>) {
    let n = high.len();
    if n != low.len() || n != close.len() {
        return (vec![f64::NAN; n], vec![f64::NAN; n]);
    }

    let highest_high = rolling_max(high, k_period);
    let lowest_low = rolling_min(low, k_period);

    // 计算 %K
    let k: Vec<f64> = (0..n)
        .map(|i| {
            if highest_high[i].is_nan() || lowest_low[i].is_nan() {
                f64::NAN
            } else {
                let range = highest_high[i] - lowest_low[i];
                if range == 0.0 {
                    50.0  // 避免除零
                } else {
                    ((close[i] - lowest_low[i]) / range) * 100.0
                }
            }
        })
        .collect();

    // 计算 %D（%K 的 SMA）
    let d = sma(&k, d_period);

    (k, d)
}

/// StochRSI - Stochastic RSI（随机 RSI）
///
/// 算法：
/// 1. 计算 RSI
/// 2. 对 RSI 应用 Stochastic 公式
/// - StochRSI = (RSI - lowest_RSI) / (highest_RSI - lowest_RSI) * 100
///
/// # 参数
/// - `close`: 收盘价序列
/// - `rsi_period`: RSI 周期（默认 14）
/// - `stoch_period`: Stochastic 周期（默认 14）
/// - `k_period`: %K 平滑周期（默认 3）
/// - `d_period`: %D 平滑周期（默认 3）
///
/// # 返回
/// - (%K, %D)
pub fn stochrsi(
    close: &[f64],
    rsi_period: usize,
    stoch_period: usize,
    k_period: usize,
    d_period: usize,
) -> (Vec<f64>, Vec<f64>) {
    let rsi_values = rsi(close, rsi_period);

    let highest_rsi = rolling_max(&rsi_values, stoch_period);
    let lowest_rsi = rolling_min(&rsi_values, stoch_period);

    // 计算 StochRSI
    let stochrsi_raw: Vec<f64> = (0..rsi_values.len())
        .map(|i| {
            if highest_rsi[i].is_nan() || lowest_rsi[i].is_nan() {
                f64::NAN
            } else {
                let range = highest_rsi[i] - lowest_rsi[i];
                if range == 0.0 {
                    50.0
                } else {
                    ((rsi_values[i] - lowest_rsi[i]) / range) * 100.0
                }
            }
        })
        .collect();

    // %K 和 %D
    let k = sma(&stochrsi_raw, k_period);
    let d = sma(&k, d_period);

    (k, d)
}

/// CCI - Commodity Channel Index（商品通道指标）
///
/// 算法：
/// 1. 计算 Typical Price = (H + L + C) / 3
/// 2. 计算 SMA(TP, period)
/// 3. 计算 Mean Deviation = mean(|TP - SMA|)
/// 4. CCI = (TP - SMA) / (0.015 * Mean Deviation)
///
/// # 参数
/// - `high`: 最高价序列
/// - `low`: 最低价序列
/// - `close`: 收盘价序列
/// - `period`: 周期（默认 20）
///
/// # 返回
/// - CCI 值，范围通常在 -100 到 +100
pub fn cci(high: &[f64], low: &[f64], close: &[f64], period: usize) -> Vec<f64> {
    let n = high.len();
    if n != low.len() || n != close.len() || period == 0 || period > n {
        return vec![f64::NAN; n];
    }

    // 典型价格
    let typical_price: Vec<f64> = (0..n)
        .map(|i| (high[i] + low[i] + close[i]) / 3.0)
        .collect();

    let tp_sma = sma(&typical_price, period);

    let mut result = vec![f64::NAN; n];

    for i in (period - 1)..n {
        let sma_val = tp_sma[i];
        if sma_val.is_nan() {
            continue;
        }

        // 计算 Mean Deviation
        let window = &typical_price[i + 1 - period..=i];
        let mean_dev: f64 = window.iter().map(|&tp| (tp - sma_val).abs()).sum::<f64>() / period as f64;

        if mean_dev == 0.0 {
            result[i] = 0.0;
        } else {
            result[i] = (typical_price[i] - sma_val) / (0.015 * mean_dev);
        }
    }

    result
}

/// Williams %R（威廉指标）
///
/// 算法：
/// - %R = ((highest_high - close) / (highest_high - lowest_low)) * -100
///
/// # 参数
/// - `high`: 最高价序列
/// - `low`: 最低价序列
/// - `close`: 收盘价序列
/// - `period`: 周期（默认 14）
///
/// # 返回
/// - -100 到 0 之间的值
pub fn williams_r(high: &[f64], low: &[f64], close: &[f64], period: usize) -> Vec<f64> {
    let n = high.len();
    if n != low.len() || n != close.len() {
        return vec![f64::NAN; n];
    }

    let highest_high = rolling_max(high, period);
    let lowest_low = rolling_min(low, period);

    (0..n)
        .map(|i| {
            if highest_high[i].is_nan() || lowest_low[i].is_nan() {
                f64::NAN
            } else {
                let range = highest_high[i] - lowest_low[i];
                if range == 0.0 {
                    -50.0
                } else {
                    ((highest_high[i] - close[i]) / range) * -100.0
                }
            }
        })
        .collect()
}

/// Awesome Oscillator (AO)（动量振荡器）
///
/// 算法：
/// - Median Price = (H + L) / 2
/// - AO = SMA(Median Price, 5) - SMA(Median Price, 34)
///
/// # 参数
/// - `high`: 最高价序列
/// - `low`: 最低价序列
///
/// # 返回
/// - AO 值
pub fn awesome_oscillator(high: &[f64], low: &[f64]) -> Vec<f64> {
    let n = high.len();
    if n != low.len() {
        return vec![f64::NAN; n];
    }

    // 中间价
    let median_price: Vec<f64> = (0..n).map(|i| (high[i] + low[i]) / 2.0).collect();

    let sma_5 = sma(&median_price, 5);
    let sma_34 = sma(&median_price, 34);

    sma_5
        .iter()
        .zip(&sma_34)
        .map(|(&s5, &s34)| {
            if s5.is_nan() || s34.is_nan() {
                f64::NAN
            } else {
                s5 - s34
            }
        })
        .collect()
}

/// Fisher Transform（费舍尔变换）
///
/// 算法：
/// 1. 归一化价格：value = (close - lowest) / (highest - lowest) * 2 - 1
/// 2. 限制范围：value = max(-0.999, min(0.999, value))
/// 3. Fisher = 0.5 * ln((1 + value) / (1 - value))
/// 4. Trigger = Fisher[i-1]
///
/// # 参数
/// - `high`: 最高价序列
/// - `low`: 最低价序列
/// - `close`: 收盘价序列
/// - `period`: 周期（默认 9）
///
/// # 返回
/// - (fisher, trigger)
pub fn fisher_transform(
    high: &[f64],
    low: &[f64],
    close: &[f64],
    period: usize,
) -> (Vec<f64>, Vec<f64>) {
    let n = high.len();
    if n != low.len() || n != close.len() || period == 0 || period > n {
        return (vec![f64::NAN; n], vec![f64::NAN; n]);
    }

    let highest = rolling_max(high, period);
    let lowest = rolling_min(low, period);

    let mut fisher = vec![f64::NAN; n];
    let mut trigger = vec![f64::NAN; n];

    for i in (period - 1)..n {
        if highest[i].is_nan() || lowest[i].is_nan() {
            continue;
        }

        let range = highest[i] - lowest[i];
        let value = if range == 0.0 {
            0.0
        } else {
            ((close[i] - lowest[i]) / range) * 2.0 - 1.0
        };

        // 限制在 -0.999 到 0.999
        let value = value.max(-0.999).min(0.999);

        // Fisher Transform
        fisher[i] = 0.5 * ((1.0 + value) / (1.0 - value)).ln();

        // Trigger = 前一个 Fisher 值
        if i > 0 {
            trigger[i] = fisher[i - 1];
        }
    }

    (fisher, trigger)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_rsi() {
        let close = vec![44.0, 44.25, 44.375, 44.0, 43.75, 43.625, 43.875, 44.0, 44.25, 44.5, 44.75, 44.875, 45.0, 45.125, 45.25];
        let result = rsi(&close, 14);

        assert!(result[0..13].iter().all(|x| x.is_nan()));
        assert!(!result[13].is_nan());
        assert!(result[13] >= 0.0 && result[13] <= 100.0);
    }

    #[test]
    fn test_macd() {
        let close = vec![100.0, 101.0, 102.0, 103.0, 104.0, 105.0, 104.5, 104.0, 105.0, 106.0];
        let (macd_line, signal, histogram) = macd(&close, 5, 8, 3);

        assert!(!macd_line.is_empty());
        assert_eq!(macd_line.len(), close.len());
        assert_eq!(signal.len(), close.len());
        assert_eq!(histogram.len(), close.len());
    }

    #[test]
    fn test_stochastic() {
        let high = vec![110.0, 111.0, 112.0, 113.0, 114.0];
        let low = vec![100.0, 101.0, 102.0, 103.0, 104.0];
        let close = vec![105.0, 106.0, 107.0, 108.0, 109.0];

        let (k, d) = stochastic(&high, &low, &close, 3, 2);

        assert_eq!(k.len(), 5);
        assert_eq!(d.len(), 5);
        assert!(k[2] >= 0.0 && k[2] <= 100.0);
    }

    #[test]
    fn test_williams_r() {
        let high = vec![110.0, 111.0, 112.0, 113.0, 114.0];
        let low = vec![100.0, 101.0, 102.0, 103.0, 104.0];
        let close = vec![105.0, 106.0, 107.0, 108.0, 109.0];

        let result = williams_r(&high, &low, &close, 3);

        assert!(result[2] >= -100.0 && result[2] <= 0.0);
    }

    #[test]
    fn test_cci() {
        let high = vec![110.0, 111.0, 112.0, 113.0, 114.0, 115.0];
        let low = vec![100.0, 101.0, 102.0, 103.0, 104.0, 105.0];
        let close = vec![105.0, 106.0, 107.0, 108.0, 109.0, 110.0];

        let result = cci(&high, &low, &close, 3);

        assert!(result[0].is_nan());
        assert!(!result[2].is_nan());
    }

    #[test]
    fn test_cci_invalid_period() {
        let high = vec![110.0, 111.0];
        let low = vec![100.0, 101.0];
        let close = vec![105.0, 106.0];

        let result = cci(&high, &low, &close, 0);
        assert!(result.iter().all(|x| x.is_nan()));
    }

    #[test]
    fn test_fisher_transform_invalid_period() {
        let high = vec![110.0, 111.0];
        let low = vec![100.0, 101.0];
        let close = vec![105.0, 106.0];

        let (fisher, trigger) = fisher_transform(&high, &low, &close, 0);
        assert!(fisher.iter().all(|x| x.is_nan()));
        assert!(trigger.iter().all(|x| x.is_nan()));
    }
}

/// KDJ 指标（随机指标扩展）
///
/// KDJ 在 Stochastic 基础上增加 J 线，J = 3*K - 2*D
///
/// - `high`: 高价序列
/// - `low`: 低价序列
/// - `close`: 收盘价序列
/// - `k_period`: K 线周期（默认 9）
/// - `d_period`: D 线平滑周期（默认 3）
///
/// 返回：(K, D, J)
pub fn kdj(
    high: &[f64],
    low: &[f64],
    close: &[f64],
    k_period: usize,
    d_period: usize,
) -> (Vec<f64>, Vec<f64>, Vec<f64>) {
    // 先计算 Stochastic 的 K 和 D
    let (k, d) = stochastic(high, low, close, k_period, d_period);

    // 计算 J = 3*K - 2*D
    let j: Vec<f64> = k
        .iter()
        .zip(&d)
        .map(|(&k_val, &d_val)| {
            if k_val.is_nan() || d_val.is_nan() {
                f64::NAN
            } else {
                3.0 * k_val - 2.0 * d_val
            }
        })
        .collect();

    (k, d, j)
}

/// TSI (True Strength Index) 真实强度指数
///
/// 双重平滑的动量指标，比 RSI 更平滑
///
/// - `close`: 收盘价序列
/// - `long_period`: 长周期（默认 25）
/// - `short_period`: 短周期（默认 13）
/// - `signal_period`: 信号线周期（默认 13）
///
/// 返回：(TSI, Signal)
///
/// # 算法
/// 1. Momentum = Close[i] - Close[i-1]
/// 2. Double_Smoothed_Momentum = EMA(EMA(Momentum, long), short)
/// 3. Double_Smoothed_Abs_Momentum = EMA(EMA(|Momentum|, long), short)
/// 4. TSI = 100 * Double_Smoothed_Momentum / Double_Smoothed_Abs_Momentum
/// 5. Signal = EMA(TSI, signal_period)
pub fn tsi(
    close: &[f64],
    long_period: usize,
    short_period: usize,
    signal_period: usize,
) -> (Vec<f64>, Vec<f64>) {
    let n = close.len();
    if n < 2 {
        return (vec![f64::NAN; n], vec![f64::NAN; n]);
    }

    // 1. 计算动量（价格变化）
    let mut momentum = vec![f64::NAN; n];
    for i in 1..n {
        momentum[i] = close[i] - close[i - 1];
    }

    // 2. 计算动量的绝对值
    let abs_momentum: Vec<f64> = momentum.iter().map(|&m| m.abs()).collect();

    // 3. 双重 EMA 平滑
    let ema_momentum_long = ema(&momentum, long_period);
    let ema_momentum = ema(&ema_momentum_long, short_period);

    let ema_abs_momentum_long = ema(&abs_momentum, long_period);
    let ema_abs_momentum = ema(&ema_abs_momentum_long, short_period);

    // 4. 计算 TSI
    let mut tsi_values = vec![f64::NAN; n];
    for i in 0..n {
        if !ema_momentum[i].is_nan() && !ema_abs_momentum[i].is_nan() && ema_abs_momentum[i] != 0.0
        {
            tsi_values[i] = 100.0 * ema_momentum[i] / ema_abs_momentum[i];
        }
    }

    // 5. 信号线（TSI 的 EMA）
    let signal = ema(&tsi_values, signal_period);

    (tsi_values, signal)
}

/// UO (Ultimate Oscillator) 终极振荡器
///
/// 多周期加权动量指标，结合短中长期动量
///
/// - `high`: 高价序列
/// - `low`: 低价序列
/// - `close`: 收盘价序列
/// - `period1`: 短周期（默认 7）
/// - `period2`: 中周期（默认 14）
/// - `period3`: 长周期（默认 28）
///
/// 返回：UO 值（0-100）
///
/// # 算法
/// 1. BP (Buying Pressure) = Close - Min(Low, Prev_Close)
/// 2. TR (True Range) = Max(High, Prev_Close) - Min(Low, Prev_Close)
/// 3. Average_BP_period = Sum(BP, period) / Sum(TR, period)
/// 4. UO = 100 * (4*Avg7 + 2*Avg14 + Avg28) / (4 + 2 + 1)
pub fn ultimate_oscillator(
    high: &[f64],
    low: &[f64],
    close: &[f64],
    period1: usize,
    period2: usize,
    period3: usize,
) -> Vec<f64> {
    let n = close.len();
    if n < 2 {
        return vec![f64::NAN; n];
    }

    // 1. 计算 BP 和 TR
    let mut bp = vec![f64::NAN; n];
    let mut tr = vec![f64::NAN; n];

    for i in 1..n {
        let prev_close = close[i - 1];
        let true_low = low[i].min(prev_close);
        let true_high = high[i].max(prev_close);

        bp[i] = close[i] - true_low;
        tr[i] = true_high - true_low;
    }

    // 2. 计算三个周期的平均 BP/TR 比率
    let avg1 = calc_uo_avg(&bp, &tr, period1);
    let avg2 = calc_uo_avg(&bp, &tr, period2);
    let avg3 = calc_uo_avg(&bp, &tr, period3);

    // 3. 加权计算 UO
    let mut uo = vec![f64::NAN; n];
    for i in 0..n {
        if !avg1[i].is_nan() && !avg2[i].is_nan() && !avg3[i].is_nan() {
            uo[i] = 100.0 * (4.0 * avg1[i] + 2.0 * avg2[i] + avg3[i]) / 7.0;
        }
    }

    uo
}

/// APO (Absolute Price Oscillator) 绝对价格振荡器
///
/// MACD的简化版本，仅返回快慢EMA差值
///
/// - `close`: 收盘价序列
/// - `fast_period`: 快速EMA周期（默认 12）
/// - `slow_period`: 慢速EMA周期（默认 26）
///
/// 返回：APO 值（快EMA - 慢EMA）
///
/// # 算法
/// APO = EMA(close, fast) - EMA(close, slow)
pub fn apo(close: &[f64], fast_period: usize, slow_period: usize) -> Vec<f64> {
    let ema_fast = ema(close, fast_period);
    let ema_slow = ema(close, slow_period);

    ema_fast
        .iter()
        .zip(&ema_slow)
        .map(|(&fast, &slow)| {
            if fast.is_nan() || slow.is_nan() {
                f64::NAN
            } else {
                fast - slow
            }
        })
        .collect()
}

/// PPO (Percentage Price Oscillator) 百分比价格振荡器
///
/// MACD的百分比版本
///
/// - `close`: 收盘价序列
/// - `fast_period`: 快速EMA周期（默认 12）
/// - `slow_period`: 慢速EMA周期（默认 26）
///
/// 返回：PPO 值（百分比）
///
/// # 算法
/// PPO = ((EMA_fast - EMA_slow) / EMA_slow) * 100
pub fn ppo(close: &[f64], fast_period: usize, slow_period: usize) -> Vec<f64> {
    let ema_fast = ema(close, fast_period);
    let ema_slow = ema(close, slow_period);

    ema_fast
        .iter()
        .zip(&ema_slow)
        .map(|(&fast, &slow)| {
            if fast.is_nan() || slow.is_nan() || slow == 0.0 {
                f64::NAN
            } else {
                ((fast - slow) / slow) * 100.0
            }
        })
        .collect()
}

/// CMO (Chande Momentum Oscillator) 钱德动量振荡器
///
/// 类似RSI，但使用不同的归一化公式
///
/// - `close`: 收盘价序列
/// - `period`: 周期（默认 14）
///
/// 返回：CMO 值（-100 到 +100）
///
/// # 算法
/// 1. 上涨日：su = sum(up_changes, period)
/// 2. 下跌日：sd = sum(down_changes, period)
/// 3. CMO = 100 * (su - sd) / (su + sd)
pub fn cmo(close: &[f64], period: usize) -> Vec<f64> {
    let n = close.len();
    if period == 0 || period >= n {
        return vec![f64::NAN; n];
    }

    let mut result = vec![f64::NAN; n];

    // 计算价格变化
    let mut up_changes = vec![0.0; n];
    let mut down_changes = vec![0.0; n];

    for i in 1..n {
        let change = close[i] - close[i - 1];
        if change > 0.0 {
            up_changes[i] = change;
        } else if change < 0.0 {
            down_changes[i] = -change;
        }
    }

    // 滚动窗口计算
    for i in period..n {
        let sum_up: f64 = up_changes[i + 1 - period..=i].iter().sum();
        let sum_down: f64 = down_changes[i + 1 - period..=i].iter().sum();

        let sum_total = sum_up + sum_down;
        if sum_total == 0.0 {
            result[i] = 0.0;
        } else {
            result[i] = 100.0 * (sum_up - sum_down) / sum_total;
        }
    }

    result
}

/// UO 辅助函数：计算指定周期的平均 BP/TR 比率
fn calc_uo_avg(bp: &[f64], tr: &[f64], period: usize) -> Vec<f64> {
    let n = bp.len();
    let mut result = vec![f64::NAN; n];

    for i in period..n {
        let mut sum_bp = 0.0;
        let mut sum_tr = 0.0;

        for j in 0..period {
            let idx = i - period + 1 + j;
            if !bp[idx].is_nan() && !tr[idx].is_nan() {
                sum_bp += bp[idx];
                sum_tr += tr[idx];
            }
        }

        if sum_tr != 0.0 {
            result[i] = sum_bp / sum_tr;
        }
    }

    result
}

#[cfg(test)]
mod kdj_tests {
    use super::*;

    #[test]
    fn test_kdj_basic() {
        let high = vec![110.0; 30];
        let low = vec![100.0; 30];
        let close = vec![105.0; 30];

        let (k, d, j) = kdj(&high, &low, &close, 9, 3);

        // 横盘市场中，K=D=50，J=3*50-2*50=50
        let valid_idx = 15;
        if !k[valid_idx].is_nan() && !d[valid_idx].is_nan() {
            assert!((k[valid_idx] - 50.0).abs() < 5.0);
            assert!((d[valid_idx] - 50.0).abs() < 5.0);
            assert!((j[valid_idx] - 50.0).abs() < 5.0);
        }
    }

    #[test]
    fn test_tsi_basic() {
        let close: Vec<f64> = (100..130).map(|x| x as f64).collect();

        let (tsi, _signal) = tsi(&close, 25, 13, 13);

        // 上升趋势中，TSI 应为正值
        let valid_idx = 28;
        if !tsi[valid_idx].is_nan() {
            assert!(tsi[valid_idx] > 0.0);
        }
    }

    #[test]
    fn test_uo_basic() {
        let high = vec![110.0; 50];
        let low = vec![100.0; 50];
        let close = vec![105.0; 50];

        let uo = ultimate_oscillator(&high, &low, &close, 7, 14, 28);

        // 横盘市场中，UO 应接近 50
        let valid_idx = 30;
        if !uo[valid_idx].is_nan() {
            assert!(uo[valid_idx] > 30.0 && uo[valid_idx] < 70.0);
        }
    }
}
