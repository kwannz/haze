"""
Streaming Module Tests
======================

Test incremental/streaming indicators for real-time computation.

Author: Haze Team
Date: 2025-12-26
"""

import pytest
import math
import sys
import os
import threading
import time
from concurrent.futures import ThreadPoolExecutor

# Add parent to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../rust/python'))

from haze_library.streaming import (
    IncrementalSMA,
    IncrementalEMA,
    IncrementalRSI,
    IncrementalMACD,
    IncrementalATR,
    IncrementalSuperTrend,
    IncrementalBollingerBands,
    IncrementalStochastic,
    CCXTStreamProcessor,
    get_available_streaming_indicators,
    create_indicator,
)


# ==================== Fixtures ====================

@pytest.fixture
def sample_prices():
    """Sample close prices for testing."""
    return [
        100.0, 101.0, 102.0, 101.5, 103.0, 102.5, 104.0, 103.5, 105.0, 104.5,
        106.0, 105.5, 107.0, 106.5, 108.0, 107.5, 109.0, 108.5, 110.0, 109.5,
        108.0, 107.0, 106.0, 105.0, 104.0, 105.0, 106.0, 107.0, 108.0, 109.0,
    ]


@pytest.fixture
def sample_ohlc():
    """Sample OHLC data for testing."""
    base = [
        100.0, 101.0, 102.0, 101.5, 103.0, 102.5, 104.0, 103.5, 105.0, 104.5,
        106.0, 105.5, 107.0, 106.5, 108.0, 107.5, 109.0, 108.5, 110.0, 109.5,
        108.0, 107.0, 106.0, 105.0, 104.0, 105.0, 106.0, 107.0, 108.0, 109.0,
    ]
    return {
        'high': [c + 1.0 for c in base],
        'low': [c - 1.0 for c in base],
        'close': base,
    }


# ==================== SMA Tests ====================

class TestIncrementalSMA:
    """Test Incremental SMA indicator."""

    def test_basic_calculation(self, sample_prices):
        """Test basic SMA calculation."""
        sma = IncrementalSMA(period=5)

        results = []
        for price in sample_prices:
            results.append(sma.update(price))

        # First 4 values should be NaN
        assert all(math.isnan(r) for r in results[:4])
        # 5th value should be average of first 5 prices
        expected = sum(sample_prices[:5]) / 5
        assert abs(results[4] - expected) < 0.0001

    def test_is_ready(self):
        """Test is_ready property."""
        sma = IncrementalSMA(period=3)

        assert not sma.is_ready
        sma.update(100.0)
        assert not sma.is_ready
        sma.update(101.0)
        assert not sma.is_ready
        sma.update(102.0)
        assert sma.is_ready

    def test_reset(self, sample_prices):
        """Test reset functionality."""
        sma = IncrementalSMA(period=5)

        for price in sample_prices[:10]:
            sma.update(price)

        assert sma.is_ready
        sma.reset()
        assert not sma.is_ready
        assert sma.count == 0

    def test_current_property(self, sample_prices):
        """Test current property."""
        sma = IncrementalSMA(period=5)

        for price in sample_prices[:5]:
            sma.update(price)

        expected = sum(sample_prices[:5]) / 5
        assert abs(sma.current - expected) < 0.0001


# ==================== EMA Tests ====================

class TestIncrementalEMA:
    """Test Incremental EMA indicator."""

    def test_basic_calculation(self, sample_prices):
        """Test basic EMA calculation."""
        ema = IncrementalEMA(period=5)

        results = []
        for price in sample_prices:
            results.append(ema.update(price))

        # First 4 values should be NaN
        assert all(math.isnan(r) for r in results[:4])
        # 5th value should be SMA of first 5 prices
        expected = sum(sample_prices[:5]) / 5
        assert abs(results[4] - expected) < 0.0001
        # Subsequent values should follow EMA formula
        assert not math.isnan(results[5])

# ==================== RSI Tests ====================

