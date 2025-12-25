use crate::indicators;
use crate::types::{candles_to_vectors, validate_ohlc, Candle, IndicatorResult, MultiIndicatorResult};

#[test]
fn test_overlap_indicators_extra() {
    let values = vec![1.0, 5.0, 3.0, 4.0, 2.0];
    let high = vec![5.0, 6.0, 7.0, 6.0, 5.0];
    let low = vec![1.0, 2.0, 3.0, 2.0, 1.0];
    let open = vec![2.0, 3.0, 4.0, 3.5, 2.5];
    let close = vec![3.0, 4.0, 5.0, 3.0, 2.0];

    let ohlc4_vals = indicators::overlap::ohlc4(&open, &high, &low, &close);
    assert!((ohlc4_vals[0] - 2.75).abs() < 1e-10);

    let midpoint_vals = indicators::midpoint(&values, 3);
    assert_eq!(midpoint_vals[2], 3.0);

    let midprice_vals = indicators::midprice(&high, &low, 2);
    assert!((midprice_vals[1] - 3.5).abs() < 1e-10);

    let trima_vals = indicators::trima(&values, 3);
    assert_eq!(trima_vals.len(), values.len());

    let sar_vals = indicators::sar(&high, &low, 0.02, 0.2);
    assert_eq!(sar_vals.len(), high.len());

    let sarext_vals = indicators::sarext(&high, &low, 0.0, 0.0, 0.02, 0.02, 0.2, 0.02, 0.02, 0.2);
    assert_eq!(sarext_vals.len(), high.len());

    let (mama_vals, fama_vals) = indicators::mama(&values, 0.5, 0.05);
    assert_eq!(mama_vals.len(), values.len());
    assert_eq!(fama_vals.len(), values.len());
}

#[test]
fn test_overlap_indicators_early_returns() {
    let short = vec![1.0];
    let _ = indicators::sar(&short, &short, 0.02, 0.2);
    let _ = indicators::sarext(&short, &short, 0.0, 0.0, 0.02, 0.02, 0.2, 0.02, 0.02, 0.2);
    let _ = indicators::mama(&short, 0.5, 0.05);
}

#[test]
fn test_harmonics_patterns() {
    use indicators::harmonics::{detect_all_harmonics, detect_bat, detect_butterfly, detect_crab, detect_cypher, detect_gartley, detect_shark, SwingPoint};

    fn swings_from_prices(points: &[(f64, bool)]) -> Vec<SwingPoint> {
        points
            .iter()
            .enumerate()
            .map(|(i, (price, is_high))| SwingPoint { index: i, price: *price, is_high: *is_high })
            .collect()
    }

    let gartley = swings_from_prices(&[
        (0.0, false),
        (100.0, true),
        (38.2, false),
        (69.1, true),
        (21.4, false),
    ]);
    assert!(!detect_gartley(&gartley).is_empty());

    let bat = swings_from_prices(&[
        (0.0, false),
        (100.0, true),
        (50.0, false),
        (75.0, true),
        (11.4, false),
    ]);
    assert!(!detect_bat(&bat).is_empty());

    let butterfly = swings_from_prices(&[
        (0.0, false),
        (100.0, true),
        (21.4, false),
        (60.7, true),
        (-27.0, false),
    ]);
    assert!(!detect_butterfly(&butterfly).is_empty());

    let crab = swings_from_prices(&[
        (0.0, false),
        (100.0, true),
        (50.0, false),
        (94.3, true),
        (-61.8, false),
    ]);
    assert!(!detect_crab(&crab).is_empty());

    let shark = swings_from_prices(&[
        (0.0, false),
        (100.0, true),
        (50.0, false),
        (115.0, true),
        (0.0, false),
    ]);
    assert!(!detect_shark(&shark).is_empty());

    let cypher = swings_from_prices(&[
        (0.0, false),
        (100.0, true),
        (50.0, false),
        (115.0, true),
        (21.4, false),
    ]);
    assert!(!detect_cypher(&cypher).is_empty());

    let high = vec![10.0, 12.0, 11.0, 13.0, 12.0, 14.0, 13.0];
    let low = vec![9.0, 11.0, 10.0, 12.0, 11.0, 13.0, 12.0];
    let _ = detect_all_harmonics(&high, &low, 1, 1);
}

