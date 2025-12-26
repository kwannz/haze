"""
Haze: High-Performance Quantitative Trading Indicators
======================================================

Convenience alias for `haze_library`.

Usage:
------
    # Short import
    import haze
    df.haze.sma(20)  # stable accessor auto-registered

    # NumPy interface
    from haze import np_ta
    sma = np_ta.sma(close, 20)

    # Direct Rust functions (with py_ prefix)
    from haze import py_sma, py_rsi
    sma = py_sma(close_list, 20)
"""

from __future__ import annotations

import haze_library as _haze_library

__version__ = _haze_library.__version__
np_ta = _haze_library.np_ta

# DataFrame accessor is auto-registered on import
try:
    TechnicalAnalysisAccessor = _haze_library.TechnicalAnalysisAccessor
    SeriesTechnicalAnalysisAccessor = _haze_library.SeriesTechnicalAnalysisAccessor
except Exception:
    TechnicalAnalysisAccessor = None
    SeriesTechnicalAnalysisAccessor = None

def __getattr__(name: str):
    return getattr(_haze_library, name)


def __dir__():
    return sorted(set(globals()) | set(dir(_haze_library)))


__all__ = [name for name in dir(_haze_library) if not name.startswith("_")]
