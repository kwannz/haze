"""
Haze-Library: High-Performance Quantitative Trading Indicators
==============================================================

Rust-powered technical indicators for Python with 200+ indicators.

Usage:
------
    # Direct function calls
    from haze_library import py_sma, py_rsi, py_macd

    sma = py_sma(close_prices, 20)
    rsi = py_rsi(close_prices, 14)

    # DataFrame accessor (recommended)
    import pandas as pd
    import haze_library

    df = pd.read_csv('ohlcv.csv')
    df['sma_20'] = df.haze.sma(20)
    df['rsi_14'] = df.haze.rsi(14)
    upper, middle, lower = df.haze.bollinger_bands(20, 2.0)

    # Series accessor
    df['close'].haze.sma(20)
    df['close'].haze.rsi(14)

Performance:
-----------
    - 5-10x faster than pure Python implementations
    - 4.8-6.3x faster than TA-Lib for most indicators
    - High numerical precision using f64
"""

__version__ = "0.1.0"
__author__ = "kwannz"

import inspect
from typing import Any, Callable, Dict

# Import Rust extension
try:
    from .haze_library import *
except ImportError:
    import warnings
    warnings.warn(
        "Could not import Rust extension module. "
        "Please ensure the package is properly installed."
    )

# -----------------------------------------------------------------------------
# Clean API aliases (no `py_` prefix)
# -----------------------------------------------------------------------------

_KW_ALIASES: Dict[str, str] = {
    "close": "values",
    "std_dev": "std_multiplier",
    "fast": "fast_period",
    "slow": "slow_period",
    "signal": "signal_period",
    "long": "long_period",
    "short": "short_period",
}


def _make_clean_wrapper(py_func: Callable[..., Any], *, clean_name: str) -> Callable[..., Any]:
    signature = inspect.signature(py_func)
    parameter_names = set(signature.parameters)

    def wrapper(*args: Any, **kwargs: Any) -> Any:
        for alias_name, real_name in _KW_ALIASES.items():
            if (
                alias_name in kwargs
                and alias_name not in parameter_names
                and real_name in parameter_names
                and real_name not in kwargs
            ):
                kwargs[real_name] = kwargs.pop(alias_name)
        return py_func(*args, **kwargs)

    wrapper.__name__ = clean_name
    wrapper.__qualname__ = clean_name
    wrapper.__doc__ = getattr(py_func, "__doc__", None)
    return wrapper


def _install_clean_api_aliases() -> Dict[str, str]:
    mapping: Dict[str, str] = {}

    for name, obj in list(globals().items()):
        if not name.startswith("py_"):
            continue

        clean_name = name[3:]
        if clean_name in globals():
            mapping[name] = clean_name
            continue

        if callable(obj):
            globals()[clean_name] = _make_clean_wrapper(obj, clean_name=clean_name)
        else:
            globals()[clean_name] = obj
        mapping[name] = clean_name

    return mapping


# Mapping from legacy `py_*` function names to clean names. Used for tooling/tests.
_PY_PREFIX_ALIASES = _install_clean_api_aliases()

# Register pandas accessor
try:
    from . import accessor
    from .accessor import TechnicalAnalysisAccessor, SeriesTechnicalAnalysisAccessor
except ImportError:
    # pandas not available
    TechnicalAnalysisAccessor = None
    SeriesTechnicalAnalysisAccessor = None

# NumPy compatibility layer (no-prefix functions returning np.ndarray)
try:
    from . import numpy_compat as np_ta
except ImportError:
    np_ta = None

# Convenience re-exports for common indicators
__all__ = [
    # Version
    "__version__",
    # Accessors
    "TechnicalAnalysisAccessor",
    "SeriesTechnicalAnalysisAccessor",
    # NumPy module
    "np_ta",
]
