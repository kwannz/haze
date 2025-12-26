#!/usr/bin/env python3
"""
生成增强版 haze_library 类型存根文件 (.pyi)
包含完整的文档字符串和类型注解
"""

# 手工维护的函数文档字符串映射
FUNCTION_DOCS = {
    # Volatility Indicators
    'py_atr': '''Calculate Average True Range.

    Args:
        high: High prices
        low: Low prices
        close: Close prices
        period: Lookback period (default: 14)

    Returns:
        ATR values

    Raises:
        ValueError: If data length < period''',

    'py_natr': '''Calculate Normalized Average True Range (percentage form).

    Args:
        high: High prices
        low: Low prices
        close: Close prices
        period: Lookback period (default: 14)

    Returns:
        NATR values (0-100 range)''',

    'py_true_range': '''Calculate True Range.

    Args:
        high: High prices
        low: Low prices
        close: Close prices
        drift: Drift period (default: 1)

    Returns:
        True Range values''',

    'py_bollinger_bands': '''Calculate Bollinger Bands.

    Args:
        close: Close prices
        period: MA period (default: 20)
        std_multiplier: Standard deviation multiplier (default: 2.0)

    Returns:
        Tuple of (upper_band, middle_band, lower_band)''',

    'py_keltner_channel': '''Calculate Keltner Channel.

    Args:
        high: High prices
        low: Low prices
        close: Close prices
        period: MA period (default: 20)
        atr_period: ATR period (default: 10)
        multiplier: ATR multiplier (default: 2.0)

    Returns:
        Tuple of (upper, middle, lower)''',

    'py_donchian_channel': '''Calculate Donchian Channel.

    Args:
        high: High prices
        low: Low prices
        period: Lookback period (default: 20)

    Returns:
        Tuple of (upper, middle, lower)''',

    # Momentum Indicators
    'py_rsi': '''Calculate Relative Strength Index.

    Args:
        close: Close prices
        period: Lookback period (default: 14)

    Returns:
        RSI values (0-100 range)

    Raises:
        ValueError: If period <= 0 or period >= len(data)''',

    'py_macd': '''Calculate MACD (Moving Average Convergence Divergence).

    Args:
        close: Close prices
        fast_period: Fast EMA period (default: 12)
        slow_period: Slow EMA period (default: 26)
        signal_period: Signal line period (default: 9)

    Returns:
        Tuple of (macd_line, signal_line, histogram)''',

    'py_stochastic': '''Calculate Stochastic Oscillator.

    Args:
        high: High prices
        low: Low prices
        close: Close prices
        k_period: %K period (default: 14)
        d_period: %D smoothing period (default: 3)

    Returns:
        Tuple of (%K, %D)''',

    'py_stochrsi': '''Calculate Stochastic RSI.

    Args:
        close: Close prices
        rsi_period: RSI period (default: 14)
        stoch_period: Stochastic period (default: 14)
        k_period: %K period (default: 3)
        d_period: %D period (default: 3)

    Returns:
        Tuple of (%K, %D)''',

    'py_cci': '''Calculate Commodity Channel Index.

    Args:
        high: High prices
        low: Low prices
        close: Close prices
        period: Lookback period (default: 20)

    Returns:
        CCI values''',

    'py_williams_r': '''Calculate Williams %R.

    Args:
        high: High prices
        low: Low prices
        close: Close prices
        period: Lookback period (default: 14)

    Returns:
        Williams %R values (-100 to 0 range)''',

    'py_awesome_oscillator': '''Calculate Awesome Oscillator.

    Args:
        high: High prices
        low: Low prices
        fast_period: Fast MA period (default: 5)
        slow_period: Slow MA period (default: 34)

    Returns:
        Awesome Oscillator values''',

    'py_fisher_transform': '''Calculate Fisher Transform.

    Args:
        high: High prices
        low: Low prices
        close: Close prices
        period: Lookback period (default: 10)

    Returns:
        Tuple of (fisher, signal)''',

    'py_kdj': '''Calculate KDJ Indicator (Stochastic extension).

    Args:
        high: High prices
        low: Low prices
        close: Close prices
        k_period: K period (default: 9)
        d_period: D period (default: 3)

    Returns:
        Tuple of (K, D, J) where J = 3K - 2D''',

    'py_tsi': '''Calculate True Strength Index.

    Args:
        close: Close prices
        long_period: Long momentum period (default: 25)
        short_period: Short momentum period (default: 13)
        signal_period: Signal line period (default: 13)

    Returns:
        Tuple of (tsi, signal)''',

    'py_ultimate_oscillator': '''Calculate Ultimate Oscillator.

    Args:
        high: High prices
        low: Low prices
        close: Close prices
        period1: First period (default: 7)
        period2: Second period (default: 14)
        period3: Third period (default: 28)

    Returns:
        Ultimate Oscillator values (0-100 range)''',

    'py_mom': '''Calculate Momentum.

    Args:
        values: Price values
        period: Lookback period (default: 10)

    Returns:
        Momentum values''',

    'py_roc': '''Calculate Rate of Change.

    Args:
        values: Price values
        period: Lookback period (default: 10)

    Returns:
        ROC values (percentage change)''',

    # Trend Indicators
    'py_supertrend': '''Calculate SuperTrend indicator.

    Args:
        high: High prices
        low: Low prices
        close: Close prices
        period: ATR period (default: 10)
        multiplier: ATR multiplier (default: 3.0)

    Returns:
        Tuple of (supertrend, direction, lower_band, upper_band)''',

    'py_adx': '''Calculate Average Directional Index.

    Args:
        high: High prices
        low: Low prices
        close: Close prices
        period: Lookback period (default: 14)

    Returns:
        Tuple of (adx, plus_di, minus_di)''',

    'py_aroon': '''Calculate Aroon Indicator.

    Args:
        high: High prices
        low: Low prices
        period: Lookback period (default: 25)

    Returns:
        Tuple of (aroon_up, aroon_down, oscillator)''',

    'py_psar': '''Calculate Parabolic SAR.

    Args:
        high: High prices
        low: Low prices
        close: Close prices
        af_init: Initial acceleration factor (default: 0.02)
        af_increment: AF increment (default: 0.02)
        af_max: Maximum AF (default: 0.2)

    Returns:
        Tuple of (psar, trend)''',

    # Volume Indicators
    'py_obv': '''Calculate On-Balance Volume.

    Args:
        close: Close prices
        volume: Volume data

    Returns:
        OBV values''',

    'py_vwap': '''Calculate Volume Weighted Average Price.

    Args:
        high: High prices
        low: Low prices
        close: Close prices
        volume: Volume data
        period: Lookback period (optional)

    Returns:
        VWAP values''',

    'py_mfi': '''Calculate Money Flow Index.

    Args:
        high: High prices
        low: Low prices
        close: Close prices
        volume: Volume data
        period: Lookback period (default: 14)

    Returns:
        MFI values (0-100 range)''',

    'py_cmf': '''Calculate Chaikin Money Flow.

    Args:
        high: High prices
        low: Low prices
        close: Close prices
        volume: Volume data
        period: Lookback period (default: 20)

    Returns:
        CMF values''',

    'py_ad': '''Calculate Accumulation/Distribution Line.

    Args:
        high: High prices
        low: Low prices
        close: Close prices
        volume: Volume data

    Returns:
        A/D line values''',

    # Moving Averages
    'py_sma': '''Calculate Simple Moving Average.

    Args:
        values: Price values
        period: MA period

    Returns:
        SMA values''',

    'py_ema': '''Calculate Exponential Moving Average.

    Args:
        values: Price values
        period: MA period

    Returns:
        EMA values''',

    'py_wma': '''Calculate Weighted Moving Average.

    Args:
        values: Price values
        period: MA period

    Returns:
        WMA values''',

    'py_dema': '''Calculate Double Exponential Moving Average.

    Args:
        values: Price values
        period: MA period

    Returns:
        DEMA values''',

    'py_tema': '''Calculate Triple Exponential Moving Average.

    Args:
        values: Price values
        period: MA period

    Returns:
        TEMA values''',

    'py_hma': '''Calculate Hull Moving Average.

    Args:
        values: Price values
        period: MA period

    Returns:
        HMA values''',

    'py_rma': '''Calculate Wilder's Moving Average (RMA).

    Args:
        values: Price values
        period: MA period

    Returns:
        RMA values''',

    'py_zlma': '''Calculate Zero Lag Moving Average.

    Args:
        values: Price values
        period: MA period

    Returns:
        ZLMA values''',

    'py_t3': '''Calculate Tillson T3 Moving Average.

    Args:
        values: Price values
        period: MA period
        vfactor: Volume factor (default: 0.7)

    Returns:
        T3 values''',

    'py_kama': '''Calculate Kaufman Adaptive Moving Average.

    Args:
        values: Price values
        period: MA period (default: 10)
        fast_period: Fast period (default: 2)
        slow_period: Slow period (default: 30)

    Returns:
        KAMA values''',

    'py_frama': '''Calculate Fractal Adaptive Moving Average.

    Args:
        values: Price values
        period: MA period (default: 16)

    Returns:
        FRAMA values''',
}

