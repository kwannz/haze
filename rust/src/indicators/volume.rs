//! Volume Indicators Module
//!
//! # Overview
//! This module provides volume-based technical indicators that analyze trading
//! volume to confirm price trends, identify accumulation/distribution patterns,
//! and measure money flow. Volume indicators are essential for validating price
//! movements and detecting potential reversals.
//!
//! # Available Functions
//! - [`obv`] - On-Balance Volume (cumulative volume flow)
//! - [`volume_oscillator`] - Volume Oscillator (SMA ratio of volume)
//! - [`vwap`] - Volume Weighted Average Price (fair value benchmark)
//! - [`mfi`] - Money Flow Index (volume-weighted RSI, 0-100)
//! - [`cmf`] - Chaikin Money Flow (accumulation/distribution strength)
//! - [`volume_profile`] - Volume Profile (volume at price distribution)
//! - [`accumulation_distribution`] - A/D Line (cumulative money flow)
//! - [`price_volume_trend`] - PVT (price-weighted volume trend)
//! - [`negative_volume_index`] - NVI (smart money tracking)
//! - [`positive_volume_index`] - PVI (crowd behavior tracking)
//! - [`ease_of_movement`] - EOM (price movement efficiency)
//! - [`chaikin_ad_oscillator`] - ADOSC (A/D line momentum)
//!
//! # Examples
//! ```rust
//! use haze_library::indicators::volume::{obv, vwap, mfi};
//!
//! let n = 20;
//! let high: Vec<f64> = (0..n).map(|i| 110.0 + i as f64).collect();
//! let low: Vec<f64> = (0..n).map(|i| 100.0 + i as f64).collect();
//! let close: Vec<f64> = (0..n).map(|i| 105.0 + i as f64).collect();
//! let volume: Vec<f64> = (0..n).map(|i| 1000.0 + (i as f64) * 100.0).collect();
//!
//! // Calculate On-Balance Volume
//! let obv_values = obv(&close, &volume).unwrap();
//!
//! // Calculate VWAP (cumulative mode with period=0)
//! let vwap_values = vwap(&high, &low, &close, &volume, 0).unwrap();
//!
//! // Calculate Money Flow Index with 14-period
//! let mfi_values = mfi(&high, &low, &close, &volume, 14).unwrap();
//! ```
//!
//! # Performance Characteristics
//! - OBV: O(n) single pass cumulative calculation
//! - VWAP: O(n) with cumulative sum tracking
//! - MFI/CMF: O(n) with sliding window sums
//! - Volume Profile: O(n) with histogram binning
//!
//! # Volume Signal Interpretation
//! - OBV rising with price: Confirms uptrend
//! - MFI > 80: Overbought; MFI < 20: Oversold
//! - CMF > 0: Buying pressure; CMF < 0: Selling pressure
//! - NVI used when volume decreases (smart money)
//! - PVI used when volume increases (crowd behavior)
//!
//! # Cross-References
//! - [`crate::utils::ma`] - SMA/EMA for smoothing volume data
//! - [`crate::indicators::momentum`] - RSI-like calculations in MFI

#![allow(clippy::needless_range_loop)]

use crate::errors::validation::{validate_lengths_match, validate_not_empty, validate_period};
use crate::errors::HazeResult;
use crate::init_result;
use crate::utils::math::{is_not_zero, is_zero};
use crate::utils::{sma, vwap as vwap_util};

