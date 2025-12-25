// indicators/harmonics.rs - 谐波形态检测（XABCD Patterns）
//
// 基于 Fibonacci 比率检测经典谐波形态：
// - Gartley, Bat, Butterfly, Crab, Shark, Cypher 等
//
// 算法核心：
// 1. Swing Point Detection（摆动点检测）- 找出局部高点/低点
// 2. XABCD Pattern Matching（模式匹配）- 验证 Fibonacci 比率
// 3. Pattern Validation（有效性验证）- 确认形态完整性

use std::collections::HashMap;

/// Swing Point - 摆动点结构
#[derive(Debug, Clone, Copy)]
pub struct SwingPoint {
    pub index: usize,
    pub price: f64,
    pub is_high: bool,  // true=高点，false=低点
}

/// XABCD Pattern - 谐波形态结构
#[derive(Debug, Clone)]
pub struct HarmonicPattern {
    pub pattern_type: String,  // "Gartley", "Bat", "Butterfly", etc.
    pub x: SwingPoint,
    pub a: SwingPoint,
    pub b: SwingPoint,
    pub c: SwingPoint,
    pub d: SwingPoint,
    pub is_bullish: bool,
    pub ratios: HashMap<String, f64>,  // 实际 Fibonacci 比率
}

/// Fibonacci 比率容差（允许 ±3% 误差）
const FIB_TOLERANCE: f64 = 0.03;

/// 检测摆动点（局部极值）
///
/// - `high`: 高价序列
/// - `low`: 低价序列
/// - `left_bars`: 左侧窗口大小
/// - `right_bars`: 右侧窗口大小
///
/// 返回：摆动点向量（按时间顺序）
pub fn detect_swing_points(
    high: &[f64],
    low: &[f64],
    left_bars: usize,
    right_bars: usize,
) -> Vec<SwingPoint> {
    let n = high.len();
    let mut swings = Vec::new();

    for i in left_bars..(n - right_bars) {
        // 检测高点：当前高价 >= 左右窗口内所有高价
        let is_swing_high = (i - left_bars..i).all(|j| high[i] >= high[j])
            && (i + 1..=i + right_bars).all(|j| high[i] >= high[j]);

        if is_swing_high {
            swings.push(SwingPoint {
                index: i,
                price: high[i],
                is_high: true,
            });
        }

        // 检测低点：当前低价 <= 左右窗口内所有低价
        let is_swing_low = (i - left_bars..i).all(|j| low[i] <= low[j])
            && (i + 1..=i + right_bars).all(|j| low[i] <= low[j]);

        if is_swing_low {
            swings.push(SwingPoint {
                index: i,
                price: low[i],
                is_high: false,
            });
        }
    }

    // 按索引排序
    swings.sort_by_key(|s| s.index);
    swings
}

/// 检查 Fibonacci 比率是否在容差范围内
#[inline]
fn check_fib_ratio(actual: f64, expected: f64, tolerance: f64) -> bool {
    (actual - expected).abs() <= tolerance
}

/// 计算两点之间的价格变动比率（回撤或扩展）
#[inline]
fn calc_ratio(point1_price: f64, point2_price: f64, reference_start: f64, reference_end: f64) -> f64 {
    let point_move = (point2_price - point1_price).abs();
    let reference_move = (reference_end - reference_start).abs();
    if reference_move == 0.0 {
        0.0
    } else {
        point_move / reference_move
    }
}

/// 检测 Gartley 形态
///
/// Fibonacci 比率要求：
/// - AB = 0.618 XA
/// - BC = 0.382 ~ 0.886 AB
/// - CD = 1.272 ~ 1.618 BC
/// - AD = 0.786 XA
pub fn detect_gartley(swings: &[SwingPoint]) -> Vec<HarmonicPattern> {
    let mut patterns = Vec::new();

    if swings.len() < 5 {
        return patterns;
    }

    // 遍历所有可能的 XABCD 组合
    for i in 0..swings.len() - 4 {
        let x = swings[i];
        let a = swings[i + 1];
        let b = swings[i + 2];
        let c = swings[i + 3];
        let d = swings[i + 4];

        // 验证摆动点交替（高低高低高 或 低高低高低）
        if x.is_high == a.is_high || a.is_high == b.is_high
            || b.is_high == c.is_high || c.is_high == d.is_high
        {
            continue;
        }

        let is_bullish = !x.is_high;  // X 是低点则为看涨

        // 计算 Fibonacci 比率
        let ab_xa = calc_ratio(a.price, b.price, x.price, a.price);
        let bc_ab = calc_ratio(b.price, c.price, a.price, b.price);
        let cd_bc = calc_ratio(c.price, d.price, b.price, c.price);
        let ad_xa = calc_ratio(a.price, d.price, x.price, a.price);

        // Gartley 比率验证
        if check_fib_ratio(ab_xa, 0.618, FIB_TOLERANCE)
            && bc_ab >= 0.382 - FIB_TOLERANCE && bc_ab <= 0.886 + FIB_TOLERANCE
            && cd_bc >= 1.272 - FIB_TOLERANCE && cd_bc <= 1.618 + FIB_TOLERANCE
            && check_fib_ratio(ad_xa, 0.786, FIB_TOLERANCE)
        {
            let mut ratios = HashMap::new();
            ratios.insert("AB/XA".to_string(), ab_xa);
            ratios.insert("BC/AB".to_string(), bc_ab);
            ratios.insert("CD/BC".to_string(), cd_bc);
            ratios.insert("AD/XA".to_string(), ad_xa);

            patterns.push(HarmonicPattern {
                pattern_type: "Gartley".to_string(),
                x,
                a,
                b,
                c,
                d,
                is_bullish,
                ratios,
            });
        }
    }

    patterns
}

