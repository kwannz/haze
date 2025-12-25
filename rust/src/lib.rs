// lib.rs - Haze-Library Rust 扩展模块
//
// PyO3 入口点，暴露所有指标函数给 Python

#[cfg(feature = "python")]
use pyo3::prelude::*;

mod types;
mod utils;
mod indicators;

#[cfg(feature = "python")]
use types::{Candle, IndicatorResult, MultiIndicatorResult};

// ==================== PyO3 模块定义 ====================

#[cfg(feature = "python")]
#[pymodule]
fn _haze_rust(_py: Python, m: &PyModule) -> PyResult<()> {
    // 类型
    m.add_class::<Candle>()?;
    m.add_class::<IndicatorResult>()?;
    m.add_class::<MultiIndicatorResult>()?;

    // Volatility 指标
    m.add_function(wrap_pyfunction!(py_true_range, m)?)?;
    m.add_function(wrap_pyfunction!(py_atr, m)?)?;
    m.add_function(wrap_pyfunction!(py_natr, m)?)?;
    m.add_function(wrap_pyfunction!(py_bollinger_bands, m)?)?;
    m.add_function(wrap_pyfunction!(py_keltner_channel, m)?)?;
    m.add_function(wrap_pyfunction!(py_donchian_channel, m)?)?;

    // Momentum 指标
    m.add_function(wrap_pyfunction!(py_rsi, m)?)?;
    m.add_function(wrap_pyfunction!(py_macd, m)?)?;
    m.add_function(wrap_pyfunction!(py_stochastic, m)?)?;
    m.add_function(wrap_pyfunction!(py_stochrsi, m)?)?;
    m.add_function(wrap_pyfunction!(py_cci, m)?)?;
    m.add_function(wrap_pyfunction!(py_williams_r, m)?)?;
    m.add_function(wrap_pyfunction!(py_awesome_oscillator, m)?)?;
    m.add_function(wrap_pyfunction!(py_fisher_transform, m)?)?;

    // Trend 指标
    m.add_function(wrap_pyfunction!(py_supertrend, m)?)?;
    m.add_function(wrap_pyfunction!(py_adx, m)?)?;
    m.add_function(wrap_pyfunction!(py_aroon, m)?)?;
    m.add_function(wrap_pyfunction!(py_psar, m)?)?;

    // Volume 指标
    m.add_function(wrap_pyfunction!(py_obv, m)?)?;
    m.add_function(wrap_pyfunction!(py_vwap, m)?)?;
    m.add_function(wrap_pyfunction!(py_mfi, m)?)?;
    m.add_function(wrap_pyfunction!(py_cmf, m)?)?;
    m.add_function(wrap_pyfunction!(py_volume_profile, m)?)?;

    // MA/Overlap 指标
    m.add_function(wrap_pyfunction!(py_sma, m)?)?;
    m.add_function(wrap_pyfunction!(py_ema, m)?)?;
    m.add_function(wrap_pyfunction!(py_rma, m)?)?;
    m.add_function(wrap_pyfunction!(py_wma, m)?)?;
    m.add_function(wrap_pyfunction!(py_hma, m)?)?;
    m.add_function(wrap_pyfunction!(py_dema, m)?)?;
    m.add_function(wrap_pyfunction!(py_tema, m)?)?;

    // Fibonacci 指标
    m.add_function(wrap_pyfunction!(py_fib_retracement, m)?)?;
    m.add_function(wrap_pyfunction!(py_fib_extension, m)?)?;

    // Ichimoku 指标
    m.add_function(wrap_pyfunction!(py_ichimoku_cloud, m)?)?;

    // Pivot Points 指标
    m.add_function(wrap_pyfunction!(py_standard_pivots, m)?)?;
    m.add_function(wrap_pyfunction!(py_fibonacci_pivots, m)?)?;
    m.add_function(wrap_pyfunction!(py_camarilla_pivots, m)?)?;


    // 扩展 Momentum 指标
    m.add_function(wrap_pyfunction!(py_kdj, m)?)?;
    m.add_function(wrap_pyfunction!(py_tsi, m)?)?;
    m.add_function(wrap_pyfunction!(py_ultimate_oscillator, m)?)?;
    m.add_function(wrap_pyfunction!(py_mom, m)?)?;
    m.add_function(wrap_pyfunction!(py_roc, m)?)?;

    // 扩展 Trend 指标
    m.add_function(wrap_pyfunction!(py_vortex, m)?)?;
    m.add_function(wrap_pyfunction!(py_choppiness, m)?)?;
    m.add_function(wrap_pyfunction!(py_qstick, m)?)?;
    m.add_function(wrap_pyfunction!(py_vhf, m)?)?;

    // 扩展 Volume 指标
    m.add_function(wrap_pyfunction!(py_ad, m)?)?;
    m.add_function(wrap_pyfunction!(py_pvt, m)?)?;
    m.add_function(wrap_pyfunction!(py_nvi, m)?)?;
    m.add_function(wrap_pyfunction!(py_pvi, m)?)?;
    m.add_function(wrap_pyfunction!(py_eom, m)?)?;

    // 扩展 MA 指标
    m.add_function(wrap_pyfunction!(py_zlma, m)?)?;
    m.add_function(wrap_pyfunction!(py_t3, m)?)?;
    m.add_function(wrap_pyfunction!(py_kama, m)?)?;
    m.add_function(wrap_pyfunction!(py_frama, m)?)?;
    // 蜡烛图形态识别
    m.add_function(wrap_pyfunction!(py_doji, m)?)?;
    m.add_function(wrap_pyfunction!(py_hammer, m)?)?;
    m.add_function(wrap_pyfunction!(py_inverted_hammer, m)?)?;
    m.add_function(wrap_pyfunction!(py_hanging_man, m)?)?;
    m.add_function(wrap_pyfunction!(py_bullish_engulfing, m)?)?;
    m.add_function(wrap_pyfunction!(py_bearish_engulfing, m)?)?;
    m.add_function(wrap_pyfunction!(py_bullish_harami, m)?)?;
    m.add_function(wrap_pyfunction!(py_bearish_harami, m)?)?;
    m.add_function(wrap_pyfunction!(py_piercing_pattern, m)?)?;
    m.add_function(wrap_pyfunction!(py_dark_cloud_cover, m)?)?;
    m.add_function(wrap_pyfunction!(py_morning_star, m)?)?;
    m.add_function(wrap_pyfunction!(py_evening_star, m)?)?;
    m.add_function(wrap_pyfunction!(py_three_white_soldiers, m)?)?;
    m.add_function(wrap_pyfunction!(py_three_black_crows, m)?)?;
    // 统计指标
    m.add_function(wrap_pyfunction!(py_linear_regression, m)?)?;
    m.add_function(wrap_pyfunction!(py_correlation, m)?)?;
    m.add_function(wrap_pyfunction!(py_zscore, m)?)?;
    m.add_function(wrap_pyfunction!(py_covariance, m)?)?;
    m.add_function(wrap_pyfunction!(py_beta, m)?)?;
    m.add_function(wrap_pyfunction!(py_standard_error, m)?)?;
    // 价格变换指标
    m.add_function(wrap_pyfunction!(py_avgprice, m)?)?;
    m.add_function(wrap_pyfunction!(py_medprice, m)?)?;
    m.add_function(wrap_pyfunction!(py_typprice, m)?)?;
    m.add_function(wrap_pyfunction!(py_wclprice, m)?)?;
    // 数学运算函数
    m.add_function(wrap_pyfunction!(py_max, m)?)?;
    m.add_function(wrap_pyfunction!(py_min, m)?)?;
    m.add_function(wrap_pyfunction!(py_sum, m)?)?;
    m.add_function(wrap_pyfunction!(py_sqrt, m)?)?;
    m.add_function(wrap_pyfunction!(py_ln, m)?)?;
    m.add_function(wrap_pyfunction!(py_log10, m)?)?;
    m.add_function(wrap_pyfunction!(py_exp, m)?)?;
    m.add_function(wrap_pyfunction!(py_abs, m)?)?;
    m.add_function(wrap_pyfunction!(py_ceil, m)?)?;
    m.add_function(wrap_pyfunction!(py_floor, m)?)?;
    m.add_function(wrap_pyfunction!(py_sin, m)?)?;
    m.add_function(wrap_pyfunction!(py_cos, m)?)?;
    m.add_function(wrap_pyfunction!(py_tan, m)?)?;
    m.add_function(wrap_pyfunction!(py_asin, m)?)?;
    m.add_function(wrap_pyfunction!(py_acos, m)?)?;
    m.add_function(wrap_pyfunction!(py_atan, m)?)?;
    m.add_function(wrap_pyfunction!(py_sinh, m)?)?;
    m.add_function(wrap_pyfunction!(py_cosh, m)?)?;
    m.add_function(wrap_pyfunction!(py_tanh, m)?)?;
    m.add_function(wrap_pyfunction!(py_add, m)?)?;
    m.add_function(wrap_pyfunction!(py_sub, m)?)?;
    m.add_function(wrap_pyfunction!(py_mult, m)?)?;
    m.add_function(wrap_pyfunction!(py_div, m)?)?;
    m.add_function(wrap_pyfunction!(py_minmax, m)?)?;
    m.add_function(wrap_pyfunction!(py_minmaxindex, m)?)?;
    // 扩展蜡烛图形态
    m.add_function(wrap_pyfunction!(py_shooting_star, m)?)?;
    m.add_function(wrap_pyfunction!(py_marubozu, m)?)?;
    m.add_function(wrap_pyfunction!(py_spinning_top, m)?)?;
    m.add_function(wrap_pyfunction!(py_dragonfly_doji, m)?)?;
    m.add_function(wrap_pyfunction!(py_gravestone_doji, m)?)?;
    m.add_function(wrap_pyfunction!(py_long_legged_doji, m)?)?;
    m.add_function(wrap_pyfunction!(py_tweezers_top, m)?)?;
    m.add_function(wrap_pyfunction!(py_tweezers_bottom, m)?)?;
    m.add_function(wrap_pyfunction!(py_rising_three_methods, m)?)?;
    m.add_function(wrap_pyfunction!(py_falling_three_methods, m)?)?;
    // 新增蜡烛图形态（第二批）
    m.add_function(wrap_pyfunction!(py_harami_cross, m)?)?;
    m.add_function(wrap_pyfunction!(py_morning_doji_star, m)?)?;
    m.add_function(wrap_pyfunction!(py_evening_doji_star, m)?)?;
    m.add_function(wrap_pyfunction!(py_three_inside, m)?)?;
    m.add_function(wrap_pyfunction!(py_three_outside, m)?)?;
    m.add_function(wrap_pyfunction!(py_abandoned_baby, m)?)?;
    m.add_function(wrap_pyfunction!(py_kicking, m)?)?;
    m.add_function(wrap_pyfunction!(py_long_line, m)?)?;
    m.add_function(wrap_pyfunction!(py_short_line, m)?)?;
    m.add_function(wrap_pyfunction!(py_doji_star, m)?)?;
    // 新增蜡烛图形态（第三批）
    m.add_function(wrap_pyfunction!(py_identical_three_crows, m)?)?;
    m.add_function(wrap_pyfunction!(py_stick_sandwich, m)?)?;
    m.add_function(wrap_pyfunction!(py_tristar, m)?)?;
    m.add_function(wrap_pyfunction!(py_upside_gap_two_crows, m)?)?;
    m.add_function(wrap_pyfunction!(py_gap_sidesidewhite, m)?)?;
    m.add_function(wrap_pyfunction!(py_takuri, m)?)?;
    m.add_function(wrap_pyfunction!(py_homing_pigeon, m)?)?;
    m.add_function(wrap_pyfunction!(py_matching_low, m)?)?;
    m.add_function(wrap_pyfunction!(py_separating_lines, m)?)?;
    m.add_function(wrap_pyfunction!(py_thrusting, m)?)?;
    m.add_function(wrap_pyfunction!(py_inneck, m)?)?;
    m.add_function(wrap_pyfunction!(py_onneck, m)?)?;
    m.add_function(wrap_pyfunction!(py_advance_block, m)?)?;
    m.add_function(wrap_pyfunction!(py_stalled_pattern, m)?)?;
    m.add_function(wrap_pyfunction!(py_belthold, m)?)?;
    // 新增蜡烛图形态（第四批 - TA-Lib 61 完整集合补充）
    m.add_function(wrap_pyfunction!(py_concealing_baby_swallow, m)?)?;
    m.add_function(wrap_pyfunction!(py_counterattack, m)?)?;
    m.add_function(wrap_pyfunction!(py_highwave, m)?)?;
    m.add_function(wrap_pyfunction!(py_hikkake, m)?)?;
    m.add_function(wrap_pyfunction!(py_hikkake_mod, m)?)?;
    m.add_function(wrap_pyfunction!(py_ladder_bottom, m)?)?;
    m.add_function(wrap_pyfunction!(py_mat_hold, m)?)?;
    m.add_function(wrap_pyfunction!(py_rickshaw_man, m)?)?;
    m.add_function(wrap_pyfunction!(py_unique_3_river, m)?)?;
    m.add_function(wrap_pyfunction!(py_xside_gap_3_methods, m)?)?;
    m.add_function(wrap_pyfunction!(py_closing_marubozu, m)?)?;
    m.add_function(wrap_pyfunction!(py_breakaway, m)?)?;

    // Overlap Studies 指标
    m.add_function(wrap_pyfunction!(py_midpoint, m)?)?;
    m.add_function(wrap_pyfunction!(py_midprice, m)?)?;
    m.add_function(wrap_pyfunction!(py_trima, m)?)?;
    m.add_function(wrap_pyfunction!(py_sar, m)?)?;
    m.add_function(wrap_pyfunction!(py_sarext, m)?)?;
    m.add_function(wrap_pyfunction!(py_mama, m)?)?;

    // SFG 交易信号指标
    m.add_function(wrap_pyfunction!(py_ai_supertrend, m)?)?;
    m.add_function(wrap_pyfunction!(py_ai_momentum_index, m)?)?;
    m.add_function(wrap_pyfunction!(py_dynamic_macd, m)?)?;
    m.add_function(wrap_pyfunction!(py_atr2_signals, m)?)?;

    // 周期指标 (Hilbert Transform)
    m.add_function(wrap_pyfunction!(py_ht_dcperiod, m)?)?;
    m.add_function(wrap_pyfunction!(py_ht_dcphase, m)?)?;
    m.add_function(wrap_pyfunction!(py_ht_phasor, m)?)?;
    m.add_function(wrap_pyfunction!(py_ht_sine, m)?)?;
    m.add_function(wrap_pyfunction!(py_ht_trendmode, m)?)?;

    // 统计函数 (TA-Lib Compatible)
    m.add_function(wrap_pyfunction!(py_correl, m)?)?;
    m.add_function(wrap_pyfunction!(py_linearreg, m)?)?;
    m.add_function(wrap_pyfunction!(py_linearreg_slope, m)?)?;
    m.add_function(wrap_pyfunction!(py_linearreg_angle, m)?)?;
    m.add_function(wrap_pyfunction!(py_linearreg_intercept, m)?)?;
    m.add_function(wrap_pyfunction!(py_var, m)?)?;
    m.add_function(wrap_pyfunction!(py_tsf, m)?)?;

    // Batch 7: TA-Lib Advanced Indicators (170 → 180)
    // Note: py_ad already registered at line ~80, only new indicators below
    m.add_function(wrap_pyfunction!(py_adosc, m)?)?;
    m.add_function(wrap_pyfunction!(py_apo, m)?)?;
    m.add_function(wrap_pyfunction!(py_ppo, m)?)?;
    m.add_function(wrap_pyfunction!(py_cmo, m)?)?;
    m.add_function(wrap_pyfunction!(py_dx, m)?)?;
    m.add_function(wrap_pyfunction!(py_plus_di, m)?)?;
    m.add_function(wrap_pyfunction!(py_minus_di, m)?)?;
    m.add_function(wrap_pyfunction!(py_t3, m)?)?;
    m.add_function(wrap_pyfunction!(py_kama, m)?)?;

    // Batch 8: pandas-ta 独有指标 (180 → 190)
    m.add_function(wrap_pyfunction!(py_entropy, m)?)?;
    m.add_function(wrap_pyfunction!(py_aberration, m)?)?;
    m.add_function(wrap_pyfunction!(py_squeeze, m)?)?;
    m.add_function(wrap_pyfunction!(py_qqe, m)?)?;
    m.add_function(wrap_pyfunction!(py_cti, m)?)?;
    m.add_function(wrap_pyfunction!(py_er, m)?)?;
    m.add_function(wrap_pyfunction!(py_bias, m)?)?;
    m.add_function(wrap_pyfunction!(py_psl, m)?)?;
    m.add_function(wrap_pyfunction!(py_rvi, m)?)?;
    m.add_function(wrap_pyfunction!(py_inertia, m)?)?;

    // Batch 9: pandas-ta 独有指标（第二批）(190 → 200)
    m.add_function(wrap_pyfunction!(py_alligator, m)?)?;
    m.add_function(wrap_pyfunction!(py_efi, m)?)?;
    m.add_function(wrap_pyfunction!(py_kst, m)?)?;
    m.add_function(wrap_pyfunction!(py_stc, m)?)?;
    m.add_function(wrap_pyfunction!(py_tdfi, m)?)?;
    m.add_function(wrap_pyfunction!(py_wae, m)?)?;
    m.add_function(wrap_pyfunction!(py_smi, m)?)?;
    m.add_function(wrap_pyfunction!(py_coppock, m)?)?;
    m.add_function(wrap_pyfunction!(py_pgo, m)?)?;
    m.add_function(wrap_pyfunction!(py_vwma, m)?)?;

    // Batch 10: 最终批次（202 → 212 指标，达成 100%）
    m.add_function(wrap_pyfunction!(py_alma, m)?)?;
    m.add_function(wrap_pyfunction!(py_vidya, m)?)?;
    m.add_function(wrap_pyfunction!(py_pwma, m)?)?;
    m.add_function(wrap_pyfunction!(py_sinwma, m)?)?;
    m.add_function(wrap_pyfunction!(py_swma, m)?)?;
    m.add_function(wrap_pyfunction!(py_bop, m)?)?;
    m.add_function(wrap_pyfunction!(py_ssl_channel, m)?)?;
    m.add_function(wrap_pyfunction!(py_cfo, m)?)?;
    m.add_function(wrap_pyfunction!(py_slope, m)?)?;
    m.add_function(wrap_pyfunction!(py_percent_rank, m)?)?;

    Ok(())
}

