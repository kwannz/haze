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

[1.0.0] - 2025-12-27
--------------------

Changed
^^^^^^^
- Parallel utilities return ``HazeResult`` and fail fast on invalid inputs
  (``parallel_sma``, ``parallel_ema``, ``parallel_rsi``, ``parallel_atr``,
  ``parallel_multi_period_sma``, ``parallel_multi_period_ema``).
- AI indicators (``adaptive_rsi``, ``ensemble_signal``, ``ml_supertrend``) are exported at
  the top-level and enforce strict parameter/length validation (fail-fast).

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
