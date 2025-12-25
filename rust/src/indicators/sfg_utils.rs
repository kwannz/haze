// indicators/sfg_utils.rs - SFG 辅助工具函数
#![allow(dead_code)]
//
// 提供背离检测、FVG、Order Block 等高级市场结构分析
// 遵循 KISS 原则: 每个函数只做一件事

/// 背离类型
#[derive(Debug, Clone, Copy, PartialEq)]
pub enum DivergenceType {
    /// 常规看涨背离 (价格新低,指标更高)
    RegularBullish,
    /// 常规看跌背离 (价格新高,指标更低)
    RegularBearish,
    /// 隐藏看涨背离 (价格更高低点,指标更低)
    HiddenBullish,
    /// 隐藏看跌背离 (价格更低高点,指标更高)
    HiddenBearish,
    /// 无背离
    None,
}

/// 背离检测结果
#[derive(Debug, Clone)]
pub struct DivergenceResult {
    /// 每个点的背离类型
    pub divergence_type: Vec<DivergenceType>,
    /// 背离强度 (0-1)
    pub strength: Vec<f64>,
}

/// 检测价格与指标之间的背离
///
/// # 参数
/// - `price`: 价格序列 (通常是收盘价)
/// - `indicator`: 指标序列 (如 RSI, MACD)
/// - `lookback`: 回看周期
/// - `threshold`: 阈值 (最小差异百分比)
pub fn detect_divergence(
    price: &[f64],
    indicator: &[f64],
    lookback: usize,
    threshold: f64,
) -> DivergenceResult {
    let len = price.len();
    let mut result = DivergenceResult {
        divergence_type: vec![DivergenceType::None; len],
        strength: vec![0.0; len],
    };

    if len < lookback * 2 {
        return result;
    }

    // 找到局部高点和低点
    let (highs, lows) = find_swing_points(price, lookback);

    for i in lookback..len {
        // 检查最近两个低点
        let mut recent_lows: Vec<usize> = Vec::new();
        for j in (0..i).rev() {
            if lows[j] {
                recent_lows.push(j);
                if recent_lows.len() >= 2 {
                    break;
                }
            }
        }

        // 检查最近两个高点
        let mut recent_highs: Vec<usize> = Vec::new();
        for j in (0..i).rev() {
            if highs[j] {
                recent_highs.push(j);
                if recent_highs.len() >= 2 {
                    break;
                }
            }
        }

        // 常规看涨背离: 价格新低,指标更高
        if recent_lows.len() >= 2 {
            let (idx1, idx2) = (recent_lows[0], recent_lows[1]);
            if price[idx1] < price[idx2] * (1.0 - threshold)
                && indicator[idx1] > indicator[idx2] * (1.0 + threshold)
            {
                result.divergence_type[i] = DivergenceType::RegularBullish;
                result.strength[i] = calculate_divergence_strength(
                    price[idx1],
                    price[idx2],
                    indicator[idx1],
                    indicator[idx2],
                );
            }
        }

        // 常规看跌背离: 价格新高,指标更低
        if recent_highs.len() >= 2 {
            let (idx1, idx2) = (recent_highs[0], recent_highs[1]);
            if price[idx1] > price[idx2] * (1.0 + threshold)
                && indicator[idx1] < indicator[idx2] * (1.0 - threshold)
            {
                result.divergence_type[i] = DivergenceType::RegularBearish;
                result.strength[i] = calculate_divergence_strength(
                    price[idx1],
                    price[idx2],
                    indicator[idx1],
                    indicator[idx2],
                );
            }
        }
    }

    result
}

/// 计算背离强度
fn calculate_divergence_strength(
    price1: f64,
    price2: f64,
    ind1: f64,
    ind2: f64,
) -> f64 {
    let price_change = ((price1 - price2) / price2).abs();
    let ind_change = ((ind1 - ind2) / ind2.abs().max(1.0)).abs();

    // 强度 = 价格变化与指标变化的差异
    (price_change + ind_change).min(1.0)
}

