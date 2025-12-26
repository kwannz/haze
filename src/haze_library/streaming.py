from __future__ import annotations

import math
import threading
from collections import deque
from dataclasses import dataclass
from typing import Any, Dict, Iterable, Mapping


_NAN = float("nan")


def _is_nan(value: float) -> bool:
    return math.isnan(value)


def _clamp(value: float, lo: float, hi: float) -> float:
    return lo if value < lo else hi if value > hi else value


class IncrementalSMA:
    def __init__(self, period: int) -> None:
        if period <= 0:
            raise ValueError("period must be > 0")
        self.period = int(period)
        self._lock = threading.Lock()
        self.reset()

    def reset(self) -> None:
        with self._lock:
            self.window: deque[float] = deque(maxlen=self.period)
            self._sum = 0.0
            self._nan_count = 0
            self.count = 0
            self._current = _NAN

    @property
    def is_ready(self) -> bool:
        return self.count >= self.period

    @property
    def current(self) -> float:
        return self._current

    def update(self, value: float) -> float:
        v = float(value)
        with self._lock:
            if len(self.window) == self.period:
                old = self.window[0]
                if _is_nan(old):
                    self._nan_count -= 1
                else:
                    self._sum -= old

            self.window.append(v)
            self.count += 1

            if _is_nan(v):
                self._nan_count += 1
            else:
                self._sum += v

            if len(self.window) < self.period or self._nan_count > 0:
                self._current = _NAN
            else:
                self._current = self._sum / self.period
            return self._current

    def update_batch(self, values: Iterable[float]) -> list[float]:
        return [self.update(v) for v in values]

    def status(self) -> dict[str, Any]:
        return {"count": self.count, "is_ready": self.is_ready, "current": self.current}


class IncrementalEMA:
    def __init__(self, period: int) -> None:
        if period <= 0:
            raise ValueError("period must be > 0")
        self.period = int(period)
        self._alpha = 2.0 / (self.period + 1.0)
        self._lock = threading.Lock()
        self.reset()

    def reset(self) -> None:
        with self._lock:
            self.count = 0
            self._warmup_count = 0
            self._warmup_sum = 0.0
            self._current = _NAN

    @property
    def is_ready(self) -> bool:
        return self.count >= self.period

    @property
    def current(self) -> float:
        return self._current

    def update(self, value: float) -> float:
        v = float(value)
        with self._lock:
            self.count += 1
            if self._warmup_count < self.period:
                self._warmup_count += 1
                self._warmup_sum += v
                if self._warmup_count == self.period:
                    self._current = self._warmup_sum / self.period
                else:
                    self._current = _NAN
                return self._current

            self._current = self._alpha * v + (1.0 - self._alpha) * self._current
            return self._current

    def status(self) -> dict[str, Any]:
        return {"count": self.count, "is_ready": self.is_ready, "current": self.current}


class IncrementalRSI:
    def __init__(self, period: int = 14) -> None:
        if period <= 0:
            raise ValueError("period must be > 0")
        self.period = int(period)
        self._lock = threading.Lock()
        self.reset()

    def reset(self) -> None:
        with self._lock:
            self.count = 0
            self._prev: float | None = None
            self._gains: list[float] = []
            self._losses: list[float] = []
            self._avg_gain: float | None = None
            self._avg_loss: float | None = None
            self._current = _NAN

    @property
    def is_ready(self) -> bool:
        return self.count >= self.period

    @property
    def current(self) -> float:
        return self._current

    def update(self, value: float) -> float:
        v = float(value)
        with self._lock:
            if self.count == 0:
                self.count = 1
                self._prev = v
                self._gains = [0.0]
                self._losses = [0.0]
                self._current = _NAN
                return self._current

            assert self._prev is not None
            change = v - self._prev
            gain = max(change, 0.0)
            loss = max(-change, 0.0)

            self.count += 1

            if self._avg_gain is None or self._avg_loss is None:
                self._gains.append(gain)
                self._losses.append(loss)
                if self.count < self.period:
                    self._prev = v
                    self._current = _NAN
                    return self._current

                self._avg_gain = sum(self._gains[: self.period]) / self.period
                self._avg_loss = sum(self._losses[: self.period]) / self.period
            else:
                self._avg_gain = (self._avg_gain * (self.period - 1) + gain) / self.period
                self._avg_loss = (self._avg_loss * (self.period - 1) + loss) / self.period

            self._prev = v
            self._current = _rsi_value(self._avg_gain, self._avg_loss)
            return self._current

    def status(self) -> dict[str, Any]:
        return {"count": self.count, "is_ready": self.is_ready, "current": self.current}