#[test]
fn test_harmonics_short_inputs() {
    use indicators::harmonics::{detect_bat, detect_butterfly, detect_crab, detect_cypher, detect_gartley, detect_shark, SwingPoint};

    let swings = vec![
        SwingPoint { index: 0, price: 0.0, is_high: false },
        SwingPoint { index: 1, price: 1.0, is_high: true },
        SwingPoint { index: 2, price: 0.5, is_high: false },
        SwingPoint { index: 3, price: 0.8, is_high: true },
    ];

    assert!(detect_gartley(&swings).is_empty());
    assert!(detect_bat(&swings).is_empty());
    assert!(detect_butterfly(&swings).is_empty());
    assert!(detect_crab(&swings).is_empty());
    assert!(detect_shark(&swings).is_empty());
    assert!(detect_cypher(&swings).is_empty());
}

#[test]
fn test_candlestick_patterns_extra() {
    use indicators::candlestick::*;

    let inv_open = vec![100.0, 98.0];
    let inv_high = vec![103.0, 104.0];
    let inv_low = vec![98.5, 94.0];
    let inv_close = vec![99.0, 101.0];
    let inverted = inverted_hammer(&inv_open, &inv_high, &inv_low, &inv_close);
    assert_eq!(inverted[0], -1.0);

    let hang_open = vec![100.0, 98.0];
    let hang_high = vec![100.5, 104.0];
    let hang_low = vec![96.0, 94.0];
    let hang_close = vec![99.0, 101.0];
    let hanging = hanging_man(&hang_open, &hang_high, &hang_low, &hang_close);
    assert_eq!(hanging[0], -1.0);

    let bullish_harami_vals = bullish_harami(&[105.0, 96.0], &[95.0, 100.0]);
    assert_eq!(bullish_harami_vals[1], 1.0);

    let bearish_harami_vals = bearish_harami(&[95.0, 104.0], &[105.0, 100.0]);
    assert_eq!(bearish_harami_vals[1], -1.0);

    let bearish_engulf_vals = bearish_engulfing(&[98.0, 103.0], &[102.0, 97.0]);
    assert_eq!(bearish_engulf_vals[1], -1.0);

    let piercing_vals = piercing_pattern(&[105.0, 90.0], &[94.0, 89.0], &[95.0, 101.0]);
    assert_eq!(piercing_vals[1], 1.0);

    let dark_cloud_vals = dark_cloud_cover(&[95.0, 107.0], &[106.0, 108.0], &[105.0, 99.0]);
    assert_eq!(dark_cloud_vals[1], -1.0);

    let evening_open = vec![100.0, 112.0, 110.0];
    let evening_high = vec![111.0, 113.0, 110.0];
    let evening_low = vec![95.0, 110.0, 98.0];
    let evening_close = vec![110.0, 111.0, 99.0];
    let evening_vals = evening_star(&evening_open, &evening_high, &evening_low, &evening_close);
    assert_eq!(evening_vals[2], -1.0);

    let open_crows = vec![105.0, 104.0, 103.0];
    let low_crows = vec![99.0, 98.0, 97.0];
    let close_crows = vec![100.0, 99.0, 98.0];
    let crows = three_black_crows(&open_crows, &low_crows, &close_crows);
    assert_eq!(crows[2], -1.0);

    let shooting_vals = shooting_star(&inv_open, &inv_high, &inv_low, &inv_close);
    assert_eq!(shooting_vals[0], -1.0);

    let gravestone_vals = gravestone_doji(&[100.0], &[110.0], &[99.8], &[100.5], 0.1);
    assert_eq!(gravestone_vals[0], -1.0);

    let long_legged_vals = long_legged_doji(&[100.0], &[110.0], &[90.0], &[100.2], 0.1);
    assert_eq!(long_legged_vals[0], 1.0);

    let tweezers_bottom_vals = tweezers_bottom(&[105.0, 100.0], &[95.0, 95.1], &[100.0, 104.0], 0.01);
    assert_eq!(tweezers_bottom_vals[1], 1.0);

    let rising_open = vec![100.0, 109.0, 108.5, 108.0, 109.0];
    let rising_high = vec![111.0, 109.5, 109.0, 108.5, 112.0];
    let rising_low = vec![99.0, 107.5, 107.0, 106.5, 108.0];
    let rising_close = vec![110.0, 108.0, 107.5, 107.0, 112.0];
    let rising_vals = rising_three_methods(&rising_open, &rising_high, &rising_low, &rising_close);
    assert_eq!(rising_vals[4], 1.0);

    let falling_open = vec![110.0, 101.0, 101.5, 102.0, 101.0];
    let falling_high = vec![111.0, 103.0, 103.0, 103.0, 101.5];
    let falling_low = vec![99.0, 100.5, 100.5, 100.5, 94.0];
    let falling_close = vec![100.0, 102.0, 102.5, 103.0, 95.0];
    let falling_vals = falling_three_methods(&falling_open, &falling_high, &falling_low, &falling_close);
    assert_eq!(falling_vals[4], -1.0);
}

