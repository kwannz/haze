"""
Haze-Library Type Stubs
=======================

High-performance quantitative trading technical indicators library.
Provides IDE auto-completion and type checking support.

This module exposes 268 technical indicators and utilities implemented in Rust via PyO3.
"""

from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union
from types import ModuleType

# ==================== Type Aliases ====================
FloatList = List[float]
IntList = List[int]
BoolList = List[bool]
ArrayLike = Union[List[float], Sequence[float]]

# ==================== Version Info ====================
__version__: str
__author__: str
__all__: List[str]

# ==================== Submodules ====================
accessor: ModuleType
ai_indicators: ModuleType
ai_ta: ModuleType
exceptions: ModuleType
haze_library: ModuleType
np_ta: ModuleType
numpy_compat: ModuleType
polars_accessor: ModuleType
polars_ta: ModuleType
stream_ta: ModuleType
streaming: ModuleType
torch_compat: ModuleType
torch_ta: ModuleType

# ==================== Classes ====================

class Candle:
    """OHLCV Candle data structure."""
    timestamp: int
    open: float
    high: float
    low: float
    close: float
    volume: float
    def __init__(self, timestamp: int, open: float, high: float, low: float, close: float, volume: float) -> None: ...
    def to_dict(self) -> Dict[str, float]: ...
    @property
    def typical_price(self) -> float: ...
    @property
    def median_price(self) -> float: ...
    @property
    def weighted_close(self) -> float: ...

class IndicatorResult:
    """Single indicator result container."""
    name: str
    values: FloatList
    metadata: Dict[str, str]
    def __init__(self, name: str, values: FloatList) -> None: ...
    def add_metadata(self, key: str, value: str) -> None: ...
    @property
    def len(self) -> int: ...

class MultiIndicatorResult:
    """Multiple indicator results container."""
    names: List[str]
    results: Dict[str, FloatList]
    def __init__(self, names: List[str]) -> None: ...
    def add_result(self, name: str, values: FloatList) -> None: ...
    def get(self, name: str) -> Optional[FloatList]: ...

class PyHarmonicPattern:
    """Harmonic pattern detection result."""
    pattern_type: str
    direction: str
    x_idx: int
    a_idx: int
    b_idx: int
    c_idx: int
    d_idx: int
    x_price: float
    a_price: float
    b_price: float
    c_price: float
    d_price: float
    completion_ratio: float
    potential_reversal_zone: Tuple[float, float]

# ==================== Error Classes ====================

class HazeError(Exception):
    """Base exception for Haze library errors."""
    ...

class InvalidParameterError(HazeError):
    """Raised when invalid parameters are provided."""
    ...

class InvalidPeriodError(HazeError):
    """Raised when an invalid period is specified."""
    ...

class InsufficientDataError(HazeError):
    """Raised when insufficient data is provided for calculation."""
    ...

class ComputationError(HazeError):
    """Raised when a computation fails."""
    ...

class ColumnNotFoundError(HazeError):
    """Raised when a required column is not found in DataFrame."""
    ...

# ==================== Incremental/Streaming Indicators ====================

class IncrementalIndicator:
    """Base class for incremental indicators."""
    def update(self, value: float) -> Optional[float]: ...
    def reset(self) -> None: ...
    @property
    def current_value(self) -> Optional[float]: ...

class IncrementalSMA(IncrementalIndicator):
    """Incremental Simple Moving Average."""
    def __init__(self, period: int) -> None: ...

class IncrementalEMA(IncrementalIndicator):
    """Incremental Exponential Moving Average."""
    def __init__(self, period: int) -> None: ...

class IncrementalRSI(IncrementalIndicator):
    """Incremental Relative Strength Index."""
    def __init__(self, period: int = 14) -> None: ...

class IncrementalMACD(IncrementalIndicator):
    """Incremental MACD."""
    def __init__(self, fast: int = 12, slow: int = 26, signal: int = 9) -> None: ...
    def update(self, value: float) -> Optional[Tuple[float, float, float]]: ...

class IncrementalATR(IncrementalIndicator):
    """Incremental Average True Range."""
    def __init__(self, period: int = 14) -> None: ...
    def update(self, high: float, low: float, close: float) -> Optional[float]: ...

class IncrementalBollingerBands(IncrementalIndicator):
    """Incremental Bollinger Bands."""
    def __init__(self, period: int = 20, std_dev: float = 2.0) -> None: ...
    def update(self, value: float) -> Optional[Tuple[float, float, float]]: ...

class IncrementalStochastic(IncrementalIndicator):
    """Incremental Stochastic Oscillator."""
    def __init__(self, k_period: int = 14, d_period: int = 3) -> None: ...
    def update(self, high: float, low: float, close: float) -> Optional[Tuple[float, float]]: ...

class IncrementalSuperTrend(IncrementalIndicator):
    """Incremental SuperTrend."""
    def __init__(self, period: int = 10, multiplier: float = 3.0) -> None: ...
    def update(self, high: float, low: float, close: float) -> Optional[Tuple[float, int]]: ...

class IncrementalAdaptiveRSI(IncrementalIndicator):
    """Incremental Adaptive RSI."""
    def __init__(self, period: int = 14) -> None: ...

class IncrementalEnsembleSignal(IncrementalIndicator):
    """Incremental Ensemble Signal."""
    def __init__(self) -> None: ...

class IncrementalMLSuperTrend(IncrementalIndicator):
    """Incremental ML-Enhanced SuperTrend."""
    def __init__(self, period: int = 10, multiplier: float = 3.0) -> None: ...

class CCXTStreamProcessor:
    """CCXT Stream Processor for real-time data."""
    def __init__(self) -> None: ...
    def process(self, data: Dict[str, Any]) -> Dict[str, Any]: ...

# ==================== Accessor Classes ====================

class TechnicalAnalysisAccessor:
    """DataFrame accessor for technical analysis."""
    def __init__(self, df: Any) -> None: ...
    def sma(self, period: int = 20) -> Any: ...
    def ema(self, period: int = 20) -> Any: ...
    def rsi(self, period: int = 14) -> Any: ...
    def macd(self, fast: int = 12, slow: int = 26, signal: int = 9) -> Tuple[Any, Any, Any]: ...
    def bollinger_bands(self, period: int = 20, std_dev: float = 2.0) -> Tuple[Any, Any, Any]: ...
    def atr(self, period: int = 14) -> Any: ...
    def supertrend(self, period: int = 10, multiplier: float = 3.0) -> Tuple[Any, Any]: ...
    # ... many more methods

