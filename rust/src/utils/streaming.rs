// utils/streaming.rs - 流式/在线计算模块
#![allow(dead_code)]
//
// 提供增量更新的指标计算，适用于实时交易系统
// 遵循 KISS 原则：简单状态机设计

use std::collections::VecDeque;

/// 在线 SMA 计算器
///
/// 支持增量更新，O(1) 时间复杂度
#[derive(Debug, Clone)]
pub struct OnlineSMA {
    period: usize,
    window: VecDeque<f64>,
    sum: f64,
}

impl OnlineSMA {
    pub fn new(period: usize) -> Self {
        Self {
            period,
            window: VecDeque::with_capacity(period),
            sum: 0.0,
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
        }

        if self.window.len() == self.period {
            Some(self.sum / self.period as f64)
        } else {
            None
        }
    }

    /// 重置状态
    pub fn reset(&mut self) {
        self.window.clear();
        self.sum = 0.0;
    }

    /// 当前窗口大小
    pub fn len(&self) -> usize {
        self.window.len()
    }

    pub fn is_empty(&self) -> bool {
        self.window.is_empty()
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
#[derive(Debug, Clone)]
pub struct OnlineBollingerBands {
    period: usize,
    std_dev: f64,
    window: VecDeque<f64>,
    sum: f64,
    sum_sq: f64,
}

impl OnlineBollingerBands {
    pub fn new(period: usize, std_dev: f64) -> Self {
        Self {
            period,
            std_dev,
            window: VecDeque::with_capacity(period),
            sum: 0.0,
            sum_sq: 0.0,
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

    pub fn reset(&mut self) {
        self.window.clear();
        self.sum = 0.0;
        self.sum_sq = 0.0;
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