#[test]
fn test_candlestick_short_inputs() {
    use indicators::candlestick::*;

    let open = vec![1.0];
    let high = vec![2.0];
    let low = vec![0.5];
    let close = vec![1.5];

    let _ = bullish_engulfing(&open, &close);
    let _ = bearish_engulfing(&open, &close);
    let _ = bullish_harami(&open, &close);
    let _ = bearish_harami(&open, &close);
    let _ = piercing_pattern(&open, &low, &close);
    let _ = dark_cloud_cover(&open, &high, &close);
    let _ = tweezers_top(&open, &high, &close, 0.01);
    let _ = tweezers_bottom(&open, &low, &close, 0.01);
    let _ = morning_star(&open, &high, &low, &close);
    let _ = evening_star(&open, &high, &low, &close);
    let _ = three_white_soldiers(&open, &high, &close);
    let _ = three_black_crows(&open, &low, &close);
    let _ = rising_three_methods(&open, &high, &low, &close);
    let _ = falling_three_methods(&open, &high, &low, &close);
}

#[test]
fn test_types_extras() {
    let candle = Candle::new(1704067200000, 100.0, 102.0, 99.0, 101.0, 1000.0);
    let dict = candle.to_dict().unwrap();
    assert_eq!(dict.get("open"), Some(&100.0));
    assert!((candle.median_price() - 100.5).abs() < 1e-10);
    assert!((candle.weighted_close() - 100.75).abs() < 1e-10);
    assert!(candle.__repr__().contains("Candle("));

    let mut result = IndicatorResult::new("test".to_string(), vec![1.0, 2.0]);
    result.add_metadata("k".to_string(), "v".to_string());
    assert_eq!(result.len(), 2);

    let mut multi = MultiIndicatorResult::new("multi".to_string());
    multi.add_series("s".to_string(), vec![1.0]);
    multi.add_metadata("k".to_string(), "v".to_string());

    let candles = vec![
        Candle::new(1, 1.0, 2.0, 0.5, 1.5, 10.0),
        Candle::new(2, 2.0, 3.0, 1.5, 2.5, 11.0),
    ];
    let (open, high, _low, _close, volume) = candles_to_vectors(&candles);
    assert_eq!(open.len(), 2);
    assert_eq!(high[1], 3.0);
    assert_eq!(volume[0], 10.0);

    let bad = vec![Candle::new(1, 10.0, 9.0, 9.5, 9.8, 1.0)];
    assert!(validate_ohlc(&bad).is_err());

    let bad_low = vec![Candle::new(1, 1.0, 2.0, 1.5, 1.2, 1.0)];
    assert!(validate_ohlc(&bad_low).is_err());
}