class SeriesTechnicalAnalysisAccessor:
    """Series accessor for technical analysis."""
    def __init__(self, series: Any) -> None: ...
    def sma(self, period: int = 20) -> Any: ...
    def ema(self, period: int = 20) -> Any: ...
    def rsi(self, period: int = 14) -> Any: ...

# ==================== Moving Averages ====================

def sma(close: ArrayLike, period: int = 20) -> FloatList:
    """Simple Moving Average."""
    ...

def ema(close: ArrayLike, period: int = 20) -> FloatList:
    """Exponential Moving Average."""
    ...

def wma(close: ArrayLike, period: int = 20) -> FloatList:
    """Weighted Moving Average."""
    ...

def dema(close: ArrayLike, period: int = 20) -> FloatList:
    """Double Exponential Moving Average."""
    ...

def tema(close: ArrayLike, period: int = 20) -> FloatList:
    """Triple Exponential Moving Average."""
    ...

def trima(close: ArrayLike, period: int = 20) -> FloatList:
    """Triangular Moving Average."""
    ...

def kama(close: ArrayLike, period: int = 10, fast: int = 2, slow: int = 30) -> FloatList:
    """Kaufman Adaptive Moving Average."""
    ...

def zlma(close: ArrayLike, period: int = 20) -> FloatList:
    """Zero-Lag Moving Average."""
    ...

def hma(close: ArrayLike, period: int = 20) -> FloatList:
    """Hull Moving Average."""
    ...

def vwma(close: ArrayLike, volume: ArrayLike, period: int = 20) -> FloatList:
    """Volume Weighted Moving Average."""
    ...

def frama(close: ArrayLike, period: int = 16) -> FloatList:
    """Fractal Adaptive Moving Average."""
    ...

def alma(close: ArrayLike, period: int = 9, offset: float = 0.85, sigma: float = 6.0) -> FloatList:
    """Arnaud Legoux Moving Average."""
    ...

def t3(close: ArrayLike, period: int = 5, vfactor: float = 0.7) -> FloatList:
    """T3 Moving Average."""
    ...

def swma(close: ArrayLike) -> FloatList:
    """Symmetric Weighted Moving Average."""
    ...

def vidya(close: ArrayLike, period: int = 14, cmo_period: int = 9) -> FloatList:
    """Variable Index Dynamic Average."""
    ...

def rma(close: ArrayLike, period: int = 14) -> FloatList:
    """Running Moving Average (Wilder's Smoothing)."""
    ...

def sinwma(close: ArrayLike, period: int = 14) -> FloatList:
    """Sine Weighted Moving Average."""
    ...

def pwma(close: ArrayLike, period: int = 14) -> FloatList:
    """Pascal's Weighted Moving Average."""
    ...

def mama(close: ArrayLike, fast_limit: float = 0.5, slow_limit: float = 0.05) -> Tuple[FloatList, FloatList]:
    """MESA Adaptive Moving Average."""
    ...

# ==================== Momentum Indicators ====================

def rsi(close: ArrayLike, period: int = 14) -> FloatList:
    """Relative Strength Index."""
    ...

def stochrsi(close: ArrayLike, period: int = 14, stoch_period: int = 14, k_period: int = 3, d_period: int = 3) -> Tuple[FloatList, FloatList]:
    """Stochastic RSI."""
    ...

def stochastic(high: ArrayLike, low: ArrayLike, close: ArrayLike, k_period: int = 14, d_period: int = 3) -> Tuple[FloatList, FloatList]:
    """Stochastic Oscillator."""
    ...

def macd(close: ArrayLike, fast: int = 12, slow: int = 26, signal: int = 9) -> Tuple[FloatList, FloatList, FloatList]:
    """Moving Average Convergence Divergence."""
    ...

def mom(close: ArrayLike, period: int = 10) -> FloatList:
    """Momentum."""
    ...

def roc(close: ArrayLike, period: int = 10) -> FloatList:
    """Rate of Change."""
    ...

def ppo(close: ArrayLike, fast: int = 12, slow: int = 26, signal: int = 9) -> Tuple[FloatList, FloatList, FloatList]:
    """Percentage Price Oscillator."""
    ...

def cci(high: ArrayLike, low: ArrayLike, close: ArrayLike, period: int = 20) -> FloatList:
    """Commodity Channel Index."""
    ...

def williams_r(high: ArrayLike, low: ArrayLike, close: ArrayLike, period: int = 14) -> FloatList:
    """Williams %R."""
    ...

def cmf(high: ArrayLike, low: ArrayLike, close: ArrayLike, volume: ArrayLike, period: int = 20) -> FloatList:
    """Chaikin Money Flow."""
    ...

def ultimate_oscillator(high: ArrayLike, low: ArrayLike, close: ArrayLike, short: int = 7, medium: int = 14, long: int = 28) -> FloatList:
    """Ultimate Oscillator."""
    ...

def tsi(close: ArrayLike, long: int = 25, short: int = 13, signal: int = 13) -> Tuple[FloatList, FloatList]:
    """True Strength Index."""
    ...

def trix(close: ArrayLike, period: int = 15, signal: int = 9) -> Tuple[FloatList, FloatList]:
    """TRIX Indicator."""
    ...

def dpo(close: ArrayLike, period: int = 20) -> FloatList:
    """Detrended Price Oscillator."""
    ...

def awesome_oscillator(high: ArrayLike, low: ArrayLike, fast: int = 5, slow: int = 34) -> FloatList:
    """Awesome Oscillator."""
    ...

def coppock(close: ArrayLike, wma: int = 10, roc1: int = 14, roc2: int = 11) -> FloatList:
    """Coppock Curve."""
    ...

def fisher_transform(high: ArrayLike, low: ArrayLike, period: int = 9) -> Tuple[FloatList, FloatList]:
    """Fisher Transform."""
    ...

def pgo(high: ArrayLike, low: ArrayLike, close: ArrayLike, period: int = 14) -> FloatList:
    """Pretty Good Oscillator."""
    ...

def inertia(close: ArrayLike, high: ArrayLike, low: ArrayLike, rvi_period: int = 20, regression_period: int = 14) -> FloatList:
    """Inertia Indicator."""
    ...

def cmo(close: ArrayLike, period: int = 14) -> FloatList:
    """Chande Momentum Oscillator."""
    ...

