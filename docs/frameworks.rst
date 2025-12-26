Multi-Framework Support
=======================

Haze-Library supports multiple data frameworks beyond pandas.

Polars Integration
------------------

`Polars <https://www.pola.rs/>`_ is a fast DataFrame library implemented in Rust.

.. code-block:: python

   import polars as pl
   from haze_library import polars_ta

   # Create DataFrame
   df = pl.DataFrame({
       'open': [100.0, 101.0, 102.0, 101.5, 103.0],
       'high': [101.0, 102.0, 103.0, 102.5, 104.0],
       'low': [99.0, 100.0, 101.0, 100.5, 102.0],
       'close': [100.5, 101.5, 102.5, 101.0, 103.5],
       'volume': [1000.0, 1100.0, 1200.0, 1150.0, 1300.0],
   })

   # Calculate indicators
   df = polars_ta.sma(df, 'close', period=3)
   df = polars_ta.rsi(df, 'close', period=3)
   df = polars_ta.bollinger_bands(df, 'close', period=3)

   print(df)

Available Polars Functions
^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``polars_ta.sma(df, column, period, result_column=None)``
- ``polars_ta.ema(df, column, period, result_column=None)``
- ``polars_ta.rsi(df, column, period, result_column=None)``
- ``polars_ta.macd(df, column, fast, slow, signal)``
- ``polars_ta.bollinger_bands(df, column, period, std)``
- ``polars_ta.atr(df, period)``
- ``polars_ta.supertrend(df, period, multiplier)``
- ``polars_ta.obv(df)``
- ``polars_ta.vwap(df)``

PyTorch Integration
-------------------

`PyTorch <https://pytorch.org/>`_ tensors are supported for ML workflows.

.. code-block:: python

   import torch
   from haze_library import torch_ta

   # Create tensors
   close = torch.tensor([100.0, 101.0, 102.0, 101.5, 103.0, 102.5, 104.0])
   high = torch.tensor([101.0, 102.0, 103.0, 102.5, 104.0, 103.5, 105.0])
   low = torch.tensor([99.0, 100.0, 101.0, 100.5, 102.0, 101.5, 103.0])

   # Calculate indicators (returns tensors)
   sma = torch_ta.sma(close, period=3)
   rsi = torch_ta.rsi(close, period=5)
   macd_line, signal, histogram = torch_ta.macd(close, 3, 5, 2)

   print(f"SMA: {sma}")
   print(f"RSI: {rsi}")

Device Preservation
^^^^^^^^^^^^^^^^^^^

PyTorch tensors maintain their device:

.. code-block:: python

   # GPU tensor (if available)
   if torch.cuda.is_available():
       close_gpu = close.cuda()
       sma_gpu = torch_ta.sma(close_gpu, period=5)
       assert sma_gpu.device == close_gpu.device

NumPy Integration
-----------------

NumPy arrays work directly with the core functions:

.. code-block:: python

   import numpy as np
   import haze_library as haze

   close = np.array([100.0, 101.0, 102.0, 101.5, 103.0])

   # Pass numpy arrays directly
   sma = haze.sma(close.tolist(), 3)

   # Or use the np_ta module
   from haze_library import np_ta

   sma = np_ta.sma(close, period=3)

Framework Comparison
--------------------

+-------------+-------------+------------------+-------------+
| Framework   | Performance | Memory Overhead  | Use Case    |
+=============+=============+==================+=============+
| Pandas      | Baseline    | Moderate         | General use |
+-------------+-------------+------------------+-------------+
| Polars      | Faster      | Lower            | Big data    |
+-------------+-------------+------------------+-------------+
| PyTorch     | Baseline    | Higher           | ML pipeline |
+-------------+-------------+------------------+-------------+
| NumPy       | Fastest     | Lowest           | Low-level   |
+-------------+-------------+------------------+-------------+