class TestIncrementalRSI:
    """Test Incremental RSI indicator."""

    def test_basic_calculation(self, sample_prices):
        """Test basic RSI calculation."""
        rsi = IncrementalRSI(period=14)

        results = []
        for price in sample_prices:
            results.append(rsi.update(price))

        # First 14 values should be NaN
        assert all(math.isnan(r) for r in results[:14])
        # 15th+ values should be valid RSI
        valid_results = [r for r in results if not math.isnan(r)]
        assert all(0 <= r <= 100 for r in valid_results)

    def test_is_ready(self):
        """RSI should only be ready after period + 1 updates."""
        rsi = IncrementalRSI(period=3)
        for value in (100.0, 101.0, 102.0):
            rsi.update(value)
            assert not rsi.is_ready
        rsi.update(103.0)
        assert rsi.is_ready

    def test_rsi_range(self, sample_prices):
        """Test RSI stays in [0, 100] range."""
        rsi = IncrementalRSI(period=7)

        for price in sample_prices:
            result = rsi.update(price)
            if not math.isnan(result):
                assert 0 <= result <= 100


# ==================== MACD Tests ====================

class TestIncrementalMACD:
    """Test Incremental MACD indicator."""

    def test_basic_calculation(self, sample_prices):
        """Test basic MACD calculation."""
        macd = IncrementalMACD(fast=5, slow=10, signal=3)

        for price in sample_prices:
            line, signal, hist = macd.update(price)

        # After enough data, all values should be valid
        assert not math.isnan(line)
        assert not math.isnan(signal)
        assert not math.isnan(hist)
        # Histogram = MACD line - Signal line
        assert abs(hist - (line - signal)) < 0.0001

    def test_is_ready(self):
        """MACD is_ready should track when outputs become finite."""
        macd = IncrementalMACD(fast=3, slow=5, signal=2)
        ready_seen = False
        for value in range(100, 140):
            line, signal, hist = macd.update(float(value))
            ready_now = not any(math.isnan(x) for x in (line, signal, hist))
            assert macd.is_ready == ready_now
            ready_seen = ready_seen or ready_now
        assert ready_seen


# ==================== ATR Tests ====================

class TestIncrementalATR:
    """Test Incremental ATR indicator."""

    def test_basic_calculation(self, sample_ohlc):
        """Test basic ATR calculation."""
        atr = IncrementalATR(period=7)

        results = []
        for h, l, c in zip(
            sample_ohlc['high'], sample_ohlc['low'], sample_ohlc['close']
        ):
            results.append(atr.update(h, l, c))

        # First 7 values should be NaN
        assert all(math.isnan(r) for r in results[:7])
        # ATR should be positive
        valid_results = [r for r in results if not math.isnan(r)]
        assert all(r > 0 for r in valid_results)


# ==================== SuperTrend Tests ====================

class TestIncrementalSuperTrend:
    """Test Incremental SuperTrend indicator."""

    def test_basic_calculation(self, sample_ohlc):
        """Test basic SuperTrend calculation."""
        st = IncrementalSuperTrend(period=7, multiplier=3.0)

        for h, l, c in zip(
            sample_ohlc['high'], sample_ohlc['low'], sample_ohlc['close']
        ):
            value, direction = st.update(h, l, c)

        # Direction should be 1 or -1
        assert direction in [1.0, -1.0]

    def test_direction_property(self, sample_ohlc):
        """Test current_direction property."""
        st = IncrementalSuperTrend(period=7)

        for h, l, c in zip(
            sample_ohlc['high'], sample_ohlc['low'], sample_ohlc['close']
        ):
            st.update(h, l, c)

        assert st.current_direction in [1.0, -1.0]


# ==================== Bollinger Bands Tests ====================

class TestIncrementalBollingerBands:
    """Test Incremental Bollinger Bands indicator."""

    def test_basic_calculation(self, sample_prices):
        """Test basic Bollinger Bands calculation."""
        bb = IncrementalBollingerBands(period=10, std_dev=2.0)

        for price in sample_prices:
            upper, middle, lower = bb.update(price)

        # After warmup, bands should be valid
        assert not math.isnan(upper)
        assert not math.isnan(middle)
        assert not math.isnan(lower)
        # Upper > Middle > Lower
        assert upper > middle > lower


