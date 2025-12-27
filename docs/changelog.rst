Changelog
=========

All notable changes to this project will be documented in this file.

The format is based on `Keep a Changelog <https://keepachangelog.com/>`_,
and this project adheres to `Semantic Versioning <https://semver.org/>`_.

[Unreleased]
------------

Added
^^^^^
- Polars DataFrame integration (fallback mode)
- PyTorch tensor support
- Custom exception types (HazeError hierarchy)
- Enhanced type hints and docstrings
- Sphinx documentation

Changed
^^^^^^^
- Clean API names (sma instead of py_sma)
- Deprecation warnings for legacy py_* functions

[1.0.1] - 2025-12-28
--------------------

Changed
^^^^^^^
- Updated Rust dependency pins to latest compatible patch versions (linfa 0.8.1, thiserror 2.0.17,
  ndarray 0.16.1, criterion 0.8.1, bincode 2.0.1).
- Raised maturin minimum version to 1.10.2 for Python builds.

Fixed
^^^^^
- Mass Index doc example now uses sufficient input length to avoid ``InsufficientData`` errors.

[1.0.0] - 2025-12-27
--------------------

Changed
^^^^^^^
- Parallel utilities return ``HazeResult`` and fail fast on invalid inputs
  (``parallel_sma``, ``parallel_ema``, ``parallel_rsi``, ``parallel_atr``,
  ``parallel_multi_period_sma``, ``parallel_multi_period_ema``).
- AI indicators (``adaptive_rsi``, ``ensemble_signal``, ``ml_supertrend``) are exported at
  the top-level and enforce strict parameter/length validation (fail-fast).
- Streaming incremental indicators now raise on non-finite inputs instead of
  propagating NaN, aligning streaming APIs with fail-fast behavior.
- Python runtime deps now require ``numpy>=2.4.0`` and ``pandas>=2.3.3`` to match
  Python 3.14 support.

Fixed
^^^^^
- ``vhf`` now raises ``InsufficientData`` when ``period >= data_len``.
- ``pvt``, ``nvi``, ``pvi``, ``eom`` now raise ``InsufficientData`` when input length < 2.
- ``volume_profile`` now raises ``ParameterOutOfRange`` when ``num_bins == 0``.
- Online adaptive RSI uses Kahan summation for gain/loss windows to reduce drift.
- Regenerated ``tests/fixtures/golden_indicators_v1.json`` after fail-fast updates.

Migration Notes
^^^^^^^^^^^^^^^
- Update parallel calls to handle ``Result`` (use ``?`` or ``.unwrap()``).
- Ensure ``pvt``, ``nvi``, ``pvi``, ``eom`` inputs contain at least 2 data points.
- Pass ``num_bins >= 1`` for ``volume_profile``.
- AI indicators now require ``base_period`` within ``[min_period, max_period]``, and
  ``min_period``, ``max_period``, ``volatility_window``, and ``period`` must be ``< data length``.
  ``ml_supertrend`` now errors if ``confirmation_bars`` exceeds data length.
- Streaming updates now raise ``ValueError`` on NaN/Inf inputs; remove any caller-side
  reliance on NaN propagation for ``IncrementalSMA`` and ``IncrementalAdaptiveRSI``.

[0.1.0] - 2025-12-26
--------------------

Initial release.

Added
^^^^^
- 200+ technical indicators
- Pandas DataFrame accessor (``.haze``)
- NumPy compatibility layer
- High-performance Rust core
- Python 3.14+ support
