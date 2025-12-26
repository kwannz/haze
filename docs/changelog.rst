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

[0.1.0] - 2025-12-26
--------------------

Initial release.

Added
^^^^^
- 200+ technical indicators
- Pandas DataFrame accessor (``.ta``)
- NumPy compatibility layer
- High-performance Rust core
- Python 3.9+ support
