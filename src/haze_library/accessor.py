"""
Haze-Library Pandas DataFrame Accessor
======================================

Provides a Pythonic `.haze` accessor for pandas DataFrames.

Usage:
    import pandas as pd
    import haze_library

    df = pd.read_csv('ohlcv.csv')

    # Using accessor
    df['sma_20'] = df.haze.sma(20)
    df['rsi_14'] = df.haze.rsi(14)
    upper, middle, lower = df.haze.bollinger_bands(20, 2.0)

    # Chain with pandas
    df.haze.macd().assign(signal=lambda x: x[1])
"""

from __future__ import annotations

import pandas as pd
import numpy as np
from typing import Optional, Union, Tuple, List, Any

# Import Rust extension
try:
    from . import haze_library as _lib
except ImportError:
    import haze_library as _lib


def _to_list(data: Union[pd.Series, np.ndarray, List[float]]) -> List[float]:
    """Convert various input types to Python list."""
    if isinstance(data, pd.Series):
        return data.tolist()
    elif isinstance(data, np.ndarray):
        return data.tolist()
    return list(data)


def _to_series(data: List[float], index: pd.Index) -> pd.Series:
    """Convert result list to pandas Series with proper index."""
    return pd.Series(data, index=index)


def _normalize_column_name(name: str) -> str:
    """Normalize column name to lowercase."""
    return str(name).lower().strip()


