#!/usr/bin/env python3
"""
ccxt Real-Time Trading Indicators Demo
=======================================

This example demonstrates how to use Haze-Library's streaming
indicators with ccxt.pro WebSocket feeds for real-time trading.

Requirements:
    pip install ccxt>=4.0.0

Usage:
    python ccxt_realtime_demo.py

Author: Haze Team
Date: 2025-12-26
"""

import asyncio
import sys
import os
from datetime import datetime

# Add parent to path for development
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../rust/python'))

try:
    import ccxt.pro as ccxt
    CCXT_AVAILABLE = True
except ImportError:
    CCXT_AVAILABLE = False
    print("WARNING: ccxt.pro not available. Install with: pip install ccxt")

from haze_library.streaming import (
    IncrementalSMA,
    IncrementalEMA,
    IncrementalRSI,
    IncrementalMACD,
    IncrementalSuperTrend,
    IncrementalBollingerBands,
    CCXTStreamProcessor,
    realtime_rsi,
    realtime_supertrend,
    realtime_multi_indicator,
)


# ==================== Configuration ====================

SYMBOL = 'BTC/USDT'
TIMEFRAME = '1m'
EXCHANGE_ID = 'binance'


# ==================== Example 1: Simple RSI Streaming ====================

async def simple_rsi_example():
    """
    Simple example: Stream RSI for a single symbol.

    This is the most basic usage pattern with error handling.
    """
    print("\n" + "=" * 60)
    print("Example 1: Simple RSI Streaming")
    print("=" * 60)

    if not CCXT_AVAILABLE:
        print("Skipping - ccxt not available")
        return

    exchange = getattr(ccxt, EXCHANGE_ID)()
    rsi_calc = IncrementalRSI(period=14)

    try:
        count = 0
        while count < 10:  # Limit to 10 updates for demo
            try:
                candles = await exchange.watch_ohlcv(SYMBOL, TIMEFRAME)
                if candles:
                    close = candles[-1][4]  # Close price
                    timestamp = datetime.fromtimestamp(candles[-1][0] / 1000)

                    # Update RSI with error handling for invalid data
                    try:
                        rsi = rsi_calc.update(close)

                        if rsi_calc.is_ready:
                            status = "OVERSOLD" if rsi < 30 else "OVERBOUGHT" if rsi > 70 else "NEUTRAL"
                            print(f"[{timestamp}] {SYMBOL} Close: ${close:.2f}, RSI(14): {rsi:.2f} - {status}")
                        else:
                            print(f"[{timestamp}] {SYMBOL} Close: ${close:.2f}, RSI: warming up ({rsi_calc.count}/14)")
                    except ValueError as e:
                        print(f"[{timestamp}] Error calculating RSI: {e}")
                        continue

                    count += 1
            except Exception as e:
                print(f"Error fetching candles: {e}")
                break
    finally:
        await exchange.close()


# ==================== Example 2: Multi-Indicator Streaming ====================

async def multi_indicator_example():
    """
    Advanced example: Stream multiple indicators simultaneously.

    Uses CCXTStreamProcessor to manage multiple indicators.
    """
    print("\n" + "=" * 60)
    print("Example 2: Multi-Indicator Streaming")
    print("=" * 60)

    if not CCXT_AVAILABLE:
        print("Skipping - ccxt not available")
        return

    exchange = getattr(ccxt, EXCHANGE_ID)()

    # Create processor and add indicators
    processor = CCXTStreamProcessor()
    processor.add_indicator('rsi_14', IncrementalRSI(14))
    processor.add_indicator('sma_20', IncrementalSMA(20))
    processor.add_indicator('ema_12', IncrementalEMA(12))
    processor.add_indicator('macd', IncrementalMACD(12, 26, 9))
    processor.add_indicator('bb', IncrementalBollingerBands(20, 2.0))

    try:
        count = 0
        while count < 10:
            candles = await exchange.watch_ohlcv(SYMBOL, TIMEFRAME)
            if candles:
                timestamp = datetime.fromtimestamp(candles[-1][0] / 1000)
                results = processor.process_candle(candles[-1])

                print(f"\n[{timestamp}] {SYMBOL}")
                print(f"  Close: ${candles[-1][4]:.2f}")

                # Display results
                if not isinstance(results.get('rsi_14'), float) or not __import__('math').isnan(results['rsi_14']):
                    print(f"  RSI(14): {results['rsi_14']:.2f}")
                if not isinstance(results.get('sma_20'), float) or not __import__('math').isnan(results['sma_20']):
                    print(f"  SMA(20): ${results['sma_20']:.2f}")
                if not isinstance(results.get('ema_12'), float) or not __import__('math').isnan(results['ema_12']):
                    print(f"  EMA(12): ${results['ema_12']:.2f}")

                if 'macd' in results and isinstance(results['macd'], dict):
                    macd = results['macd']
                    if not __import__('math').isnan(macd.get('macd', float('nan'))):
                        print(f"  MACD: {macd['macd']:.4f}, Signal: {macd['signal']:.4f}, Hist: {macd['histogram']:.4f}")

                if 'bb' in results and isinstance(results['bb'], dict):
                    bb = results['bb']
                    if not __import__('math').isnan(bb.get('middle', float('nan'))):
                        print(f"  Bollinger: Upper=${bb['upper']:.2f}, Middle=${bb['middle']:.2f}, Lower=${bb['lower']:.2f}")

                count += 1
    finally:
        await exchange.close()