#[test]
fn test_cycle_indicators_extra() {
    let short = vec![1.0; 10];
    assert!(indicators::ht_dcphase(&short).iter().all(|x| x.is_nan()));
    let (sine_short, lead_short) = indicators::ht_sine(&short);
    assert!(sine_short.iter().all(|x| x.is_nan()));
    assert!(lead_short.iter().all(|x| x.is_nan()));
    assert!(indicators::ht_trendmode(&short).iter().all(|x| x.is_nan()));

    let values: Vec<f64> = (0..120).map(|i| (i as f64 * 0.1).sin() * 10.0 + 100.0).collect();
    let phase = indicators::ht_dcphase(&values);
    assert_eq!(phase.len(), values.len());

    let (sine, lead) = indicators::ht_sine(&values);
    assert_eq!(sine.len(), values.len());
    assert_eq!(lead.len(), values.len());

    let trend = indicators::ht_trendmode(&values);
    assert_eq!(trend.len(), values.len());
}

#[test]
fn test_pivots_extra() {
    use indicators::pivots::*;

    let woodie = woodie_pivots(110.0, 100.0, 105.0);
    assert!((woodie.pivot - 105.0).abs() < 0.1);

    let open = vec![100.0, 101.0, 102.0];
    let high = vec![110.0, 111.0, 112.0];
    let low = vec![90.0, 91.0, 92.0];
    let close = vec![105.0, 106.0, 107.0];

    for method in ["standard", "fibonacci", "woodie", "camarilla", "demark", "unknown"] {
        let pivots = calc_pivot_series(&open, &high, &low, &close, method);
        assert_eq!(pivots.len(), open.len());
    }

    let pivots = camarilla_pivots(110.0, 100.0, 105.0);
    let touched = detect_pivot_touch(pivots.r4.unwrap(), &pivots, 0.001);
    assert_eq!(touched.as_deref(), Some("R4"));
    let not_touched = detect_pivot_touch(1000.0, &pivots, 0.001);
    assert!(not_touched.is_none());

    let standard = standard_pivots(110.0, 100.0, 105.0);
    assert_eq!(pivot_zone(121.0, &standard), "Above R3");
    assert_eq!(pivot_zone(118.0, &standard), "R2-R3");
    assert_eq!(pivot_zone(112.0, &standard), "R1-R2");
    assert_eq!(pivot_zone(107.0, &standard), "PP-R1");
    assert_eq!(pivot_zone(104.0, &standard), "PP-S1");
    assert_eq!(pivot_zone(99.5, &standard), "S1-S2");
    assert_eq!(pivot_zone(95.0, &standard), "S2-S3");
    assert_eq!(pivot_zone(89.0, &standard), "Below S3");
}

#[test]
fn test_fibonacci_extra() {
    use indicators::fibonacci::*;

    let custom = [0.25, 0.75];
    let fib = fib_retracement(10.0, 20.0, Some(&custom));
    assert!(fib.levels.contains_key("0.250"));

    let ext = fib_extension(10.0, 20.0, 15.0, Some(&[1.0]));
    assert!(ext.levels.contains_key("1.000"));

    let prices = vec![10.0, 11.0, 12.0, 13.0, 12.0, 11.0, 14.0];
    let dynamic = dynamic_fib_retracement(&prices, 3);
    assert!(dynamic[0].is_empty());
    assert!(dynamic[3].contains_key("0.618"));

    let (fan_382, _fan_500, fan_618) = fib_fan_lines(0, 5, 100.0, 110.0, 10);
    assert!(fan_382 < fan_618);
    let (fan_nan, _, _) = fib_fan_lines(0, 5, 100.0, 110.0, 5);
    assert!(fan_nan.is_nan());

    let zones = fib_time_zones(0, 0);
    assert!(zones.is_empty());
    let zones_one = fib_time_zones(5, 1);
    assert_eq!(zones_one, vec![6]);
}

