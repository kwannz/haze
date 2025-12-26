//! Streaming/Online Calculation Module
//!
//! # Overview
//! This module provides incremental (online) indicator calculators that maintain
//! internal state and update with O(1) time complexity per data point. These are
//! essential for real-time trading systems where recalculating entire histories
//! on each tick is impractical.
//!
//! # Design Philosophy
//! - **State Machine Pattern**: Each calculator encapsulates its warmup and running state
//! - **Numerical Stability**: Periodic recalculation prevents floating-point error accumulation
//! - **Zero Allocation**: Updates allocate no memory after initialization
//! - **NaN Safety**: Invalid inputs are handled gracefully without corrupting state
//!
//! # Available Calculators
//!
//! ## Moving Averages
//! - [`OnlineSMA`] - Simple Moving Average with O(1) updates
//! - [`OnlineEMA`] - Exponential Moving Average with warmup handling
//!
//! ## Momentum Indicators
//! - [`OnlineRSI`] - Relative Strength Index with Wilder's smoothing
//! - [`OnlineMACD`] - MACD with signal line and histogram
//!
//! ## Volatility Indicators
//! - [`OnlineATR`] - Average True Range for OHLC data
//! - [`OnlineBollingerBands`] - Bollinger Bands with configurable std dev
//!
//! # Examples
//! ```rust
//! use haze_library::utils::streaming::{OnlineSMA, OnlineEMA, OnlineRSI};
//!
//! let prices = vec![100.0, 101.0, 102.0, 103.0, 104.0, 105.0];
//!
//! // Real-time SMA calculation
//! let mut sma = OnlineSMA::new(20);
//! for price in prices.iter() {
//!     if let Some(value) = sma.update(*price) {
//!         println!("SMA(20): {}", value);
//!     }
//! }
//!
//! // Online RSI for momentum tracking
//! let mut rsi = OnlineRSI::new(14);
//! for price in prices.iter() {
//!     if let Some(value) = rsi.update(*price) {
//!         if value > 70.0 { println!("Overbought!"); }
//!         if value < 30.0 { println!("Oversold!"); }
//!     }
//! }
//! ```
//!
//! # Performance Characteristics
//! - All update operations are O(1) time complexity
//! - Memory usage is O(period) for window-based calculators
//! - OnlineSMA/OnlineBollingerBands recalculate every 1000 updates for numerical stability
//! - Warmup period returns None until sufficient data is accumulated
//!
//! # Cross-References
//! - [`crate::utils::ma`] - Batch moving average implementations
//! - [`crate::indicators::momentum`] - Batch momentum indicators
//! - [`crate::indicators::volatility`] - Batch volatility indicators

// utils/streaming.rs - 流式/在线计算模块
#![allow(dead_code)]
//
// 提供增量更新的指标计算，适用于实时交易系统
// 遵循 KISS 原则：简单状态机设计

use std::collections::VecDeque;

/// 在线 SMA 计算器
///
/// 支持增量更新，O(1) 时间复杂度
/// 使用定期重新计算以防止浮点误差累积
#[derive(Debug, Clone)]
pub struct OnlineSMA {
    period: usize,
    window: VecDeque<f64>,
    sum: f64,
    /// 自上次完整重新计算以来的更新次数
    updates_since_recalc: usize,
}

/// 重新计算间隔：每 1000 次更新重新计算一次以重置累积误差
const SMA_RECALC_INTERVAL: usize = 1000;

impl OnlineSMA {
    pub fn new(period: usize) -> Self {
        Self {
            period,
            window: VecDeque::with_capacity(period),
            sum: 0.0,
            updates_since_recalc: 0,
        }
    }

    /// 添加新值并返回当前 SMA
    pub fn update(&mut self, value: f64) -> Option<f64> {
        if value.is_nan() {
            return None;
        }

        self.window.push_back(value);
        self.sum += value;

        if self.window.len() > self.period {
            if let Some(old) = self.window.pop_front() {
                self.sum -= old;
            }
            self.updates_since_recalc += 1;

            // 定期完整重新计算以消除累积浮点误差
            if self.updates_since_recalc >= SMA_RECALC_INTERVAL {
                self.recalculate_sum();
            }
        }

        if self.window.len() == self.period {
            Some(self.sum / self.period as f64)
        } else {
            None
        }
    }

