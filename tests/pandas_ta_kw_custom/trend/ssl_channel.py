# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from pandas_ta_classic.utils import get_offset, verify_series


def _sma(values, length):
    n = len(values)
    if length <= 0 or length > n:
        return pd.Series([np.nan] * n, index=values.index)

    result = [np.nan] * n
    total = 0.0
    count = 0
    vals = values.to_numpy()

    for i in range(n):
        v = vals[i]
        if np.isnan(v):
            total = 0.0
            count = 0
            continue
        total += v
        count += 1
        if count > length:
            total -= vals[i - length]
            count = length
        if count == length:
            result[i] = total / length

    return pd.Series(result, index=values.index)


def ssl_channel(high, low, close, length=None, offset=None, **kwargs):
    """SSL Channel"""
    length = int(length) if length and length > 0 else 10
    high = verify_series(high, length)
    low = verify_series(low, length)
    close = verify_series(close, length)
    offset = get_offset(offset)

    if high is None or low is None or close is None:
        return

    sma_high = _sma(high, length)
    sma_low = _sma(low, length)

    n = len(close)
    up = [np.nan] * n
    down = [np.nan] * n
    close_vals = close.to_numpy()
    high_vals = sma_high.to_numpy()
    low_vals = sma_low.to_numpy()

    for i in range(length - 1, n):
        h = high_vals[i]
        l = low_vals[i]
        c = close_vals[i]
        if np.isnan(h) or np.isnan(l) or np.isnan(c):
            continue
        if c > h:
            up[i] = l
            down[i] = h
        else:
            up[i] = h
            down[i] = l

    df = pd.DataFrame({"SSL_UP": up, "SSL_DOWN": down}, index=close.index)
    df.name = f"SSL_{length}"
    df.category = "trend"

    if offset != 0:
        df = df.shift(offset)

    if "fillna" in kwargs:
        df.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        df.fillna(method=kwargs["fill_method"], inplace=True)

    return df


def ssl_channel_method(self, length=None, offset=None, **kwargs):
    high = self._get_column(kwargs.pop("high", "high"))
    low = self._get_column(kwargs.pop("low", "low"))
    close = self._get_column(kwargs.pop("close", "close"))
    result = ssl_channel(
        high=high,
        low=low,
        close=close,
        length=length,
        offset=offset,
        **kwargs,
    )
    return self._post_process(result, **kwargs)