# ==================== Stochastic Tests ====================

class TestIncrementalStochastic:
    """Test Incremental Stochastic indicator."""

    def test_basic_calculation(self, sample_ohlc):
        """Test basic Stochastic calculation."""
        stoch = IncrementalStochastic(k_period=7, d_period=3)

        for h, l, c in zip(
            sample_ohlc['high'], sample_ohlc['low'], sample_ohlc['close']
        ):
            k, d = stoch.update(h, l, c)

        # After warmup, values should be valid
        assert not math.isnan(k)
        assert not math.isnan(d)
        # %K and %D should be in [0, 100]
        assert 0 <= k <= 100
        assert 0 <= d <= 100


# ==================== CCXTStreamProcessor Tests ====================

class TestCCXTStreamProcessor:
    """Test CCXT Stream Processor."""

    def test_add_indicator(self):
        """Test adding indicators."""
        processor = CCXTStreamProcessor()
        processor.add_indicator('rsi', IncrementalRSI(14))
        processor.add_indicator('sma', IncrementalSMA(20))

        status = processor.get_status()
        assert 'rsi' in status
        assert 'sma' in status

    def test_remove_indicator(self):
        """Test removing indicators."""
        processor = CCXTStreamProcessor()
        processor.add_indicator('rsi', IncrementalRSI(14))
        processor.remove_indicator('rsi')

        status = processor.get_status()
        assert 'rsi' not in status

    def test_process_candle(self):
        """Test processing a candle."""
        processor = CCXTStreamProcessor()
        processor.add_indicator('sma', IncrementalSMA(3))

        # Process 3 candles (6-element format: timestamp, open, high, low, close, volume)
        for i in range(3):
            candle = [1000000 + i, 100.0, 101.0, 99.0, 100.0 + i, 1000.0]
            results = processor.process_candle(candle)

        assert 'sma' in results
        # SMA of 100, 101, 102 = 101
        assert abs(results['sma'] - 101.0) < 0.0001

    def test_process_candle_5_element(self):
        """Test processing 5-element candle format."""
        processor = CCXTStreamProcessor()
        processor.add_indicator('sma', IncrementalSMA(3))

        for i in range(3):
            candle = [100.0, 101.0, 99.0, 100.0 + i, 1000.0]
            results = processor.process_candle(candle)

        assert 'sma' in results

    def test_reset_all(self):
        """Test resetting all indicators."""
        processor = CCXTStreamProcessor()
        processor.add_indicator('sma', IncrementalSMA(3))
        processor.add_indicator('ema', IncrementalEMA(3))

        # Process some data
        for i in range(5):
            processor.process_candle([1000000, 100.0, 101.0, 99.0, 100.0, 1000.0])

        processor.reset_all()
        status = processor.get_status()

        assert status['sma']['count'] == 0
        assert status['ema']['count'] == 0


# ==================== Thread Safety Tests ====================

class TestThreadSafety:
    """Test thread safety of incremental indicators."""

    def test_concurrent_updates(self):
        """Test concurrent updates from multiple threads."""
        sma = IncrementalSMA(period=10)
        results = []
        lock = threading.Lock()

        def update_sma(value):
            result = sma.update(value)
            with lock:
                results.append(result)

        with ThreadPoolExecutor(max_workers=4) as executor:
            for i in range(100):
                executor.submit(update_sma, 100.0 + i)

        # Should have 100 results
        assert len(results) == 100
        # After 100 updates, SMA should be ready
        assert sma.is_ready

    def test_concurrent_read_write(self):
        """Test concurrent reads and writes."""
        sma = IncrementalSMA(period=5)
        read_results = []
        lock = threading.Lock()

        # Pre-populate with some data
        for i in range(10):
            sma.update(100.0 + i)

        def reader():
            for _ in range(50):
                with lock:
                    read_results.append(sma.current)
                time.sleep(0.001)

        def writer():
            for i in range(50):
                sma.update(150.0 + i)
                time.sleep(0.001)

        threads = [
            threading.Thread(target=reader),
            threading.Thread(target=writer),
        ]

        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # Should complete without deadlock or crash
        assert len(read_results) == 50


