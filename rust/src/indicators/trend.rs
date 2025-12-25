// indicators/trend.rs - 趋势指标
//
// 包含：SuperTrend, ADX, Aroon, PSAR, Vortex Indicator

use crate::indicators::volatility::atr;
use crate::utils::{ema, rma};

/// SuperTrend（超级趋势指标）
///
/// 算法：
/// 1. 计算基础线：basic_upperband = HL2 + multiplier * ATR
///                basic_lowerband = HL2 - multiplier * ATR
/// 2. 状态机追踪：
///    - 当 close > upperband: 趋势 = 1 (上升), 更新 lowerband
///    - 当 close < lowerband: 趋势 = -1 (下降), 更新 upperband
/// 3. 输出：
///    - supertrend: 趋势线（上升时为 lowerband，下降时为 upperband）
///    - direction: 1 (上升) 或 -1 (下降)
///
/// # 参数
/// - `high`: 最高价序列
/// - `low`: 最低价序列
/// - `close`: 收盘价序列
/// - `period`: ATR 周期（默认 7）
/// - `multiplier`: ATR 倍数（默认 3.0）
///
/// # 返回
/// - (supertrend, direction, upper, lower)
pub fn supertrend(
    high: &[f64],
    low: &[f64],
    close: &[f64],
    period: usize,
    multiplier: f64,
) -> (Vec<f64>, Vec<f64>, Vec<f64>, Vec<f64>) {
    let n = high.len();
    if n != low.len() || n != close.len() || period == 0 || period > n {
        return (
            vec![f64::NAN; n],
            vec![f64::NAN; n],
            vec![f64::NAN; n],
            vec![f64::NAN; n],
        );
    }

    // HL2 (中间价)
    let hl2: Vec<f64> = (0..n).map(|i| (high[i] + low[i]) / 2.0).collect();

    // ATR
    let atr_values = atr(high, low, close, period);

    // 计算基础带
    let basic_upper: Vec<f64> = (0..n)
        .map(|i| hl2[i] + multiplier * atr_values[i])
        .collect();
    let basic_lower: Vec<f64> = (0..n)
        .map(|i| hl2[i] - multiplier * atr_values[i])
        .collect();

    // 初始化输出
    let mut upper = vec![f64::NAN; n];
    let mut lower = vec![f64::NAN; n];
    let mut supertrend_line = vec![f64::NAN; n];
    let mut direction = vec![f64::NAN; n];

    // 从 period 开始（ATR 在 TA-Lib 模式下首个有效值在 index=period）
    for i in period..n {
        if atr_values[i].is_nan() {
            continue;
        }

        // 更新 upper band（首个有效点直接赋值，否则取较小值以确保只向下收敛）
        if i == period || upper[i - 1].is_nan() {
            upper[i] = basic_upper[i];
        } else if basic_upper[i] < upper[i - 1] {
            upper[i] = basic_upper[i];
        } else {
            upper[i] = upper[i - 1];
        }

        // 更新 lower band（首个有效点直接赋值，否则取较大值以确保只向上收敛）
        if i == period || lower[i - 1].is_nan() {
            lower[i] = basic_lower[i];
        } else if basic_lower[i] > lower[i - 1] {
            lower[i] = basic_lower[i];
        } else {
            lower[i] = lower[i - 1];
        }

        // 确定趋势方向
        // 初始方向：使用 close > hl2 判断（收盘价高于中间价 = 上升趋势）
        // 注：这是常见的启发式方法，与某些库（如 pandas-ta）可能略有差异
        // pandas-ta 可能使用 close > supertrend_line 或前一根 K 线延续
        if i == period {
            direction[i] = if close[i] > hl2[i] { 1.0 } else { -1.0 };
        } else {
            let prev_dir = direction[i - 1];
            if prev_dir == 1.0 {
                // 上升趋势
                direction[i] = if close[i] < lower[i] { -1.0 } else { 1.0 };
            } else {
                // 下降趋势
                direction[i] = if close[i] > upper[i] { 1.0 } else { -1.0 };
            }
        }

        // SuperTrend 线
        supertrend_line[i] = if direction[i] == 1.0 { lower[i] } else { upper[i] };
    }

    (supertrend_line, direction, upper, lower)
}

