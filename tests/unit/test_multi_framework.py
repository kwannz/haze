"""
Multi-Framework Integration Tests
=================================

测试 Polars 和 PyTorch 集成功能。

Author: Haze Team
Date: 2025-12-26
"""

import pytest
import numpy as np
from typing import Dict, List

# Import haze library
import haze_library
from haze_library import polars_ta, torch_ta


# ==================== Fixtures ====================

@pytest.fixture
def sample_close() -> List[float]:
    """Sample close prices for testing."""
    return [100.0, 101.0, 102.0, 101.5, 103.0, 102.5, 104.0, 103.5, 105.0, 104.5,
            106.0, 105.5, 107.0, 106.5, 108.0, 107.5, 109.0, 108.5, 110.0, 109.5]


@pytest.fixture
def sample_ohlcv() -> Dict[str, List[float]]:
    """Sample OHLCV data for testing."""
    return {
        'open': [100.0, 101.0, 102.0, 101.5, 103.0, 102.5, 104.0, 103.5, 105.0, 104.5],
        'high': [101.0, 102.0, 103.0, 102.5, 104.0, 103.5, 105.0, 104.5, 106.0, 105.5],
        'low': [99.0, 100.0, 101.0, 100.5, 102.0, 101.5, 103.0, 102.5, 104.0, 103.5],
        'close': [100.5, 101.5, 102.5, 101.0, 103.5, 102.0, 104.5, 103.0, 105.5, 104.0],
        'volume': [1000.0, 1100.0, 1200.0, 1150.0, 1300.0, 1250.0, 1400.0, 1350.0, 1500.0, 1450.0],
    }


# ==================== Polars Tests ====================

class TestPolarsIntegration:
    """Test Polars DataFrame integration."""

    @pytest.fixture
    def polars_df(self, sample_ohlcv):
        """Create a Polars DataFrame from sample data."""
        pytest.importorskip("polars")
        import polars as pl
        return pl.DataFrame(sample_ohlcv)

    def test_polars_module_available(self):
        """Test that polars_ta module is available."""
        assert polars_ta is not None

    def test_polars_sma(self, polars_df):
        """Test SMA calculation with Polars."""
        result = polars_ta.sma(polars_df, "close", period=5)
        assert "sma" in result.columns
        assert len(result) == len(polars_df)

    def test_polars_ema(self, polars_df):
        """Test EMA calculation with Polars."""
        result = polars_ta.ema(polars_df, "close", period=5)
        assert "ema" in result.columns
        assert len(result) == len(polars_df)

    def test_polars_rsi(self, polars_df):
        """Test RSI calculation with Polars."""
        result = polars_ta.rsi(polars_df, "close", period=7)
        assert "rsi" in result.columns
        # RSI should be between 0 and 100 (ignoring NaN)
        rsi_values = result["rsi"].to_list()
        valid_values = [v for v in rsi_values if v is not None and not np.isnan(v)]
        assert all(0 <= v <= 100 for v in valid_values)

    def test_polars_macd(self, polars_df):
        """Test MACD calculation with Polars."""
        result = polars_ta.macd(polars_df, "close", fast_period=3, slow_period=5, signal_period=2)
        assert "macd" in result.columns
        assert "macd_signal" in result.columns
        assert "macd_histogram" in result.columns

    def test_polars_bollinger_bands(self, polars_df):
        """Test Bollinger Bands calculation with Polars."""
        result = polars_ta.bollinger_bands(polars_df, "close", period=5, std_multiplier=2.0)
        assert "bb_upper" in result.columns
        assert "bb_middle" in result.columns
        assert "bb_lower" in result.columns

    def test_polars_atr(self, polars_df):
        """Test ATR calculation with Polars."""
        result = polars_ta.atr(polars_df, period=5)
        assert "atr" in result.columns
        # ATR should be positive
        atr_values = result["atr"].to_list()
        valid_values = [v for v in atr_values if v is not None and not np.isnan(v)]
        assert all(v >= 0 for v in valid_values)

    def test_polars_supertrend(self, polars_df):
        """Test SuperTrend calculation with Polars."""
        result = polars_ta.supertrend(polars_df, period=5, multiplier=2.0)
        assert "supertrend" in result.columns
        assert "supertrend_direction" in result.columns

    def test_polars_obv(self, polars_df):
        """Test OBV calculation with Polars."""
        result = polars_ta.obv(polars_df)
        assert "obv" in result.columns

    def test_polars_vwap(self, polars_df):
        """Test VWAP calculation with Polars."""
        result = polars_ta.vwap(polars_df)
        assert "vwap" in result.columns

    def test_polars_custom_column_name(self, polars_df):
        """Test custom result column naming."""
        result = polars_ta.sma(polars_df, "close", period=5, result_column="my_sma")
        assert "my_sma" in result.columns
        assert "sma" not in result.columns

    def test_polars_chaining(self, polars_df):
        """Test chaining multiple indicators."""
        result = polars_ta.sma(polars_df, "close", period=5)
        result = polars_ta.rsi(result, "close", period=7)
        assert "sma" in result.columns
        assert "rsi" in result.columns


