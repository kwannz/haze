from __future__ import annotations

import builtins
import types

import numpy as np

from haze_library import polars_ta, torch_ta


class FakeSeries:
    def __init__(self, name: str, values):
        self.name = name
        self.values = list(values)


class FakeColumn:
    def __init__(self, values):
        self._values = list(values)

    def to_list(self):
        return list(self._values)


class FakeDataFrame:
    def __init__(self, data: dict[str, list[float]]):
        self._data = data

    def __getitem__(self, key: str) -> FakeColumn:
        return FakeColumn(self._data[key])

    def with_columns(self, _series):
        return self


class FakeTensor:
    def __init__(self, values):
        self._values = list(values)
        self.device = "cpu"

    def detach(self):
        return self

    def to(self, device=None, dtype=None):
        if device is not None:
            self.device = device
        return self

    def tolist(self):
        return list(self._values)


def test_polars_backend(monkeypatch) -> None:
    original_import = builtins.__import__

    def blocked_import(name, globals=None, locals=None, fromlist=(), level=0):
        if name == "polars":
            raise ImportError("blocked")
        return original_import(name, globals, locals, fromlist, level)

    monkeypatch.setattr(builtins, "__import__", blocked_import)
    assert polars_ta.is_available() is False

    fake_polars = types.SimpleNamespace(Series=FakeSeries)
    monkeypatch.setitem(__import__("sys").modules, "polars", fake_polars)
    monkeypatch.setattr(builtins, "__import__", original_import)

    data = {
        "close": list(np.linspace(100, 120, 50)),
        "high": list(np.linspace(101, 121, 50)),
        "low": list(np.linspace(99, 119, 50)),
        "volume": list(np.linspace(1000, 1200, 50)),
    }
    df = FakeDataFrame(data)

    assert polars_ta.is_available() is True
    assert "sma" in polars_ta.get_available_functions()

    out = polars_ta._series_to_float_list([1.0, None])
    assert np.isnan(out[1])

    _ = polars_ta.sma(df, "close", 5)
    _ = polars_ta.ema(df, "close", 5)
    _ = polars_ta.rsi(df, "close", 5)
    _ = polars_ta.macd(df, "close")
    _ = polars_ta.bollinger_bands(df, "close")
    _ = polars_ta.atr(df)
    _ = polars_ta.supertrend(df)
    _ = polars_ta.obv(df)
    _ = polars_ta.vwap(df)


def test_torch_backend(monkeypatch) -> None:
    original_import = builtins.__import__

    def blocked_import(name, globals=None, locals=None, fromlist=(), level=0):
        if name == "torch":
            raise ImportError("blocked")
        return original_import(name, globals, locals, fromlist, level)

    monkeypatch.setattr(builtins, "__import__", blocked_import)
    assert torch_ta.is_available() is False

    fake_torch = types.SimpleNamespace(
        tensor=lambda values, device=None, dtype=None: FakeTensor(values),
        float64=object(),
    )
    monkeypatch.setitem(__import__("sys").modules, "torch", fake_torch)
    monkeypatch.setattr(builtins, "__import__", original_import)

    close = FakeTensor(np.linspace(100, 120, 50))
    high = FakeTensor(np.linspace(101, 121, 50))
    low = FakeTensor(np.linspace(99, 119, 50))
    volume = FakeTensor(np.linspace(1000, 1200, 50))

    assert torch_ta.is_available() is True
    assert "sma" in torch_ta.get_available_functions()

    _ = torch_ta.sma(close, 5)
    _ = torch_ta.ema(close, 5)
    _ = torch_ta.rsi(close, 5)
    _ = torch_ta.macd(close)
    _ = torch_ta.bollinger_bands(close)
    _ = torch_ta.atr(high, low, close, period=5)
    _ = torch_ta.supertrend(high, low, close, period=5)
    _ = torch_ta.obv(close, volume)
    _ = torch_ta.vwap(high, low, close, volume, period=0)
