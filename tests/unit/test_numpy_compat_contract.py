"""
NumPy Compatibility Layer Contract Tests
=======================================

验证 `haze_library.np_ta` (numpy_compat) 的函数签名与返回值结构与 Rust extension 一致，
确保 NumPy 工作流不会因 wrapper 契约断链而在运行时崩溃。
"""

from __future__ import annotations

import numpy as np

import haze_library


def _assert_array(arr: np.ndarray, length: int) -> None:
    assert isinstance(arr, np.ndarray)
    assert arr.shape == (length,)


class TestNumpyCompatContract:
    def test_multi_output_indicators(self, ohlcv_data_extended):
        assert haze_library.np_ta is not None

        high = np.array(ohlcv_data_extended["high"], dtype=np.float64)
        low = np.array(ohlcv_data_extended["low"], dtype=np.float64)
        close = np.array(ohlcv_data_extended["close"], dtype=np.float64)
        n = len(close)

        k, d = haze_library.np_ta.stochastic(high, low, close, smooth_k=3)
        _assert_array(k, n)
        _assert_array(d, n)

        k, d = haze_library.np_ta.stochrsi(close, period=14, k_period=3, d_period=3)
        _assert_array(k, n)
        _assert_array(d, n)

        k, d, j = haze_library.np_ta.kdj(high, low, close, k_period=9, d_period=3, j_period=3)
        _assert_array(k, n)
        _assert_array(d, n)
        _assert_array(j, n)

        tsi, signal = haze_library.np_ta.tsi(close, fast=13, slow=25, signal=13)
        _assert_array(tsi, n)
        _assert_array(signal, n)

        sar, direction = haze_library.np_ta.psar(
            high, low, close, af_start=0.02, af_increment=0.02, af_max=0.2
        )
        _assert_array(sar, n)
        _assert_array(direction, n)

    def test_candlestick_and_utilities(self, ohlcv_data_extended):
        assert haze_library.np_ta is not None

        open_ = np.array(ohlcv_data_extended["open"], dtype=np.float64)
        high = np.array(ohlcv_data_extended["high"], dtype=np.float64)
        low = np.array(ohlcv_data_extended["low"], dtype=np.float64)
        close = np.array(ohlcv_data_extended["close"], dtype=np.float64)
        n = len(close)

        ha_o, ha_h, ha_l, ha_c = haze_library.np_ta.heikin_ashi(open_, high, low, close)
        _assert_array(ha_o, n)
        _assert_array(ha_h, n)
        _assert_array(ha_l, n)
        _assert_array(ha_c, n)

        engulfing = haze_library.np_ta.engulfing(open_, high, low, close)
        _assert_array(engulfing, n)

        highest = haze_library.np_ta.highest(high, period=5)
        _assert_array(highest, n)

        lowest = haze_library.np_ta.lowest(low, period=5)
        _assert_array(lowest, n)

        crossover = haze_library.np_ta.crossover(close, close)
        _assert_array(crossover, n)

        crossunder = haze_library.np_ta.crossunder(close, close)
        _assert_array(crossunder, n)

    def test_statistical_wrappers(self, ohlcv_data_extended):
        assert haze_library.np_ta is not None

        close = np.array(ohlcv_data_extended["close"], dtype=np.float64)
        n = len(close)

        variance = haze_library.np_ta.variance(close, period=5)
        _assert_array(variance, n)

        stddev = haze_library.np_ta.stddev(close, period=5)
        _assert_array(stddev, n)

        lr = haze_library.np_ta.linear_regression(close, period=5)
        _assert_array(lr, n)

        slope = haze_library.np_ta.linreg_slope(close, period=5)
        _assert_array(slope, n)

        angle = haze_library.np_ta.linreg_angle(close, period=5)
        _assert_array(angle, n)

        intercept = haze_library.np_ta.linreg_intercept(close, period=5)
        _assert_array(intercept, n)
