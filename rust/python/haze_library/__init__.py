"""
Haze-Library: High-Performance Quantitative Trading Indicators
==============================================================

Rust-powered technical indicators for Python with 200+ indicators.

Usage:
------
    # TA-Lib style (recommended)
    import haze_library as haze

    sma = haze.sma(close_prices, 20)
    rsi = haze.rsi(close_prices, 14)
    macd_line, signal, histogram = haze.macd(close_prices, 12, 26, 9)

    # DataFrame accessor
    import pandas as pd
    import haze_library

    df = pd.read_csv('ohlcv.csv')
    df['sma_20'] = df.ta.sma(20)
    df['rsi_14'] = df.ta.rsi(14)

    # Legacy py_ prefix (still supported)
    from haze_library import py_sma, py_rsi

Performance:
-----------
    - 5-10x faster than pure Python implementations
    - 4.8-6.3x faster than TA-Lib for most indicators
    - High numerical precision using f64
"""

__version__ = "0.1.0"
__author__ = "kwannz"

# Import Rust extension with py_ prefix functions
try:
    from .haze_library import (
        # Math functions
        py_abs, py_acos, py_add, py_asin, py_atan, py_ceil, py_cos, py_cosh,
        py_div, py_exp, py_floor, py_ln, py_log10, py_max, py_min, py_minmax,
        py_minmaxindex, py_mult, py_sin, py_sinh, py_sqrt, py_sub, py_sum,
        py_tan, py_tanh,
        # Moving Averages
        py_sma, py_ema, py_rma, py_wma, py_hma, py_dema, py_tema, py_zlma,
        py_kama, py_t3, py_alma, py_frama, py_trima, py_vidya, py_pwma,
        py_sinwma, py_swma, py_vwma, py_mama,
        # Volatility
        py_true_range, py_atr, py_natr, py_bollinger_bands, py_keltner_channel,
        py_donchian_channel, py_aberration,
        # Momentum
        py_rsi, py_macd, py_stochastic, py_stochrsi, py_cci, py_williams_r,
        py_awesome_oscillator, py_fisher_transform, py_kdj, py_tsi, py_mom,
        py_roc, py_cmo, py_apo, py_ppo, py_ultimate_oscillator, py_bop,
        py_coppock, py_cti, py_er, py_inertia, py_kst, py_pgo, py_psl,
        py_qqe, py_qstick, py_rvi, py_smi, py_squeeze, py_stc, py_tdfi,
        py_vhf, py_wae,
        # Trend
        py_supertrend, py_adx, py_aroon, py_psar, py_sar, py_sarext,
        py_vortex, py_choppiness, py_dx, py_plus_di, py_minus_di,
        py_alligator, py_ichimoku_cloud, py_ssl_channel,
        # Volume
        py_obv, py_vwap, py_mfi, py_cmf, py_ad, py_adosc, py_pvt, py_nvi,
        py_pvi, py_eom, py_efi, py_volume_profile, py_volume_filter,
        # Statistical
        py_linear_regression, py_linearreg, py_linearreg_angle,
        py_linearreg_intercept, py_linearreg_slope, py_correlation, py_correl,
        py_zscore, py_var, py_standard_error, py_beta, py_covariance,
        py_entropy, py_percent_rank, py_slope, py_tsf, py_bias, py_cfo,
        # Price transforms
        py_avgprice, py_medprice, py_typprice, py_wclprice, py_midpoint,
        py_midprice,
        # Hilbert Transform
        py_ht_dcperiod, py_ht_dcphase, py_ht_phasor, py_ht_sine, py_ht_trendmode,
        # Pivots & Fibonacci
        py_standard_pivots, py_camarilla_pivots, py_fibonacci_pivots,
        py_fib_retracement, py_fib_extension, py_harmonics, py_harmonics_patterns,
        # Candlestick Patterns
        py_doji, py_hammer, py_inverted_hammer, py_hanging_man, py_shooting_star,
        py_bullish_engulfing, py_bearish_engulfing, py_bullish_harami,
        py_bearish_harami, py_piercing_pattern, py_dark_cloud_cover,
        py_morning_star, py_evening_star, py_three_white_soldiers,
        py_three_black_crows, py_marubozu, py_spinning_top, py_dragonfly_doji,
        py_gravestone_doji, py_long_legged_doji, py_tweezers_top,
        py_tweezers_bottom, py_rising_three_methods, py_falling_three_methods,
        py_harami_cross, py_morning_doji_star, py_evening_doji_star,
        py_three_inside, py_three_outside, py_abandoned_baby, py_kicking,
        py_long_line, py_short_line, py_doji_star, py_identical_three_crows,
        py_stick_sandwich, py_tristar, py_upside_gap_two_crows,
        py_gap_sidesidewhite, py_takuri, py_homing_pigeon, py_matching_low,
        py_separating_lines, py_thrusting, py_inneck, py_onneck,
        py_advance_block, py_stalled_pattern, py_belthold,
        py_concealing_baby_swallow, py_counterattack, py_highwave, py_hikkake,
        py_hikkake_mod, py_ladder_bottom, py_mat_hold, py_rickshaw_man,
        py_closing_marubozu, py_breakaway, py_unique_3_river,
        py_xside_gap_3_methods,
        # SFG Trading Signals
        py_ai_supertrend, py_ai_supertrend_ml, py_atr2_signals, py_atr2_signals_ml,
        py_pivot_buy_sell, py_ai_momentum_index, py_ai_momentum_index_ml,
        py_dynamic_macd, py_swing_points, py_fvg_signals, py_detect_divergence,
        py_calculate_stops, py_combine_signals, py_breaker_block_signals,
        py_pd_array_signals, py_general_parameters_signals,
        py_linreg_supply_demand_signals,
    )

    # =========================================================================
    # Clean API aliases (TA-Lib style, no py_ prefix)
    # =========================================================================

    # Math functions
    abs = py_abs
    acos = py_acos
    add = py_add
    asin = py_asin
    atan = py_atan
    ceil = py_ceil
    cos = py_cos
    cosh = py_cosh
    div = py_div
    exp = py_exp
    floor = py_floor
    ln = py_ln
    log10 = py_log10
    max = py_max
    min = py_min
    minmax = py_minmax
    minmaxindex = py_minmaxindex
    mult = py_mult
    sin = py_sin
    sinh = py_sinh
    sqrt = py_sqrt
    sub = py_sub
    sum = py_sum
    tan = py_tan
    tanh = py_tanh

    # Moving Averages
    sma = py_sma
    ema = py_ema
    rma = py_rma
    wma = py_wma
    hma = py_hma
    dema = py_dema
    tema = py_tema
    zlma = py_zlma
    kama = py_kama
    t3 = py_t3
    alma = py_alma
    frama = py_frama
    trima = py_trima
    vidya = py_vidya
    pwma = py_pwma
    sinwma = py_sinwma
    swma = py_swma
    vwma = py_vwma
    mama = py_mama

    # Volatility
    true_range = py_true_range
    atr = py_atr
    natr = py_natr
    bollinger_bands = py_bollinger_bands
    keltner_channel = py_keltner_channel
    donchian_channel = py_donchian_channel
    aberration = py_aberration

    # Momentum
    rsi = py_rsi
    macd = py_macd
    stochastic = py_stochastic
    stochrsi = py_stochrsi
    cci = py_cci
    williams_r = py_williams_r
    awesome_oscillator = py_awesome_oscillator
    fisher_transform = py_fisher_transform
    kdj = py_kdj
    tsi = py_tsi
    mom = py_mom
    roc = py_roc
    cmo = py_cmo
    apo = py_apo
    ppo = py_ppo
    ultimate_oscillator = py_ultimate_oscillator
    bop = py_bop
    coppock = py_coppock
    cti = py_cti
    er = py_er
    inertia = py_inertia
    kst = py_kst
    pgo = py_pgo
    psl = py_psl
    qqe = py_qqe
    qstick = py_qstick
    rvi = py_rvi
    smi = py_smi
    squeeze = py_squeeze
    stc = py_stc
    tdfi = py_tdfi
    vhf = py_vhf
    wae = py_wae

    # Trend
    supertrend = py_supertrend
    adx = py_adx
    aroon = py_aroon
    psar = py_psar
    sar = py_sar
    sarext = py_sarext
    vortex = py_vortex
    choppiness = py_choppiness
    dx = py_dx
    plus_di = py_plus_di
    minus_di = py_minus_di
    alligator = py_alligator
    ichimoku_cloud = py_ichimoku_cloud
    ssl_channel = py_ssl_channel

    # Volume
    obv = py_obv
    vwap = py_vwap
    mfi = py_mfi
    cmf = py_cmf
    ad = py_ad
    adosc = py_adosc
    pvt = py_pvt
    nvi = py_nvi
    pvi = py_pvi
    eom = py_eom
    efi = py_efi
    volume_profile = py_volume_profile
    volume_filter = py_volume_filter

    # Statistical
    linear_regression = py_linear_regression
    linearreg = py_linearreg
    linearreg_angle = py_linearreg_angle
    linearreg_intercept = py_linearreg_intercept
    linearreg_slope = py_linearreg_slope
    correlation = py_correlation
    correl = py_correl
    zscore = py_zscore
    var = py_var
    standard_error = py_standard_error
    beta = py_beta
    covariance = py_covariance
    entropy = py_entropy
    percent_rank = py_percent_rank
    slope = py_slope
    tsf = py_tsf
    bias = py_bias
    cfo = py_cfo

    # Price transforms
    avgprice = py_avgprice
    medprice = py_medprice
    typprice = py_typprice
    wclprice = py_wclprice
    midpoint = py_midpoint
    midprice = py_midprice

    # Hilbert Transform
    ht_dcperiod = py_ht_dcperiod
    ht_dcphase = py_ht_dcphase
    ht_phasor = py_ht_phasor
    ht_sine = py_ht_sine
    ht_trendmode = py_ht_trendmode

    # Pivots & Fibonacci
    standard_pivots = py_standard_pivots
    camarilla_pivots = py_camarilla_pivots
    fibonacci_pivots = py_fibonacci_pivots
    fib_retracement = py_fib_retracement
    fib_extension = py_fib_extension
    harmonics = py_harmonics
    harmonics_patterns = py_harmonics_patterns

    # Candlestick Patterns
    doji = py_doji
    hammer = py_hammer
    inverted_hammer = py_inverted_hammer
    hanging_man = py_hanging_man
    shooting_star = py_shooting_star
    bullish_engulfing = py_bullish_engulfing
    bearish_engulfing = py_bearish_engulfing
    bullish_harami = py_bullish_harami
    bearish_harami = py_bearish_harami
    piercing_pattern = py_piercing_pattern
    dark_cloud_cover = py_dark_cloud_cover
    morning_star = py_morning_star
    evening_star = py_evening_star
    three_white_soldiers = py_three_white_soldiers
    three_black_crows = py_three_black_crows
    marubozu = py_marubozu
    spinning_top = py_spinning_top
    dragonfly_doji = py_dragonfly_doji
    gravestone_doji = py_gravestone_doji
    long_legged_doji = py_long_legged_doji
    tweezers_top = py_tweezers_top
    tweezers_bottom = py_tweezers_bottom
    rising_three_methods = py_rising_three_methods
    falling_three_methods = py_falling_three_methods
    harami_cross = py_harami_cross
    morning_doji_star = py_morning_doji_star
    evening_doji_star = py_evening_doji_star
    three_inside = py_three_inside
    three_outside = py_three_outside
    abandoned_baby = py_abandoned_baby
    kicking = py_kicking
    long_line = py_long_line
    short_line = py_short_line
    doji_star = py_doji_star
    identical_three_crows = py_identical_three_crows
    stick_sandwich = py_stick_sandwich
    tristar = py_tristar
    upside_gap_two_crows = py_upside_gap_two_crows
    gap_sidesidewhite = py_gap_sidesidewhite
    takuri = py_takuri
    homing_pigeon = py_homing_pigeon
    matching_low = py_matching_low
    separating_lines = py_separating_lines
    thrusting = py_thrusting
    inneck = py_inneck
    onneck = py_onneck
    advance_block = py_advance_block
    stalled_pattern = py_stalled_pattern
    belthold = py_belthold
    concealing_baby_swallow = py_concealing_baby_swallow
    counterattack = py_counterattack
    highwave = py_highwave
    hikkake = py_hikkake
    hikkake_mod = py_hikkake_mod
    ladder_bottom = py_ladder_bottom
    mat_hold = py_mat_hold
    rickshaw_man = py_rickshaw_man
    closing_marubozu = py_closing_marubozu
    breakaway = py_breakaway
    unique_3_river = py_unique_3_river
    xside_gap_3_methods = py_xside_gap_3_methods

    # SFG Trading Signals
    ai_supertrend = py_ai_supertrend
    ai_supertrend_ml = py_ai_supertrend_ml
    atr2_signals = py_atr2_signals
    atr2_signals_ml = py_atr2_signals_ml
    pivot_buy_sell = py_pivot_buy_sell
    ai_momentum_index = py_ai_momentum_index
    ai_momentum_index_ml = py_ai_momentum_index_ml
    dynamic_macd = py_dynamic_macd
    swing_points = py_swing_points
    fvg_signals = py_fvg_signals
    detect_divergence = py_detect_divergence
    calculate_stops = py_calculate_stops
    combine_signals = py_combine_signals
    breaker_block_signals = py_breaker_block_signals
    pd_array_signals = py_pd_array_signals
    general_parameters_signals = py_general_parameters_signals
    linreg_supply_demand_signals = py_linreg_supply_demand_signals

    _RUST_AVAILABLE = True

