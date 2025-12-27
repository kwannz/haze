Haze-Library Documentation
===========================

.. image:: https://img.shields.io/badge/python-3.14%2B-blue
   :alt: Python 3.14+

.. image:: https://img.shields.io/badge/rust-1.75%2B-orange
   :alt: Rust 1.75+

**Haze-Library** is a high-performance quantitative trading indicators library
powered by Rust with Python bindings. It provides 200+ technical indicators
with 5-10x faster performance than pure Python implementations.

.. note::

   This project is under active development.

Quick Start
-----------

Installation
^^^^^^^^^^^^

.. code-block:: bash

   pip install haze-library

Basic Usage
^^^^^^^^^^^

.. code-block:: python

   import haze_library as haze

   # Calculate indicators directly
   close = [100.0, 101.0, 102.0, 101.5, 103.0, ...]

   sma_20 = haze.sma(close, 20)
   rsi_14 = haze.rsi(close, 14)
   macd_line, signal, histogram = haze.macd(close, 12, 26, 9)

DataFrame Accessor
^^^^^^^^^^^^^^^^^^

.. code-block:: python

   import pandas as pd
   import haze_library

   df = pd.read_csv('ohlcv.csv')

   # Using the .haze accessor
   df['sma_20'] = df.haze.sma(20)
   df['rsi_14'] = df.haze.rsi(14)
   upper, middle, lower = df.haze.bollinger_bands(20, 2.0)

Multi-Framework Support
^^^^^^^^^^^^^^^^^^^^^^^

Haze-Library supports multiple data frameworks:

**Polars DataFrames:**

.. code-block:: python

   import polars as pl
   from haze_library import polars_ta

   df = pl.read_csv('ohlcv.csv')
   df = polars_ta.sma(df, 'close', 20)
   df = polars_ta.rsi(df, 'close', 14)

**PyTorch Tensors:**

.. code-block:: python

   import torch
   from haze_library import torch_ta

   close = torch.tensor([100.0, 101.0, ...])
   sma = torch_ta.sma(close, period=20)
   rsi = torch_ta.rsi(close, period=14)

Contents
--------

.. toctree::
   :maxdepth: 2
   :caption: User Guide

   installation
   quickstart
   frameworks

.. toctree::
   :maxdepth: 2
   :caption: API Reference

   api/indicators
   api/accessor
   api/exceptions

.. toctree::
   :maxdepth: 1
   :caption: Development

   contributing
   changelog

Indices and Tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
