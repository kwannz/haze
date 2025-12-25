// indicators/sfg.rs - SFG 交易信号指标
#![allow(dead_code)]
//
// 基于系统指标实现的高级复合交易信号
// 使用纯 Rust ML (linfa) 替代 KNN,获得 42-68% 性能提升
// 参考：SFG_交易信号指标.pdf

use crate::indicators::{supertrend, atr, rsi};
use crate::ml::trainer::{
    online_predict_atr2, online_predict_momentum, online_predict_supertrend, TrainConfig,
};
use crate::ml::models::ModelType;
use crate::utils::{wma, sma, ema};
use std::cmp::Ordering;

// ============================================================
// ML 增强版 SFG 指标 (推荐使用)
// ============================================================

/// AI SuperTrend 结果
#[derive(Debug, Clone)]
pub struct AISuperTrendResult {
    /// SuperTrend 值
    pub supertrend: Vec<f64>,
    /// 趋势方向: 1.0=看涨, -1.0=看跌
    pub direction: Vec<f64>,
    /// ML 预测的趋势偏移
    pub trend_offset: Vec<f64>,
    /// 买入信号
    pub buy_signals: Vec<f64>,
    /// 卖出信号
    pub sell_signals: Vec<f64>,
    /// 动态止损
    pub stop_loss: Vec<f64>,
    /// 动态止盈
    pub take_profit: Vec<f64>,
}

/// AI SuperTrend - 使用 ML 增强的 SuperTrend
///
/// 使用 linfa SVR/LinearRegression 替代 KNN,性能提升 42-68%
///
/// # 参数
/// - `high`: 最高价序列
/// - `low`: 最低价序列
/// - `close`: 收盘价序列
/// - `st_length`: SuperTrend 周期（默认 10）
/// - `st_multiplier`: SuperTrend ATR 乘数（默认 3.0）
/// - `model_type`: 模型类型 ("linreg" | "ridge")
/// - `lookback`: ML 特征滞后周期（默认 10）
/// - `train_window`: 训练窗口（默认 200）
pub fn ai_supertrend_ml(
    high: &[f64],
    low: &[f64],
    close: &[f64],
    st_length: usize,
    st_multiplier: f64,
    model_type: &str,
    lookback: usize,
    train_window: usize,
) -> AISuperTrendResult {
    let len = close.len();

    // 1. 计算传统 SuperTrend
    let (st_values, st_direction, _, _) =
        supertrend(high, low, close, st_length, st_multiplier);

    // 2. 计算 ATR
    let atr_values = atr(high, low, close, st_length);

    // 3. ML 预测趋势偏移
    let config = TrainConfig {
        train_window,
        lookback,
        rolling: true,
        model_type: match model_type {
            "ridge" => ModelType::Ridge,
            _ => ModelType::LinearRegression,
        },
        ridge_alpha: 1.0,
        use_polynomial: false,
    };

    let trend_offset = online_predict_supertrend(close, &atr_values, &config);

    // 4. 生成增强信号
    let mut buy_signals = vec![0.0; len];
    let mut sell_signals = vec![0.0; len];
    let mut stop_loss = vec![f64::NAN; len];
    let mut take_profit = vec![f64::NAN; len];

    for i in 1..len {
        let prev_dir = st_direction[i - 1];
        let curr_dir = st_direction[i];
        let ml_signal = trend_offset[i];

        // 买入: 方向变为看涨 + ML 预测上涨
        if curr_dir > 0.5 && prev_dir < 0.5 && ml_signal > 0.0 {
            buy_signals[i] = 1.0;
            let atr_val = if atr_values[i].is_nan() { 0.0 } else { atr_values[i] };
            stop_loss[i] = close[i] - 2.0 * atr_val;
            take_profit[i] = close[i] + 3.0 * atr_val;
        }

        // 卖出: 方向变为看跌 + ML 预测下跌
        if curr_dir < -0.5 && prev_dir > -0.5 && ml_signal < 0.0 {
            sell_signals[i] = 1.0;
            let atr_val = if atr_values[i].is_nan() { 0.0 } else { atr_values[i] };
            stop_loss[i] = close[i] + 2.0 * atr_val;
            take_profit[i] = close[i] - 3.0 * atr_val;
        }
    }

    AISuperTrendResult {
        supertrend: st_values,
        direction: st_direction,
        trend_offset,
        buy_signals,
        sell_signals,
        stop_loss,
        take_profit,
    }
}