    /// 完整重新计算窗口和以消除累积浮点误差
    fn recalculate_sum(&mut self) {
        self.sum = self.window.iter().sum();
        self.updates_since_recalc = 0;
    }

    /// 重置状态
    pub fn reset(&mut self) {
        self.window.clear();
        self.sum = 0.0;
        self.updates_since_recalc = 0;
    }

    /// 当前窗口大小
    pub fn len(&self) -> usize {
        self.window.len()
    }

    pub fn is_empty(&self) -> bool {
        self.window.is_empty()
    }

    /// 强制重新计算和以消除累积误差（用于关键计算点）
    pub fn force_recalculate(&mut self) {
        if self.window.len() == self.period {
            self.recalculate_sum();
        }
    }
}

/// 在线 EMA 计算器
///
/// 支持增量更新，O(1) 时间复杂度
#[derive(Debug, Clone)]
pub struct OnlineEMA {
    period: usize,
    alpha: f64,
    current: Option<f64>,
    warmup_count: usize,
    warmup_sum: f64,
}

impl OnlineEMA {
    pub fn new(period: usize) -> Self {
        Self {
            period,
            alpha: 2.0 / (period as f64 + 1.0),
            current: None,
            warmup_count: 0,
            warmup_sum: 0.0,
        }
    }

    /// 添加新值并返回当前 EMA
    pub fn update(&mut self, value: f64) -> Option<f64> {
        if value.is_nan() {
            return self.current;
        }

        match self.current {
            None => {
                self.warmup_count += 1;
                self.warmup_sum += value;
                if self.warmup_count == self.period {
                    self.current = Some(self.warmup_sum / self.period as f64);
                }
                self.current
            }
            Some(prev) => {
                let new_ema = self.alpha * value + (1.0 - self.alpha) * prev;
                self.current = Some(new_ema);
                self.current
            }
        }
    }

    /// 重置状态
    pub fn reset(&mut self) {
        self.current = None;
        self.warmup_count = 0;
        self.warmup_sum = 0.0;
    }

    /// 是否完成预热
    pub fn is_ready(&self) -> bool {
        self.current.is_some()
    }
}

/// 在线 RSI 计算器
#[derive(Debug, Clone)]
pub struct OnlineRSI {
    period: usize,
    alpha: f64,
    prev_value: Option<f64>,
    avg_gain: Option<f64>,
    avg_loss: Option<f64>,
    warmup_gains: Vec<f64>,
    warmup_losses: Vec<f64>,
}

impl OnlineRSI {
    pub fn new(period: usize) -> Self {
        Self {
            period,
            alpha: 1.0 / period as f64,
            prev_value: None,
            avg_gain: None,
            avg_loss: None,
            warmup_gains: Vec::with_capacity(period),
            warmup_losses: Vec::with_capacity(period),
        }
    }

    pub fn update(&mut self, value: f64) -> Option<f64> {
        if value.is_nan() {
            return None;
        }

        let prev = match self.prev_value {
            Some(p) => p,
            None => {
                self.prev_value = Some(value);
                return None;
            }
        };

        let change = value - prev;
        self.prev_value = Some(value);

        let gain = if change > 0.0 { change } else { 0.0 };
        let loss = if change < 0.0 { -change } else { 0.0 };

        match (self.avg_gain, self.avg_loss) {
            (None, None) => {
                self.warmup_gains.push(gain);
                self.warmup_losses.push(loss);

                if self.warmup_gains.len() == self.period {
                    let avg_g: f64 = self.warmup_gains.iter().sum::<f64>() / self.period as f64;
                    let avg_l: f64 = self.warmup_losses.iter().sum::<f64>() / self.period as f64;
                    self.avg_gain = Some(avg_g);
                    self.avg_loss = Some(avg_l);
                    Some(Self::calc_rsi(avg_g, avg_l))
                } else {
                    None
                }
            }
            (Some(ag), Some(al)) => {
                let new_avg_gain = (ag * (self.period - 1) as f64 + gain) / self.period as f64;
                let new_avg_loss = (al * (self.period - 1) as f64 + loss) / self.period as f64;
                self.avg_gain = Some(new_avg_gain);
                self.avg_loss = Some(new_avg_loss);
                Some(Self::calc_rsi(new_avg_gain, new_avg_loss))
            }
            _ => None,
        }
    }

