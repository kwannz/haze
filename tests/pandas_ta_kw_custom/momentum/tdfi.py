# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from pandas_ta_classic.utils import get_offset, verify_series


def _ema(values, length):
    n = len(values)
    if length <= 0 or length > n:
        return pd.Series([np.nan] * n, index=values.index)

    alpha = 2.0 / (length + 1.0)
    result = [np.nan] * n
    total = 0.0
    count = 0
    start = None
    vals = values.to_numpy()

    for i in range(n):
        v = vals[i]
        if np.isnan(v):
            total = 0.0
            count = 0
            continue
        total += v
        count += 1
        if count == length:
            result[i] = total / length
            start = i
            break

    if start is not None:
        for i in range(start + 1, n):
            v = vals[i]
            if np.isnan(v):
                result[i] = result[i - 1]
            else:
                result[i] = alpha * v + (1.0 - alpha) * result[i - 1]

    return pd.Series(result, index=values.index)


def tdfi(close, length=None, smooth=None, offset=None, **kwargs):
    """Trend Direction Force Index (TDFI)"""
    length = int(length) if length and length > 0 else 13
    smooth = int(smooth) if smooth and smooth > 0 else 3
    close = verify_series(close, max(length, smooth))
    offset = get_offset(offset)

    if close is None:
        return

    tdf = (close - close.shift(length)).abs()
    tdfi = _ema(tdf, smooth)

    if offset != 0:
        tdfi = tdfi.shift(offset)

    if "fillna" in kwargs:
        tdfi.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        tdfi.fillna(method=kwargs["fill_method"], inplace=True)

    tdfi.name = f"TDFI_{length}_{smooth}"
    tdfi.category = "momentum"

    return tdfi


def tdfi_method(self, length=None, smooth=None, offset=None, **kwargs):
    close = self._get_column(kwargs.pop("close", "close"))
    result = tdfi(close=close, length=length, smooth=smooth, offset=offset, **kwargs)
    return self._post_process(result, **kwargs)