/// 检测 Bat 形态
///
/// Fibonacci 比率要求：
/// - AB = 0.382 ~ 0.500 XA
/// - BC = 0.382 ~ 0.886 AB
/// - CD = 1.618 ~ 2.618 BC
/// - AD = 0.886 XA
pub fn detect_bat(swings: &[SwingPoint]) -> Vec<HarmonicPattern> {
    let mut patterns = Vec::new();

    if swings.len() < 5 {
        return patterns;
    }

    for i in 0..swings.len() - 4 {
        let x = swings[i];
        let a = swings[i + 1];
        let b = swings[i + 2];
        let c = swings[i + 3];
        let d = swings[i + 4];

        if x.is_high == a.is_high || a.is_high == b.is_high
            || b.is_high == c.is_high || c.is_high == d.is_high
        {
            continue;
        }

        let is_bullish = !x.is_high;

        let ab_xa = calc_ratio(a.price, b.price, x.price, a.price);
        let bc_ab = calc_ratio(b.price, c.price, a.price, b.price);
        let cd_bc = calc_ratio(c.price, d.price, b.price, c.price);
        let ad_xa = calc_ratio(a.price, d.price, x.price, a.price);

        // Bat 比率验证
        if ab_xa >= 0.382 - FIB_TOLERANCE && ab_xa <= 0.500 + FIB_TOLERANCE
            && bc_ab >= 0.382 - FIB_TOLERANCE && bc_ab <= 0.886 + FIB_TOLERANCE
            && cd_bc >= 1.618 - FIB_TOLERANCE && cd_bc <= 2.618 + FIB_TOLERANCE
            && check_fib_ratio(ad_xa, 0.886, FIB_TOLERANCE)
        {
            let mut ratios = HashMap::new();
            ratios.insert("AB/XA".to_string(), ab_xa);
            ratios.insert("BC/AB".to_string(), bc_ab);
            ratios.insert("CD/BC".to_string(), cd_bc);
            ratios.insert("AD/XA".to_string(), ad_xa);

            patterns.push(HarmonicPattern {
                pattern_type: "Bat".to_string(),
                x,
                a,
                b,
                c,
                d,
                is_bullish,
                ratios,
            });
        }
    }

    patterns
}

/// 检测 Butterfly 形态
///
/// Fibonacci 比率要求：
/// - AB = 0.786 XA
/// - BC = 0.382 ~ 0.886 AB
/// - CD = 1.618 ~ 2.24 BC
/// - AD = 1.27 ~ 1.618 XA
pub fn detect_butterfly(swings: &[SwingPoint]) -> Vec<HarmonicPattern> {
    let mut patterns = Vec::new();

    if swings.len() < 5 {
        return patterns;
    }

    for i in 0..swings.len() - 4 {
        let x = swings[i];
        let a = swings[i + 1];
        let b = swings[i + 2];
        let c = swings[i + 3];
        let d = swings[i + 4];

        if x.is_high == a.is_high || a.is_high == b.is_high
            || b.is_high == c.is_high || c.is_high == d.is_high
        {
            continue;
        }

        let is_bullish = !x.is_high;

        let ab_xa = calc_ratio(a.price, b.price, x.price, a.price);
        let bc_ab = calc_ratio(b.price, c.price, a.price, b.price);
        let cd_bc = calc_ratio(c.price, d.price, b.price, c.price);
        let ad_xa = calc_ratio(a.price, d.price, x.price, a.price);

        // Butterfly 比率验证
        if check_fib_ratio(ab_xa, 0.786, FIB_TOLERANCE)
            && bc_ab >= 0.382 - FIB_TOLERANCE && bc_ab <= 0.886 + FIB_TOLERANCE
            && cd_bc >= 1.618 - FIB_TOLERANCE && cd_bc <= 2.24 + FIB_TOLERANCE
            && ad_xa >= 1.27 - FIB_TOLERANCE && ad_xa <= 1.618 + FIB_TOLERANCE
        {
            let mut ratios = HashMap::new();
            ratios.insert("AB/XA".to_string(), ab_xa);
            ratios.insert("BC/AB".to_string(), bc_ab);
            ratios.insert("CD/BC".to_string(), cd_bc);
            ratios.insert("AD/XA".to_string(), ad_xa);

            patterns.push(HarmonicPattern {
                pattern_type: "Butterfly".to_string(),
                x,
                a,
                b,
                c,
                d,
                is_bullish,
                ratios,
            });
        }
    }

    patterns
}