# ==================== Example 3: SuperTrend Trading Signals ====================

async def supertrend_signals_example():
    """
    Trading example: Generate buy/sell signals using SuperTrend.

    Demonstrates a simple trend-following strategy.
    """
    print("\n" + "=" * 60)
    print("Example 3: SuperTrend Trading Signals")
    print("=" * 60)

    if not CCXT_AVAILABLE:
        print("Skipping - ccxt not available")
        return

    exchange = getattr(ccxt, EXCHANGE_ID)()
    st = IncrementalSuperTrend(period=10, multiplier=3.0)
    prev_direction = None

    try:
        count = 0
        while count < 15:
            candles = await exchange.watch_ohlcv(SYMBOL, TIMEFRAME)
            if candles:
                ohlcv = candles[-1]
                timestamp = datetime.fromtimestamp(ohlcv[0] / 1000)
                high, low, close = ohlcv[2], ohlcv[3], ohlcv[4]

                value, direction = st.update(high, low, close)

                if st.is_ready:
                    trend = "🟢 UPTREND" if direction > 0 else "🔴 DOWNTREND"

                    # Detect trend changes (trading signals)
                    signal = ""
                    if prev_direction is not None and direction != prev_direction:
                        if direction > 0:
                            signal = " ⬆️ BUY SIGNAL!"
                        else:
                            signal = " ⬇️ SELL SIGNAL!"

                    print(f"[{timestamp}] {SYMBOL} Close: ${close:.2f} | SuperTrend: ${value:.2f} | {trend}{signal}")
                    prev_direction = direction
                else:
                    print(f"[{timestamp}] SuperTrend warming up ({st.count}/10)")

                count += 1
    finally:
        await exchange.close()


# ==================== Example 4: Multiple Symbols ====================

async def multi_symbol_example():
    """
    Multi-symbol example: Track indicators for multiple trading pairs.

    Demonstrates concurrent streaming for multiple symbols.
    """
    print("\n" + "=" * 60)
    print("Example 4: Multiple Symbols Streaming")
    print("=" * 60)

    if not CCXT_AVAILABLE:
        print("Skipping - ccxt not available")
        return

    symbols = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT']
    exchange = getattr(ccxt, EXCHANGE_ID)()

    # Create a processor for each symbol
    processors = {
        symbol: CCXTStreamProcessor()
        for symbol in symbols
    }

    for symbol, processor in processors.items():
        processor.add_indicator('rsi', IncrementalRSI(14))
        processor.add_indicator('sma', IncrementalSMA(20))

    try:
        count = 0
        while count < 15:
            # Watch all symbols concurrently
            for symbol in symbols:
                candles = await exchange.watch_ohlcv(symbol, TIMEFRAME)
                if candles:
                    results = processors[symbol].process_candle(candles[-1])
                    close = candles[-1][4]

                    rsi = results.get('rsi', float('nan'))
                    sma = results.get('sma', float('nan'))

                    if not __import__('math').isnan(rsi):
                        print(f"{symbol}: Close=${close:.2f}, RSI={rsi:.2f}, SMA=${sma:.2f}")

            count += 1
    finally:
        await exchange.close()


# ==================== Example 5: Using Helper Functions ====================

async def helper_functions_example():
    """
    Helper functions example: Using convenience async generators.

    Shows the simplest way to get streaming indicators.
    """
    print("\n" + "=" * 60)
    print("Example 5: Using Helper Functions")
    print("=" * 60)

    if not CCXT_AVAILABLE:
        print("Skipping - ccxt not available")
        return

    exchange = getattr(ccxt, EXCHANGE_ID)()

    try:
        count = 0
        async for results in realtime_multi_indicator(exchange, SYMBOL, TIMEFRAME):
            print(f"\n{SYMBOL} Indicators:")
            for name, value in results.items():
                if isinstance(value, dict):
                    print(f"  {name}: {value}")
                elif not __import__('math').isnan(value):
                    print(f"  {name}: {value:.4f}")

            count += 1
            if count >= 5:
                break
    finally:
        await exchange.close()


