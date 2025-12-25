// utils/ma.rs - 移动平均工具函数
//
// 所有 MA 函数均为其他指标的构建块（ATR 使用 RMA，MACD 使用 EMA 等）

/// SMA - Simple Moving Average（简单移动平均）
///
/// 算法：sum(values[i-period+1 .. i+1]) / period
///
/// # 参数
/// - `values`: 输入序列
/// - `period`: 周期
///
/// # 返回
/// - 与输入等长的向量，前 period-1 个值为 NaN
pub fn sma(values: &[f64], period: usize) -> Vec<f64> {
    if period == 0 || period > values.len() {
        return vec![f64::NAN; values.len()];
    }

    let n = values.len();
    let mut result = vec![f64::NAN; n];
    let mut sum = 0.0;
    let mut count = 0usize;

    for i in 0..n {
        if values[i].is_nan() {
            sum = 0.0;
            count = 0;
            continue;
        }

        sum += values[i];
        count += 1;

        if count > period {
            sum -= values[i - period];
            count = period;
        }

        if count == period {
            result[i] = sum / period as f64;
        }
    }

    result
}

/// EMA - Exponential Moving Average（指数移动平均）
///
/// 算法：
/// - alpha = 2 / (period + 1)
/// - EMA[0] = SMA(period)  // 初始值使用 SMA
/// - EMA[i] = alpha * value[i] + (1 - alpha) * EMA[i-1]
///
/// # 参数
/// - `values`: 输入序列
/// - `period`: 周期
///
/// # 返回
/// - 与输入等长的向量，前 period-1 个值为 NaN
pub fn ema(values: &[f64], period: usize) -> Vec<f64> {
    if period == 0 || period > values.len() {
        return vec![f64::NAN; values.len()];
    }

    let n = values.len();
    let alpha = 2.0 / (period as f64 + 1.0);
    let mut result = vec![f64::NAN; n];

    // 支持输入中存在前导 NaN 的情况
    let mut sum = 0.0;
    let mut count = 0usize;
    let mut start_idx = None;

    for i in 0..n {
        if values[i].is_nan() {
            sum = 0.0;
            count = 0;
            continue;
        }

        count += 1;
        sum += values[i];

        if count > period {
            sum -= values[i - period];
            count = period;
        }

        if count == period {
            result[i] = sum / period as f64;
            start_idx = Some(i);
            break;
        }
    }

    if let Some(start) = start_idx {
        for i in (start + 1)..n {
            if values[i].is_nan() {
                result[i] = result[i - 1];
            } else {
                result[i] = alpha * values[i] + (1.0 - alpha) * result[i - 1];
            }
        }
    }

    result
}

/// RMA - Wilder's Moving Average（威尔德移动平均）
///
/// 算法：RMA[i] = (RMA[i-1] * (period - 1) + value[i]) / period
/// 等价于 EMA with alpha = 1 / period
///
/// 用于：ATR、RSI 等指标
///
/// # 参数
/// - `values`: 输入序列
/// - `period`: 周期
///
/// # 返回
/// - 与输入等长的向量，前 period-1 个值为 NaN
pub fn rma(values: &[f64], period: usize) -> Vec<f64> {
    if period == 0 || period > values.len() {
        return vec![f64::NAN; values.len()];
    }

    let alpha = 1.0 / period as f64;
    let mut result = vec![f64::NAN; values.len()];

    // 初始值使用 SMA
    let first_sum: f64 = values[..period].iter().sum();
    result[period - 1] = first_sum / period as f64;

    // Wilder's smoothing
    for i in period..values.len() {
        result[i] = alpha * values[i] + (1.0 - alpha) * result[i - 1];
    }

    result
}

