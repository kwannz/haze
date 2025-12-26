#!/usr/bin/env python3
"""
Type Hints Demo for Haze-Library
=================================

Demonstrates IDE type hint support with .pyi stub files.

Run this file in VS Code or PyCharm to see:
- Auto-completion
- Parameter hints
- Type checking
- Documentation tooltips
"""

from typing import List, Tuple
import haze_library as haze

def demo_simple_indicators():
    """Demo simple indicators with single outputs."""
    close_prices: List[float] = [
        100.0, 101.0, 102.0, 103.0, 104.0,
        105.0, 104.0, 103.0, 102.0, 101.0
    ]

    # Simple Moving Average
    # IDE should show: py_sma(values: List[float], period: int) -> List[float]
    sma_5: List[float] = haze.py_sma(close_prices, 5)
    print(f"SMA(5): {sma_5}")

    # Relative Strength Index
    # IDE should show: py_rsi(close: List[float], period: Optional[int] = None) -> List[float]
    rsi_14: List[float] = haze.py_rsi(close_prices, 14)
    rsi_default: List[float] = haze.py_rsi(close_prices)  # Uses default period=14
    print(f"RSI(14): {rsi_14}")

    # Exponential Moving Average
    ema_10: List[float] = haze.py_ema(close_prices, 10)
    print(f"EMA(10): {ema_10}")


def demo_multi_output_indicators():
    """Demo indicators with multiple outputs."""
    close_prices: List[float] = [
        100.0, 101.0, 102.0, 103.0, 104.0,
        105.0, 104.0, 103.0, 102.0, 101.0
    ] * 10  # Longer series for MACD

    # MACD - Returns tuple
    # IDE should show return type: Tuple[List[float], List[float], List[float]]
    macd_line: List[float]
    signal_line: List[float]
    histogram: List[float]

    macd_line, signal_line, histogram = haze.py_macd(
        close_prices,
        fast_period=12,
        slow_period=26,
        signal_period=9
    )

    print(f"MACD Line: {macd_line[-5:]}")
    print(f"Signal Line: {signal_line[-5:]}")
    print(f"Histogram: {histogram[-5:]}")

    # Bollinger Bands - Returns tuple
    upper: List[float]
    middle: List[float]
    lower: List[float]

    upper, middle, lower = haze.py_bollinger_bands(
        close_prices,
        period=20,
        std_multiplier=2.0
    )

    print(f"BB Upper: {upper[-5:]}")
    print(f"BB Middle: {middle[-5:]}")
    print(f"BB Lower: {lower[-5:]}")


def demo_multi_input_indicators():
    """Demo indicators requiring OHLCV data."""
    # Sample OHLCV data
    high: List[float] = [101.0, 102.0, 103.0, 104.0, 105.0] * 10
    low: List[float] = [99.0, 100.0, 101.0, 102.0, 103.0] * 10
    close: List[float] = [100.0, 101.0, 102.0, 103.0, 104.0] * 10
    volume: List[float] = [1000.0, 1100.0, 1200.0, 1300.0, 1400.0] * 10

    # Average True Range
    # IDE should show: py_atr(high: List[float], low: List[float], close: List[float], period: Optional[int] = None) -> List[float]
    atr_14: List[float] = haze.py_atr(high, low, close, 14)
    print(f"ATR(14): {atr_14[-5:]}")

    # Stochastic Oscillator
    k_values: List[float]
    d_values: List[float]

    k_values, d_values = haze.py_stochastic(
        high, low, close,
        k_period=14,
        d_period=3
    )

    print(f"%K: {k_values[-5:]}")
    print(f"%D: {d_values[-5:]}")

    # Money Flow Index
    mfi: List[float] = haze.py_mfi(high, low, close, volume, 14)
    print(f"MFI(14): {mfi[-5:]}")

    # VWAP
    vwap: List[float] = haze.py_vwap(high, low, close, volume)
    print(f"VWAP: {vwap[-5:]}")


def demo_optional_parameters():
    """Demo indicators with optional parameters."""
    close_prices: List[float] = [100.0, 101.0, 102.0, 103.0, 104.0] * 10

    # Using default parameters
    sma_default = haze.py_sma(close_prices, 20)

    # T3 with optional volume factor
    t3_default = haze.py_t3(close_prices, 5)  # vfactor defaults to 0.7
    t3_custom = haze.py_t3(close_prices, 5, vfactor=0.5)

    # KAMA with optional parameters
    kama_default = haze.py_kama(close_prices)  # Uses defaults
    kama_custom = haze.py_kama(
        close_prices,
        period=10,
        fast_period=2,
        slow_period=30
    )

    print(f"T3 (default vfactor): {t3_default[-5:]}")
    print(f"T3 (vfactor=0.5): {t3_custom[-5:]}")