except ImportError:
    import warnings
    warnings.warn(
        "Could not import Rust extension module. "
        "Please ensure the package is properly installed."
    )
    _RUST_AVAILABLE = False

# Register pandas accessor
try:
    from . import accessor
    from .accessor import TechnicalAnalysisAccessor, SeriesTechnicalAnalysisAccessor
except ImportError:
    TechnicalAnalysisAccessor = None
    SeriesTechnicalAnalysisAccessor = None

# NumPy compatibility layer
try:
    from . import numpy_compat as np_ta
except ImportError:
    np_ta = None

# Polars compatibility layer
try:
    from . import polars_accessor as polars_ta
except ImportError:
    polars_ta = None

# PyTorch compatibility layer
try:
    from . import torch_compat as torch_ta
except ImportError:
    torch_ta = None

# Custom exceptions
try:
    from .exceptions import (
        HazeError,
        InvalidPeriodError,
        InsufficientDataError,
        ColumnNotFoundError,
        InvalidParameterError,
        ComputationError,
    )
except ImportError:
    HazeError = None
    InvalidPeriodError = None
    InsufficientDataError = None
    ColumnNotFoundError = None
    InvalidParameterError = None
    ComputationError = None

# =========================================================================
# Deprecation warnings for legacy py_* functions
# =========================================================================
import warnings as _warnings
from functools import wraps as _wraps

