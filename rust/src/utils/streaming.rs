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

// ==================== 边界条件测试 ====================

#[cfg(test)]
mod boundary_tests {
    use super::*;

    // ==================== OnlineSMA 边界测试 ====================

    #[test]
    fn test_online_sma_period_one() {
        let mut sma = OnlineSMA::new(1);
        // Period=1 means immediate output
        assert_eq!(sma.update(5.0), Some(5.0));
        assert_eq!(sma.update(10.0), Some(10.0));
        assert_eq!(sma.update(3.0), Some(3.0));
    }

    #[test]
    fn test_online_sma_nan_input() {
        let mut sma = OnlineSMA::new(3);
        sma.update(1.0);
        sma.update(2.0);
        // NaN input should return None and not corrupt state
        assert_eq!(sma.update(f64::NAN), None);
        // Normal value should still work
        assert_eq!(sma.update(3.0), Some(2.0)); // (1+2+3)/3
    }

    #[test]
    fn test_online_sma_reset() {
        let mut sma = OnlineSMA::new(3);
        sma.update(1.0);
        sma.update(2.0);
        sma.update(3.0);
        assert_eq!(sma.len(), 3);

        sma.reset();
        assert!(sma.is_empty());
        assert_eq!(sma.len(), 0);

        // After reset, should behave like new
        assert_eq!(sma.update(10.0), None);
        assert_eq!(sma.update(20.0), None);
        assert_eq!(sma.update(30.0), Some(20.0));
    }

    #[test]
    fn test_online_sma_len_and_is_empty() {
        let mut sma = OnlineSMA::new(5);
        assert!(sma.is_empty());
        assert_eq!(sma.len(), 0);

        sma.update(1.0);
        assert!(!sma.is_empty());
        assert_eq!(sma.len(), 1);

        sma.update(2.0);
        sma.update(3.0);
        assert_eq!(sma.len(), 3);

        // After warmup complete
        sma.update(4.0);
        sma.update(5.0);
        assert_eq!(sma.len(), 5);

        // After window slides
        sma.update(6.0);
        assert_eq!(sma.len(), 5); // Still 5 (window size)
    }

    #[test]
    fn test_online_sma_constant_values() {
        let mut sma = OnlineSMA::new(5);
        for _ in 0..10 {
            let result = sma.update(100.0);
            if let Some(val) = result {
                assert!((val - 100.0).abs() < 1e-10);
            }
        }
    }

    #[test]
    fn test_online_sma_force_recalculate_before_ready() {
        let mut sma = OnlineSMA::new(5);
        sma.update(1.0);
        sma.update(2.0);
        // Force recalculate when not yet ready - should be safe
        sma.force_recalculate();
        sma.update(3.0);
        sma.update(4.0);
        assert_eq!(sma.update(5.0), Some(3.0)); // (1+2+3+4+5)/5
    }

    #[test]
    fn test_online_sma_large_values() {
        let mut sma = OnlineSMA::new(3);
        sma.update(1e15);
        sma.update(2e15);
        let result = sma.update(3e15).unwrap();
        assert!((result - 2e15).abs() < 1e5);
    }

    #[test]
    fn test_online_sma_small_values() {
        let mut sma = OnlineSMA::new(3);
        sma.update(1e-15);
        sma.update(2e-15);
        let result = sma.update(3e-15).unwrap();
        assert!((result - 2e-15).abs() < 1e-25);
    }

    // ==================== OnlineEMA 边界测试 ====================

    #[test]
    fn test_online_ema_period_one() {
        let mut ema = OnlineEMA::new(1);
        // Period=1 means alpha=1, so EMA = latest value
        assert_eq!(ema.update(5.0), Some(5.0));
        assert_eq!(ema.update(10.0), Some(10.0));
        assert_eq!(ema.update(3.0), Some(3.0));
    }

    #[test]
    fn test_online_ema_nan_input_warmup() {
        let mut ema = OnlineEMA::new(3);
        ema.update(1.0);
        ema.update(2.0);
        // NaN during warmup should return current state (None)
        let result = ema.update(f64::NAN);
        assert!(result.is_none());
    }

    #[test]
    fn test_online_ema_nan_input_ready() {
        let mut ema = OnlineEMA::new(3);
        ema.update(1.0);
        ema.update(2.0);
        ema.update(3.0);
        let current = ema.current;

        // NaN input after ready should return current value unchanged
        let after_nan = ema.update(f64::NAN);
        assert_eq!(after_nan, current);
    }

