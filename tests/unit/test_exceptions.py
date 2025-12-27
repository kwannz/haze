"""
Exception Tests
===============

Test custom exception types and validation functions.

Author: Haze Team
Date: 2025-12-26
"""

import pytest
import sys
import os

# Add parent to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../rust/python'))

from haze_library.exceptions import (
    HazeError,
    InvalidPeriodError,
    InsufficientDataError,
    ColumnNotFoundError,
    InvalidParameterError,
    ComputationError,
    validate_period,
    validate_data_length,
    require_columns,
)


class TestExceptionHierarchy:
    """Test exception class hierarchy."""

    def test_haze_error_is_base(self):
        """Test that HazeError is the base class."""
        assert issubclass(InvalidPeriodError, HazeError)
        assert issubclass(InsufficientDataError, HazeError)
        assert issubclass(ColumnNotFoundError, HazeError)
        assert issubclass(InvalidParameterError, HazeError)
        assert issubclass(ComputationError, HazeError)

    def test_can_catch_all_with_base(self):
        """Test that all exceptions can be caught with HazeError."""
        with pytest.raises(HazeError):
            raise InvalidPeriodError(100, 50, "SMA")

        with pytest.raises(HazeError):
            raise InsufficientDataError(100, 50, "RSI")

        with pytest.raises(HazeError):
            raise ColumnNotFoundError("close", ["open", "high"])


class TestInvalidPeriodError:
    """Test InvalidPeriodError."""

    def test_error_message(self):
        """Test error message formatting."""
        err = InvalidPeriodError(100, 50, "SMA", min_period=1)
        assert "100" in str(err)
        assert "SMA" in str(err)
        assert "50" in str(err)

    def test_attributes(self):
        """Test error attributes."""
        err = InvalidPeriodError(100, 50, "SMA", min_period=2)
        assert err.period == 100
        assert err.data_length == 50
        assert err.indicator == "SMA"
        assert err.min_period == 2


class TestInsufficientDataError:
    """Test InsufficientDataError."""

    def test_error_message(self):
        """Test error message formatting."""
        err = InsufficientDataError(100, 50, "RSI")
        assert "100" in str(err)
        assert "50" in str(err)
        assert "RSI" in str(err)

    def test_attributes(self):
        """Test error attributes."""
        err = InsufficientDataError(100, 50, "RSI")
        assert err.required == 100
        assert err.provided == 50
        assert err.indicator == "RSI"


class TestColumnNotFoundError:
    """Test ColumnNotFoundError."""

    def test_error_message(self):
        """Test error message formatting."""
        err = ColumnNotFoundError("close", ["open", "high", "low"])
        assert "close" in str(err)
        assert "open" in str(err)

    def test_with_indicator(self):
        """Test error message with indicator name."""
        err = ColumnNotFoundError("close", ["open"], indicator="RSI")
        assert "close" in str(err)
        assert "RSI" in str(err)


class TestValidationFunctions:
    """Test validation helper functions."""

    def test_validate_period_valid(self):
        """Test that valid period doesn't raise."""
        # Should not raise
        validate_period(10, 100, "SMA")
        validate_period(1, 100, "SMA", min_period=1)

    def test_validate_period_too_small(self):
        """Test that period < min raises."""
        with pytest.raises(InvalidPeriodError):
            validate_period(0, 100, "SMA", min_period=1)

    def test_validate_period_too_large(self):
        """Test that period > data_length raises."""
        with pytest.raises(InvalidPeriodError):
            validate_period(101, 100, "SMA")

    def test_validate_data_length_valid(self):
        """Test that sufficient data doesn't raise."""
        # Should not raise
        validate_data_length(100, 50, "RSI")

    def test_validate_data_length_insufficient(self):
        """Test that insufficient data raises."""
        with pytest.raises(InsufficientDataError):
            validate_data_length(50, 100, "RSI")


class TestAdditionalExceptionCoverage:
    def test_invalid_parameter_error_message(self):
        err = InvalidParameterError("period", -1, indicator="SMA")
        assert "period" in str(err)
        assert "SMA" in str(err)

    def test_computation_error_message(self):
        err = ComputationError("RSI", "overflow")
        assert "RSI" in str(err)
        assert "overflow" in str(err)

    def test_require_columns(self):
        with pytest.raises(ColumnNotFoundError):
            require_columns(["open", "high"], ["close"], indicator="SMA")