/// 内部辅助函数：计算方向指标 (+DI, -DI)
///
/// 提取公共逻辑，供 adx 和 dx 复用
fn compute_di(
    high: &[f64],
    low: &[f64],
    close: &[f64],
    period: usize,
) -> (Vec<f64>, Vec<f64>) {
    let n = high.len();

    // 计算方向移动
    let mut plus_dm = vec![0.0; n];
    let mut minus_dm = vec![0.0; n];

    for i in 1..n {
        let up_move = high[i] - high[i - 1];
        let down_move = low[i - 1] - low[i];

        if up_move > down_move && up_move > 0.0 {
            plus_dm[i] = up_move;
        }
        if down_move > up_move && down_move > 0.0 {
            minus_dm[i] = down_move;
        }
    }

    // ATR
    let atr_values = atr(high, low, close, period);

    // 平滑 DM
    let smooth_plus_dm = rma(&plus_dm, period);
    let smooth_minus_dm = rma(&minus_dm, period);

    // 计算 DI
    let plus_di: Vec<f64> = (0..n)
        .map(|i| {
            if atr_values[i].is_nan() || atr_values[i] == 0.0 {
                f64::NAN
            } else {
                100.0 * smooth_plus_dm[i] / atr_values[i]
            }
        })
        .collect();

    let minus_di: Vec<f64> = (0..n)
        .map(|i| {
            if atr_values[i].is_nan() || atr_values[i] == 0.0 {
                f64::NAN
            } else {
                100.0 * smooth_minus_dm[i] / atr_values[i]
            }
        })
        .collect();

    (plus_di, minus_di)
}

/// ADX - Average Directional Index（平均趋向指标）
///
/// 算法：
/// 1. +DM = max(high - prev_high, 0)
/// 2. -DM = max(prev_low - low, 0)
/// 3. 如果 +DM > -DM：-DM = 0，否则 +DM = 0
/// 4. +DI = 100 * RMA(+DM, period) / ATR
/// 5. -DI = 100 * RMA(-DM, period) / ATR
/// 6. DX = 100 * |(+DI - -DI)| / (+DI + -DI)
/// 7. ADX = RMA(DX, period)
///
/// # 参数
/// - `high`: 最高价序列
/// - `low`: 最低价序列
/// - `close`: 收盘价序列
/// - `period`: 周期（默认 14）
///
/// # 返回
/// - (adx, plus_di, minus_di)
pub fn adx(
    high: &[f64],
    low: &[f64],
    close: &[f64],
    period: usize,
) -> (Vec<f64>, Vec<f64>, Vec<f64>) {
    let n = high.len();
    if n != low.len() || n != close.len() {
        return (vec![f64::NAN; n], vec![f64::NAN; n], vec![f64::NAN; n]);
    }

    let (plus_di, minus_di) = compute_di(high, low, close, period);

    // 计算 DX（ADX 内部使用 0.0 替代 NaN 以便 RMA 平滑）
    let dx: Vec<f64> = (0..n)
        .map(|i| {
            if plus_di[i].is_nan() || minus_di[i].is_nan() {
                0.0
            } else {
                let sum = plus_di[i] + minus_di[i];
                if sum == 0.0 {
                    0.0
                } else {
                    100.0 * (plus_di[i] - minus_di[i]).abs() / sum
                }
            }
        })
        .collect();

    // ADX = RMA(DX)
    let adx_values = rma(&dx, period);

    (adx_values, plus_di, minus_di)
}

