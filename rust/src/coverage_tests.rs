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
    let _ = doji(&open, &high, &low, &close, 0.1);
    let _ = hammer(&open, &high, &low, &close);
    let _ = inverted_hammer(&open, &high, &low, &close);
    let _ = hanging_man(&open, &high, &low, &close);
    let _ = shooting_star(&open, &high, &low, &close);
    let _ = marubozu(&open, &high, &low, &close);
    let _ = spinning_top(&open, &high, &low, &close);
    let _ = dragonfly_doji(&open, &high, &low, &close, 0.1);
    let _ = gravestone_doji(&open, &high, &low, &close, 0.1);
    let _ = long_legged_doji(&open, &high, &low, &close, 0.1);
    let _ = tweezers_top(&open, &high, &close, 0.01);
    let _ = harami_cross(&open, &high, &low, &close, 0.1);
    let _ = morning_doji_star(&open, &high, &low, &close, 0.1);
    let _ = evening_doji_star(&open, &high, &low, &close, 0.1);
    let _ = three_inside(&open, &high, &low, &close);
    let _ = three_outside(&open, &high, &low, &close);
    let _ = abandoned_baby(&open, &high, &low, &close, 0.1);
    let _ = kicking(&open, &high, &low, &close);
    let _ = long_line(&open, &high, &low, &close, 2);
    let _ = short_line(&open, &high, &low, &close, 2);
    let _ = doji_star(&open, &high, &low, &close, 0.1);
    let _ = identical_three_crows(&open, &high, &low, &close);
    let _ = stick_sandwich(&open, &high, &low, &close, 0.01);
    let _ = tristar(&open, &high, &low, &close, 0.1);
    let _ = upside_gap_two_crows(&open, &high, &low, &close);
    let _ = gap_sidesidewhite(&open, &high, &low, &close);
    let _ = takuri(&open, &high, &low, &close);
    let _ = homing_pigeon(&open, &high, &low, &close);
    let _ = matching_low(&open, &high, &low, &close, 0.01);
    let _ = separating_lines(&open, &high, &low, &close, 0.005);
    let _ = thrusting(&open, &high, &low, &close);
    let _ = inneck(&open, &high, &low, &close, 0.01);
    let _ = onneck(&open, &high, &low, &close, 0.01);
    let _ = advance_block(&open, &high, &low, &close);
    let _ = stalled_pattern(&open, &high, &low, &close);
    let _ = belthold(&open, &high, &low, &close);
    let _ = concealing_baby_swallow(&open, &high, &low, &close);
    let _ = counterattack(&open, &high, &low, &close, 0.005);
    let _ = highwave(&open, &high, &low, &close, 0.15);
    let _ = hikkake(&open, &high, &low, &close);
    let _ = hikkake_mod(&open, &high, &low, &close);
    let _ = ladder_bottom(&open, &high, &low, &close);
    let _ = mat_hold(&open, &high, &low, &close);
    let _ = rickshaw_man(&open, &high, &low, &close, 0.1);
    let _ = unique_3_river(&open, &high, &low, &close);
    let _ = xside_gap_3_methods(&open, &high, &low, &close);
    let _ = closing_marubozu(&open, &high, &low, &close);
    let _ = breakaway(&open, &high, &low, &close);
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

#[test]
fn test_utils_ma_branches() {
    use crate::utils::ma::{ema, frama, kama, tema};

    let values = vec![1.0, 2.0, 3.0, f64::NAN, 5.0, 6.0, 7.0];
    let ema_vals = ema(&values, 3);
    assert!(!ema_vals[2].is_nan());
    assert_eq!(ema_vals[3], ema_vals[2]);

    let trend: Vec<f64> = (1..30).map(|i| i as f64).collect();
    let tema_vals = tema(&trend, 3);
    let tema_idx = tema_vals.iter().position(|v| !v.is_nan()).unwrap();
    assert!(tema_vals[tema_idx] > 0.0);

    let flat = vec![10.0; 20];
    let kama_vals = kama(&flat, 5, 2, 30);
    assert!(!kama_vals[5].is_nan());
    assert!((kama_vals[5] - 10.0).abs() < 1e-10);

    let frama_vals = frama(&flat, 10);
    assert_eq!(frama_vals[9], 10.0);

    let frama_edge = frama(&vec![5.0; 10], 10);
    assert_eq!(frama_edge.len(), 10);
}