    fn calc_rsi(avg_gain: f64, avg_loss: f64) -> f64 {
        if avg_loss < 1e-10 {
            100.0
        } else {
            100.0 - 100.0 / (1.0 + avg_gain / avg_loss)
        }
    }

    pub fn reset(&mut self) {
        self.prev_value = None;
        self.avg_gain = None;
        self.avg_loss = None;
        self.warmup_gains.clear();
        self.warmup_losses.clear();
    }
}

/// 在线 ATR 计算器
#[derive(Debug, Clone)]
pub struct OnlineATR {
    period: usize,
    prev_close: Option<f64>,
    atr: Option<f64>,
    warmup_tr: Vec<f64>,
}

impl OnlineATR {
    pub fn new(period: usize) -> Self {
        Self {
            period,
            prev_close: None,
            atr: None,
            warmup_tr: Vec::with_capacity(period),
        }
    }

    /// 更新并返回当前 ATR
    pub fn update(&mut self, high: f64, low: f64, close: f64) -> Option<f64> {
        if high.is_nan() || low.is_nan() || close.is_nan() {
            return self.atr;
        }

        let tr = match self.prev_close {
            Some(pc) => {
                let hl = high - low;
                let hc = (high - pc).abs();
                let lc = (low - pc).abs();
                hl.max(hc).max(lc)
            }
            None => high - low,
        };
        self.prev_close = Some(close);

        match self.atr {
            None => {
                self.warmup_tr.push(tr);
                if self.warmup_tr.len() == self.period {
                    let avg: f64 = self.warmup_tr.iter().sum::<f64>() / self.period as f64;
                    self.atr = Some(avg);
                }
                self.atr
            }
            Some(prev_atr) => {
                // RMA 更新
                let new_atr = (prev_atr * (self.period - 1) as f64 + tr) / self.period as f64;
                self.atr = Some(new_atr);
                self.atr
            }
        }
    }

    pub fn reset(&mut self) {
        self.prev_close = None;
        self.atr = None;
        self.warmup_tr.clear();
    }

    pub fn is_ready(&self) -> bool {
        self.atr.is_some()
    }
}

/// 在线 MACD 计算器
#[derive(Debug, Clone)]
pub struct OnlineMACD {
    fast_ema: OnlineEMA,
    slow_ema: OnlineEMA,
    signal_ema: OnlineEMA,
}

impl OnlineMACD {
    pub fn new(fast: usize, slow: usize, signal: usize) -> Self {
        Self {
            fast_ema: OnlineEMA::new(fast),
            slow_ema: OnlineEMA::new(slow),
            signal_ema: OnlineEMA::new(signal),
        }
    }

    /// 返回 (MACD, Signal, Histogram)
    pub fn update(&mut self, value: f64) -> Option<(f64, f64, f64)> {
        let fast = self.fast_ema.update(value)?;
        let slow = self.slow_ema.update(value)?;
        let macd = fast - slow;
        let signal = self.signal_ema.update(macd)?;
        let histogram = macd - signal;
        Some((macd, signal, histogram))
    }

    pub fn reset(&mut self) {
        self.fast_ema.reset();
        self.slow_ema.reset();
        self.signal_ema.reset();
    }
}

/// 在线 Bollinger Bands 计算器
///
/// 使用定期重新计算以防止浮点误差累积
#[derive(Debug, Clone)]
pub struct OnlineBollingerBands {
    period: usize,
    std_dev: f64,
    window: VecDeque<f64>,
    sum: f64,
    sum_sq: f64,
    /// 自上次完整重新计算以来的更新次数
    updates_since_recalc: usize,
}

/// 重新计算间隔：每 1000 次更新重新计算一次以重置累积误差
const BB_RECALC_INTERVAL: usize = 1000;

impl OnlineBollingerBands {
    pub fn new(period: usize, std_dev: f64) -> Self {
        Self {
            period,
            std_dev,
            window: VecDeque::with_capacity(period),
            sum: 0.0,
            sum_sq: 0.0,
            updates_since_recalc: 0,
        }
    }