def kdj(high: ArrayLike, low: ArrayLike, close: ArrayLike, k_period: int = 9, d_period: int = 3, j_period: int = 3) -> Tuple[FloatList, FloatList, FloatList]:
    """KDJ Indicator."""
    ...

def kst(close: ArrayLike, roc1: int = 10, roc2: int = 15, roc3: int = 20, roc4: int = 30, sma1: int = 10, sma2: int = 10, sma3: int = 10, sma4: int = 15, signal: int = 9) -> Tuple[FloatList, FloatList]:
    """Know Sure Thing."""
    ...

def smi(high: ArrayLike, low: ArrayLike, close: ArrayLike, k_period: int = 5, d_period: int = 3) -> Tuple[FloatList, FloatList]:
    """Stochastic Momentum Index."""
    ...

def qqe(close: ArrayLike, rsi_period: int = 14, sf: int = 5, threshold: float = 4.236) -> Tuple[FloatList, FloatList, FloatList]:
    """Quantitative Qualitative Estimation."""
    ...

def rvi(close: ArrayLike, high: ArrayLike, low: ArrayLike, open: ArrayLike, period: int = 10) -> Tuple[FloatList, FloatList]:
    """Relative Vigor Index."""
    ...

def stc(close: ArrayLike, fast: int = 23, slow: int = 50, cycle: int = 10, d1: int = 3, d2: int = 3) -> FloatList:
    """Schaff Trend Cycle."""
    ...

def tdfi(close: ArrayLike, period: int = 13) -> FloatList:
    """Trend Detection Filter Index."""
    ...

def cti(close: ArrayLike, period: int = 12) -> FloatList:
    """Correlation Trend Indicator."""
    ...

def cfo(close: ArrayLike, period: int = 9) -> FloatList:
    """Chande Forecast Oscillator."""
    ...

def er(close: ArrayLike, period: int = 10) -> FloatList:
    """Efficiency Ratio."""
    ...

def bias(close: ArrayLike, period: int = 26) -> FloatList:
    """Bias Indicator."""
    ...

def bop(open: ArrayLike, high: ArrayLike, low: ArrayLike, close: ArrayLike) -> FloatList:
    """Balance of Power."""
    ...

# ==================== Trend Indicators ====================

def supertrend(high: ArrayLike, low: ArrayLike, close: ArrayLike, period: int = 10, multiplier: float = 3.0) -> Tuple[FloatList, IntList]:
    """SuperTrend Indicator."""
    ...

def adx(high: ArrayLike, low: ArrayLike, close: ArrayLike, period: int = 14) -> FloatList:
    """Average Directional Index."""
    ...

def plus_di(high: ArrayLike, low: ArrayLike, close: ArrayLike, period: int = 14) -> FloatList:
    """Plus Directional Indicator."""
    ...

def minus_di(high: ArrayLike, low: ArrayLike, close: ArrayLike, period: int = 14) -> FloatList:
    """Minus Directional Indicator."""
    ...

def dx(high: ArrayLike, low: ArrayLike, close: ArrayLike, period: int = 14) -> FloatList:
    """Directional Movement Index."""
    ...

def aroon(high: ArrayLike, low: ArrayLike, period: int = 25) -> Tuple[FloatList, FloatList, FloatList]:
    """Aroon Indicator."""
    ...

def vortex(high: ArrayLike, low: ArrayLike, close: ArrayLike, period: int = 14) -> Tuple[FloatList, FloatList]:
    """Vortex Indicator."""
    ...

def psar(high: ArrayLike, low: ArrayLike, af: float = 0.02, max_af: float = 0.2) -> FloatList:
    """Parabolic SAR."""
    ...

def sar(high: ArrayLike, low: ArrayLike, af: float = 0.02, max_af: float = 0.2) -> FloatList:
    """Parabolic SAR (alias)."""
    ...

def sarext(high: ArrayLike, low: ArrayLike, start_value: float = 0.0, offset_on_reverse: float = 0.0, af_init: float = 0.02, af_step: float = 0.02, af_max: float = 0.2) -> FloatList:
    """Extended Parabolic SAR."""
    ...

def linear_regression(close: ArrayLike, period: int = 14) -> FloatList:
    """Linear Regression."""
    ...

def linearreg(close: ArrayLike, period: int = 14) -> FloatList:
    """Linear Regression."""
    ...

def linearreg_slope(close: ArrayLike, period: int = 14) -> FloatList:
    """Linear Regression Slope."""
    ...

def linearreg_intercept(close: ArrayLike, period: int = 14) -> FloatList:
    """Linear Regression Intercept."""
    ...

def linearreg_angle(close: ArrayLike, period: int = 14) -> FloatList:
    """Linear Regression Angle."""
    ...

def tsf(close: ArrayLike, period: int = 14) -> FloatList:
    """Time Series Forecast."""
    ...

def vhf(close: ArrayLike, period: int = 28) -> FloatList:
    """Vertical Horizontal Filter."""
    ...

def qstick(open: ArrayLike, close: ArrayLike, period: int = 14) -> FloatList:
    """QStick Indicator."""
    ...

def slope(close: ArrayLike, period: int = 1) -> FloatList:
    """Slope."""
    ...

def ichimoku_cloud(high: ArrayLike, low: ArrayLike, close: ArrayLike, tenkan: int = 9, kijun: int = 26, senkou: int = 52) -> Tuple[FloatList, FloatList, FloatList, FloatList, FloatList]:
    """Ichimoku Cloud."""
    ...

def alligator(close: ArrayLike, jaw: int = 13, teeth: int = 8, lips: int = 5, jaw_offset: int = 8, teeth_offset: int = 5, lips_offset: int = 3) -> Tuple[FloatList, FloatList, FloatList]:
    """Williams Alligator."""
    ...

def ssl_channel(high: ArrayLike, low: ArrayLike, close: ArrayLike, period: int = 10) -> Tuple[FloatList, FloatList]:
    """SSL Channel."""
    ...

def choppiness(high: ArrayLike, low: ArrayLike, close: ArrayLike, period: int = 14) -> FloatList:
    """Choppiness Index."""
    ...

def dynamic_macd(close: ArrayLike, fast: int = 12, slow: int = 26, signal: int = 9) -> Tuple[FloatList, FloatList, FloatList]:
    """Dynamic MACD."""
    ...

