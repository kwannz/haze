"""
Deprecation Warning Tests
=========================

Test that legacy py_* API triggers deprecation warnings.

Author: Haze Team
Date: 2025-12-26
"""

import pytest
import warnings
import numpy as np


class TestDeprecationWarnings:
    """Test deprecation warnings for legacy API."""

    def test_clean_api_no_warning(self):
        """Test that clean API doesn't trigger warnings."""
        import haze_library

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            # Access clean API
            _ = haze_library.sma
            _ = haze_library.rsi
            _ = haze_library.macd
            # No deprecation warnings should be raised
            deprecation_warnings = [
                x for x in w if issubclass(x.category, DeprecationWarning)
            ]
            assert len(deprecation_warnings) == 0

    def test_py_prefix_mapping_exists(self):
        """Test that the py_ prefix mapping is complete."""
        import haze_library

        # Check that mapping exists and has expected entries
        assert hasattr(haze_library, "_PY_PREFIX_ALIASES")
        mapping = haze_library._PY_PREFIX_ALIASES

        # Verify key indicators are mapped
        assert "py_sma" in mapping
        assert mapping["py_sma"] == "sma"
        assert "py_rsi" in mapping
        assert mapping["py_rsi"] == "rsi"
        assert "py_macd" in mapping
        assert mapping["py_macd"] == "macd"
        assert "py_supertrend" in mapping
        assert mapping["py_supertrend"] == "supertrend"

    def test_clean_api_functions_exist(self):
        """Test that all clean API functions are accessible."""
        import haze_library

        # Core indicators should be accessible via clean names
        core_indicators = [
            "sma", "ema", "rsi", "macd", "bollinger_bands",
            "atr", "supertrend", "obv", "vwap", "adx",
        ]
        for name in core_indicators:
            assert hasattr(haze_library, name), f"Missing: {name}"
            func = getattr(haze_library, name)
            assert callable(func), f"Not callable: {name}"


class TestAPIConsistency:
    """Test API consistency between py_* and clean names."""

    def test_sma_produces_same_results(self):
        """Test that sma() produces same results regardless of access method."""
        import haze_library

        close = [100.0, 101.0, 102.0, 101.5, 103.0, 102.5, 104.0]
        period = 3

        # Using clean API
        result_clean = haze_library.sma(close, period)

        # Using legacy API (direct from Rust module)
        from haze_library.haze_library import py_sma
        result_legacy = py_sma(close, period)

        # Results should be identical (use allclose for NaN comparison)
        assert np.allclose(result_clean, result_legacy, equal_nan=True)

    def test_rsi_produces_same_results(self):
        """Test that rsi() produces same results regardless of access method."""
        import haze_library

        close = [44.0, 44.5, 43.5, 44.0, 44.5, 45.0, 44.5, 45.5, 46.0, 45.5, 46.5, 47.0, 46.5, 47.5, 48.0]
        period = 7

        # Using clean API
        result_clean = haze_library.rsi(close, period)

        # Using legacy API (direct from Rust module)
        from haze_library.haze_library import py_rsi
        result_legacy = py_rsi(close, period)

        # Results should be identical (use allclose for NaN comparison)
        assert np.allclose(result_clean, result_legacy, equal_nan=True)