# ==================== PyTorch Tests ====================

class TestPyTorchIntegration:
    """Test PyTorch tensor integration."""

    @pytest.fixture
    def torch_tensors(self, sample_ohlcv):
        """Create PyTorch tensors from sample data."""
        pytest.importorskip("torch")
        import torch
        return {
            'high': torch.tensor(sample_ohlcv['high']),
            'low': torch.tensor(sample_ohlcv['low']),
            'close': torch.tensor(sample_ohlcv['close']),
            'volume': torch.tensor(sample_ohlcv['volume']),
        }

    def test_torch_module_available(self):
        """Test that torch_ta module is available."""
        assert torch_ta is not None

    def test_torch_sma(self, torch_tensors):
        """Test SMA calculation with PyTorch."""
        import torch
        result = torch_ta.sma(torch_tensors['close'], period=5)
        assert isinstance(result, torch.Tensor)
        assert result.shape == torch_tensors['close'].shape

    def test_torch_ema(self, torch_tensors):
        """Test EMA calculation with PyTorch."""
        import torch
        result = torch_ta.ema(torch_tensors['close'], period=5)
        assert isinstance(result, torch.Tensor)
        assert result.shape == torch_tensors['close'].shape

    def test_torch_rsi(self, torch_tensors):
        """Test RSI calculation with PyTorch."""
        import torch
        result = torch_ta.rsi(torch_tensors['close'], period=7)
        assert isinstance(result, torch.Tensor)
        # RSI should be between 0 and 100 (ignoring NaN)
        valid_mask = ~torch.isnan(result)
        if valid_mask.any():
            valid_values = result[valid_mask]
            assert (valid_values >= 0).all() and (valid_values <= 100).all()

    def test_torch_macd(self, torch_tensors):
        """Test MACD calculation with PyTorch."""
        import torch
        macd_line, signal_line, histogram = torch_ta.macd(
            torch_tensors['close'], fast_period=3, slow_period=5, signal_period=2
        )
        assert isinstance(macd_line, torch.Tensor)
        assert isinstance(signal_line, torch.Tensor)
        assert isinstance(histogram, torch.Tensor)

    def test_torch_bollinger_bands(self, torch_tensors):
        """Test Bollinger Bands calculation with PyTorch."""
        import torch
        upper, middle, lower = torch_ta.bollinger_bands(
            torch_tensors['close'], period=5, std_multiplier=2.0
        )
        assert isinstance(upper, torch.Tensor)
        assert isinstance(middle, torch.Tensor)
        assert isinstance(lower, torch.Tensor)

    def test_torch_atr(self, torch_tensors):
        """Test ATR calculation with PyTorch."""
        import torch
        result = torch_ta.atr(
            torch_tensors['high'], torch_tensors['low'], torch_tensors['close'], period=5
        )
        assert isinstance(result, torch.Tensor)
        # ATR should be positive
        valid_mask = ~torch.isnan(result)
        if valid_mask.any():
            assert (result[valid_mask] >= 0).all()

    def test_torch_supertrend(self, torch_tensors):
        """Test SuperTrend calculation with PyTorch."""
        import torch
        trend, direction = torch_ta.supertrend(
            torch_tensors['high'], torch_tensors['low'], torch_tensors['close'],
            period=5, multiplier=2.0
        )
        assert isinstance(trend, torch.Tensor)
        assert isinstance(direction, torch.Tensor)

    def test_torch_obv(self, torch_tensors):
        """Test OBV calculation with PyTorch."""
        import torch
        result = torch_ta.obv(torch_tensors['close'], torch_tensors['volume'])
        assert isinstance(result, torch.Tensor)

    def test_torch_vwap(self, torch_tensors):
        """Test VWAP calculation with PyTorch."""
        import torch
        result = torch_ta.vwap(
            torch_tensors['high'], torch_tensors['low'],
            torch_tensors['close'], torch_tensors['volume']
        )
        assert isinstance(result, torch.Tensor)

    def test_torch_device_preservation(self, torch_tensors):
        """Test that output tensor preserves input device."""
        import torch
        # CPU test
        close_cpu = torch_tensors['close']
        result = torch_ta.sma(close_cpu, period=5)
        assert result.device == close_cpu.device

    def test_torch_gradient_detached(self, torch_tensors):
        """Test that gradients are detached (no grad tracking)."""
        import torch
        close = torch_tensors['close'].requires_grad_(True)
        result = torch_ta.sma(close, period=5)
        # Result should not require grad (computation done in Rust)
        assert not result.requires_grad