def ml_supertrend(high: ArrayLike, low: ArrayLike, close: ArrayLike, period: int = 10, multiplier: float = 3.0, lookback: int = 100) -> Tuple[FloatList, IntList, FloatList]:
    """ML-Enhanced SuperTrend."""
    ...

def adaptive_rsi(close: ArrayLike, period: int = 14, smooth: int = 5) -> FloatList:
    """Adaptive RSI."""
    ...

# ==================== Volatility Indicators ====================

def true_range(high: ArrayLike, low: ArrayLike, close: ArrayLike) -> FloatList:
    """True Range."""
    ...

def atr(high: ArrayLike, low: ArrayLike, close: ArrayLike, period: int = 14) -> FloatList:
    """Average True Range."""
    ...

def natr(high: ArrayLike, low: ArrayLike, close: ArrayLike, period: int = 14) -> FloatList:
    """Normalized Average True Range."""
    ...

def bollinger_bands(close: ArrayLike, period: int = 20, std_dev: float = 2.0) -> Tuple[FloatList, FloatList, FloatList]:
    """Bollinger Bands."""
    ...

def keltner_channel(high: ArrayLike, low: ArrayLike, close: ArrayLike, period: int = 20, multiplier: float = 2.0, atr_period: int = 10) -> Tuple[FloatList, FloatList, FloatList]:
    """Keltner Channel."""
    ...

def donchian_channel(high: ArrayLike, low: ArrayLike, period: int = 20) -> Tuple[FloatList, FloatList, FloatList]:
    """Donchian Channel."""
    ...

def chandelier_exit(high: ArrayLike, low: ArrayLike, close: ArrayLike, period: int = 22, multiplier: float = 3.0) -> Tuple[FloatList, FloatList]:
    """Chandelier Exit."""
    ...

def historical_volatility(close: ArrayLike, period: int = 20) -> FloatList:
    """Historical Volatility."""
    ...

def ulcer_index(close: ArrayLike, period: int = 14) -> FloatList:
    """Ulcer Index."""
    ...

def mass_index(high: ArrayLike, low: ArrayLike, fast: int = 9, slow: int = 25) -> FloatList:
    """Mass Index."""
    ...

def squeeze(close: ArrayLike, high: ArrayLike, low: ArrayLike, bb_period: int = 20, bb_mult: float = 2.0, kc_period: int = 20, kc_mult: float = 1.5) -> Tuple[FloatList, IntList]:
    """Squeeze Indicator."""
    ...

def aberration(high: ArrayLike, low: ArrayLike, close: ArrayLike, period: int = 5, atr_period: int = 14) -> Tuple[FloatList, FloatList, FloatList, FloatList]:
    """Aberration."""
    ...

# ==================== Volume Indicators ====================

def obv(close: ArrayLike, volume: ArrayLike) -> FloatList:
    """On Balance Volume."""
    ...

def vwap(high: ArrayLike, low: ArrayLike, close: ArrayLike, volume: ArrayLike) -> FloatList:
    """Volume Weighted Average Price."""
    ...

def ad(high: ArrayLike, low: ArrayLike, close: ArrayLike, volume: ArrayLike) -> FloatList:
    """Accumulation/Distribution Line."""
    ...

def adosc(high: ArrayLike, low: ArrayLike, close: ArrayLike, volume: ArrayLike, fast: int = 3, slow: int = 10) -> FloatList:
    """Chaikin A/D Oscillator."""
    ...

def mfi(high: ArrayLike, low: ArrayLike, close: ArrayLike, volume: ArrayLike, period: int = 14) -> FloatList:
    """Money Flow Index."""
    ...

def pvt(close: ArrayLike, volume: ArrayLike) -> FloatList:
    """Price Volume Trend."""
    ...

def nvi(close: ArrayLike, volume: ArrayLike) -> FloatList:
    """Negative Volume Index."""
    ...

def pvi(close: ArrayLike, volume: ArrayLike) -> FloatList:
    """Positive Volume Index."""
    ...

def eom(high: ArrayLike, low: ArrayLike, volume: ArrayLike, period: int = 14, divisor: float = 10000.0) -> FloatList:
    """Ease of Movement."""
    ...

def force_index(close: ArrayLike, volume: ArrayLike, period: int = 13) -> FloatList:
    """Force Index."""
    ...

def efi(close: ArrayLike, volume: ArrayLike, period: int = 13) -> FloatList:
    """Elder Force Index."""
    ...

def volume_oscillator(volume: ArrayLike, fast: int = 5, slow: int = 10) -> FloatList:
    """Volume Oscillator."""
    ...

def volume_profile(high: ArrayLike, low: ArrayLike, close: ArrayLike, volume: ArrayLike, bins: int = 12) -> Dict[str, Any]:
    """Volume Profile."""
    ...

def volume_filter(close: ArrayLike, volume: ArrayLike, period: int = 14) -> FloatList:
    """Volume Filter."""
    ...

def wae(close: ArrayLike, volume: ArrayLike, sensitivity: float = 150.0, fast: int = 20, slow: int = 40, bb_period: int = 20, bb_mult: float = 2.0) -> Tuple[FloatList, FloatList, FloatList, FloatList]:
    """Waddah Attar Explosion."""
    ...

# ==================== Statistical Functions ====================

def correl(x: ArrayLike, y: ArrayLike, period: int = 20) -> FloatList:
    """Correlation Coefficient."""
    ...

def correlation(x: ArrayLike, y: ArrayLike, period: int = 20) -> FloatList:
    """Correlation Coefficient (alias)."""
    ...

def covariance(x: ArrayLike, y: ArrayLike, period: int = 20) -> FloatList:
    """Covariance."""
    ...

def beta(close: ArrayLike, benchmark: ArrayLike, period: int = 20) -> FloatList:
    """Beta."""
    ...

def var(close: ArrayLike, period: int = 20) -> FloatList:
    """Variance."""
    ...

def zscore(close: ArrayLike, period: int = 20) -> FloatList:
    """Z-Score."""
    ...

def percent_rank(close: ArrayLike, period: int = 20) -> FloatList:
    """Percent Rank."""
    ...

def entropy(close: ArrayLike, period: int = 10) -> FloatList:
    """Entropy."""
    ...

def standard_error(close: ArrayLike, period: int = 21) -> FloatList:
    """Standard Error."""
    ...

# ==================== Math Functions ====================

def abs(x: ArrayLike) -> FloatList:
    """Absolute Value."""
    ...

def acos(x: ArrayLike) -> FloatList:
    """Arc Cosine."""
    ...