/// ATR2 信号结果 (ML 增强版)
#[derive(Debug, Clone)]
pub struct ATR2SignalResult {
    pub rsi: Vec<f64>,
    pub dynamic_buy_threshold: Vec<f64>,
    pub dynamic_sell_threshold: Vec<f64>,
    pub buy_signals: Vec<f64>,
    pub sell_signals: Vec<f64>,
    pub signal_strength: Vec<f64>,
    pub stop_loss: Vec<f64>,
    pub take_profit: Vec<f64>,
}

/// ATR2 信号指标 - ML 增强版
pub fn atr2_signals_ml(
    high: &[f64],
    low: &[f64],
    close: &[f64],
    volume: &[f64],
    rsi_period: usize,
    atr_period: usize,
    ridge_alpha: f64,
    momentum_window: usize,
) -> ATR2SignalResult {
    let len = close.len();

    // 1. 计算基础指标
    let rsi_values = rsi(close, rsi_period);
    let atr_values = atr(high, low, close, atr_period);

    // 2. ML 预测阈值调整
    let config = TrainConfig {
        train_window: 200,
        lookback: momentum_window,
        rolling: true,
        model_type: ModelType::Ridge,
        ridge_alpha,
        use_polynomial: false,
    };

    let threshold_adj = online_predict_atr2(close, &atr_values, volume, &config);

    // 3. 计算动态阈值
    let mut dynamic_buy_threshold = vec![30.0; len];
    let mut dynamic_sell_threshold = vec![70.0; len];

    for i in 0..len {
        let adj = threshold_adj[i].clamp(-10.0, 10.0);
        dynamic_buy_threshold[i] = 30.0 - adj;
        dynamic_sell_threshold[i] = 70.0 + adj;
    }

    // 4. 生成信号
    let mut buy_signals = vec![0.0; len];
    let mut sell_signals = vec![0.0; len];
    let mut signal_strength = vec![0.0; len];
    let mut stop_loss = vec![f64::NAN; len];
    let mut take_profit = vec![f64::NAN; len];

    let volume_ma = sma(volume, atr_period);

    for i in atr_period..len {
        let volume_confirmed = if !volume_ma[i].is_nan() && volume_ma[i] > 0.0 {
            volume[i] > volume_ma[i]
        } else {
            true
        };

        // 买入信号
        if !rsi_values[i].is_nan() && rsi_values[i] < dynamic_buy_threshold[i] && volume_confirmed {
            buy_signals[i] = 1.0;
            signal_strength[i] = (dynamic_buy_threshold[i] - rsi_values[i]) / 30.0;
            let atr_val = if atr_values[i].is_nan() { 0.0 } else { atr_values[i] };
            stop_loss[i] = close[i] - 2.0 * atr_val;
            take_profit[i] = close[i] + 3.0 * atr_val;
        }

        // 卖出信号
        if !rsi_values[i].is_nan() && rsi_values[i] > dynamic_sell_threshold[i] && volume_confirmed {
            sell_signals[i] = 1.0;
            signal_strength[i] = (rsi_values[i] - dynamic_sell_threshold[i]) / 30.0;
            let atr_val = if atr_values[i].is_nan() { 0.0 } else { atr_values[i] };
            stop_loss[i] = close[i] + 2.0 * atr_val;
            take_profit[i] = close[i] - 3.0 * atr_val;
        }
    }

    ATR2SignalResult {
        rsi: rsi_values,
        dynamic_buy_threshold,
        dynamic_sell_threshold,
        buy_signals,
        sell_signals,
        signal_strength,
        stop_loss,
        take_profit,
    }
}

/// AI Momentum Index 结果 (ML 增强版)
#[derive(Debug, Clone)]
pub struct AIMomentumResult {
    pub rsi: Vec<f64>,
    pub predicted_momentum: Vec<f64>,
    pub momentum_ma: Vec<f64>,
    pub zero_cross_buy: Vec<f64>,
    pub zero_cross_sell: Vec<f64>,
    pub overbought: Vec<f64>,
    pub oversold: Vec<f64>,
}