/// WMA - Weighted Moving Average（加权移动平均）
///
/// 算法：WMA = sum(value[i] * weight[i]) / sum(weight)
/// 其中 weight[i] = i + 1（线性递增权重）
///
/// # 参数
/// - `values`: 输入序列
/// - `period`: 周期
///
/// # 返回
/// - 与输入等长的向量，前 period-1 个值为 NaN
pub fn wma(values: &[f64], period: usize) -> Vec<f64> {
    if period == 0 || period > values.len() {
        return vec![f64::NAN; values.len()];
    }

    let mut result = vec![f64::NAN; values.len()];
    let weight_sum: f64 = (1..=period).map(|x| x as f64).sum();

    for i in (period - 1)..values.len() {
        let weighted_sum: f64 = values[i + 1 - period..=i]
            .iter()
            .enumerate()
            .map(|(idx, &val)| val * (idx + 1) as f64)
            .sum();
        result[i] = weighted_sum / weight_sum;
    }

    result
}

/// HMA - Hull Moving Average（赫尔移动平均，低延迟）
///
/// 算法：
/// - half_period = period / 2
/// - sqrt_period = sqrt(period)
/// - HMA = WMA(2 * WMA(half_period) - WMA(period), sqrt_period)
///
/// 特点：响应速度快，延迟低
///
/// # 参数
/// - `values`: 输入序列
/// - `period`: 周期
///
/// # 返回
/// - 与输入等长的向量
pub fn hma(values: &[f64], period: usize) -> Vec<f64> {
    if period == 0 || period > values.len() {
        return vec![f64::NAN; values.len()];
    }

    let half_period = period / 2;
    let sqrt_period = (period as f64).sqrt() as usize;

    let wma_half = wma(values, half_period);
    let wma_full = wma(values, period);

    // 2 * WMA(half) - WMA(full)
    let diff: Vec<f64> = wma_half
        .iter()
        .zip(&wma_full)
        .map(|(&a, &b)| {
            if a.is_nan() || b.is_nan() {
                f64::NAN
            } else {
                2.0 * a - b
            }
        })
        .collect();

    wma(&diff, sqrt_period)
}

/// DEMA - Double Exponential Moving Average（双重指数移动平均）
///
/// 算法：DEMA = 2 * EMA(period) - EMA(EMA(period))
///
/// # 参数
/// - `values`: 输入序列
/// - `period`: 周期
///
/// # 返回
/// - 与输入等长的向量
pub fn dema(values: &[f64], period: usize) -> Vec<f64> {
    let ema1 = ema(values, period);
    let ema2 = ema(&ema1, period);

    ema1.iter()
        .zip(&ema2)
        .map(|(&e1, &e2)| {
            if e1.is_nan() || e2.is_nan() {
                f64::NAN
            } else {
                2.0 * e1 - e2
            }
        })
        .collect()
}

/// TEMA - Triple Exponential Moving Average（三重指数移动平均）
///
/// 算法：TEMA = 3*EMA - 3*EMA(EMA) + EMA(EMA(EMA))
///
/// # 参数
/// - `values`: 输入序列
/// - `period`: 周期
///
/// # 返回
/// - 与输入等长的向量
pub fn tema(values: &[f64], period: usize) -> Vec<f64> {
    let ema1 = ema(values, period);
    let ema2 = ema(&ema1, period);
    let ema3 = ema(&ema2, period);

    ema1.iter()
        .zip(&ema2)
        .zip(&ema3)
        .map(|((&e1, &e2), &e3)| {
            if e1.is_nan() || e2.is_nan() || e3.is_nan() {
                f64::NAN
            } else {
                3.0 * e1 - 3.0 * e2 + e3
            }
        })
        .collect()
}

