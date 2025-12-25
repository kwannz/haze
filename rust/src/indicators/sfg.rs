// indicators/sfg.rs - SFG 交易信号指标
//
// 基于系统指标实现的高级复合交易信号
// 参考：SFG_交易信号指标.pdf

use crate::indicators::{supertrend, atr};
use crate::utils::{wma, sma};

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
    let optimized_st = st_values.clone();
    let mut optimized_dir = st_direction.clone();
    
    if len > n + k {
        for i in n..len {
            // 提取当前窗口的特征
            let current_price_trend = if !price_wma[i].is_nan() { price_wma[i] } else { close[i] };
            let current_st_trend = if !st_wma[i].is_nan() { st_wma[i] } else { st_values[i] };
            
            // KNN: 找到最相似的 k 个历史点
            let mut distances: Vec<(usize, f64)> = Vec::new();
            
            for j in (k..(i - k)).step_by(1) {
                if !price_wma[j].is_nan() && !st_wma[j].is_nan() {
                    // 计算欧氏距离
                    let price_diff = (current_price_trend - price_wma[j]).powi(2);
                    let st_diff = (current_st_trend - st_wma[j]).powi(2);
                    let distance = (price_diff + st_diff).sqrt();
                    
                    distances.push((j, distance));
                }
            }
            
            // 排序找到最近的 k 个邻居
            distances.sort_by(|a, b| a.1.partial_cmp(&b.1).unwrap());
            
            if distances.len() >= k {
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
    if len > k + trend_length {
        for i in (k + trend_length)..len {
            let current_rsi = if !rsi[i].is_nan() { rsi[i] } else { 50.0 };
            let current_price = close[i];
            
            // 找到相似的历史点
            let mut distances: Vec<(usize, f64)> = Vec::new();
            
            for j in trend_length..(i - trend_length) {
                if !rsi[j].is_nan() {
                    // 计算特征距离
                    let rsi_diff = (current_rsi - rsi[j]).powi(2);
                    let price_ratio = if close[j] != 0.0 {
                        ((current_price / close[j]) - 1.0).powi(2)
                    } else {
                        0.0
                    };
                    
                    let distance = (rsi_diff + price_ratio * 100.0).sqrt();
                    distances.push((j, distance));
                }
            }
            
            // 排序找邻居
            distances.sort_by(|a, b| a.1.partial_cmp(&b.1).unwrap());
            
            if distances.len() >= k {
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