/// 检测 Crab 形态
///
/// Fibonacci 比率要求：
/// - AB = 0.382 ~ 0.618 XA
/// - BC = 0.382 ~ 0.886 AB
/// - CD = 2.24 ~ 3.618 BC
/// - AD = 1.618 XA
pub fn detect_crab(swings: &[SwingPoint]) -> Vec<HarmonicPattern> {
    let mut patterns = Vec::new();

    if swings.len() < 5 {
        return patterns;
    }

    for i in 0..swings.len() - 4 {
        let x = swings[i];
        let a = swings[i + 1];
        let b = swings[i + 2];
        let c = swings[i + 3];
        let d = swings[i + 4];

        if x.is_high == a.is_high || a.is_high == b.is_high
            || b.is_high == c.is_high || c.is_high == d.is_high
        {
            continue;
        }

        let is_bullish = !x.is_high;

        let ab_xa = calc_ratio(a.price, b.price, x.price, a.price);
        let bc_ab = calc_ratio(b.price, c.price, a.price, b.price);
        let cd_bc = calc_ratio(c.price, d.price, b.price, c.price);
        let ad_xa = calc_ratio(a.price, d.price, x.price, a.price);

        // Crab 比率验证
        if ab_xa >= 0.382 - FIB_TOLERANCE && ab_xa <= 0.618 + FIB_TOLERANCE
            && bc_ab >= 0.382 - FIB_TOLERANCE && bc_ab <= 0.886 + FIB_TOLERANCE
            && cd_bc >= 2.24 - FIB_TOLERANCE && cd_bc <= 3.618 + FIB_TOLERANCE
            && check_fib_ratio(ad_xa, 1.618, FIB_TOLERANCE)
        {
            let mut ratios = HashMap::new();
            ratios.insert("AB/XA".to_string(), ab_xa);
            ratios.insert("BC/AB".to_string(), bc_ab);
            ratios.insert("CD/BC".to_string(), cd_bc);
            ratios.insert("AD/XA".to_string(), ad_xa);

            patterns.push(HarmonicPattern {
                pattern_type: "Crab".to_string(),
                x,
                a,
                b,
                c,
                d,
                is_bullish,
                ratios,
            });
        }
    }

    patterns
}

/// 检测 Shark 形态
///
/// Fibonacci 比率要求：
/// - AB = 0.382 ~ 0.618 XA（通常 0.618）
/// - BC = 1.13 ~ 1.618 AB
/// - CD = 1.618 ~ 2.24 BC
/// - AD = 0.886 ~ 1.13 XA
pub fn detect_shark(swings: &[SwingPoint]) -> Vec<HarmonicPattern> {
    let mut patterns = Vec::new();

    if swings.len() < 5 {
        return patterns;
    }

    for i in 0..swings.len() - 4 {
        let x = swings[i];
        let a = swings[i + 1];
        let b = swings[i + 2];
        let c = swings[i + 3];
        let d = swings[i + 4];

        if x.is_high == a.is_high || a.is_high == b.is_high
            || b.is_high == c.is_high || c.is_high == d.is_high
        {
            continue;
        }

        let is_bullish = !x.is_high;

        let ab_xa = calc_ratio(a.price, b.price, x.price, a.price);
        let bc_ab = calc_ratio(b.price, c.price, a.price, b.price);
        let cd_bc = calc_ratio(c.price, d.price, b.price, c.price);
        let ad_xa = calc_ratio(a.price, d.price, x.price, a.price);

        // Shark 比率验证
        if ab_xa >= 0.382 - FIB_TOLERANCE && ab_xa <= 0.618 + FIB_TOLERANCE
            && bc_ab >= 1.13 - FIB_TOLERANCE && bc_ab <= 1.618 + FIB_TOLERANCE
            && cd_bc >= 1.618 - FIB_TOLERANCE && cd_bc <= 2.24 + FIB_TOLERANCE
            && ad_xa >= 0.886 - FIB_TOLERANCE && ad_xa <= 1.13 + FIB_TOLERANCE
        {
            let mut ratios = HashMap::new();
            ratios.insert("AB/XA".to_string(), ab_xa);
            ratios.insert("BC/AB".to_string(), bc_ab);
            ratios.insert("CD/BC".to_string(), cd_bc);
            ratios.insert("AD/XA".to_string(), ad_xa);

            patterns.push(HarmonicPattern {
                pattern_type: "Shark".to_string(),
                x,
                a,
                b,
                c,
                d,
                is_bullish,
                ratios,
            });
        }
    }

    patterns
}