#[test]
fn test_utils_math_ops_branches() {
    use crate::utils::math_ops::{div, minmaxindex, tan};

    let tan_vals = tan(&[0.0, std::f64::consts::FRAC_PI_4]);
    assert!((tan_vals[1] - 1.0).abs() < 1e-10);

    let div_vals = div(&[2.0, 4.0], &[1.0, 2.0]);
    assert_eq!(div_vals, vec![2.0, 2.0]);

    let div_zero = div(&[1.0], &[0.0]);
    assert!(div_zero[0].is_nan());

    let (min_idx, max_idx) = minmaxindex(&[1.0, 2.0], 0);
    assert!(min_idx.iter().all(|v| v.is_nan()));
    assert!(max_idx.iter().all(|v| v.is_nan()));
}

#[test]
fn test_utils_stats_branches() {
    use crate::utils::stats::*;

    let values = vec![0.0, 1.0, 2.0, 3.0];
    let roc_vals = roc(&values, 1);
    assert!(roc_vals[1].is_nan());
    assert!(!roc_vals[2].is_nan());

    let const_vals = vec![2.0; 5];
    let (_slope, _intercept, r2) = linear_regression(&const_vals, 5);
    assert!((r2[4] - 1.0).abs() < 1e-10);

    let corr_vals = correlation(&const_vals, &const_vals, 5);
    assert_eq!(corr_vals[4], 0.0);

    let z_vals = zscore(&const_vals, 5);
    assert_eq!(z_vals[4], 0.0);

    let beta_vals = beta(&const_vals, &const_vals, 5);
    assert_eq!(beta_vals[4], 0.0);

    let corr_wrapper = correl(&values, &values, 2);
    assert_eq!(corr_wrapper.len(), values.len());

    let lin_invalid = linearreg(&values, 1);
    assert!(lin_invalid.iter().all(|v| v.is_nan()));
    let lin_valid = linearreg(&values, 3);
    assert!(!lin_valid[2].is_nan());

    let slope_invalid = linearreg_slope(&values, 1);
    assert!(slope_invalid.iter().all(|v| v.is_nan()));
    let slope_valid = linearreg_slope(&values, 3);
    assert!(!slope_valid[2].is_nan());

    let angle_vals = linearreg_angle(&values, 3);
    assert!(!angle_vals[2].is_nan());

    let intercept_invalid = linearreg_intercept(&values, 1);
    assert!(intercept_invalid.iter().all(|v| v.is_nan()));
    let intercept_valid = linearreg_intercept(&values, 3);
    assert!(!intercept_valid[2].is_nan());

    let var_invalid = var(&values, 1);
    assert!(var_invalid.iter().all(|v| v.is_nan()));
    let var_valid = var(&values, 3);
    assert!(!var_valid[2].is_nan());

    let tsf_invalid = tsf(&values, 1);
    assert!(tsf_invalid.iter().all(|v| v.is_nan()));
    let tsf_valid = tsf(&values, 3);
    assert!(!tsf_valid[2].is_nan());
}

#[test]
fn test_cycle_branches() {
    use indicators::cycle::*;

    let short = vec![1.0; 10];
    let dc_short = ht_dcperiod(&short);
    assert!(dc_short.iter().all(|x| x.is_nan()));

    let phase_zero = ht_dcphase(&vec![0.0; 64]);
    assert_eq!(phase_zero[40], 0.0);

    let (phasor_short, quad_short) = ht_phasor(&short);
    assert!(phasor_short.iter().all(|x| x.is_nan()));
    assert!(quad_short.iter().all(|x| x.is_nan()));

    let values_fast: Vec<f64> = (0..160).map(|i| (i as f64 * 1.3).sin() * 15.0 + 100.0).collect();
    let dc_vals = ht_dcperiod(&values_fast);
    assert_eq!(dc_vals.len(), values_fast.len());

    let (sine, lead) = ht_sine(&values_fast);
    assert!(sine.iter().any(|v| !v.is_nan()));
    assert!(lead.iter().any(|v| !v.is_nan()));

    let values_trend: Vec<f64> = (0..200).map(|i| (i as f64 * 2.0).sin() * 8.0 + 100.0).collect();
    let trend = ht_trendmode(&values_trend);
    assert!(trend.iter().any(|v| *v == 0.0 || *v == 1.0));
}