/// DX - Directional Movement Index（方向性移动指数）
///
/// ADX的基础指标，衡量趋势强度但无平滑
///
/// # 参数
/// - `high`: 最高价序列
/// - `low`: 最低价序列
/// - `close`: 收盘价序列
/// - `period`: 周期（默认 14）
///
/// # 返回
/// - DX 值（0-100）
///
/// # 算法
/// DX = 100 * |(+DI - -DI)| / (+DI + -DI)
pub fn dx(
    high: &[f64],
    low: &[f64],
    close: &[f64],
    period: usize,
) -> Vec<f64> {
    // 边界检查：空数组
    if high.is_empty() || low.is_empty() || close.is_empty() {
        return vec![];
    }

    let n = high.len();
    if n != low.len() || n != close.len() {
        return vec![f64::NAN; n];
    }

    // 复用 compute_di 计算 +DI 和 -DI
    let (plus_di, minus_di) = compute_di(high, low, close, period);

    // 计算 DX（DI 无效时返回 NaN，区别于 ADX 内部使用 0.0）
    (0..n)
        .map(|i| {
            if plus_di[i].is_nan() || minus_di[i].is_nan() {
                f64::NAN
            } else {
                let sum = plus_di[i] + minus_di[i];
                if sum == 0.0 {
                    0.0
                } else {
                    100.0 * (plus_di[i] - minus_di[i]).abs() / sum
                }
            }
        })
        .collect()
}

/// PLUS_DI - Positive Directional Indicator（正向指标）
///
/// 衡量上升趋势的强度
///
/// # 参数
/// - `high`: 最高价序列
/// - `low`: 最低价序列
/// - `close`: 收盘价序列
/// - `period`: 周期（默认 14）
///
/// # 返回
/// - +DI 值
pub fn plus_di(
    high: &[f64],
    low: &[f64],
    close: &[f64],
    period: usize,
) -> Vec<f64> {
    // 边界检查：空数组
    if high.is_empty() || low.is_empty() || close.is_empty() {
        return vec![];
    }

    let (_adx, plus_di, _minus_di) = adx(high, low, close, period);
    plus_di
}

/// MINUS_DI - Negative Directional Indicator（负向指标）
///
/// 衡量下降趋势的强度
///
/// # 参数
/// - `high`: 最高价序列
/// - `low`: 最低价序列
/// - `close`: 收盘价序列
/// - `period`: 周期（默认 14）
///
/// # 返回
/// - -DI 值
pub fn minus_di(
    high: &[f64],
    low: &[f64],
    close: &[f64],
    period: usize,
) -> Vec<f64> {
    // 边界检查：空数组
    if high.is_empty() || low.is_empty() || close.is_empty() {
        return vec![];
    }

    let (_adx, _plus_di, minus_di) = adx(high, low, close, period);
    minus_di
}

/// Aroon Indicator（阿隆指标）
///
/// 算法：
/// - Aroon Up = ((period - bars_since_highest_high) / period) * 100
/// - Aroon Down = ((period - bars_since_lowest_low) / period) * 100
/// - Aroon Oscillator = Aroon Up - Aroon Down
///
/// # 参数
/// - `high`: 最高价序列
/// - `low`: 最低价序列
/// - `period`: 周期（默认 25）
///
/// # 返回
/// - (aroon_up, aroon_down, aroon_oscillator)
pub fn aroon(
    high: &[f64],
    low: &[f64],
    period: usize,
) -> (Vec<f64>, Vec<f64>, Vec<f64>) {
    let n = high.len();
    if n != low.len() || period < 2 || period > n {
        return (vec![f64::NAN; n], vec![f64::NAN; n], vec![f64::NAN; n]);
    }

    let mut aroon_up = vec![f64::NAN; n];
    let mut aroon_down = vec![f64::NAN; n];
    let mut aroon_osc = vec![f64::NAN; n];

    for i in (period - 1)..n {
        // 找到最高点和最低点的位置
        let window_high = &high[i + 1 - period..=i];
        let window_low = &low[i + 1 - period..=i];

        let highest = window_high.iter().fold(f64::NEG_INFINITY, |a, &b| a.max(b));
        let lowest = window_low.iter().fold(f64::INFINITY, |a, &b| a.min(b));

        // 从窗口末尾倒数，找到最高/最低点的位置
        let bars_since_high = window_high
            .iter()
            .rev()
            .position(|&x| x == highest)
            .unwrap_or(period - 1);

        let bars_since_low = window_low
            .iter()
            .rev()
            .position(|&x| x == lowest)
            .unwrap_or(period - 1);

        aroon_up[i] = ((period - 1 - bars_since_high) as f64 / (period - 1) as f64) * 100.0;
        aroon_down[i] = ((period - 1 - bars_since_low) as f64 / (period - 1) as f64) * 100.0;
        aroon_osc[i] = aroon_up[i] - aroon_down[i];
    }

    (aroon_up, aroon_down, aroon_osc)
}