    #[test]
    fn test_online_ema_reset() {
        let mut ema = OnlineEMA::new(3);
        ema.update(1.0);
        ema.update(2.0);
        ema.update(3.0);
        assert!(ema.is_ready());

        ema.reset();
        assert!(!ema.is_ready());

        // After reset, should behave like new
        assert_eq!(ema.update(10.0), None);
        assert_eq!(ema.update(20.0), None);
        let result = ema.update(30.0).unwrap();
        assert!((result - 20.0).abs() < 1e-10); // Initial EMA = SMA of warmup
    }

    #[test]
    fn test_online_ema_is_ready() {
        let mut ema = OnlineEMA::new(5);
        assert!(!ema.is_ready());

        for i in 1..5 {
            ema.update(i as f64);
            assert!(!ema.is_ready());
        }

        ema.update(5.0);
        assert!(ema.is_ready());
    }

    #[test]
    fn test_online_ema_constant_values() {
        let mut ema = OnlineEMA::new(5);
        for _ in 0..20 {
            let result = ema.update(100.0);
            if let Some(val) = result {
                assert!((val - 100.0).abs() < 1e-10);
            }
        }
    }

    #[test]
    fn test_online_ema_alpha_calculation() {
        // For period=10, alpha = 2/(10+1) = 0.1818...
        let ema = OnlineEMA::new(10);
        let expected_alpha = 2.0 / 11.0;
        assert!((ema.alpha - expected_alpha).abs() < 1e-10);
    }

    // ==================== OnlineRSI 边界测试 ====================

    #[test]
    fn test_online_rsi_all_gains() {
        let mut rsi = OnlineRSI::new(5);
        // First value establishes baseline
        rsi.update(100.0);
        // All subsequent values are gains
        for i in 1..10 {
            rsi.update(100.0 + i as f64);
        }
        let result = rsi.update(115.0).unwrap();
        assert!((result - 100.0).abs() < 1e-10); // All gains -> RSI = 100
    }

    #[test]
    fn test_online_rsi_all_losses() {
        let mut rsi = OnlineRSI::new(5);
        // First value establishes baseline
        rsi.update(100.0);
        // All subsequent values are losses
        for i in 1..10 {
            rsi.update(100.0 - i as f64);
        }
        let result = rsi.update(85.0).unwrap();
        assert!(result < 1.0); // All losses -> RSI ≈ 0
    }

    #[test]
    fn test_online_rsi_nan_input() {
        let mut rsi = OnlineRSI::new(5);
        for i in 0..10 {
            rsi.update(100.0 + (i as f64));
        }
        // NaN input should return None
        assert_eq!(rsi.update(f64::NAN), None);
        // Normal update should still work
        assert!(rsi.update(110.0).is_some());
    }

    #[test]
    fn test_online_rsi_reset() {
        let mut rsi = OnlineRSI::new(5);
        for i in 0..10 {
            rsi.update(100.0 + (i as f64));
        }
        assert!(rsi.update(110.0).is_some());

        rsi.reset();

        // After reset, need warmup again
        assert!(rsi.update(100.0).is_none());
        assert!(rsi.update(101.0).is_none());
    }

    #[test]
    fn test_online_rsi_flat_market() {
        let mut rsi = OnlineRSI::new(5);
        rsi.update(100.0);
        // Flat market - no change
        for _ in 0..10 {
            rsi.update(100.0);
        }
        // RSI should be 100 (avg_loss < 1e-10 in calc_rsi)
        let result = rsi.update(100.0).unwrap();
        assert!((result - 100.0).abs() < 1e-10);
    }

    #[test]
    fn test_online_rsi_oscillating() {
        let mut rsi = OnlineRSI::new(5);
        rsi.update(100.0);
        // Oscillating market
        for i in 0..20 {
            if i % 2 == 0 {
                rsi.update(101.0);
            } else {
                rsi.update(99.0);
            }
        }
        let result = rsi.update(100.0).unwrap();
        // Oscillating should give RSI around 50
        assert!(result > 30.0 && result < 70.0);
    }

    // ==================== OnlineATR 边界测试 ====================

    #[test]
    fn test_online_atr_nan_input() {
        let mut atr = OnlineATR::new(3);
        atr.update(102.0, 98.0, 100.0);
        atr.update(103.0, 99.0, 101.0);
        atr.update(104.0, 100.0, 102.0);

        let prev_atr = atr.atr;
        // NaN input should return current ATR unchanged
        let result = atr.update(f64::NAN, 101.0, 103.0);
        assert_eq!(result, prev_atr);

        // Test with NaN in different positions
        let result2 = atr.update(105.0, f64::NAN, 103.0);
        assert_eq!(result2, prev_atr);
    }

    #[test]
    fn test_online_atr_reset() {
        let mut atr = OnlineATR::new(3);
        atr.update(102.0, 98.0, 100.0);
        atr.update(103.0, 99.0, 101.0);
        atr.update(104.0, 100.0, 102.0);
        assert!(atr.is_ready());

        atr.reset();
        assert!(!atr.is_ready());

        // After reset, need warmup again
        assert!(atr.update(102.0, 98.0, 100.0).is_none());
    }