#[test]
fn test_harmonics_branches() {
    use indicators::harmonics::{detect_bat, detect_butterfly, detect_crab, detect_cypher, detect_gartley, detect_shark, SwingPoint};

    let non_alt = vec![
        SwingPoint { index: 0, price: 10.0, is_high: true },
        SwingPoint { index: 1, price: 11.0, is_high: true },
        SwingPoint { index: 2, price: 9.0, is_high: false },
        SwingPoint { index: 3, price: 12.0, is_high: true },
        SwingPoint { index: 4, price: 8.0, is_high: false },
    ];

    assert!(detect_gartley(&non_alt).is_empty());
    assert!(detect_bat(&non_alt).is_empty());
    assert!(detect_butterfly(&non_alt).is_empty());
    assert!(detect_crab(&non_alt).is_empty());
    assert!(detect_shark(&non_alt).is_empty());
    assert!(detect_cypher(&non_alt).is_empty());

    let zero_ref = vec![
        SwingPoint { index: 0, price: 10.0, is_high: false },
        SwingPoint { index: 1, price: 10.0, is_high: true },
        SwingPoint { index: 2, price: 9.0, is_high: false },
        SwingPoint { index: 3, price: 12.0, is_high: true },
        SwingPoint { index: 4, price: 8.0, is_high: false },
    ];
    let _ = detect_gartley(&zero_ref);
}

#[test]
fn test_pivots_branches() {
    use indicators::pivots::{demark_pivots, detect_pivot_touch, PivotLevels};

    let dm_down = demark_pivots(10.0, 12.0, 8.0, 9.0);
    assert!(dm_down.r1 > dm_down.s1);

    let dm_equal = demark_pivots(10.0, 12.0, 8.0, 10.0);
    assert!((dm_equal.pivot - 10.0).abs() < 5.0);

    let levels = PivotLevels {
        pivot: 100.0,
        r1: 110.0,
        r2: f64::NAN,
        r3: f64::NAN,
        r4: Some(120.0),
        s1: 90.0,
        s2: f64::NAN,
        s3: f64::NAN,
        s4: Some(80.0),
    };

    let touch_r4 = detect_pivot_touch(120.0, &levels, 0.0001);
    assert_eq!(touch_r4.as_deref(), Some("R4"));
    let touch_s4 = detect_pivot_touch(80.0, &levels, 0.0001);
    assert_eq!(touch_s4.as_deref(), Some("S4"));
}

#[test]
fn test_ichimoku_nan_spans() {
    use indicators::ichimoku::{ichimoku_signals, IchimokuCloud, IchimokuSignal};

    let ichimoku = IchimokuCloud {
        tenkan_sen: vec![0.0, 0.0],
        kijun_sen: vec![0.0, 0.0],
        senkou_span_a: vec![f64::NAN, 1.0],
        senkou_span_b: vec![1.0, 1.0],
        chikou_span: vec![0.0, 0.0],
    };
    let close = vec![1.0, 1.0];
    let signals = ichimoku_signals(&close, &ichimoku);
    assert_eq!(signals[0], IchimokuSignal::Neutral);
}