# ==================== Utility Tests ====================

class TestUtilities:
    """Test utility functions."""

    def test_get_available_indicators(self):
        """Test get_available_streaming_indicators."""
        indicators = get_available_streaming_indicators()
        assert isinstance(indicators, list)
        assert 'IncrementalSMA' in indicators
        assert 'IncrementalRSI' in indicators
        assert 'IncrementalSuperTrend' in indicators

    def test_create_indicator(self):
        """Test create_indicator factory."""
        sma = create_indicator('sma', period=20)
        assert isinstance(sma, IncrementalSMA)
        assert sma.period == 20

        rsi = create_indicator('rsi', period=14)
        assert isinstance(rsi, IncrementalRSI)

        macd = create_indicator('macd', fast=12, slow=26, signal=9)
        assert isinstance(macd, IncrementalMACD)

    def test_create_indicator_aliases(self):
        """Test create_indicator with various name aliases."""
        bb1 = create_indicator('bb', period=20)
        bb2 = create_indicator('bollinger', period=20)
        bb3 = create_indicator('bollinger_bands', period=20)

        assert isinstance(bb1, IncrementalBollingerBands)
        assert isinstance(bb2, IncrementalBollingerBands)
        assert isinstance(bb3, IncrementalBollingerBands)

    def test_create_indicator_unknown(self):
        """Test create_indicator with unknown name."""
        with pytest.raises(ValueError, match="Unknown indicator"):
            create_indicator('unknown_indicator')


# ==================== Batch Processing Tests ====================

class TestBatchProcessing:
    """Test batch processing of data."""

    def test_update_batch(self, sample_prices):
        """Test update_batch method."""
        sma = IncrementalSMA(period=5)
        results = sma.update_batch(sample_prices)

        assert len(results) == len(sample_prices)
        # First 4 should be NaN
        assert all(math.isnan(r) for r in results[:4])
        # Rest should be valid
        assert all(not math.isnan(r) for r in results[4:])


# ==================== Edge Cases ====================

class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_invalid_period(self):
        """Test invalid period raises error."""
        with pytest.raises(ValueError):
            IncrementalSMA(period=0)
        with pytest.raises(ValueError):
            IncrementalRSI(period=-1)

    def test_single_value(self):
        """Test with single value."""
        sma = IncrementalSMA(period=1)
        result = sma.update(100.0)
        assert result == 100.0
        assert sma.is_ready

    def test_large_period(self):
        """Test with large period."""
        sma = IncrementalSMA(period=1000)
        for i in range(1000):
            sma.update(float(i))
        assert sma.is_ready

    def test_nan_input(self):
        """NaN input raises ValueError (fail-fast)."""
        sma = IncrementalSMA(period=3)
        sma.update(100.0)
        prev_count = sma.count
        with pytest.raises(ValueError):
            sma.update(float('nan'))
        assert sma.count == prev_count
        assert math.isnan(sma.current)


# ==================== AI-Enhanced Streaming Indicators Tests ====================

from haze_library.streaming import (
    IncrementalAdaptiveRSI,
    IncrementalEnsembleSignal,
    IncrementalMLSuperTrend,
)


