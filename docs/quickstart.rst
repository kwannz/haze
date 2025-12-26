Quick Start Guide
=================

This guide will help you get started with Haze-Library in 5 minutes.

Basic Usage
-----------

.. code-block:: python

   import haze_library as haze

   # Sample data
   close = [100.0, 101.0, 102.0, 101.5, 103.0, 102.5, 104.0, 103.5, 105.0]

   # Calculate indicators
   sma_3 = haze.sma(close, 3)
   ema_5 = haze.ema(close, 5)
   rsi_7 = haze.rsi(close, 7)

   print(f"SMA: {sma_3}")
   print(f"EMA: {ema_5}")
   print(f"RSI: {rsi_7}")

DataFrame Integration
---------------------

Haze-Library integrates seamlessly with pandas:

.. code-block:: python

   import pandas as pd
   import haze_library

   # Create sample DataFrame
   df = pd.DataFrame({
       'open': [100.0, 101.0, 102.0, 101.5, 103.0],
       'high': [101.0, 102.0, 103.0, 102.5, 104.0],
       'low': [99.0, 100.0, 101.0, 100.5, 102.0],
       'close': [100.5, 101.5, 102.5, 101.0, 103.5],
       'volume': [1000, 1100, 1200, 1150, 1300],
   })

   # Use the .ta accessor
   df['sma_3'] = df.ta.sma(3)
   df['rsi'] = df.ta.rsi(3)
   df['atr'] = df.ta.atr(3)

   print(df)

Common Indicators
-----------------

Moving Averages
^^^^^^^^^^^^^^^

.. code-block:: python

   # Simple Moving Average
   sma = haze.sma(close, 20)

   # Exponential Moving Average
   ema = haze.ema(close, 12)

   # Hull Moving Average
   hma = haze.hma(close, 9)

Momentum
^^^^^^^^

.. code-block:: python

   # RSI
   rsi = haze.rsi(close, 14)

   # MACD
   macd_line, signal_line, histogram = haze.macd(close, 12, 26, 9)

   # Stochastic
   k, d = haze.stochastic(high, low, close, 14, 3)

Volatility
^^^^^^^^^^

.. code-block:: python

   # ATR
   atr = haze.atr(high, low, close, 14)

   # Bollinger Bands
   upper, middle, lower = haze.bollinger_bands(close, 20, 2.0)

Trend
^^^^^

.. code-block:: python

   # SuperTrend
   trend, direction, ub, lb = haze.supertrend(high, low, close, 10, 3.0)

   # ADX
   adx, plus_di, minus_di = haze.adx(high, low, close, 14)

Next Steps
----------

- See :doc:`frameworks` for multi-framework support (Polars, PyTorch)
- Browse the :doc:`api/indicators` for all 200+ indicators
- Check :doc:`api/accessor` for DataFrame integration details