/// OBV - On-Balance Volume（能量潮）
///
/// 算法：
/// - 如果 close > prev_close：OBV = prev_OBV + volume
/// - 如果 close < prev_close：OBV = prev_OBV - volume
/// - 如果 close == prev_close：OBV = prev_OBV
///
/// 说明：
/// - 为了与 TA-Lib 的 `OBV` 行为对齐，初始值使用 `volume[0]`（而不是 0）。
///
/// # 参数
/// - `close`: 收盘价序列
/// - `volume`: 成交量序列
///
/// # 返回
/// - `HazeResult<Vec<f64>>`: OBV 累积值
///
/// # 错误
/// - `EmptyInput`: 输入为空
/// - `LengthMismatch`: close 和 volume 长度不匹配
pub fn obv(close: &[f64], volume: &[f64]) -> HazeResult<Vec<f64>> {
    validate_not_empty(close, "close")?;
    validate_lengths_match(&[(close, "close"), (volume, "volume")])?;

    let n = close.len();
    let mut result = vec![0.0; n];
    result[0] = volume[0];

    for i in 1..n {
        if close[i] > close[i - 1] {
            result[i] = result[i - 1] + volume[i];
        } else if close[i] < close[i - 1] {
            result[i] = result[i - 1] - volume[i];
        } else {
            result[i] = result[i - 1];
        }
    }

    Ok(result)
}

/// Volume Oscillator（成交量振荡器）
///
/// 算法：
/// VO = ((SMA(short) - SMA(long)) / SMA(long)) * 100
///
/// # 参数
/// - `volume`: 成交量序列
/// - `short_period`: 短周期（默认 5）
/// - `long_period`: 长周期（默认 10）
///
/// # 返回
/// - `HazeResult<Vec<f64>>`: VO 值
///
/// # 错误
/// - `EmptyInput`: 输入为空
/// - `InvalidPeriod`: 周期参数无效
pub fn volume_oscillator(
    volume: &[f64],
    short_period: usize,
    long_period: usize,
) -> HazeResult<Vec<f64>> {
    validate_not_empty(volume, "volume")?;

    let n = volume.len();
    let mut short = short_period;
    let mut long = long_period;

    // 自动交换确保 short < long
    if short > long {
        std::mem::swap(&mut short, &mut long);
    }

    // 验证周期
    validate_period(short, n)?;
    validate_period(long, n)?;

    let sma_short = sma(volume, short)?;
    let sma_long = sma(volume, long)?;

    let result = sma_short
        .iter()
        .zip(&sma_long)
        .map(|(&s, &l)| {
            if s.is_nan() || l.is_nan() || is_zero(l) {
                f64::NAN
            } else {
                ((s - l) / l) * 100.0
            }
        })
        .collect();

    Ok(result)
}

/// VWAP - Volume Weighted Average Price（成交量加权平均价）
///
/// 算法：VWAP = sum(typical_price * volume) / sum(volume)
///
/// # 参数
/// - `high`: 最高价序列
/// - `low`: 最低价序列
/// - `close`: 收盘价序列
/// - `volume`: 成交量序列
/// - `period`: 周期（0 = 累积 VWAP）
///
/// # 返回
/// - `HazeResult<Vec<f64>>`: VWAP 值
///
/// # 错误
/// - `EmptyInput`: 输入为空
/// - `LengthMismatch`: 数组长度不匹配
pub fn vwap(
    high: &[f64],
    low: &[f64],
    close: &[f64],
    volume: &[f64],
    period: usize,
) -> HazeResult<Vec<f64>> {
    validate_not_empty(high, "high")?;
    validate_lengths_match(&[
        (high, "high"),
        (low, "low"),
        (close, "close"),
        (volume, "volume"),
    ])?;

    let n = high.len();

    // 典型价格
    let typical_prices: Vec<f64> = (0..n)
        .map(|i| (high[i] + low[i] + close[i]) / 3.0)
        .collect();

    vwap_util(&typical_prices, volume, period)
}

