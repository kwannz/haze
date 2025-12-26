Contributing
============

We welcome contributions to Haze-Library!

Development Setup
-----------------

1. Fork and clone the repository:

   .. code-block:: bash

      git clone https://github.com/YOUR-USERNAME/haze-library.git
      cd haze-library

2. Install Rust:

   .. code-block:: bash

      curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

3. Create a virtual environment:

   .. code-block:: bash

      python -m venv .venv
      source .venv/bin/activate  # Linux/macOS
      # or
      .venv\Scripts\activate  # Windows

4. Install development dependencies:

   .. code-block:: bash

      pip install maturin pytest numpy pandas polars torch

5. Build the package:

   .. code-block:: bash

      maturin develop

Running Tests
-------------

.. code-block:: bash

   pytest tests/

Code Style
----------

- **Rust**: Follow Rust formatting guidelines (use ``cargo fmt``)
- **Python**: Follow PEP 8 (use ``black`` and ``ruff``)

Pull Request Process
--------------------

1. Create a feature branch from ``main``
2. Make your changes with tests
3. Ensure all tests pass
4. Update documentation if needed
5. Submit a pull request

Adding New Indicators
---------------------

1. Implement the indicator in Rust (``rust/src/indicators/``)
2. Add Python bindings (``rust/src/lib.rs``)
3. Add accessor method (``accessor.py``)
4. Add tests (``tests/unit/``)
5. Update documentation