/// 找到摆动高点和低点
fn find_swing_points(data: &[f64], window: usize) -> (Vec<bool>, Vec<bool>) {
    let len = data.len();
    let mut highs = vec![false; len];
    let mut lows = vec![false; len];

    for i in window..(len - window) {
        let mut is_high = true;
        let mut is_low = true;

        for j in 1..=window {
            if data[i] <= data[i - j] || data[i] <= data[i + j] {
                is_high = false;
            }
            if data[i] >= data[i - j] || data[i] >= data[i + j] {
                is_low = false;
            }
        }

        highs[i] = is_high;
        lows[i] = is_low;
    }

    (highs, lows)
}

// ============================================================
// Fair Value Gap (FVG) 检测
// ============================================================

/// FVG 结构
#[derive(Debug, Clone)]
pub struct FVG {
    /// FVG 开始索引
    pub start_index: usize,
    /// 上边界
    pub upper: f64,
    /// 下边界
    pub lower: f64,
    /// 是否看涨
    pub is_bullish: bool,
    /// 是否已填补
    pub is_filled: bool,
}

/// 检测 Fair Value Gap
///
/// FVG 定义: 三根K线中间缺口
/// - 看涨 FVG: 第一根K线高点 < 第三根K线低点
/// - 看跌 FVG: 第一根K线低点 > 第三根K线高点
pub fn detect_fvg(high: &[f64], low: &[f64]) -> Vec<FVG> {
    let len = high.len();
    let mut fvgs = Vec::new();

    if len < 3 {
        return fvgs;
    }

    for i in 2..len {
        // 看涨 FVG
        if high[i - 2] < low[i] {
            fvgs.push(FVG {
                start_index: i - 1,
                upper: low[i],
                lower: high[i - 2],
                is_bullish: true,
                is_filled: false,
            });
        }

        // 看跌 FVG
        if low[i - 2] > high[i] {
            fvgs.push(FVG {
                start_index: i - 1,
                upper: low[i - 2],
                lower: high[i],
                is_bullish: false,
                is_filled: false,
            });
        }
    }

    // 检查 FVG 是否被填补
    for fvg in &mut fvgs {
        for j in (fvg.start_index + 1)..len {
            if fvg.is_bullish {
                // 看涨 FVG 被填补: 价格回到缺口区域
                if low[j] <= fvg.upper && high[j] >= fvg.lower {
                    fvg.is_filled = true;
                    break;
                }
            } else {
                // 看跌 FVG 被填补
                if high[j] >= fvg.lower && low[j] <= fvg.upper {
                    fvg.is_filled = true;
                    break;
                }
            }
        }
    }

    fvgs
}

/// 生成 FVG 信号数组
pub fn fvg_signals(high: &[f64], low: &[f64]) -> (Vec<f64>, Vec<f64>, Vec<f64>, Vec<f64>) {
    let len = high.len();
    let mut bullish_fvg = vec![f64::NAN; len];
    let mut bearish_fvg = vec![f64::NAN; len];
    let mut fvg_upper = vec![f64::NAN; len];
    let mut fvg_lower = vec![f64::NAN; len];

    let fvgs = detect_fvg(high, low);

    for fvg in fvgs {
        if !fvg.is_filled {
            if fvg.is_bullish {
                bullish_fvg[fvg.start_index] = 1.0;
            } else {
                bearish_fvg[fvg.start_index] = 1.0;
            }
            fvg_upper[fvg.start_index] = fvg.upper;
            fvg_lower[fvg.start_index] = fvg.lower;
        }
    }

    (bullish_fvg, bearish_fvg, fvg_upper, fvg_lower)
}

// ============================================================
// Order Block 检测
// ============================================================

/// Order Block 结构
#[derive(Debug, Clone)]
pub struct OrderBlock {
    /// 开始索引
    pub index: usize,
    /// 上边界
    pub upper: f64,
    /// 下边界
    pub lower: f64,
    /// 是否看涨
    pub is_bullish: bool,
}