def asin(x: ArrayLike) -> FloatList:
    """Arc Sine."""
    ...

def atan(x: ArrayLike) -> FloatList:
    """Arc Tangent."""
    ...

def ceil(x: ArrayLike) -> FloatList:
    """Ceiling."""
    ...

def cos(x: ArrayLike) -> FloatList:
    """Cosine."""
    ...

def cosh(x: ArrayLike) -> FloatList:
    """Hyperbolic Cosine."""
    ...

def exp(x: ArrayLike) -> FloatList:
    """Exponential."""
    ...

def floor(x: ArrayLike) -> FloatList:
    """Floor."""
    ...

def ln(x: ArrayLike) -> FloatList:
    """Natural Logarithm."""
    ...

def log10(x: ArrayLike) -> FloatList:
    """Logarithm Base 10."""
    ...

def sin(x: ArrayLike) -> FloatList:
    """Sine."""
    ...

def sinh(x: ArrayLike) -> FloatList:
    """Hyperbolic Sine."""
    ...

def sqrt(x: ArrayLike) -> FloatList:
    """Square Root."""
    ...

def tan(x: ArrayLike) -> FloatList:
    """Tangent."""
    ...

def tanh(x: ArrayLike) -> FloatList:
    """Hyperbolic Tangent."""
    ...

def add(x: ArrayLike, y: ArrayLike) -> FloatList:
    """Addition."""
    ...

def sub(x: ArrayLike, y: ArrayLike) -> FloatList:
    """Subtraction."""
    ...

def mult(x: ArrayLike, y: ArrayLike) -> FloatList:
    """Multiplication."""
    ...

def div(x: ArrayLike, y: ArrayLike) -> FloatList:
    """Division."""
    ...

def max(x: ArrayLike, period: int = 30) -> FloatList:
    """Rolling Maximum."""
    ...

def min(x: ArrayLike, period: int = 30) -> FloatList:
    """Rolling Minimum."""
    ...

def sum(x: ArrayLike, period: int = 30) -> FloatList:
    """Rolling Sum."""
    ...

def minmax(x: ArrayLike, period: int = 30) -> Tuple[FloatList, FloatList]:
    """Rolling Min and Max."""
    ...

def minmaxindex(x: ArrayLike, period: int = 30) -> Tuple[IntList, IntList]:
    """Rolling Min and Max Index."""
    ...

# ==================== Price Transform ====================

def avgprice(open: ArrayLike, high: ArrayLike, low: ArrayLike, close: ArrayLike) -> FloatList:
    """Average Price."""
    ...

def medprice(high: ArrayLike, low: ArrayLike) -> FloatList:
    """Median Price."""
    ...

def typprice(high: ArrayLike, low: ArrayLike, close: ArrayLike) -> FloatList:
    """Typical Price."""
    ...

def wclprice(high: ArrayLike, low: ArrayLike, close: ArrayLike) -> FloatList:
    """Weighted Close Price."""
    ...

def midpoint(close: ArrayLike, period: int = 14) -> FloatList:
    """Midpoint."""
    ...

def midprice(high: ArrayLike, low: ArrayLike, period: int = 14) -> FloatList:
    """Midprice."""
    ...

# ==================== Hilbert Transform ====================

def ht_dcperiod(close: ArrayLike) -> FloatList:
    """Hilbert Transform - Dominant Cycle Period."""
    ...

def ht_dcphase(close: ArrayLike) -> FloatList:
    """Hilbert Transform - Dominant Cycle Phase."""
    ...

def ht_phasor(close: ArrayLike) -> Tuple[FloatList, FloatList]:
    """Hilbert Transform - Phasor Components."""
    ...

def ht_sine(close: ArrayLike) -> Tuple[FloatList, FloatList]:
    """Hilbert Transform - SineWave."""
    ...

def ht_trendmode(close: ArrayLike) -> IntList:
    """Hilbert Transform - Trend vs Cycle Mode."""
    ...

# ==================== Pivot Points ====================

def standard_pivots(high: ArrayLike, low: ArrayLike, close: ArrayLike) -> Tuple[FloatList, FloatList, FloatList, FloatList, FloatList]:
    """Standard Pivot Points."""
    ...

def fibonacci_pivots(high: ArrayLike, low: ArrayLike, close: ArrayLike) -> Tuple[FloatList, FloatList, FloatList, FloatList, FloatList, FloatList, FloatList]:
    """Fibonacci Pivot Points."""
    ...

def camarilla_pivots(high: ArrayLike, low: ArrayLike, close: ArrayLike) -> Tuple[FloatList, FloatList, FloatList, FloatList, FloatList, FloatList, FloatList, FloatList, FloatList]:
    """Camarilla Pivot Points."""
    ...

def fib_retracement(high: float, low: float) -> Dict[str, float]:
    """Fibonacci Retracement Levels."""
    ...

def fib_extension(high: float, low: float, retracement: float) -> Dict[str, float]:
    """Fibonacci Extension Levels."""
    ...

# ==================== Candlestick Patterns ====================

def doji(open: ArrayLike, high: ArrayLike, low: ArrayLike, close: ArrayLike) -> IntList:
    """Doji Pattern."""
    ...

def doji_star(open: ArrayLike, high: ArrayLike, low: ArrayLike, close: ArrayLike) -> IntList:
    """Doji Star Pattern."""
    ...

def dragonfly_doji(open: ArrayLike, high: ArrayLike, low: ArrayLike, close: ArrayLike) -> IntList:
    """Dragonfly Doji Pattern."""
    ...

def gravestone_doji(open: ArrayLike, high: ArrayLike, low: ArrayLike, close: ArrayLike) -> IntList:
    """Gravestone Doji Pattern."""
    ...

def long_legged_doji(open: ArrayLike, high: ArrayLike, low: ArrayLike, close: ArrayLike) -> IntList:
    """Long-Legged Doji Pattern."""
    ...

def hammer(open: ArrayLike, high: ArrayLike, low: ArrayLike, close: ArrayLike) -> IntList:
    """Hammer Pattern."""
    ...

def inverted_hammer(open: ArrayLike, high: ArrayLike, low: ArrayLike, close: ArrayLike) -> IntList:
    """Inverted Hammer Pattern."""
    ...

def hanging_man(open: ArrayLike, high: ArrayLike, low: ArrayLike, close: ArrayLike) -> IntList:
    """Hanging Man Pattern."""
    ...

