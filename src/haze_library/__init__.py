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
    df['sma_20'] = df.ta.sma(20)
    df['rsi_14'] = df.ta.rsi(14)
    upper, middle, lower = df.ta.bollinger_bands(20, 2.0)

    # Series accessor
    df['close'].ta.sma(20)
    df['close'].ta.rsi(14)

Performance:
-----------
    - 5-10x faster than pure Python implementations
    - 4.8-6.3x faster than TA-Lib for most indicators
    - High numerical precision using f64
"""

__version__ = "0.1.0"
__author__ = "kwannz"

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

# Mapping from legacy `py_*` function names to clean names. This is used for
# backwards compatibility and for tooling/tests that verify the public API.
_PY_PREFIX_ALIASES = {
    # Moving averages / overlap
    "py_sma": "sma",
    "py_ema": "ema",
    # Momentum
    "py_rsi": "rsi",
    "py_macd": "macd",
    # Volatility
    "py_bollinger_bands": "bollinger_bands",
    "py_atr": "atr",
    # Trend
    "py_supertrend": "supertrend",
    "py_adx": "adx",
    # Volume
    "py_obv": "obv",
    "py_vwap": "vwap",
}

# Materialize the clean API names in the module namespace.
for _legacy_name, _clean_name in _PY_PREFIX_ALIASES.items():
    if _legacy_name in globals():
        globals()[_clean_name] = globals()[_legacy_name]

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