    #[test]
    fn test_online_atr_is_ready() {
        let mut atr = OnlineATR::new(3);
        assert!(!atr.is_ready());

        atr.update(102.0, 98.0, 100.0);
        assert!(!atr.is_ready());

        atr.update(103.0, 99.0, 101.0);
        assert!(!atr.is_ready());

        atr.update(104.0, 100.0, 102.0);
        assert!(atr.is_ready());
    }

    #[test]
    fn test_online_atr_first_tr_calculation() {
        let mut atr = OnlineATR::new(1);
        // First bar: TR = high - low (no previous close)
        let result = atr.update(105.0, 95.0, 100.0);
        // Period=1, so should be ready immediately
        assert!(result.is_some());
        assert!((result.unwrap() - 10.0).abs() < 1e-10); // 105-95=10
    }

    #[test]
    fn test_online_atr_gap_up() {
        let mut atr = OnlineATR::new(2);
        atr.update(102.0, 98.0, 100.0);
        // Gap up: close was 100, now low is 105
        let result = atr.update(110.0, 105.0, 108.0);
        // TR should be max of: 110-105=5, |110-100|=10, |105-100|=5 -> 10
        // ATR = (4 + 10)/2 = 7 (first TR was 4)
        assert!(result.is_some());
    }

    #[test]
    fn test_online_atr_gap_down() {
        let mut atr = OnlineATR::new(2);
        atr.update(102.0, 98.0, 100.0);
        // Gap down: close was 100, now high is 95
        let result = atr.update(95.0, 90.0, 92.0);
        // TR should be max of: 95-90=5, |95-100|=5, |90-100|=10 -> 10
        assert!(result.is_some());
    }

    // ==================== OnlineMACD 边界测试 ====================

    #[test]
    fn test_online_macd_reset() {
        let mut macd = OnlineMACD::new(12, 26, 9);
        for i in 0..50 {
            macd.update(100.0 + (i as f64) * 0.5);
        }
        assert!(macd.update(125.0).is_some());

        macd.reset();

        // After reset, need full warmup again
        for _ in 0..35 {
            assert!(macd.update(100.0).is_none());
        }
    }

    #[test]
    fn test_online_macd_small_periods() {
        let mut macd = OnlineMACD::new(2, 3, 2);
        // With small periods, should be ready faster
        macd.update(100.0);
        macd.update(101.0);
        macd.update(102.0);
        // After 3 values: fast EMA ready (period=2 needs 2)
        // slow EMA ready (period=3 needs 3), signal needs 2 more
        macd.update(103.0);
        let result = macd.update(104.0);
        assert!(result.is_some());
    }

    #[test]
    fn test_online_macd_trending_market() {
        let mut macd = OnlineMACD::new(12, 26, 9);
        // Strong uptrend
        for i in 0..60 {
            macd.update(100.0 + (i as f64) * 2.0);
        }
        let (macd_line, _signal, _histogram) = macd.update(220.0).unwrap();
        // In uptrend: fast EMA > slow EMA -> positive MACD
        assert!(macd_line > 0.0);
    }

    #[test]
    fn test_online_macd_downtrend() {
        let mut macd = OnlineMACD::new(12, 26, 9);
        // Strong downtrend
        for i in 0..60 {
            macd.update(200.0 - (i as f64) * 2.0);
        }
        let (macd_line, _signal, _histogram) = macd.update(80.0).unwrap();
        // In downtrend: fast EMA < slow EMA -> negative MACD
        assert!(macd_line < 0.0);
    }

    // ==================== OnlineBollingerBands 边界测试 ====================

    #[test]
    fn test_online_bollinger_nan_input() {
        let mut bb = OnlineBollingerBands::new(5, 2.0);
        for i in 0..5 {
            bb.update(100.0 + (i as f64));
        }

        // NaN input should return None
        assert!(bb.update(f64::NAN).is_none());

        // Normal update should still work
        assert!(bb.update(105.0).is_some());
    }

    #[test]
    fn test_online_bollinger_reset() {
        let mut bb = OnlineBollingerBands::new(5, 2.0);
        for i in 0..10 {
            bb.update(100.0 + (i as f64));
        }

        bb.reset();
        assert!(bb.window.is_empty());

        // After reset, need warmup again
        for _ in 0..4 {
            assert!(bb.update(100.0).is_none());
        }
        assert!(bb.update(100.0).is_some());
    }