# 生成pyi内容的模板
PYI_TEMPLATE = '''"""
Haze-Library Type Stubs
================================================================================

Type annotations for haze_library Rust extension module.
Provides IDE support for 225+ technical indicators.

Auto-generated from Rust source code with enhanced docstrings.

Performance:
    - 5-10x faster than pure Python implementations
    - 4.8-6.3x faster than TA-Lib for most indicators
    - High numerical precision using f64

Usage:
    >>> from haze_library import py_sma, py_rsi, py_macd
    >>> sma_20 = py_sma(close_prices, 20)
    >>> rsi_14 = py_rsi(close_prices, 14)
    >>> macd, signal, hist = py_macd(close_prices)
"""

from typing import List, Optional, Tuple, Any

__version__: str
__author__: str

'''

def generate_enhanced_pyi():
    """生成增强版的 .pyi 文件"""
    from pathlib import Path
    import subprocess

    # 首先运行原始生成脚本
    project_root = Path(__file__).parent
    result = subprocess.run(
        ['python3', str(project_root / 'generate_pyi.py')],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print("Error running generate_pyi.py:")
        print(result.stderr)
        return

    # 读取生成的文件
    pyi_file = project_root / 'src' / 'haze_library' / 'haze_library.pyi'
    content = pyi_file.read_text()

    # 添加增强的文档字符串
    lines = content.split('\n')
    enhanced_lines = []

    i = 0
    while i < len(lines):
        line = lines[i]

        # 检查是否是函数定义
        if line.startswith('def py_'):
            func_name = line.split('(')[0].replace('def ', '')

            # 如果有文档字符串,添加它
            if func_name in FUNCTION_DOCS:
                # 添加缩进的文档字符串
                doc = FUNCTION_DOCS[func_name]
                enhanced_lines.append(line.replace(' ...', ':'))
                enhanced_lines.append('    """' + doc.split('\n')[0])
                for doc_line in doc.split('\n')[1:]:
                    enhanced_lines.append('    ' + doc_line)
                enhanced_lines.append('    """')
                enhanced_lines.append('    ...')
                enhanced_lines.append('')
            else:
                enhanced_lines.append(line)
        else:
            enhanced_lines.append(line)

        i += 1

    # 写回文件
    final_content = '\n'.join(enhanced_lines)
    pyi_file.write_text(final_content)

    print(f"Enhanced .pyi file generated: {pyi_file}")
    print(f"Added docstrings for {len(FUNCTION_DOCS)} functions")

if __name__ == '__main__':
    generate_enhanced_pyi()