def _rsi_value(avg_gain: float, avg_loss: float) -> float:
    if avg_loss == 0.0 and avg_gain == 0.0:
        return 50.0
    if avg_loss == 0.0:
        return 100.0
    rs = avg_gain / avg_loss
    return 100.0 - (100.0 / (1.0 + rs))


class IncrementalMACD:
    def __init__(self, fast: int = 12, slow: int = 26, signal: int = 9) -> None:
        if fast <= 0 or slow <= 0 or signal <= 0:
            raise ValueError("fast/slow/signal must be > 0")
        if slow <= fast:
            raise ValueError("slow must be > fast")

        self.fast = int(fast)
        self.slow = int(slow)
        self.signal = int(signal)

        self._ema_fast = IncrementalEMA(self.fast)
        self._ema_slow = IncrementalEMA(self.slow)

        self._signal_alpha = 2.0 / (self.signal + 1.0)
        self._signal_count = 0
        self._signal_warmup: list[float] = []
        self._signal_value = _NAN

        self._lock = threading.Lock()
        self.count = 0
        self._current = (_NAN, _NAN, _NAN)

    @property
    def is_ready(self) -> bool:
        return not _is_nan(self._current[1])

    def reset(self) -> None:
        with self._lock:
            self.count = 0
            self._ema_fast.reset()
            self._ema_slow.reset()
            self._signal_count = 0
            self._signal_warmup = []
            self._signal_value = _NAN
            self._current = (_NAN, _NAN, _NAN)

    def update(self, value: float) -> tuple[float, float, float]:
        v = float(value)
        with self._lock:
            self.count += 1
            fast_val = self._ema_fast.update(v)
            slow_val = self._ema_slow.update(v)
            if _is_nan(fast_val) or _is_nan(slow_val):
                self._current = (_NAN, _NAN, _NAN)
                return self._current

            macd_line = fast_val - slow_val
            signal_line = self._update_signal(macd_line)
            histogram = macd_line - signal_line if not _is_nan(signal_line) else _NAN
            self._current = (macd_line, signal_line, histogram)
            return self._current

    def _update_signal(self, value: float) -> float:
        if _is_nan(value):
            return _NAN

        self._signal_count += 1
        if self._signal_count < self.signal:
            self._signal_warmup.append(value)
            return _NAN

        if self._signal_count == self.signal:
            self._signal_warmup.append(value)
            self._signal_value = sum(self._signal_warmup) / self.signal
            return self._signal_value

        if _is_nan(self._signal_value):
            self._signal_value = value
        else:
            self._signal_value = self._signal_alpha * value + (1.0 - self._signal_alpha) * self._signal_value
        return self._signal_value

    def status(self) -> dict[str, Any]:
        line, sig, hist = self._current
        return {
            "count": self.count,
            "is_ready": self.is_ready,
            "macd": line,
            "signal": sig,
            "histogram": hist,
        }


