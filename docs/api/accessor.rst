DataFrame Accessor API
======================

Haze-Library provides a ```.haze``` accessor for pandas DataFrames,
allowing you to call technical indicators directly on your data.

TechnicalAnalysisAccessor
-------------------------

.. autoclass:: haze_library.accessor.TechnicalAnalysisAccessor
   :members:
   :undoc-members:

Usage
^^^^^

.. code-block:: python

   import pandas as pd
   import haze_library  # Registers the accessor

   df = pd.read_csv('ohlcv.csv')

   # Single return value indicators
   df['sma_20'] = df.haze.sma(20)
   df['rsi_14'] = df.haze.rsi(14)
   df['atr_14'] = df.haze.atr(14)

   # Multiple return value indicators
   upper, middle, lower = df.haze.bollinger_bands(20, 2.0)
   df['bb_upper'] = upper
   df['bb_middle'] = middle
   df['bb_lower'] = lower

   # Trend indicators
   st, direction, ub, lb = df.haze.supertrend(10, 3.0)
   df['supertrend'] = st
   df['trend_direction'] = direction

SeriesTechnicalAnalysisAccessor
-------------------------------

.. autoclass:: haze_library.accessor.SeriesTechnicalAnalysisAccessor
   :members:
   :undoc-members:

Usage
^^^^^

.. code-block:: python

   import pandas as pd
   import haze_library

   close = df['close']

   # Apply indicators to a single Series
   sma = close.haze.sma(20)
   ema = close.haze.ema(12)
   rsi = close.haze.rsi(14)
