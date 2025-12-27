from __future__ import annotations

import math

import pytest

from haze_library.streaming import (
    CCXTStreamProcessor,
    IncrementalAdaptiveRSI,
    IncrementalATR,
    IncrementalBollingerBands,
    IncrementalEMA,
    IncrementalEnsembleSignal,
    IncrementalMACD,
    IncrementalMLSuperTrend,
    IncrementalSMA,
    IncrementalStochastic,
    IncrementalSuperTrend,
    create_indicator,
    get_available_streaming_indicators,
)


def test_incremental_sma_nan_window() -> None:
    sma = IncrementalSMA(period=2)
    with pytest.raises(ValueError):
        sma.update(float("nan"))
    sma.update(1.0)
    result = sma.update(1.0)
    assert not math.isnan(result)
    assert sma.value == result


def test_invalid_parameter_checks() -> None:
    with pytest.raises(ValueError):
        IncrementalEMA(period=0)
    with pytest.raises(ValueError):
        IncrementalMACD(fast=0, slow=26, signal=9)
    with pytest.raises(ValueError):
        IncrementalMACD(fast=12, slow=12, signal=9)
    with pytest.raises(ValueError):
        IncrementalATR(period=0)
    with pytest.raises(ValueError):
        IncrementalSuperTrend(period=0)
    with pytest.raises(ValueError):
        IncrementalBollingerBands(period=0)
    with pytest.raises(ValueError):
        IncrementalStochastic(k_period=0, d_period=3)
    with pytest.raises(ValueError):
        IncrementalStochastic(k_period=3, smooth_k=0, d_period=3)
    with pytest.raises(ValueError):
        IncrementalAdaptiveRSI(min_period=0)
    with pytest.raises(ValueError):
        IncrementalAdaptiveRSI(volatility_window=0)
    with pytest.raises(ValueError):
        IncrementalAdaptiveRSI(min_period=10, max_period=5)
    with pytest.raises(ValueError):
        IncrementalAdaptiveRSI(base_period=0)
    with pytest.raises(ValueError):
        IncrementalAdaptiveRSI(base_period=30, min_period=7, max_period=21)
    with pytest.raises(ValueError):
        IncrementalMLSuperTrend(period=0)
    with pytest.raises(ValueError):
        IncrementalMLSuperTrend(multiplier=0.0)
    with pytest.raises(ValueError):
        IncrementalMLSuperTrend(confirmation_bars=0)


def test_status_methods() -> None:
    macd = IncrementalMACD()
    macd.update(1.0)
    assert "macd" in macd.status()

    atr = IncrementalATR()
    atr.update(1.0, 0.5, 0.8)
    assert "current" in atr.status()

    st = IncrementalSuperTrend()
    st.update(1.0, 0.5, 0.8)
    assert "trend" in st.status()

    bb = IncrementalBollingerBands()
    bb.update(1.0)
    assert "upper" in bb.status()
    bb.reset()
    assert bb.status()["count"] == 0

    stoch = IncrementalStochastic()
    stoch.update(1.0, 0.5, 0.8)
    assert "k" in stoch.status()


def test_ensemble_signal_branches() -> None:
    ensemble = IncrementalEnsembleSignal()
    _ = ensemble.update(1.0, 0.5, 0.8)

    class DummyResult:
        signal = 0.7
        rsi_contrib = 0.2
        macd_contrib = 0.1
        stoch_contrib = 0.3
        trend_contrib = 0.4

    class DummyInner:
        def update(self, h, l, c):
            return DummyResult()

        def reset(self):
            return None

    ensemble_plain = IncrementalEnsembleSignal()
    ensemble_plain._inner = DummyInner()
    signal, _components = ensemble_plain.update(1.0, 0.5, 0.8)
    assert signal == pytest.approx(DummyResult.signal)

    ensemble_weighted = IncrementalEnsembleSignal(weights={"rsi": 1.0})
    ensemble_weighted._inner = DummyInner()
    signal, components = ensemble_weighted.update(1.0, 0.5, 0.8)
    assert signal == pytest.approx(components["rsi"])


def test_ml_supertrend_branches() -> None:
    class DummyResultZero:
        value = 1.0
        confirmed_trend = 0.0
        confidence = 0.5

    class DummyResultUp:
        value = 1.0
        confirmed_trend = 1.0
        confidence = 0.6

    class DummyInner:
        def __init__(self, result):
            self._result = result

        def update(self, h, l, c):
            return self._result

        def reset(self):
            return None

    ml = IncrementalMLSuperTrend()
    ml._inner = DummyInner(DummyResultZero())
    _value, direction, _confidence = ml.update(1.0, 0.5, 0.8)
    assert math.isnan(direction)

    ml._inner = DummyInner(DummyResultUp())
    _value, direction, _confidence = ml.update(1.0, 0.5, 0.8)
    assert direction == 1.0

    ml._inner = DummyInner(None)
    _value, direction, _confidence = ml.update(1.0, 0.5, 0.8)
    assert math.isnan(direction)


def test_stream_processor_and_factory() -> None:
    proc = CCXTStreamProcessor()

    class DummyIndicator:
        def __init__(self):
            self.count = 0

        def update(self, value):
            self.count += 1
            return value

        def reset(self):
            self.count = 0

    class StatusIndicator(DummyIndicator):
        def status(self):
            return {"count": self.count}

    proc.add_indicator("dummy", DummyIndicator())
    proc.add_indicator("status", StatusIndicator())
    proc.add_indicator("sma", IncrementalSMA(period=2))
    proc.add_indicator("atr", IncrementalATR())

    out = proc.process_candle([1.0, 2.0, 3.0, 4.0, 5.0])
    assert "dummy" in out

    out = proc.process_candle([0.0, 1.0, 2.0, 3.0, 4.0, 5.0])
    assert "status" in out

    with pytest.raises(ValueError):
        proc.process_candle([1.0, 2.0])

    status = proc.get_status()
    assert "dummy" in status

    proc.reset_all()
    proc.remove_indicator("dummy")

    names = get_available_streaming_indicators()
    assert "IncrementalSMA" in names

    assert isinstance(create_indicator("bb"), IncrementalBollingerBands)
    with pytest.raises(ValueError):
        create_indicator("unknown_indicator")