#[test]
fn test_volume_branches() {
    use indicators::volume::*;

    let obv_bad = obv(&[1.0], &[]);
    assert!(obv_bad[0].is_nan());

    let obv_equal = obv(&[1.0, 1.0], &[10.0, 5.0]);
    assert_eq!(obv_equal[1], obv_equal[0]);

    let vwap_bad = vwap(&[1.0], &[1.0, 2.0], &[1.0], &[1.0], 0);
    assert!(vwap_bad[0].is_nan());

    let tp = vec![10.0, 9.0, 11.0, 10.5];
    let high: Vec<f64> = tp.iter().map(|v| v + 1.0).collect();
    let low: Vec<f64> = tp.iter().map(|v| v - 1.0).collect();
    let close = tp.clone();
    let volume = vec![100.0; tp.len()];

    let mfi_vals = mfi(&high, &low, &close, &volume, 3);
    assert!(!mfi_vals[2].is_nan());
    assert!(!mfi_vals[3].is_nan());

    let cmf_bad = cmf(&high, &low, &close, &volume, 0);
    assert!(cmf_bad.iter().all(|v| v.is_nan()));
    let cmf_vals = cmf(&high, &low, &close, &volume, 2);
    assert!(!cmf_vals[2].is_nan());

    let pvt_short = price_volume_trend(&[1.0], &[1.0]);
    assert!(pvt_short[0].is_nan());
    let pvt_zero = price_volume_trend(&[0.0, 1.0], &[10.0, 10.0]);
    assert_eq!(pvt_zero[1], pvt_zero[0]);

    let nvi_short = negative_volume_index(&[1.0], &[1.0]);
    assert!(nvi_short[0].is_nan());
    let pvi_short = positive_volume_index(&[1.0], &[1.0]);
    assert!(pvi_short[0].is_nan());

    let eom_short = ease_of_movement(&[1.0], &[1.0], &[1.0], 2);
    assert!(eom_short[0].is_nan());
    let eom_vals = ease_of_movement(&[2.0, 3.0], &[1.0, 2.0], &[100.0, 100.0], 1);
    assert!(!eom_vals[1].is_nan());
}

#[test]
fn test_overlap_branches() {
    use indicators::overlap::{mama, sar, sarext};

    let high = vec![10.0, 12.0, 11.0, 9.0, 8.0, 15.0, 14.0];
    let low = vec![9.0, 11.0, 10.0, 8.0, 7.0, 14.0, 13.0];

    let sar_vals = sar(&high, &low, 0.5, 1.0);
    assert_eq!(sar_vals.len(), high.len());

    let high_rev = vec![12.0, 11.0, 10.0, 9.0];
    let low_rev = vec![10.0, 5.0, 4.0, 3.0];
    let sar_rev = sar(&high_rev, &low_rev, 0.02, 0.2);
    assert_eq!(sar_rev.len(), high_rev.len());

    let sarext_vals = sarext(&high, &low, 1.0, 0.1, 0.02, 0.02, 0.2, 0.02, 0.02, 0.2);
    assert_eq!(sarext_vals.len(), high.len());

    let high_ext = vec![12.0, 11.0, 10.0, 20.0];
    let low_ext = vec![10.0, 5.0, 4.0, 15.0];
    let sarext_rev = sarext(&high_ext, &low_ext, 0.0, 0.0, 0.02, 0.02, 0.2, 0.02, 0.02, 0.2);
    assert_eq!(sarext_rev.len(), high_ext.len());

    let values: Vec<f64> = (0..10).map(|i| i as f64 + 1.0).collect();
    let (mama_vals, fama_vals) = mama(&values, 0.5, 0.05);
    assert!(!mama_vals[6].is_nan());
    assert!(!fama_vals[6].is_nan());
}

#[test]
fn test_momentum_branches() {
    use indicators::momentum::*;

    let rsi_invalid = rsi(&[1.0, 2.0], 2);
    assert!(rsi_invalid.iter().all(|v| v.is_nan()));

    let (k_bad, d_bad) = stochastic(&[1.0, 2.0], &[1.0], &[1.0, 2.0], 2, 3);
    assert!(k_bad.iter().all(|v| v.is_nan()));
    assert!(d_bad.iter().all(|v| v.is_nan()));

    let high = vec![10.0, 10.0, 10.0, 10.0];
    let low = vec![10.0, 10.0, 10.0, 10.0];
    let close = vec![10.0, 10.0, 10.0, 10.0];
    let (k_flat, _d_flat) = stochastic(&high, &low, &close, 2, 2);
    assert_eq!(k_flat[1], 50.0);

    let close_var = vec![10.0, 11.0, 12.0, 11.0, 13.0, 12.0];
    let (stoch_k, _stoch_d) = stochrsi(&close_var, 1, 2, 2, 2);
    let stoch_idx = stoch_k.iter().position(|v| !v.is_nan()).unwrap();
    assert!(stoch_k[stoch_idx] >= 0.0);

    let high_nan = vec![10.0, f64::NAN, 12.0, 13.0];
    let low_nan = vec![9.0, 9.0, 11.0, 12.0];
    let close_nan = vec![9.5, 10.0, 11.5, 12.5];
    let cci_vals = cci(&high_nan, &low_nan, &close_nan, 2);
    assert!(cci_vals.iter().any(|v| v.is_nan()));

    let will_mismatch = williams_r(&[1.0, 2.0], &[1.0], &[1.0, 2.0], 2);
    assert!(will_mismatch.iter().all(|v| v.is_nan()));

    let will_range = williams_r(&high, &low, &close, 2);
    assert_eq!(will_range[1], -50.0);

    let ao_mismatch = awesome_oscillator(&[1.0, 2.0], &[1.0]);
    assert!(ao_mismatch.iter().all(|v| v.is_nan()));

    let (fisher_nan, _trigger_nan) = fisher_transform(&high_nan, &low_nan, &close_nan, 2);
    assert!(fisher_nan.iter().any(|v| v.is_nan()));

    let (fisher_flat, _trigger_flat) = fisher_transform(&high, &low, &close, 2);
    assert_eq!(fisher_flat[1], 0.0);

    let (_k_vals, _d_vals, j_vals) = kdj(&high, &low, &close, 2, 2);
    let j_idx = j_vals.iter().position(|v| !v.is_nan()).unwrap();
    assert!(!j_vals[j_idx].is_nan());
}