/// MFI - Money Flow Index（资金流量指标）
///
/// 算法：
/// 1. Typical Price = (H + L + C) / 3
/// 2. Raw Money Flow = TP * volume
/// 3. Positive/Negative Money Flow（根据 TP 变化分类）
/// 4. Money Ratio = sum(Positive MF, period) / sum(Negative MF, period)
/// 5. MFI = 100 - (100 / (1 + Money Ratio))
///
/// # 参数
/// - `high`: 最高价序列
/// - `low`: 最低价序列
/// - `close`: 收盘价序列
/// - `volume`: 成交量序列
/// - `period`: 周期（默认 14）
///
/// # 返回
/// - `HazeResult<Vec<f64>>`: 0-100 的 MFI 值
///
/// # 错误
/// - `EmptyInput`: 输入为空
/// - `LengthMismatch`: 数组长度不匹配
/// - `InvalidPeriod`: 周期参数无效
pub fn mfi(
    high: &[f64],
    low: &[f64],
    close: &[f64],
    volume: &[f64],
    period: usize,
) -> HazeResult<Vec<f64>> {
    validate_not_empty(high, "high")?;
    validate_lengths_match(&[
        (high, "high"),
        (low, "low"),
        (close, "close"),
        (volume, "volume"),
    ])?;
    let n = high.len();
    validate_period(period, n)?;

    let mut positive_mf = vec![0.0; n];
    let mut negative_mf = vec![0.0; n];
    let mut prev_tp = (high[0] + low[0] + close[0]) / 3.0;

    for i in 1..n {
        let tp = (high[i] + low[i] + close[i]) / 3.0;
        let raw_money_flow = tp * volume[i];
        if tp > prev_tp {
            positive_mf[i] = raw_money_flow;
        } else if tp < prev_tp {
            negative_mf[i] = raw_money_flow;
        }
        prev_tp = tp;
    }

    let mut result = init_result!(n);
    let mut pos_sum: f64 = positive_mf[..period].iter().sum();
    let mut neg_sum: f64 = negative_mf[..period].iter().sum();

    result[period - 1] = if is_zero(neg_sum) {
        100.0
    } else {
        let money_ratio = pos_sum / neg_sum;
        100.0 - (100.0 / (1.0 + money_ratio))
    };

    for i in period..n {
        pos_sum += positive_mf[i] - positive_mf[i - period];
        neg_sum += negative_mf[i] - negative_mf[i - period];

        result[i] = if is_zero(neg_sum) {
            100.0
        } else {
            let money_ratio = pos_sum / neg_sum;
            100.0 - (100.0 / (1.0 + money_ratio))
        };
    }

    Ok(result)
}

/// CMF - Chaikin Money Flow（蔡金资金流量）
///
/// 算法：
/// 1. Money Flow Multiplier = ((C - L) - (H - C)) / (H - L)
/// 2. Money Flow Volume = MF Multiplier * Volume
/// 3. CMF = sum(MF Volume, period) / sum(Volume, period)
///
/// # 参数
/// - `high`: 最高价序列
/// - `low`: 最低价序列
/// - `close`: 收盘价序列
/// - `volume`: 成交量序列
/// - `period`: 周期（默认 20）
///
/// # 返回
/// - `HazeResult<Vec<f64>>`: -1 到 +1 之间的 CMF 值
///
/// # 错误
/// - `EmptyInput`: 输入为空
/// - `LengthMismatch`: 数组长度不匹配
/// - `InvalidPeriod`: 周期参数无效
pub fn cmf(
    high: &[f64],
    low: &[f64],
    close: &[f64],
    volume: &[f64],
    period: usize,
) -> HazeResult<Vec<f64>> {
    validate_not_empty(high, "high")?;
    validate_lengths_match(&[
        (high, "high"),
        (low, "low"),
        (close, "close"),
        (volume, "volume"),
    ])?;
    let n = high.len();
    validate_period(period, n)?;

    // Money Flow Multiplier
    let mf_multiplier: Vec<f64> = (0..n)
        .map(|i| {
            let range = high[i] - low[i];
            if is_zero(range) {
                0.0
            } else {
                ((close[i] - low[i]) - (high[i] - close[i])) / range
            }
        })
        .collect();

    // Money Flow Volume
    let mf_volume: Vec<f64> = (0..n).map(|i| mf_multiplier[i] * volume[i]).collect();

    let mut result = init_result!(n);
    let mut mfv_sum: f64 = mf_volume[..period].iter().sum();
    let mut vol_sum: f64 = volume[..period].iter().sum();

    result[period - 1] = if is_zero(vol_sum) {
        0.0
    } else {
        mfv_sum / vol_sum
    };

    for i in period..n {
        mfv_sum += mf_volume[i] - mf_volume[i - period];
        vol_sum += volume[i] - volume[i - period];
        result[i] = if is_zero(vol_sum) {
            0.0
        } else {
            mfv_sum / vol_sum
        };
    }

    Ok(result)
}