/// VWAP - Volume Weighted Average Price（成交量加权平均价）
///
/// 算法：VWAP = sum(typical_price * volume) / sum(volume)
///
/// # 参数
/// - `typical_prices`: 典型价格序列 (H+L+C)/3
/// - `volumes`: 成交量序列
/// - `period`: 周期（0 表示累积 VWAP）
///
/// # 返回
/// - 与输入等长的向量
pub fn vwap(typical_prices: &[f64], volumes: &[f64], period: usize) -> Vec<f64> {
    if typical_prices.len() != volumes.len() {
        return vec![f64::NAN; typical_prices.len()];
    }

    let n = typical_prices.len();
    let mut result = vec![f64::NAN; n];

    if n == 0 {
        return result;
    }

    if period == 0 {
        // 累积 VWAP
        let mut cum_pv = 0.0;
        let mut cum_v = 0.0;
        for i in 0..n {
            cum_pv += typical_prices[i] * volumes[i];
            cum_v += volumes[i];
            result[i] = if cum_v == 0.0 { f64::NAN } else { cum_pv / cum_v };
        }
        return result;
    }

    if period > n {
        return result;
    }

    // 滚动 VWAP（增量更新）
    let mut pv_sum: f64 = typical_prices[..period]
        .iter()
        .zip(&volumes[..period])
        .map(|(&p, &v)| p * v)
        .sum();
    let mut v_sum: f64 = volumes[..period].iter().sum();

    result[period - 1] = if v_sum == 0.0 { f64::NAN } else { pv_sum / v_sum };

    for i in period..n {
        pv_sum += typical_prices[i] * volumes[i] - typical_prices[i - period] * volumes[i - period];
        v_sum += volumes[i] - volumes[i - period];
        result[i] = if v_sum == 0.0 { f64::NAN } else { pv_sum / v_sum };
    }

    result
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_sma() {
        let values = vec![1.0, 2.0, 3.0, 4.0, 5.0];
        let result = sma(&values, 3);
        assert!(result[0].is_nan());
        assert!(result[1].is_nan());
        assert_eq!(result[2], 2.0);  // (1+2+3)/3
        assert_eq!(result[3], 3.0);  // (2+3+4)/3
        assert_eq!(result[4], 4.0);  // (3+4+5)/3
    }

    #[test]
    fn test_ema() {
        let values = vec![1.0, 2.0, 3.0, 4.0, 5.0];
        let result = ema(&values, 3);
        assert!(result[0].is_nan());
        assert!(result[1].is_nan());
        assert_eq!(result[2], 2.0);  // 初始值 = SMA
        // EMA[3] = 0.5 * 4 + 0.5 * 2 = 3.0
        assert!((result[3] - 3.0).abs() < 1e-10);
    }

    #[test]
    fn test_rma() {
        let values = vec![1.0, 2.0, 3.0, 4.0, 5.0];
        let result = rma(&values, 3);
        assert!(result[0].is_nan());
        assert!(result[1].is_nan());
        assert_eq!(result[2], 2.0);  // 初始值 = SMA
    }

    #[test]
    fn test_vwap() {
        let prices = vec![100.0, 101.0, 102.0];
        let volumes = vec![1000.0, 1100.0, 1200.0];
        let result = vwap(&prices, &volumes, 0);  // 累积 VWAP
        assert_eq!(result[0], 100.0);
        // (100*1000 + 101*1100) / (1000+1100) = 211100 / 2100 ≈ 100.52
        assert!((result[1] - 100.52380952380952).abs() < 1e-10);
    }

    #[test]
    fn test_vwap_rolling() {
        let prices = vec![100.0, 101.0, 102.0, 103.0];
        let volumes = vec![10.0, 10.0, 10.0, 10.0];
        let result = vwap(&prices, &volumes, 2);
        assert!(result[0].is_nan());
        assert!((result[1] - 100.5).abs() < 1e-10);
        assert!((result[2] - 101.5).abs() < 1e-10);
        assert!((result[3] - 102.5).abs() < 1e-10);
    }

    #[test]
    fn test_vwap_zero_volume() {
        let prices = vec![100.0, 101.0];
        let volumes = vec![0.0, 0.0];
        let result = vwap(&prices, &volumes, 0);
        assert!(result[0].is_nan());
        assert!(result[1].is_nan());
    }
}

/// ZLMA (Zero Lag Moving Average) 零延迟移动平均
///
/// 尝试消除 EMA 的延迟，更快响应价格变化
///
/// - `values`: 输入序列
/// - `period`: 周期
///
/// 返回：ZLMA 序列
///
/// # 算法
/// 1. Lag = (period - 1) / 2
/// 2. EMA_Data = 2 * values - values[lag_ago]
/// 3. ZLMA = EMA(EMA_Data, period)
pub fn zlma(values: &[f64], period: usize) -> Vec<f64> {
    let n = values.len();
    if period == 0 || period > n {
        return vec![f64::NAN; n];
    }

    let lag = (period - 1) / 2;
    let mut ema_data = vec![f64::NAN; n];

    for i in lag..n {
        ema_data[i] = 2.0 * values[i] - values[i - lag];
    }

    ema(&ema_data, period)
}

