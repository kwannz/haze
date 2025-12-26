"""
Public Workflow Smoke Tests
==========================

验证文档中提到的常见工作流可以跑通：
- clean API（无 `py_` 前缀）
- `haze` 作为 `haze_library` 的别名包
"""

from __future__ import annotations

import haze
import haze_library as haze_library


class TestCleanAPIWorkflows:
    def test_clean_functions_exist(self):
        expected = [
            "sma",
            "ema",
            "hma",
            "rsi",
            "macd",
            "stochastic",
            "atr",
            "bollinger_bands",
            "supertrend",
            "adx",
        ]
        for name in expected:
            assert hasattr(haze_library, name), f"Missing: {name}"
            assert callable(getattr(haze_library, name)), f"Not callable: {name}"

    def test_clean_keyword_aliases(self):
        close = [100.0, 101.0, 102.0, 101.5, 103.0]
        high = [101.0, 102.0, 103.0, 102.5, 104.0]
        low = [99.0, 100.0, 101.0, 100.5, 102.0]

        _ = haze_library.sma(close=close, period=3)
        _ = haze_library.ema(close=close, period=3)
        _ = haze_library.hma(close=close, period=3)

        _ = haze_library.macd(close, fast=3, slow=5, signal=2)
        _ = haze_library.bollinger_bands(close=close, period=3, std_dev=2.0)
        _ = haze_library.stochastic(high, low, close, k_period=3, d_period=2)


class TestHazeAliasPackage:
    def test_forwarded_attributes(self):
        assert hasattr(haze, "sma")
        assert hasattr(haze, "py_sma")
        assert hasattr(haze, "stochastic")

    def test_import_specific_name(self):
        from haze import py_sma

        result = py_sma([1.0, 2.0, 3.0], 2)
        assert isinstance(result, list)