#[test]
fn test_ichimoku_signals_and_colors() {
    use indicators::ichimoku::{cloud_color, ichimoku_signals, IchimokuCloud, IchimokuSignal};

    let ichimoku = IchimokuCloud {
        tenkan_sen: vec![0.0; 5],
        kijun_sen: vec![0.0; 5],
        senkou_span_a: vec![3.0, 1.0, 2.0, 4.0, 2.0],
        senkou_span_b: vec![2.0, 2.0, 2.0, 3.0, 4.0],
        chikou_span: vec![5.0, -1.0, f64::NAN, 0.0, 1.0],
    };

    let close = vec![4.0, 0.5, 2.0, 5.0, 1.0];
    let signals = ichimoku_signals(&close, &ichimoku);
    assert_eq!(signals[0], IchimokuSignal::StrongBullish);
    assert_eq!(signals[1], IchimokuSignal::StrongBearish);
    assert_eq!(signals[2], IchimokuSignal::Neutral);
    assert_eq!(signals[3], IchimokuSignal::Bullish);
    assert_eq!(signals[4], IchimokuSignal::Bearish);

    let colors = cloud_color(&ichimoku);
    assert_eq!(colors[0], 1.0);
    assert_eq!(colors[1], -1.0);
    assert_eq!(colors[2], 0.0);
}

#[test]
fn test_utils_stats_extra() {
    use crate::utils::stats::*;

    let values = vec![3.0, 1.0, 4.0, 1.0, 5.0];
    let min_vals = rolling_min(&values, 3);
    assert_eq!(min_vals[2], 1.0);

    let sum_vals = rolling_sum(&values, 2);
    assert_eq!(sum_vals[1], 4.0);

    let pct_vals = rolling_percentile(&values, 5, 0.5);
    assert_eq!(pct_vals[4], 3.0);

    let cov_vals = covariance(&[1.0, 2.0, 3.0], &[2.0, 4.0, 6.0], 2);
    assert!(!cov_vals[1].is_nan());

    let se_vals = standard_error(&[1.0, 2.0, 3.0, 4.0], 3);
    assert!((se_vals[2] - 0.0).abs() < 1e-10);
}

#[test]
fn test_utils_stats_early_returns() {
    use crate::utils::stats::*;

    let values = vec![1.0, 2.0];
    assert!(stdev(&values, 1).iter().all(|x| x.is_nan()));
    assert!(rolling_max(&values, 0).iter().all(|x| x.is_nan()));
    assert!(rolling_min(&values, 3).iter().all(|x| x.is_nan()));
    assert!(rolling_sum(&values, 0).iter().all(|x| x.is_nan()));
    assert!(rolling_percentile(&values, 2, 2.0).iter().all(|x| x.is_nan()));
    assert!(roc(&values, 0).iter().all(|x| x.is_nan()));
    assert!(momentum(&values, 2).iter().all(|x| x.is_nan()));
    assert!(linear_regression(&values, 1).0.iter().all(|x| x.is_nan()));
    assert!(correlation(&values, &values, 1).iter().all(|x| x.is_nan()));
    assert!(zscore(&values, 1).iter().all(|x| x.is_nan()));
    assert!(covariance(&values, &values, 1).iter().all(|x| x.is_nan()));
    assert!(beta(&values, &values, 1).iter().all(|x| x.is_nan()));
    assert!(standard_error(&values, 2).iter().all(|x| x.is_nan()));
}

