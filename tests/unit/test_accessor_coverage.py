from __future__ import annotations


import numpy as np
import pandas as pd
import pytest

from haze_library import accessor as acc_mod
from haze_library.accessor import TechnicalAnalysisAccessor, SeriesTechnicalAnalysisAccessor
from haze_library.exceptions import ColumnNotFoundError


def _build_df(n: int = 300) -> pd.DataFrame:
    rng = np.random.default_rng(42)
    close = np.linspace(100.0, 120.0, n)
    open_ = close + rng.normal(0.0, 0.5, n)
    high = close + 1.0
    low = close - 1.0
    volume = rng.integers(1000, 2000, size=n).astype(float)
    return pd.DataFrame(
        {
            "open": open_,
            "high": high,
            "low": low,
            "close": close,
            "volume": volume,
        }
    )


def test_accessor_frame_cache_and_aliases() -> None:
    df = _build_df()
    acc = TechnicalAnalysisAccessor(df)

    frame1 = acc.frame()
    frame2 = acc.frame()
    assert frame1 is frame2

    frame3 = acc.frame(refresh=True)
    assert frame3 is not frame2

    acc.clear_frame_cache()
    frame4 = acc.frame()
    assert frame4 is not None

    df_alias = df.rename(
        columns={
            "close": "Adj Close",
            "high": "High",
            "low": "Low",
            "open": "Open",
            "volume": "Volume",
        }
    )
    acc_alias = TechnicalAnalysisAccessor(df_alias)
    assert acc_alias._get_column("close").equals(df_alias["Adj Close"])

    with pytest.raises(ColumnNotFoundError):
        acc_alias._get_column("missing")

    _ = acc_mod._to_list(np.array([1.0, 2.0], dtype=np.float64))
    _ = acc_mod._to_list([1.0, 2.0])


def test_accessor_dynamic_wrapped_results(monkeypatch: pytest.MonkeyPatch) -> None:
    df = _build_df()
    acc = TechnicalAnalysisAccessor(df)

    def py_fake_list(values: list[float]) -> list[float]:
        return [1.0] * len(values)

    def py_fake_tuple(values: list[float]) -> tuple[list[float], list[float]]:
        return [1.0] * len(values), [2.0] * len(values)

    def py_fake_dict(values: list[float]) -> dict[str, list[float]]:
        return {"alpha": [3.0] * len(values)}

    def py_fake_extra(values: list[float], period: int = 3) -> list[float]:
        return [float(period)] * len(values)

    def py_fake_scalar(values: list[float]) -> float:
        return 42.0

    def py_fake_ohlc(open: list[float], high: list[float]) -> list[float]:
        return [o + h for o, h in zip(open, high)]

    monkeypatch.setattr(acc_mod._lib, "py_fake_list", py_fake_list, raising=False)
    monkeypatch.setattr(acc_mod._lib, "py_fake_tuple", py_fake_tuple, raising=False)
    monkeypatch.setattr(acc_mod._lib, "py_fake_dict", py_fake_dict, raising=False)
    monkeypatch.setattr(acc_mod._lib, "py_fake_extra", py_fake_extra, raising=False)
    monkeypatch.setattr(acc_mod._lib, "py_fake_scalar", py_fake_scalar, raising=False)
    monkeypatch.setattr(acc_mod._lib, "py_fake_ohlc", py_fake_ohlc, raising=False)

    assert isinstance(acc.fake_list(), pd.Series)
    assert isinstance(acc.fake_tuple(), tuple)
    assert all(isinstance(v, pd.Series) for v in acc.fake_tuple())
    assert isinstance(acc.fake_dict(), dict)
    assert isinstance(acc.fake_dict()["alpha"], pd.Series)

    assert acc.fake_scalar() == 42.0
    _ = acc.fake_extra()
    _ = acc.fake_ohlc()

    _ = acc.fake_list()

    with pytest.raises(AttributeError):
        _ = acc._private
    with pytest.raises(AttributeError):
        _ = acc.unknown_indicator


def test_accessor_required_methods() -> None:
    df = _build_df()
    acc = TechnicalAnalysisAccessor(df)

    crossover = acc.crossover(df["close"], df["open"])
    crossunder = acc.crossunder(df["close"], df["open"])
    assert len(crossover) == len(df)
    assert len(crossunder) == len(df)


def test_accessor_all_methods_smoke() -> None:
    df = _build_df()
    acc = TechnicalAnalysisAccessor(df)

    skip_names = {"crossover", "crossunder", "frame", "clear_frame_cache", "index"}
    for name in dir(TechnicalAnalysisAccessor):
        if name.startswith("_") or name in skip_names:
            continue
        attr = getattr(acc, name)
        if not callable(attr):
            continue
        try:
            attr()
        except Exception:
            pass


def test_accessor_frame_fallbacks(monkeypatch: pytest.MonkeyPatch) -> None:
    df = _build_df()
    acc = TechnicalAnalysisAccessor(df)

    class DummyFrame:
        pass

    monkeypatch.setattr(acc, "frame", lambda refresh=False: DummyFrame())

    _ = acc.sma()
    _ = acc.ema()
    _ = acc.wma()
    _ = acc.hma()
    _ = acc.atr()
    _ = acc.true_range()
    _ = acc.bollinger_bands()
    _ = acc.rsi()
    _ = acc.macd()
    _ = acc.stochastic()
    _ = acc.cci()
    _ = acc.williams_r()
    _ = acc.supertrend()
    _ = acc.adx()
    _ = acc.obv()
    _ = acc.vwap()
    _ = acc.mfi()


def test_heikin_ashi_empty_dataframe() -> None:
    df = _build_df(0)
    acc = TechnicalAnalysisAccessor(df)
    ha_open, ha_high, ha_low, ha_close = acc.heikin_ashi()
    assert ha_open.empty and ha_high.empty and ha_low.empty and ha_close.empty


def test_series_accessor_methods() -> None:
    df = _build_df()
    series_acc = SeriesTechnicalAnalysisAccessor(df["close"])

    for name in dir(SeriesTechnicalAnalysisAccessor):
        if name.startswith("_") or name == "index":
            continue
        attr = getattr(series_acc, name)
        if not callable(attr):
            continue
        try:
            attr()
        except Exception:
            pass


def test_register_pandas_accessors_idempotent() -> None:
    original_df = acc_mod.pd.api.extensions.register_dataframe_accessor
    original_series = acc_mod.pd.api.extensions.register_series_accessor

    def raise_value_error(_name):
        def _decorator(_cls):
            raise ValueError("already registered")

        return _decorator

    acc_mod.pd.api.extensions.register_dataframe_accessor = raise_value_error
    acc_mod.pd.api.extensions.register_series_accessor = raise_value_error
    try:
        acc_mod._register_pandas_accessors()
    finally:
        acc_mod.pd.api.extensions.register_dataframe_accessor = original_df
        acc_mod.pd.api.extensions.register_series_accessor = original_series


def test_accessor_import_fallback(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test import fallback when haze_library is not available."""
    import importlib
    import sys
    import haze_library as hl

    original_ext = sys.modules.get("haze_library.haze_library")
    sys.modules["haze_library.haze_library"] = None
    monkeypatch.delattr(hl, "haze_library", raising=False)

    importlib.reload(acc_mod)
    assert acc_mod._lib is hl

    if original_ext is not None:
        sys.modules["haze_library.haze_library"] = original_ext
        hl.haze_library = original_ext
    else:
        sys.modules.pop("haze_library.haze_library", None)
    importlib.reload(acc_mod)
