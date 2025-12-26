from __future__ import annotations

import math
from typing import Any, Mapping, Sequence


def is_available() -> bool:
    try:
        from . import haze_library as _ext  # noqa: F401
    except Exception:
        return False
    return True


def get_available_ai_indicators() -> list[str]:
    return ["adaptive_rsi", "ensemble_signal", "ml_supertrend"]


def _clamp(value: float, lo: float, hi: float) -> float:
    return lo if value < lo else hi if value > hi else value


def _to_float_list(values: Sequence[float]) -> list[float]:
    return [float(v) for v in values]


def _rolling_volatility(values: Sequence[float], window: int) -> list[float]:
    if window <= 0:
        raise ValueError("volatility_window must be > 0")

    vols: list[float] = []
    returns: list[float] = []

    for i, v in enumerate(values):
        if i == 0:
            vols.append(0.0)
            continue

        prev = values[i - 1]
        if prev == 0.0 or math.isnan(prev) or math.isnan(v):
            ret = 0.0
        else:
            ret = (v - prev) / prev

        returns.append(ret)
        if len(returns) > window:
            returns.pop(0)

        if len(returns) < 2:
            vols.append(0.0)
            continue

        mean = sum(returns) / len(returns)
        var = sum((r - mean) ** 2 for r in returns) / len(returns)
        vols.append(math.sqrt(max(0.0, var)))

    return vols


def adaptive_rsi(
    close: Sequence[float],
    *,
    base_period: int = 14,
    min_period: int = 7,
    max_period: int = 28,
    volatility_window: int = 14,
) -> tuple[list[float], list[int]]:
    close_list = _to_float_list(close)
    if not close_list:
        return [], []

    if min_period <= 0 or max_period <= 0:
        raise ValueError("min_period/max_period must be > 0")
    if min_period > max_period:
        raise ValueError("min_period must be <= max_period")
    if base_period <= 0:
        raise ValueError("base_period must be > 0")

    from . import haze_library as _ext

    vols = _rolling_volatility(close_list, volatility_window)
    running_max = 0.0
    periods: list[int] = []
    for v in vols:
        running_max = max(running_max, v)
        if running_max == 0.0:
            p = base_period
        else:
            norm = v / (running_max + 1e-12)
            p = int(round(max_period - norm * (max_period - min_period)))
        periods.append(int(_clamp(p, min_period, max_period)))

    rsi_values = list(_ext.py_rsi(close_list, int(_clamp(base_period, 1, len(close_list)))))
    return rsi_values, periods


def ensemble_signal(
    high: Sequence[float],
    low: Sequence[float],
    close: Sequence[float],
    volume: Sequence[float] | None = None,
    *,
    weights: Mapping[str, float] | None = None,
) -> tuple[list[float], dict[str, list[float]]]:
    high_list = _to_float_list(high)
    low_list = _to_float_list(low)
    close_list = _to_float_list(close)
    if not (len(high_list) == len(low_list) == len(close_list)):
        raise ValueError("high/low/close lengths must match")

    from . import haze_library as _ext

    rsi = list(_ext.py_rsi(close_list, 14))
    macd_line, macd_signal, macd_hist = _ext.py_macd(close_list, 12, 26, 9)
    stoch_k, _stoch_d = _ext.py_stochastic(high_list, low_list, close_list, 14, 3)
    st_trend, st_dir, _st_upper, _st_lower = _ext.py_supertrend(high_list, low_list, close_list, 10, 3.0)

    mfi = None
    if volume is not None:
        volume_list = _to_float_list(volume)
        if len(volume_list) != len(close_list):
            raise ValueError("volume length must match close length")
        mfi = list(_ext.py_mfi(high_list, low_list, close_list, volume_list, 14))

    def rsi_sig(x: float) -> float:
        if math.isnan(x):
            return 0.0
        return _clamp((x - 50.0) / 50.0, -1.0, 1.0)

    def osc_sig(x: float) -> float:
        if math.isnan(x):
            return 0.0
        return _clamp((x - 50.0) / 50.0, -1.0, 1.0)

    def tanh_sig(x: float) -> float:
        if math.isnan(x):
            return 0.0
        return float(math.tanh(x))

    def dir_sig(x: float) -> float:
        if math.isnan(x):
            return 0.0
        return 1.0 if x > 0 else -1.0

    components: dict[str, list[float]] = {
        "rsi": [rsi_sig(x) for x in rsi],
        "macd": [tanh_sig(x) for x in macd_hist],
        "stochastic": [osc_sig(x) for x in stoch_k],
        "supertrend": [dir_sig(x) for x in st_dir],
    }
    if mfi is not None:
        components["mfi"] = [rsi_sig(x) for x in mfi]

    if weights is None:
        keys = list(components.keys())
        w = 1.0 / len(keys) if keys else 1.0
        weights = {k: w for k in keys}

    signal: list[float] = []
    for i in range(len(close_list)):
        s = 0.0
        for name, series in components.items():
            s += float(weights.get(name, 0.0)) * float(series[i])
        signal.append(_clamp(s, -1.0, 1.0))

    return signal, components


def ml_supertrend(
    high: Sequence[float],
    low: Sequence[float],
    close: Sequence[float],
    *,
    period: int = 10,
    multiplier: float = 3.0,
    confirmation_bars: int = 2,
    use_atr_filter: bool = True,
) -> tuple[list[float], list[float], list[float]]:
    high_list = _to_float_list(high)
    low_list = _to_float_list(low)
    close_list = _to_float_list(close)
    if not (len(high_list) == len(low_list) == len(close_list)):
        raise ValueError("high/low/close lengths must match")
    if not close_list:
        return [], [], []

    from . import haze_library as _ext

    trend, direction, _upper, _lower = _ext.py_supertrend(
        high_list,
        low_list,
        close_list,
        period,
        multiplier,
    )

    confirmed: list[float] = [math.nan] * len(close_list)
    if confirmation_bars <= 1:
        confirmed = list(direction)
    else:
        window: list[float] = []
        for i, d in enumerate(direction):
            if math.isnan(d):
                window.clear()
                continue
            window.append(float(d))
            if len(window) > confirmation_bars:
                window.pop(0)
            if len(window) == confirmation_bars and all(x == window[0] for x in window):
                confirmed[i] = window[0]

    confidence: list[float] = [0.0] * len(close_list)
    if use_atr_filter:
        atr = list(_ext.py_atr(high_list, low_list, close_list, period))
        for i, (d, a, c) in enumerate(zip(confirmed, atr, close_list)):
            if math.isnan(d) or math.isnan(a) or c == 0.0 or math.isnan(c):
                confidence[i] = 0.0
                continue
            atr_pct = abs(a / c)
            confidence[i] = _clamp(1.0 - atr_pct * 5.0, 0.0, 1.0)
    else:
        for i, d in enumerate(confirmed):
            confidence[i] = 1.0 if not math.isnan(d) else 0.0

    return list(trend), confirmed, confidence