    #[test]
    fn test_online_bollinger_constant_values() {
        let mut bb = OnlineBollingerBands::new(5, 2.0);
        for _ in 0..10 {
            bb.update(100.0);
        }
        let (mid, upper, lower) = bb.update(100.0).unwrap();
        // Constant values -> zero std dev
        assert!((mid - 100.0).abs() < 1e-10);
        assert!((upper - 100.0).abs() < 1e-10);
        assert!((lower - 100.0).abs() < 1e-10);
    }

    #[test]
    fn test_online_bollinger_different_std_devs() {
        let mut bb1 = OnlineBollingerBands::new(5, 1.0);
        let mut bb2 = OnlineBollingerBands::new(5, 2.0);
        let mut bb3 = OnlineBollingerBands::new(5, 3.0);

        let values = vec![100.0, 102.0, 98.0, 101.0, 99.0, 103.0];
        for &val in &values {
            bb1.update(val);
            bb2.update(val);
            bb3.update(val);
        }

        let (mid1, upper1, lower1) = bb1.update(100.0).unwrap();
        let (mid2, upper2, lower2) = bb2.update(100.0).unwrap();
        let (mid3, upper3, lower3) = bb3.update(100.0).unwrap();

        // All should have same middle
        assert!((mid1 - mid2).abs() < 1e-10);
        assert!((mid2 - mid3).abs() < 1e-10);

        // Wider bands for higher std_dev
        assert!(upper3 > upper2);
        assert!(upper2 > upper1);
        assert!(lower3 < lower2);
        assert!(lower2 < lower1);
    }

    #[test]
    fn test_online_bollinger_period_one() {
        let mut bb = OnlineBollingerBands::new(1, 2.0);
        // Period=1 means single value, std=0
        let (mid, upper, lower) = bb.update(100.0).unwrap();
        assert!((mid - 100.0).abs() < 1e-10);
        assert!((upper - 100.0).abs() < 1e-10);
        assert!((lower - 100.0).abs() < 1e-10);
    }

    #[test]
    fn test_online_bollinger_volatile_market() {
        let mut bb = OnlineBollingerBands::new(5, 2.0);
        // Highly volatile data
        let values = vec![100.0, 120.0, 80.0, 130.0, 70.0, 110.0];
        for &val in &values {
            bb.update(val);
        }
        let (_mid, upper, lower) = bb.update(100.0).unwrap();
        // High volatility should give wide bands
        let band_width = upper - lower;
        assert!(band_width > 40.0); // Should be quite wide
    }

    // ==================== 集成测试 ====================

    #[test]
    fn test_all_calculators_with_infinity() {
        let mut sma = OnlineSMA::new(3);
        let mut ema = OnlineEMA::new(3);

        // Test with infinity
        sma.update(1.0);
        sma.update(2.0);
        let sma_result = sma.update(f64::INFINITY);
        // Infinity is not NaN, so it will be used
        assert!(sma_result.is_some());
        assert!(sma_result.unwrap().is_infinite());

        ema.update(1.0);
        ema.update(2.0);
        ema.update(3.0);
        let ema_result = ema.update(f64::INFINITY);
        assert!(ema_result.is_some());
        assert!(ema_result.unwrap().is_infinite());
    }

    #[test]
    fn test_all_calculators_negative_values() {
        let mut sma = OnlineSMA::new(3);
        let mut ema = OnlineEMA::new(3);
        let mut rsi = OnlineRSI::new(3);
        let mut bb = OnlineBollingerBands::new(3, 2.0);

        // Negative values should work fine
        sma.update(-100.0);
        sma.update(-200.0);
        let sma_result = sma.update(-300.0).unwrap();
        assert!((sma_result - (-200.0)).abs() < 1e-10);

        ema.update(-100.0);
        ema.update(-200.0);
        let ema_result = ema.update(-300.0).unwrap();
        assert!(ema_result < 0.0);

        rsi.update(-100.0);
        rsi.update(-110.0);
        rsi.update(-120.0);
        let rsi_result = rsi.update(-130.0);
        assert!(rsi_result.is_some());
        assert!(rsi_result.unwrap() < 50.0); // All losses

        bb.update(-100.0);
        bb.update(-200.0);
        let bb_result = bb.update(-300.0).unwrap();
        let (mid, upper, lower) = bb_result;
        assert!(mid < 0.0);
        assert!(upper > lower);
    }

    #[test]
    fn test_clone_independence() {
        let mut sma1 = OnlineSMA::new(3);
        sma1.update(1.0);
        sma1.update(2.0);

        let mut sma2 = sma1.clone();

        sma1.update(3.0);
        sma2.update(6.0);

        let result1 = sma1.update(4.0).unwrap();
        let result2 = sma2.update(9.0).unwrap();

        // They should be independent
        assert!((result1 - 3.0).abs() < 1e-10); // (2+3+4)/3
        assert!((result2 - 5.666666666666667).abs() < 1e-10); // (2+6+9)/3
    }
}