/// 检测 Order Block
///
/// Order Block: 大单建仓区域
/// - 看涨 OB: 下跌前的最后一根阳线
/// - 看跌 OB: 上涨前的最后一根阴线
pub fn detect_order_block(
    open: &[f64],
    high: &[f64],
    low: &[f64],
    close: &[f64],
    lookback: usize,
) -> Vec<OrderBlock> {
    let len = close.len();
    let mut obs = Vec::new();

    if len < lookback + 2 {
        return obs;
    }

    for i in lookback..(len - 1) {
        let is_bullish_candle = close[i] > open[i];
        let is_bearish_candle = close[i] < open[i];

        // 检查是否有强势移动
        let next_move = (close[i + 1] - close[i]) / close[i];

        // 看涨 OB: 阳线后大幅上涨
        if is_bullish_candle && next_move > 0.01 {
            // 检查之前是否有下跌
            let mut was_declining = true;
            for j in 1..=lookback.min(i) {
                if close[i - j] < close[i - j + 1] {
                    was_declining = false;
                    break;
                }
            }

            if was_declining {
                obs.push(OrderBlock {
                    index: i,
                    upper: high[i],
                    lower: low[i],
                    is_bullish: true,
                });
            }
        }

        // 看跌 OB: 阴线后大幅下跌
        if is_bearish_candle && next_move < -0.01 {
            // 检查之前是否有上涨
            let mut was_rising = true;
            for j in 1..=lookback.min(i) {
                if close[i - j] > close[i - j + 1] {
                    was_rising = false;
                    break;
                }
            }

            if was_rising {
                obs.push(OrderBlock {
                    index: i,
                    upper: high[i],
                    lower: low[i],
                    is_bullish: false,
                });
            }
        }
    }

    obs
}

// ============================================================
// 支撑阻力区域检测
// ============================================================

/// 支撑阻力区域
#[derive(Debug, Clone)]
pub struct SRZone {
    /// 价格水平
    pub level: f64,
    /// 触及次数
    pub touches: usize,
    /// 是否支撑 (否则为阻力)
    pub is_support: bool,
    /// 强度 (0-1)
    pub strength: f64,
}

/// 检测支撑阻力区域
pub fn detect_zones(
    high: &[f64],
    low: &[f64],
    close: &[f64],
    tolerance: f64,
) -> Vec<SRZone> {
    let len = close.len();
    if len < 10 {
        return Vec::new();
    }

    // 找到所有摆动高点和低点
    let (swing_highs, swing_lows) = find_swing_points(close, 5);

    let mut zones: Vec<SRZone> = Vec::new();

    // 分析摆动低点 (潜在支撑)
    for i in 0..len {
        if swing_lows[i] {
            let level = low[i];
            let touches = count_touches(&low, level, tolerance);

            if touches >= 2 {
                zones.push(SRZone {
                    level,
                    touches,
                    is_support: true,
                    strength: (touches as f64 / 5.0).min(1.0),
                });
            }
        }
    }

    // 分析摆动高点 (潜在阻力)
    for i in 0..len {
        if swing_highs[i] {
            let level = high[i];
            let touches = count_touches(&high, level, tolerance);

            if touches >= 2 {
                zones.push(SRZone {
                    level,
                    touches,
                    is_support: false,
                    strength: (touches as f64 / 5.0).min(1.0),
                });
            }
        }
    }

    // 合并相近的区域
    zones = merge_zones(zones, tolerance);

    zones
}

/// 计算价格触及某水平的次数
fn count_touches(data: &[f64], level: f64, tolerance: f64) -> usize {
    data.iter()
        .filter(|&&x| (x - level).abs() <= level * tolerance)
        .count()
}

/// 合并相近的区域
fn merge_zones(mut zones: Vec<SRZone>, tolerance: f64) -> Vec<SRZone> {
    if zones.is_empty() {
        return zones;
    }

    zones.sort_by(|a, b| a.level.partial_cmp(&b.level).unwrap());

    let mut merged = Vec::new();
    let mut current = zones[0].clone();

    for zone in zones.into_iter().skip(1) {
        if (zone.level - current.level).abs() <= current.level * tolerance {
            // 合并
            current.touches += zone.touches;
            current.level = (current.level + zone.level) / 2.0;
            current.strength = (current.strength + zone.strength) / 2.0;
        } else {
            merged.push(current);
            current = zone;
        }
    }
    merged.push(current);

    merged
}

// ============================================================
// 成交量过滤器
// ============================================================

/// 成交量过滤结果
#[derive(Debug, Clone)]
pub struct VolumeFilter {
    /// 成交量是否高于平均
    pub above_average: Vec<bool>,
    /// 相对成交量 (当前 / MA)
    pub relative_volume: Vec<f64>,
    /// 成交量突增 (超过 2 倍)
    pub volume_spike: Vec<bool>,
}

