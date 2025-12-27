Installation
============

Requirements
------------

- Python 3.14 or higher
- Rust 1.75 or higher (for building from source)

Install from PyPI
-----------------

.. code-block:: bash

   pip install haze-library

If you want to ensure you always install a prebuilt wheel (no local Rust build),
you can force binary-only installs:

.. code-block:: bash

   pip install --only-binary=:all: haze-library

Install from Source
-------------------

1. Clone the repository:

   .. code-block:: bash

      git clone https://github.com/your-org/haze-library.git
      cd haze-library

2. Install Rust (if not already installed):

   .. code-block:: bash

      curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

3. Build and install:

   .. code-block:: bash

      pip install maturin
      maturin develop --release

Optional Dependencies
---------------------

For CCXT execution helpers:

.. code-block:: bash

   pip install haze-library[execution]

For Polars support:

.. code-block:: bash

   pip install polars

For PyTorch support:

.. code-block:: bash

   pip install torch

Verify Installation
-------------------

.. code-block:: python

   import haze_library
   print(haze_library.__version__)

   # Test a simple calculation
   close = [100.0, 101.0, 102.0, 101.5, 103.0]
   sma = haze_library.sma(close, 3)
   print(sma)