class TechnicalAnalysisAccessor:
    """
    Technical Analysis accessor for pandas DataFrames.

    Provides easy access to 200+ technical indicators.

    Example:
        >>> df.haze.sma(20)
        >>> df.haze.rsi(14)
        >>> df.haze.macd(12, 26, 9)
    """

    def __init__(self, pandas_obj: pd.DataFrame):
        self._obj = pandas_obj
        self._cache_columns()

    def _cache_columns(self):
        """Cache normalized column name mappings."""
        self._col_map = {}
        for col in self._obj.columns:
            normalized = _normalize_column_name(col)
            self._col_map[normalized] = col

    def _get_column(self, name: str) -> pd.Series:
        """Get column by normalized name."""
        normalized = _normalize_column_name(name)

        # Try exact match first
        if normalized in self._col_map:
            return self._obj[self._col_map[normalized]]

        # Try common aliases
        aliases = {
            'close': ['close', 'c', 'adj close', 'adj_close', 'adjclose', 'price'],
            'open': ['open', 'o'],
            'high': ['high', 'h', 'hi'],
            'low': ['low', 'l', 'lo'],
            'volume': ['volume', 'vol', 'v'],
        }

        if normalized in aliases:
            for alias in aliases[normalized]:
                if alias in self._col_map:
                    return self._obj[self._col_map[alias]]

        raise KeyError(f"Column '{name}' not found. Available: {list(self._obj.columns)}")

    def _get_ohlc(self) -> Tuple[List[float], List[float], List[float], List[float]]:
        """Get OHLC data as lists."""
        return (
            _to_list(self._get_column('open')),
            _to_list(self._get_column('high')),
            _to_list(self._get_column('low')),
            _to_list(self._get_column('close')),
        )

    def _get_hlc(self) -> Tuple[List[float], List[float], List[float]]:
        """Get HLC data as lists."""
        return (
            _to_list(self._get_column('high')),
            _to_list(self._get_column('low')),
            _to_list(self._get_column('close')),
        )

    @property
    def index(self) -> pd.Index:
        """Get DataFrame index."""
        return self._obj.index

    # ==================== Moving Averages ====================

    def sma(self, period: int = 20, column: str = 'close') -> pd.Series:
        """Simple Moving Average."""
        data = _to_list(self._get_column(column))
        result = _lib.py_sma(data, period)
        return _to_series(result, self.index)

    def ema(self, period: int = 20, column: str = 'close') -> pd.Series:
        """Exponential Moving Average."""
        data = _to_list(self._get_column(column))
        result = _lib.py_ema(data, period)
        return _to_series(result, self.index)

    def rma(self, period: int = 14, column: str = 'close') -> pd.Series:
        """Wilder's Moving Average (RMA)."""
        data = _to_list(self._get_column(column))
        result = _lib.py_rma(data, period)
        return _to_series(result, self.index)

    def wma(self, period: int = 20, column: str = 'close') -> pd.Series:
        """Weighted Moving Average."""
        data = _to_list(self._get_column(column))
        result = _lib.py_wma(data, period)
        return _to_series(result, self.index)

    def hma(self, period: int = 20, column: str = 'close') -> pd.Series:
        """Hull Moving Average."""
        data = _to_list(self._get_column(column))
        result = _lib.py_hma(data, period)
        return _to_series(result, self.index)

    def dema(self, period: int = 20, column: str = 'close') -> pd.Series:
        """Double Exponential Moving Average."""
        data = _to_list(self._get_column(column))
        result = _lib.py_dema(data, period)
        return _to_series(result, self.index)

    def tema(self, period: int = 20, column: str = 'close') -> pd.Series:
        """Triple Exponential Moving Average."""
        data = _to_list(self._get_column(column))
        result = _lib.py_tema(data, period)
        return _to_series(result, self.index)

    def zlma(self, period: int = 20, column: str = 'close') -> pd.Series:
        """Zero Lag Moving Average."""
        data = _to_list(self._get_column(column))
        result = _lib.py_zlma(data, period)
        return _to_series(result, self.index)

    def kama(self, period: int = 10, fast: int = 2, slow: int = 30,
             column: str = 'close') -> pd.Series:
        """Kaufman's Adaptive Moving Average."""
        data = _to_list(self._get_column(column))
        result = _lib.py_kama(data, period, fast, slow)
        return _to_series(result, self.index)

    def t3(self, period: int = 5, v_factor: float = 0.7,
           column: str = 'close') -> pd.Series:
        """T3 Moving Average."""
        data = _to_list(self._get_column(column))
        result = _lib.py_t3(data, period, v_factor)
        return _to_series(result, self.index)

    def alma(self, period: int = 9, offset: float = 0.85, sigma: float = 6.0,
             column: str = 'close') -> pd.Series:
        """Arnaud Legoux Moving Average."""
        data = _to_list(self._get_column(column))
        result = _lib.py_alma(data, period, offset, sigma)
        return _to_series(result, self.index)

    def frama(self, period: int = 10, column: str = 'close') -> pd.Series:
        """Fractal Adaptive Moving Average."""
        data = _to_list(self._get_column(column))
        result = _lib.py_frama(data, period)
        return _to_series(result, self.index)

    def trima(self, period: int = 20, column: str = 'close') -> pd.Series:
        """Triangular Moving Average."""
        data = _to_list(self._get_column(column))
        result = _lib.py_trima(data, period)
        return _to_series(result, self.index)

    def vidya(self, period: int = 14, column: str = 'close') -> pd.Series:
        """Variable Index Dynamic Average."""
        data = _to_list(self._get_column(column))
        result = _lib.py_vidya(data, period)
        return _to_series(result, self.index)

    # ==================== Volatility Indicators ====================

    def atr(self, period: int = 14) -> pd.Series:
        """Average True Range."""
        high, low, close = self._get_hlc()
        result = _lib.py_atr(high, low, close, period)
        return _to_series(result, self.index)

    def natr(self, period: int = 14) -> pd.Series:
        """Normalized Average True Range (percentage)."""
        high, low, close = self._get_hlc()
        result = _lib.py_natr(high, low, close, period)
        return _to_series(result, self.index)

    def true_range(self, drift: int = 1) -> pd.Series:
        """True Range."""
        high, low, close = self._get_hlc()
        result = _lib.py_true_range(high, low, close, drift)
        return _to_series(result, self.index)

    def bollinger_bands(self, period: int = 20, std: float = 2.0,
                        column: str = 'close') -> Tuple[pd.Series, pd.Series, pd.Series]:
        """Bollinger Bands. Returns (upper, middle, lower)."""
        data = _to_list(self._get_column(column))
        upper, middle, lower = _lib.py_bollinger_bands(data, period, std)
        return (
            _to_series(upper, self.index),
            _to_series(middle, self.index),
            _to_series(lower, self.index),
        )

    def keltner_channel(self, period: int = 20, atr_period: int = 10,
                        multiplier: float = 2.0) -> Tuple[pd.Series, pd.Series, pd.Series]:
        """Keltner Channel. Returns (upper, middle, lower)."""
        high, low, close = self._get_hlc()
        upper, middle, lower = _lib.py_keltner_channel(
            high, low, close, period, atr_period, multiplier
        )
        return (
            _to_series(upper, self.index),
            _to_series(middle, self.index),
            _to_series(lower, self.index),
        )

    def donchian_channel(self, period: int = 20) -> Tuple[pd.Series, pd.Series, pd.Series]:
        """Donchian Channel. Returns (upper, middle, lower)."""
        high = _to_list(self._get_column('high'))
        low = _to_list(self._get_column('low'))
        upper, middle, lower = _lib.py_donchian_channel(high, low, period)
        return (
            _to_series(upper, self.index),
            _to_series(middle, self.index),
            _to_series(lower, self.index),
        )

    # ==================== Momentum Indicators ====================

    def rsi(self, period: int = 14, column: str = 'close') -> pd.Series:
        """Relative Strength Index."""
        data = _to_list(self._get_column(column))
        result = _lib.py_rsi(data, period)
        return _to_series(result, self.index)

    def macd(self, fast: int = 12, slow: int = 26,
             signal: int = 9, column: str = 'close') -> Tuple[pd.Series, pd.Series, pd.Series]:
        """MACD. Returns (macd_line, signal_line, histogram)."""
        data = _to_list(self._get_column(column))
        macd_line, signal_line, histogram = _lib.py_macd(data, fast, slow, signal)
        return (
            _to_series(macd_line, self.index),
            _to_series(signal_line, self.index),
            _to_series(histogram, self.index),
        )

    def stochastic(self, k_period: int = 14, d_period: int = 3,
                   smooth_k: int = 3) -> Tuple[pd.Series, pd.Series]:
        """Stochastic Oscillator. Returns (%K, %D)."""
        high, low, close = self._get_hlc()
        k, d = _lib.py_stochastic(high, low, close, k_period, d_period)
        return _to_series(k, self.index), _to_series(d, self.index)

    def stochrsi(self, period: int = 14, k_period: int = 3, d_period: int = 3,
                 column: str = 'close') -> Tuple[pd.Series, pd.Series]:
        """Stochastic RSI. Returns (%K, %D)."""
        data = _to_list(self._get_column(column))
        k, d = _lib.py_stochrsi(data, period, period, k_period, d_period)
        return _to_series(k, self.index), _to_series(d, self.index)

    def cci(self, period: int = 20) -> pd.Series:
        """Commodity Channel Index."""
        high, low, close = self._get_hlc()
        result = _lib.py_cci(high, low, close, period)
        return _to_series(result, self.index)

    def williams_r(self, period: int = 14) -> pd.Series:
        """Williams %R."""
        high, low, close = self._get_hlc()
        result = _lib.py_williams_r(high, low, close, period)
        return _to_series(result, self.index)

    def awesome_oscillator(self, fast: int = 5, slow: int = 34) -> pd.Series:
        """Awesome Oscillator."""
        high = _to_list(self._get_column('high'))
        low = _to_list(self._get_column('low'))
        result = _lib.py_awesome_oscillator(high, low, fast, slow)
        return _to_series(result, self.index)

    def fisher_transform(self, period: int = 9) -> Tuple[pd.Series, pd.Series]:
        """Fisher Transform. Returns (fisher, signal)."""
        high, low, close = self._get_hlc()
        fisher, signal = _lib.py_fisher_transform(high, low, close, period)
        return _to_series(fisher, self.index), _to_series(signal, self.index)

    def kdj(self, k_period: int = 9, d_period: int = 3,
            j_period: int = 3) -> Tuple[pd.Series, pd.Series, pd.Series]:
        """KDJ Indicator. Returns (K, D, J)."""
        high, low, close = self._get_hlc()
        k, d, j = _lib.py_kdj(high, low, close, k_period, d_period)
        return (
            _to_series(k, self.index),
            _to_series(d, self.index),
            _to_series(j, self.index),
        )

    def tsi(self, fast: int = 13, slow: int = 25, signal: int = 13,
            column: str = 'close') -> Tuple[pd.Series, pd.Series]:
        """True Strength Index. Returns (tsi, signal)."""
        data = _to_list(self._get_column(column))
        tsi, signal_line = _lib.py_tsi(data, slow, fast, signal)
        return _to_series(tsi, self.index), _to_series(signal_line, self.index)

    def ultimate_oscillator(self, short: int = 7, medium: int = 14,
                           long: int = 28) -> pd.Series:
        """Ultimate Oscillator."""
        high, low, close = self._get_hlc()
        result = _lib.py_ultimate_oscillator(high, low, close, short, medium, long)
        return _to_series(result, self.index)

    def mom(self, period: int = 10, column: str = 'close') -> pd.Series:
        """Momentum."""
        data = _to_list(self._get_column(column))
        result = _lib.py_mom(data, period)
        return _to_series(result, self.index)

    def roc(self, period: int = 10, column: str = 'close') -> pd.Series:
        """Rate of Change (percentage)."""
        data = _to_list(self._get_column(column))
        result = _lib.py_roc(data, period)
        return _to_series(result, self.index)

    def cmo(self, period: int = 14, column: str = 'close') -> pd.Series:
        """Chande Momentum Oscillator."""
        data = _to_list(self._get_column(column))
        result = _lib.py_cmo(data, period)
        return _to_series(result, self.index)

    def apo(self, fast: int = 12, slow: int = 26,
            column: str = 'close') -> pd.Series:
        """Absolute Price Oscillator."""
        data = _to_list(self._get_column(column))
        result = _lib.py_apo(data, fast, slow)
        return _to_series(result, self.index)

    def ppo(self, fast: int = 12, slow: int = 26,
            column: str = 'close') -> pd.Series:
        """Percentage Price Oscillator."""
        data = _to_list(self._get_column(column))
        result = _lib.py_ppo(data, fast, slow)
        return _to_series(result, self.index)

    # ==================== Trend Indicators ====================

    def supertrend(self, period: int = 10, multiplier: float = 3.0
                   ) -> Tuple[pd.Series, pd.Series, pd.Series, pd.Series]:
        """SuperTrend. Returns (supertrend, direction, upper_band, lower_band)."""
        high, low, close = self._get_hlc()
        st, direction, upper, lower = _lib.py_supertrend(high, low, close, period, multiplier)
        return (
            _to_series(st, self.index),
            _to_series(direction, self.index),
            _to_series(upper, self.index),
            _to_series(lower, self.index),
        )

    def adx(self, period: int = 14) -> Tuple[pd.Series, pd.Series, pd.Series]:
        """Average Directional Index. Returns (adx, plus_di, minus_di)."""
        high, low, close = self._get_hlc()
        adx_val, plus_di, minus_di = _lib.py_adx(high, low, close, period)
        return (
            _to_series(adx_val, self.index),
            _to_series(plus_di, self.index),
            _to_series(minus_di, self.index),
        )

    def aroon(self, period: int = 25) -> Tuple[pd.Series, pd.Series, pd.Series]:
        """Aroon. Returns (aroon_up, aroon_down, oscillator)."""
        high = _to_list(self._get_column('high'))
        low = _to_list(self._get_column('low'))
        up, down, osc = _lib.py_aroon(high, low, period)
        return (
            _to_series(up, self.index),
            _to_series(down, self.index),
            _to_series(osc, self.index),
        )

    def psar(self, af_start: float = 0.02, af_increment: float = 0.02,
             af_max: float = 0.2) -> Tuple[pd.Series, pd.Series]:
        """Parabolic SAR. Returns (sar, direction)."""
        high = _to_list(self._get_column('high'))
        low = _to_list(self._get_column('low'))
        close = _to_list(self._get_column('close'))
        sar, direction = _lib.py_psar(high, low, close, af_start, af_increment, af_max)
        return _to_series(sar, self.index), _to_series(direction, self.index)

    def vortex(self, period: int = 14) -> Tuple[pd.Series, pd.Series]:
        """Vortex Indicator. Returns (VI+, VI-)."""
        high, low, close = self._get_hlc()
        vi_plus, vi_minus = _lib.py_vortex(high, low, close, period)
        return _to_series(vi_plus, self.index), _to_series(vi_minus, self.index)

    def choppiness(self, period: int = 14) -> pd.Series:
        """Choppiness Index."""
        high, low, close = self._get_hlc()
        result = _lib.py_choppiness(high, low, close, period)
        return _to_series(result, self.index)

    def dx(self, period: int = 14) -> pd.Series:
        """Directional Movement Index."""
        high, low, close = self._get_hlc()
        result = _lib.py_dx(high, low, close, period)
        return _to_series(result, self.index)

    def plus_di(self, period: int = 14) -> pd.Series:
        """Plus Directional Indicator (+DI)."""
        high, low, close = self._get_hlc()
        result = _lib.py_plus_di(high, low, close, period)
        return _to_series(result, self.index)

    def minus_di(self, period: int = 14) -> pd.Series:
        """Minus Directional Indicator (-DI)."""
        high, low, close = self._get_hlc()
        result = _lib.py_minus_di(high, low, close, period)
        return _to_series(result, self.index)

    # ==================== Volume Indicators ====================

    def obv(self) -> pd.Series:
        """On Balance Volume."""
        close = _to_list(self._get_column('close'))
        volume = _to_list(self._get_column('volume'))
        result = _lib.py_obv(close, volume)
        return _to_series(result, self.index)

    def vwap(self) -> pd.Series:
        """Volume Weighted Average Price."""
        high, low, close = self._get_hlc()
        volume = _to_list(self._get_column('volume'))
        result = _lib.py_vwap(high, low, close, volume)
        return _to_series(result, self.index)

    def mfi(self, period: int = 14) -> pd.Series:
        """Money Flow Index."""
        high, low, close = self._get_hlc()
        volume = _to_list(self._get_column('volume'))
        result = _lib.py_mfi(high, low, close, volume, period)
        return _to_series(result, self.index)

    def cmf(self, period: int = 20) -> pd.Series:
        """Chaikin Money Flow."""
        high, low, close = self._get_hlc()
        volume = _to_list(self._get_column('volume'))
        result = _lib.py_cmf(high, low, close, volume, period)
        return _to_series(result, self.index)

    def ad(self) -> pd.Series:
        """Accumulation/Distribution Line."""
        high, low, close = self._get_hlc()
        volume = _to_list(self._get_column('volume'))
        result = _lib.py_ad(high, low, close, volume)
        return _to_series(result, self.index)

    def adosc(self, fast: int = 3, slow: int = 10) -> pd.Series:
        """Accumulation/Distribution Oscillator."""
        high, low, close = self._get_hlc()
        volume = _to_list(self._get_column('volume'))
        result = _lib.py_adosc(high, low, close, volume, fast, slow)
        return _to_series(result, self.index)

    def pvt(self) -> pd.Series:
        """Price Volume Trend."""
        close = _to_list(self._get_column('close'))
        volume = _to_list(self._get_column('volume'))
        result = _lib.py_pvt(close, volume)
        return _to_series(result, self.index)

    def nvi(self) -> pd.Series:
        """Negative Volume Index."""
        close = _to_list(self._get_column('close'))
        volume = _to_list(self._get_column('volume'))
        result = _lib.py_nvi(close, volume)
        return _to_series(result, self.index)

    def pvi(self) -> pd.Series:
        """Positive Volume Index."""
        close = _to_list(self._get_column('close'))
        volume = _to_list(self._get_column('volume'))
        result = _lib.py_pvi(close, volume)
        return _to_series(result, self.index)

    def eom(self, period: int = 14) -> pd.Series:
        """Ease of Movement."""
        high = _to_list(self._get_column('high'))
        low = _to_list(self._get_column('low'))
        volume = _to_list(self._get_column('volume'))
        result = _lib.py_eom(high, low, volume, period)
        return _to_series(result, self.index)

    # ==================== Statistical Indicators ====================

    def variance(self, period: int = 20, column: str = 'close') -> pd.Series:
        """Rolling Variance."""
        data = _to_list(self._get_column(column))
        result = _lib.py_var(data, period)
        return _to_series(result, self.index)

    def stddev(self, period: int = 20, column: str = 'close') -> pd.Series:
        """Rolling Standard Deviation."""
        data = _to_list(self._get_column(column))
        var = np.array(_lib.py_var(data, period), dtype=np.float64)
        std = np.sqrt(np.clip(var, 0.0, None)).tolist()
        return _to_series(std, self.index)

    def zscore(self, period: int = 20, column: str = 'close') -> pd.Series:
        """Rolling Z-Score."""
        data = _to_list(self._get_column(column))
        result = _lib.py_zscore(data, period)
        return _to_series(result, self.index)

    def linear_regression(self, period: int = 14,
                         column: str = 'close') -> pd.Series:
        """Linear Regression Value."""
        data = _to_list(self._get_column(column))
        result = _lib.py_linearreg(data, period)
        return _to_series(result, self.index)

    def linreg_slope(self, period: int = 14, column: str = 'close') -> pd.Series:
        """Linear Regression Slope."""
        data = _to_list(self._get_column(column))
        result = _lib.py_linearreg_slope(data, period)
        return _to_series(result, self.index)

    def linreg_angle(self, period: int = 14, column: str = 'close') -> pd.Series:
        """Linear Regression Angle (degrees)."""
        data = _to_list(self._get_column(column))
        result = _lib.py_linearreg_angle(data, period)
        return _to_series(result, self.index)

    def linreg_intercept(self, period: int = 14, column: str = 'close') -> pd.Series:
        """Linear Regression Intercept."""
        data = _to_list(self._get_column(column))
        result = _lib.py_linearreg_intercept(data, period)
        return _to_series(result, self.index)

    # ==================== Candlestick Patterns ====================

    def heikin_ashi(self) -> Tuple[pd.Series, pd.Series, pd.Series, pd.Series]:
        """Heikin Ashi candles. Returns (ha_open, ha_high, ha_low, ha_close)."""
        open_, high, low, close = self._get_ohlc()
        ha_o, ha_h, ha_l, ha_c = _lib.py_heikin_ashi(open_, high, low, close)
        return (
            _to_series(ha_o, self.index),
            _to_series(ha_h, self.index),
            _to_series(ha_l, self.index),
            _to_series(ha_c, self.index),
        )

    def doji(self, threshold: float = 0.1) -> pd.Series:
        """Doji pattern detection."""
        open_, high, low, close = self._get_ohlc()
        result = _lib.py_doji(open_, high, low, close, threshold)
        return _to_series(result, self.index)

    def hammer(self) -> pd.Series:
        """Hammer pattern detection."""
        open_, high, low, close = self._get_ohlc()
        result = _lib.py_hammer(open_, high, low, close)
        return _to_series(result, self.index)

    def engulfing(self) -> pd.Series:
        """Engulfing pattern detection."""
        open_, high, low, close = self._get_ohlc()
        result = _lib.py_engulfing(open_, high, low, close)
        return _to_series(result, self.index)

    def morning_star(self) -> pd.Series:
        """Morning Star pattern detection."""
        open_, high, low, close = self._get_ohlc()
        result = _lib.py_morning_star(open_, high, low, close)
        return _to_series(result, self.index)

    def evening_star(self) -> pd.Series:
        """Evening Star pattern detection."""
        open_, high, low, close = self._get_ohlc()
        result = _lib.py_evening_star(open_, high, low, close)
        return _to_series(result, self.index)

    # ==================== Utility Methods ====================

    def crossover(self, series1: pd.Series, series2: pd.Series) -> pd.Series:
        """Detect crossover (series1 crosses above series2)."""
        s1 = _to_list(series1)
        s2 = _to_list(series2)
        result = _lib.py_crossover(s1, s2)
        return _to_series(result, series1.index)

    def crossunder(self, series1: pd.Series, series2: pd.Series) -> pd.Series:
        """Detect crossunder (series1 crosses below series2)."""
        s1 = _to_list(series1)
        s2 = _to_list(series2)
        result = _lib.py_crossunder(s1, s2)
        return _to_series(result, series1.index)

    def highest(self, period: int = 14, column: str = 'high') -> pd.Series:
        """Rolling highest value."""
        data = _to_list(self._get_column(column))
        result = _lib.py_highest(data, period)
        return _to_series(result, self.index)

    def lowest(self, period: int = 14, column: str = 'low') -> pd.Series:
        """Rolling lowest value."""
        data = _to_list(self._get_column(column))
        result = _lib.py_lowest(data, period)
        return _to_series(result, self.index)

    def percent_rank(self, period: int = 20, column: str = 'close') -> pd.Series:
        """Percent Rank."""
        data = _to_list(self._get_column(column))
        result = _lib.py_percent_rank(data, period)
        return _to_series(result, self.index)


