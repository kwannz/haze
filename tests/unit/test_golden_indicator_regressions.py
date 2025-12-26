"""
Golden Indicator Regression Tests
=================================

This suite pins a small, representative subset of indicator outputs to a
versioned fixture file. It is meant to catch accidental numerical regressions
or API contract drift.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable, Mapping

import numpy as np
import pytest

import haze_library as haze


_FIXTURE_PATH = Path(__file__).resolve().parents[1] / "fixtures" / "golden_indicators_v1.json"


def _to_float_array(values: list[float | None]) -> np.ndarray:
    return np.array(
        [np.nan if v is None else float(v) for v in values],
        dtype=np.float64,
    )


def _assert_series_allclose(actual: list[float], expected: list[float | None]) -> None:
    actual_arr = _to_float_array([float(v) for v in actual])
    expected_arr = _to_float_array(expected)
    np.testing.assert_allclose(
        actual_arr,
        expected_arr,
        rtol=0.0,
        atol=1e-12,
        equal_nan=True,
    )


def _load_fixture() -> dict[str, Any]:
    if not _FIXTURE_PATH.exists():
        raise AssertionError(f"Missing golden fixture: {_FIXTURE_PATH}")
    return json.loads(_FIXTURE_PATH.read_text(encoding="utf-8"))


def _call_indicator(
    name: str,
    inputs: Mapping[str, list[float]],
    params: Mapping[str, Any],
) -> Any:
    close = inputs["close"]
    high = inputs["high"]
    low = inputs["low"]
    volume = inputs["volume"]

    if name == "py_sma":
        return haze.py_sma(close, int(params["period"]))
    if name == "py_ema":
        return haze.py_ema(close, int(params["period"]))
    if name == "py_rsi":
        return haze.py_rsi(close, int(params["period"]))
    if name == "py_macd":
        return haze.py_macd(
            close,
            int(params["fast_period"]),
            int(params["slow_period"]),
            int(params["signal_period"]),
        )
    if name == "py_bollinger_bands":
        return haze.py_bollinger_bands(
            close,
            int(params["period"]),
            float(params["std_multiplier"]),
        )
    if name == "py_atr":
        return haze.py_atr(high, low, close, int(params["period"]))
    if name == "py_supertrend":
        return haze.py_supertrend(
            high,
            low,
            close,
            int(params["period"]),
            float(params["multiplier"]),
        )
    if name == "py_vwap":
        return haze.py_vwap(high, low, close, volume, int(params["period"]))
    if name == "py_correlation":
        return haze.py_correlation(close, volume, int(params["period"]))
    if name == "py_zscore":
        return haze.py_zscore(close, int(params["period"]))

    raise AssertionError(f"Unsupported indicator in golden suite: {name}")


def _assert_output_matches(actual: Any, expected: Any) -> None:
    if isinstance(expected, list) and expected and isinstance(expected[0], list):
        assert isinstance(actual, (tuple, list)), f"Expected tuple/list, got {type(actual).__name__}"
        assert len(actual) == len(expected), "Multi-output length mismatch"
        for actual_item, expected_item in zip(actual, expected):
            _assert_series_allclose(list(actual_item), list(expected_item))
        return

    assert isinstance(expected, list), "Expected list output in fixture"
    _assert_series_allclose(list(actual), list(expected))


class TestGoldenIndicatorRegressions:
    def test_fixture_version_matches_package_version(self) -> None:
        fixture = _load_fixture()
        assert fixture["schema_version"] == 1
        assert fixture["haze_library_version"] == haze.__version__

    def test_outputs_match_golden_fixture(self) -> None:
        fixture = _load_fixture()

        inputs = fixture["inputs"]
        expected = fixture["expected"]

        for name, spec in expected.items():
            params = spec["params"]
            expected_output = spec["output"]

            actual_output = _call_indicator(name, inputs, params)
            _assert_output_matches(actual_output, expected_output)