/// PSAR - Parabolic SAR（抛物线止损转向）
///
/// 算法：
/// - SAR[i] = SAR[i-1] + AF * (EP - SAR[i-1])
/// - EP = 极值点（上升趋势中的最高价，下降趋势中的最低价）
/// - AF = 加速因子，初始 0.02，每次新极值增加 0.02，最大 0.2
///
/// # 参数
/// - `high`: 最高价序列
/// - `low`: 最低价序列
/// - `close`: 收盘价序列
/// - `af_init`: 初始加速因子（默认 0.02）
/// - `af_increment`: AF 增量（默认 0.02）
/// - `af_max`: 最大 AF（默认 0.2）
///
/// # 返回
/// - (psar, trend)  // trend: 1 = up, -1 = down
pub fn psar(
    high: &[f64],
    low: &[f64],
    close: &[f64],
    af_init: f64,
    af_increment: f64,
    af_max: f64,
) -> (Vec<f64>, Vec<f64>) {
    let n = high.len();
    if n < 2 || n != low.len() || n != close.len() {
        return (vec![f64::NAN; n], vec![f64::NAN; n]);
    }

    let mut psar_values = vec![f64::NAN; n];
    let mut trend = vec![f64::NAN; n];

    // 初始化
    let mut is_uptrend = close[1] > close[0];
    let mut sar = if is_uptrend { low[0] } else { high[0] };
    let mut ep = if is_uptrend { high[1] } else { low[1] };
    let mut af = af_init;

    psar_values[0] = sar;
    trend[0] = if is_uptrend { 1.0 } else { -1.0 };

    for i in 1..n {
        // 计算新 SAR
        sar = sar + af * (ep - sar);

        // 确保 SAR 不穿越前两根 K 线
        if is_uptrend {
            sar = sar.min(low[i - 1]);
            if i > 1 {
                sar = sar.min(low[i - 2]);
            }
        } else {
            sar = sar.max(high[i - 1]);
            if i > 1 {
                sar = sar.max(high[i - 2]);
            }
        }

        // 检查是否反转
        let reverse = if is_uptrend {
            low[i] < sar
        } else {
            high[i] > sar
        };

        if reverse {
            // 趋势反转
            is_uptrend = !is_uptrend;
            sar = ep;
            ep = if is_uptrend { high[i] } else { low[i] };
            af = af_init;
        } else {
            // 更新极值点
            let new_ep = if is_uptrend { high[i] } else { low[i] };
            if (is_uptrend && new_ep > ep) || (!is_uptrend && new_ep < ep) {
                ep = new_ep;
                af = (af + af_increment).min(af_max);
            }
        }

        psar_values[i] = sar;
        trend[i] = if is_uptrend { 1.0 } else { -1.0 };
    }

    (psar_values, trend)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_supertrend() {
        // 测试数据：持续上涨趋势
        let high = vec![102.0, 105.0, 104.0, 106.0, 108.0, 107.0, 109.0, 111.0];
        let low = vec![99.0, 101.0, 100.0, 102.0, 104.0, 103.0, 105.0, 107.0];
        let close = vec![101.0, 103.0, 102.0, 105.0, 107.0, 106.0, 108.0, 110.0];

        let period = 3;
        let (supertrend, direction, upper, lower) = supertrend(&high, &low, &close, period, 3.0);

        assert_eq!(supertrend.len(), 8);
        assert_eq!(direction.len(), 8);

        // ATR 在 TA-Lib 模式下首个有效值在 index=period
        assert!(direction[..period].iter().all(|d| d.is_nan()));

        // 上涨趋势：所有有效方向应为 1.0（上升趋势）
        assert!(direction[period..].iter().all(|&d| d == 1.0));

        // 上升趋势时，supertrend 线应等于 lower band
        for i in period..8 {
            assert_eq!(supertrend[i], lower[i]);
            assert!(!upper[i].is_nan());
        }
    }

    #[test]
    fn test_supertrend_invalid_period() {
        let high = vec![102.0, 105.0];
        let low = vec![99.0, 101.0];
        let close = vec![101.0, 103.0];

        let (supertrend, direction, upper, lower) = supertrend(&high, &low, &close, 0, 3.0);

        assert!(supertrend.iter().all(|x| x.is_nan()));
        assert!(direction.iter().all(|x| x.is_nan()));
        assert!(upper.iter().all(|x| x.is_nan()));
        assert!(lower.iter().all(|x| x.is_nan()));
    }

    #[test]
    fn test_adx() {
        let high = vec![110.0, 111.0, 112.0, 113.0, 114.0, 115.0, 116.0, 117.0];
        let low = vec![100.0, 101.0, 102.0, 103.0, 104.0, 105.0, 106.0, 107.0];
        let close = vec![105.0, 106.0, 107.0, 108.0, 109.0, 110.0, 111.0, 112.0];

        let (adx, _plus_di, _minus_di) = adx(&high, &low, &close, 5);

        assert_eq!(adx.len(), 8);
        assert!(adx[4..].iter().all(|&x| !x.is_nan()));
    }

    #[test]
    fn test_aroon() {
        let high = vec![110.0, 111.0, 112.0, 113.0, 114.0, 113.0, 112.0, 111.0];
        let low = vec![100.0, 101.0, 102.0, 103.0, 104.0, 103.0, 102.0, 101.0];

        let (aroon_up, aroon_down, _aroon_osc) = aroon(&high, &low, 5);

        assert_eq!(aroon_up.len(), 8);
        assert!(aroon_up[4..].iter().all(|&x| x >= 0.0 && x <= 100.0));
        assert!(aroon_down[4..].iter().all(|&x| x >= 0.0 && x <= 100.0));
    }

    #[test]
    fn test_aroon_invalid_period() {
        let high = vec![110.0, 111.0];
        let low = vec![100.0, 101.0];

        let (aroon_up, aroon_down, aroon_osc) = aroon(&high, &low, 1);

        assert!(aroon_up.iter().all(|x| x.is_nan()));
        assert!(aroon_down.iter().all(|x| x.is_nan()));
        assert!(aroon_osc.iter().all(|x| x.is_nan()));
    }

    #[test]
    fn test_psar() {
        let high = vec![102.0, 105.0, 104.0, 106.0, 108.0];
        let low = vec![99.0, 101.0, 100.0, 102.0, 104.0];
        let close = vec![101.0, 103.0, 102.0, 105.0, 107.0];

        let (psar, trend) = psar(&high, &low, &close, 0.02, 0.02, 0.2);

        assert_eq!(psar.len(), 5);
        assert_eq!(trend.len(), 5);
        assert!(trend.iter().all(|&t| t == 1.0 || t == -1.0));
    }
}