/// 检测 Cypher 形态
///
/// Fibonacci 比率要求：
/// - AB = 0.382 ~ 0.618 XA
/// - BC = 1.272 ~ 1.414 AB
/// - CD = 0.786 XC
/// - AD = 0.786 XA
pub fn detect_cypher(swings: &[SwingPoint]) -> Vec<HarmonicPattern> {
    let mut patterns = Vec::new();

    if swings.len() < 5 {
        return patterns;
    }

    for i in 0..swings.len() - 4 {
        let x = swings[i];
        let a = swings[i + 1];
        let b = swings[i + 2];
        let c = swings[i + 3];
        let d = swings[i + 4];

        if x.is_high == a.is_high || a.is_high == b.is_high
            || b.is_high == c.is_high || c.is_high == d.is_high
        {
            continue;
        }

        let is_bullish = !x.is_high;

        let ab_xa = calc_ratio(a.price, b.price, x.price, a.price);
        let bc_ab = calc_ratio(b.price, c.price, a.price, b.price);
        let cd_xc = calc_ratio(c.price, d.price, x.price, c.price);
        let ad_xa = calc_ratio(a.price, d.price, x.price, a.price);

        // Cypher 比率验证（注意 CD 是相对 XC 而非 BC）
        if ab_xa >= 0.382 - FIB_TOLERANCE && ab_xa <= 0.618 + FIB_TOLERANCE
            && bc_ab >= 1.272 - FIB_TOLERANCE && bc_ab <= 1.414 + FIB_TOLERANCE
            && check_fib_ratio(cd_xc, 0.786, FIB_TOLERANCE)
            && check_fib_ratio(ad_xa, 0.786, FIB_TOLERANCE)
        {
            let mut ratios = HashMap::new();
            ratios.insert("AB/XA".to_string(), ab_xa);
            ratios.insert("BC/AB".to_string(), bc_ab);
            ratios.insert("CD/XC".to_string(), cd_xc);
            ratios.insert("AD/XA".to_string(), ad_xa);

            patterns.push(HarmonicPattern {
                pattern_type: "Cypher".to_string(),
                x,
                a,
                b,
                c,
                d,
                is_bullish,
                ratios,
            });
        }
    }

    patterns
}

/// 检测所有谐波形态（聚合函数）
pub fn detect_all_harmonics(
    high: &[f64],
    low: &[f64],
    left_bars: usize,
    right_bars: usize,
) -> Vec<HarmonicPattern> {
    let swings = detect_swing_points(high, low, left_bars, right_bars);

    let mut all_patterns = Vec::new();

    all_patterns.extend(detect_gartley(&swings));
    all_patterns.extend(detect_bat(&swings));
    all_patterns.extend(detect_butterfly(&swings));
    all_patterns.extend(detect_crab(&swings));
    all_patterns.extend(detect_shark(&swings));
    all_patterns.extend(detect_cypher(&swings));

    // 按 D 点索引排序（时间顺序）
    all_patterns.sort_by_key(|p| p.d.index);

    all_patterns
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_swing_detection() {
        let high = vec![10.0, 12.0, 11.0, 13.0, 12.0, 14.0, 13.0];
        let low = vec![9.0, 11.0, 10.0, 12.0, 11.0, 13.0, 12.0];

        let swings = detect_swing_points(&high, &low, 1, 1);

        // 应至少检测到一些摆动点
        assert!(!swings.is_empty());
    }

    #[test]
    fn test_fib_ratio_check() {
        assert!(check_fib_ratio(0.62, 0.618, 0.03));
        assert!(check_fib_ratio(0.615, 0.618, 0.03));
        assert!(!check_fib_ratio(0.70, 0.618, 0.03));
    }
}
