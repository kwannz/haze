from __future__ import annotations

import inspect

import numpy as np
import pytest

from haze_library import numpy_compat as nc


def _arrays(n: int = 300) -> dict[str, np.ndarray]:
    close = np.linspace(100.0, 120.0, n, dtype=np.float32)
    high = close + 1.0
    low = close - 1.0
    open_ = close + 0.5
    volume = np.linspace(1000.0, 1200.0, n, dtype=np.float64)

    # RSI-like indicator for divergence detection (range 0-100)
    indicator = 30.0 + 40.0 * np.sin(np.linspace(0, 4 * np.pi, n))

    # Binary signals for combine_signals (0.0 or 1.0)
    buy1 = np.zeros(n, dtype=np.float64)
    buy1[::20] = 1.0  # Buy signal every 20 bars
    sell1 = np.zeros(n, dtype=np.float64)
    sell1[10::20] = 1.0  # Sell signal offset by 10

    buy2 = np.zeros(n, dtype=np.float64)
    buy2[5::25] = 1.0  # Different pattern
    sell2 = np.zeros(n, dtype=np.float64)
    sell2[15::25] = 1.0

    # ATR values for calculate_stops (volatility measure)
    atr_values = np.full(n, 2.0, dtype=np.float64)  # Constant ATR for simplicity

    return {
        "data": close,
        "close": close,
        "high": high,
        "low": low,
        "open_": open_,
        "volume": volume,
        "series1": close,
        "series2": open_,
        # SFG function parameters
        "price": close,  # For detect_divergence
        "indicator": indicator,  # For detect_divergence
        "buy1": buy1,  # For combine_signals
        "sell1": sell1,
        "buy2": buy2,
        "sell2": sell2,
        "atr_values": atr_values,  # For calculate_stops
        "buy_signals": buy1,  # For calculate_stops
        "sell_signals": sell1,
    }


def test_numpy_compat_helpers() -> None:
    arr32 = np.array([1.0, 2.0], dtype=np.float32)
    arr64 = np.array([1.0, 2.0], dtype=np.float64)

    out32 = nc._ensure_float64(arr32)
    assert out32.dtype == np.float64

    out64 = nc._ensure_float64(arr64)
    assert out64 is arr64

    list_out = nc._ensure_float64([1.0, 2.0])
    assert list_out.dtype == np.float64

    assert nc._to_list_fast(arr64) == [1.0, 2.0]
    assert nc._to_list_fast([1.0, 2.0]) == [1.0, 2.0]

    result = nc._to_array([1.0, 2.0])
    assert isinstance(result, np.ndarray)
    assert result.dtype == np.float64


def test_numpy_compat_call_all_functions() -> None:
    arrays = _arrays()

    for name, obj in nc.__dict__.items():
        if name.startswith("_"):
            continue
        if not inspect.isfunction(obj):
            continue

        sig = inspect.signature(obj)
        kwargs = {}
        for param in sig.parameters.values():
            if param.default is inspect._empty:
                kwargs[param.name] = arrays[param.name]

        result = obj(**kwargs)
        if isinstance(result, tuple):
            assert len(result) > 0
        else:
            assert result is not None


def test_numpy_compat_edge_branches(monkeypatch) -> None:
    with pytest.raises(ValueError):
        nc.crossover([1.0, 2.0], [1.0])
    assert nc.crossover([1.0], [1.0]).shape == (1,)

    with pytest.raises(ValueError):
        nc.crossunder([1.0, 2.0], [1.0])
    assert nc.crossunder([1.0], [1.0]).shape == (1,)

    with pytest.raises(ValueError):
        nc.highest([1.0, 2.0], period=0)
    assert nc.highest([], period=2).shape == (0,)

    with pytest.raises(ValueError):
        nc.lowest([1.0, 2.0], period=0)
    assert nc.lowest([], period=2).shape == (0,)

    empty = nc.heikin_ashi([], [], [], [])
    assert all(arr.size == 0 for arr in empty)


def test_numpy_compat_import_fallback(monkeypatch) -> None:
    """Test import fallback when haze_library is not available."""
    import importlib
    import sys
    import haze_library as hl

    original_ext = sys.modules.get("haze_library.haze_library")
    sys.modules["haze_library.haze_library"] = None
    monkeypatch.delattr(hl, "haze_library", raising=False)

    importlib.reload(nc)
    assert nc._lib is hl

    if original_ext is not None:
        sys.modules["haze_library.haze_library"] = original_ext
        hl.haze_library = original_ext
    else:
        sys.modules.pop("haze_library.haze_library", None)
    importlib.reload(nc)
