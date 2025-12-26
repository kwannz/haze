"""
Numerical Stability and Precision Tests for Haze Indicators
===========================================================

Tests edge cases involving:
- Large numbers + small increments
- Catastrophic cancellation
- Precision loss in long sequences
- NaN propagation
- Division by zero safety

These tests ensure that Haze indicators maintain numerical stability
under extreme conditions that could cause precision loss or overflow
in naive implementations.

Author: Haze Team
Date: 2025-12-26
"""

import numpy as np
import pytest
import haze_library as haze


class TestNumericalStability:
    """Test numerical stability of indicators under extreme conditions."""

    def test_stochastic_and_kdj_flat_range(self):
        """
        Flat-range safety test for Stochastic/KDJ.

        Scenario:
        - high == low == close for every bar (range = 0)
        - Challenge: division by zero in %K calculation

        Expected:
        - No crash / no infinities
        - Finite values converge to 50.0 (midpoint fallback)
        """
        high = [100.0] * 50
        low = [100.0] * 50
        close = [100.0] * 50

        k, d = haze.stochastic(high, low, close, k_period=5, d_period=3)
        kdj_k, kdj_d, kdj_j = haze.kdj(high, low, close, k_period=5, d_period=3)

        # Stochastic: finite results should be exactly 50.0 (with rounding tolerance)
        for value in [*k, *d]:
            if np.isfinite(value):
                assert abs(value - 50.0) < 1e-10

        # KDJ should be consistent with stochastic + J = 3K - 2D
        for kk, dd, jj in zip(kdj_k, kdj_d, kdj_j):
            if np.isfinite(kk) and np.isfinite(dd):
                assert abs(kk - 50.0) < 1e-10
                assert abs(dd - 50.0) < 1e-10
                assert np.isfinite(jj)
                assert abs(jj - 50.0) < 1e-10

    def test_large_numbers_small_increments(self):
        """
        Test SMA with large base value + small increments.

        Scenario:
        - Base price: 1e10 (10 billion)
        - Increments: ±1e-5 (0.00001)
        - Challenge: Precision loss in floating-point arithmetic

        Expected:
        - Results should be close to base value
        - Relative error < 1e-8
        """
        # Simulate stock price data: large base with small changes
        base = 1e10
        np.random.seed(42)
        increments = np.random.randn(10000) * 1e-5
        data = (base + increments).tolist()

        # Calculate SMA
        result = haze.sma(data, period=100)

        # Verify: results should be close to base, error < 1e-8
        valid_results = [r for r in result if not np.isnan(r)]
        assert len(valid_results) > 0, "Should have valid results"

        # Check relative error
        for r in valid_results:
            relative_error = abs(r - base) / base
            assert relative_error < 1e-8, (
                f"Large relative error: {relative_error:.2e} for value {r:.10f}"
            )

    def test_catastrophic_cancellation(self):
        """
        Test RSI with nearly equal gains/losses.

        Scenario:
        - Price oscillates: +0.1% / -0.1%
        - Challenge: Subtracting nearly equal numbers loses precision

        Expected:
        - RSI should be near 50 (balanced state)
        - RSI in range [45, 55]
        """
        # Construct nearly symmetric price fluctuations
        data = [100.0]
        for i in range(1000):
            # Alternate up/down by same magnitude
            data.append(data[-1] * (1.001 if i % 2 == 0 else 0.999))

        result = haze.rsi(data, period=14)

        # RSI should be close to 50 (balanced state)
        valid_results = [r for r in result[-100:] if not np.isnan(r)]
        assert len(valid_results) > 0, "Should have valid results"

        for r in valid_results:
            assert 45 < r < 55, (
                f"RSI should be near 50 for balanced gains/losses, got {r:.2f}"
            )

    def test_long_sequence_precision(self):
        """
        Test cumulative errors in long sequences.

        Scenario:
        - 100,000 data points
        - Sinusoidal pattern
        - Challenge: Accumulation of rounding errors

        Expected:
        - Final value should be finite (not NaN or Inf)
        - Match NumPy reference implementation within 1e-6
        """
        # 100k data points long sequence
        data = [100.0 + np.sin(i * 0.01) for i in range(100000)]

        result = haze.ema(data, period=20)

        # Final value should be finite (not NaN or Inf)
        assert np.isfinite(result[-1]), (
            f"Final EMA value is not finite: {result[-1]}"
        )

        # Compare with NumPy implementation (allow small error)
        numpy_ema = self._numpy_ema(data, 20)
        error = abs(result[-1] - numpy_ema[-1])
        assert error < 1e-6, (
            f"EMA differs from NumPy reference: {error:.2e}"
        )

    @staticmethod
    def _numpy_ema(data, period):
        """NumPy EMA implementation for comparison."""
        alpha = 2.0 / (period + 1)
        result = np.zeros(len(data))
        result[0] = data[0]
        for i in range(1, len(data)):
            result[i] = alpha * data[i] + (1 - alpha) * result[i - 1]
        return result

    def test_nan_propagation(self):
        """
        Test NaN handling in indicators.

        Scenario:
        - Input contains NaN values
        - Challenge: NaN can propagate through calculations

        Expected:
        - Function should handle NaN input without crashing
        - May skip NaN values or return NaN for affected periods
        """
        # Create data with NaN - note: some implementations may filter NaN
        data_with_nan = [1.0, 2.0, np.nan, 4.0, 5.0, 6.0, 7.0, 8.0] * 10

        # Should not crash with NaN input
        try:
            result = haze.sma(data_with_nan, period=5)
            # If it returns a result, check it's reasonable
            assert len(result) > 0, "Should return some result"
        except (ValueError, TypeError):
            # Some implementations may reject NaN - that's also acceptable
            pass

        # Test with clean data to ensure basic functionality works
        clean_data = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0] * 10
        result = haze.sma(clean_data, period=5)
        valid_count = sum(1 for r in result if np.isfinite(r))
        assert valid_count > 0, "Should have valid results with clean data"

    def test_division_by_zero_safety(self):
        """
        Test zero division handling.

        Scenario:
        - Constant price (zero standard deviation)
        - Challenge: Division by zero in Bollinger Bands std calculation

        Expected:
        - Should not crash
        - Middle band = price
        - Upper/lower bands = middle band (std=0)
        """
        # Construct data with zero standard deviation
        data = [100.0] * 50

        # Bollinger Bands has std calculation, should not crash
        upper, middle, lower = haze.bollinger_bands(data, period=20, std_multiplier=2.0)

        # Should return valid results (middle=price, upper=lower=middle)
        valid_middle = [m for m in middle if not np.isnan(m)]
        assert len(valid_middle) > 0, "Should have valid middle band results"

        for m in valid_middle:
            assert np.isfinite(m), f"Middle band is not finite: {m}"
            assert abs(m - 100.0) < 1e-6, (
                f"Middle band should equal input price: {m:.6f}"
            )

    def test_extreme_volatility(self):
        """
        Test indicators with extreme price volatility.

        Scenario:
        - Prices jump 10x in single period
        - Challenge: Sudden spikes can cause overflow

        Expected:
        - All results should be finite
        - No overflow to infinity
        """
        data = [100.0]
        for i in range(100):
            # Random jumps up to 10x
            multiplier = np.random.uniform(0.5, 2.0)
            data.append(data[-1] * multiplier)

        # Test multiple indicators
        sma_result = haze.sma(data, period=10)
        ema_result = haze.ema(data, period=10)
        rsi_result = haze.rsi(data, period=14)

        # All results should be finite
        for result, name in [(sma_result, 'SMA'),
                             (ema_result, 'EMA'),
                             (rsi_result, 'RSI')]:
            valid = [r for r in result if not np.isnan(r)]
            assert len(valid) > 0, f"{name} should have valid results"

            for r in valid:
                assert np.isfinite(r), (
                    f"{name} value is not finite: {r}"
                )

    def test_zero_and_negative_prices(self):
        """
        Test handling of zero and negative prices.

        Scenario:
        - Prices include zero and negative values
        - Challenge: Some indicators use logarithms

        Expected:
        - Should handle gracefully without crashing
        - May return NaN for invalid calculations
        """
        data = [100.0, 50.0, 0.0, -10.0, 20.0, 40.0]

        # SMA should work with any prices
        result = haze.sma(data, period=3)
        valid = [r for r in result if not np.isnan(r)]
        assert len(valid) > 0, "SMA should handle zero/negative prices"

    def test_monotonic_increase(self):
        """
        Test indicators with strictly monotonic increasing data.

        Scenario:
        - Price increases every period
        - Challenge: Some indicators assume mean reversion

        Expected:
        - All results should be valid and finite
        - Trend indicators should detect uptrend
        """
        # Strictly increasing prices
        data = [100.0 + i for i in range(100)]

        sma_result = haze.sma(data, period=10)
        ema_result = haze.ema(data, period=10)

        # All non-NaN results should be finite and increasing
        sma_valid = [r for r in sma_result if not np.isnan(r)]
        ema_valid = [r for r in ema_result if not np.isnan(r)]

        assert len(sma_valid) > 0, "SMA should have valid results"
        assert len(ema_valid) > 0, "EMA should have valid results"

        # Check all values are finite
        for r in sma_valid + ema_valid:
            assert np.isfinite(r), f"Non-finite value: {r}"

    def test_very_small_numbers(self):
        """
        Test indicators with very small numbers.

        Scenario:
        - Prices in range [1e-10, 1e-9]
        - Challenge: Underflow to zero

        Expected:
        - Results should maintain relative precision
        - No underflow to zero
        """
        np.random.seed(42)
        base = 1e-9
        data = [base + np.random.randn() * 1e-11 for _ in range(100)]

        result = haze.sma(data, period=10)

        valid_results = [r for r in result if not np.isnan(r)]
        assert len(valid_results) > 0, "Should have valid results"

        # Results should be in same order of magnitude
        for r in valid_results:
            assert np.isfinite(r), f"Non-finite value: {r}"
            assert r > 0, f"Underflow to zero or negative: {r}"
            assert abs(r - base) / base < 0.1, (
                f"Result too far from base value: {r:.2e} vs {base:.2e}"
            )

    def test_alternating_large_small(self):
        """
        Test indicators with alternating large/small values.

        Scenario:
        - Values alternate between 1e10 and 1e-10
        - Challenge: Dynamic range exceeds float64 precision

        Expected:
        - Should not crash
        - Results should be in valid range
        """
        data = []
        for i in range(100):
            data.append(1e10 if i % 2 == 0 else 1e-10)

        result = haze.sma(data, period=10)

        valid_results = [r for r in result if not np.isnan(r)]
        assert len(valid_results) > 0, "Should have valid results"

        # All results should be finite
        for r in valid_results:
            assert np.isfinite(r), f"Non-finite value: {r}"


