"""
Pandas Accessor Contract Tests
==============================

验证 pandas DataFrame/Series `.haze` accessor 与 Rust extension 的调用契约一致，
避免因参数/返回值不匹配导致的运行时 TypeError/ValueError。
"""

from __future__ import annotations

import pandas as pd
import pytest

# Import haze_library to register the `.ta` accessor
import haze_library  # noqa: F401
from haze_library import ColumnNotFoundError


def _assert_series(series: pd.Series, index: pd.Index) -> None:
    assert isinstance(series, pd.Series)
    assert series.index.equals(index)
    assert len(series) == len(index)


def _get_df_accessor(df: pd.DataFrame):
    return getattr(df, "haze") if hasattr(df, "haze") else df.ta


def _get_series_accessor(series: pd.Series):
    return getattr(series, "haze") if hasattr(series, "haze") else series.ta


class TestDataFrameAccessorContract:
    def test_accessor_is_registered(self):
        df = pd.DataFrame({"close": [1.0, 2.0, 3.0]})
        assert hasattr(df, "haze")
        assert hasattr(df["close"], "haze")

    def test_removed_params_fail_fast(self, ohlcv_data_extended):
        df = pd.DataFrame(ohlcv_data_extended)
        ta = _get_df_accessor(df)

        with pytest.raises(TypeError):
            ta.stochastic(smooth_k=3)

        with pytest.raises(TypeError):
            ta.kdj(j_period=3)

    def test_missing_column_raises_typed_error(self):
        df = pd.DataFrame({"close": [1.0, 2.0, 3.0]})
        ta = _get_df_accessor(df)

        with pytest.raises(ColumnNotFoundError):
            ta.sma(period=2, column="not_a_column")

    def test_multi_output_indicators(self, ohlcv_data_extended):
        df = pd.DataFrame(ohlcv_data_extended)
        ta = _get_df_accessor(df)

        k, d = ta.stochastic()
        _assert_series(k, df.index)
        _assert_series(d, df.index)

        k, d = ta.stochrsi(period=14, k_period=3, d_period=3)
        _assert_series(k, df.index)
        _assert_series(d, df.index)

        k, d, j = ta.kdj(k_period=9, d_period=3)
        _assert_series(k, df.index)
        _assert_series(d, df.index)
        _assert_series(j, df.index)

        tsi, signal = ta.tsi(fast=13, slow=25, signal=13)
        _assert_series(tsi, df.index)
        _assert_series(signal, df.index)

        sar, direction = ta.psar(af_start=0.02, af_increment=0.02, af_max=0.2)
        _assert_series(sar, df.index)
        _assert_series(direction, df.index)

    def test_candlestick_and_utilities(self, ohlcv_data_extended):
        df = pd.DataFrame(ohlcv_data_extended)
        ta = _get_df_accessor(df)

        ha_o, ha_h, ha_l, ha_c = ta.heikin_ashi()
        _assert_series(ha_o, df.index)
        _assert_series(ha_h, df.index)
        _assert_series(ha_l, df.index)
        _assert_series(ha_c, df.index)

        engulfing = ta.engulfing()
        _assert_series(engulfing, df.index)

        highest = ta.highest(period=5, column="high")
        _assert_series(highest, df.index)

        lowest = ta.lowest(period=5, column="low")
        _assert_series(lowest, df.index)

        crossover = ta.crossover(df["close"], df["close"])
        _assert_series(crossover, df.index)

        crossunder = ta.crossunder(df["close"], df["close"])
        _assert_series(crossunder, df.index)

    def test_statistical_wrappers(self, ohlcv_data_extended):
        df = pd.DataFrame(ohlcv_data_extended)
        ta = _get_df_accessor(df)

        variance = ta.variance(period=5)
        _assert_series(variance, df.index)

        stddev = ta.stddev(period=5)
        _assert_series(stddev, df.index)

        lr = ta.linear_regression(period=5)
        _assert_series(lr, df.index)

        slope = ta.linreg_slope(period=5)
        _assert_series(slope, df.index)

        angle = ta.linreg_angle(period=5)
        _assert_series(angle, df.index)

        intercept = ta.linreg_intercept(period=5)
        _assert_series(intercept, df.index)


class TestSeriesAccessorContract:
    def test_series_statistical_wrappers(self, ohlcv_data_extended):
        df = pd.DataFrame(ohlcv_data_extended)
        close = df["close"]
        ta = _get_series_accessor(close)

        stddev = ta.stddev(period=5)
        _assert_series(stddev, close.index)

        variance = ta.variance(period=5)
        _assert_series(variance, close.index)

        lr = ta.linear_regression(period=5)
        _assert_series(lr, close.index)