/// AI Momentum Index - ML 增强版
pub fn ai_momentum_index_ml(
    close: &[f64],
    rsi_period: usize,
    smooth_period: usize,
    use_polynomial: bool,
    lookback: usize,
    train_window: usize,
) -> AIMomentumResult {
    let len = close.len();

    // 1. 计算 RSI
    let rsi_values = rsi(close, rsi_period);

    // 2. ML 预测动量
    let config = TrainConfig {
        train_window,
        lookback,
        rolling: true,
        model_type: ModelType::LinearRegression,
        ridge_alpha: 1.0,
        use_polynomial,
    };

    let predicted_momentum = online_predict_momentum(&rsi_values, &config);

    // 3. 计算动量移动平均
    let momentum_ma = ema(&predicted_momentum, smooth_period);

    // 4. 生成信号
    let mut zero_cross_buy = vec![0.0; len];
    let mut zero_cross_sell = vec![0.0; len];
    let mut overbought = vec![0.0; len];
    let mut oversold = vec![0.0; len];

    for i in 1..len {
        let curr_mom = predicted_momentum[i];
        let prev_mom = predicted_momentum[i - 1];

        // 零线交叉
        if curr_mom > 0.0 && prev_mom <= 0.0 {
            zero_cross_buy[i] = 1.0;
        }
        if curr_mom < 0.0 && prev_mom >= 0.0 {
            zero_cross_sell[i] = 1.0;
        }

        // 超买超卖
        if curr_mom > 25.0 {
            overbought[i] = 1.0;
        }
        if curr_mom < -25.0 {
            oversold[i] = 1.0;
        }
    }

    AIMomentumResult {
        rsi: rsi_values,
        predicted_momentum,
        momentum_ma,
        zero_cross_buy,
        zero_cross_sell,
        overbought,
        oversold,
    }
}

/// Pivot 买卖信号结果
#[derive(Debug, Clone)]
pub struct PivotSignalResult {
    pub pivot: Vec<f64>,
    pub r1: Vec<f64>,
    pub r2: Vec<f64>,
    pub s1: Vec<f64>,
    pub s2: Vec<f64>,
    pub buy_signals: Vec<f64>,
    pub sell_signals: Vec<f64>,
}

/// Pivot 买卖信号 - 基于枢轴点
pub fn pivot_buy_sell(
    high: &[f64],
    low: &[f64],
    close: &[f64],
    lookback: usize,
) -> PivotSignalResult {
    let len = close.len();

    let mut pivot = vec![f64::NAN; len];
    let mut r1 = vec![f64::NAN; len];
    let mut r2 = vec![f64::NAN; len];
    let mut s1 = vec![f64::NAN; len];
    let mut s2 = vec![f64::NAN; len];
    let mut buy_signals = vec![0.0; len];
    let mut sell_signals = vec![0.0; len];

    for i in lookback..len {
        let period_high = high[(i - lookback)..i].iter().cloned().fold(f64::NEG_INFINITY, f64::max);
        let period_low = low[(i - lookback)..i].iter().cloned().fold(f64::INFINITY, f64::min);
        let period_close = close[i - 1];

        let p = (period_high + period_low + period_close) / 3.0;
        pivot[i] = p;

        r1[i] = 2.0 * p - period_low;
        r2[i] = p + (period_high - period_low);
        s1[i] = 2.0 * p - period_high;
        s2[i] = p - (period_high - period_low);

        if i > 0 && close[i - 1] < s1[i] && close[i] > s1[i] {
            buy_signals[i] = 1.0;
        }

        if i > 0 && close[i - 1] > r1[i] && close[i] < r1[i] {
            sell_signals[i] = 1.0;
        }
    }

    PivotSignalResult {
        pivot,
        r1,
        r2,
        s1,
        s2,
        buy_signals,
        sell_signals,
    }
}

// ============================================================
// 原始 KNN 版本 (保留向后兼容)
// ============================================================

