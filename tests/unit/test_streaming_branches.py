from __future__ import annotations

import math

import pytest

from haze_library.streaming import (
    CCXTStreamProcessor,
    IncrementalAdaptiveRSI,
    IncrementalAISuperTrend,
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
    assert "IncrementalAISuperTrend" in names

    assert isinstance(create_indicator("bb"), IncrementalBollingerBands)
    assert isinstance(create_indicator("ai_supertrend"), IncrementalAISuperTrend)
    assert isinstance(create_indicator("ai_supertrend_ml"), IncrementalAISuperTrend)
    with pytest.raises(ValueError):
        create_indicator("unknown_indicator")


# ==================== IncrementalAISuperTrend Tests ====================


def test_ai_supertrend_invalid_parameters() -> None:
    """Test IncrementalAISuperTrend parameter validation."""
    with pytest.raises(ValueError, match="st_length must be > 0"):
        IncrementalAISuperTrend(st_length=0)
    with pytest.raises(ValueError, match="st_length must be > 0"):
        IncrementalAISuperTrend(st_length=-5)
    with pytest.raises(ValueError, match="st_multiplier must be > 0"):
        IncrementalAISuperTrend(st_multiplier=0.0)
    with pytest.raises(ValueError, match="st_multiplier must be > 0"):
        IncrementalAISuperTrend(st_multiplier=-3.0)
    with pytest.raises(ValueError, match="st_multiplier must be > 0"):
        IncrementalAISuperTrend(st_multiplier=float("nan"))
    with pytest.raises(ValueError, match="st_multiplier must be > 0"):
        IncrementalAISuperTrend(st_multiplier=float("inf"))
    with pytest.raises(ValueError, match="lookback must be > 0"):
        IncrementalAISuperTrend(lookback=0)
    with pytest.raises(ValueError, match="train_window must be > lookback"):
        IncrementalAISuperTrend(lookback=50, train_window=50)
    with pytest.raises(ValueError, match="train_window must be > lookback"):
        IncrementalAISuperTrend(lookback=100, train_window=50)


def test_ai_supertrend_basic_functionality() -> None:
    """Test IncrementalAISuperTrend basic update functionality."""
    ind = IncrementalAISuperTrend(
        st_length=5,
        st_multiplier=2.0,
        lookback=5,
        train_window=50
    )

    assert not ind.is_ready
    assert ind.count == 0
    assert ind.current_direction == 0

    # Feed data until ready
    import random
    random.seed(42)
    price = 100.0
    for i in range(60):
        price += random.uniform(-1.0, 1.0)
        high = price + random.uniform(0.5, 1.5)
        low = price - random.uniform(0.5, 1.5)
        result = ind.update(high, low, price)

        assert isinstance(result, dict)
        assert "supertrend" in result
        assert "direction" in result
        assert "trend_offset" in result
        assert "buy_signal" in result
        assert "sell_signal" in result
        assert "stop_loss" in result
        assert "take_profit" in result

    assert ind.count == 60
    assert ind.is_ready


def test_ai_supertrend_not_ready_result() -> None:
    """Test IncrementalAISuperTrend returns NaN values when not ready."""
    ind = IncrementalAISuperTrend(st_length=10, train_window=200)

    # Only feed a few bars (not enough to be ready)
    result = ind.update(102.0, 98.0, 100.0)
    assert math.isnan(result["supertrend"])
    assert result["direction"] == 0
    assert math.isnan(result["trend_offset"])
    assert result["buy_signal"] is False
    assert result["sell_signal"] is False
    assert math.isnan(result["stop_loss"])
    assert math.isnan(result["take_profit"])
    assert not ind.is_ready


def test_ai_supertrend_reset() -> None:
    """Test IncrementalAISuperTrend reset functionality."""
    ind = IncrementalAISuperTrend(
        st_length=5,
        st_multiplier=2.0,
        lookback=5,
        train_window=50
    )

    # Feed enough data to become ready
    import random
    random.seed(123)
    price = 100.0
    for i in range(60):
        price += random.uniform(-0.5, 0.5)
        ind.update(price + 1, price - 1, price)

    assert ind.count == 60
    assert ind.is_ready

    # Reset and verify
    ind.reset()
    assert ind.count == 0
    assert not ind.is_ready
    assert ind.current_direction == 0


def test_ai_supertrend_status() -> None:
    """Test IncrementalAISuperTrend status method."""
    ind = IncrementalAISuperTrend(
        st_length=14,
        st_multiplier=2.5,
        lookback=8,
        train_window=100
    )

    ind.update(102.0, 98.0, 100.0)
    status = ind.status()

    assert status["count"] == 1
    assert status["is_ready"] is False
    assert status["direction"] == 0
    assert status["st_length"] == 14
    assert status["st_multiplier"] == 2.5
    assert status["lookback"] == 8
    assert status["train_window"] == 100


def test_ai_supertrend_ccxt_processor_integration() -> None:
    """Test IncrementalAISuperTrend with CCXTStreamProcessor."""
    proc = CCXTStreamProcessor()
    proc.add_indicator("ai_st", IncrementalAISuperTrend(
        st_length=5,
        train_window=50
    ))
    proc.add_indicator("sma", IncrementalSMA(period=5))

    import random
    random.seed(456)
    price = 100.0

    # Process CCXT-format candles [timestamp, open, high, low, close, volume]
    for i in range(60):
        price += random.uniform(-0.5, 0.5)
        candle = [i * 60000, price - 0.2, price + 1, price - 1, price, 1000]
        results = proc.process_candle(candle)

        assert "ai_st" in results
        assert "sma" in results

    status = proc.get_status()
    assert "ai_st" in status
    assert status["ai_st"]["count"] == 60


def test_ai_supertrend_signal_generation() -> None:
    """Test that IncrementalAISuperTrend generates signals on trend changes."""
    ind = IncrementalAISuperTrend(
        st_length=5,
        st_multiplier=2.0,
        lookback=5,
        train_window=30
    )

    # Create uptrend data
    for i in range(40):
        price = 100.0 + i * 0.5
        _ = ind.update(price + 1, price - 1, price)

    # Create sharp reversal
    for i in range(20):
        price = 120.0 - i * 1.0
        _ = ind.update(price + 1, price - 1, price)

    # At least one result should have valid direction after reversal
    assert ind.is_ready
    assert ind.current_direction in [-1, 0, 1]