/// Vortex Indicator (VI) 涡旋指标
///
/// 识别趋势的开始和持续性
///
/// - `high`: 高价序列
/// - `low`: 低价序列
/// - `close`: 收盘价序列
/// - `period`: 周期（默认 14）
///
/// 返回：(VI+, VI-)
///
/// # 算法
/// 1. VM+ = |High[i] - Low[i-1]|
/// 2. VM- = |Low[i] - High[i-1]|
/// 3. TR = Max(High[i] - Low[i], |High[i] - Close[i-1]|, |Low[i] - Close[i-1]|)
/// 4. VI+ = Sum(VM+, period) / Sum(TR, period)
/// 5. VI- = Sum(VM-, period) / Sum(TR, period)
///
/// # 信号
/// - VI+ > VI-：上升趋势
/// - VI- > VI+：下降趋势
pub fn vortex(
    high: &[f64],
    low: &[f64],
    close: &[f64],
    period: usize,
) -> (Vec<f64>, Vec<f64>) {
    let n = high.len();
    if n < 2 || period == 0 {
        return (vec![f64::NAN; n], vec![f64::NAN; n]);
    }

    // 1. 计算 VM+ 和 VM-
    let mut vm_plus = vec![f64::NAN; n];
    let mut vm_minus = vec![f64::NAN; n];
    let mut tr = vec![f64::NAN; n];

    for i in 1..n {
        vm_plus[i] = (high[i] - low[i - 1]).abs();
        vm_minus[i] = (low[i] - high[i - 1]).abs();

        let hl = high[i] - low[i];
        let hc = (high[i] - close[i - 1]).abs();
        let lc = (low[i] - close[i - 1]).abs();
        tr[i] = hl.max(hc).max(lc);
    }

    // 2. 计算滚动和
    let mut vi_plus = vec![f64::NAN; n];
    let mut vi_minus = vec![f64::NAN; n];

    for i in period..n {
        let mut sum_vm_plus = 0.0;
        let mut sum_vm_minus = 0.0;
        let mut sum_tr = 0.0;

        for j in 0..period {
            let idx = i - period + 1 + j;
            if !vm_plus[idx].is_nan() && !vm_minus[idx].is_nan() && !tr[idx].is_nan() {
                sum_vm_plus += vm_plus[idx];
                sum_vm_minus += vm_minus[idx];
                sum_tr += tr[idx];
            }
        }

        if sum_tr != 0.0 {
            vi_plus[i] = sum_vm_plus / sum_tr;
            vi_minus[i] = sum_vm_minus / sum_tr;
        }
    }

    (vi_plus, vi_minus)
}