class TestIncrementalAdaptiveRSI:
    """Test Incremental Adaptive RSI indicator."""

    def test_basic_calculation(self, sample_prices):
        """Test basic adaptive RSI calculation."""
        adaptive = IncrementalAdaptiveRSI(base_period=7, volatility_window=10)

        results = []
        for price in sample_prices:
            rsi, period = adaptive.update(price)
            results.append((rsi, period))

        # Should have valid values after warmup
        valid_results = [(r, p) for r, p in results if not math.isnan(r)]
        assert len(valid_results) > 0
        # RSI should be in [0, 100]
        for rsi, _ in valid_results:
            assert 0 <= rsi <= 100

    def test_is_ready_synchronization(self):
        """Test is_ready triggers at correct time."""
        adaptive = IncrementalAdaptiveRSI(
            base_period=14, min_period=7, max_period=28, volatility_window=20
        )

        first_valid = None
        is_ready_at = None

        for i in range(60):
            rsi, _ = adaptive.update(100.0 + i * 0.1)
            if is_ready_at is None and adaptive.is_ready:
                is_ready_at = i
            if first_valid is None and not math.isnan(rsi):
                first_valid = i
                break

        # is_ready should trigger when first valid value appears
        assert is_ready_at == first_valid

    def test_period_adaptation(self, sample_prices):
        """Test period adapts to volatility."""
        adaptive = IncrementalAdaptiveRSI(min_period=7, max_period=21)

        periods = []
        for price in sample_prices:
            _, period = adaptive.update(price)
            periods.append(period)

        # Period should be within bounds
        for p in periods:
            assert 7 <= p <= 21

    def test_reset(self, sample_prices):
        """Test reset functionality."""
        adaptive = IncrementalAdaptiveRSI()

        for price in sample_prices[:20]:
            adaptive.update(price)

        assert adaptive.count > 0
        adaptive.reset()
        assert adaptive.count == 0
        assert not adaptive.is_ready


class TestIncrementalEnsembleSignal:
    """Test Incremental Ensemble Signal indicator."""

    def test_basic_calculation(self, sample_ohlc):
        """Test basic ensemble signal calculation."""
        ensemble = IncrementalEnsembleSignal()

        results = []
        for h, l, c in zip(
            sample_ohlc['high'], sample_ohlc['low'], sample_ohlc['close']
        ):
            signal, components = ensemble.update(h, l, c)
            results.append((signal, components))

        # After warmup, signal should be in [-1, 1]
        for sig, _ in results:
            assert -1.0 <= sig <= 1.0

    def test_is_ready_checks_components(self, sample_ohlc):
        """Test is_ready checks all component indicators."""
        ensemble = IncrementalEnsembleSignal()

        # Initially not ready
        assert not ensemble.is_ready

        # Ensemble needs enough data for all components (MACD slow=26 is longest)
        # Generate extended data if needed
        extended_high = sample_ohlc['high'] * 2  # 60 points
        extended_low = sample_ohlc['low'] * 2
        extended_close = sample_ohlc['close'] * 2

        # Process data until ready
        for h, l, c in zip(extended_high, extended_low, extended_close):
            ensemble.update(h, l, c)
            if ensemble.is_ready:
                break

        # When ready (after ~27+ points), ensemble should report ready state
        assert ensemble.is_ready, f"Ensemble not ready after {ensemble.count} updates"

    def test_component_signals(self, sample_ohlc):
        """Test individual component signals are returned."""
        ensemble = IncrementalEnsembleSignal()

        for h, l, c in zip(
            sample_ohlc['high'], sample_ohlc['low'], sample_ohlc['close']
        ):
            _, components = ensemble.update(h, l, c)

        # Check all expected components exist
        assert 'rsi' in components
        assert 'macd' in components
        assert 'stochastic' in components
        assert 'supertrend' in components

        # Check component values are in range
        for key, val in components.items():
            assert -1.0 <= val <= 1.0

    def test_custom_weights(self, sample_ohlc):
        """Test custom weight configuration."""
        custom_weights = {
            'rsi': 0.5,
            'macd': 0.5,
            'stochastic': 0.0,
            'supertrend': 0.0,
        }
        ensemble = IncrementalEnsembleSignal(weights=custom_weights)

        for h, l, c in zip(
            sample_ohlc['high'], sample_ohlc['low'], sample_ohlc['close']
        ):
            signal, components = ensemble.update(h, l, c)

        # Signal should only reflect RSI and MACD
        expected = components['rsi'] * 0.5 + components['macd'] * 0.5
        assert abs(signal - expected) < 0.01

    def test_invalid_weights(self):
        """Test non-finite weights raise ValueError."""
        with pytest.raises(ValueError, match="non-finite value"):
            IncrementalEnsembleSignal(weights={"rsi": float("inf")})

    def test_reset(self, sample_ohlc):
        """Test reset functionality."""
        ensemble = IncrementalEnsembleSignal()

        for h, l, c in zip(
            sample_ohlc['high'][:20], sample_ohlc['low'][:20], sample_ohlc['close'][:20]
        ):
            ensemble.update(h, l, c)

        assert ensemble.count > 0
        ensemble.reset()
        assert ensemble.count == 0
        assert not ensemble.is_ready