class IncrementalATR:
    def __init__(self, period: int = 14) -> None:
        if period <= 0:
            raise ValueError("period must be > 0")
        self.period = int(period)
        self._lock = threading.Lock()
        self.reset()

    def reset(self) -> None:
        with self._lock:
            self.count = 0
            self._prev_close: float | None = None
            self._tr_values: list[float] = []
            self._atr = _NAN

    @property
    def is_ready(self) -> bool:
        return self.count >= self.period

    @property
    def current(self) -> float:
        return self._atr

    def update(self, high: float, low: float, close: float) -> float:
        h = float(high)
        l = float(low)
        c = float(close)

        with self._lock:
            self.count += 1
            if self._prev_close is None:
                tr = h - l
                self._prev_close = c
            else:
                prev = self._prev_close
                tr = max(h - l, abs(h - prev), abs(l - prev))
                self._prev_close = c

            if self.count < self.period:
                self._tr_values.append(tr)
                self._atr = _NAN
                return self._atr

            if self.count == self.period:
                self._tr_values.append(tr)
                self._atr = sum(self._tr_values[: self.period]) / self.period
                return self._atr

            self._atr = (self._atr * (self.period - 1) + tr) / self.period
            return self._atr

    def status(self) -> dict[str, Any]:
        return {"count": self.count, "is_ready": self.is_ready, "current": self.current}


class IncrementalSuperTrend:
    def __init__(self, period: int = 10, multiplier: float = 3.0) -> None:
        if period <= 0:
            raise ValueError("period must be > 0")
        self.period = int(period)
        self.multiplier = float(multiplier)
        self._lock = threading.Lock()
        self._atr = IncrementalATR(period=self.period)
        self.reset()

    def reset(self) -> None:
        with self._lock:
            self.count = 0
            self._atr.reset()
            self._prev_close: float | None = None
            self._prev_final_upper = _NAN
            self._prev_final_lower = _NAN
            self._trend = _NAN
            self._direction = _NAN
            self.current_direction = _NAN

    @property
    def is_ready(self) -> bool:
        return self._atr.is_ready

    def update(self, high: float, low: float, close: float) -> tuple[float, float]:
        h = float(high)
        l = float(low)
        c = float(close)

        with self._lock:
            self.count += 1
            atr = self._atr.update(h, l, c)
            if not self._atr.is_ready or _is_nan(atr):
                self._prev_close = c
                self._trend = _NAN
                self._direction = _NAN
                return self._trend, self._direction

            hl2 = (h + l) / 2.0
            basic_upper = hl2 + self.multiplier * atr
            basic_lower = hl2 - self.multiplier * atr

            if _is_nan(self._prev_final_upper) or (basic_upper < self._prev_final_upper) or (
                self._prev_close is not None and self._prev_close > self._prev_final_upper
            ):
                final_upper = basic_upper
            else:
                final_upper = self._prev_final_upper

            if _is_nan(self._prev_final_lower) or (basic_lower > self._prev_final_lower) or (
                self._prev_close is not None and self._prev_close < self._prev_final_lower
            ):
                final_lower = basic_lower
            else:
                final_lower = self._prev_final_lower

            if _is_nan(self._direction):
                direction = 1.0
            else:
                direction = self._direction

            if direction > 0 and c < final_lower:
                direction = -1.0
            elif direction < 0 and c > final_upper:
                direction = 1.0

            trend = final_lower if direction > 0 else final_upper

            self._prev_final_upper = final_upper
            self._prev_final_lower = final_lower
            self._prev_close = c
            self._trend = trend
            self._direction = direction
            self.current_direction = direction
            return trend, direction

    def status(self) -> dict[str, Any]:
        return {
            "count": self.count,
            "is_ready": self.is_ready,
            "trend": self._trend,
            "direction": self._direction,
        }