// ==================== Volatility 指标包装 ====================

#[cfg(feature = "python")]
#[pyfunction]
fn py_true_range(high: Vec<f64>, low: Vec<f64>, close: Vec<f64>, drift: Option<usize>) -> PyResult<Vec<f64>> {
    Ok(indicators::true_range(&high, &low, &close, drift.unwrap_or(1)))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_atr(high: Vec<f64>, low: Vec<f64>, close: Vec<f64>, period: Option<usize>) -> PyResult<Vec<f64>> {
    Ok(indicators::atr(&high, &low, &close, period.unwrap_or(14)))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_natr(high: Vec<f64>, low: Vec<f64>, close: Vec<f64>, period: Option<usize>) -> PyResult<Vec<f64>> {
    Ok(indicators::natr(&high, &low, &close, period.unwrap_or(14)))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_bollinger_bands(
    close: Vec<f64>,
    period: Option<usize>,
    std_multiplier: Option<f64>,
) -> PyResult<(Vec<f64>, Vec<f64>, Vec<f64>)> {
    Ok(indicators::bollinger_bands(
        &close,
        period.unwrap_or(20),
        std_multiplier.unwrap_or(2.0),
    ))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_keltner_channel(
    high: Vec<f64>,
    low: Vec<f64>,
    close: Vec<f64>,
    period: Option<usize>,
    atr_period: Option<usize>,
    multiplier: Option<f64>,
) -> PyResult<(Vec<f64>, Vec<f64>, Vec<f64>)> {
    Ok(indicators::keltner_channel(
        &high,
        &low,
        &close,
        period.unwrap_or(20),
        atr_period.unwrap_or(10),
        multiplier.unwrap_or(2.0),
    ))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_donchian_channel(high: Vec<f64>, low: Vec<f64>, period: Option<usize>) -> PyResult<(Vec<f64>, Vec<f64>, Vec<f64>)> {
    Ok(indicators::donchian_channel(&high, &low, period.unwrap_or(20)))
}

// ==================== Momentum 指标包装 ====================

#[cfg(feature = "python")]
#[pyfunction]
fn py_rsi(close: Vec<f64>, period: Option<usize>) -> PyResult<Vec<f64>> {
    Ok(indicators::rsi(&close, period.unwrap_or(14)))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_macd(
    close: Vec<f64>,
    fast_period: Option<usize>,
    slow_period: Option<usize>,
    signal_period: Option<usize>,
) -> PyResult<(Vec<f64>, Vec<f64>, Vec<f64>)> {
    Ok(indicators::macd(
        &close,
        fast_period.unwrap_or(12),
        slow_period.unwrap_or(26),
        signal_period.unwrap_or(9),
    ))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_stochastic(
    high: Vec<f64>,
    low: Vec<f64>,
    close: Vec<f64>,
    k_period: Option<usize>,
    d_period: Option<usize>,
) -> PyResult<(Vec<f64>, Vec<f64>)> {
    Ok(indicators::stochastic(
        &high,
        &low,
        &close,
        k_period.unwrap_or(14),
        d_period.unwrap_or(3),
    ))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_stochrsi(
    close: Vec<f64>,
    rsi_period: Option<usize>,
    stoch_period: Option<usize>,
    k_period: Option<usize>,
    d_period: Option<usize>,
) -> PyResult<(Vec<f64>, Vec<f64>)> {
    Ok(indicators::stochrsi(
        &close,
        rsi_period.unwrap_or(14),
        stoch_period.unwrap_or(14),
        k_period.unwrap_or(3),
        d_period.unwrap_or(3),
    ))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_cci(high: Vec<f64>, low: Vec<f64>, close: Vec<f64>, period: Option<usize>) -> PyResult<Vec<f64>> {
    Ok(indicators::cci(&high, &low, &close, period.unwrap_or(20)))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_williams_r(high: Vec<f64>, low: Vec<f64>, close: Vec<f64>, period: Option<usize>) -> PyResult<Vec<f64>> {
    Ok(indicators::williams_r(&high, &low, &close, period.unwrap_or(14)))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_awesome_oscillator(high: Vec<f64>, low: Vec<f64>) -> PyResult<Vec<f64>> {
    Ok(indicators::awesome_oscillator(&high, &low))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_fisher_transform(
    high: Vec<f64>,
    low: Vec<f64>,
    close: Vec<f64>,
    period: Option<usize>,
) -> PyResult<(Vec<f64>, Vec<f64>)> {
    Ok(indicators::fisher_transform(&high, &low, &close, period.unwrap_or(9)))
}

// ==================== Trend 指标包装 ====================

#[cfg(feature = "python")]
#[pyfunction]
fn py_supertrend(
    high: Vec<f64>,
    low: Vec<f64>,
    close: Vec<f64>,
    period: Option<usize>,
    multiplier: Option<f64>,
) -> PyResult<(Vec<f64>, Vec<f64>, Vec<f64>, Vec<f64>)> {
    Ok(indicators::supertrend(
        &high,
        &low,
        &close,
        period.unwrap_or(7),
        multiplier.unwrap_or(3.0),
    ))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_adx(high: Vec<f64>, low: Vec<f64>, close: Vec<f64>, period: Option<usize>) -> PyResult<(Vec<f64>, Vec<f64>, Vec<f64>)> {
    Ok(indicators::adx(&high, &low, &close, period.unwrap_or(14)))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_aroon(high: Vec<f64>, low: Vec<f64>, period: Option<usize>) -> PyResult<(Vec<f64>, Vec<f64>, Vec<f64>)> {
    Ok(indicators::aroon(&high, &low, period.unwrap_or(25)))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_psar(
    high: Vec<f64>,
    low: Vec<f64>,
    close: Vec<f64>,
    af_init: Option<f64>,
    af_increment: Option<f64>,
    af_max: Option<f64>,
) -> PyResult<(Vec<f64>, Vec<f64>)> {
    Ok(indicators::psar(
        &high,
        &low,
        &close,
        af_init.unwrap_or(0.02),
        af_increment.unwrap_or(0.02),
        af_max.unwrap_or(0.2),
    ))
}

// ==================== Volume 指标包装 ====================

#[cfg(feature = "python")]
#[pyfunction]
fn py_obv(close: Vec<f64>, volume: Vec<f64>) -> PyResult<Vec<f64>> {
    Ok(indicators::obv(&close, &volume))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_vwap(
    high: Vec<f64>,
    low: Vec<f64>,
    close: Vec<f64>,
    volume: Vec<f64>,
    period: Option<usize>,
) -> PyResult<Vec<f64>> {
    Ok(indicators::volume::vwap(&high, &low, &close, &volume, period.unwrap_or(0)))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_mfi(
    high: Vec<f64>,
    low: Vec<f64>,
    close: Vec<f64>,
    volume: Vec<f64>,
    period: Option<usize>,
) -> PyResult<Vec<f64>> {
    Ok(indicators::mfi(&high, &low, &close, &volume, period.unwrap_or(14)))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_cmf(
    high: Vec<f64>,
    low: Vec<f64>,
    close: Vec<f64>,
    volume: Vec<f64>,
    period: Option<usize>,
) -> PyResult<Vec<f64>> {
    Ok(indicators::cmf(&high, &low, &close, &volume, period.unwrap_or(20)))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_volume_profile(
    high: Vec<f64>,
    low: Vec<f64>,
    close: Vec<f64>,
    volume: Vec<f64>,
    num_bins: Option<usize>,
) -> PyResult<(Vec<f64>, Vec<f64>, f64)> {
    Ok(indicators::volume_profile(&high, &low, &close, &volume, num_bins.unwrap_or(24)))
}

// ==================== MA/Overlap 指标包装 ====================

#[cfg(feature = "python")]
#[pyfunction]
fn py_sma(values: Vec<f64>, period: usize) -> PyResult<Vec<f64>> {
    Ok(utils::sma(&values, period))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_ema(values: Vec<f64>, period: usize) -> PyResult<Vec<f64>> {
    Ok(utils::ema(&values, period))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_rma(values: Vec<f64>, period: usize) -> PyResult<Vec<f64>> {
    Ok(utils::rma(&values, period))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_wma(values: Vec<f64>, period: usize) -> PyResult<Vec<f64>> {
    Ok(utils::wma(&values, period))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_hma(values: Vec<f64>, period: usize) -> PyResult<Vec<f64>> {
    Ok(utils::hma(&values, period))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_dema(values: Vec<f64>, period: usize) -> PyResult<Vec<f64>> {
    Ok(utils::dema(&values, period))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_tema(values: Vec<f64>, period: usize) -> PyResult<Vec<f64>> {
    Ok(utils::tema(&values, period))
}

// ==================== Fibonacci 指标包装 ====================

#[cfg(feature = "python")]
#[pyfunction]
fn py_fib_retracement(
    start_price: f64,
    end_price: f64,
) -> PyResult<Vec<(String, f64)>> {
    let fib = indicators::fibonacci::fib_retracement(start_price, end_price, None);
    let mut levels: Vec<(String, f64)> = fib.levels.into_iter().collect();
    levels.sort_by(|a, b| a.0.partial_cmp(&b.0).unwrap());
    Ok(levels)
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_fib_extension(
    start_price: f64,
    end_price: f64,
    retracement_price: f64,
) -> PyResult<Vec<(String, f64)>> {
    let ext = indicators::fibonacci::fib_extension(start_price, end_price, retracement_price, None);
    let mut levels: Vec<(String, f64)> = ext.levels.into_iter().collect();
    levels.sort_by(|a, b| a.0.partial_cmp(&b.0).unwrap());
    Ok(levels)
}

// ==================== Ichimoku 指标包装 ====================

#[cfg(feature = "python")]
#[pyfunction]
fn py_ichimoku_cloud(
    high: Vec<f64>,
    low: Vec<f64>,
    close: Vec<f64>,
    tenkan_period: Option<usize>,
    kijun_period: Option<usize>,
    senkou_b_period: Option<usize>,
) -> PyResult<(Vec<f64>, Vec<f64>, Vec<f64>, Vec<f64>, Vec<f64>)> {
    let ichimoku = indicators::ichimoku::ichimoku_cloud(
        &high,
        &low,
        &close,
        tenkan_period.unwrap_or(9),
        kijun_period.unwrap_or(26),
        senkou_b_period.unwrap_or(52),
    );

    Ok((
        ichimoku.tenkan_sen,
        ichimoku.kijun_sen,
        ichimoku.senkou_span_a,
        ichimoku.senkou_span_b,
        ichimoku.chikou_span,
    ))
}

// ==================== Pivot Points 指标包装 ====================

#[cfg(feature = "python")]
#[pyfunction]
fn py_standard_pivots(
    high: f64,
    low: f64,
    close: f64,
) -> PyResult<(f64, f64, f64, f64, f64, f64, f64)> {
    let pivots = indicators::pivots::standard_pivots(high, low, close);
    Ok((
        pivots.pivot,
        pivots.r1,
        pivots.r2,
        pivots.r3,
        pivots.s1,
        pivots.s2,
        pivots.s3,
    ))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_fibonacci_pivots(
    high: f64,
    low: f64,
    close: f64,
) -> PyResult<(f64, f64, f64, f64, f64, f64, f64)> {
    let pivots = indicators::pivots::fibonacci_pivots(high, low, close);
    Ok((
        pivots.pivot,
        pivots.r1,
        pivots.r2,
        pivots.r3,
        pivots.s1,
        pivots.s2,
        pivots.s3,
    ))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_camarilla_pivots(
    high: f64,
    low: f64,
    close: f64,
) -> PyResult<(f64, f64, f64, f64, f64, f64, f64, f64, f64)> {
    let pivots = indicators::pivots::camarilla_pivots(high, low, close);
    Ok((
        pivots.pivot,
        pivots.r1,
        pivots.r2,
        pivots.r3,
        pivots.r4.unwrap_or(f64::NAN),
        pivots.s1,
        pivots.s2,
        pivots.s3,
        pivots.s4.unwrap_or(f64::NAN),
    ))
}

// ==================== 扩展 Momentum 指标包装 ====================

#[cfg(feature = "python")]
#[pyfunction]
fn py_kdj(
    high: Vec<f64>,
    low: Vec<f64>,
    close: Vec<f64>,
    k_period: Option<usize>,
    d_period: Option<usize>,
) -> PyResult<(Vec<f64>, Vec<f64>, Vec<f64>)> {
    Ok(indicators::kdj(&high, &low, &close, k_period.unwrap_or(9), d_period.unwrap_or(3)))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_tsi(
    close: Vec<f64>,
    long_period: Option<usize>,
    short_period: Option<usize>,
    signal_period: Option<usize>,
) -> PyResult<(Vec<f64>, Vec<f64>)> {
    Ok(indicators::tsi(&close, long_period.unwrap_or(25), short_period.unwrap_or(13), signal_period.unwrap_or(13)))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_ultimate_oscillator(
    high: Vec<f64>,
    low: Vec<f64>,
    close: Vec<f64>,
    period1: Option<usize>,
    period2: Option<usize>,
    period3: Option<usize>,
) -> PyResult<Vec<f64>> {
    Ok(indicators::ultimate_oscillator(&high, &low, &close, period1.unwrap_or(7), period2.unwrap_or(14), period3.unwrap_or(28)))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_mom(values: Vec<f64>, period: Option<usize>) -> PyResult<Vec<f64>> {
    Ok(utils::stats::momentum(&values, period.unwrap_or(10)))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_roc(values: Vec<f64>, period: Option<usize>) -> PyResult<Vec<f64>> {
    Ok(utils::stats::roc(&values, period.unwrap_or(10)))
}

// ==================== 扩展 Trend 指标包装 ====================

#[cfg(feature = "python")]
#[pyfunction]
fn py_vortex(
    high: Vec<f64>,
    low: Vec<f64>,
    close: Vec<f64>,
    period: Option<usize>,
) -> PyResult<(Vec<f64>, Vec<f64>)> {
    Ok(indicators::vortex(&high, &low, &close, period.unwrap_or(14)))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_choppiness(
    high: Vec<f64>,
    low: Vec<f64>,
    close: Vec<f64>,
    period: Option<usize>,
) -> PyResult<Vec<f64>> {
    Ok(indicators::choppiness_index(&high, &low, &close, period.unwrap_or(14)))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_qstick(
    open: Vec<f64>,
    close: Vec<f64>,
    period: Option<usize>,
) -> PyResult<Vec<f64>> {
    Ok(indicators::qstick(&open, &close, period.unwrap_or(14)))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_vhf(close: Vec<f64>, period: Option<usize>) -> PyResult<Vec<f64>> {
    Ok(indicators::vhf(&close, period.unwrap_or(28)))
}

// ==================== 扩展 Volume 指标包装 ====================

#[cfg(feature = "python")]
#[pyfunction]
fn py_ad(
    high: Vec<f64>,
    low: Vec<f64>,
    close: Vec<f64>,
    volume: Vec<f64>,
) -> PyResult<Vec<f64>> {
    Ok(indicators::accumulation_distribution(&high, &low, &close, &volume))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_pvt(close: Vec<f64>, volume: Vec<f64>) -> PyResult<Vec<f64>> {
    Ok(indicators::price_volume_trend(&close, &volume))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_nvi(close: Vec<f64>, volume: Vec<f64>) -> PyResult<Vec<f64>> {
    Ok(indicators::negative_volume_index(&close, &volume))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_pvi(close: Vec<f64>, volume: Vec<f64>) -> PyResult<Vec<f64>> {
    Ok(indicators::positive_volume_index(&close, &volume))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_eom(
    high: Vec<f64>,
    low: Vec<f64>,
    volume: Vec<f64>,
    period: Option<usize>,
) -> PyResult<Vec<f64>> {
    Ok(indicators::ease_of_movement(&high, &low, &volume, period.unwrap_or(14)))
}

// ==================== 扩展 MA 指标包装 ====================

#[cfg(feature = "python")]
#[pyfunction]
fn py_zlma(values: Vec<f64>, period: usize) -> PyResult<Vec<f64>> {
    Ok(utils::zlma(&values, period))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_t3(values: Vec<f64>, period: usize, v_factor: Option<f64>) -> PyResult<Vec<f64>> {
    Ok(utils::t3(&values, period, v_factor.unwrap_or(0.7)))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_kama(
    values: Vec<f64>,
    period: Option<usize>,
    fast_period: Option<usize>,
    slow_period: Option<usize>,
) -> PyResult<Vec<f64>> {
    Ok(utils::kama(&values, period.unwrap_or(10), fast_period.unwrap_or(2), slow_period.unwrap_or(30)))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_frama(values: Vec<f64>, period: Option<usize>) -> PyResult<Vec<f64>> {
    Ok(utils::frama(&values, period.unwrap_or(16)))
}

// ==================== 蜡烛图形态识别包装 ====================

#[cfg(feature = "python")]
#[pyfunction]
fn py_doji(
    open: Vec<f64>,
    high: Vec<f64>,
    low: Vec<f64>,
    close: Vec<f64>,
    body_threshold: Option<f64>,
) -> PyResult<Vec<f64>> {
    Ok(indicators::doji(&open, &high, &low, &close, body_threshold.unwrap_or(0.1)))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_hammer(
    open: Vec<f64>,
    high: Vec<f64>,
    low: Vec<f64>,
    close: Vec<f64>,
) -> PyResult<Vec<f64>> {
    Ok(indicators::hammer(&open, &high, &low, &close))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_inverted_hammer(
    open: Vec<f64>,
    high: Vec<f64>,
    low: Vec<f64>,
    close: Vec<f64>,
) -> PyResult<Vec<f64>> {
    Ok(indicators::inverted_hammer(&open, &high, &low, &close))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_hanging_man(
    open: Vec<f64>,
    high: Vec<f64>,
    low: Vec<f64>,
    close: Vec<f64>,
) -> PyResult<Vec<f64>> {
    Ok(indicators::hanging_man(&open, &high, &low, &close))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_bullish_engulfing(
    open: Vec<f64>,
    close: Vec<f64>,
) -> PyResult<Vec<f64>> {
    Ok(indicators::bullish_engulfing(&open, &close))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_bearish_engulfing(
    open: Vec<f64>,
    close: Vec<f64>,
) -> PyResult<Vec<f64>> {
    Ok(indicators::bearish_engulfing(&open, &close))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_bullish_harami(
    open: Vec<f64>,
    close: Vec<f64>,
) -> PyResult<Vec<f64>> {
    Ok(indicators::bullish_harami(&open, &close))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_bearish_harami(
    open: Vec<f64>,
    close: Vec<f64>,
) -> PyResult<Vec<f64>> {
    Ok(indicators::bearish_harami(&open, &close))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_piercing_pattern(
    open: Vec<f64>,
    low: Vec<f64>,
    close: Vec<f64>,
) -> PyResult<Vec<f64>> {
    Ok(indicators::piercing_pattern(&open, &low, &close))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_dark_cloud_cover(
    open: Vec<f64>,
    high: Vec<f64>,
    close: Vec<f64>,
) -> PyResult<Vec<f64>> {
    Ok(indicators::dark_cloud_cover(&open, &high, &close))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_morning_star(
    open: Vec<f64>,
    high: Vec<f64>,
    low: Vec<f64>,
    close: Vec<f64>,
) -> PyResult<Vec<f64>> {
    Ok(indicators::morning_star(&open, &high, &low, &close))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_evening_star(
    open: Vec<f64>,
    high: Vec<f64>,
    low: Vec<f64>,
    close: Vec<f64>,
) -> PyResult<Vec<f64>> {
    Ok(indicators::evening_star(&open, &high, &low, &close))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_three_white_soldiers(
    open: Vec<f64>,
    high: Vec<f64>,
    close: Vec<f64>,
) -> PyResult<Vec<f64>> {
    Ok(indicators::three_white_soldiers(&open, &high, &close))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_three_black_crows(
    open: Vec<f64>,
    low: Vec<f64>,
    close: Vec<f64>,
) -> PyResult<Vec<f64>> {
    Ok(indicators::three_black_crows(&open, &low, &close))
}

// ==================== 统计指标包装 ====================

#[cfg(feature = "python")]
#[pyfunction]
fn py_linear_regression(
    y_values: Vec<f64>,
    period: usize,
) -> PyResult<(Vec<f64>, Vec<f64>, Vec<f64>)> {
    Ok(utils::linear_regression(&y_values, period))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_correlation(
    x: Vec<f64>,
    y: Vec<f64>,
    period: usize,
) -> PyResult<Vec<f64>> {
    Ok(utils::correlation(&x, &y, period))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_zscore(values: Vec<f64>, period: usize) -> PyResult<Vec<f64>> {
    Ok(utils::zscore(&values, period))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_covariance(
    x: Vec<f64>,
    y: Vec<f64>,
    period: usize,
) -> PyResult<Vec<f64>> {
    Ok(utils::covariance(&x, &y, period))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_beta(
    asset_returns: Vec<f64>,
    benchmark_returns: Vec<f64>,
    period: usize,
) -> PyResult<Vec<f64>> {
    Ok(utils::beta(&asset_returns, &benchmark_returns, period))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_standard_error(y_values: Vec<f64>, period: usize) -> PyResult<Vec<f64>> {
    Ok(utils::standard_error(&y_values, period))
}

// ==================== 价格变换指标包装 ====================

#[cfg(feature = "python")]
#[pyfunction]
fn py_avgprice(
    open: Vec<f64>,
    high: Vec<f64>,
    low: Vec<f64>,
    close: Vec<f64>,
) -> PyResult<Vec<f64>> {
    Ok(indicators::avgprice(&open, &high, &low, &close))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_medprice(high: Vec<f64>, low: Vec<f64>) -> PyResult<Vec<f64>> {
    Ok(indicators::medprice(&high, &low))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_typprice(
    high: Vec<f64>,
    low: Vec<f64>,
    close: Vec<f64>,
) -> PyResult<Vec<f64>> {
    Ok(indicators::typprice(&high, &low, &close))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_wclprice(
    high: Vec<f64>,
    low: Vec<f64>,
    close: Vec<f64>,
) -> PyResult<Vec<f64>> {
    Ok(indicators::wclprice(&high, &low, &close))
}

// ==================== 数学运算函数包装 ====================

#[cfg(feature = "python")]
#[pyfunction]
fn py_max(values: Vec<f64>, period: usize) -> PyResult<Vec<f64>> {
    Ok(utils::max(&values, period))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_min(values: Vec<f64>, period: usize) -> PyResult<Vec<f64>> {
    Ok(utils::min(&values, period))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_sum(values: Vec<f64>, period: usize) -> PyResult<Vec<f64>> {
    Ok(utils::sum(&values, period))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_sqrt(values: Vec<f64>) -> PyResult<Vec<f64>> {
    Ok(utils::sqrt(&values))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_ln(values: Vec<f64>) -> PyResult<Vec<f64>> {
    Ok(utils::ln(&values))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_log10(values: Vec<f64>) -> PyResult<Vec<f64>> {
    Ok(utils::log10(&values))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_exp(values: Vec<f64>) -> PyResult<Vec<f64>> {
    Ok(utils::exp(&values))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_abs(values: Vec<f64>) -> PyResult<Vec<f64>> {
    Ok(utils::abs(&values))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_ceil(values: Vec<f64>) -> PyResult<Vec<f64>> {
    Ok(utils::ceil(&values))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_floor(values: Vec<f64>) -> PyResult<Vec<f64>> {
    Ok(utils::floor(&values))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_sin(values: Vec<f64>) -> PyResult<Vec<f64>> {
    Ok(utils::sin(&values))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_cos(values: Vec<f64>) -> PyResult<Vec<f64>> {
    Ok(utils::cos(&values))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_tan(values: Vec<f64>) -> PyResult<Vec<f64>> {
    Ok(utils::tan(&values))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_asin(values: Vec<f64>) -> PyResult<Vec<f64>> {
    Ok(utils::asin(&values))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_acos(values: Vec<f64>) -> PyResult<Vec<f64>> {
    Ok(utils::acos(&values))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_atan(values: Vec<f64>) -> PyResult<Vec<f64>> {
    Ok(utils::atan(&values))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_sinh(values: Vec<f64>) -> PyResult<Vec<f64>> {
    Ok(utils::sinh(&values))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_cosh(values: Vec<f64>) -> PyResult<Vec<f64>> {
    Ok(utils::cosh(&values))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_tanh(values: Vec<f64>) -> PyResult<Vec<f64>> {
    Ok(utils::tanh(&values))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_add(values1: Vec<f64>, values2: Vec<f64>) -> PyResult<Vec<f64>> {
    Ok(utils::add(&values1, &values2))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_sub(values1: Vec<f64>, values2: Vec<f64>) -> PyResult<Vec<f64>> {
    Ok(utils::sub(&values1, &values2))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_mult(values1: Vec<f64>, values2: Vec<f64>) -> PyResult<Vec<f64>> {
    Ok(utils::mult(&values1, &values2))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_div(values1: Vec<f64>, values2: Vec<f64>) -> PyResult<Vec<f64>> {
    Ok(utils::div(&values1, &values2))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_minmax(values: Vec<f64>, period: usize) -> PyResult<(Vec<f64>, Vec<f64>)> {
    Ok(utils::minmax(&values, period))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_minmaxindex(values: Vec<f64>, period: usize) -> PyResult<(Vec<f64>, Vec<f64>)> {
    Ok(utils::minmaxindex(&values, period))
}

// ==================== 扩展蜡烛图形态包装 ====================

#[cfg(feature = "python")]
#[pyfunction]
fn py_shooting_star(
    open: Vec<f64>,
    high: Vec<f64>,
    low: Vec<f64>,
    close: Vec<f64>,
) -> PyResult<Vec<f64>> {
    Ok(indicators::shooting_star(&open, &high, &low, &close))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_marubozu(
    open: Vec<f64>,
    high: Vec<f64>,
    low: Vec<f64>,
    close: Vec<f64>,
) -> PyResult<Vec<f64>> {
    Ok(indicators::marubozu(&open, &high, &low, &close))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_spinning_top(
    open: Vec<f64>,
    high: Vec<f64>,
    low: Vec<f64>,
    close: Vec<f64>,
) -> PyResult<Vec<f64>> {
    Ok(indicators::spinning_top(&open, &high, &low, &close))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_dragonfly_doji(
    open: Vec<f64>,
    high: Vec<f64>,
    low: Vec<f64>,
    close: Vec<f64>,
    body_threshold: Option<f64>,
) -> PyResult<Vec<f64>> {
    Ok(indicators::dragonfly_doji(&open, &high, &low, &close, body_threshold.unwrap_or(0.1)))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_gravestone_doji(
    open: Vec<f64>,
    high: Vec<f64>,
    low: Vec<f64>,
    close: Vec<f64>,
    body_threshold: Option<f64>,
) -> PyResult<Vec<f64>> {
    Ok(indicators::gravestone_doji(&open, &high, &low, &close, body_threshold.unwrap_or(0.1)))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_long_legged_doji(
    open: Vec<f64>,
    high: Vec<f64>,
    low: Vec<f64>,
    close: Vec<f64>,
    body_threshold: Option<f64>,
) -> PyResult<Vec<f64>> {
    Ok(indicators::long_legged_doji(&open, &high, &low, &close, body_threshold.unwrap_or(0.1)))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_tweezers_top(
    open: Vec<f64>,
    high: Vec<f64>,
    close: Vec<f64>,
    tolerance: Option<f64>,
) -> PyResult<Vec<f64>> {
    Ok(indicators::tweezers_top(&open, &high, &close, tolerance.unwrap_or(0.01)))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_tweezers_bottom(
    open: Vec<f64>,
    low: Vec<f64>,
    close: Vec<f64>,
    tolerance: Option<f64>,
) -> PyResult<Vec<f64>> {
    Ok(indicators::tweezers_bottom(&open, &low, &close, tolerance.unwrap_or(0.01)))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_rising_three_methods(
    open: Vec<f64>,
    high: Vec<f64>,
    low: Vec<f64>,
    close: Vec<f64>,
) -> PyResult<Vec<f64>> {
    Ok(indicators::rising_three_methods(&open, &high, &low, &close))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_falling_three_methods(
    open: Vec<f64>,
    high: Vec<f64>,
    low: Vec<f64>,
    close: Vec<f64>,
) -> PyResult<Vec<f64>> {
    Ok(indicators::falling_three_methods(&open, &high, &low, &close))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_harami_cross(
    open: Vec<f64>,
    high: Vec<f64>,
    low: Vec<f64>,
    close: Vec<f64>,
    body_threshold: Option<f64>,
) -> PyResult<Vec<f64>> {
    Ok(indicators::harami_cross(&open, &high, &low, &close, body_threshold.unwrap_or(0.1)))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_morning_doji_star(
    open: Vec<f64>,
    high: Vec<f64>,
    low: Vec<f64>,
    close: Vec<f64>,
    body_threshold: Option<f64>,
) -> PyResult<Vec<f64>> {
    Ok(indicators::morning_doji_star(&open, &high, &low, &close, body_threshold.unwrap_or(0.1)))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_evening_doji_star(
    open: Vec<f64>,
    high: Vec<f64>,
    low: Vec<f64>,
    close: Vec<f64>,
    body_threshold: Option<f64>,
) -> PyResult<Vec<f64>> {
    Ok(indicators::evening_doji_star(&open, &high, &low, &close, body_threshold.unwrap_or(0.1)))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_three_inside(
    open: Vec<f64>,
    high: Vec<f64>,
    low: Vec<f64>,
    close: Vec<f64>,
) -> PyResult<Vec<f64>> {
    Ok(indicators::three_inside(&open, &high, &low, &close))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_three_outside(
    open: Vec<f64>,
    high: Vec<f64>,
    low: Vec<f64>,
    close: Vec<f64>,
) -> PyResult<Vec<f64>> {
    Ok(indicators::three_outside(&open, &high, &low, &close))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_abandoned_baby(
    open: Vec<f64>,
    high: Vec<f64>,
    low: Vec<f64>,
    close: Vec<f64>,
    body_threshold: Option<f64>,
) -> PyResult<Vec<f64>> {
    Ok(indicators::abandoned_baby(&open, &high, &low, &close, body_threshold.unwrap_or(0.1)))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_kicking(
    open: Vec<f64>,
    high: Vec<f64>,
    low: Vec<f64>,
    close: Vec<f64>,
) -> PyResult<Vec<f64>> {
    Ok(indicators::kicking(&open, &high, &low, &close))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_long_line(
    open: Vec<f64>,
    high: Vec<f64>,
    low: Vec<f64>,
    close: Vec<f64>,
    lookback: Option<usize>,
) -> PyResult<Vec<f64>> {
    Ok(indicators::long_line(&open, &high, &low, &close, lookback.unwrap_or(10)))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_short_line(
    open: Vec<f64>,
    high: Vec<f64>,
    low: Vec<f64>,
    close: Vec<f64>,
    lookback: Option<usize>,
) -> PyResult<Vec<f64>> {
    Ok(indicators::short_line(&open, &high, &low, &close, lookback.unwrap_or(10)))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_doji_star(
    open: Vec<f64>,
    high: Vec<f64>,
    low: Vec<f64>,
    close: Vec<f64>,
    body_threshold: Option<f64>,
) -> PyResult<Vec<f64>> {
    Ok(indicators::doji_star(&open, &high, &low, &close, body_threshold.unwrap_or(0.1)))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_identical_three_crows(
    open: Vec<f64>,
    high: Vec<f64>,
    low: Vec<f64>,
    close: Vec<f64>,
) -> PyResult<Vec<f64>> {
    Ok(indicators::identical_three_crows(&open, &high, &low, &close))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_stick_sandwich(
    open: Vec<f64>,
    high: Vec<f64>,
    low: Vec<f64>,
    close: Vec<f64>,
    tolerance: Option<f64>,
) -> PyResult<Vec<f64>> {
    Ok(indicators::stick_sandwich(&open, &high, &low, &close, tolerance.unwrap_or(0.01)))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_tristar(
    open: Vec<f64>,
    high: Vec<f64>,
    low: Vec<f64>,
    close: Vec<f64>,
    body_threshold: Option<f64>,
) -> PyResult<Vec<f64>> {
    Ok(indicators::tristar(&open, &high, &low, &close, body_threshold.unwrap_or(0.1)))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_upside_gap_two_crows(
    open: Vec<f64>,
    high: Vec<f64>,
    low: Vec<f64>,
    close: Vec<f64>,
) -> PyResult<Vec<f64>> {
    Ok(indicators::upside_gap_two_crows(&open, &high, &low, &close))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_gap_sidesidewhite(
    open: Vec<f64>,
    high: Vec<f64>,
    low: Vec<f64>,
    close: Vec<f64>,
) -> PyResult<Vec<f64>> {
    Ok(indicators::gap_sidesidewhite(&open, &high, &low, &close))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_takuri(
    open: Vec<f64>,
    high: Vec<f64>,
    low: Vec<f64>,
    close: Vec<f64>,
) -> PyResult<Vec<f64>> {
    Ok(indicators::takuri(&open, &high, &low, &close))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_homing_pigeon(
    open: Vec<f64>,
    high: Vec<f64>,
    low: Vec<f64>,
    close: Vec<f64>,
) -> PyResult<Vec<f64>> {
    Ok(indicators::homing_pigeon(&open, &high, &low, &close))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_matching_low(
    open: Vec<f64>,
    high: Vec<f64>,
    low: Vec<f64>,
    close: Vec<f64>,
    tolerance: Option<f64>,
) -> PyResult<Vec<f64>> {
    Ok(indicators::matching_low(&open, &high, &low, &close, tolerance.unwrap_or(0.01)))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_separating_lines(
    open: Vec<f64>,
    high: Vec<f64>,
    low: Vec<f64>,
    close: Vec<f64>,
    tolerance: Option<f64>,
) -> PyResult<Vec<f64>> {
    Ok(indicators::separating_lines(&open, &high, &low, &close, tolerance.unwrap_or(0.005)))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_thrusting(
    open: Vec<f64>,
    high: Vec<f64>,
    low: Vec<f64>,
    close: Vec<f64>,
) -> PyResult<Vec<f64>> {
    Ok(indicators::thrusting(&open, &high, &low, &close))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_inneck(
    open: Vec<f64>,
    high: Vec<f64>,
    low: Vec<f64>,
    close: Vec<f64>,
    tolerance: Option<f64>,
) -> PyResult<Vec<f64>> {
    Ok(indicators::inneck(&open, &high, &low, &close, tolerance.unwrap_or(0.01)))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_onneck(
    open: Vec<f64>,
    high: Vec<f64>,
    low: Vec<f64>,
    close: Vec<f64>,
    tolerance: Option<f64>,
) -> PyResult<Vec<f64>> {
    Ok(indicators::onneck(&open, &high, &low, &close, tolerance.unwrap_or(0.01)))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_advance_block(
    open: Vec<f64>,
    high: Vec<f64>,
    low: Vec<f64>,
    close: Vec<f64>,
) -> PyResult<Vec<f64>> {
    Ok(indicators::advance_block(&open, &high, &low, &close))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_stalled_pattern(
    open: Vec<f64>,
    high: Vec<f64>,
    low: Vec<f64>,
    close: Vec<f64>,
) -> PyResult<Vec<f64>> {
    Ok(indicators::stalled_pattern(&open, &high, &low, &close))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_belthold(
    open: Vec<f64>,
    high: Vec<f64>,
    low: Vec<f64>,
    close: Vec<f64>,
) -> PyResult<Vec<f64>> {
    Ok(indicators::belthold(&open, &high, &low, &close))
}

// 新增蜡烛图形态（第四批 - TA-Lib 61 完整集合补充）
#[cfg(feature = "python")]
#[pyfunction]
fn py_concealing_baby_swallow(
    open: Vec<f64>,
    high: Vec<f64>,
    low: Vec<f64>,
    close: Vec<f64>,
) -> PyResult<Vec<f64>> {
    Ok(indicators::concealing_baby_swallow(&open, &high, &low, &close))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_counterattack(
    open: Vec<f64>,
    high: Vec<f64>,
    low: Vec<f64>,
    close: Vec<f64>,
    tolerance: Option<f64>,
) -> PyResult<Vec<f64>> {
    Ok(indicators::counterattack(&open, &high, &low, &close, tolerance.unwrap_or(0.005)))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_highwave(
    open: Vec<f64>,
    high: Vec<f64>,
    low: Vec<f64>,
    close: Vec<f64>,
    body_threshold: Option<f64>,
) -> PyResult<Vec<f64>> {
    Ok(indicators::highwave(&open, &high, &low, &close, body_threshold.unwrap_or(0.15)))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_hikkake(
    open: Vec<f64>,
    high: Vec<f64>,
    low: Vec<f64>,
    close: Vec<f64>,
) -> PyResult<Vec<f64>> {
    Ok(indicators::hikkake(&open, &high, &low, &close))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_hikkake_mod(
    open: Vec<f64>,
    high: Vec<f64>,
    low: Vec<f64>,
    close: Vec<f64>,
) -> PyResult<Vec<f64>> {
    Ok(indicators::hikkake_mod(&open, &high, &low, &close))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_ladder_bottom(
    open: Vec<f64>,
    high: Vec<f64>,
    low: Vec<f64>,
    close: Vec<f64>,
) -> PyResult<Vec<f64>> {
    Ok(indicators::ladder_bottom(&open, &high, &low, &close))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_mat_hold(
    open: Vec<f64>,
    high: Vec<f64>,
    low: Vec<f64>,
    close: Vec<f64>,
) -> PyResult<Vec<f64>> {
    Ok(indicators::mat_hold(&open, &high, &low, &close))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_rickshaw_man(
    open: Vec<f64>,
    high: Vec<f64>,
    low: Vec<f64>,
    close: Vec<f64>,
    body_threshold: Option<f64>,
) -> PyResult<Vec<f64>> {
    Ok(indicators::rickshaw_man(&open, &high, &low, &close, body_threshold.unwrap_or(0.1)))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_unique_3_river(
    open: Vec<f64>,
    high: Vec<f64>,
    low: Vec<f64>,
    close: Vec<f64>,
) -> PyResult<Vec<f64>> {
    Ok(indicators::unique_3_river(&open, &high, &low, &close))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_xside_gap_3_methods(
    open: Vec<f64>,
    high: Vec<f64>,
    low: Vec<f64>,
    close: Vec<f64>,
) -> PyResult<Vec<f64>> {
    Ok(indicators::xside_gap_3_methods(&open, &high, &low, &close))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_closing_marubozu(
    open: Vec<f64>,
    high: Vec<f64>,
    low: Vec<f64>,
    close: Vec<f64>,
) -> PyResult<Vec<f64>> {
    Ok(indicators::closing_marubozu(&open, &high, &low, &close))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_breakaway(
    open: Vec<f64>,
    high: Vec<f64>,
    low: Vec<f64>,
    close: Vec<f64>,
) -> PyResult<Vec<f64>> {
    Ok(indicators::breakaway(&open, &high, &low, &close))
}

// ==================== Overlap Studies 指标包装 ====================
#[cfg(feature = "python")]
#[pyfunction]
fn py_midpoint(values: Vec<f64>, period: usize) -> PyResult<Vec<f64>> {
    Ok(indicators::midpoint(&values, period))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_midprice(high: Vec<f64>, low: Vec<f64>, period: usize) -> PyResult<Vec<f64>> {
    Ok(indicators::midprice(&high, &low, period))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_trima(values: Vec<f64>, period: usize) -> PyResult<Vec<f64>> {
    Ok(indicators::trima(&values, period))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_sar(
    high: Vec<f64>,
    low: Vec<f64>,
    acceleration: Option<f64>,
    maximum: Option<f64>,
) -> PyResult<Vec<f64>> {
    Ok(indicators::sar(
        &high,
        &low,
        acceleration.unwrap_or(0.02),
        maximum.unwrap_or(0.2),
    ))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_sarext(
    high: Vec<f64>,
    low: Vec<f64>,
    start_value: Option<f64>,
    offset_on_reverse: Option<f64>,
    af_init_long: Option<f64>,
    af_long: Option<f64>,
    af_max_long: Option<f64>,
    af_init_short: Option<f64>,
    af_short: Option<f64>,
    af_max_short: Option<f64>,
) -> PyResult<Vec<f64>> {
    Ok(indicators::sarext(
        &high,
        &low,
        start_value.unwrap_or(0.0),
        offset_on_reverse.unwrap_or(0.0),
        af_init_long.unwrap_or(0.02),
        af_long.unwrap_or(0.02),
        af_max_long.unwrap_or(0.2),
        af_init_short.unwrap_or(0.02),
        af_short.unwrap_or(0.02),
        af_max_short.unwrap_or(0.2),
    ))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_mama(
    values: Vec<f64>,
    fast_limit: Option<f64>,
    slow_limit: Option<f64>,
) -> PyResult<(Vec<f64>, Vec<f64>)> {
    Ok(indicators::mama(
        &values,
        fast_limit.unwrap_or(0.5),
        slow_limit.unwrap_or(0.05),
    ))
}

// ==================== SFG 交易信号指标包装 ====================
#[cfg(feature = "python")]
#[pyfunction]
fn py_ai_supertrend(
    high: Vec<f64>,
    low: Vec<f64>,
    close: Vec<f64>,
    k: Option<usize>,
    n: Option<usize>,
    price_trend: Option<usize>,
    predict_trend: Option<usize>,
    st_length: Option<usize>,
    st_multiplier: Option<f64>,
) -> PyResult<(Vec<f64>, Vec<f64>)> {
    Ok(indicators::ai_supertrend(
        &high,
        &low,
        &close,
        k.unwrap_or(5),
        n.unwrap_or(100),
        price_trend.unwrap_or(10),
        predict_trend.unwrap_or(10),
        st_length.unwrap_or(10),
        st_multiplier.unwrap_or(3.0),
    ))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_ai_momentum_index(
    close: Vec<f64>,
    k: Option<usize>,
    trend_length: Option<usize>,
    smooth: Option<usize>,
) -> PyResult<(Vec<f64>, Vec<f64>)> {
    Ok(indicators::ai_momentum_index(
        &close,
        k.unwrap_or(50),
        trend_length.unwrap_or(14),
        smooth.unwrap_or(3),
    ))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_dynamic_macd(
    open: Vec<f64>,
    high: Vec<f64>,
    low: Vec<f64>,
    close: Vec<f64>,
    fast_length: Option<usize>,
    slow_length: Option<usize>,
    signal_smooth: Option<usize>,
) -> PyResult<(Vec<f64>, Vec<f64>, Vec<f64>, Vec<f64>, Vec<f64>)> {
    Ok(indicators::dynamic_macd(
        &open,
        &high,
        &low,
        &close,
        fast_length.unwrap_or(12),
        slow_length.unwrap_or(26),
        signal_smooth.unwrap_or(9),
    ))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_atr2_signals(
    high: Vec<f64>,
    low: Vec<f64>,
    close: Vec<f64>,
    volume: Vec<f64>,
    trend_length: Option<usize>,
    confirmation_threshold: Option<f64>,
    momentum_window: Option<usize>,
) -> PyResult<(Vec<f64>, Vec<f64>, Vec<f64>)> {
    Ok(indicators::atr2_signals(
        &high,
        &low,
        &close,
        &volume,
        trend_length.unwrap_or(14),
        confirmation_threshold.unwrap_or(2.0),
        momentum_window.unwrap_or(10),
    ))
}

// ==================== 周期指标包装 (Hilbert Transform) ====================
#[cfg(feature = "python")]
#[pyfunction]
fn py_ht_dcperiod(values: Vec<f64>) -> PyResult<Vec<f64>> {
    Ok(indicators::ht_dcperiod(&values))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_ht_dcphase(values: Vec<f64>) -> PyResult<Vec<f64>> {
    Ok(indicators::ht_dcphase(&values))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_ht_phasor(values: Vec<f64>) -> PyResult<(Vec<f64>, Vec<f64>)> {
    Ok(indicators::ht_phasor(&values))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_ht_sine(values: Vec<f64>) -> PyResult<(Vec<f64>, Vec<f64>)> {
    Ok(indicators::ht_sine(&values))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_ht_trendmode(values: Vec<f64>) -> PyResult<Vec<f64>> {
    Ok(indicators::ht_trendmode(&values))
}

#[cfg(test)]
mod coverage_tests;

// ==================== 统计函数包装 (TA-Lib Compatible) ====================
#[cfg(feature = "python")]
#[pyfunction]
fn py_correl(values1: Vec<f64>, values2: Vec<f64>, period: usize) -> PyResult<Vec<f64>> {
    Ok(utils::correl(&values1, &values2, period))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_linearreg(values: Vec<f64>, period: usize) -> PyResult<Vec<f64>> {
    Ok(utils::linearreg(&values, period))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_linearreg_slope(values: Vec<f64>, period: usize) -> PyResult<Vec<f64>> {
    Ok(utils::linearreg_slope(&values, period))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_linearreg_angle(values: Vec<f64>, period: usize) -> PyResult<Vec<f64>> {
    Ok(utils::linearreg_angle(&values, period))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_linearreg_intercept(values: Vec<f64>, period: usize) -> PyResult<Vec<f64>> {
    Ok(utils::linearreg_intercept(&values, period))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_var(values: Vec<f64>, period: usize) -> PyResult<Vec<f64>> {
    Ok(utils::var(&values, period))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_tsf(values: Vec<f64>, period: usize) -> PyResult<Vec<f64>> {
    Ok(utils::tsf(&values, period))
}

// ==================== Batch 7: TA-Lib Advanced Indicators ====================
// Volume Indicators (AD already exists at line 766)
#[cfg(feature = "python")]
#[pyfunction]
fn py_adosc(
    high: Vec<f64>,
    low: Vec<f64>,
    close: Vec<f64>,
    volume: Vec<f64>,
    fast_period: Option<usize>,
    slow_period: Option<usize>,
) -> PyResult<Vec<f64>> {
    Ok(indicators::chaikin_ad_oscillator(
        &high,
        &low,
        &close,
        &volume,
        fast_period.unwrap_or(3),
        slow_period.unwrap_or(10),
    ))
}

// Momentum Indicators
#[cfg(feature = "python")]
#[pyfunction]
fn py_apo(
    close: Vec<f64>,
    fast_period: Option<usize>,
    slow_period: Option<usize>,
) -> PyResult<Vec<f64>> {
    Ok(indicators::apo(
        &close,
        fast_period.unwrap_or(12),
        slow_period.unwrap_or(26),
    ))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_ppo(
    close: Vec<f64>,
    fast_period: Option<usize>,
    slow_period: Option<usize>,
) -> PyResult<Vec<f64>> {
    Ok(indicators::ppo(
        &close,
        fast_period.unwrap_or(12),
        slow_period.unwrap_or(26),
    ))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_cmo(close: Vec<f64>, period: Option<usize>) -> PyResult<Vec<f64>> {
    Ok(indicators::cmo(&close, period.unwrap_or(14)))
}

// Trend Indicators
#[cfg(feature = "python")]
#[pyfunction]
fn py_dx(
    high: Vec<f64>,
    low: Vec<f64>,
    close: Vec<f64>,
    period: Option<usize>,
) -> PyResult<Vec<f64>> {
    Ok(indicators::dx(&high, &low, &close, period.unwrap_or(14)))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_plus_di(
    high: Vec<f64>,
    low: Vec<f64>,
    close: Vec<f64>,
    period: Option<usize>,
) -> PyResult<Vec<f64>> {
    Ok(indicators::plus_di(&high, &low, &close, period.unwrap_or(14)))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_minus_di(
    high: Vec<f64>,
    low: Vec<f64>,
    close: Vec<f64>,
    period: Option<usize>,
) -> PyResult<Vec<f64>> {
    Ok(indicators::minus_di(&high, &low, &close, period.unwrap_or(14)))
}

// Overlap Studies (Advanced MA)
#[cfg(feature = "python")]
#[pyfunction]
fn py_t3(
    values: Vec<f64>,
    period: Option<usize>,
    v_factor: Option<f64>,
) -> PyResult<Vec<f64>> {
    Ok(utils::t3(&values, period.unwrap_or(5), v_factor.unwrap_or(0.7)))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_kama(
    values: Vec<f64>,
    period: Option<usize>,
    fast_period: Option<usize>,
    slow_period: Option<usize>,
) -> PyResult<Vec<f64>> {
    Ok(utils::kama(
        &values,
        period.unwrap_or(10),
        fast_period.unwrap_or(2),
        slow_period.unwrap_or(30),
    ))
}

// ==================== Batch 8: pandas-ta 独有指标 (180 → 190) ====================

#[cfg(feature = "python")]
#[pyfunction]
fn py_entropy(
    close: Vec<f64>,
    period: Option<usize>,
    bins: Option<usize>,
) -> PyResult<Vec<f64>> {
    Ok(indicators::entropy(&close, period.unwrap_or(10), bins.unwrap_or(10)))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_aberration(
    high: Vec<f64>,
    low: Vec<f64>,
    close: Vec<f64>,
    period: Option<usize>,
    atr_period: Option<usize>,
) -> PyResult<Vec<f64>> {
    Ok(indicators::aberration(
        &high,
        &low,
        &close,
        period.unwrap_or(20),
        atr_period.unwrap_or(20),
    ))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_squeeze(
    high: Vec<f64>,
    low: Vec<f64>,
    close: Vec<f64>,
    bb_period: Option<usize>,
    bb_std: Option<f64>,
    kc_period: Option<usize>,
    kc_atr_period: Option<usize>,
    kc_mult: Option<f64>,
) -> PyResult<(Vec<f64>, Vec<f64>, Vec<f64>)> {
    Ok(indicators::squeeze(
        &high,
        &low,
        &close,
        bb_period.unwrap_or(20),
        bb_std.unwrap_or(2.0),
        kc_period.unwrap_or(20),
        kc_atr_period.unwrap_or(20),
        kc_mult.unwrap_or(1.5),
    ))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_qqe(
    close: Vec<f64>,
    rsi_period: Option<usize>,
    smooth: Option<usize>,
    multiplier: Option<f64>,
) -> PyResult<(Vec<f64>, Vec<f64>, Vec<f64>)> {
    Ok(indicators::qqe(
        &close,
        rsi_period.unwrap_or(14),
        smooth.unwrap_or(5),
        multiplier.unwrap_or(4.236),
    ))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_cti(close: Vec<f64>, period: Option<usize>) -> PyResult<Vec<f64>> {
    Ok(indicators::cti(&close, period.unwrap_or(12)))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_er(close: Vec<f64>, period: Option<usize>) -> PyResult<Vec<f64>> {
    Ok(indicators::er(&close, period.unwrap_or(10)))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_bias(close: Vec<f64>, period: Option<usize>) -> PyResult<Vec<f64>> {
    Ok(indicators::bias(&close, period.unwrap_or(20)))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_psl(close: Vec<f64>, period: Option<usize>) -> PyResult<Vec<f64>> {
    Ok(indicators::psl(&close, period.unwrap_or(12)))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_rvi(
    open: Vec<f64>,
    high: Vec<f64>,
    low: Vec<f64>,
    close: Vec<f64>,
    period: Option<usize>,
    signal_period: Option<usize>,
) -> PyResult<(Vec<f64>, Vec<f64>)> {
    Ok(indicators::rvi(
        &open,
        &high,
        &low,
        &close,
        period.unwrap_or(10),
        signal_period.unwrap_or(4),
    ))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_inertia(
    open: Vec<f64>,
    high: Vec<f64>,
    low: Vec<f64>,
    close: Vec<f64>,
    rvi_period: Option<usize>,
    regression_period: Option<usize>,
) -> PyResult<Vec<f64>> {
    Ok(indicators::inertia(
        &open,
        &high,
        &low,
        &close,
        rvi_period.unwrap_or(14),
        regression_period.unwrap_or(20),
    ))
}

// ==================== Batch 9: pandas-ta 独有指标（第二批）(190 → 200) ====================

#[cfg(feature = "python")]
#[pyfunction]
fn py_alligator(
    high: Vec<f64>,
    low: Vec<f64>,
    jaw_period: Option<usize>,
    teeth_period: Option<usize>,
    lips_period: Option<usize>,
) -> PyResult<(Vec<f64>, Vec<f64>, Vec<f64>)> {
    Ok(indicators::alligator(
        &high,
        &low,
        jaw_period.unwrap_or(13),
        teeth_period.unwrap_or(8),
        lips_period.unwrap_or(5),
    ))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_efi(
    close: Vec<f64>,
    volume: Vec<f64>,
    period: Option<usize>,
) -> PyResult<Vec<f64>> {
    Ok(indicators::efi(&close, &volume, period.unwrap_or(13)))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_kst(
    close: Vec<f64>,
    roc1: Option<usize>,
    roc2: Option<usize>,
    roc3: Option<usize>,
    roc4: Option<usize>,
    signal_period: Option<usize>,
) -> PyResult<(Vec<f64>, Vec<f64>)> {
    Ok(indicators::kst(
        &close,
        roc1.unwrap_or(10),
        roc2.unwrap_or(15),
        roc3.unwrap_or(20),
        roc4.unwrap_or(30),
        signal_period.unwrap_or(9),
    ))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_stc(
    close: Vec<f64>,
    fast: Option<usize>,
    slow: Option<usize>,
    cycle: Option<usize>,
) -> PyResult<Vec<f64>> {
    Ok(indicators::stc(
        &close,
        fast.unwrap_or(23),
        slow.unwrap_or(50),
        cycle.unwrap_or(10),
    ))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_tdfi(
    close: Vec<f64>,
    period: Option<usize>,
    smooth: Option<usize>,
) -> PyResult<Vec<f64>> {
    Ok(indicators::tdfi(&close, period.unwrap_or(13), smooth.unwrap_or(3)))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_wae(
    close: Vec<f64>,
    fast: Option<usize>,
    slow: Option<usize>,
    signal: Option<usize>,
    bb_period: Option<usize>,
    multiplier: Option<f64>,
) -> PyResult<(Vec<f64>, Vec<f64>)> {
    Ok(indicators::wae(
        &close,
        fast.unwrap_or(20),
        slow.unwrap_or(40),
        signal.unwrap_or(9),
        bb_period.unwrap_or(20),
        multiplier.unwrap_or(2.0),
    ))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_smi(
    high: Vec<f64>,
    low: Vec<f64>,
    close: Vec<f64>,
    period: Option<usize>,
    smooth1: Option<usize>,
    smooth2: Option<usize>,
) -> PyResult<Vec<f64>> {
    Ok(indicators::smi(
        &high,
        &low,
        &close,
        period.unwrap_or(13),
        smooth1.unwrap_or(25),
        smooth2.unwrap_or(2),
    ))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_coppock(
    close: Vec<f64>,
    period1: Option<usize>,
    period2: Option<usize>,
    wma_period: Option<usize>,
) -> PyResult<Vec<f64>> {
    Ok(indicators::coppock(
        &close,
        period1.unwrap_or(11),
        period2.unwrap_or(14),
        wma_period.unwrap_or(10),
    ))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_pgo(
    high: Vec<f64>,
    low: Vec<f64>,
    close: Vec<f64>,
    period: Option<usize>,
) -> PyResult<Vec<f64>> {
    Ok(indicators::pgo(&high, &low, &close, period.unwrap_or(14)))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_vwma(
    close: Vec<f64>,
    volume: Vec<f64>,
    period: Option<usize>,
) -> PyResult<Vec<f64>> {
    Ok(indicators::vwma(&close, &volume, period.unwrap_or(20)))
}

// Batch 10: 最终批次（202 → 212 指标，达成 100%）

#[cfg(feature = "python")]
#[pyfunction]
fn py_alma(
    values: Vec<f64>,
    period: Option<usize>,
    offset: Option<f64>,
    sigma: Option<f64>,
) -> PyResult<Vec<f64>> {
    Ok(indicators::alma(
        &values,
        period.unwrap_or(9),
        offset.unwrap_or(0.85),
        sigma.unwrap_or(6.0),
    ))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_vidya(
    close: Vec<f64>,
    period: Option<usize>,
) -> PyResult<Vec<f64>> {
    Ok(indicators::vidya(&close, period.unwrap_or(14)))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_pwma(
    values: Vec<f64>,
    period: Option<usize>,
) -> PyResult<Vec<f64>> {
    Ok(indicators::pwma(&values, period.unwrap_or(5)))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_sinwma(
    values: Vec<f64>,
    period: Option<usize>,
) -> PyResult<Vec<f64>> {
    Ok(indicators::sinwma(&values, period.unwrap_or(14)))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_swma(
    values: Vec<f64>,
    period: Option<usize>,
) -> PyResult<Vec<f64>> {
    Ok(indicators::swma(&values, period.unwrap_or(7)))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_bop(
    open: Vec<f64>,
    high: Vec<f64>,
    low: Vec<f64>,
    close: Vec<f64>,
) -> PyResult<Vec<f64>> {
    Ok(indicators::bop(&open, &high, &low, &close))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_ssl_channel(
    high: Vec<f64>,
    low: Vec<f64>,
    close: Vec<f64>,
    period: Option<usize>,
) -> PyResult<(Vec<f64>, Vec<f64>)> {
    Ok(indicators::ssl_channel(&high, &low, &close, period.unwrap_or(10)))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_cfo(
    close: Vec<f64>,
    period: Option<usize>,
) -> PyResult<Vec<f64>> {
    Ok(indicators::cfo(&close, period.unwrap_or(14)))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_slope(
    values: Vec<f64>,
    period: Option<usize>,
) -> PyResult<Vec<f64>> {
    Ok(indicators::slope(&values, period.unwrap_or(14)))
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_percent_rank(
    values: Vec<f64>,
    period: Option<usize>,
) -> PyResult<Vec<f64>> {
    Ok(indicators::percent_rank(&values, period.unwrap_or(14)))
}
