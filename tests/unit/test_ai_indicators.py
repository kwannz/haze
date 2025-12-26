"""
AI Indicators Tests
===================

Test AI-enhanced technical indicators.

Author: Haze Team
Date: 2025-12-26
"""

import pytest
import math
import sys
import os

# Add parent to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../rust/python'))

from haze_library.ai_indicators import (
    adaptive_rsi,
    ensemble_signal,
    ml_supertrend,
    get_available_ai_indicators,
    is_available,
)


# ==================== Fixtures ====================

@pytest.fixture
def sample_close():
    """Sample close prices with some volatility."""
    return [
        100.0, 101.0, 102.0, 101.5, 103.0, 102.5, 104.0, 103.5, 105.0, 104.5,
        106.0, 105.5, 107.0, 106.5, 108.0, 107.5, 109.0, 108.5, 110.0, 109.5,
        108.0, 107.0, 106.0, 105.0, 104.0, 105.0, 106.0, 107.0, 108.0, 109.0,
        110.0, 111.0, 112.0, 113.0, 114.0, 113.0, 112.0, 111.0, 110.0, 109.0,
        108.0, 109.0, 110.0, 111.0, 112.0, 113.0, 114.0, 115.0, 116.0, 117.0,
    ]


@pytest.fixture
def sample_ohlcv():
    """Sample OHLCV data."""
    base_close = [
        100.0, 101.0, 102.0, 101.5, 103.0, 102.5, 104.0, 103.5, 105.0, 104.5,
        106.0, 105.5, 107.0, 106.5, 108.0, 107.5, 109.0, 108.5, 110.0, 109.5,
        108.0, 107.0, 106.0, 105.0, 104.0, 105.0, 106.0, 107.0, 108.0, 109.0,
        110.0, 111.0, 112.0, 113.0, 114.0, 113.0, 112.0, 111.0, 110.0, 109.0,
        108.0, 109.0, 110.0, 111.0, 112.0, 113.0, 114.0, 115.0, 116.0, 117.0,
    ]
    return {
        'high': [c + 1.0 for c in base_close],
        'low': [c - 1.0 for c in base_close],
        'close': base_close,
        'volume': [1000.0 + i * 10 for i in range(len(base_close))],
    }


# ==================== Utility Tests ====================

class TestUtilityFunctions:
    """Test utility functions."""

    def test_is_available(self):
        """Test is_available returns True."""
        assert is_available() is True

    def test_get_available_indicators(self):
        """Test get_available_ai_indicators."""
        indicators = get_available_ai_indicators()
        assert isinstance(indicators, list)
        assert "adaptive_rsi" in indicators
        assert "ensemble_signal" in indicators
        assert "ml_supertrend" in indicators


# ==================== Adaptive RSI Tests ====================

class TestAdaptiveRSI:
    """Test Adaptive RSI indicator."""

    def test_basic_calculation(self, sample_close):
        """Test basic adaptive RSI calculation."""
        rsi, periods = adaptive_rsi(sample_close)

        assert len(rsi) == len(sample_close)
        assert len(periods) == len(sample_close)

    def test_rsi_range(self, sample_close):
        """Test RSI values are in valid range."""
        rsi, _ = adaptive_rsi(sample_close)

        valid_values = [v for v in rsi if not math.isnan(v)]
        assert all(0 <= v <= 100 for v in valid_values)

    def test_periods_in_range(self, sample_close):
        """Test adaptive periods are within configured range."""
        min_p, max_p = 7, 28
        _, periods = adaptive_rsi(sample_close, min_period=min_p, max_period=max_p)

        assert all(min_p <= p <= max_p for p in periods)

    def test_custom_parameters(self, sample_close):
        """Test with custom parameters."""
        rsi, periods = adaptive_rsi(
            sample_close,
            base_period=10,
            min_period=5,
            max_period=20,
            volatility_window=15,
        )
        assert len(rsi) == len(sample_close)
        assert all(5 <= p <= 20 for p in periods)