class SeriesTechnicalAnalysisAccessor:
    """
    Technical Analysis accessor for pandas Series.

    Example:
        >>> close_series.haze.sma(20)
        >>> close_series.haze.ema(12)
    """

    def __init__(self, pandas_obj: pd.Series):
        self._obj = pandas_obj

    @property
    def index(self) -> pd.Index:
        return self._obj.index

    def _to_list(self) -> List[float]:
        return self._obj.tolist()

    # Moving Averages
    def sma(self, period: int = 20) -> pd.Series:
        """Simple Moving Average."""
        result = _lib.py_sma(self._to_list(), period)
        return _to_series(result, self.index)

    def ema(self, period: int = 20) -> pd.Series:
        """Exponential Moving Average."""
        result = _lib.py_ema(self._to_list(), period)
        return _to_series(result, self.index)

    def rma(self, period: int = 14) -> pd.Series:
        """Wilder's Moving Average."""
        result = _lib.py_rma(self._to_list(), period)
        return _to_series(result, self.index)

    def wma(self, period: int = 20) -> pd.Series:
        """Weighted Moving Average."""
        result = _lib.py_wma(self._to_list(), period)
        return _to_series(result, self.index)

    def hma(self, period: int = 20) -> pd.Series:
        """Hull Moving Average."""
        result = _lib.py_hma(self._to_list(), period)
        return _to_series(result, self.index)

    def dema(self, period: int = 20) -> pd.Series:
        """Double Exponential Moving Average."""
        result = _lib.py_dema(self._to_list(), period)
        return _to_series(result, self.index)

    def tema(self, period: int = 20) -> pd.Series:
        """Triple Exponential Moving Average."""
        result = _lib.py_tema(self._to_list(), period)
        return _to_series(result, self.index)

    # Momentum
    def rsi(self, period: int = 14) -> pd.Series:
        """Relative Strength Index."""
        result = _lib.py_rsi(self._to_list(), period)
        return _to_series(result, self.index)

    def mom(self, period: int = 10) -> pd.Series:
        """Momentum."""
        result = _lib.py_mom(self._to_list(), period)
        return _to_series(result, self.index)

    def roc(self, period: int = 10) -> pd.Series:
        """Rate of Change."""
        result = _lib.py_roc(self._to_list(), period)
        return _to_series(result, self.index)

    def cmo(self, period: int = 14) -> pd.Series:
        """Chande Momentum Oscillator."""
        result = _lib.py_cmo(self._to_list(), period)
        return _to_series(result, self.index)

    # Statistical
    def stddev(self, period: int = 20) -> pd.Series:
        """Standard Deviation."""
        var = np.array(_lib.py_var(self._to_list(), period), dtype=np.float64)
        std = np.sqrt(np.clip(var, 0.0, None)).tolist()
        return _to_series(std, self.index)

    def variance(self, period: int = 20) -> pd.Series:
        """Variance."""
        result = _lib.py_var(self._to_list(), period)
        return _to_series(result, self.index)

    def zscore(self, period: int = 20) -> pd.Series:
        """Z-Score."""
        result = _lib.py_zscore(self._to_list(), period)
        return _to_series(result, self.index)

    def linear_regression(self, period: int = 14) -> pd.Series:
        """Linear Regression."""
        result = _lib.py_linearreg(self._to_list(), period)
        return _to_series(result, self.index)


def _register_pandas_accessors() -> None:
    """Register DataFrame/Series accessors with a safe fallback name.

    `.ta` is commonly used by third-party libraries (e.g. pandas-ta). To avoid
    breaking imports in those environments, we always register `.haze` and only
    register `.ta` when it is available.
    """

    for accessor_name in ("haze", "ta"):
        try:
            pd.api.extensions.register_dataframe_accessor(accessor_name)(
                TechnicalAnalysisAccessor
            )
        except ValueError:
            pass

        try:
            pd.api.extensions.register_series_accessor(accessor_name)(
                SeriesTechnicalAnalysisAccessor
            )
        except ValueError:
            pass


_register_pandas_accessors()