    /// 返回 (Middle, Upper, Lower)
    pub fn update(&mut self, value: f64) -> Option<(f64, f64, f64)> {
        if value.is_nan() {
            return None;
        }

        self.window.push_back(value);
        self.sum += value;
        self.sum_sq += value * value;

        if self.window.len() > self.period {
            if let Some(old) = self.window.pop_front() {
                self.sum -= old;
                self.sum_sq -= old * old;
            }
            self.updates_since_recalc += 1;

            // 定期完整重新计算以消除累积浮点误差
            if self.updates_since_recalc >= BB_RECALC_INTERVAL {
                self.recalculate_sums();
            }
        }

        if self.window.len() == self.period {
            let mean = self.sum / self.period as f64;
            let variance = self.sum_sq / self.period as f64 - mean * mean;
            let std = variance.max(0.0).sqrt();
            let upper = mean + self.std_dev * std;
            let lower = mean - self.std_dev * std;
            Some((mean, upper, lower))
        } else {
            None
        }
    }

    /// 完整重新计算窗口和以消除累积浮点误差
    fn recalculate_sums(&mut self) {
        self.sum = self.window.iter().sum();
        self.sum_sq = self.window.iter().map(|&x| x * x).sum();
        self.updates_since_recalc = 0;
    }

    pub fn reset(&mut self) {
        self.window.clear();
        self.sum = 0.0;
        self.sum_sq = 0.0;
        self.updates_since_recalc = 0;
    }

