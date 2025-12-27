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
    _rolling_volatility,
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

    def test_is_available_false(self, monkeypatch):
        """Test is_available returns False on import failure.

        We force the nested import to fail by stubbing the extension module.
        """
        import importlib
        import sys
        import haze_library as hl
        import haze_library.ai_indicators as ai_mod

        original_ext = sys.modules.get("haze_library.haze_library")
        sys.modules["haze_library.haze_library"] = None
        monkeypatch.delattr(hl, "haze_library", raising=False)

        importlib.reload(ai_mod)
        assert ai_mod.is_available() is False

        if original_ext is not None:
            sys.modules["haze_library.haze_library"] = original_ext
            hl.haze_library = original_ext
        else:
            sys.modules.pop("haze_library.haze_library", None)
        importlib.reload(ai_mod)

        # Document that 99% coverage is acceptable for this edge case:
        # Lines 10-11 in ai_indicators.py are only executed when the
        # Rust extension (.so/.pyd) file is missing or corrupted.
        # This is an installation-time error, not a runtime scenario.


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

    def test_invalid_parameters(self, sample_close):
        with pytest.raises(ValueError):
            adaptive_rsi(sample_close, min_period=0)
        with pytest.raises(ValueError):
            adaptive_rsi(sample_close, min_period=10, max_period=5)
        with pytest.raises(ValueError):
            adaptive_rsi(sample_close, base_period=0)

    def test_periods_exceed_length(self):
        short_close = [100.0, 101.0, 102.0, 103.0]
        with pytest.raises(ValueError, match="min_period/max_period must be < data length"):
            adaptive_rsi(short_close, min_period=4, max_period=4)
        with pytest.raises(ValueError, match="base_period must be < data length"):
            adaptive_rsi(short_close, base_period=4, min_period=2, max_period=3)
        # volatility_window validation may trigger min/max period error first
        with pytest.raises(ValueError):
            adaptive_rsi(short_close, volatility_window=4)

    def test_base_period_out_of_range(self):
        close = [100.0 + i for i in range(20)]
        with pytest.raises(ValueError, match="base_period must be within \\[min_period, max_period\\]"):
            adaptive_rsi(close, base_period=9, min_period=10, max_period=14)

    def test_rolling_volatility_invalid_window(self, sample_close):
        with pytest.raises(ValueError):
            _rolling_volatility(sample_close, 0)

    def test_rolling_volatility_zero_prev(self):
        values = [0.0, 1.0, 1.1]
        vols = _rolling_volatility(values, 2)
        assert len(vols) == len(values)

    def test_rolling_volatility_long_data(self):
        """Test rolling volatility with data longer than window (covers pop branch)."""
        values = [100.0 + i * 0.5 for i in range(30)]  # 30 data points
        vols = _rolling_volatility(values, 5)  # window of 5
        assert len(vols) == len(values)
        # After warmup, volatility should be calculated
        assert all(v >= 0.0 for v in vols)

    def test_volatility_window_zero(self, sample_close):
        """Test volatility_window <= 0 raises ValueError."""
        with pytest.raises(ValueError, match="volatility_window must be > 0"):
            adaptive_rsi(sample_close, volatility_window=0)

    def test_volatility_window_exceeds_data(self):
        """Test volatility_window >= data length raises ValueError."""
        short_close = [100.0, 101.0, 102.0, 103.0, 104.0]
        with pytest.raises(ValueError, match="volatility_window must be < data length"):
            adaptive_rsi(short_close, volatility_window=5, min_period=2, max_period=4, base_period=3)

    def test_empty_input(self):
        """Test empty input raises ValueError."""
        with pytest.raises(ValueError, match="close cannot be empty"):
            adaptive_rsi([])

    def test_non_finite_value(self):
        """Test non-finite value raises ValueError."""
        with pytest.raises(ValueError, match="non-finite value"):
            adaptive_rsi([1.0, float('inf'), 3.0])


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

    def test_zero_weights(self, sample_ohlcv):
        """Test zero weights raises ValueError."""
        weights = {
            'rsi': 0.0,
            'macd': 0.0,
            'stochastic': 0.0,
            'supertrend': 0.0,
        }
        with pytest.raises(ValueError, match="weights sum cannot be zero"):
            ensemble_signal(
                sample_ohlcv['high'],
                sample_ohlcv['low'],
                sample_ohlcv['close'],
                weights=weights,
            )

    def test_length_mismatch(self, sample_ohlcv):
        with pytest.raises(ValueError):
            ensemble_signal(
                sample_ohlcv['high'][:-1],
                sample_ohlcv['low'],
                sample_ohlcv['close'],
            )

    def test_empty_input(self):
        """Test empty input raises ValueError."""
        with pytest.raises(ValueError, match="close cannot be empty"):
            ensemble_signal([], [], [])

    def test_volume_length_mismatch(self, sample_ohlcv):
        with pytest.raises(ValueError):
            ensemble_signal(
                sample_ohlcv['high'],
                sample_ohlcv['low'],
                sample_ohlcv['close'],
                sample_ohlcv['volume'][:-1],
            )

    def test_non_finite_inputs(self, sample_ohlcv):
        bad_high = list(sample_ohlcv['high'])
        bad_high[0] = float("inf")
        with pytest.raises(ValueError, match="high contains non-finite value"):
            ensemble_signal(
                bad_high,
                sample_ohlcv['low'],
                sample_ohlcv['close'],
            )

        with pytest.raises(ValueError, match="weights contains non-finite value"):
            ensemble_signal(
                sample_ohlcv['high'],
                sample_ohlcv['low'],
                sample_ohlcv['close'],
                weights={"rsi": float("inf")},
            )


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

    def test_empty_input(self):
        """Test empty input raises ValueError."""
        with pytest.raises(ValueError, match="close cannot be empty"):
            ml_supertrend([], [], [])

    def test_invalid_period(self, sample_ohlcv):
        """Test period <= 0 raises ValueError."""
        with pytest.raises(ValueError, match="period must be > 0"):
            ml_supertrend(
                sample_ohlcv['high'],
                sample_ohlcv['low'],
                sample_ohlcv['close'],
                period=0,
            )

    def test_period_exceeds_length(self, sample_ohlcv):
        data_len = len(sample_ohlcv['close'])
        with pytest.raises(ValueError, match="period must be < data length"):
            ml_supertrend(
                sample_ohlcv['high'],
                sample_ohlcv['low'],
                sample_ohlcv['close'],
                period=data_len,
            )

    def test_invalid_multiplier(self, sample_ohlcv):
        """Test multiplier <= 0 raises ValueError."""
        with pytest.raises(ValueError, match="multiplier must be > 0"):
            ml_supertrend(
                sample_ohlcv['high'],
                sample_ohlcv['low'],
                sample_ohlcv['close'],
                multiplier=0.0,
            )

    def test_invalid_confirmation_bars(self, sample_ohlcv):
        """Test confirmation_bars <= 0 raises ValueError."""
        with pytest.raises(ValueError, match="confirmation_bars must be > 0"):
            ml_supertrend(
                sample_ohlcv['high'],
                sample_ohlcv['low'],
                sample_ohlcv['close'],
                confirmation_bars=0,
            )

    def test_confirmation_bars_exceeds_length(self, sample_ohlcv):
        data_len = len(sample_ohlcv['close'])
        with pytest.raises(ValueError, match="confirmation_bars must be <= data length"):
            ml_supertrend(
                sample_ohlcv['high'],
                sample_ohlcv['low'],
                sample_ohlcv['close'],
                confirmation_bars=data_len + 1,
            )

    def test_length_mismatch(self, sample_ohlcv):
        with pytest.raises(ValueError):
            ml_supertrend(
                sample_ohlcv['high'][:-1],
                sample_ohlcv['low'],
                sample_ohlcv['close'],
            )

    def test_confirmation_bars_one(self, sample_ohlcv):
        _st, direction, confidence = ml_supertrend(
            sample_ohlcv['high'],
            sample_ohlcv['low'],
            sample_ohlcv['close'],
            confirmation_bars=1,
            use_atr_filter=False,
        )
        assert len(direction) == len(sample_ohlcv['close'])
        assert len(confidence) == len(sample_ohlcv['close'])