/// Volume Profile（成交量分布）
///
/// 算法：
/// 1. 将价格范围分为 n 个区间
/// 2. 统计每个区间的成交量
/// 3. 找到成交量最大的价格水平（POC - Point of Control）
///
/// # 参数
/// - `high`: 最高价序列
/// - `low`: 最低价序列
/// - `close`: 收盘价序列
/// - `volume`: 成交量序列
/// - `num_bins`: 价格区间数量（默认 24）
///
/// # 返回
/// - `HazeResult<(价格水平, 对应成交量, POC 价格)>`
///
/// # 错误
/// - `EmptyInput`: 输入为空
/// - `LengthMismatch`: 数组长度不匹配
pub fn volume_profile(
    high: &[f64],
    low: &[f64],
    close: &[f64],
    volume: &[f64],
    num_bins: usize,
) -> HazeResult<(Vec<f64>, Vec<f64>, f64)> {
    validate_not_empty(high, "high")?;
    validate_lengths_match(&[
        (high, "high"),
        (low, "low"),
        (close, "close"),
        (volume, "volume"),
    ])?;

    if num_bins == 0 {
        return Ok((vec![], vec![], f64::NAN));
    }

    let n = high.len();

    // 找到价格范围
    let min_price = low.iter().fold(f64::INFINITY, |a, &b| a.min(b));
    let max_price = high.iter().fold(f64::NEG_INFINITY, |a, &b| a.max(b));
    let price_range = max_price - min_price;

    if is_zero(price_range) {
        return Ok((vec![min_price], vec![volume.iter().sum()], min_price));
    }

    let bin_size = price_range / num_bins as f64;

    // 统计每个区间的成交量
    let mut bins = vec![0.0; num_bins];
    let mut price_levels = vec![0.0; num_bins];

    for i in 0..num_bins {
        price_levels[i] = min_price + (i as f64 + 0.5) * bin_size;
    }

    // 分配成交量到各个区间
    for i in 0..n {
        let typical_price = (high[i] + low[i] + close[i]) / 3.0;
        let bin_index = ((typical_price - min_price) / bin_size).floor() as usize;
        let bin_index = bin_index.min(num_bins - 1);
        bins[bin_index] += volume[i];
    }

    // 找到 POC（最大成交量的价格水平）
    let max_volume = bins.iter().fold(f64::NEG_INFINITY, |a, &b| a.max(b));
    let poc_index = bins.iter().position(|&v| v == max_volume).unwrap_or(0);
    let poc_price = price_levels[poc_index];

    Ok((price_levels, bins, poc_price))
}

/// AD (Accumulation/Distribution) 累积/派发指标
///
/// 衡量资金流入流出的指标，结合价格和成交量
///
/// # 参数
/// - `high`: 高价序列
/// - `low`: 低价序列
/// - `close`: 收盘价序列
/// - `volume`: 成交量序列
///
/// # 返回
/// - `HazeResult<Vec<f64>>`: AD 线（累积值）
///
/// # 算法
/// 1. MF Multiplier = [(Close - Low) - (High - Close)] / (High - Low)
/// 2. MF Volume = MF Multiplier * Volume
/// 3. AD = Cumulative_Sum(MF Volume)
///
/// # 错误
/// - `EmptyInput`: 输入为空
/// - `LengthMismatch`: 数组长度不匹配
pub fn accumulation_distribution(
    high: &[f64],
    low: &[f64],
    close: &[f64],
    volume: &[f64],
) -> HazeResult<Vec<f64>> {
    validate_not_empty(high, "high")?;
    validate_lengths_match(&[
        (high, "high"),
        (low, "low"),
        (close, "close"),
        (volume, "volume"),
    ])?;

    let n = high.len();
    let mut ad = init_result!(n);
    let mut cumulative = 0.0;

    for i in 0..n {
        let range = high[i] - low[i];

        if range > 0.0 {
            // MF Multiplier = [(C-L) - (H-C)] / (H-L) = (2C - H - L) / (H - L)
            let mf_multiplier = ((close[i] - low[i]) - (high[i] - close[i])) / range;
            let mf_volume = mf_multiplier * volume[i];

            cumulative += mf_volume;
            ad[i] = cumulative;
        } else {
            // 如果 high == low，保持前值
            ad[i] = if i > 0 { ad[i - 1] } else { 0.0 };
        }
    }

    Ok(ad)
}