# Build mapping of py_* names to clean names for deprecation warnings
_PY_PREFIX_ALIASES = {
    # Moving Averages
    "py_sma": "sma", "py_ema": "ema", "py_rma": "rma", "py_wma": "wma",
    "py_hma": "hma", "py_dema": "dema", "py_tema": "tema", "py_zlma": "zlma",
    "py_kama": "kama", "py_t3": "t3", "py_alma": "alma", "py_frama": "frama",
    "py_trima": "trima", "py_vidya": "vidya", "py_pwma": "pwma",
    "py_sinwma": "sinwma", "py_swma": "swma", "py_vwma": "vwma", "py_mama": "mama",
    # Volatility
    "py_true_range": "true_range", "py_atr": "atr", "py_natr": "natr",
    "py_bollinger_bands": "bollinger_bands", "py_keltner_channel": "keltner_channel",
    "py_donchian_channel": "donchian_channel", "py_aberration": "aberration",
    # Momentum
    "py_rsi": "rsi", "py_macd": "macd", "py_stochastic": "stochastic",
    "py_stochrsi": "stochrsi", "py_cci": "cci", "py_williams_r": "williams_r",
    "py_awesome_oscillator": "awesome_oscillator", "py_fisher_transform": "fisher_transform",
    "py_kdj": "kdj", "py_tsi": "tsi", "py_mom": "mom", "py_roc": "roc",
    "py_cmo": "cmo", "py_apo": "apo", "py_ppo": "ppo",
    "py_ultimate_oscillator": "ultimate_oscillator", "py_bop": "bop",
    "py_coppock": "coppock", "py_cti": "cti", "py_er": "er", "py_inertia": "inertia",
    "py_kst": "kst", "py_pgo": "pgo", "py_psl": "psl", "py_qqe": "qqe",
    "py_qstick": "qstick", "py_rvi": "rvi", "py_smi": "smi", "py_squeeze": "squeeze",
    "py_stc": "stc", "py_tdfi": "tdfi", "py_vhf": "vhf", "py_wae": "wae",
    # Trend
    "py_supertrend": "supertrend", "py_adx": "adx", "py_aroon": "aroon",
    "py_psar": "psar", "py_sar": "sar", "py_sarext": "sarext",
    "py_vortex": "vortex", "py_choppiness": "choppiness", "py_dx": "dx",
    "py_plus_di": "plus_di", "py_minus_di": "minus_di",
    "py_alligator": "alligator", "py_ichimoku_cloud": "ichimoku_cloud",
    "py_ssl_channel": "ssl_channel",
    # Volume
    "py_obv": "obv", "py_vwap": "vwap", "py_mfi": "mfi", "py_cmf": "cmf",
    "py_ad": "ad", "py_adosc": "adosc", "py_pvt": "pvt", "py_nvi": "nvi",
    "py_pvi": "pvi", "py_eom": "eom", "py_efi": "efi",
    "py_volume_profile": "volume_profile", "py_volume_filter": "volume_filter",
    # Statistical
    "py_linear_regression": "linear_regression", "py_linearreg": "linearreg",
    "py_linearreg_angle": "linearreg_angle", "py_linearreg_intercept": "linearreg_intercept",
    "py_linearreg_slope": "linearreg_slope", "py_correlation": "correlation",
    "py_correl": "correl", "py_zscore": "zscore", "py_var": "var",
    "py_standard_error": "standard_error", "py_beta": "beta",
    "py_covariance": "covariance", "py_entropy": "entropy",
    "py_percent_rank": "percent_rank", "py_slope": "slope", "py_tsf": "tsf",
    "py_bias": "bias", "py_cfo": "cfo",
    # Price transforms
    "py_avgprice": "avgprice", "py_medprice": "medprice", "py_typprice": "typprice",
    "py_wclprice": "wclprice", "py_midpoint": "midpoint", "py_midprice": "midprice",
    # Hilbert Transform
    "py_ht_dcperiod": "ht_dcperiod", "py_ht_dcphase": "ht_dcphase",
    "py_ht_phasor": "ht_phasor", "py_ht_sine": "ht_sine",
    "py_ht_trendmode": "ht_trendmode",
    # Pivots & Fibonacci
    "py_standard_pivots": "standard_pivots", "py_camarilla_pivots": "camarilla_pivots",
    "py_fibonacci_pivots": "fibonacci_pivots", "py_fib_retracement": "fib_retracement",
    "py_fib_extension": "fib_extension", "py_harmonics": "harmonics",
    "py_harmonics_patterns": "harmonics_patterns",
}