class IncrementalBollingerBands:
    def __init__(self, period: int = 20, std_dev: float = 2.0) -> None:
        if period <= 0:
            raise ValueError("period must be > 0")
        self.period = int(period)
        self.std_dev = float(std_dev)
        self._lock = threading.Lock()
        self.reset()

    def reset(self) -> None:
        with self._lock:
            self.count = 0
            self._values: deque[float] = deque(maxlen=self.period)
            self._sum = 0.0
            self._sumsq = 0.0
            self._nan_count = 0
            self._current = (_NAN, _NAN, _NAN)

    @property
    def is_ready(self) -> bool:
        return self.count >= self.period

    def update(self, value: float) -> tuple[float, float, float]:
        v = float(value)
        with self._lock:
            if len(self._values) == self.period:
                old = self._values[0]
                if _is_nan(old):
                    self._nan_count -= 1
                else:
                    self._sum -= old
                    self._sumsq -= old * old

            self._values.append(v)
            self.count += 1

            if _is_nan(v):
                self._nan_count += 1
            else:
                self._sum += v
                self._sumsq += v * v

            if len(self._values) < self.period or self._nan_count > 0:
                self._current = (_NAN, _NAN, _NAN)
                return self._current

            mean = self._sum / self.period
            var = max(0.0, (self._sumsq / self.period) - (mean * mean))
            std = math.sqrt(var)
            upper = mean + self.std_dev * std
            lower = mean - self.std_dev * std
            self._current = (upper, mean, lower)
            return self._current

    def status(self) -> dict[str, Any]:
        upper, middle, lower = self._current
        return {
            "count": self.count,
            "is_ready": self.is_ready,
            "upper": upper,
            "middle": middle,
            "lower": lower,
        }


class IncrementalStochastic:
    def __init__(self, k_period: int = 14, d_period: int = 3) -> None:
        if k_period <= 0 or d_period <= 0:
            raise ValueError("k_period/d_period must be > 0")
        self.k_period = int(k_period)
        self.d_period = int(d_period)
        self._lock = threading.Lock()
        self.reset()

    def reset(self) -> None:
        with self._lock:
            self.count = 0
            self._high: deque[float] = deque(maxlen=self.k_period)
            self._low: deque[float] = deque(maxlen=self.k_period)
            self._k_values: deque[float] = deque(maxlen=self.d_period)
            self._current = (_NAN, _NAN)

    @property
    def is_ready(self) -> bool:
        return self.count >= (self.k_period + self.d_period - 1)

    def update(self, high: float, low: float, close: float) -> tuple[float, float]:
        h = float(high)
        l = float(low)
        c = float(close)
        with self._lock:
            self.count += 1
            self._high.append(h)
            self._low.append(l)

            if len(self._high) < self.k_period or len(self._low) < self.k_period:
                self._current = (_NAN, _NAN)
                return self._current

            highest = max(self._high)
            lowest = min(self._low)
            if highest == lowest:
                k = 0.0
            else:
                k = (c - lowest) / (highest - lowest) * 100.0
                k = _clamp(k, 0.0, 100.0)

            self._k_values.append(k)
            if len(self._k_values) < self.d_period:
                self._current = (k, _NAN)
                return self._current

            d = sum(self._k_values) / self.d_period
            self._current = (k, d)
            return self._current

    def status(self) -> dict[str, Any]:
        k, d = self._current
        return {"count": self.count, "is_ready": self.is_ready, "k": k, "d": d}


class CCXTStreamProcessor:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._indicators: dict[str, Any] = {}

    def add_indicator(self, name: str, indicator: Any) -> None:
        with self._lock:
            self._indicators[name] = indicator

    def remove_indicator(self, name: str) -> None:
        with self._lock:
            self._indicators.pop(name, None)

    def reset_all(self) -> None:
        with self._lock:
            for ind in self._indicators.values():
                if hasattr(ind, "reset"):
                    ind.reset()

    def get_status(self) -> dict[str, dict[str, Any]]:
        with self._lock:
            status: dict[str, dict[str, Any]] = {}
            for name, ind in self._indicators.items():
                if hasattr(ind, "status"):
                    status[name] = ind.status()
                else:
                    status[name] = {"count": getattr(ind, "count", None)}
            return status

    def process_candle(self, candle: Iterable[float]) -> dict[str, Any]:
        data = list(candle)
        if len(data) == 6:
            _ts, open_, high, low, close, volume = data
        elif len(data) == 5:
            open_, high, low, close, volume = data
        else:
            raise ValueError("candle must be length 5 or 6")

        results: dict[str, Any] = {}
        with self._lock:
            for name, ind in self._indicators.items():
                if isinstance(ind, (IncrementalATR, IncrementalSuperTrend, IncrementalStochastic)):
                    out = ind.update(high, low, close)
                else:
                    out = ind.update(close)

                results[name] = out
        return results


