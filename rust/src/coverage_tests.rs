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
fn test_candlestick_long_line_and_concealing_branches() {
    use indicators::candlestick::{concealing_baby_swallow, long_line};

    let open = vec![10.0, 10.0, 10.0];
    let high = vec![11.2, 11.2, 10.8];
    let low = vec![9.8, 9.8, 10.3];
    let close = vec![11.0, 11.0, 10.5];
    let long_vals = long_line(&open, &high, &low, &close, 2);
    assert_eq!(long_vals[2], 0.0);

    let open_cb = vec![10.0, 9.0, 8.0, 7.0];
    let high_cb = vec![10.5, 10.5, 8.5, 7.5];
    let low_cb = vec![8.5, 8.5, 6.5, 5.5];
    let close_cb = vec![9.0, 10.0, 7.0, 6.0];
    let conceal = concealing_baby_swallow(&open_cb, &high_cb, &low_cb, &close_cb);
    assert_eq!(conceal[3], 0.0);
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
fn test_ichimoku_tk_cross_and_nan_cloud() {
    use indicators::ichimoku::{cloud_color, cloud_thickness, ichimoku_tk_cross, IchimokuCloud};

    let ichimoku = IchimokuCloud {
        tenkan_sen: vec![1.0, 3.0, 1.0],
        kijun_sen: vec![2.0, 2.0, 2.0],
        senkou_span_a: vec![f64::NAN, 2.0, 3.0],
        senkou_span_b: vec![1.0, f64::NAN, 2.0],
        chikou_span: vec![0.0; 3],
    };

    let tk = ichimoku_tk_cross(&ichimoku);
    assert_eq!(tk[1], 1.0);
    assert_eq!(tk[2], -1.0);

    let thickness = cloud_thickness(&ichimoku);
    assert!(thickness[0].is_nan());
    assert!(thickness[1].is_nan());

    let colors = cloud_color(&ichimoku);
    assert_eq!(colors[0], 0.0);
    assert_eq!(colors[1], 0.0);
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
fn test_momentum_cci_zero_mean_dev() {
    use indicators::momentum::cci;

    let high = vec![10.0; 5];
    let low = vec![10.0; 5];
    let close = vec![10.0; 5];
    let cci_vals = cci(&high, &low, &close, 3);
    assert_eq!(cci_vals[2], 0.0);
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
fn test_trend_adx_minus_dm_branch() {
    use indicators::trend::adx;

    let high = vec![10.0, 9.0, 8.0, 7.0, 6.0];
    let low = vec![9.0, 7.0, 6.0, 5.0, 4.0];
    let close = vec![9.5, 8.0, 6.5, 5.5, 4.5];
    let (_adx, _plus, minus) = adx(&high, &low, &close, 2);
    assert!(minus.iter().any(|v| v.is_finite()));
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
fn test_sfg_ai_supertrend_short_len() {
    let close = vec![10.0, 10.5, 10.2, 10.8, 10.6];
    let high: Vec<f64> = close.iter().map(|v| v + 0.5).collect();
    let low: Vec<f64> = close.iter().map(|v| v - 0.5).collect();

    let (_st, dir) = indicators::ai_supertrend(&high, &low, &close, 3, 10, 2, 2, 2, 2.0);
    assert_eq!(dir.len(), close.len());
}

#[test]
fn test_sfg_ai_momentum_index_with_nan() {
    let close = vec![100.0, 101.0, f64::NAN, 102.0, 103.0, 104.0, 105.0, 106.0];
    let (prediction, prediction_ma) = indicators::ai_momentum_index(&close, 2, 2, 2);

    assert_eq!(prediction.len(), close.len());
    assert_eq!(prediction_ma.len(), close.len());
}

#[test]
fn test_sfg_atr2_signals_nan_momentum() {
    let high = vec![10.0, 11.0, 12.0, 13.0, 14.0, 15.0];
    let low = vec![9.0, 10.0, 11.0, 12.0, 13.0, 14.0];
    let close = vec![9.5, 10.5, 11.5, 12.5, 13.5, 14.5];
    let volume = vec![100.0; 6];

    let (signals, stop_loss, take_profit) = indicators::atr2_signals(&high, &low, &close, &volume, 2, 0.5, 5);
    assert_eq!(signals.len(), close.len());
    assert_eq!(stop_loss.len(), close.len());
    assert_eq!(take_profit.len(), close.len());
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

#[test]
fn test_candlestick_single_patterns() {
    use indicators::candlestick::*;

    let doji_vals = doji(&[100.0], &[101.0], &[99.0], &[100.05], 0.1);
    assert_eq!(doji_vals[0], 1.0);

    let hammer_vals = hammer(&[100.0], &[101.0], &[96.0], &[101.0]);
    assert_eq!(hammer_vals[0], 1.0);

    let inverted_vals = inverted_hammer(&[100.0], &[105.0], &[99.5], &[101.0]);
    assert_eq!(inverted_vals[0], 1.0);

    let hanging_vals = hanging_man(&[100.0], &[101.0], &[96.0], &[101.0]);
    assert_eq!(hanging_vals[0], -1.0);

    let shooting_vals = shooting_star(&[100.0], &[105.0], &[99.5], &[101.0]);
    assert_eq!(shooting_vals[0], -1.0);

    let maru_bull = marubozu(&[100.0], &[110.1], &[99.9], &[110.0]);
    assert_eq!(maru_bull[0], 1.0);
    let maru_bear = marubozu(&[110.0], &[110.1], &[99.9], &[100.0]);
    assert_eq!(maru_bear[0], -1.0);

    let spin = spinning_top(&[100.0], &[105.0], &[95.0], &[101.0]);
    assert_eq!(spin[0], 1.0);

    let dragon = dragonfly_doji(&[100.0], &[100.2], &[95.0], &[100.05], 0.1);
    assert_eq!(dragon[0], 1.0);

    let grave = gravestone_doji(&[100.0], &[105.0], &[99.8], &[100.05], 0.1);
    assert_eq!(grave[0], -1.0);

    let long_leg = long_legged_doji(&[100.0], &[106.0], &[94.0], &[100.05], 0.1);
    assert_eq!(long_leg[0], 1.0);

    let takuri_vals = takuri(&[100.0], &[100.3], &[95.0], &[100.2]);
    assert_eq!(takuri_vals[0], 1.0);

    let rickshaw_vals = rickshaw_man(&[100.0], &[102.0], &[98.0], &[100.1], 0.1);
    assert_eq!(rickshaw_vals[0], 1.0);

    let highwave_vals = highwave(&[100.0], &[110.0], &[90.0], &[100.2], 0.15);
    assert_eq!(highwave_vals[0], 1.0);

    let belt_bull = belthold(&[100.0], &[110.2], &[99.9], &[110.0]);
    assert_eq!(belt_bull[0], 1.0);
    let belt_bear = belthold(&[110.0], &[110.1], &[99.8], &[100.0]);
    assert_eq!(belt_bear[0], -1.0);

    let closing_bull = closing_marubozu(&[100.0], &[110.0], &[99.0], &[110.0]);
    assert_eq!(closing_bull[0], 1.0);
    let closing_bear = closing_marubozu(&[110.0], &[111.0], &[100.0], &[100.0]);
    assert_eq!(closing_bear[0], -1.0);

    let open_ll = vec![100.0, 100.5, 100.2, 100.0];
    let high_ll = vec![101.5, 101.5, 101.5, 110.5];
    let low_ll = vec![99.5, 99.8, 99.9, 99.5];
    let close_ll = vec![101.0, 101.0, 101.1, 110.0];
    let long_vals = long_line(&open_ll, &high_ll, &low_ll, &close_ll, 3);
    assert_eq!(long_vals[3], 1.0);

    let open_sl = vec![110.0, 120.0, 130.0, 100.0];
    let high_sl = vec![111.0, 121.0, 131.0, 101.0];
    let low_sl = vec![99.0, 109.0, 119.0, 99.0];
    let close_sl = vec![100.0, 110.0, 120.0, 100.5];
    let short_vals = short_line(&open_sl, &high_sl, &low_sl, &close_sl, 3);
    assert_eq!(short_vals[3], 1.0);

    let open_sl_bear = vec![110.0, 120.0, 130.0, 100.5];
    let high_sl_bear = vec![111.0, 121.0, 131.0, 101.0];
    let low_sl_bear = vec![99.0, 109.0, 119.0, 99.0];
    let close_sl_bear = vec![100.0, 110.0, 120.0, 100.0];
    let short_bear = short_line(&open_sl_bear, &high_sl_bear, &low_sl_bear, &close_sl_bear, 3);
    assert_eq!(short_bear[3], -1.0);
}

#[test]
fn test_candlestick_two_candle_patterns() {
    use indicators::candlestick::*;

    let bull_eng = bullish_engulfing(&[105.0, 100.0], &[100.0, 110.0]);
    assert_eq!(bull_eng[1], 1.0);

    let bear_eng = bearish_engulfing(&[100.0, 110.0], &[110.0, 95.0]);
    assert_eq!(bear_eng[1], -1.0);

    let bull_harami = bullish_harami(&[110.0, 102.0], &[100.0, 108.0]);
    assert_eq!(bull_harami[1], 1.0);

    let bear_harami = bearish_harami(&[100.0, 108.0], &[110.0, 102.0]);
    assert_eq!(bear_harami[1], -1.0);

    let piercing_open = vec![110.0, 95.0];
    let piercing_low = vec![100.0, 94.0];
    let piercing_close = vec![100.0, 106.0];
    let piercing_vals = piercing_pattern(&piercing_open, &piercing_low, &piercing_close);
    assert_eq!(piercing_vals[1], 1.0);

    let dark_open = vec![100.0, 115.0];
    let dark_high = vec![112.0, 116.0];
    let dark_close = vec![110.0, 104.0];
    let dark_vals = dark_cloud_cover(&dark_open, &dark_high, &dark_close);
    assert_eq!(dark_vals[1], -1.0);

    let tweez_top_open = vec![100.0, 110.0];
    let tweez_top_high = vec![120.0, 119.9];
    let tweez_top_close = vec![110.0, 100.0];
    let tweez_top_vals = tweezers_top(&tweez_top_open, &tweez_top_high, &tweez_top_close, 0.01);
    assert_eq!(tweez_top_vals[1], -1.0);

    let tweez_bot_open = vec![110.0, 100.0];
    let tweez_bot_low = vec![90.0, 90.1];
    let tweez_bot_close = vec![100.0, 110.0];
    let tweez_bot_vals = tweezers_bottom(&tweez_bot_open, &tweez_bot_low, &tweez_bot_close, 0.01);
    assert_eq!(tweez_bot_vals[1], 1.0);

    let harami_open = vec![120.0, 110.0];
    let harami_high = vec![121.0, 111.0];
    let harami_low = vec![99.0, 109.0];
    let harami_close = vec![100.0, 110.05];
    let harami_vals = harami_cross(&harami_open, &harami_high, &harami_low, &harami_close, 0.1);
    assert_eq!(harami_vals[1], 1.0);

    let doji_open = vec![120.0, 95.0];
    let doji_high = vec![121.0, 95.5];
    let doji_low = vec![99.0, 94.5];
    let doji_close = vec![100.0, 95.05];
    let doji_vals = doji_star(&doji_open, &doji_high, &doji_low, &doji_close, 0.1);
    assert_eq!(doji_vals[1], 1.0);

    let homing_open = vec![120.0, 110.0];
    let homing_high = vec![121.0, 111.0];
    let homing_low = vec![99.0, 104.0];
    let homing_close = vec![100.0, 105.0];
    let homing_vals = homing_pigeon(&homing_open, &homing_high, &homing_low, &homing_close);
    assert_eq!(homing_vals[1], 1.0);

    let match_open = vec![110.0, 108.0];
    let match_high = vec![111.0, 109.0];
    let match_low = vec![99.0, 98.0];
    let match_close = vec![100.0, 100.5];
    let match_vals = matching_low(&match_open, &match_high, &match_low, &match_close, 0.01);
    assert_eq!(match_vals[1], 1.0);

    let sep_open = vec![100.0, 100.2];
    let sep_high = vec![101.0, 106.0];
    let sep_low = vec![94.0, 99.0];
    let sep_close = vec![95.0, 105.0];
    let sep_vals = separating_lines(&sep_open, &sep_high, &sep_low, &sep_close, 0.005);
    assert_eq!(sep_vals[1], 1.0);

    let sep_open_bear = vec![100.0, 100.2];
    let sep_high_bear = vec![111.0, 101.0];
    let sep_low_bear = vec![99.0, 94.0];
    let sep_close_bear = vec![110.0, 95.0];
    let sep_bear = separating_lines(&sep_open_bear, &sep_high_bear, &sep_low_bear, &sep_close_bear, 0.005);
    assert_eq!(sep_bear[1], -1.0);

    let thrust_open = vec![110.0, 98.0];
    let thrust_high = vec![111.0, 105.0];
    let thrust_low = vec![99.0, 97.0];
    let thrust_close = vec![100.0, 104.0];
    let thrust_vals = thrusting(&thrust_open, &thrust_high, &thrust_low, &thrust_close);
    assert_eq!(thrust_vals[1], -1.0);

    let inneck_open = vec![110.0, 98.0];
    let inneck_high = vec![111.0, 100.0];
    let inneck_low = vec![99.0, 97.0];
    let inneck_close = vec![100.0, 99.2];
    let inneck_vals = inneck(&inneck_open, &inneck_high, &inneck_low, &inneck_close, 0.01);
    assert_eq!(inneck_vals[1], -1.0);

    let onneck_open = vec![110.0, 99.0];
    let onneck_high = vec![111.0, 100.5];
    let onneck_low = vec![99.0, 98.5];
    let onneck_close = vec![100.0, 100.2];
    let onneck_vals = onneck(&onneck_open, &onneck_high, &onneck_low, &onneck_close, 0.01);
    assert_eq!(onneck_vals[1], -1.0);

    let counter_open = vec![110.0, 100.0];
    let counter_high = vec![111.0, 101.0];
    let counter_low = vec![99.0, 99.0];
    let counter_close = vec![100.0, 100.4];
    let counter_vals = counterattack(&counter_open, &counter_high, &counter_low, &counter_close, 0.01);
    assert_eq!(counter_vals[1], 1.0);

    let counter_open_bear = vec![100.0, 110.0];
    let counter_high_bear = vec![111.0, 111.0];
    let counter_low_bear = vec![99.0, 99.0];
    let counter_close_bear = vec![110.0, 109.6];
    let counter_bear = counterattack(&counter_open_bear, &counter_high_bear, &counter_low_bear, &counter_close_bear, 0.01);
    assert_eq!(counter_bear[1], -1.0);

    let kick_open = vec![110.0, 112.0];
    let kick_high = vec![110.1, 122.1];
    let kick_low = vec![99.9, 111.9];
    let kick_close = vec![100.0, 122.0];
    let kick_vals = kicking(&kick_open, &kick_high, &kick_low, &kick_close);
    assert_eq!(kick_vals[1], 1.0);
}

#[test]
fn test_candlestick_three_candle_patterns_a() {
    use indicators::candlestick::*;

    let morning_open = vec![105.0, 94.0, 96.0];
    let morning_high = vec![106.0, 95.0, 106.0];
    let morning_low = vec![95.0, 93.0, 95.0];
    let morning_close = vec![95.0, 94.5, 104.0];
    let morning_vals = morning_star(&morning_open, &morning_high, &morning_low, &morning_close);
    assert_eq!(morning_vals[2], 1.0);

    let evening_open = vec![95.0, 106.0, 104.0];
    let evening_high = vec![106.0, 107.0, 105.0];
    let evening_low = vec![94.0, 105.0, 94.0];
    let evening_close = vec![105.0, 106.5, 96.0];
    let evening_vals = evening_star(&evening_open, &evening_high, &evening_low, &evening_close);
    assert_eq!(evening_vals[2], -1.0);

    let mds_open = vec![110.0, 98.0, 99.0];
    let mds_high = vec![111.0, 98.5, 109.0];
    let mds_low = vec![99.0, 97.0, 98.0];
    let mds_close = vec![100.0, 98.05, 108.0];
    let mds_vals = morning_doji_star(&mds_open, &mds_high, &mds_low, &mds_close, 0.1);
    assert_eq!(mds_vals[2], 1.0);

    let eds_open = vec![100.0, 112.0, 111.0];
    let eds_high = vec![111.0, 112.5, 112.0];
    let eds_low = vec![99.0, 111.5, 100.0];
    let eds_close = vec![110.0, 112.05, 101.0];
    let eds_vals = evening_doji_star(&eds_open, &eds_high, &eds_low, &eds_close, 0.1);
    assert_eq!(eds_vals[2], -1.0);

    let soldiers_open = vec![100.0, 104.0, 107.0];
    let soldiers_high = vec![105.5, 108.5, 112.5];
    let soldiers_close = vec![105.0, 108.0, 112.0];
    let soldiers_vals = three_white_soldiers(&soldiers_open, &soldiers_high, &soldiers_close);
    assert_eq!(soldiers_vals[2], 1.0);

    let crows_open = vec![105.0, 101.0, 97.0];
    let crows_low = vec![99.5, 95.5, 91.5];
    let crows_close = vec![100.0, 96.0, 92.0];
    let crows_vals = three_black_crows(&crows_open, &crows_low, &crows_close);
    assert_eq!(crows_vals[2], -1.0);

    let inside_open = vec![110.0, 102.0, 105.0];
    let inside_high = vec![111.0, 109.0, 116.0];
    let inside_low = vec![99.0, 101.0, 104.0];
    let inside_close = vec![100.0, 108.0, 115.0];
    let inside_vals = three_inside(&inside_open, &inside_high, &inside_low, &inside_close);
    assert_eq!(inside_vals[2], 1.0);

    let inside_open_bear = vec![100.0, 108.0, 105.0];
    let inside_high_bear = vec![111.0, 109.0, 106.0];
    let inside_low_bear = vec![99.0, 101.0, 94.0];
    let inside_close_bear = vec![110.0, 102.0, 95.0];
    let inside_bear = three_inside(&inside_open_bear, &inside_high_bear, &inside_low_bear, &inside_close_bear);
    assert_eq!(inside_bear[2], -1.0);

    let outside_open = vec![110.0, 99.0, 110.0];
    let outside_high = vec![111.0, 113.0, 121.0];
    let outside_low = vec![99.0, 98.0, 109.0];
    let outside_close = vec![100.0, 112.0, 120.0];
    let outside_vals = three_outside(&outside_open, &outside_high, &outside_low, &outside_close);
    assert_eq!(outside_vals[2], 1.0);

    let outside_open_bear = vec![100.0, 112.0, 108.0];
    let outside_high_bear = vec![111.0, 113.0, 109.0];
    let outside_low_bear = vec![99.0, 94.0, 89.0];
    let outside_close_bear = vec![110.0, 95.0, 90.0];
    let outside_bear = three_outside(&outside_open_bear, &outside_high_bear, &outside_low_bear, &outside_close_bear);
    assert_eq!(outside_bear[2], -1.0);

    let baby_open = vec![110.0, 95.0, 97.0];
    let baby_high = vec![111.0, 95.2, 106.0];
    let baby_low = vec![99.0, 94.5, 96.0];
    let baby_close = vec![100.0, 95.05, 105.0];
    let baby_vals = abandoned_baby(&baby_open, &baby_high, &baby_low, &baby_close, 0.1);
    assert_eq!(baby_vals[2], 1.0);

    let baby_open_bear = vec![100.0, 112.0, 108.0];
    let baby_high_bear = vec![111.0, 112.5, 109.0];
    let baby_low_bear = vec![99.0, 111.5, 97.0];
    let baby_close_bear = vec![110.0, 112.05, 98.0];
    let baby_bear = abandoned_baby(&baby_open_bear, &baby_high_bear, &baby_low_bear, &baby_close_bear, 0.1);
    assert_eq!(baby_bear[2], -1.0);
}

#[test]
fn test_candlestick_three_candle_patterns_b() {
    use indicators::candlestick::*;

    let crow_open = vec![110.0, 108.0, 106.0];
    let crow_high = vec![111.0, 109.0, 107.0];
    let crow_low = vec![99.0, 97.0, 95.0];
    let crow_close = vec![100.0, 98.0, 96.0];
    let crow_vals = identical_three_crows(&crow_open, &crow_high, &crow_low, &crow_close);
    assert_eq!(crow_vals[2], -1.0);

    let stick_open = vec![110.0, 101.0, 109.0];
    let stick_high = vec![111.0, 109.5, 110.0];
    let stick_low = vec![99.0, 101.5, 99.5];
    let stick_close = vec![100.0, 108.0, 100.5];
    let stick_vals = stick_sandwich(&stick_open, &stick_high, &stick_low, &stick_close, 0.01);
    assert_eq!(stick_vals[2], 1.0);

    let tristar_open = vec![100.0, 95.0, 100.0];
    let tristar_high = vec![101.0, 95.5, 101.0];
    let tristar_low = vec![99.5, 94.5, 99.6];
    let tristar_close = vec![100.05, 95.05, 100.05];
    let tristar_vals = tristar(&tristar_open, &tristar_high, &tristar_low, &tristar_close, 0.1);
    assert_eq!(tristar_vals[2], 1.0);

    let tristar_open_bear = vec![100.0, 105.0, 100.0];
    let tristar_high_bear = vec![101.0, 105.5, 101.0];
    let tristar_low_bear = vec![99.5, 104.5, 99.6];
    let tristar_close_bear = vec![100.05, 105.05, 100.05];
    let tristar_bear = tristar(&tristar_open_bear, &tristar_high_bear, &tristar_low_bear, &tristar_close_bear, 0.1);
    assert_eq!(tristar_bear[2], -1.0);

    let ug_open = vec![100.0, 110.0, 111.0];
    let ug_high = vec![106.0, 111.0, 112.0];
    let ug_low = vec![99.0, 107.0, 105.0];
    let ug_close = vec![105.0, 108.0, 106.0];
    let ug_vals = upside_gap_two_crows(&ug_open, &ug_high, &ug_low, &ug_close);
    assert_eq!(ug_vals[2], -1.0);

    let gap_open = vec![100.0, 108.0, 108.5];
    let gap_high = vec![106.0, 113.0, 113.0];
    let gap_low = vec![99.0, 107.0, 108.0];
    let gap_close = vec![105.0, 112.0, 112.5];
    let gap_vals = gap_sidesidewhite(&gap_open, &gap_high, &gap_low, &gap_close);
    assert_eq!(gap_vals[2], 1.0);

    let gap_open_bear = vec![110.0, 95.0, 95.5];
    let gap_high_bear = vec![111.0, 100.0, 100.0];
    let gap_low_bear = vec![99.0, 94.0, 94.5];
    let gap_close_bear = vec![100.0, 99.0, 99.5];
    let gap_bear = gap_sidesidewhite(&gap_open_bear, &gap_high_bear, &gap_low_bear, &gap_close_bear);
    assert_eq!(gap_bear[2], -1.0);

    let adv_open = vec![100.0, 111.0, 119.0];
    let adv_high = vec![112.0, 121.0, 128.0];
    let adv_low = vec![99.0, 110.0, 118.0];
    let adv_close = vec![110.0, 118.0, 124.0];
    let adv_vals = advance_block(&adv_open, &adv_high, &adv_low, &adv_close);
    assert_eq!(adv_vals[2], -1.0);

    let stalled_open = vec![100.0, 110.0, 120.0];
    let stalled_high = vec![112.0, 121.0, 130.0];
    let stalled_low = vec![99.0, 109.0, 118.0];
    let stalled_close = vec![110.0, 120.0, 122.0];
    let stalled_vals = stalled_pattern(&stalled_open, &stalled_high, &stalled_low, &stalled_close);
    assert_eq!(stalled_vals[2], -1.0);

    let u3_open = vec![120.0, 99.0, 98.0];
    let u3_high = vec![121.0, 100.0, 102.0];
    let u3_low = vec![98.0, 90.0, 97.0];
    let u3_close = vec![100.0, 97.0, 101.0];
    let u3_vals = unique_3_river(&u3_open, &u3_high, &u3_low, &u3_close);
    assert_eq!(u3_vals[2], 1.0);

    let xgap_open = vec![100.0, 112.0, 114.0];
    let xgap_high = vec![111.0, 118.0, 115.0];
    let xgap_low = vec![99.0, 112.0, 111.2];
    let xgap_close = vec![110.0, 118.0, 111.5];
    let xgap_vals = xside_gap_3_methods(&xgap_open, &xgap_high, &xgap_low, &xgap_close);
    assert_eq!(xgap_vals[2], 1.0);

    let xgap_open_bear = vec![120.0, 94.0, 92.0];
    let xgap_high_bear = vec![121.0, 95.0, 98.0];
    let xgap_low_bear = vec![99.0, 88.0, 91.0];
    let xgap_close_bear = vec![100.0, 90.0, 97.0];
    let xgap_bear = xside_gap_3_methods(&xgap_open_bear, &xgap_high_bear, &xgap_low_bear, &xgap_close_bear);
    assert_eq!(xgap_bear[2], -1.0);
}

#[test]
fn test_candlestick_multi_candle_patterns() {
    use indicators::candlestick::*;

    let rising_open = vec![100.0, 108.0, 107.0, 106.0, 108.0];
    let rising_high = vec![111.0, 109.0, 108.0, 107.0, 113.0];
    let rising_low = vec![99.0, 105.0, 104.0, 103.0, 107.0];
    let rising_close = vec![110.0, 106.0, 105.0, 104.0, 112.0];
    let rising_vals = rising_three_methods(&rising_open, &rising_high, &rising_low, &rising_close);
    assert_eq!(rising_vals[4], 1.0);

    let falling_open = vec![110.0, 102.0, 103.0, 104.0, 105.0];
    let falling_high = vec![111.0, 105.0, 106.0, 107.0, 106.0];
    let falling_low = vec![99.0, 101.0, 102.0, 103.0, 95.0];
    let falling_close = vec![100.0, 104.0, 105.0, 106.0, 96.0];
    let falling_vals = falling_three_methods(&falling_open, &falling_high, &falling_low, &falling_close);
    assert_eq!(falling_vals[4], -1.0);

    let ladder_open = vec![110.0, 100.0, 90.0, 80.0, 78.0];
    let ladder_high = vec![111.0, 101.0, 91.0, 81.0, 91.0];
    let ladder_low = vec![99.0, 89.0, 79.0, 70.0, 77.0];
    let ladder_close = vec![100.0, 90.0, 80.0, 75.0, 90.0];
    let ladder_vals = ladder_bottom(&ladder_open, &ladder_high, &ladder_low, &ladder_close);
    assert_eq!(ladder_vals[4], 1.0);

    let mat_open = vec![100.0, 118.0, 116.0, 114.0, 118.0];
    let mat_high = vec![121.0, 119.0, 117.0, 115.0, 126.0];
    let mat_low = vec![99.0, 111.0, 109.0, 107.0, 117.0];
    let mat_close = vec![120.0, 112.0, 110.0, 108.0, 125.0];
    let mat_vals = mat_hold(&mat_open, &mat_high, &mat_low, &mat_close);
    assert_eq!(mat_vals[4], 1.0);

    let swallow_open = vec![120.0, 110.0, 95.0, 98.0];
    let swallow_high = vec![121.0, 111.0, 96.0, 99.0];
    let swallow_low = vec![109.0, 99.0, 89.0, 84.0];
    let swallow_close = vec![110.0, 100.0, 90.0, 85.0];
    let swallow_vals = concealing_baby_swallow(&swallow_open, &swallow_high, &swallow_low, &swallow_close);
    assert_eq!(swallow_vals[3], 1.0);

    let hikkake_open = vec![105.0, 105.0, 105.0];
    let hikkake_high = vec![110.0, 108.0, 109.0];
    let hikkake_low = vec![100.0, 102.0, 101.0];
    let hikkake_close = vec![105.0, 105.0, 105.0];
    let hikkake_vals = hikkake(&hikkake_open, &hikkake_high, &hikkake_low, &hikkake_close);
    assert_eq!(hikkake_vals[2], 1.0);

    let hikkake_open_mod = vec![105.0, 105.0, 105.0, 106.0];
    let hikkake_high_mod = vec![110.0, 108.0, 109.0, 111.0];
    let hikkake_low_mod = vec![100.0, 102.0, 101.0, 103.0];
    let hikkake_close_mod = vec![105.0, 105.0, 105.0, 107.0];
    let hikkake_mod_vals = hikkake_mod(&hikkake_open_mod, &hikkake_high_mod, &hikkake_low_mod, &hikkake_close_mod);
    assert_eq!(hikkake_mod_vals[3], 1.0);

    let break_open = vec![120.0, 95.0, 90.0, 85.0, 85.0];
    let break_high = vec![121.0, 96.0, 91.0, 86.0, 106.0];
    let break_low = vec![99.0, 89.0, 84.0, 79.0, 84.0];
    let break_close = vec![100.0, 90.0, 85.0, 80.0, 105.0];
    let break_vals = breakaway(&break_open, &break_high, &break_low, &break_close);
    assert_eq!(break_vals[4], 1.0);
}

#[test]
fn test_pandas_ta_core() {
    use indicators::pandas_ta::*;

    let close: Vec<f64> = (0..60)
        .map(|i| 100.0 + i as f64 * 0.5 + if i % 3 == 0 { 1.0 } else { 0.0 })
        .collect();
    let high: Vec<f64> = close.iter().map(|v| v + 1.0).collect();
    let low: Vec<f64> = close.iter().map(|v| v - 1.0).collect();
    let open: Vec<f64> = close.iter().map(|v| v - 0.3).collect();
    let volume: Vec<f64> = (0..60).map(|i| 100.0 + i as f64).collect();

    let ent = entropy(&close, 10, 5);
    assert!(!ent[20].is_nan());

    let ab = aberration(&high, &low, &close, 5, 5);
    assert!(!ab[10].is_nan());

    let (sq_on, sq_off, momentum) = squeeze(&high, &low, &close, 5, 2.0, 5, 5, 1.5);
    assert_eq!(sq_on.len(), close.len());
    assert_eq!(sq_off.len(), close.len());
    assert_eq!(momentum.len(), close.len());

    let (_fast, slow, signal) = qqe(&close, 3, 2, 1.0);
    assert!(slow.iter().any(|v| v.is_finite()));
    assert!(signal.iter().any(|&v| v == 1.0 || v == -1.0));

    let cti_vals = cti(&close, 5);
    assert!(!cti_vals[10].is_nan());

    let er_vals = er(&close, 5);
    assert!(!er_vals[10].is_nan());

    let bias_vals = bias(&close, 5);
    assert!(!bias_vals[10].is_nan());

    let psl_vals = psl(&close, 5);
    assert!(!psl_vals[10].is_nan());

    let (rvi_vals, rvi_signal) = rvi(&open, &high, &low, &close, 5, 3);
    assert_eq!(rvi_vals.len(), close.len());
    assert_eq!(rvi_signal.len(), close.len());

    let inertia_vals = inertia(&open, &high, &low, &close, 5, 5);
    assert_eq!(inertia_vals.len(), close.len());

    let (jaw, teeth, lips) = alligator(&high, &low, 13, 8, 5);
    assert_eq!(jaw.len(), close.len());
    assert_eq!(teeth.len(), close.len());
    assert_eq!(lips.len(), close.len());

    let efi_vals = efi(&close, &volume, 5);
    assert_eq!(efi_vals.len(), close.len());

    let (kst_vals, kst_signal) = kst(&close, 10, 15, 20, 30, 9);
    assert_eq!(kst_vals.len(), close.len());
    assert_eq!(kst_signal.len(), close.len());

    let stc_vals = stc(&close, 5, 10, 5);
    assert_eq!(stc_vals.len(), close.len());

    let tdfi_vals = tdfi(&close, 5, 3);
    assert_eq!(tdfi_vals.len(), close.len());

    let (wae_explosion, wae_dead) = wae(&close, 5, 10, 3, 5, 2.0);
    assert_eq!(wae_explosion.len(), close.len());
    assert_eq!(wae_dead.len(), close.len());

    let smi_vals = smi(&high, &low, &close, 5, 3, 2);
    assert_eq!(smi_vals.len(), close.len());

    let coppock_vals = coppock(&close, 5, 10, 5);
    assert_eq!(coppock_vals.len(), close.len());

    let pgo_vals = pgo(&high, &low, &close, 5);
    assert_eq!(pgo_vals.len(), close.len());

    let vwma_vals = vwma(&close, &volume, 5);
    assert_eq!(vwma_vals.len(), close.len());

    let alma_vals = alma(&close, 5, 0.85, 6.0);
    assert_eq!(alma_vals.len(), close.len());

    let vidya_vals = vidya(&close, 5);
    assert_eq!(vidya_vals.len(), close.len());

    let pwma_vals = pwma(&close, 5);
    assert_eq!(pwma_vals.len(), close.len());

    let sinwma_vals = sinwma(&close, 5);
    assert_eq!(sinwma_vals.len(), close.len());

    let swma_vals = swma(&close, 6);
    assert_eq!(swma_vals.len(), close.len());

    let bop_vals = bop(&open, &high, &low, &close);
    assert_eq!(bop_vals.len(), close.len());

    let (ssl_up, ssl_down) = ssl_channel(&high, &low, &close, 5);
    assert_eq!(ssl_up.len(), close.len());
    assert_eq!(ssl_down.len(), close.len());

    let cfo_vals = cfo(&close, 5);
    assert_eq!(cfo_vals.len(), close.len());

    let slope_vals = slope(&close, 5);
    assert_eq!(slope_vals.len(), close.len());

    let rank_vals = percent_rank(&close, 5);
    assert_eq!(rank_vals.len(), close.len());
}

#[test]
fn test_pandas_ta_edge_cases() {
    use indicators::pandas_ta::*;

    let close_short = vec![1.0, 2.0, 3.0];
    let high_short = vec![2.0, 3.0, 4.0];
    let low_short = vec![0.5, 1.5, 2.5];

    assert!(entropy(&close_short, 0, 5).iter().all(|v| v.is_nan()));
    assert!(entropy(&close_short, 2, 0).iter().all(|v| v.is_nan()));
    let entropy_flat = entropy(&vec![10.0; 12], 5, 5);
    assert_eq!(entropy_flat[5], 0.0);

    let aberration_bad = aberration(&high_short, &low_short, &close_short, 0, 2);
    assert!(aberration_bad.iter().all(|v| v.is_nan()));
    let flat = vec![10.0; 10];
    let aberration_zero = aberration(&flat, &flat, &flat, 3, 3);
    assert!(aberration_zero[3].is_nan());

    let close_flat = vec![100.0; 20];
    let high_wide = vec![110.0; 20];
    let low_wide = vec![90.0; 20];
    let (sq_on, sq_off, _mom) = squeeze(&high_wide, &low_wide, &close_flat, 5, 2.0, 5, 5, 1.5);
    assert_eq!(sq_on[10], 1.0);
    assert_eq!(sq_off[10], 0.0);
    assert!(sq_on[0].is_nan());

    let close_var = vec![100.0, 110.0, 90.0, 115.0, 85.0];
    let high_narrow: Vec<f64> = close_var.iter().map(|v| v + 0.1).collect();
    let low_narrow: Vec<f64> = close_var.iter().map(|v| v - 0.1).collect();
    let (_sq_on, sq_off_var, _) = squeeze(&high_narrow, &low_narrow, &close_var, 3, 2.0, 3, 3, 1.5);
    assert_eq!(sq_off_var[4], 1.0);

    let (_fast, slow_short, _signal) = qqe(&close_short, 10, 2, 1.0);
    assert!(slow_short.iter().all(|v| v.is_nan()));

    let cti_flat = cti(&vec![1.0; 10], 5);
    assert_eq!(cti_flat[5], 0.0);

    let er_flat = er(&vec![10.0; 10], 3);
    assert_eq!(er_flat[3], 0.0);

    let bias_zero = bias(&vec![0.0; 5], 3);
    assert!(bias_zero[3].is_nan());

    let psl_bad = psl(&close_short, 0);
    assert!(psl_bad.iter().all(|v| v.is_nan()));

    let (rvi_flat, _sig_flat) = rvi(&flat, &flat, &flat, &flat, 3, 2);
    assert!(rvi_flat[3].is_nan());

    let inertia_bad = inertia(&flat, &flat, &flat, &flat, 3, 0);
    assert!(inertia_bad.iter().all(|v| v.is_nan()));

    let close_zero: Vec<f64> = (0..40).map(|i| if i == 0 { 0.0 } else { i as f64 }).collect();
    let (kst_vals, _kst_sig) = kst(&close_zero, 3, 4, 5, 6, 3);
    assert_eq!(kst_vals.len(), close_zero.len());

    let stc_const = stc(&vec![10.0; 20], 3, 5, 3);
    assert_eq!(stc_const[10], 50.0);

    let smi_flat = smi(&flat, &flat, &flat, 3, 2, 2);
    assert!(smi_flat[3].is_nan());

    let coppock_bad = coppock(&close_short, 2, 3, 0);
    assert!(coppock_bad.iter().all(|v| v.is_nan()));

    let pgo_zero = pgo(&flat, &flat, &flat, 3);
    assert!(pgo_zero[3].is_nan());

    let vwma_bad = vwma(&close_short, &[1.0, 2.0, 3.0], 0);
    assert!(vwma_bad.iter().all(|v| v.is_nan()));
    let vwma_zero = vwma(&close_short, &[0.0, 0.0, 0.0], 2);
    assert!(vwma_zero[2].is_nan());

    let alma_bad = alma(&close_short, 0, 0.85, 6.0);
    assert!(alma_bad.iter().all(|v| v.is_nan()));

    let vidya_bad = vidya(&close_short, 0);
    assert!(vidya_bad.iter().all(|v| v.is_nan()));
    let close_with_zero = vec![1.0, 2.0, 3.0, 0.0, 4.0];
    let vidya_vals = vidya(&close_with_zero, 3);
    assert!(vidya_vals[3].is_nan());

    let pwma_bad = pwma(&close_short, 0);
    assert!(pwma_bad.iter().all(|v| v.is_nan()));
    let sinwma_bad = sinwma(&close_short, 0);
    assert!(sinwma_bad.iter().all(|v| v.is_nan()));
    let swma_bad = swma(&close_short, 10);
    assert!(swma_bad.iter().all(|v| v.is_nan()));

    let bop_bad = bop(&[1.0], &[1.0, 2.0], &[1.0], &[1.0]);
    assert!(bop_bad[0].is_nan());
    let bop_zero = bop(&[1.0, 1.0], &[1.0, 1.0], &[1.0, 1.0], &[1.0, 1.0]);
    assert_eq!(bop_zero[0], 0.0);

    let cfo_bad = cfo(&close_short, 0);
    assert!(cfo_bad.iter().all(|v| v.is_nan()));
    let close_with_zero = vec![1.0, 2.0, 0.0, 3.0, 4.0, 5.0];
    let cfo_vals = cfo(&close_with_zero, 3);
    assert!(cfo_vals[2].is_nan());

    let slope_bad = slope(&close_short, 0);
    assert!(slope_bad.iter().all(|v| v.is_nan()));
    let slope_flat = slope(&vec![10.0; 10], 5);
    assert!(!slope_flat[5].is_nan());

    let rank_bad = percent_rank(&close_short, 0);
    assert!(rank_bad.iter().all(|v| v.is_nan()));
}

#[test]
fn test_candlestick_two_candle_branches() {
    use indicators::candlestick::*;

    let bull_eng = bullish_engulfing(&[10.0, 9.0, 8.0], &[8.0, 9.5, 7.0]);
    assert_eq!(bull_eng[1], 0.0);
    assert_eq!(bull_eng[2], 0.0);

    let bear_eng = bearish_engulfing(&[8.0, 9.0, 9.0], &[10.0, 8.5, 10.0]);
    assert_eq!(bear_eng[1], 0.0);
    assert_eq!(bear_eng[2], 0.0);

    let bull_harami = bullish_harami(&[10.0, 9.0, 8.0], &[8.0, 10.5, 7.0]);
    assert_eq!(bull_harami[1], 0.0);
    assert_eq!(bull_harami[2], 0.0);

    let bear_harami = bearish_harami(&[8.0, 9.0, 9.0], &[10.0, 7.5, 10.0]);
    assert_eq!(bear_harami[1], 0.0);
    assert_eq!(bear_harami[2], 0.0);

    let piercing = piercing_pattern(&[10.0, 9.0, 8.0], &[7.0, 8.0, 7.5], &[8.0, 9.5, 7.0]);
    assert_eq!(piercing[1], 0.0);
    assert_eq!(piercing[2], 0.0);

    let dark_cloud = dark_cloud_cover(&[8.0, 9.0, 9.5], &[12.0, 10.0, 10.5], &[10.0, 8.5, 10.0]);
    assert_eq!(dark_cloud[1], 0.0);
    assert_eq!(dark_cloud[2], 0.0);

    let tweez_top = tweezers_top(&[10.0, 11.0, 12.0], &[15.0, 18.0, 12.5], &[12.0, 10.0, 13.0], 0.01);
    assert_eq!(tweez_top[1], 0.0);
    assert_eq!(tweez_top[2], 0.0);

    let tweez_bot = tweezers_bottom(&[12.0, 11.0, 10.0], &[5.0, 8.0, 9.5], &[10.0, 12.0, 9.0], 0.01);
    assert_eq!(tweez_bot[1], 0.0);
    assert_eq!(tweez_bot[2], 0.0);
}

#[test]
fn test_candlestick_two_candle_extra_branches() {
    use indicators::candlestick::*;

    let homing = homing_pigeon(&[10.0, 9.0], &[10.5, 9.5], &[7.0, 7.5], &[8.0, 7.5]);
    assert_eq!(homing[1], 0.0);

    let homing_skip = homing_pigeon(&[10.0, 9.0], &[10.5, 9.5], &[7.0, 7.5], &[8.0, 9.5]);
    assert_eq!(homing_skip[1], 0.0);

    let matching = matching_low(&[10.0, 9.0], &[10.5, 9.5], &[7.0, 7.5], &[8.0, 7.0], 0.01);
    assert_eq!(matching[1], 0.0);

    let matching_skip = matching_low(&[10.0, 9.0], &[10.5, 9.5], &[7.0, 7.5], &[8.0, 9.5], 0.01);
    assert_eq!(matching_skip[1], 0.0);

    let separating = separating_lines(
        &[10.0, 9.0, 9.0],
        &[10.5, 9.7, 9.7],
        &[7.0, 8.8, 8.8],
        &[8.0, 9.5, 9.4],
        0.005,
    );
    assert_eq!(separating[1], 0.0);
    assert_eq!(separating[2], 0.0);

    let thrust = thrusting(&[10.0, 9.0, 8.0], &[10.5, 9.6, 9.2], &[7.0, 8.0, 7.5], &[8.0, 9.5, 7.0]);
    assert_eq!(thrust[1], 0.0);
    assert_eq!(thrust[2], 0.0);

    let inneck_vals = inneck(&[10.0, 9.0, 8.0], &[10.5, 9.7, 9.2], &[7.0, 8.0, 7.5], &[8.0, 9.5, 7.0], 0.01);
    assert_eq!(inneck_vals[1], 0.0);
    assert_eq!(inneck_vals[2], 0.0);

    let onneck_vals = onneck(&[10.0, 9.0, 9.0], &[10.5, 9.7, 9.6], &[7.0, 8.8, 8.9], &[8.0, 9.5, 9.4], 0.01);
    assert_eq!(onneck_vals[1], 0.0);
    assert_eq!(onneck_vals[2], 0.0);
}

#[test]
fn test_candlestick_two_candle_special_branches() {
    use indicators::candlestick::*;

    let open = vec![10.0, 11.0, 12.0];
    let high = vec![12.5, 11.2, 13.2];
    let low = vec![9.5, 10.8, 11.8];
    let close = vec![12.0, 11.05, 13.0];
    let harami = harami_cross(&open, &high, &low, &close, 0.2);
    assert_eq!(harami[1], -1.0);
    assert_eq!(harami[2], 0.0);

    let doji_bull = doji_star(&[10.0, 7.5], &[10.2, 7.6], &[7.8, 7.4], &[8.0, 7.52], 0.2);
    assert_eq!(doji_bull[1], 1.0);

    let doji_bear = doji_star(&[10.0, 12.6], &[12.2, 12.8], &[9.8, 12.5], &[12.0, 12.62], 0.2);
    assert_eq!(doji_bear[1], -1.0);

    let doji_none = doji_star(&[10.0, 11.0], &[10.6, 11.6], &[9.5, 10.8], &[9.0, 11.5], 0.05);
    assert_eq!(doji_none[1], 0.0);

    let counter_small_open = vec![10.0, 9.0];
    let counter_small_close = vec![10.0, 9.1];
    let counter_small_high = vec![10.2, 9.2];
    let counter_small_low = vec![9.8, 8.9];
    let counter_small = counterattack(&counter_small_open, &counter_small_high, &counter_small_low, &counter_small_close, 0.01);
    assert_eq!(counter_small[1], 0.0);

    let counter_no_match_open = vec![10.0, 9.0];
    let counter_no_match_close = vec![8.0, 7.0];
    let counter_no_match_high = vec![10.2, 9.2];
    let counter_no_match_low = vec![7.8, 6.8];
    let counter_no_match = counterattack(
        &counter_no_match_open,
        &counter_no_match_high,
        &counter_no_match_low,
        &counter_no_match_close,
        0.001,
    );
    assert_eq!(counter_no_match[1], 0.0);

    let kick_bear_open = vec![100.0, 98.0];
    let kick_bear_high = vec![110.1, 98.1];
    let kick_bear_low = vec![99.9, 87.9];
    let kick_bear_close = vec![110.0, 88.0];
    let kick_bear = kicking(&kick_bear_open, &kick_bear_high, &kick_bear_low, &kick_bear_close);
    assert_eq!(kick_bear[1], -1.0);

    let kick_none_open = vec![100.0, 99.0];
    let kick_none_high = vec![101.0, 100.0];
    let kick_none_low = vec![98.0, 97.5];
    let kick_none_close = vec![99.5, 99.2];
    let kick_none = kicking(&kick_none_open, &kick_none_high, &kick_none_low, &kick_none_close);
    assert_eq!(kick_none[1], 0.0);
}

#[test]
fn test_candlestick_three_candle_branches_a() {
    use indicators::candlestick::*;

    let morning_open = vec![10.0, 9.5, 9.6, 9.8];
    let morning_high = vec![10.2, 9.6, 10.4, 10.2];
    let morning_low = vec![7.5, 8.5, 9.0, 9.4];
    let morning_close = vec![8.0, 9.4, 10.2, 10.0];
    let morning = morning_star(&morning_open, &morning_high, &morning_low, &morning_close);
    assert_eq!(morning[2], 0.0);
    assert_eq!(morning[3], 0.0);

    let evening_open = vec![8.0, 9.5, 9.6, 9.0];
    let evening_high = vec![10.2, 9.8, 9.7, 9.3];
    let evening_low = vec![7.8, 9.0, 8.8, 8.7];
    let evening_close = vec![10.0, 9.4, 8.8, 9.1];
    let evening = evening_star(&evening_open, &evening_high, &evening_low, &evening_close);
    assert_eq!(evening[2], 0.0);
    assert_eq!(evening[3], 0.0);

    let soldiers_open = vec![10.0, 15.0, 20.0];
    let soldiers_high = vec![12.1, 17.1, 22.1];
    let soldiers_close = vec![12.0, 17.0, 22.0];
    let soldiers = three_white_soldiers(&soldiers_open, &soldiers_high, &soldiers_close);
    assert_eq!(soldiers[2], 0.0);

    let soldiers_open2 = vec![10.0, 15.0, 20.0];
    let soldiers_high2 = vec![12.1, 16.0, 21.0];
    let soldiers_close2 = vec![12.0, 14.0, 18.0];
    let soldiers2 = three_white_soldiers(&soldiers_open2, &soldiers_high2, &soldiers_close2);
    assert_eq!(soldiers2[2], 0.0);

    let crows_open = vec![20.0, 15.0, 10.0];
    let crows_low = vec![12.0, 10.0, 6.0];
    let crows_close = vec![18.0, 13.0, 8.0];
    let crows = three_black_crows(&crows_open, &crows_low, &crows_close);
    assert_eq!(crows[2], 0.0);

    let crows_open2 = vec![20.0, 15.0, 10.0];
    let crows_low2 = vec![12.0, 10.0, 6.0];
    let crows_close2 = vec![18.0, 16.0, 8.0];
    let crows2 = three_black_crows(&crows_open2, &crows_low2, &crows_close2);
    assert_eq!(crows2[2], 0.0);
}

#[test]
fn test_candlestick_three_candle_branches_b() {
    use indicators::candlestick::*;

    let mds_open = vec![10.0, 9.8, 9.5];
    let mds_high = vec![10.2, 9.9, 9.8];
    let mds_low = vec![7.8, 9.7, 9.2];
    let mds_close = vec![8.0, 9.75, 9.6];
    let mds = morning_doji_star(&mds_open, &mds_high, &mds_low, &mds_close, 0.3);
    assert_eq!(mds[2], 0.0);

    let eds_open = vec![8.0, 9.5, 9.2];
    let eds_high = vec![10.2, 9.6, 9.4];
    let eds_low = vec![7.8, 9.4, 8.8];
    let eds_close = vec![10.0, 9.45, 9.1];
    let eds = evening_doji_star(&eds_open, &eds_high, &eds_low, &eds_close, 0.3);
    assert_eq!(eds[2], 0.0);

    let inside_open = vec![10.0, 9.0, 9.5];
    let inside_high = vec![11.5, 10.5, 10.8];
    let inside_low = vec![9.5, 8.8, 9.0];
    let inside_close = vec![11.0, 10.0, 10.5];
    let inside = three_inside(&inside_open, &inside_high, &inside_low, &inside_close);
    assert_eq!(inside[2], 0.0);

    let outside_open = vec![10.0, 9.0, 9.5];
    let outside_high = vec![11.5, 10.5, 10.8];
    let outside_low = vec![9.5, 8.8, 9.0];
    let outside_close = vec![11.0, 10.0, 10.5];
    let outside = three_outside(&outside_open, &outside_high, &outside_low, &outside_close);
    assert_eq!(outside[2], 0.0);

    let baby_open = vec![10.0, 9.0, 9.5];
    let baby_high = vec![10.5, 9.5, 9.8];
    let baby_low = vec![7.5, 8.8, 9.0];
    let baby_close = vec![8.0, 9.2, 9.4];
    let baby = abandoned_baby(&baby_open, &baby_high, &baby_low, &baby_close, 0.1);
    assert_eq!(baby[2], 0.0);
}

#[test]
fn test_candlestick_three_candle_branches_c() {
    use indicators::candlestick::*;

    let crows_skip = identical_three_crows(
        &[10.0, 9.0, 8.0],
        &[10.5, 9.5, 8.5],
        &[7.5, 8.0, 7.0],
        &[9.0, 10.0, 7.0],
    );
    assert_eq!(crows_skip[2], 0.0);

    let crows_fail = identical_three_crows(
        &[10.0, 9.0, 8.0],
        &[10.5, 9.5, 8.5],
        &[7.0, 4.0, 6.0],
        &[8.0, 5.0, 7.0],
    );
    assert_eq!(crows_fail[2], 0.0);

    let stick_skip = stick_sandwich(
        &[10.0, 9.0, 8.0],
        &[10.5, 9.5, 8.5],
        &[7.5, 8.5, 7.0],
        &[8.0, 8.5, 7.0],
        0.01,
    );
    assert_eq!(stick_skip[2], 0.0);

    let stick_fail = stick_sandwich(
        &[10.0, 9.0, 9.5],
        &[10.5, 11.0, 10.0],
        &[7.5, 8.5, 6.5],
        &[8.0, 9.5, 7.0],
        0.01,
    );
    assert_eq!(stick_fail[2], 0.0);

    let tristar_skip = tristar(
        &[10.0, 9.0, 8.0],
        &[11.5, 9.2, 8.2],
        &[9.5, 8.9, 7.9],
        &[11.0, 9.05, 8.02],
        0.1,
    );
    assert_eq!(tristar_skip[2], 0.0);

    let tristar_none = tristar(
        &[10.0, 10.1, 10.05],
        &[10.2, 10.2, 10.2],
        &[9.9, 9.95, 9.95],
        &[10.02, 10.08, 10.03],
        0.1,
    );
    assert_eq!(tristar_none[2], 0.0);
}

#[test]
fn test_candlestick_three_candle_branches_d() {
    use indicators::candlestick::*;

    let ug_skip = upside_gap_two_crows(
        &[10.0, 11.0, 10.0],
        &[12.5, 12.2, 10.5],
        &[9.5, 10.8, 8.5],
        &[12.0, 12.0, 9.0],
    );
    assert_eq!(ug_skip[2], 0.0);

    let ug_fail = upside_gap_two_crows(
        &[10.0, 12.0, 11.0],
        &[12.5, 12.2, 11.2],
        &[9.5, 10.8, 9.8],
        &[12.0, 11.0, 10.0],
    );
    assert_eq!(ug_fail[2], 0.0);

    let gap_skip = gap_sidesidewhite(
        &[10.0, 9.0, 9.2],
        &[10.6, 9.2, 9.6],
        &[9.8, 8.5, 9.0],
        &[10.5, 8.8, 9.5],
    );
    assert_eq!(gap_skip[2], 0.0);

    let gap_fail = gap_sidesidewhite(
        &[10.0, 10.2, 10.25],
        &[10.6, 10.5, 10.55],
        &[9.8, 10.1, 10.2],
        &[10.5, 10.4, 10.45],
    );
    assert_eq!(gap_fail[2], 0.0);

    let adv_skip = advance_block(
        &[10.0, 9.0, 8.0],
        &[11.0, 9.5, 8.5],
        &[9.5, 8.5, 7.5],
        &[11.0, 8.5, 9.0],
    );
    assert_eq!(adv_skip[2], 0.0);

    let adv_fail = advance_block(
        &[10.0, 11.0, 12.0],
        &[12.5, 13.1, 14.1],
        &[9.5, 10.5, 11.5],
        &[12.0, 13.0, 14.0],
    );
    assert_eq!(adv_fail[2], 0.0);

    let stalled_skip = stalled_pattern(
        &[10.0, 9.0, 8.0],
        &[11.0, 9.5, 8.5],
        &[9.5, 8.5, 7.5],
        &[11.0, 8.5, 9.0],
    );
    assert_eq!(stalled_skip[2], 0.0);

    let stalled_fail = stalled_pattern(
        &[10.0, 11.0, 12.0],
        &[12.2, 13.2, 14.2],
        &[9.5, 10.5, 11.5],
        &[12.0, 13.0, 14.0],
    );
    assert_eq!(stalled_fail[2], 0.0);

    let u3_skip = unique_3_river(
        &[10.0, 9.0, 8.0],
        &[11.0, 9.5, 9.0],
        &[9.5, 8.5, 8.5],
        &[11.0, 7.0, 7.5],
    );
    assert_eq!(u3_skip[2], 0.0);

    let u3_continue = unique_3_river(
        &[12.0, 9.0, 8.6],
        &[12.5, 9.2, 9.0],
        &[7.5, 8.4, 8.5],
        &[8.0, 8.5, 8.8],
    );
    assert_eq!(u3_continue[2], 0.0);

    let xgap_up = xside_gap_3_methods(
        &[10.0, 13.0, 13.8],
        &[12.5, 14.5, 14.0],
        &[9.8, 13.2, 12.9],
        &[12.0, 14.0, 13.0],
    );
    assert_eq!(xgap_up[2], 1.0);

    let xgap_down = xside_gap_3_methods(
        &[12.0, 9.5, 9.6],
        &[12.2, 9.7, 9.8],
        &[9.8, 8.8, 9.0],
        &[10.0, 9.0, 9.75],
    );
    assert_eq!(xgap_down[2], -1.0);
}

#[test]
fn test_candlestick_multi_candle_branches() {
    use indicators::candlestick::*;

    let rising_open = vec![10.0, 14.0, 13.0, 12.0, 12.0];
    let rising_high = vec![15.5, 16.0, 13.5, 12.5, 16.5];
    let rising_low = vec![9.5, 12.0, 11.5, 10.5, 11.5];
    let rising_close = vec![15.0, 13.0, 12.0, 11.0, 16.0];
    let rising_vals = rising_three_methods(&rising_open, &rising_high, &rising_low, &rising_close);
    assert_eq!(rising_vals[4], 0.0);

    let rising_open2 = vec![10.0, 11.0, 12.0, 13.0, 14.0];
    let rising_high2 = vec![12.0, 13.0, 14.0, 15.0, 16.0];
    let rising_low2 = vec![9.5, 10.5, 11.5, 12.5, 13.5];
    let rising_close2 = vec![12.0, 13.0, 14.0, 15.0, 16.0];
    let rising_vals2 = rising_three_methods(&rising_open2, &rising_high2, &rising_low2, &rising_close2);
    assert_eq!(rising_vals2[4], 0.0);

    let falling_open = vec![15.0, 11.0, 12.0, 13.0, 13.0];
    let falling_high = vec![15.5, 16.0, 13.5, 14.5, 13.5];
    let falling_low = vec![9.5, 10.5, 11.5, 12.5, 8.5];
    let falling_close = vec![10.0, 12.0, 13.0, 14.0, 9.0];
    let falling_vals = falling_three_methods(&falling_open, &falling_high, &falling_low, &falling_close);
    assert_eq!(falling_vals[4], 0.0);

    let falling_open2 = vec![15.0, 14.0, 13.0, 12.0, 11.0];
    let falling_high2 = vec![15.5, 14.5, 13.5, 12.5, 11.5];
    let falling_low2 = vec![9.5, 8.5, 7.5, 6.5, 5.5];
    let falling_close2 = vec![10.0, 13.0, 12.0, 11.0, 10.0];
    let falling_vals2 = falling_three_methods(&falling_open2, &falling_high2, &falling_low2, &falling_close2);
    assert_eq!(falling_vals2[4], 0.0);

    let ladder_open = vec![10.0, 11.0, 12.0, 13.0, 14.0];
    let ladder_high = vec![10.5, 11.5, 12.5, 13.5, 14.5];
    let ladder_low = vec![9.5, 10.5, 11.5, 12.5, 13.5];
    let ladder_close = vec![9.0, 12.0, 11.0, 10.0, 15.0];
    let ladder_vals = ladder_bottom(&ladder_open, &ladder_high, &ladder_low, &ladder_close);
    assert_eq!(ladder_vals[4], 0.0);

    let ladder_open2 = vec![10.0, 9.0, 8.0, 7.0, 9.0];
    let ladder_high2 = vec![10.5, 9.5, 8.5, 7.6, 10.5];
    let ladder_low2 = vec![8.5, 7.5, 6.5, 7.4, 8.0];
    let ladder_close2 = vec![9.0, 8.0, 7.0, 7.5, 10.0];
    let ladder_vals2 = ladder_bottom(&ladder_open2, &ladder_high2, &ladder_low2, &ladder_close2);
    assert_eq!(ladder_vals2[4], 0.0);

    let mat_open = vec![10.0, 9.0, 8.0, 7.0, 6.0];
    let mat_high = vec![10.5, 9.5, 8.5, 7.5, 6.5];
    let mat_low = vec![9.5, 8.5, 7.5, 6.5, 5.5];
    let mat_close = vec![9.0, 8.0, 7.0, 6.0, 5.0];
    let mat_vals = mat_hold(&mat_open, &mat_high, &mat_low, &mat_close);
    assert_eq!(mat_vals[4], 0.0);

    let mat_open2 = vec![10.0, 12.0, 12.0, 12.0, 13.0];
    let mat_high2 = vec![16.5, 16.5, 13.5, 12.5, 17.5];
    let mat_low2 = vec![9.5, 11.5, 11.5, 11.5, 12.5];
    let mat_close2 = vec![16.0, 16.0, 13.0, 12.5, 17.0];
    let mat_vals2 = mat_hold(&mat_open2, &mat_high2, &mat_low2, &mat_close2);
    assert_eq!(mat_vals2[4], 0.0);

    let hikkake_vals = hikkake(&[0.0, 0.0, 0.0], &[10.0, 9.0, 10.5], &[5.0, 6.0, 5.5], &[0.0, 0.0, 0.0]);
    assert_eq!(hikkake_vals[2], -1.0);

    let hikkake_mod_none = hikkake_mod(
        &[1.0, 2.0, 3.0, 4.0],
        &[3.0, 4.0, 5.0, 6.0],
        &[0.5, 1.5, 2.5, 3.5],
        &[2.0, 3.0, 4.0, 5.0],
    );
    assert_eq!(hikkake_mod_none[3], 0.0);

    let hikkake_mod_bear = hikkake_mod(
        &[7.0, 7.2, 7.1, 6.8],
        &[10.0, 9.0, 10.5, 9.0],
        &[5.0, 6.0, 5.5, 5.0],
        &[7.0, 7.2, 7.1, 6.8],
    );
    assert_eq!(hikkake_mod_bear[3], -1.0);

    let break_open = vec![10.0, 4.0, 3.5, 2.8, 2.5];
    let break_high = vec![10.2, 4.2, 3.7, 3.0, 8.2];
    let break_low = vec![4.8, 2.8, 2.4, 1.8, 2.3];
    let break_close = vec![5.0, 3.0, 2.5, 2.0, 8.0];
    let break_vals = breakaway(&break_open, &break_high, &break_low, &break_close);
    assert_eq!(break_vals[4], 1.0);

    let break_open2 = vec![5.0, 11.0, 12.0, 13.0, 13.0];
    let break_high2 = vec![10.2, 12.2, 13.2, 14.2, 13.5];
    let break_low2 = vec![4.8, 10.8, 11.8, 12.8, 6.5];
    let break_close2 = vec![10.0, 12.0, 13.0, 14.0, 7.0];
    let break_vals2 = breakaway(&break_open2, &break_high2, &break_low2, &break_close2);
    assert_eq!(break_vals2[4], -1.0);
}

#[test]
fn test_candlestick_single_line_branches() {
    use indicators::candlestick::*;

    let long_open = vec![100.0, 100.0, 100.0, 120.0];
    let long_high = vec![101.0, 101.0, 101.0, 120.5];
    let long_low = vec![99.0, 99.0, 99.0, 99.5];
    let long_close = vec![101.0, 101.0, 101.0, 100.0];
    let long_vals = long_line(&long_open, &long_high, &long_low, &long_close, 3);
    assert_eq!(long_vals[3], -1.0);

    let short_open = vec![100.0, 100.0, 100.0, 100.0, 100.0];
    let short_high = vec![101.0, 101.0, 101.0, 101.0, 102.0];
    let short_low = vec![99.0, 99.0, 99.0, 99.0, 99.0];
    let short_close = vec![101.0, 101.0, 101.0, 100.0, 102.0];
    let short_vals = short_line(&short_open, &short_high, &short_low, &short_close, 3);
    assert_eq!(short_vals[3], 0.0);
    assert_eq!(short_vals[4], 0.0);
}

#[test]
fn test_pandas_ta_missing_branches() {
    use indicators::pandas_ta::*;

    let close = vec![1.0, 1.1, 1.2];
    let entropy_short = entropy(&close, 1, 3);
    assert!(entropy_short[1].is_nan());

    let qqe_close = vec![10.0, 9.0, 10.0, 11.0];
    let (_fast, slow, signal) = qqe(&qqe_close, 1, 1, 1.0);
    assert_eq!(slow[3], slow[2]);
    assert_eq!(signal[3], 0.0);

    let cti_bad = cti(&close, close.len());
    assert!(cti_bad.iter().all(|v| v.is_nan()));

    let er_bad = er(&close, close.len());
    assert!(er_bad.iter().all(|v| v.is_nan()));

    let (rvi_bad, sig_bad) = rvi(&close, &close, &close, &close, close.len(), 2);
    assert!(rvi_bad.iter().all(|v| v.is_nan()));
    assert!(sig_bad.iter().all(|v| v.is_nan()));

    let cfo_short = cfo(&close, 1);
    assert!(cfo_short[0].is_nan());

    let slope_short = slope(&close, 1);
    assert!(slope_short[0].is_nan());
}

#[test]
fn test_momentum_missing_branches() {
    use indicators::momentum::{cmo, fisher_transform, ultimate_oscillator};

    let high = vec![10.0, 11.0, 12.0];
    let low = vec![9.0, 10.0, 11.0];
    let close = vec![9.5, 10.5, 11.5];
    let (fisher, trigger) = fisher_transform(&high, &low, &close, 2);
    assert!(!fisher[1].is_nan());
    assert_eq!(trigger[2], fisher[1]);

    let cmo_bad = cmo(&[1.0, 2.0], 2);
    assert!(cmo_bad.iter().all(|v| v.is_nan()));

    let high_uo = vec![10.0, 11.0, 12.0, 13.0, 14.0];
    let low_uo = vec![9.0, 10.0, 11.0, 12.0, 13.0];
    let close_uo = vec![9.5, 10.5, 11.5, 12.5, 13.5];
    let uo = ultimate_oscillator(&high_uo, &low_uo, &close_uo, 1, 1, 1);
    assert!(!uo[1].is_nan());
}

#[test]
fn test_trend_missing_branches() {
    use indicators::trend::{choppiness_index, supertrend, vhf, vortex};

    let high = vec![10.0, f64::NAN, 12.0, 13.0];
    let low = vec![9.0, f64::NAN, 11.0, 12.0];
    let close = vec![9.5, 9.0, 11.5, 12.5];
    let (st, dir, _, _) = supertrend(&high, &low, &close, 2, 3.0);
    assert!(st[1].is_nan());
    assert!(dir[1].is_nan());

    let high_v = vec![10.0, 11.0, 12.0, 11.0, 13.0];
    let low_v = vec![9.0, 10.0, 11.0, 10.0, 12.0];
    let close_v = vec![9.5, 10.5, 11.5, 10.5, 12.5];
    let (vi_plus, vi_minus) = vortex(&high_v, &low_v, &close_v, 2);
    assert!(!vi_plus[2].is_nan());
    assert!(!vi_minus[2].is_nan());

    let chop = choppiness_index(&high_v, &low_v, &close_v, 2);
    assert!(!chop[2].is_nan());

    let vhf_vals = vhf(&close_v, 2);
    assert!(!vhf_vals[2].is_nan());
}

#[test]
fn test_cycle_missing_branches() {
    use indicators::cycle::{ht_dcperiod, ht_sine, ht_trendmode};

    let values: Vec<f64> = (0..200).map(|i| (i as f64 * 3.0).sin() * 10.0 + 100.0).collect();
    let period = ht_dcperiod(&values);
    assert!(period.iter().any(|v| v.is_finite() && *v >= 6.0));
    assert!(period.iter().any(|v| v.is_finite() && *v < 15.0));

    let (sine, lead) = ht_sine(&values);
    assert!(sine.iter().any(|v| !v.is_nan()));
    assert!(lead.iter().any(|v| !v.is_nan()));

    let trend = ht_trendmode(&values);
    assert!(trend.iter().any(|v| v.is_finite()));
}

#[test]
fn test_cycle_phase_normalization_and_trendmode_thresholds() {
    use indicators::cycle::{ht_dcperiod, ht_dcphase, ht_trendmode};

    let values_phase: Vec<f64> = (0..200).map(|i| (i as f64 * 0.2).sin()).collect();
    let phase = ht_dcphase(&values_phase);
    assert!(phase.iter().any(|v| v.is_finite() && *v > 270.0));

    let mut selected = None;
    for freq in [0.03, 0.05, 0.07, 0.09, 0.11] {
        let values: Vec<f64> = (0..200).map(|i| (i as f64 * freq).sin()).collect();
        let period = ht_dcperiod(&values);
        let has_trend = (63..period.len()).any(|i| {
            let value = period[i];
            let slope = if i > 63 { value - period[i - 1] } else { 0.0 };
            value.is_finite() && (value > 40.0 || slope > 1.0)
        });
        if has_trend && selected.is_none() {
            selected = Some(values);
        }
    }

    let values_trend = selected.expect("expected period slope or threshold");
    let trend = ht_trendmode(&values_trend);
    assert!(trend.iter().any(|v| v.is_finite()));
}

#[test]
fn test_sfg_knn_branches() {
    let close: Vec<f64> = (0..40).map(|i| 100.0 + i as f64).collect();
    let high: Vec<f64> = close.iter().map(|v| v + 1.0).collect();
    let low: Vec<f64> = close.iter().map(|v| v - 1.0).collect();

    let (_st, dir) = indicators::ai_supertrend(&high, &low, &close, 1, 5, 1, 1, 2, 1.5);
    assert!(dir.iter().skip(6).any(|v| v.abs() == 1.0));

    let close_knn: Vec<f64> = (0..40)
        .map(|i| 100.0 + (i as f64 * 0.5) + if i % 2 == 0 { 1.0 } else { -1.0 })
        .collect();
    let (prediction, prediction_ma) = indicators::ai_momentum_index(&close_knn, 3, 2, 2);
    assert!(prediction.iter().any(|v| v.is_finite()));
    assert_eq!(prediction_ma.len(), close_knn.len());

    let close_sig = vec![100.0, 80.0, 60.0, 40.0, 20.0, 10.0];
    let high2: Vec<f64> = close_sig.iter().map(|v| v + 1.0).collect();
    let low2: Vec<f64> = close_sig.iter().map(|v| v - 1.0).collect();
    let volume: Vec<f64> = (1..=close_sig.len()).map(|i| i as f64 * 1000.0).collect();
    let (_signals, stop_loss, _take_profit) = indicators::atr2_signals(&high2, &low2, &close_sig, &volume, 2, 0.1, 1);
    assert!(stop_loss.iter().any(|v| v.is_finite()));
}