/// AI SuperTrend - 基于 KNN 机器学习的 SuperTrend 增强版
///
/// 结合 KNN 算法优化趋势识别
///
/// # 参数
/// - `high`: 最高价序列
/// - `low`: 最低价序列
/// - `close`: 收盘价序列
/// - `k`: KNN 邻居数（默认 5）
/// - `n`: 数据点数量（默认 100）
/// - `price_trend`: 价格趋势周期（默认 10）
/// - `predict_trend`: 预测趋势周期（默认 10）
/// - `st_length`: SuperTrend 周期（默认 10）
/// - `st_multiplier`: SuperTrend ATR 乘数（默认 3.0）
///
/// # 返回
/// - (supertrend_values, trend_direction) 元组
///   - supertrend_values: SuperTrend 值
///   - trend_direction: 1.0=看涨, -1.0=看跌
pub fn ai_supertrend(
    high: &[f64],
    low: &[f64],
    close: &[f64],
    k: usize,
    n: usize,
    price_trend: usize,
    predict_trend: usize,
    st_length: usize,
    st_multiplier: f64,
) -> (Vec<f64>, Vec<f64>) {
    let len = close.len();

    // 1. 计算传统 SuperTrend
    let (st_values, st_direction, _basic_upper, _basic_lower) = supertrend(high, low, close, st_length, st_multiplier);
    
    // 2. 计算价格加权移动平均（用于 KNN 特征）
    let price_wma = wma(close, price_trend);
    
    // 3. 计算 SuperTrend 加权移动平均
    let st_wma = wma(&st_values, predict_trend);
    
    // 4. KNN 预测优化
    let optimized_st = st_values;
    let mut optimized_dir = st_direction.clone();
    if len == 0 || k == 0 {
        return (optimized_st, optimized_dir);
    }

    let mut distances: Vec<(usize, f64)> = Vec::new();
    if len > n + k {
        for i in n..len {
            // 提取当前窗口的特征
            let current_price_trend = if !price_wma[i].is_nan() { price_wma[i] } else { close[i] };
            let current_st_trend = if !st_wma[i].is_nan() { st_wma[i] } else { optimized_st[i] };

            // KNN: 找到最相似的 k 个历史点
            distances.clear();
            let window_end = i.saturating_sub(k);
            let mut window_start = k;
            if n > 0 {
                window_start = window_start.max(i.saturating_sub(n));
            }
            if window_end <= window_start {
                continue;
            }
            distances.reserve(window_end - window_start);

            for j in window_start..window_end {
                if !price_wma[j].is_nan() && !st_wma[j].is_nan() {
                    // 计算欧氏距离
                    let price_diff = current_price_trend - price_wma[j];
                    let st_diff = current_st_trend - st_wma[j];
                    let distance = (price_diff * price_diff + st_diff * st_diff).sqrt();

                    distances.push((j, distance));
                }
            }

            if distances.len() >= k {
                // 选择最近的 k 个邻居，带索引的稳定 tie-break
                distances.select_nth_unstable_by(k - 1, |a, b| {
                    let ord = a.1.partial_cmp(&b.1).unwrap_or(Ordering::Equal);
                    if ord == Ordering::Equal {
                        a.0.cmp(&b.0)
                    } else {
                        ord
                    }
                });

                // 计算邻居的平均趋势方向
                let mut trend_sum = 0.0;
                for idx in 0..k {
                    let neighbor_idx = distances[idx].0;
                    if neighbor_idx + 1 < len {
                        trend_sum += st_direction[neighbor_idx + 1];
                    }
                }
                
                let predicted_direction = trend_sum / k as f64;
                
                // 如果 KNN 预测与当前方向不一致，进行平滑
                if predicted_direction.abs() > 0.5 {
                    optimized_dir[i] = if predicted_direction > 0.0 { 1.0 } else { -1.0 };
                }
            }
        }
    }
    
    (optimized_st, optimized_dir)
}