def shooting_star(open: ArrayLike, high: ArrayLike, low: ArrayLike, close: ArrayLike) -> IntList:
    """Shooting Star Pattern."""
    ...

def bullish_engulfing(open: ArrayLike, high: ArrayLike, low: ArrayLike, close: ArrayLike) -> IntList:
    """Bullish Engulfing Pattern."""
    ...

def bearish_engulfing(open: ArrayLike, high: ArrayLike, low: ArrayLike, close: ArrayLike) -> IntList:
    """Bearish Engulfing Pattern."""
    ...

def bullish_harami(open: ArrayLike, high: ArrayLike, low: ArrayLike, close: ArrayLike) -> IntList:
    """Bullish Harami Pattern."""
    ...

def bearish_harami(open: ArrayLike, high: ArrayLike, low: ArrayLike, close: ArrayLike) -> IntList:
    """Bearish Harami Pattern."""
    ...

def harami_cross(open: ArrayLike, high: ArrayLike, low: ArrayLike, close: ArrayLike) -> IntList:
    """Harami Cross Pattern."""
    ...

def morning_star(open: ArrayLike, high: ArrayLike, low: ArrayLike, close: ArrayLike) -> IntList:
    """Morning Star Pattern."""
    ...

def morning_doji_star(open: ArrayLike, high: ArrayLike, low: ArrayLike, close: ArrayLike) -> IntList:
    """Morning Doji Star Pattern."""
    ...

def evening_star(open: ArrayLike, high: ArrayLike, low: ArrayLike, close: ArrayLike) -> IntList:
    """Evening Star Pattern."""
    ...

def evening_doji_star(open: ArrayLike, high: ArrayLike, low: ArrayLike, close: ArrayLike) -> IntList:
    """Evening Doji Star Pattern."""
    ...

def three_white_soldiers(open: ArrayLike, high: ArrayLike, low: ArrayLike, close: ArrayLike) -> IntList:
    """Three White Soldiers Pattern."""
    ...

def three_black_crows(open: ArrayLike, high: ArrayLike, low: ArrayLike, close: ArrayLike) -> IntList:
    """Three Black Crows Pattern."""
    ...

def dark_cloud_cover(open: ArrayLike, high: ArrayLike, low: ArrayLike, close: ArrayLike) -> IntList:
    """Dark Cloud Cover Pattern."""
    ...

def piercing_pattern(open: ArrayLike, high: ArrayLike, low: ArrayLike, close: ArrayLike) -> IntList:
    """Piercing Pattern."""
    ...

def spinning_top(open: ArrayLike, high: ArrayLike, low: ArrayLike, close: ArrayLike) -> IntList:
    """Spinning Top Pattern."""
    ...

def marubozu(open: ArrayLike, high: ArrayLike, low: ArrayLike, close: ArrayLike) -> IntList:
    """Marubozu Pattern."""
    ...

def closing_marubozu(open: ArrayLike, high: ArrayLike, low: ArrayLike, close: ArrayLike) -> IntList:
    """Closing Marubozu Pattern."""
    ...

def tweezers_top(open: ArrayLike, high: ArrayLike, low: ArrayLike, close: ArrayLike) -> IntList:
    """Tweezers Top Pattern."""
    ...

def tweezers_bottom(open: ArrayLike, high: ArrayLike, low: ArrayLike, close: ArrayLike) -> IntList:
    """Tweezers Bottom Pattern."""
    ...

def rising_three_methods(open: ArrayLike, high: ArrayLike, low: ArrayLike, close: ArrayLike) -> IntList:
    """Rising Three Methods Pattern."""
    ...

def falling_three_methods(open: ArrayLike, high: ArrayLike, low: ArrayLike, close: ArrayLike) -> IntList:
    """Falling Three Methods Pattern."""
    ...

def three_inside(open: ArrayLike, high: ArrayLike, low: ArrayLike, close: ArrayLike) -> IntList:
    """Three Inside Up/Down Pattern."""
    ...

def three_outside(open: ArrayLike, high: ArrayLike, low: ArrayLike, close: ArrayLike) -> IntList:
    """Three Outside Up/Down Pattern."""
    ...

def long_line(open: ArrayLike, high: ArrayLike, low: ArrayLike, close: ArrayLike) -> IntList:
    """Long Line Pattern."""
    ...

def short_line(open: ArrayLike, high: ArrayLike, low: ArrayLike, close: ArrayLike) -> IntList:
    """Short Line Pattern."""
    ...

def highwave(open: ArrayLike, high: ArrayLike, low: ArrayLike, close: ArrayLike) -> IntList:
    """High Wave Pattern."""
    ...

def rickshaw_man(open: ArrayLike, high: ArrayLike, low: ArrayLike, close: ArrayLike) -> IntList:
    """Rickshaw Man Pattern."""
    ...

def takuri(open: ArrayLike, high: ArrayLike, low: ArrayLike, close: ArrayLike) -> IntList:
    """Takuri Pattern."""
    ...

def belthold(open: ArrayLike, high: ArrayLike, low: ArrayLike, close: ArrayLike) -> IntList:
    """Belt Hold Pattern."""
    ...

def kicking(open: ArrayLike, high: ArrayLike, low: ArrayLike, close: ArrayLike) -> IntList:
    """Kicking Pattern."""
    ...

def counterattack(open: ArrayLike, high: ArrayLike, low: ArrayLike, close: ArrayLike) -> IntList:
    """Counterattack Pattern."""
    ...

def separating_lines(open: ArrayLike, high: ArrayLike, low: ArrayLike, close: ArrayLike) -> IntList:
    """Separating Lines Pattern."""
    ...

def thrusting(open: ArrayLike, high: ArrayLike, low: ArrayLike, close: ArrayLike) -> IntList:
    """Thrusting Pattern."""
    ...

def inneck(open: ArrayLike, high: ArrayLike, low: ArrayLike, close: ArrayLike) -> IntList:
    """In Neck Pattern."""
    ...

def onneck(open: ArrayLike, high: ArrayLike, low: ArrayLike, close: ArrayLike) -> IntList:
    """On Neck Pattern."""
    ...

def abandoned_baby(open: ArrayLike, high: ArrayLike, low: ArrayLike, close: ArrayLike) -> IntList:
    """Abandoned Baby Pattern."""
    ...

def advance_block(open: ArrayLike, high: ArrayLike, low: ArrayLike, close: ArrayLike) -> IntList:
    """Advance Block Pattern."""
    ...