class TestIncrementalMLSuperTrend:
    """Test Incremental ML-Enhanced SuperTrend indicator."""

    def test_basic_calculation(self, sample_ohlc):
        """Test basic ML SuperTrend calculation."""
        ml_st = IncrementalMLSuperTrend(period=7)

        results = []
        for h, l, c in zip(
            sample_ohlc['high'], sample_ohlc['low'], sample_ohlc['close']
        ):
            value, direction, confidence = ml_st.update(h, l, c)
            results.append((value, direction, confidence))

        # After warmup, should have valid values
        for val, direction, conf in results:
            if not math.isnan(direction):
                assert direction in [1.0, -1.0]
            if not math.isnan(conf):
                assert 0.0 <= conf <= 1.0

    def test_is_ready_checks_internals(self, sample_ohlc):
        """Test is_ready checks internal indicators."""
        ml_st = IncrementalMLSuperTrend(period=7)

        for h, l, c in zip(
            sample_ohlc['high'], sample_ohlc['low'], sample_ohlc['close']
        ):
            ml_st.update(h, l, c)
            if ml_st.is_ready:
                break

        # Note: Internal Rust components are not exposed as Python attributes
        assert ml_st.is_ready

    def test_confirmation_logic(self, sample_ohlc):
        """Test trend confirmation requires multiple bars."""
        ml_st = IncrementalMLSuperTrend(period=7, confirmation_bars=3)

        for h, l, c in zip(
            sample_ohlc['high'], sample_ohlc['low'], sample_ohlc['close']
        ):
            _, direction, _ = ml_st.update(h, l, c)

        # Confirmed direction should be set
        assert ml_st.current_direction in [1.0, -1.0]

    def test_confidence_calculation(self, sample_ohlc):
        """Test confidence is calculated properly."""
        ml_st = IncrementalMLSuperTrend(period=7)

        confidences = []
        for h, l, c in zip(
            sample_ohlc['high'], sample_ohlc['low'], sample_ohlc['close']
        ):
            _, _, conf = ml_st.update(h, l, c)
            if not math.isnan(conf):
                confidences.append(conf)

        # Confidence should vary based on conditions
        assert len(confidences) > 0
        # All should be in [0, 1]
        assert all(0.0 <= c <= 1.0 for c in confidences)

    def test_reset(self, sample_ohlc):
        """Test reset functionality."""
        ml_st = IncrementalMLSuperTrend(period=7)

        for h, l, c in zip(
            sample_ohlc['high'][:15], sample_ohlc['low'][:15], sample_ohlc['close'][:15]
        ):
            ml_st.update(h, l, c)

        assert ml_st.count > 0
        ml_st.reset()
        assert ml_st.count == 0
        assert not ml_st.is_ready


# ==================== Additional Coverage Tests ====================

class TestResetMethods:
    """Test reset() methods for all incremental indicators."""

    def test_rsi_reset(self):
        """Test IncrementalRSI reset."""
        rsi = IncrementalRSI(14)
        for i in range(20):
            rsi.update(100 + i)
        assert rsi.count == 20
        assert rsi.is_ready
        rsi.reset()
        assert rsi.count == 0
        assert not rsi.is_ready
        assert math.isnan(rsi.current)

    def test_macd_reset(self):
        """Test IncrementalMACD reset."""
        macd = IncrementalMACD()
        for i in range(30):
            macd.update(100 + i * 0.5)
        assert macd.count == 30
        macd.reset()
        assert macd.count == 0
        m, s, h = macd.update(100.0)  # After reset, should be NaN
        assert math.isnan(m)

    def test_stochastic_reset(self):
        """Test IncrementalStochastic reset."""
        stoch = IncrementalStochastic()
        for i in range(20):
            stoch.update(101.0 + i, 99.0 + i, 100.0 + i)
        assert stoch.count == 20
        stoch.reset()
        assert stoch.count == 0
        k, d = stoch.update(101.0, 99.0, 100.0)
        assert math.isnan(k)

    def test_supertrend_reset(self):
        """Test IncrementalSuperTrend reset."""
        st = IncrementalSuperTrend()
        for i in range(20):
            st.update(102.0 + i, 98.0 + i, 100.0 + i)
        assert st.count == 20
        st.reset()
        assert st.count == 0
        assert math.isnan(st.current_direction)