/// PVT (Price Volume Trend) 价量趋势指标
///
/// 类似 OBV，但考虑价格变化的幅度
///
/// # 参数
/// - `close`: 收盘价序列
/// - `volume`: 成交量序列
///
/// # 返回
/// - `HazeResult<Vec<f64>>`: PVT 线（累积值）
///
/// # 算法
/// PVT[i] = PVT[i-1] + Volume[i] * (Close[i] - Close[i-1]) / Close[i-1]
///
/// # 错误
/// - `EmptyInput`: 输入为空
/// - `LengthMismatch`: 数组长度不匹配
pub fn price_volume_trend(close: &[f64], volume: &[f64]) -> HazeResult<Vec<f64>> {
    validate_not_empty(close, "close")?;
    validate_lengths_match(&[(close, "close"), (volume, "volume")])?;

    let n = close.len();
    if n < 2 {
        return Ok(init_result!(n));
    }

    let mut pvt = init_result!(n);
    pvt[0] = 0.0;

    for i in 1..n {
        if is_not_zero(close[i - 1]) {
            let price_change_pct = (close[i] - close[i - 1]) / close[i - 1];
            pvt[i] = pvt[i - 1] + volume[i] * price_change_pct;
        } else {
            pvt[i] = pvt[i - 1];
        }
    }

    Ok(pvt)
}

/// NVI (Negative Volume Index) 负成交量指标
///
/// 仅在成交量减少时更新，追踪"聪明钱"
///
/// # 参数
/// - `close`: 收盘价序列
/// - `volume`: 成交量序列
///
/// # 返回
/// - `HazeResult<Vec<f64>>`: NVI 线（起始值 1000）
///
/// # 算法
/// 如果 Volume[i] < Volume[i-1]:
///     NVI[i] = NVI[i-1] + NVI[i-1] * (Close[i] - Close[i-1]) / Close[i-1]
/// 否则:
///     NVI[i] = NVI[i-1]
///
/// # 错误
/// - `EmptyInput`: 输入为空
/// - `LengthMismatch`: 数组长度不匹配
pub fn negative_volume_index(close: &[f64], volume: &[f64]) -> HazeResult<Vec<f64>> {
    validate_not_empty(close, "close")?;
    validate_lengths_match(&[(close, "close"), (volume, "volume")])?;

    let n = close.len();
    if n < 2 {
        return Ok(init_result!(n));
    }

    let mut nvi = init_result!(n);
    nvi[0] = 1000.0; // 起始值

    for i in 1..n {
        if volume[i] < volume[i - 1] && is_not_zero(close[i - 1]) {
            // 成交量减少时更新
            let price_change_pct = (close[i] - close[i - 1]) / close[i - 1];
            nvi[i] = nvi[i - 1] * (1.0 + price_change_pct);
        } else {
            nvi[i] = nvi[i - 1];
        }
    }

    Ok(nvi)
}