# ==================== Offline Demo (No ccxt) ====================

def offline_demo():
    """
    Offline demo: Test streaming indicators without ccxt.

    Useful for understanding the API without exchange connection.
    Demonstrates error handling for invalid inputs.
    """
    print("\n" + "=" * 60)
    print("Offline Demo: Simulated Data")
    print("=" * 60)

    # Simulated price data
    prices = [
        100.0, 101.5, 102.0, 101.0, 103.5, 104.0, 103.0, 105.5,
        106.0, 105.0, 107.5, 108.0, 107.0, 109.5, 110.0, 109.0,
        108.0, 107.0, 106.0, 108.0, 109.0, 110.0, 111.0, 110.0,
    ]

    # Create indicators with error handling
    try:
        sma = IncrementalSMA(period=5)
        ema = IncrementalEMA(period=5)
        rsi = IncrementalRSI(period=7)
    except ValueError as e:
        print(f"Error creating indicators: {e}")
        return

    print("\nProcessing simulated price data...")
    print("-" * 60)
    print(f"{'Price':>10} | {'SMA(5)':>10} | {'EMA(5)':>10} | {'RSI(7)':>10}")
    print("-" * 60)

    for i, price in enumerate(prices):
        try:
            sma_val = sma.update(price)
            ema_val = ema.update(price)
            rsi_val = rsi.update(price)

            sma_str = f"{sma_val:.2f}" if not __import__('math').isnan(sma_val) else "---"
            ema_str = f"{ema_val:.2f}" if not __import__('math').isnan(ema_val) else "---"
            rsi_str = f"{rsi_val:.2f}" if not __import__('math').isnan(rsi_val) else "---"

            print(f"{price:>10.2f} | {sma_str:>10} | {ema_str:>10} | {rsi_str:>10}")
        except ValueError as e:
            print(f"Error at index {i} (price={price}): {e}")
            continue

    print("-" * 60)
    print(f"Final values: SMA={sma.current:.2f}, EMA={ema.current:.2f}, RSI={rsi.current:.2f}")

    # Demo: Error handling for batch calculations
    print("\n" + "=" * 60)
    print("Error Handling Demo: Invalid Inputs")
    print("=" * 60)

    # Example 1: Invalid period
    print("\nExample 1: Period too large for data")
    try:
        import haze_library as haze
        short_data = [100.0, 101.0, 102.0]
        result = haze.py_rsi(short_data, period=14)
        print(f"  RSI: {result}")
    except ValueError as e:
        print(f"  Caught error: {e}")

    # Example 2: Mismatched array lengths
    print("\nExample 2: Mismatched array lengths")
    try:
        import haze_library as haze
        high = [101.0, 102.0, 103.0, 104.0]
        low = [99.0, 100.0, 101.0]  # Different length
        close = [100.0, 101.0, 102.0, 103.0]
        result = haze.py_atr(high, low, close, period=2)
        print(f"  ATR: {result}")
    except ValueError as e:
        print(f"  Caught error: {e}")

    # Example 3: Empty input
    print("\nExample 3: Empty input data")
    try:
        import haze_library as haze
        result = haze.py_rsi([], period=14)
        print(f"  RSI: {result}")
    except ValueError as e:
        print(f"  Caught error: {e}")

    print("\n" + "=" * 60)


# ==================== Main ====================

async def main():
    """Run all examples."""
    print("=" * 60)
    print("Haze-Library ccxt Real-Time Demo")
    print("=" * 60)

    # Always run offline demo first
    offline_demo()

    if CCXT_AVAILABLE:
        print("\n\nRunning live examples with ccxt...")
        print("Press Ctrl+C to stop\n")

        try:
            # Run examples (uncomment the ones you want to try)
            await simple_rsi_example()
            # await multi_indicator_example()
            # await supertrend_signals_example()
            # await multi_symbol_example()
            # await helper_functions_example()
        except KeyboardInterrupt:
            print("\n\nStopped by user")
        except Exception as e:
            print(f"\nError: {e}")
    else:
        print("\n\nTo run live examples, install ccxt:")
        print("  pip install ccxt>=4.0.0")


if __name__ == '__main__':
    asyncio.run(main())