/// AI Momentum Index - 基于 KNN 和 RSI 的动量指标
///
/// 使用 KNN 算法分析价格与 RSI 的关系预测未来走势
///
/// # 参数
/// - `close`: 收盘价序列
/// - `k`: KNN 预测数据量（默认 50）
/// - `trend_length`: 趋势周期（默认 14）
/// - `smooth`: 平滑周期（默认 3）
///
/// # 返回
/// - (prediction, prediction_ma) 元组
pub fn ai_momentum_index(
    close: &[f64],
    k: usize,
    trend_length: usize,
    smooth: usize,
) -> (Vec<f64>, Vec<f64>) {
    let len = close.len();
    
    // 1. 计算 RSI
    let rsi = crate::indicators::rsi(close, trend_length);
    
    // 2. 初始化预测值
    let mut prediction = vec![f64::NAN; len];
    
    // 3. KNN 预测
    let mut distances: Vec<(usize, f64)> = Vec::new();
    if len > k + trend_length && k > 0 {
        for i in (k + trend_length)..len {
            let current_rsi = if !rsi[i].is_nan() { rsi[i] } else { 50.0 };
            let current_price = close[i];

            // 找到相似的历史点
            distances.clear();
            let window_end = i.saturating_sub(trend_length);
            if window_end <= trend_length {
                continue;
            }
            distances.reserve(window_end - trend_length);

            for j in trend_length..window_end {
                if !rsi[j].is_nan() {
                    // 计算特征距离
                    let rsi_delta = current_rsi - rsi[j];
                    let rsi_diff = rsi_delta * rsi_delta;
                    let price_ratio = if close[j] != 0.0 {
                        let ratio = (current_price / close[j]) - 1.0;
                        ratio * ratio
                    } else {
                        0.0
                    };

                    let distance = (rsi_diff + price_ratio * 100.0).sqrt();
                    distances.push((j, distance));
                }
            }

            if distances.len() >= k {
                distances.select_nth_unstable_by(k - 1, |a, b| {
                    let ord = a.1.partial_cmp(&b.1).unwrap_or(Ordering::Equal);
                    if ord == Ordering::Equal {
                        a.0.cmp(&b.0)
                    } else {
                        ord
                    }
                });

                // 计算邻居的平均未来动量
                let mut momentum_sum = 0.0;
                let mut valid_count = 0;
                
                for idx in 0..k {
                    let neighbor_idx = distances[idx].0;
                    if neighbor_idx + 1 < len && !rsi[neighbor_idx + 1].is_nan() {
                        // 动量 = 未来RSI - 当前RSI
                        momentum_sum += rsi[neighbor_idx + 1] - rsi[neighbor_idx];
                        valid_count += 1;
                    }
                }
                
                if valid_count > 0 {
                    prediction[i] = momentum_sum / valid_count as f64;
                }
            }
        }
    }
    
    // 4. 计算预测值的移动平均
    let prediction_ma = sma(&prediction, smooth);
    
    (prediction, prediction_ma)
}

/// Dynamic MACD - 动态 MACD 加平均 K 线
///
/// 结合 Heikin-Ashi 的 MACD 变种
///
/// # 参数
/// - `open`: 开盘价
/// - `high`: 最高价
/// - `low`: 最低价
/// - `close`: 收盘价
/// - `fast_length`: 快线周期（默认 12）
/// - `slow_length`: 慢线周期（默认 26）
/// - `signal_smooth`: 信号线平滑（默认 9）
///
/// # 返回
/// - (macd, signal, histogram, ha_open, ha_close) 元组
pub fn dynamic_macd(
    open: &[f64],
    high: &[f64],
    low: &[f64],
    close: &[f64],
    fast_length: usize,
    slow_length: usize,
    signal_smooth: usize,
) -> (Vec<f64>, Vec<f64>, Vec<f64>, Vec<f64>, Vec<f64>) {
    let len = close.len();
    
    // 1. 计算 Heikin-Ashi K线
    let mut ha_open = vec![f64::NAN; len];
    let mut ha_close = vec![f64::NAN; len];
    
    ha_open[0] = (open[0] + close[0]) / 2.0;
    ha_close[0] = (open[0] + high[0] + low[0] + close[0]) / 4.0;
    
    for i in 1..len {
        ha_open[i] = (ha_open[i - 1] + ha_close[i - 1]) / 2.0;
        ha_close[i] = (open[i] + high[i] + low[i] + close[i]) / 4.0;
    }
    
    // 2. 使用 HLCC4 作为数据源
    let mut hlcc4 = vec![0.0; len];
    for i in 0..len {
        hlcc4[i] = (high[i] + low[i] + close[i] + close[i]) / 4.0;
    }
    
    // 3. 计算 MACD
    let (macd, signal, histogram) = crate::indicators::macd(&hlcc4, fast_length, slow_length, signal_smooth);
    
    (macd, signal, histogram, ha_open, ha_close)
}