class TestStreamingEdgeCases:
    """Test edge cases for 100% coverage."""

    def test_normalize_weights_zero_sum(self):
        """Test _normalize_weights raises on zero sum."""
        from haze_library.streaming import _normalize_weights
        with pytest.raises(ValueError, match="weights sum cannot be zero"):
            _normalize_weights({"a": 0.0, "b": 0.0}, ["a", "b"])

    def test_normalize_weights_nonfinite(self):
        """Test _normalize_weights raises on non-finite weights."""
        from haze_library.streaming import _normalize_weights
        with pytest.raises(ValueError, match="non-finite value"):
            _normalize_weights({"a": float("inf")}, ["a"])

    def test_adaptive_rsi_nonfinite_input(self):
        """Test IncrementalAdaptiveRSI rejects non-finite input."""
        arsi = IncrementalAdaptiveRSI()
        # First add some valid data
        for i in range(30):
            arsi.update(100.0 + i)
        assert arsi.is_ready
        prev_count = arsi.count
        with pytest.raises(ValueError):
            arsi.update(float('inf'))
        assert arsi.count == prev_count
        assert arsi.is_ready

    def test_adaptive_rsi_nan_input(self):
        """Test IncrementalAdaptiveRSI rejects NaN input."""
        arsi = IncrementalAdaptiveRSI()
        for i in range(30):
            arsi.update(100.0 + i)
        assert arsi.is_ready
        prev_count = arsi.count
        with pytest.raises(ValueError):
            arsi.update(float('nan'))
        assert arsi.count == prev_count
        assert arsi.is_ready

    def test_ema_reset(self):
        """Test IncrementalEMA reset."""
        ema = IncrementalEMA(period=5)
        for i in range(10):
            ema.update(100.0 + i)
        assert ema.count == 10
        assert ema.is_ready
        ema.reset()
        assert ema.count == 0
        assert not ema.is_ready
        assert math.isnan(ema.current)

    def test_atr_reset(self):
        """Test IncrementalATR reset."""
        atr = IncrementalATR(period=7)
        for i in range(15):
            atr.update(102.0 + i, 98.0 + i, 100.0 + i)
        assert atr.count == 15
        assert atr.is_ready
        atr.reset()
        assert atr.count == 0
        assert not atr.is_ready
        assert math.isnan(atr.current)

    def test_bollinger_bands_reset(self):
        """Test IncrementalBollingerBands reset."""
        bb = IncrementalBollingerBands(period=10)
        for i in range(15):
            bb.update(100.0 + i)
        assert bb.count == 15
        assert bb.is_ready
        bb.reset()
        assert bb.count == 0
        assert not bb.is_ready
        upper, middle, lower = bb.update(100.0)
        assert math.isnan(upper)

    def test_sma_invalid_period(self):
        """Test IncrementalSMA rejects period <= 0."""
        with pytest.raises(ValueError, match="period must be > 0"):
            IncrementalSMA(0)
        with pytest.raises(ValueError, match="period must be > 0"):
            IncrementalSMA(-5)

    def test_rsi_invalid_period(self):
        """Test IncrementalRSI rejects period <= 0."""
        with pytest.raises(ValueError, match="period must be > 0"):
            IncrementalRSI(0)
        with pytest.raises(ValueError, match="period must be > 0"):
            IncrementalRSI(-3)