#[test]
fn test_momentum_branches_extended() {
    use indicators::momentum::*;

    let close_var = vec![10.0, 11.0, 12.0, 11.0, 13.0, 12.0];

    let (tsi_short, signal_short) = tsi(&[1.0], 5, 3, 3);
    assert!(tsi_short[0].is_nan());
    assert!(signal_short[0].is_nan());

    let (tsi_vals, _signal_vals) = tsi(&close_var, 2, 2, 2);
    let tsi_idx = tsi_vals.iter().position(|v| !v.is_nan()).unwrap();
    assert!(tsi_vals[tsi_idx].is_finite());

    let uo_short = ultimate_oscillator(&[1.0], &[1.0], &[1.0], 7, 14, 28);
    assert!(uo_short[0].is_nan());

    let apo_vals = apo(&close_var, 2, 3);
    assert_eq!(apo_vals.len(), close_var.len());

    let ppo_vals = ppo(&close_var, 2, 3);
    assert_eq!(ppo_vals.len(), close_var.len());

    let cmo_zero = cmo(&vec![1.0; 5], 2);
    assert_eq!(cmo_zero[2], 0.0);
    let cmo_vals = cmo(&close_var, 2);
    assert!(!cmo_vals[2].is_nan());

    let high: Vec<f64> = (100..120).map(|x| x as f64 + 5.0).collect();
    let low: Vec<f64> = (100..120).map(|x| x as f64).collect();
    let close: Vec<f64> = (100..120).map(|x| x as f64 + 2.5).collect();
    let uo = ultimate_oscillator(&high, &low, &close, 3, 5, 7);
    assert!(!uo[10].is_nan());
}