#[test]
fn test_utils_math_ops_extra() {
    use crate::utils::math_ops::*;

    let values = vec![0.0, 1.0];
    let exp_vals = exp(&values);
    assert!((exp_vals[0] - 1.0).abs() < 1e-10);
    let abs_vals = abs(&[-1.0, 2.0]);
    assert_eq!(abs_vals, vec![1.0, 2.0]);
    let ceil_vals = ceil(&[1.2, -1.2]);
    assert_eq!(ceil_vals, vec![2.0, -1.0]);
    let floor_vals = floor(&[1.8, -1.2]);
    assert_eq!(floor_vals, vec![1.0, -2.0]);

    let asin_vals = asin(&[0.0, 1.0]);
    assert!((asin_vals[1] - std::f64::consts::FRAC_PI_2).abs() < 1e-10);
    let acos_vals = acos(&[1.0, 0.0]);
    assert!((acos_vals[1] - std::f64::consts::FRAC_PI_2).abs() < 1e-10);
    let atan_vals = atan(&[0.0, 1.0]);
    assert!((atan_vals[1] - std::f64::consts::FRAC_PI_4).abs() < 1e-10);

    let sinh_vals = sinh(&[0.0]);
    let cosh_vals = cosh(&[0.0]);
    let tanh_vals = tanh(&[0.0]);
    assert_eq!(sinh_vals[0], 0.0);
    assert_eq!(cosh_vals[0], 1.0);
    assert_eq!(tanh_vals[0], 0.0);

    let sum_vals = sum(&[1.0, 2.0, 3.0], 2);
    assert_eq!(sum_vals[1], 3.0);
}

#[test]
fn test_utils_ma_extra() {
    use crate::utils::ma::*;

    let values = vec![1.0, 2.0, 3.0, 4.0, 5.0];
    let wma_vals = wma(&values, 3);
    assert!((wma_vals[2] - 14.0 / 6.0).abs() < 1e-10);

    let hma_vals = hma(&values, 3);
    assert_eq!(hma_vals.len(), values.len());

    let dema_vals = dema(&values, 3);
    assert_eq!(dema_vals.len(), values.len());

    let tema_vals = tema(&values, 3);
    assert_eq!(tema_vals.len(), values.len());

    let vwap_short = vwap(&values, &[1.0], 0);
    assert_eq!(vwap_short.len(), values.len());
}

#[test]
fn test_utils_ma_early_returns() {
    use crate::utils::ma::*;

    let values = vec![1.0, 2.0];
    assert!(sma(&values, 0).iter().all(|x| x.is_nan()));
    assert!(ema(&values, 0).iter().all(|x| x.is_nan()));
    assert!(rma(&values, 0).iter().all(|x| x.is_nan()));
    assert!(wma(&values, 0).iter().all(|x| x.is_nan()));
    assert!(hma(&values, 0).iter().all(|x| x.is_nan()));
    assert!(zlma(&values, 0).iter().all(|x| x.is_nan()));
    assert!(t3(&[], 0, 0.7).is_empty());
    assert!(kama(&values, 2, 2, 30).iter().all(|x| x.is_nan()));
    assert!(frama(&values, 3).iter().all(|x| x.is_nan()));
    assert!(vwap(&[], &[], 0).is_empty());
    assert!(vwap(&values, &values, 10).iter().all(|x| x.is_nan()));
}

#[test]
fn test_momentum_extras() {
    use indicators::momentum::*;

    let close = vec![10.0; 40];
    let (k, d) = stochrsi(&close, 14, 14, 3, 3);
    assert_eq!(k.len(), close.len());
    assert_eq!(d.len(), close.len());

    let high: Vec<f64> = (0..40).map(|i| i as f64 + 20.0).collect();
    let low: Vec<f64> = (0..40).map(|i| i as f64 + 10.0).collect();
    let ao = awesome_oscillator(&high, &low);
    assert_eq!(ao.len(), high.len());

    let (fisher, trigger) = fisher_transform(&high, &low, &close, 9);
    assert_eq!(fisher.len(), close.len());
    assert_eq!(trigger.len(), close.len());

    let (fisher_bad, trigger_bad) = fisher_transform(&high, &low, &close, 0);
    assert!(fisher_bad.iter().all(|x| x.is_nan()));
    assert!(trigger_bad.iter().all(|x| x.is_nan()));
}