/// PVI (Positive Volume Index) 正成交量指标
///
/// 仅在成交量增加时更新，追踪"大众"行为
///
/// # 参数
/// - `close`: 收盘价序列
/// - `volume`: 成交量序列
///
/// # 返回
/// - `HazeResult<Vec<f64>>`: PVI 线（起始值 1000）
///
/// # 算法
/// 如果 Volume[i] > Volume[i-1]:
///     PVI[i] = PVI[i-1] + PVI[i-1] * (Close[i] - Close[i-1]) / Close[i-1]
/// 否则:
///     PVI[i] = PVI[i-1]
///
/// # 错误
/// - `EmptyInput`: 输入为空
/// - `LengthMismatch`: 数组长度不匹配
pub fn positive_volume_index(close: &[f64], volume: &[f64]) -> HazeResult<Vec<f64>> {
    validate_not_empty(close, "close")?;
    validate_lengths_match(&[(close, "close"), (volume, "volume")])?;

    let n = close.len();
    if n < 2 {
        return Ok(init_result!(n));
    }

    let mut pvi = init_result!(n);
    pvi[0] = 1000.0; // 起始值

    for i in 1..n {
        if volume[i] > volume[i - 1] && is_not_zero(close[i - 1]) {
            // 成交量增加时更新
            let price_change_pct = (close[i] - close[i - 1]) / close[i - 1];
            pvi[i] = pvi[i - 1] * (1.0 + price_change_pct);
        } else {
            pvi[i] = pvi[i - 1];
        }
    }

    Ok(pvi)
}

/// EOM (Ease of Movement) 移动便利性指标
///
/// 衡量价格变动需要的成交量，值越大越容易移动
///
/// # 参数
/// - `high`: 高价序列
/// - `low`: 低价序列
/// - `volume`: 成交量序列
/// - `period`: 平滑周期（默认 14）
///
/// # 返回
/// - `HazeResult<Vec<f64>>`: EOM 线
///
/// # 算法
/// 1. Distance Moved = (High[i] + Low[i])/2 - (High[i-1] + Low[i-1])/2
/// 2. Box Ratio = Volume[i] / (High[i] - Low[i])
/// 3. EMV = Distance Moved / Box Ratio
/// 4. EOM = SMA(EMV, period)
///
/// # 错误
/// - `EmptyInput`: 输入为空
/// - `LengthMismatch`: 数组长度不匹配
/// - `InvalidPeriod`: 周期参数无效
pub fn ease_of_movement(
    high: &[f64],
    low: &[f64],
    volume: &[f64],
    period: usize,
) -> HazeResult<Vec<f64>> {
    validate_not_empty(high, "high")?;
    validate_lengths_match(&[(high, "high"), (low, "low"), (volume, "volume")])?;
    let n = high.len();
    validate_period(period, n)?;

    if n < 2 {
        return Ok(init_result!(n));
    }

    let mut emv = init_result!(n);
    emv[0] = 0.0;

    for i in 1..n {
        let mid_current = (high[i] + low[i]) / 2.0;
        let mid_prev = (high[i - 1] + low[i - 1]) / 2.0;
        let distance_moved = mid_current - mid_prev;

        let box_height = high[i] - low[i];

        if box_height > 0.0 && volume[i] > 0.0 {
            let box_ratio = volume[i] / (box_height * 100000000.0); // 比例调整（避免数值过小）
            emv[i] = distance_moved / box_ratio;
        }
    }

    // SMA 平滑
    sma(&emv, period)
}

