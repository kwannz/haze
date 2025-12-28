Technical Indicators API
========================

This page documents all available technical indicators in Haze-Library.

Moving Averages
---------------

Simple Moving Average (SMA)
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. function:: haze_library.sma(close, period=20)

   Calculate Simple Moving Average.

   :param close: Close prices as list or array
   :type close: list[float]
   :param period: Number of periods (default: 20)
   :type period: int
   :returns: SMA values
   :rtype: list[float]

   **Example:**

   .. code-block:: python

      import haze_library as haze

      close = [100.0, 101.0, 102.0, 101.5, 103.0]
      sma = haze.sma(close, period=3)

Exponential Moving Average (EMA)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. function:: haze_library.ema(close, period=20)

   Calculate Exponential Moving Average.

   :param close: Close prices
   :type close: list[float]
   :param period: EMA period (default: 20)
   :type period: int
   :returns: EMA values
   :rtype: list[float]

Additional Moving Averages
^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``wma(close, period)`` - Weighted Moving Average
- ``hma(close, period)`` - Hull Moving Average
- ``dema(close, period)`` - Double Exponential Moving Average
- ``tema(close, period)`` - Triple Exponential Moving Average
- ``kama(close, period, fast, slow)`` - Kaufman's Adaptive Moving Average
- ``zlma(close, period)`` - Zero Lag Moving Average
- ``alma(close, period, offset, sigma)`` - Arnaud Legoux Moving Average
- ``frama(close, period)`` - Fractal Adaptive Moving Average

Momentum Indicators
-------------------

Relative Strength Index (RSI)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. function:: haze_library.rsi(close, period=14)

   Calculate Relative Strength Index.

   RSI measures the magnitude of recent price changes to evaluate
   overbought or oversold conditions. Values range from 0 to 100.

   :param close: Close prices
   :type close: list[float]
   :param period: RSI period (default: 14)
   :type period: int
   :returns: RSI values (0-100)
   :rtype: list[float]

   **Interpretation:**

   - RSI > 70: Typically overbought
   - RSI < 30: Typically oversold

MACD
^^^^

.. function:: haze_library.macd(close, fast=12, slow=26, signal=9)

   Calculate Moving Average Convergence Divergence.

   :param close: Close prices
   :type close: list[float]
   :param fast: Fast EMA period (default: 12)
   :type fast: int
   :param slow: Slow EMA period (default: 26)
   :type slow: int
   :param signal: Signal line period (default: 9)
   :type signal: int
   :returns: Tuple of (macd_line, signal_line, histogram)
   :rtype: tuple[list[float], list[float], list[float]]

Stochastic Oscillator
^^^^^^^^^^^^^^^^^^^^^

.. function:: haze_library.stochastic(high, low, close, k_period=14, d_period=3)

   Calculate Stochastic Oscillator.

   :returns: Tuple of (%K, %D)
   :rtype: tuple[list[float], list[float]]

Additional Momentum Indicators
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``cci(high, low, close, period)`` - Commodity Channel Index
- ``williams_r(high, low, close, period)`` - Williams %R
- ``awesome_oscillator(high, low, fast, slow)`` - Awesome Oscillator
- ``tsi(close, fast, slow)`` - True Strength Index
- ``mom(close, period)`` - Momentum
- ``roc(close, period)`` - Rate of Change

Volatility Indicators
---------------------

Average True Range (ATR)
^^^^^^^^^^^^^^^^^^^^^^^^

.. function:: haze_library.atr(high, low, close, period=14)

   Calculate Average True Range.

   :param high: High prices
   :param low: Low prices
   :param close: Close prices
   :param period: ATR period (default: 14)
   :returns: ATR values
   :rtype: list[float]

Bollinger Bands
^^^^^^^^^^^^^^^

.. function:: haze_library.bollinger_bands(close, period=20, std=2.0)

   Calculate Bollinger Bands.

   :returns: Tuple of (upper_band, middle_band, lower_band)
   :rtype: tuple[list[float], list[float], list[float]]

Trend Indicators
----------------

SuperTrend
^^^^^^^^^^

.. function:: haze_library.supertrend(high, low, close, period=10, multiplier=3.0)

   Calculate SuperTrend indicator.

   :returns: Tuple of (trend, direction, upper_band, lower_band)
   :rtype: tuple[list[float], list[float], list[float], list[float]]

ADX (Average Directional Index)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. function:: haze_library.adx(high, low, close, period=14)

   Calculate Average Directional Index.

   :returns: Tuple of (adx, plus_di, minus_di)
   :rtype: tuple[list[float], list[float], list[float]]

Volume Indicators
-----------------

- ``obv(close, volume)`` - On Balance Volume
- ``vwap(high, low, close, volume)`` - Volume Weighted Average Price
- ``mfi(high, low, close, volume, period)`` - Money Flow Index
- ``cmf(high, low, close, volume, period)`` - Chaikin Money Flow
- ``ad(high, low, close, volume)`` - Accumulation/Distribution Line

ML-Enhanced Signal Indicators (SFG)
-----------------------------------

The SFG (Signal Force Generator) module provides ML-enhanced trading signal indicators.
See :doc:`pattern/sfg` for detailed documentation.

AI SuperTrend ML
^^^^^^^^^^^^^^^^

.. function:: haze_library.ai_supertrend_ml(high, low, close, st_length=10, st_multiplier=3.0, model_type="linreg", lookback=10, train_window=200)

   ML-enhanced SuperTrend indicator using linear/ridge regression.

   :returns: Tuple of (supertrend, direction, buy_signals, sell_signals, stop_loss, take_profit)
   :rtype: tuple[list[float], ...]

ATR2 Signals ML
^^^^^^^^^^^^^^^

.. function:: haze_library.atr2_signals_ml(high, low, close, volume, rsi_period=14, atr_period=14, ridge_alpha=1.0, momentum_window=10)

   ATR and momentum-based adaptive signal generator.

   :returns: Tuple of (rsi, buy_signals, sell_signals, signal_strength, stop_loss, take_profit)
   :rtype: tuple[list[float], ...]

AI Momentum Index ML
^^^^^^^^^^^^^^^^^^^^

.. function:: haze_library.ai_momentum_index_ml(close, rsi_period=14, smooth_period=3, use_polynomial=False, lookback=5, train_window=200)

   ML-enhanced momentum indicator with overbought/oversold detection.

   :returns: Tuple of (rsi, predicted_momentum, zero_cross_buy, zero_cross_sell, overbought, oversold)
   :rtype: tuple[list[float], ...]

General Parameters Signals
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. function:: haze_library.general_parameters_signals(high, low, close, ema_fast=20, ema_slow=50, atr_period=14, grid_multiplier=1.0)

   EMA channel with grid trading signals.

   :returns: Tuple of (buy_signals, sell_signals, stop_loss, take_profit)
   :rtype: tuple[list[float], list[float], list[float], list[float]]