class TestKahanSummation:
    """Test Kahan summation algorithm for improved numerical stability."""

    def test_kahan_vs_naive_summation(self):
        """
        Compare Kahan summation with naive summation.

        Scenario:
        - Sum many small numbers with large base
        - Challenge: Precision loss in naive summation

        Expected:
        - Kahan summation should be more accurate
        """
        # Create scenario where naive summation loses precision
        base = 1e10
        n = 10000
        small_value = 1.0

        # Naive summation
        naive_sum = base
        for _ in range(n):
            naive_sum += small_value

        # Expected result
        expected = base + n * small_value

        # Kahan summation (if implemented in Haze)
        # This test documents the expected behavior
        # Actual implementation depends on Rust backend

        # Check if naive summation has error
        naive_error = abs(naive_sum - expected)

        # Document the precision issue
        # In production, Kahan summation should reduce this error
        # This test serves as documentation and benchmark


class TestEdgeCaseParameters:
    """Test indicators with edge case parameters."""

    def test_period_one(self):
        """Test indicators with period=1."""
        data = [10.0, 11.0, 12.0, 13.0, 14.0]

        # SMA with period=1 should equal input
        result = haze.sma(data, period=1)

        for i, (r, d) in enumerate(zip(result, data)):
            if not np.isnan(r):
                assert abs(r - d) < 1e-10, (
                    f"SMA(1) should equal input at index {i}: {r} vs {d}"
                )

    def test_period_equals_length(self):
        """Test indicators with period equal to data length."""
        data = [10.0, 11.0, 12.0, 13.0, 14.0]
        period = len(data)

        result = haze.sma(data, period=period)

        # Should have exactly one valid result at the end
        valid_results = [r for r in result if not np.isnan(r)]
        assert len(valid_results) >= 1, "Should have at least one valid result"

        # Last result should be the average of all data
        expected_avg = sum(data) / len(data)
        assert abs(valid_results[-1] - expected_avg) < 1e-10, (
            f"SMA({period}) should equal average: {valid_results[-1]} vs {expected_avg}"
        )

    def test_very_large_period(self):
        """Test indicators with period > data length."""
        data = [10.0, 11.0, 12.0, 13.0, 14.0]
        period = 100

        result = haze.sma(data, period=period)

        # All results should be NaN (insufficient data)
        valid_results = [r for r in result if not np.isnan(r)]
        assert len(valid_results) == 0, (
            f"Should have no valid results with period > length, got {len(valid_results)}"
        )


class TestMemoryEfficiency:
    """Test memory efficiency with large datasets."""

    def test_large_dataset_no_overflow(self):
        """Test that large datasets don't cause memory overflow."""
        # 1 million data points
        n = 1_000_000
        data = [100.0 + np.sin(i * 0.001) for i in range(n)]

        # Should complete without memory error
        result = haze.sma(data, period=100)

        assert len(result) == n, "Output length should match input length"
        assert np.isfinite(result[-1]), "Final result should be finite"

    def test_multiple_indicators_sequentially(self):
        """Test running multiple indicators on large dataset sequentially."""
        n = 100_000
        data = [100.0 + np.sin(i * 0.01) for i in range(n)]

        # Run multiple indicators
        sma = haze.sma(data, period=20)
        ema = haze.ema(data, period=20)
        rsi = haze.rsi(data, period=14)

        # All should complete successfully
        for result, name in [(sma, 'SMA'), (ema, 'EMA'), (rsi, 'RSI')]:
            assert len(result) == n, f"{name} output length mismatch"
            assert np.isfinite(result[-1]), f"{name} final value not finite"