/// ADOSC (Chaikin A/D Oscillator) 蔡金A/D振荡器
///
/// AD线的双EMA差值，衡量资金流入流出的动量
///
/// # 参数
/// - `high`: 高价序列
/// - `low`: 低价序列
/// - `close`: 收盘价序列
/// - `volume`: 成交量序列
/// - `fast_period`: 快速EMA周期（默认 3）
/// - `slow_period`: 慢速EMA周期（默认 10）
///
/// # 返回
/// - `HazeResult<Vec<f64>>`: ADOSC 值
///
/// # 算法
/// 1. AD = accumulation_distribution(high, low, close, volume)
/// 2. ADOSC = EMA(AD, fast) - EMA(AD, slow)
///
/// # 错误
/// - `EmptyInput`: 输入为空
/// - `LengthMismatch`: 数组长度不匹配
/// - `InvalidPeriod`: 周期参数无效
pub fn chaikin_ad_oscillator(
    high: &[f64],
    low: &[f64],
    close: &[f64],
    volume: &[f64],
    fast_period: usize,
    slow_period: usize,
) -> HazeResult<Vec<f64>> {
    validate_not_empty(high, "high")?;
    validate_lengths_match(&[
        (high, "high"),
        (low, "low"),
        (close, "close"),
        (volume, "volume"),
    ])?;
    let n = high.len();
    validate_period(fast_period, n)?;
    validate_period(slow_period, n)?;

    // 1. 计算 AD 线
    let ad_line = accumulation_distribution(high, low, close, volume)?;

    // 2. 计算快慢 EMA
    let ad_ema_fast = crate::utils::ema(&ad_line, fast_period)?;
    let ad_ema_slow = crate::utils::ema(&ad_line, slow_period)?;

    // 3. 计算差值
    let result = ad_ema_fast
        .iter()
        .zip(&ad_ema_slow)
        .map(|(&fast, &slow)| {
            if fast.is_nan() || slow.is_nan() {
                f64::NAN
            } else {
                fast - slow
            }
        })
        .collect();

    Ok(result)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_obv() {
        let close = vec![100.0, 101.0, 100.5, 102.0, 101.0];
        let volume = vec![1000.0, 1100.0, 1200.0, 1300.0, 1400.0];

        let result = obv(&close, &volume).unwrap();

        // 与 TA-Lib 对齐：初始值使用 volume[0]
        assert_eq!(result[0], 1000.0);
        assert_eq!(result[1], 1000.0 + 1100.0); // 上涨: +volume[1]
        assert_eq!(result[2], 2100.0 - 1200.0); // 下跌: -volume[2]
    }

    #[test]
    fn test_obv_empty_input() {
        let result = obv(&[], &[]);
        assert!(result.is_err());
    }

    #[test]
    fn test_obv_length_mismatch() {
        let close = vec![100.0, 101.0];
        let volume = vec![1000.0];
        let result = obv(&close, &volume);
        assert!(result.is_err());
    }

    #[test]
    fn test_vwap() {
        let high = vec![102.0, 103.0, 104.0];
        let low = vec![100.0, 101.0, 102.0];
        let close = vec![101.0, 102.0, 103.0];
        let volume = vec![1000.0, 1100.0, 1200.0];

        let result = vwap(&high, &low, &close, &volume, 0).unwrap(); // 累积 VWAP

        assert!(!result[0].is_nan());
        assert!(!result[1].is_nan());
        assert!(!result[2].is_nan());
    }

    #[test]
    fn test_mfi() {
        let high = vec![110.0, 111.0, 112.0, 113.0, 114.0, 115.0];
        let low = vec![100.0, 101.0, 102.0, 103.0, 104.0, 105.0];
        let close = vec![105.0, 106.0, 107.0, 108.0, 109.0, 110.0];
        let volume = vec![1000.0, 1100.0, 1200.0, 1300.0, 1400.0, 1500.0];

        let result = mfi(&high, &low, &close, &volume, 3).unwrap();

        assert!(result[0].is_nan());
        assert!(result[1].is_nan());
        assert!(result[2] >= 0.0 && result[2] <= 100.0);
    }

    #[test]
    fn test_mfi_invalid_period() {
        let high = vec![110.0, 111.0, 112.0];
        let low = vec![100.0, 101.0, 102.0];
        let close = vec![105.0, 106.0, 107.0];
        let volume = vec![1000.0, 1100.0, 1200.0];

        let result = mfi(&high, &low, &close, &volume, 0);
        assert!(result.is_err());
    }

    #[test]
    fn test_cmf_basic() {
        let high = vec![10.0, 12.0];
        let low = vec![8.0, 9.0];
        let close = vec![9.0, 11.0];
        let volume = vec![100.0, 200.0];

        let result = cmf(&high, &low, &close, &volume, 2).unwrap();
        assert!(result[0].is_nan());
        assert!((result[1] - (2.0 / 9.0)).abs() < 1e-10);
    }

    #[test]
    fn test_volume_profile() {
        let high = vec![102.0, 105.0, 104.0, 106.0];
        let low = vec![100.0, 101.0, 100.0, 102.0];
        let close = vec![101.0, 103.0, 102.0, 105.0];
        let volume = vec![1000.0, 1100.0, 1200.0, 1300.0];

        let (price_levels, bins, poc) = volume_profile(&high, &low, &close, &volume, 10).unwrap();

        assert_eq!(price_levels.len(), 10);
        assert_eq!(bins.len(), 10);
        assert!(!poc.is_nan());
    }

    #[test]
    fn test_volume_profile_zero_bins() {
        let high = vec![102.0, 105.0];
        let low = vec![100.0, 101.0];
        let close = vec![101.0, 103.0];
        let volume = vec![1000.0, 1100.0];

        let (price_levels, bins, poc) = volume_profile(&high, &low, &close, &volume, 0).unwrap();

        assert!(price_levels.is_empty());
        assert!(bins.is_empty());
        assert!(poc.is_nan());
    }
}