def get_available_streaming_indicators() -> list[str]:
    return [
        "IncrementalSMA",
        "IncrementalEMA",
        "IncrementalRSI",
        "IncrementalMACD",
        "IncrementalATR",
        "IncrementalSuperTrend",
        "IncrementalBollingerBands",
        "IncrementalStochastic",
        "IncrementalAdaptiveRSI",
        "IncrementalEnsembleSignal",
        "IncrementalMLSuperTrend",
    ]


def create_indicator(name: str, /, **kwargs: Any) -> Any:
    key = name.strip().lower()
    aliases: dict[str, Any] = {
        "sma": IncrementalSMA,
        "ema": IncrementalEMA,
        "rsi": IncrementalRSI,
        "macd": IncrementalMACD,
        "atr": IncrementalATR,
        "supertrend": IncrementalSuperTrend,
        "stochastic": IncrementalStochastic,
        "stoch": IncrementalStochastic,
        "bb": IncrementalBollingerBands,
        "bollinger": IncrementalBollingerBands,
        "bollinger_bands": IncrementalBollingerBands,
    }
    cls = aliases.get(key)
    if cls is None:
        raise ValueError(f"Unknown indicator: {name}")
    return cls(**kwargs)


class IncrementalAdaptiveRSI:
    def __init__(
        self,
        *,
        base_period: int = 14,
        min_period: int = 7,
        max_period: int = 28,
        volatility_window: int = 14,
    ) -> None:
        if base_period <= 0 or min_period <= 0 or max_period <= 0:
            raise ValueError("periods must be > 0")
        if min_period > max_period:
            raise ValueError("min_period must be <= max_period")
        if volatility_window <= 0:
            raise ValueError("volatility_window must be > 0")

        self.base_period = int(base_period)
        self.min_period = int(min_period)
        self.max_period = int(max_period)
        self.volatility_window = int(volatility_window)

        self._lock = threading.Lock()
        self._rsi = IncrementalRSI(period=self.base_period)
        self.reset()

    def reset(self) -> None:
        with self._lock:
            self.count = 0
            self._prices: list[float] = []
            self._returns: deque[float] = deque(maxlen=self.volatility_window)
            self._max_vol = 0.0
            self._rsi.reset()
            self._is_ready = False

    @property
    def is_ready(self) -> bool:
        return self._is_ready

    def update(self, price: float) -> tuple[float, int]:
        p = float(price)
        with self._lock:
            self.count += 1
            if self._prices:
                prev = self._prices[-1]
                if prev != 0.0 and not _is_nan(prev) and not _is_nan(p):
                    self._returns.append((p - prev) / prev)
                else:
                    self._returns.append(0.0)
            self._prices.append(p)

            if len(self._returns) >= 2:
                mean = sum(self._returns) / len(self._returns)
                var = sum((r - mean) ** 2 for r in self._returns) / len(self._returns)
                vol = math.sqrt(max(0.0, var))
            else:
                vol = 0.0

            self._max_vol = max(self._max_vol, vol)
            if self._max_vol == 0.0:
                period = self.base_period
            else:
                norm = vol / (self._max_vol + 1e-12)
                period = int(round(self.max_period - norm * (self.max_period - self.min_period)))
            period = int(_clamp(period, self.min_period, self.max_period))

            rsi = self._rsi.update(p)
            if not self._is_ready and not _is_nan(rsi):
                self._is_ready = True
            return rsi, period