# ==================== Ensemble Signal Tests ====================

class TestEnsembleSignal:
    """Test Ensemble Signal indicator."""

    def test_basic_calculation(self, sample_ohlcv):
        """Test basic ensemble signal calculation."""
        signal, components = ensemble_signal(
            sample_ohlcv['high'],
            sample_ohlcv['low'],
            sample_ohlcv['close'],
        )

        assert len(signal) == len(sample_ohlcv['close'])
        assert 'rsi' in components
        assert 'macd' in components
        assert 'stochastic' in components
        assert 'supertrend' in components

    def test_signal_range(self, sample_ohlcv):
        """Test ensemble signal is in [-1, 1] range."""
        signal, _ = ensemble_signal(
            sample_ohlcv['high'],
            sample_ohlcv['low'],
            sample_ohlcv['close'],
        )

        assert all(-1.0 <= s <= 1.0 for s in signal)

    def test_with_volume(self, sample_ohlcv):
        """Test ensemble signal with volume data."""
        signal, components = ensemble_signal(
            sample_ohlcv['high'],
            sample_ohlcv['low'],
            sample_ohlcv['close'],
            sample_ohlcv['volume'],
        )

        assert len(signal) == len(sample_ohlcv['close'])
        assert 'mfi' in components

    def test_custom_weights(self, sample_ohlcv):
        """Test ensemble signal with custom weights."""
        weights = {
            'rsi': 0.5,
            'macd': 0.3,
            'stochastic': 0.1,
            'supertrend': 0.1,
        }
        signal, _ = ensemble_signal(
            sample_ohlcv['high'],
            sample_ohlcv['low'],
            sample_ohlcv['close'],
            weights=weights,
        )

        assert len(signal) == len(sample_ohlcv['close'])


# ==================== ML SuperTrend Tests ====================

class TestMLSuperTrend:
    """Test ML-enhanced SuperTrend indicator."""

    def test_basic_calculation(self, sample_ohlcv):
        """Test basic ML SuperTrend calculation."""
        st, direction, confidence = ml_supertrend(
            sample_ohlcv['high'],
            sample_ohlcv['low'],
            sample_ohlcv['close'],
        )

        assert len(st) == len(sample_ohlcv['close'])
        assert len(direction) == len(sample_ohlcv['close'])
        assert len(confidence) == len(sample_ohlcv['close'])

    def test_direction_values(self, sample_ohlcv):
        """Test direction is 1 or -1."""
        _, direction, _ = ml_supertrend(
            sample_ohlcv['high'],
            sample_ohlcv['low'],
            sample_ohlcv['close'],
        )

        valid_directions = [d for d in direction if not math.isnan(d)]
        assert all(d in [1.0, -1.0, 1, -1] for d in valid_directions)

    def test_confidence_range(self, sample_ohlcv):
        """Test confidence is in [0, 1] range."""
        _, _, confidence = ml_supertrend(
            sample_ohlcv['high'],
            sample_ohlcv['low'],
            sample_ohlcv['close'],
        )

        assert all(0.0 <= c <= 1.0 for c in confidence)

    def test_custom_parameters(self, sample_ohlcv):
        """Test with custom parameters."""
        st, direction, confidence = ml_supertrend(
            sample_ohlcv['high'],
            sample_ohlcv['low'],
            sample_ohlcv['close'],
            period=7,
            multiplier=2.5,
            confirmation_bars=3,
            use_atr_filter=True,
        )

        assert len(st) == len(sample_ohlcv['close'])

    def test_no_atr_filter(self, sample_ohlcv):
        """Test without ATR filter."""
        st, direction, confidence = ml_supertrend(
            sample_ohlcv['high'],
            sample_ohlcv['low'],
            sample_ohlcv['close'],
            use_atr_filter=False,
        )

        assert len(st) == len(sample_ohlcv['close'])
