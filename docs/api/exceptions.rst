Exceptions API
==============

Haze-Library provides custom exception types for better error handling.
All exceptions inherit from ``HazeError``, allowing you to catch all
library-specific errors with a single except clause.

Exception Hierarchy
-------------------

.. code-block:: text

   HazeError (base class)
   ├── InvalidPeriodError
   ├── InsufficientDataError
   ├── ColumnNotFoundError
   ├── InvalidParameterError
   └── ComputationError

HazeError
---------

.. autoclass:: haze_library.exceptions.HazeError
   :members:

InvalidPeriodError
------------------

.. autoclass:: haze_library.exceptions.InvalidPeriodError
   :members:

Raised when the period parameter is invalid (e.g., larger than data length).

**Example:**

.. code-block:: python

   from haze_library import sma, InvalidPeriodError

   try:
       result = sma([1.0, 2.0, 3.0], period=100)  # period > data length
   except InvalidPeriodError as e:
       print(f"Invalid period: {e.period}, data length: {e.data_length}")

InsufficientDataError
---------------------

.. autoclass:: haze_library.exceptions.InsufficientDataError
   :members:

Raised when there's not enough data for the calculation.

ColumnNotFoundError
-------------------

.. autoclass:: haze_library.exceptions.ColumnNotFoundError
   :members:

Raised when a required column is not found in the DataFrame.

**Example:**

.. code-block:: python

   from haze_library import ColumnNotFoundError

   try:
       df.ta.sma(20, column='price')  # 'price' doesn't exist
   except ColumnNotFoundError as e:
       print(f"Column '{e.column}' not found. Available: {e.available}")

InvalidParameterError
---------------------

.. autoclass:: haze_library.exceptions.InvalidParameterError
   :members:

Raised when a parameter value is invalid.

ComputationError
----------------

.. autoclass:: haze_library.exceptions.ComputationError
   :members:

Raised when computation fails unexpectedly.

Validation Functions
--------------------

.. autofunction:: haze_library.exceptions.validate_period

.. autofunction:: haze_library.exceptions.validate_data_length

Error Handling Best Practices
-----------------------------

**Catch all library errors:**

.. code-block:: python

   from haze_library import HazeError

   try:
       result = df.ta.rsi(14)
   except HazeError as e:
       print(f"Calculation failed: {e}")

**Catch specific errors:**

.. code-block:: python

   from haze_library import InvalidPeriodError, ColumnNotFoundError

   try:
       result = df.ta.sma(100, column='close')
   except InvalidPeriodError:
       print("Period too large for data")
   except ColumnNotFoundError:
       print("Column not found")