class IncrementalEnsembleSignal:
    def __init__(self, *, weights: Mapping[str, float] | None = None) -> None:
        self._lock = threading.Lock()
        self._rsi = IncrementalRSI(period=14)
        self._macd = IncrementalMACD(fast=5, slow=10, signal=3)
        self._stoch = IncrementalStochastic(k_period=7, d_period=3)
        self._supertrend = IncrementalSuperTrend(period=7, multiplier=3.0)
        self.weights = dict(weights or {})
        self.reset()

    def reset(self) -> None:
        with self._lock:
            self.count = 0
            self._rsi.reset()
            self._macd.reset()
            self._stoch.reset()
            self._supertrend.reset()

    @property
    def is_ready(self) -> bool:
        return (
            self._rsi.is_ready
            and self._macd.is_ready
            and self._stoch.is_ready
            and self._supertrend.is_ready
        )

    def update(self, high: float, low: float, close: float) -> tuple[float, Dict[str, float]]:
        with self._lock:
            self.count += 1
            rsi_val = self._rsi.update(close)
            macd_line, macd_sig, macd_hist = self._macd.update(close)
            k, d = self._stoch.update(high, low, close)
            st_val, st_dir = self._supertrend.update(high, low, close)

            rsi_signal = 0.0 if _is_nan(rsi_val) else _clamp((rsi_val - 50.0) / 50.0, -1.0, 1.0)
            macd_signal = 0.0 if _is_nan(macd_hist) else float(math.tanh(macd_hist))
            stoch_signal = 0.0 if _is_nan(k) else _clamp((k - 50.0) / 50.0, -1.0, 1.0)
            supertrend_signal = 0.0 if _is_nan(st_dir) else (1.0 if st_dir > 0 else -1.0)

            components = {
                "rsi": rsi_signal,
                "macd": macd_signal,
                "stochastic": stoch_signal,
                "supertrend": supertrend_signal,
            }

            if self.weights:
                signal = sum(float(self.weights.get(k, 0.0)) * float(v) for k, v in components.items())
            else:
                signal = sum(components.values()) / len(components)

            return _clamp(signal, -1.0, 1.0), components


class IncrementalMLSuperTrend:
    def __init__(
        self,
        *,
        period: int = 10,
        multiplier: float = 3.0,
        confirmation_bars: int = 2,
        use_atr_filter: bool = True,
    ) -> None:
        if period <= 0:
            raise ValueError("period must be > 0")
        if confirmation_bars <= 0:
            raise ValueError("confirmation_bars must be > 0")

        self.period = int(period)
        self.multiplier = float(multiplier)
        self.confirmation_bars = int(confirmation_bars)
        self.use_atr_filter = bool(use_atr_filter)

        self._lock = threading.Lock()
        self._supertrend = IncrementalSuperTrend(period=self.period, multiplier=self.multiplier)
        self._atr = IncrementalATR(period=self.period)
        self.reset()

    def reset(self) -> None:
        with self._lock:
            self.count = 0
            self._supertrend.reset()
            self._atr.reset()
            self._dir_window: deque[float] = deque(maxlen=self.confirmation_bars)
            self.current_direction = _NAN

    @property
    def is_ready(self) -> bool:
        return self._supertrend.is_ready and self._atr.is_ready

    def update(self, high: float, low: float, close: float) -> tuple[float, float, float]:
        with self._lock:
            self.count += 1
            atr = self._atr.update(high, low, close)
            trend, direction = self._supertrend.update(high, low, close)

            if not _is_nan(direction):
                self._dir_window.append(direction)
                if len(self._dir_window) == self.confirmation_bars and all(
                    d == self._dir_window[0] for d in self._dir_window
                ):
                    self.current_direction = self._dir_window[0]

            if _is_nan(atr) or _is_nan(close) or close == 0.0:
                confidence = _NAN
            else:
                atr_pct = abs(atr / close)
                confidence = _clamp(1.0 - atr_pct * 5.0, 0.0, 1.0) if self.use_atr_filter else 1.0

            return trend, self.current_direction, confidence