def __getattr__(name: str):
    """Handle deprecated py_* function access with warnings."""
    if name in _PY_PREFIX_ALIASES:
        new_name = _PY_PREFIX_ALIASES[name]
        _warnings.warn(
            f"'{name}' is deprecated, use '{new_name}' instead. "
            f"The py_ prefix will be removed in version 1.0.",
            DeprecationWarning,
            stacklevel=2,
        )
        # Return the actual function from this module
        return globals().get(new_name)
    raise AttributeError(f"module 'haze_library' has no attribute '{name}'")


# Public API exports (clean names without py_ prefix)
__all__ = [
    # Version
    "__version__",
    # Accessors
    "TechnicalAnalysisAccessor",
    "SeriesTechnicalAnalysisAccessor",
    # Compatibility modules
    "np_ta",
    "polars_ta",
    "torch_ta",
    # Moving Averages
    "sma", "ema", "rma", "wma", "hma", "dema", "tema", "zlma", "kama", "t3",
    "alma", "frama", "trima", "vidya", "pwma", "sinwma", "swma", "vwma", "mama",
    # Volatility
    "true_range", "atr", "natr", "bollinger_bands", "keltner_channel",
    "donchian_channel", "aberration",
    # Momentum
    "rsi", "macd", "stochastic", "stochrsi", "cci", "williams_r",
    "awesome_oscillator", "fisher_transform", "kdj", "tsi", "mom", "roc",
    "cmo", "apo", "ppo", "ultimate_oscillator", "bop", "coppock", "cti",
    "er", "inertia", "kst", "pgo", "psl", "qqe", "qstick", "rvi", "smi",
    "squeeze", "stc", "tdfi", "vhf", "wae",
    # Trend
    "supertrend", "adx", "aroon", "psar", "sar", "sarext", "vortex",
    "choppiness", "dx", "plus_di", "minus_di", "alligator", "ichimoku_cloud",
    "ssl_channel",
    # Volume
    "obv", "vwap", "mfi", "cmf", "ad", "adosc", "pvt", "nvi", "pvi", "eom",
    "efi", "volume_profile", "volume_filter",
    # Statistical
    "linear_regression", "linearreg", "linearreg_angle", "linearreg_intercept",
    "linearreg_slope", "correlation", "correl", "zscore", "var",
    "standard_error", "beta", "covariance", "entropy", "percent_rank",
    "slope", "tsf", "bias", "cfo",
    # Price transforms
    "avgprice", "medprice", "typprice", "wclprice", "midpoint", "midprice",
    # Hilbert Transform
    "ht_dcperiod", "ht_dcphase", "ht_phasor", "ht_sine", "ht_trendmode",
    # Pivots & Fibonacci
    "standard_pivots", "camarilla_pivots", "fibonacci_pivots",
    "fib_retracement", "fib_extension", "harmonics", "harmonics_patterns",
    # Candlestick Patterns
    "doji", "hammer", "inverted_hammer", "hanging_man", "shooting_star",
    "bullish_engulfing", "bearish_engulfing", "bullish_harami", "bearish_harami",
    "piercing_pattern", "dark_cloud_cover", "morning_star", "evening_star",
    "three_white_soldiers", "three_black_crows", "marubozu", "spinning_top",
    "dragonfly_doji", "gravestone_doji", "long_legged_doji", "tweezers_top",
    "tweezers_bottom", "rising_three_methods", "falling_three_methods",
    "harami_cross", "morning_doji_star", "evening_doji_star", "three_inside",
    "three_outside", "abandoned_baby", "kicking", "long_line", "short_line",
    "doji_star", "identical_three_crows", "stick_sandwich", "tristar",
    "upside_gap_two_crows", "gap_sidesidewhite", "takuri", "homing_pigeon",
    "matching_low", "separating_lines", "thrusting", "inneck", "onneck",
    "advance_block", "stalled_pattern", "belthold", "concealing_baby_swallow",
    "counterattack", "highwave", "hikkake", "hikkake_mod", "ladder_bottom",
    "mat_hold", "rickshaw_man", "closing_marubozu", "breakaway",
    "unique_3_river", "xside_gap_3_methods",
    # SFG Trading Signals
    "ai_supertrend", "ai_supertrend_ml", "atr2_signals", "atr2_signals_ml",
    "pivot_buy_sell", "ai_momentum_index", "ai_momentum_index_ml",
    "dynamic_macd", "swing_points", "fvg_signals", "detect_divergence",
    "calculate_stops", "combine_signals", "breaker_block_signals",
    "pd_array_signals", "general_parameters_signals",
    "linreg_supply_demand_signals",
    # Math functions
    "add", "sub", "mult", "div", "sqrt", "ln", "log10", "exp",
    "sin", "cos", "tan", "asin", "acos", "atan", "sinh", "cosh", "tanh",
    "ceil", "floor", "minmax", "minmaxindex",
]