def breakaway(open: ArrayLike, high: ArrayLike, low: ArrayLike, close: ArrayLike) -> IntList:
    """Breakaway Pattern."""
    ...

def concealing_baby_swallow(open: ArrayLike, high: ArrayLike, low: ArrayLike, close: ArrayLike) -> IntList:
    """Concealing Baby Swallow Pattern."""
    ...

def gap_sidesidewhite(open: ArrayLike, high: ArrayLike, low: ArrayLike, close: ArrayLike) -> IntList:
    """Gap Side-by-Side White Lines Pattern."""
    ...

def hikkake(open: ArrayLike, high: ArrayLike, low: ArrayLike, close: ArrayLike) -> IntList:
    """Hikkake Pattern."""
    ...

def hikkake_mod(open: ArrayLike, high: ArrayLike, low: ArrayLike, close: ArrayLike) -> IntList:
    """Modified Hikkake Pattern."""
    ...

def homing_pigeon(open: ArrayLike, high: ArrayLike, low: ArrayLike, close: ArrayLike) -> IntList:
    """Homing Pigeon Pattern."""
    ...

def identical_three_crows(open: ArrayLike, high: ArrayLike, low: ArrayLike, close: ArrayLike) -> IntList:
    """Identical Three Crows Pattern."""
    ...

def ladder_bottom(open: ArrayLike, high: ArrayLike, low: ArrayLike, close: ArrayLike) -> IntList:
    """Ladder Bottom Pattern."""
    ...

def matching_low(open: ArrayLike, high: ArrayLike, low: ArrayLike, close: ArrayLike) -> IntList:
    """Matching Low Pattern."""
    ...

def mat_hold(open: ArrayLike, high: ArrayLike, low: ArrayLike, close: ArrayLike) -> IntList:
    """Mat Hold Pattern."""
    ...

def stalled_pattern(open: ArrayLike, high: ArrayLike, low: ArrayLike, close: ArrayLike) -> IntList:
    """Stalled Pattern."""
    ...

def stick_sandwich(open: ArrayLike, high: ArrayLike, low: ArrayLike, close: ArrayLike) -> IntList:
    """Stick Sandwich Pattern."""
    ...

def tristar(open: ArrayLike, high: ArrayLike, low: ArrayLike, close: ArrayLike) -> IntList:
    """Tristar Pattern."""
    ...

def unique_3_river(open: ArrayLike, high: ArrayLike, low: ArrayLike, close: ArrayLike) -> IntList:
    """Unique 3 River Pattern."""
    ...

def upside_gap_two_crows(open: ArrayLike, high: ArrayLike, low: ArrayLike, close: ArrayLike) -> IntList:
    """Upside Gap Two Crows Pattern."""
    ...

def xside_gap_3_methods(open: ArrayLike, high: ArrayLike, low: ArrayLike, close: ArrayLike) -> IntList:
    """X-Side Gap Three Methods Pattern."""
    ...

# ==================== AI/ML Indicators ====================

def ai_supertrend(high: ArrayLike, low: ArrayLike, close: ArrayLike, period: int = 10, multiplier: float = 3.0) -> Tuple[FloatList, IntList]:
    """AI-Enhanced SuperTrend."""
    ...

def ai_supertrend_ml(high: ArrayLike, low: ArrayLike, close: ArrayLike, period: int = 10, multiplier: float = 3.0, lookback: int = 100) -> Tuple[FloatList, IntList, FloatList]:
    """ML-Enhanced SuperTrend."""
    ...

def ai_momentum_index(close: ArrayLike, period: int = 14) -> FloatList:
    """AI Momentum Index."""
    ...

def ai_momentum_index_ml(close: ArrayLike, period: int = 14, lookback: int = 100) -> Tuple[FloatList, FloatList]:
    """ML-Enhanced AI Momentum Index."""
    ...

def ensemble_signal(close: ArrayLike, high: ArrayLike, low: ArrayLike, volume: ArrayLike) -> Tuple[FloatList, FloatList]:
    """Ensemble Signal combining multiple indicators."""
    ...

def detect_divergence(close: ArrayLike, indicator: ArrayLike, lookback: int = 14) -> IntList:
    """Detect price-indicator divergence."""
    ...

# ==================== Trading Signals ====================

def pivot_buy_sell(high: ArrayLike, low: ArrayLike, close: ArrayLike, left: int = 4, right: int = 2) -> Tuple[IntList, IntList]:
    """Pivot-based Buy/Sell Signals."""
    ...

def combine_signals(signals: List[IntList], weights: Optional[List[float]] = None) -> FloatList:
    """Combine multiple trading signals."""
    ...

def calculate_stops(close: ArrayLike, atr: ArrayLike, multiplier: float = 2.0) -> Tuple[FloatList, FloatList]:
    """Calculate Stop Loss and Take Profit levels."""
    ...

def atr2_signals(high: ArrayLike, low: ArrayLike, close: ArrayLike, period: int = 14, multiplier: float = 2.0) -> Tuple[FloatList, FloatList, IntList]:
    """ATR-based Trading Signals."""
    ...

def atr2_signals_ml(high: ArrayLike, low: ArrayLike, close: ArrayLike, period: int = 14, multiplier: float = 2.0, lookback: int = 100) -> Tuple[FloatList, FloatList, IntList, FloatList]:
    """ML-Enhanced ATR Trading Signals."""
    ...

def fvg_signals(open: ArrayLike, high: ArrayLike, low: ArrayLike, close: ArrayLike) -> IntList:
    """Fair Value Gap Signals."""
    ...

# ==================== Real-time Functions ====================

def realtime_rsi(close: ArrayLike, period: int = 14) -> FloatList:
    """Real-time RSI calculation."""
    ...

def realtime_supertrend(high: ArrayLike, low: ArrayLike, close: ArrayLike, period: int = 10, multiplier: float = 3.0) -> Tuple[FloatList, IntList]:
    """Real-time SuperTrend calculation."""
    ...

def realtime_multi_indicator(high: ArrayLike, low: ArrayLike, close: ArrayLike, volume: ArrayLike) -> Dict[str, FloatList]:
    """Real-time multi-indicator calculation."""
    ...

def get_available_streaming_indicators() -> List[str]:
    """Get list of available streaming indicators."""
    ...

def create_indicator(name: str, **kwargs: Any) -> IncrementalIndicator:
    """Create an incremental indicator by name."""
    ...

