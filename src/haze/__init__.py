"""
Haze: High-Performance Quantitative Trading Indicators
======================================================

Convenience alias for `haze_library`.

Usage:
------
    # Short import
    import haze
    df.ta.sma(20)  # pandas accessor auto-registered

    # NumPy interface
    from haze import np_ta
    sma = np_ta.sma(close, 20)

    # Direct Rust functions (with py_ prefix)
    from haze import py_sma, py_rsi
    sma = py_sma(close_list, 20)
"""

# Re-export everything from haze_library
from haze_library import *
from haze_library import __version__, np_ta

# DataFrame accessor is auto-registered on import
try:
    from haze_library import TechnicalAnalysisAccessor, SeriesTechnicalAnalysisAccessor
except ImportError:
    pass

__all__ = [
    "__version__",
    "np_ta",
    "TechnicalAnalysisAccessor",
    "SeriesTechnicalAnalysisAccessor",
]