    /// 强制重新计算和以消除累积误差（用于关键计算点）
    pub fn force_recalculate(&mut self) {
        if self.window.len() == self.period {
            self.recalculate_sums();
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_online_sma() {
        let mut sma = OnlineSMA::new(3);
        assert_eq!(sma.update(1.0), None);
        assert_eq!(sma.update(2.0), None);
        assert_eq!(sma.update(3.0), Some(2.0));
        assert_eq!(sma.update(4.0), Some(3.0));
        assert_eq!(sma.update(5.0), Some(4.0));
    }

    #[test]
    fn test_online_ema() {
        let mut ema = OnlineEMA::new(3);
        assert_eq!(ema.update(1.0), None);
        assert_eq!(ema.update(2.0), None);
        let first = ema.update(3.0).unwrap();
        assert!((first - 2.0).abs() < 1e-10);
        assert!(ema.is_ready());
    }

    #[test]
    fn test_online_rsi() {
        let mut rsi = OnlineRSI::new(14);
        for i in 0..20 {
            let val = 100.0 + (i as f64);
            rsi.update(val);
        }
        // 持续上涨，RSI 应该接近 100
        let result = rsi.update(120.0).unwrap();
        assert!(result > 90.0);
    }

    #[test]
    fn test_online_atr() {
        let mut atr = OnlineATR::new(3);
        assert!(atr.update(102.0, 98.0, 100.0).is_none());
        assert!(atr.update(103.0, 99.0, 101.0).is_none());
        let result = atr.update(104.0, 100.0, 102.0);
        assert!(result.is_some());
        assert!(atr.is_ready());
    }

    #[test]
    fn test_online_macd() {
        let mut macd = OnlineMACD::new(12, 26, 9);
        // MACD 需要 slow_period (26) + signal_period (9) = 35+ 个数据点
        for i in 0..50 {
            let val = 100.0 + (i as f64) * 0.5;
            macd.update(val);
        }
        let result = macd.update(125.0);
        assert!(result.is_some());
    }

    #[test]
    fn test_online_bollinger() {
        let mut bb = OnlineBollingerBands::new(20, 2.0);
        for i in 0..25 {
            let val = 100.0 + ((i % 5) as f64);
            bb.update(val);
        }
        let (mid, upper, lower) = bb.update(102.0).unwrap();
        assert!(upper > mid);
        assert!(mid > lower);
    }
}

// ==================== 浮点误差校准测试 ====================

#[cfg(test)]
mod floating_point_error_tests {
    use super::*;

    /// 测试 OnlineSMA 在大量更新后的数值精度
    #[test]
    fn test_online_sma_large_update_precision() {
        const N: usize = 100_000;
        const PERIOD: usize = 20;

        let mut sma = OnlineSMA::new(PERIOD);

        // 收集所有值以便验证
        let values: Vec<f64> = (0..N)
            .map(|i| 1000.0 + (i as f64) * 0.001 + 0.0001 * ((i * 7) % 11) as f64)
            .collect();

        let mut last_result = None;
        for &val in &values {
            last_result = sma.update(val);
        }

        // 计算期望的精确值
        let expected: f64 = values[N - PERIOD..N].iter().sum::<f64>() / PERIOD as f64;
        let actual = last_result.unwrap();

        let relative_error = (actual - expected).abs() / expected.abs();
        assert!(
            relative_error < 1e-10,
            "OnlineSMA 精度不足: expected={expected}, actual={actual}, relative_error={relative_error}",
        );
    }

    /// 测试 OnlineSMA 强制重新计算功能
    #[test]
    fn test_online_sma_force_recalculate() {
        const PERIOD: usize = 5;

        let mut sma = OnlineSMA::new(PERIOD);

        // 添加一些值
        for i in 0..PERIOD {
            sma.update(i as f64 + 0.1);
        }

        // 强制重新计算
        sma.force_recalculate();

        // 添加更多值并检查
        let result = sma.update(10.0).unwrap();
        let expected = (1.1 + 2.1 + 3.1 + 4.1 + 10.0) / 5.0;
        assert!((result - expected).abs() < 1e-10);
    }

    /// 测试 OnlineBollingerBands 在大量更新后的数值精度
    #[test]
    fn test_online_bollinger_large_update_precision() {
        const N: usize = 100_000;
        const PERIOD: usize = 20;

        let mut bb = OnlineBollingerBands::new(PERIOD, 2.0);

        // 收集所有值以便验证
        let values: Vec<f64> = (0..N).map(|i| 100.0 + (i as f64) * 0.001).collect();

        let mut last_result = None;
        for &val in &values {
            last_result = bb.update(val);
        }

        let (mid, upper, lower) = last_result.unwrap();

        // 计算期望的精确均值
        let expected_mean: f64 = values[N - PERIOD..N].iter().sum::<f64>() / PERIOD as f64;
        let relative_error = (mid - expected_mean).abs() / expected_mean.abs();

        assert!(
            relative_error < 1e-10,
            "OnlineBollingerBands 均值精度不足: expected={expected_mean}, actual={mid}, relative_error={relative_error}",
        );

        // 验证布林带结构正确
        assert!(upper > mid, "上轨应大于中轨");
        assert!(mid > lower, "中轨应大于下轨");
    }

    /// 测试 OnlineBollingerBands 强制重新计算功能
    #[test]
    fn test_online_bollinger_force_recalculate() {
        const PERIOD: usize = 5;

        let mut bb = OnlineBollingerBands::new(PERIOD, 2.0);

        // 添加一些值
        for i in 0..PERIOD {
            bb.update(100.0 + i as f64);
        }

        // 强制重新计算
        bb.force_recalculate();

        // 添加更多值并检查结构
        let (mid, upper, lower) = bb.update(110.0).unwrap();
        assert!(upper > mid);
        assert!(mid > lower);
    }

    /// 对比在线计算与批量计算的一致性
    #[test]
    fn test_online_vs_batch_consistency() {
        use crate::utils::ma::sma;

        const N: usize = 10_000;
        const PERIOD: usize = 20;

        let values: Vec<f64> = (0..N).map(|i| 50.0 + (i as f64).sin() * 10.0).collect();

        // 批量计算
        let batch_result = sma(&values, PERIOD).unwrap();

        // 在线计算
        let mut online_sma = OnlineSMA::new(PERIOD);
        let mut online_results = Vec::with_capacity(N);
        for &val in &values {
            online_results.push(online_sma.update(val));
        }

        // 比较有效结果
        for i in (PERIOD - 1)..N {
            let batch_val = batch_result[i];
            let online_val = online_results[i].unwrap();

            let diff = (batch_val - online_val).abs();
            assert!(
                diff < 1e-10,
                "索引 {i} 处在线与批量结果不一致: batch={batch_val}, online={online_val}, diff={diff}",
            );
        }
    }
}