# ==================== Cross-Framework Consistency Tests ====================

class TestCrossFrameworkConsistency:
    """Test that different frameworks produce consistent results."""

    def test_sma_consistency(self, sample_close):
        """Test SMA produces same results across frameworks."""
        pytest.importorskip("polars")
        pytest.importorskip("torch")
        import polars as pl
        import torch

        period = 5

        # NumPy (via py_sma)
        np_result = haze_library.py_sma(sample_close, period)

        # Polars
        pl_df = pl.DataFrame({"close": sample_close})
        pl_result = polars_ta.sma(pl_df, "close", period)["sma"].to_list()

        # PyTorch
        torch_close = torch.tensor(sample_close)
        torch_result = torch_ta.sma(torch_close, period).tolist()

        # Compare (within floating point tolerance)
        for i in range(len(sample_close)):
            if np.isnan(np_result[i]):
                assert np.isnan(pl_result[i]) or pl_result[i] is None
                assert np.isnan(torch_result[i])
            else:
                assert abs(np_result[i] - pl_result[i]) < 1e-9
                assert abs(np_result[i] - torch_result[i]) < 1e-9

    def test_rsi_consistency(self, sample_close):
        """Test RSI produces same results across frameworks."""
        pytest.importorskip("polars")
        pytest.importorskip("torch")
        import polars as pl
        import torch

        period = 7

        # NumPy (via py_rsi)
        np_result = haze_library.py_rsi(sample_close, period)

        # Polars
        pl_df = pl.DataFrame({"close": sample_close})
        pl_result = polars_ta.rsi(pl_df, "close", period)["rsi"].to_list()

        # PyTorch
        torch_close = torch.tensor(sample_close)
        torch_result = torch_ta.rsi(torch_close, period).tolist()

        # Compare (within floating point tolerance)
        for i in range(len(sample_close)):
            if np.isnan(np_result[i]):
                assert np.isnan(pl_result[i]) or pl_result[i] is None
                assert np.isnan(torch_result[i])
            else:
                assert abs(np_result[i] - pl_result[i]) < 1e-9
                assert abs(np_result[i] - torch_result[i]) < 1e-9


# ==================== Utility Function Tests ====================

class TestUtilityFunctions:
    """Test utility functions."""

    def test_polars_is_available(self):
        """Test polars_ta.is_available()."""
        result = polars_ta.is_available()
        assert isinstance(result, bool)

    def test_polars_get_available_functions(self):
        """Test polars_ta.get_available_functions()."""
        funcs = polars_ta.get_available_functions()
        assert isinstance(funcs, list)
        assert "sma" in funcs
        assert "rsi" in funcs

    def test_torch_is_available(self):
        """Test torch_ta.is_available()."""
        result = torch_ta.is_available()
        assert isinstance(result, bool)

    def test_torch_get_available_functions(self):
        """Test torch_ta.get_available_functions()."""
        funcs = torch_ta.get_available_functions()
        assert isinstance(funcs, list)
        assert "sma" in funcs
        assert "rsi" in funcs
