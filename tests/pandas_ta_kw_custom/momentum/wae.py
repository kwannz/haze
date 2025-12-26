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


def _stdev(values, length):
    n = len(values)
    if length < 2 or length > n:
        return pd.Series([np.nan] * n, index=values.index)

    result = [np.nan] * n
    vals = values.to_numpy()

    for i in range(length - 1, n):
        window = vals[i + 1 - length : i + 1]
        if np.isnan(window).any():
            result[i] = np.nan
            continue
        mean = window.mean()
        variance = ((window - mean) ** 2).sum() / (length - 1)
        result[i] = np.sqrt(variance)

    return pd.Series(result, index=values.index)


def wae(
    close,
    fast=None,
    slow=None,
    signal=None,
    length=None,
    multiplier=None,
    offset=None,
    **kwargs,
):
    """Waddah Attar Explosion (WAE)"""
    fast = int(fast) if fast and fast > 0 else 20
    slow = int(slow) if slow and slow > 0 else 40
    signal = int(signal) if signal and signal > 0 else 9
    length = int(length) if length and length > 0 else 20
    multiplier = float(multiplier) if multiplier and multiplier > 0 else 2.0
    close = verify_series(close, max(fast, slow, signal, length))
    offset = get_offset(offset)

    if close is None:
        return

    ema_fast = _ema(close, fast)
    ema_slow = _ema(close, slow)
    macd = ema_fast - ema_slow
    signal_line = _sma(macd, signal)
    explosion = (macd - signal_line).abs()
    dead_zone = _stdev(close, length) * multiplier * 2.0

    df = pd.DataFrame(
        {
            "WAE_EXPLOSION": explosion,
            "WAE_DEAD": dead_zone,
        },
        index=close.index,
    )

    df.name = f"WAE_{fast}_{slow}_{signal}_{length}_{multiplier}"
    df.category = "momentum"

    if offset != 0:
        df = df.shift(offset)

    if "fillna" in kwargs:
        df.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        df.fillna(method=kwargs["fill_method"], inplace=True)

    return df


def wae_method(
    self,
    fast=None,
    slow=None,
    signal=None,
    length=None,
    multiplier=None,
    offset=None,
    **kwargs,
):
    close = self._get_column(kwargs.pop("close", "close"))
    result = wae(
        close=close,
        fast=fast,
        slow=slow,
        signal=signal,
        length=length,
        multiplier=multiplier,
        offset=offset,
        **kwargs,
    )
    return self._post_process(result, **kwargs)