/// T3 (Tillson T3) 移动平均
///
/// 6 重 EMA 平滑，减少噪音同时保持快速响应
///
/// - `values`: 输入序列
/// - `period`: 周期
/// - `v_factor`: 平滑因子（通常 0.7）
///
/// 返回：T3 序列
///
/// # 算法
/// 使用 6 层 EMA 和特殊系数
pub fn t3(values: &[f64], period: usize, v_factor: f64) -> Vec<f64> {
    let n = values.len();
    if period == 0 || n == 0 {
        return vec![f64::NAN; n];
    }

    // 计算系数
    let c1 = -v_factor * v_factor * v_factor;
    let c2 = 3.0 * v_factor * v_factor + 3.0 * v_factor * v_factor * v_factor;
    let c3 = -6.0 * v_factor * v_factor - 3.0 * v_factor - 3.0 * v_factor * v_factor * v_factor;
    let c4 = 1.0 + 3.0 * v_factor + v_factor * v_factor * v_factor + 3.0 * v_factor * v_factor;

    // 6 层 EMA
    let e1 = ema(values, period);
    let e2 = ema(&e1, period);
    let e3 = ema(&e2, period);
    let e4 = ema(&e3, period);
    let e5 = ema(&e4, period);
    let e6 = ema(&e5, period);

    // 加权组合
    let mut t3_values = vec![f64::NAN; n];
    for i in 0..n {
        if !e3[i].is_nan() && !e4[i].is_nan() && !e5[i].is_nan() && !e6[i].is_nan() {
            t3_values[i] = c1 * e6[i] + c2 * e5[i] + c3 * e4[i] + c4 * e3[i];
        }
    }

    t3_values
}

/// KAMA (Kaufman's Adaptive Moving Average) 考夫曼自适应移动平均
///
/// 根据市场波动性自适应调整平滑度
///
/// - `values`: 输入序列
/// - `period`: 效率比率周期（默认 10）
/// - `fast_period`: 快速 EMA 周期（默认 2）
/// - `slow_period`: 慢速 EMA 周期（默认 30）
///
/// 返回：KAMA 序列
///
/// # 算法
/// 1. Change = |Price[i] - Price[i-period]|
/// 2. Volatility = Sum(|Price[i] - Price[i-1]|, period)
/// 3. ER (Efficiency Ratio) = Change / Volatility
/// 4. SC (Smoothing Constant) = [ER * (Fast_SC - Slow_SC) + Slow_SC]^2
/// 5. KAMA[i] = KAMA[i-1] + SC * (Price[i] - KAMA[i-1])
pub fn kama(
    values: &[f64],
    period: usize,
    fast_period: usize,
    slow_period: usize,
) -> Vec<f64> {
    let n = values.len();
    if period == 0 || period >= n {
        return vec![f64::NAN; n];
    }

    // 计算 EMA 平滑常数
    let fast_sc = 2.0 / (fast_period + 1) as f64;
    let slow_sc = 2.0 / (slow_period + 1) as f64;

    let mut kama_values = vec![f64::NAN; n];
    kama_values[period - 1] = values[period - 1];  // 初始值

    for i in period..n {
        // 1. 计算价格变化
        let change = (values[i] - values[i - period]).abs();

        // 2. 计算波动性（价格变动的绝对值和）
        let mut volatility = 0.0;
        for j in 0..period {
            let idx = i - period + 1 + j;
            volatility += (values[idx] - values[idx - 1]).abs();
        }

        // 3. 效率比率
        let er = if volatility > 0.0 {
            change / volatility
        } else {
            0.0
        };

        // 4. 平滑常数
        let sc = (er * (fast_sc - slow_sc) + slow_sc).powi(2);

        // 5. KAMA
        kama_values[i] = kama_values[i - 1] + sc * (values[i] - kama_values[i - 1]);
    }

    kama_values
}