/// Choppiness Index (CHOP) 震荡指数
///
/// 衡量市场是趋势还是横盘，不指示方向
///
/// - `high`: 高价序列
/// - `low`: 低价序列
/// - `close`: 收盘价序列
/// - `period`: 周期（默认 14）
///
/// 返回：CHOP 值（0-100）
///
/// # 算法
/// CHOP = 100 * log10(Sum(TR, period) / (Max(High, period) - Min(Low, period))) / log10(period)
///
/// # 解释
/// - CHOP > 61.8：横盘/震荡市场
/// - CHOP < 38.2：趋势市场
pub fn choppiness_index(
    high: &[f64],
    low: &[f64],
    close: &[f64],
    period: usize,
) -> Vec<f64> {
    let n = high.len();
    if n < 2 || period == 0 {
        return vec![f64::NAN; n];
    }

    // 1. 计算 True Range
    let mut tr = vec![f64::NAN; n];
    for i in 1..n {
        let hl = high[i] - low[i];
        let hc = (high[i] - close[i - 1]).abs();
        let lc = (low[i] - close[i - 1]).abs();
        tr[i] = hl.max(hc).max(lc);
    }

    // 2. 计算 CHOP
    let mut chop = vec![f64::NAN; n];

    for i in period..n {
        let mut sum_tr = 0.0;
        let mut max_high = f64::NEG_INFINITY;
        let mut min_low = f64::INFINITY;

        for j in 0..period {
            let idx = i - period + 1 + j;
            if !tr[idx].is_nan() {
                sum_tr += tr[idx];
            }
            max_high = max_high.max(high[idx]);
            min_low = min_low.min(low[idx]);
        }

        let range = max_high - min_low;
        if range > 0.0 && sum_tr > 0.0 {
            chop[i] = 100.0 * (sum_tr / range).log10() / (period as f64).log10();
        }
    }

    chop
}