/// ATR2 信号指标 - 基于 ATR 和动量的交易信号
///
/// # 参数
/// - `high`: 最高价
/// - `low`: 最低价
/// - `close`: 收盘价
/// - `volume`: 成交量
/// - `trend_length`: 趋势周期（默认 14）
/// - `confirmation_threshold`: 确认阈值（默认 2.0）
/// - `momentum_window`: 动量窗口（默认 10）
///
/// # 返回
/// - (signals, stop_loss, take_profit) 元组
///   - signals: 1.0=买入, -1.0=卖出, 0.0=无信号
///   - stop_loss: 止损位
///   - take_profit: 止盈位
pub fn atr2_signals(
    high: &[f64],
    low: &[f64],
    close: &[f64],
    volume: &[f64],
    trend_length: usize,
    confirmation_threshold: f64,
    momentum_window: usize,
) -> (Vec<f64>, Vec<f64>, Vec<f64>) {
    let len = close.len();
    
    // 1. 计算 ATR
    let atr_values = atr(high, low, close, trend_length);
    
    // 2. 计算动量
    let mut momentum = vec![f64::NAN; len];
    for i in momentum_window..len {
        momentum[i] = close[i] - close[i - momentum_window];
    }
    
    // 3. 计算成交量均线
    let volume_ma = sma(volume, trend_length);
    
    // 4. 生成信号
    let mut signals = vec![0.0; len];
    let mut stop_loss = vec![f64::NAN; len];
    let mut take_profit = vec![f64::NAN; len];
    
    for i in trend_length..len {
        if !atr_values[i].is_nan() && !momentum[i].is_nan() {
            let normalized_momentum = if atr_values[i] != 0.0 {
                momentum[i] / atr_values[i]
            } else {
                0.0
            };
            
            // 成交量过滤
            let volume_confirmed = if !volume_ma[i].is_nan() {
                volume[i] > volume_ma[i]
            } else {
                true
            };
            
            // 买入信号
            if normalized_momentum < -confirmation_threshold && volume_confirmed {
                signals[i] = 1.0;
                stop_loss[i] = close[i] - 2.0 * atr_values[i];
                take_profit[i] = close[i] + 3.0 * atr_values[i];
            }
            // 卖出信号
            else if normalized_momentum > confirmation_threshold && volume_confirmed {
                signals[i] = -1.0;
                stop_loss[i] = close[i] + 2.0 * atr_values[i];
                take_profit[i] = close[i] - 3.0 * atr_values[i];
            }
        }
    }
    
    (signals, stop_loss, take_profit)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_ai_supertrend() {
        let high = vec![110.0, 112.0, 115.0, 113.0, 116.0, 118.0, 120.0, 119.0, 121.0, 123.0];
        let low = vec![100.0, 102.0, 103.0, 104.0, 105.0, 106.0, 107.0, 108.0, 109.0, 110.0];
        let close = vec![105.0, 107.0, 110.0, 108.0, 112.0, 115.0, 117.0, 116.0, 118.0, 120.0];

        let (st, dir) = ai_supertrend(&high, &low, &close, 3, 5, 3, 3, 3, 2.0);

        assert_eq!(st.len(), close.len());
        assert_eq!(dir.len(), close.len());
    }

    #[test]
    fn test_ai_momentum_index() {
        let close = vec![100.0, 102.0, 101.0, 103.0, 105.0, 104.0, 106.0, 108.0, 107.0, 109.0,
                         110.0, 112.0, 111.0, 113.0, 115.0, 114.0, 116.0, 118.0, 117.0, 119.0];

        let (pred, pred_ma) = ai_momentum_index(&close, 10, 14, 3);

        assert_eq!(pred.len(), close.len());
        assert_eq!(pred_ma.len(), close.len());
    }

    #[test]
    fn test_dynamic_macd() {
        let open = vec![100.0, 102.0, 101.0, 103.0, 105.0];
        let high = vec![105.0, 107.0, 106.0, 108.0, 110.0];
        let low = vec![99.0, 101.0, 100.0, 102.0, 104.0];
        let close = vec![103.0, 105.0, 104.0, 106.0, 108.0];

        let (macd, _signal, _hist, ha_o, ha_c) = dynamic_macd(&open, &high, &low, &close, 3, 5, 3);

        assert_eq!(macd.len(), close.len());
        assert_eq!(ha_o.len(), close.len());
        assert_eq!(ha_c.len(), close.len());
    }
}
