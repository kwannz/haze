DataFrame Accessor API
======================

Haze-Library provides a ```.ta``` accessor for pandas DataFrames,
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
   df['sma_20'] = df.ta.sma(20)
   df['rsi_14'] = df.ta.rsi(14)
   df['atr_14'] = df.ta.atr(14)

   # Multiple return value indicators
   upper, middle, lower = df.ta.bollinger_bands(20, 2.0)
   df['bb_upper'] = upper
   df['bb_middle'] = middle
   df['bb_lower'] = lower

   # Trend indicators
   st, direction, ub, lb = df.ta.supertrend(10, 3.0)
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
   sma = close.ta.sma(20)
   ema = close.ta.ema(12)
   rsi = close.ta.rsi(14)