#[cfg(test)]
mod volume_extended_tests {
    use super::*;

    #[test]
    fn test_ad_basic() {
        let high = vec![110.0, 111.0, 112.0];
        let low = vec![100.0, 101.0, 102.0];
        let close = vec![105.0, 106.0, 107.0];
        let volume = vec![1000.0, 1100.0, 1200.0];

        let ad = accumulation_distribution(&high, &low, &close, &volume).unwrap();

        // AD 应该是累积的，逐渐增加或减少
        assert!(!ad[0].is_nan());
        assert!(!ad[1].is_nan());
        assert!(!ad[2].is_nan());
    }

    #[test]
    fn test_pvt_basic() {
        let close = vec![100.0, 105.0, 110.0];
        let volume = vec![1000.0, 1100.0, 1200.0];

        let pvt = price_volume_trend(&close, &volume).unwrap();

        assert!(pvt[0] == 0.0);
        assert!(!pvt[1].is_nan());
        assert!(!pvt[2].is_nan());
        // PVT 应该增加（价格上升）
        assert!(pvt[2] > pvt[1]);
    }

    #[test]
    fn test_nvi_pvi() {
        let close = vec![100.0, 102.0, 101.0, 103.0];
        let volume = vec![1000.0, 900.0, 1100.0, 1000.0];

        let nvi = negative_volume_index(&close, &volume).unwrap();
        let pvi = positive_volume_index(&close, &volume).unwrap();

        assert!(nvi[0] == 1000.0);
        assert!(pvi[0] == 1000.0);
        assert!(!nvi[3].is_nan());
        assert!(!pvi[3].is_nan());
    }

    #[test]
    fn test_eom_basic() {
        let high = vec![110.0; 20];
        let low = vec![100.0; 20];
        let volume = vec![1000.0; 20];

        let eom = ease_of_movement(&high, &low, &volume, 14).unwrap();

        // 横盘市场中，EOM 应接近 0
        let valid_idx = 15;
        assert!(!eom[valid_idx].is_nan());
        assert!(eom[valid_idx].abs() < 10.0);
    }

    #[test]
    fn test_adosc_basic() {
        let high = vec![110.0; 30];
        let low = vec![100.0; 30];
        let close = vec![105.0; 30];
        let volume = vec![1000.0; 30];

        let adosc = chaikin_ad_oscillator(&high, &low, &close, &volume, 3, 10).unwrap();

        // 横盘市场中，ADOSC 应接近 0
        let valid_idx = 15;
        assert!(!adosc[valid_idx].is_nan());
        assert!(adosc[valid_idx].abs() < 1000.0);
    }
}