# ==================== Deprecated py_ prefix functions ====================
# These are deprecated and will be removed in version 1.0
# Use the non-prefixed versions instead

def py_sma(close: ArrayLike, period: int = 20) -> FloatList: ...
def py_ema(close: ArrayLike, period: int = 20) -> FloatList: ...
def py_rsi(close: ArrayLike, period: int = 14) -> FloatList: ...
def py_macd(close: ArrayLike, fast: int = 12, slow: int = 26, signal: int = 9) -> Tuple[FloatList, FloatList, FloatList]: ...
def py_bollinger_bands(close: ArrayLike, period: int = 20, std_dev: float = 2.0) -> Tuple[FloatList, FloatList, FloatList]: ...
def py_atr(high: ArrayLike, low: ArrayLike, close: ArrayLike, period: int = 14) -> FloatList: ...
def py_supertrend(high: ArrayLike, low: ArrayLike, close: ArrayLike, period: int = 10, multiplier: float = 3.0) -> Tuple[FloatList, IntList]: ...
def py_adx(high: ArrayLike, low: ArrayLike, close: ArrayLike, period: int = 14) -> FloatList: ...
def py_obv(close: ArrayLike, volume: ArrayLike) -> FloatList: ...
def py_vwap(high: ArrayLike, low: ArrayLike, close: ArrayLike, volume: ArrayLike) -> FloatList: ...
def py_mfi(high: ArrayLike, low: ArrayLike, close: ArrayLike, volume: ArrayLike, period: int = 14) -> FloatList: ...
def py_cci(high: ArrayLike, low: ArrayLike, close: ArrayLike, period: int = 20) -> FloatList: ...
def py_stochastic(high: ArrayLike, low: ArrayLike, close: ArrayLike, k_period: int = 14, d_period: int = 3) -> Tuple[FloatList, FloatList]: ...
def py_willr(high: ArrayLike, low: ArrayLike, close: ArrayLike, period: int = 14) -> FloatList: ...
def py_aroon(high: ArrayLike, low: ArrayLike, period: int = 25) -> Tuple[FloatList, FloatList, FloatList]: ...
def py_psar(high: ArrayLike, low: ArrayLike, af: float = 0.02, max_af: float = 0.2) -> FloatList: ...
def py_keltner_channels(high: ArrayLike, low: ArrayLike, close: ArrayLike, period: int = 20, multiplier: float = 2.0, atr_period: int = 10) -> Tuple[FloatList, FloatList, FloatList]: ...
def py_donchian_channels(high: ArrayLike, low: ArrayLike, period: int = 20) -> Tuple[FloatList, FloatList, FloatList]: ...
def py_ichimoku(high: ArrayLike, low: ArrayLike, close: ArrayLike, tenkan: int = 9, kijun: int = 26, senkou: int = 52) -> Tuple[FloatList, FloatList, FloatList, FloatList, FloatList]: ...
def py_true_range(high: ArrayLike, low: ArrayLike, close: ArrayLike) -> FloatList: ...
def py_natr(high: ArrayLike, low: ArrayLike, close: ArrayLike, period: int = 14) -> FloatList: ...
def py_hma(close: ArrayLike, period: int = 20) -> FloatList: ...
def py_wma(close: ArrayLike, period: int = 20) -> FloatList: ...
def py_dema(close: ArrayLike, period: int = 20) -> FloatList: ...
def py_tema(close: ArrayLike, period: int = 20) -> FloatList: ...
def py_kama(close: ArrayLike, period: int = 10, fast: int = 2, slow: int = 30) -> FloatList: ...
def py_vwma(close: ArrayLike, volume: ArrayLike, period: int = 20) -> FloatList: ...
def py_cmf(high: ArrayLike, low: ArrayLike, close: ArrayLike, volume: ArrayLike, period: int = 20) -> FloatList: ...
def py_ppo(close: ArrayLike, fast: int = 12, slow: int = 26, signal: int = 9) -> Tuple[FloatList, FloatList, FloatList]: ...
def py_roc(close: ArrayLike, period: int = 10) -> FloatList: ...
def py_momentum(close: ArrayLike, period: int = 10) -> FloatList: ...
def py_tsi(close: ArrayLike, long: int = 25, short: int = 13, signal: int = 13) -> Tuple[FloatList, FloatList]: ...
def py_ultimate_oscillator(high: ArrayLike, low: ArrayLike, close: ArrayLike, short: int = 7, medium: int = 14, long: int = 28) -> FloatList: ...
def py_vortex(high: ArrayLike, low: ArrayLike, close: ArrayLike, period: int = 14) -> Tuple[FloatList, FloatList]: ...
def py_plus_di(high: ArrayLike, low: ArrayLike, close: ArrayLike, period: int = 14) -> FloatList: ...
def py_minus_di(high: ArrayLike, low: ArrayLike, close: ArrayLike, period: int = 14) -> FloatList: ...
def py_dx(high: ArrayLike, low: ArrayLike, close: ArrayLike, period: int = 14) -> FloatList: ...
def py_ad(high: ArrayLike, low: ArrayLike, close: ArrayLike, volume: ArrayLike) -> FloatList: ...
def py_adosc(high: ArrayLike, low: ArrayLike, close: ArrayLike, volume: ArrayLike, fast: int = 3, slow: int = 10) -> FloatList: ...
def py_nvi(close: ArrayLike, volume: ArrayLike) -> FloatList: ...
def py_pvi(close: ArrayLike, volume: ArrayLike) -> FloatList: ...
def py_pvt(close: ArrayLike, volume: ArrayLike) -> FloatList: ...
def py_eom(high: ArrayLike, low: ArrayLike, volume: ArrayLike, period: int = 14, divisor: float = 10000.0) -> FloatList: ...
def py_force_index(close: ArrayLike, volume: ArrayLike, period: int = 13) -> FloatList: ...
def py_linear_regression(close: ArrayLike, period: int = 14) -> FloatList: ...
def py_tsf(close: ArrayLike, period: int = 14) -> FloatList: ...
def py_correl(x: ArrayLike, y: ArrayLike, period: int = 20) -> FloatList: ...
def py_beta(close: ArrayLike, benchmark: ArrayLike, period: int = 20) -> FloatList: ...
def py_var(close: ArrayLike, period: int = 20) -> FloatList: ...
def py_zscore(close: ArrayLike, period: int = 20) -> FloatList: ...