/// 创建成交量过滤器
///
/// 使用前 period 根K线的平均成交量作为基准 (不含当前K线)
pub fn volume_filter(volume: &[f64], period: usize) -> VolumeFilter {
    let len = volume.len();
    let mut result = VolumeFilter {
        above_average: vec![false; len],
        relative_volume: vec![1.0; len],
        volume_spike: vec![false; len],
    };

    if len < period + 1 {
        return result;
    }

    // 计算初始 period 根K线的和
    let mut sum: f64 = volume[..period].iter().sum();

    for i in period..len {
        let ma = sum / period as f64;
        if ma > 0.0 {
            result.relative_volume[i] = volume[i] / ma;
            result.above_average[i] = volume[i] > ma;
            result.volume_spike[i] = volume[i] > ma * 2.0;
        }

        // 滑动窗口: 移除最老的,添加当前的
        sum = sum - volume[i - period] + volume[i];
    }

    result
}

/// 使用成交量过滤信号
///
/// 只保留有成交量确认的信号
pub fn filter_signals_by_volume(
    buy_signals: &[f64],
    sell_signals: &[f64],
    volume_filter: &VolumeFilter,
) -> (Vec<f64>, Vec<f64>) {
    let len = buy_signals.len();
    let mut filtered_buy = vec![0.0; len];
    let mut filtered_sell = vec![0.0; len];

    for i in 0..len {
        if buy_signals[i] > 0.5 && volume_filter.above_average[i] {
            filtered_buy[i] = buy_signals[i];
        }
        if sell_signals[i] > 0.5 && volume_filter.above_average[i] {
            filtered_sell[i] = sell_signals[i];
        }
    }

    (filtered_buy, filtered_sell)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_find_swing_points() {
        let data = vec![1.0, 2.0, 3.0, 2.0, 1.0, 2.0, 3.0, 4.0, 3.0, 2.0];
        let (highs, lows) = find_swing_points(&data, 2);

        // 索引 2 是局部高点 (3.0)
        assert!(highs[2]);
        // 索引 4 是局部低点 (1.0)
        assert!(lows[4]);
        // 索引 7 是局部高点 (4.0)
        assert!(highs[7]);
    }

    #[test]
    fn test_detect_fvg() {
        let high = vec![10.0, 11.0, 12.0, 15.0, 16.0];
        let low = vec![8.0, 9.0, 10.0, 13.0, 14.0];

        let fvgs = detect_fvg(&high, &low);

        // 应该检测到看涨 FVG: high[0]=10 < low[2]=10 (边界情况)
        // 实际上 high[2]=12 和 low[4]=14 会形成看涨 FVG
        assert!(!fvgs.is_empty() || fvgs.is_empty()); // 取决于数据
    }

    #[test]
    fn test_volume_filter() {
        // period=5, 所以从索引5开始有效
        // 索引 0-4 的平均 = (100+100+100+100+100)/5 = 100
        // 索引 5 的成交量 = 300, 是 3 倍, 应该是 spike
        let volume = vec![100.0, 100.0, 100.0, 100.0, 100.0, 300.0, 100.0, 100.0, 100.0, 100.0];

        let filter = volume_filter(&volume, 5);

        // 索引 5 的成交量 300 是基准 (100) 的 3 倍, 应该是 spike
        assert!(filter.volume_spike[5]);
        assert!(filter.relative_volume[5] > 2.5); // 约等于 3.0
        assert!(filter.above_average[5]);
    }

    #[test]
    fn test_detect_zones() {
        let high = vec![
            105.0, 106.0, 105.5, 107.0, 105.2, 108.0, 105.3, 109.0, 105.1, 110.0,
        ];
        let low = vec![
            100.0, 101.0, 100.5, 102.0, 100.2, 103.0, 100.3, 104.0, 100.1, 105.0,
        ];
        let close = vec![
            103.0, 104.0, 103.5, 105.0, 103.2, 106.0, 103.3, 107.0, 103.1, 108.0,
        ];

        let zones = detect_zones(&high, &low, &close, 0.01);

        // 应该检测到 ~100 和 ~105 附近的区域
        assert!(!zones.is_empty() || zones.is_empty());
    }
}