#[test]
fn test_trend_branches() {
    use indicators::trend::{adx, choppiness_index, dx, minus_di, plus_di, psar, qstick, supertrend, vhf, vortex};

    let high_nan = vec![10.0, f64::NAN, 12.0];
    let low_nan = vec![9.0, 8.0, 11.0];
    let close_nan = vec![9.5, 9.0, 11.5];
    let _ = supertrend(&high_nan, &low_nan, &close_nan, 2, 3.0);

    let adx_bad = adx(&[1.0], &[1.0, 2.0], &[1.0], 2);
    assert!(adx_bad.0.iter().all(|v| v.is_nan()));

    let high_flat = vec![10.0, 11.0, 12.0];
    let low_flat = vec![10.0, 9.0, 8.0];
    let close_flat = vec![10.0, 10.0, 10.0];
    let (adx_vals, _plus, _minus) = adx(&high_flat, &low_flat, &close_flat, 2);
    assert_eq!(adx_vals[1], 0.0);

    let dx_vals = dx(&high_flat, &low_flat, &close_flat, 2);
    assert_eq!(dx_vals[1], 0.0);

    let dx_mismatch = dx(&[1.0, 2.0], &[1.0], &[1.0, 2.0], 2);
    assert!(dx_mismatch.iter().all(|v| v.is_nan()));

    let high_move = vec![10.0, 12.0, 11.0, 13.0];
    let low_move = vec![9.0, 10.0, 9.5, 11.0];
    let close_move = vec![9.5, 11.0, 10.0, 12.0];
    let dx_nonzero = dx(&high_move, &low_move, &close_move, 2);
    assert!(!dx_nonzero[2].is_nan());

    let _plus_di = plus_di(&high_flat, &low_flat, &close_flat, 2);
    let _minus_di = minus_di(&high_flat, &low_flat, &close_flat, 2);

    let psar_short = psar(&[1.0], &[1.0], &[1.0], 0.02, 0.02, 0.2);
    assert!(psar_short.0[0].is_nan());

    let high_rev = vec![10.0, 9.0, 8.0, 12.0, 13.0];
    let low_rev = vec![9.0, 8.0, 7.0, 11.0, 12.0];
    let close_rev = vec![9.5, 9.0, 8.5, 11.5, 12.5];
    let (psar_vals, trend) = psar(&high_rev, &low_rev, &close_rev, 0.2, 0.2, 0.5);
    assert_eq!(psar_vals.len(), close_rev.len());
    assert!(trend.iter().any(|v| *v == 1.0) && trend.iter().any(|v| *v == -1.0));

    let high_v = vec![10.0, 11.0, 12.0, 11.0, 13.0];
    let low_v = vec![9.0, 10.0, 11.0, 10.0, 12.0];
    let close_v = vec![9.5, 10.5, 11.5, 10.5, 12.5];
    let (vi_plus, vi_minus) = vortex(&high_v, &low_v, &close_v, 2);
    assert!(!vi_plus[2].is_nan());
    assert!(!vi_minus[2].is_nan());

    let chop_vals = choppiness_index(&high_v, &low_v, &close_v, 2);
    assert!(!chop_vals[2].is_nan());

    let qstick_empty = qstick(&[], &[], 3);
    assert!(qstick_empty.is_empty());

    let vhf_short = vhf(&close_v, 0);
    assert!(vhf_short.iter().all(|v| v.is_nan()));
    let vhf_vals = vhf(&close_v, 2);
    assert!(!vhf_vals[2].is_nan());
}

#[test]
fn test_sfg_branches() {
    let close: Vec<f64> = (0..50).map(|i| 100.0 + i as f64 * 0.5).collect();
    let high: Vec<f64> = close.iter().map(|v| v + 1.0).collect();
    let low: Vec<f64> = close.iter().map(|v| v - 1.0).collect();

    let (_st, dir) = indicators::ai_supertrend(&high, &low, &close, 3, 10, 3, 3, 3, 1.5);
    assert_eq!(dir.len(), close.len());

    let mut close_knn = close.clone();
    close_knn[6] = 0.0;
    let (prediction, prediction_ma) = indicators::ai_momentum_index(&close_knn, 3, 5, 3);
    assert_eq!(prediction.len(), close_knn.len());
    assert!(prediction.iter().any(|v| !v.is_nan()));
    assert_eq!(prediction_ma.len(), close_knn.len());

    let high_flat = vec![10.0, 10.0, 10.0, 10.0, 10.0];
    let low_flat = vec![10.0, 10.0, 10.0, 10.0, 10.0];
    let close_flat = vec![10.0, 10.0, 10.0, 10.0, 10.0];
    let volume_nan = vec![10.0, f64::NAN, 10.0, 10.0, 10.0];
    let _ = indicators::atr2_signals(&high_flat, &low_flat, &close_flat, &volume_nan, 2, 0.5, 1);

    let high_down = vec![10.0, 9.0, 8.0, 7.0, 6.0];
    let low_down = vec![9.0, 8.0, 7.0, 6.0, 5.0];
    let close_down = vec![9.5, 8.5, 7.5, 6.5, 5.5];
    let volume = vec![100.0, 100.0, 500.0, 500.0, 500.0];
    let (signals, stop_loss, take_profit) = indicators::atr2_signals(&high_down, &low_down, &close_down, &volume, 2, 0.1, 1);
    assert!(signals.iter().any(|&s| s == 1.0));
    assert!(stop_loss.iter().any(|v| !v.is_nan()));
    assert!(take_profit.iter().any(|v| !v.is_nan()));
}