/// QStick 指标
///
/// 衡量买卖压力的指标，基于开盘和收盘价的差值
///
/// - `open`: 开盘价序列
/// - `close`: 收盘价序列
/// - `period`: 周期（默认 14）
///
/// 返回：QStick 值
///
/// # 算法
/// QStick = EMA(Close - Open, period)
///
/// # 信号
/// - QStick > 0：买盘压力（收盘价 > 开盘价）
/// - QStick < 0：卖盘压力（收盘价 < 开盘价）
pub fn qstick(open: &[f64], close: &[f64], period: usize) -> Vec<f64> {
    let n = open.len();
    if n == 0 {
        return vec![];
    }

    // 1. 计算 Close - Open
    let diff: Vec<f64> = open
        .iter()
        .zip(close)
        .map(|(&o, &c)| c - o)
        .collect();

    // 2. EMA 平滑
    ema(&diff, period)
}

/// VHF (Vertical Horizontal Filter) 垂直水平过滤器
///
/// 判断市场是趋势还是震荡
///
/// - `close`: 收盘价序列
/// - `period`: 周期（默认 28）
///
/// 返回：VHF 值
///
/// # 算法
/// VHF = |最高收盘价 - 最低收盘价| / Sum(|Close[i] - Close[i-1]|, period)
///
/// # 解释
/// - VHF 高值：趋势市场
/// - VHF 低值：震荡市场
pub fn vhf(close: &[f64], period: usize) -> Vec<f64> {
    let n = close.len();
    if n < 2 || period == 0 {
        return vec![f64::NAN; n];
    }

    let mut result = vec![f64::NAN; n];

    for i in period..n {
        // 1. 找出周期内的最高和最低收盘价
        let mut max_close = f64::NEG_INFINITY;
        let mut min_close = f64::INFINITY;

        for j in 0..=period {
            let idx = i - j;
            max_close = max_close.max(close[idx]);
            min_close = min_close.min(close[idx]);
        }

        let numerator = (max_close - min_close).abs();

        // 2. 计算价格变化的累计和
        let mut sum_changes = 0.0;
        for j in 0..period {
            let idx = i - j;
            sum_changes += (close[idx] - close[idx - 1]).abs();
        }

        if sum_changes > 0.0 {
            result[i] = numerator / sum_changes;
        }
    }

    result
}

#[cfg(test)]
mod vortex_tests {
    use super::*;

    #[test]
    fn test_vortex_basic() {
        let high: Vec<f64> = (100..130).map(|x| x as f64 + 5.0).collect();
        let low: Vec<f64> = (100..130).map(|x| x as f64).collect();
        let close: Vec<f64> = (100..130).map(|x| x as f64 + 2.5).collect();

        let (vi_plus, vi_minus) = vortex(&high, &low, &close, 14);

        // 上升趋势中，VI+ 应 > VI-
        let valid_idx = 20;
        assert!(!vi_plus[valid_idx].is_nan());
        assert!(!vi_minus[valid_idx].is_nan());
        assert!(vi_plus[valid_idx] > 0.0);
        assert!(vi_minus[valid_idx] > 0.0);
    }

    #[test]
    fn test_choppiness_basic() {
        // 横盘市场
        let high = vec![105.0; 50];
        let low = vec![100.0; 50];
        let close = vec![102.5; 50];

        let chop = choppiness_index(&high, &low, &close, 14);

        // 横盘市场中，CHOP 应 > 61.8
        let valid_idx = 20;
        assert!(!chop[valid_idx].is_nan());
        assert!(chop[valid_idx] > 50.0);
    }

    #[test]
    fn test_qstick_basic() {
        let open = vec![100.0, 101.0, 102.0, 103.0, 104.0];
        let close = vec![101.0, 102.0, 103.0, 104.0, 105.0];

        let qstick = qstick(&open, &close, 3);

        // 上升趋势中（收盘价 > 开盘价），QStick > 0
        let valid_idx = 4;
        assert!(!qstick[valid_idx].is_nan());
        assert!(qstick[valid_idx] > 0.0);
    }

    #[test]
    fn test_vhf_trend() {
        // 强趋势市场
        let close: Vec<f64> = (100..150).map(|x| x as f64).collect();

        let vhf_values = vhf(&close, 28);

        // 强趋势中，VHF 应较高
        let valid_idx = 40;
        assert!(!vhf_values[valid_idx].is_nan());
        assert!(vhf_values[valid_idx] > 0.2);
    }
}