def demo_type_checking():
    """Demo type checking - these will be caught by mypy/pylance."""
    close_prices: List[float] = [100.0, 101.0, 102.0, 103.0, 104.0]

    # ✅ Correct usage
    result: List[float] = haze.py_sma(close_prices, 5)

    # ❌ Type error - mypy will catch this
    # wrong_type: str = haze.py_sma(close_prices, 5)  # Error: incompatible type

    # ❌ Type error - wrong parameter type
    # wrong_param = haze.py_sma(close_prices, "5")  # Error: expected int, got str

    # ❌ Type error - wrong return type unpacking
    # single_value: float = haze.py_macd(close_prices)  # Error: expected float, got Tuple

    # ✅ Correct unpacking
    macd, signal, hist = haze.py_macd(close_prices)


def demo_pandas_accessor():
    """Demo Pandas DataFrame accessor with type hints."""
    try:
        import pandas as pd

        # Create sample DataFrame
        df = pd.DataFrame({
            'open': [100.0, 101.0, 102.0, 103.0, 104.0] * 10,
            'high': [101.0, 102.0, 103.0, 104.0, 105.0] * 10,
            'low': [99.0, 100.0, 101.0, 102.0, 103.0] * 10,
            'close': [100.0, 101.0, 102.0, 103.0, 104.0] * 10,
            'volume': [1000.0, 1100.0, 1200.0, 1300.0, 1400.0] * 10
        })

        # DataFrame accessor - IDE should provide type hints
        df['sma_20'] = df.ta.sma(20)
        df['rsi_14'] = df.ta.rsi(14)
        df['ema_10'] = df.ta.ema(10)

        # Multi-output indicators
        upper, middle, lower = df.ta.bollinger_bands(20, 2.0)
        df['bb_upper'] = upper
        df['bb_middle'] = middle
        df['bb_lower'] = lower

        print("\nDataFrame with indicators:")
        print(df[['close', 'sma_20', 'rsi_14', 'bb_upper', 'bb_lower']].tail())

    except ImportError:
        print("Pandas not installed - skipping DataFrame demo")


def demo_numpy_compatibility():
    """Demo NumPy compatibility layer."""
    try:
        import numpy as np
        from haze_library import np_ta

        # NumPy arrays
        close = np.array([100.0, 101.0, 102.0, 103.0, 104.0] * 10)

        # NumPy interface - returns numpy.ndarray
        sma = np_ta.sma(close, 20)
        rsi = np_ta.rsi(close, 14)
        ema = np_ta.ema(close, 10)

        print("\nNumPy results:")
        print(f"SMA(20): {sma[-5:]}")
        print(f"RSI(14): {rsi[-5:]}")
        print(f"EMA(10): {ema[-5:]}")

        # Type should be numpy.ndarray
        print(f"Type: {type(sma)}")

    except ImportError:
        print("NumPy not installed - skipping NumPy demo")


if __name__ == '__main__':
    print("=" * 60)
    print("Haze-Library Type Hints Demo")
    print("=" * 60)

    print("\n1. Simple Indicators (Single Output)")
    print("-" * 60)
    demo_simple_indicators()

    print("\n2. Multi-Output Indicators")
    print("-" * 60)
    demo_multi_output_indicators()

    print("\n3. Multi-Input Indicators (OHLCV)")
    print("-" * 60)
    demo_multi_input_indicators()

    print("\n4. Optional Parameters")
    print("-" * 60)
    demo_optional_parameters()

    print("\n5. Pandas DataFrame Accessor")
    print("-" * 60)
    demo_pandas_accessor()

    print("\n6. NumPy Compatibility")
    print("-" * 60)
    demo_numpy_compatibility()

    print("\n" + "=" * 60)
    print("Demo completed! Check your IDE for type hints.")
    print("=" * 60)
    print("\nIDE Features to test:")
    print("  1. Auto-completion (Ctrl+Space)")
    print("  2. Parameter hints (Ctrl+Shift+Space)")
    print("  3. Type checking (mypy/pylance)")
    print("  4. Go to definition (F12)")
    print("  5. Hover documentation")