/// FRAMA (Fractal Adaptive Moving Average) 分形自适应移动平均
///
/// 基于分形维度自适应调整
///
/// - `values`: 输入序列
/// - `period`: 周期（必须是偶数，默认 16）
///
/// 返回：FRAMA 序列
///
/// # 算法
/// 使用分形维度计算自适应 alpha
pub fn frama(values: &[f64], period: usize) -> Vec<f64> {
    let n = values.len();
    if period < 2 || period % 2 != 0 || period > n {
        return vec![f64::NAN; n];
    }

    let half = period / 2;
    let mut frama_values = vec![f64::NAN; n];

    // 初始值
    if n > period {
        frama_values[period - 1] = values[period - 1];
    }

    for i in period..n {
        // 计算前半周期和后半周期的最高最低价
        let mut n1_high = f64::NEG_INFINITY;
        let mut n1_low = f64::INFINITY;
        let mut n2_high = f64::NEG_INFINITY;
        let mut n2_low = f64::INFINITY;

        for j in 0..half {
            let idx1 = i - period + j;
            let idx2 = i - half + j;

            n1_high = n1_high.max(values[idx1]);
            n1_low = n1_low.min(values[idx1]);
            n2_high = n2_high.max(values[idx2]);
            n2_low = n2_low.min(values[idx2]);
        }

        let n1 = (n1_high - n1_low) / (half as f64);
        let n2 = (n2_high - n2_low) / (half as f64);

        let mut n3_high = f64::NEG_INFINITY;
        let mut n3_low = f64::INFINITY;
        for j in 0..period {
            let idx = i - period + j;
            n3_high = n3_high.max(values[idx]);
            n3_low = n3_low.min(values[idx]);
        }
        let n3 = (n3_high - n3_low) / (period as f64);

        // 分形维度
        let dimen = if n1 + n2 > 0.0 && n3 > 0.0 {
            ((n1 + n2).ln() - n3.ln()) / 2_f64.ln()
        } else {
            1.0
        };

        // Alpha
        let alpha = (-4.6 * (dimen - 1.0)).exp();
        let alpha_clamped = alpha.clamp(0.01, 1.0);

        // FRAMA
        frama_values[i] = alpha_clamped * values[i] + (1.0 - alpha_clamped) * frama_values[i - 1];
    }

    frama_values
}

#[cfg(test)]
mod advanced_ma_tests {
    use super::*;

    #[test]
    fn test_zlma_basic() {
        let values: Vec<f64> = (100..120).map(|x| x as f64).collect();

        let zlma_values = zlma(&values, 10);

        // 上升趋势中，ZLMA 应跟随价格上升
        let valid_idx = zlma_values.iter().position(|v| !v.is_nan()).unwrap();
        assert!(zlma_values[valid_idx] > 100.0);
    }

    #[test]
    fn test_t3_basic() {
        let values: Vec<f64> = (100..130).map(|x| x as f64).collect();

        let t3_values = t3(&values, 5, 0.7);

        // T3 应该平滑趋势
        let valid_idx = t3_values.iter().position(|v| !v.is_nan()).unwrap();
        assert!(t3_values[valid_idx] > 100.0);
    }

    #[test]
    fn test_kama_basic() {
        let values: Vec<f64> = (100..150).map(|x| x as f64).collect();

        let kama_values = kama(&values, 10, 2, 30);

        // KAMA 应该跟随趋势
        let valid_idx = kama_values.iter().position(|v| !v.is_nan()).unwrap();
        assert!(kama_values[valid_idx] > 100.0);
        assert!(kama_values[valid_idx] < 150.0);
    }

    #[test]
    fn test_frama_basic() {
        let values: Vec<f64> = (100..132).map(|x| x as f64).collect();

        let frama_values = frama(&values, 16);

        // FRAMA 应该有效
        let valid_idx = frama_values.iter().position(|v| !v.is_nan()).unwrap();
        assert!(frama_values[valid_idx] > 100.0);
    }
}