#[test]
fn test_volatility_extras() {
    use indicators::volatility::*;

    let high = vec![10.0, 11.0, 12.0, 13.0, 14.0];
    let low = vec![9.0, 10.0, 11.0, 12.0, 13.0];
    let close = vec![9.5, 10.5, 11.5, 12.5, 13.5];

    let natr_vals = natr(&high, &low, &close, 3);
    assert_eq!(natr_vals.len(), close.len());

    let _ = true_range(&high, &vec![1.0], &close, 1);

    let (upper, middle, lower) = keltner_channel(&high, &low, &close, 3, 2, 1.5);
    assert_eq!(upper.len(), close.len());
    assert!(upper[2] >= middle[2]);
    assert!(middle[2] >= lower[2]);
}

#[test]
fn test_volume_extras() {
    use indicators::volume::*;

    let high = vec![10.0, 10.0];
    let low = vec![10.0, 10.0];
    let close = vec![10.0, 10.0];
    let volume = vec![100.0, 0.0];

    let (levels, bins, poc) = volume_profile(&high, &low, &close, &volume, 10);
    assert_eq!(levels.len(), 1);
    assert_eq!(bins.len(), 1);
    assert_eq!(poc, 10.0);

    let cmf_vals = cmf(&high, &low, &close, &vec![0.0, 0.0], 2);
    assert_eq!(cmf_vals[1], 0.0);

    let ad_vals = accumulation_distribution(&high, &low, &close, &volume);
    assert_eq!(ad_vals[0], 0.0);
}

#[test]
fn test_trend_extras() {
    use indicators::trend::*;

    let high = vec![10.0, 11.0];
    let low = vec![9.0, 10.0];
    let close = vec![9.5, 10.5];

    let (st, dir, _, _) = supertrend(&high, &low, &close, 0, 3.0);
    assert!(st.iter().all(|x| x.is_nan()));
    assert!(dir.iter().all(|x| x.is_nan()));

    let (adx_vals, plus, minus) = adx(&high, &low, &close, 14);
    assert!(adx_vals.iter().all(|x| x.is_nan()));
    assert!(plus.iter().all(|x| x.is_nan()));
    assert!(minus.iter().all(|x| x.is_nan()));

    let (aroon_up, aroon_down, aroon_osc) = aroon(&high, &vec![9.0], 2);
    assert!(aroon_up.iter().all(|x| x.is_nan()));
    assert!(aroon_down.iter().all(|x| x.is_nan()));
    assert!(aroon_osc.iter().all(|x| x.is_nan()));

    let (vi_plus, vi_minus) = vortex(&high, &low, &close, 0);
    assert!(vi_plus.iter().all(|x| x.is_nan()));
    assert!(vi_minus.iter().all(|x| x.is_nan()));

    let chop = choppiness_index(&high, &low, &close, 0);
    assert!(chop.iter().all(|x| x.is_nan()));
}

#[test]
fn test_sfg_atr2_signals() {
    let high = vec![10.0, 9.0, 8.0, 9.0, 10.0, 11.0];
    let low = vec![9.0, 8.0, 7.0, 8.0, 9.0, 10.0];
    let close = vec![9.5, 8.5, 7.5, 9.5, 11.0, 12.5];
    let volume = vec![100.0, 100.0, 100.0, 500.0, 500.0, 500.0];

    let (signals, stop_loss, take_profit) = indicators::atr2_signals(&high, &low, &close, &volume, 2, 0.5, 1);

    assert_eq!(signals.len(), close.len());
    assert_eq!(stop_loss.len(), close.len());
    assert_eq!(take_profit.len(), close.len());
    assert!(signals.iter().any(|&s| s == 1.0) || signals.iter().any(|&s| s == -1.0));
}
