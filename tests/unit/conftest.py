"""
Pytest Fixtures for haze-Library Unit Tests
============================================

提供所有单元测试使用的共享测试数据。

设计原则：
- 简单数据：5-20 个数据点，便于手动计算验证
- 真实场景：价格波动符合市场规律（上涨+下跌）
- 边界测试：包含特殊情况（空数组、NaN 值）

Author: Haze Team
Date: 2025-12-25
"""

import pytest
import numpy as np
from typing import Dict, List


# ==================== 基础价格数据 ====================

@pytest.fixture
def simple_prices() -> List[float]:
    """
    简单价格序列（10 个数据点，手动验证）

    特点：
    - 整数和半整数，易于手算
    - 包含上涨（10→11）和下跌（12→11.5）
    - 适用于 MA、RSI、ROC 等单序列指标

    返回：[10.0, 11.0, 12.0, 11.5, 13.0, 12.5, 14.0, 13.5, 15.0, 14.5]
    """
    return [10.0, 11.0, 12.0, 11.5, 13.0, 12.5, 14.0, 13.5, 15.0, 14.5]


@pytest.fixture
def simple_prices_short() -> List[float]:
    """
    短价格序列（5 个数据点，用于快速测试）

    手动计算示例（SMA period=3）：
    - Index 0-1: NaN (不足周期)
    - Index 2: (10+11+12)/3 = 11.0
    - Index 3: (11+12+11.5)/3 = 11.5
    - Index 4: (12+11.5+13)/3 = 12.166666667
    """
    return [10.0, 11.0, 12.0, 11.5, 13.0]


# ==================== OHLCV 数据 ====================

@pytest.fixture
def ohlcv_data() -> Dict[str, List[float]]:
    """
    完整 OHLCV 数据（5 个数据点）

    用于需要 high/low/volume 的指标：
    - ATR, NATR（波动率）
    - CCI, MFI（动量）
    - OBV, VWAP（成交量）

    数据特点：
    - High > Close > Open > Low（符合 OHLC 约束）
    - Volume 在 1000-1300 范围波动
    """
    return {
        'open': [10.0, 11.0, 12.0, 11.5, 13.0],
        'high': [10.5, 11.8, 12.5, 12.0, 13.5],
        'low': [9.8, 10.5, 11.5, 11.0, 12.5],
        'close': [10.2, 11.5, 12.0, 11.8, 13.2],
        'volume': [1000.0, 1200.0, 1100.0, 1300.0, 1250.0]
    }


@pytest.fixture
def ohlcv_data_extended() -> Dict[str, List[float]]:
    """
    扩展 OHLCV 数据（20 个数据点）

    用于需要较长历史数据的指标：
    - RSI（建议 ≥14 个数据点）
    - MACD（需要 26+ 个数据点才稳定）
    - Bollinger Bands（需要 20+ 个数据点）
    """
    np.random.seed(42)
    n = 20

    # 生成随机游走价格
    returns = np.random.normal(0.0005, 0.015, n)
    close = 100.0 * np.exp(np.cumsum(returns))

    # 生成 OHLC
    high = close * (1 + np.abs(np.random.normal(0, 0.008, n)))
    low = close * (1 - np.abs(np.random.normal(0, 0.008, n)))
    open_ = np.roll(close, 1)
    open_[0] = close[0]

    # 生成成交量
    volume = np.random.lognormal(8, 0.5, n)

    return {
        'open': open_.tolist(),
        'high': high.tolist(),
        'low': low.tolist(),
        'close': close.tolist(),
        'volume': volume.tolist()
    }


# ==================== 已知结果（手动计算）====================

@pytest.fixture
def known_sma_results() -> Dict[str, List[float]]:
    """
    SMA 已知结果（手动计算）

    基于 simple_prices_short = [10, 11, 12, 11.5, 13]

    SMA(period=3):
    - [0]: NaN
    - [1]: NaN
    - [2]: (10+11+12)/3 = 11.0
    - [3]: (11+12+11.5)/3 = 11.5
    - [4]: (12+11.5+13)/3 = 12.166666666666666
    """
    return {
        'period_3': [float('nan'), float('nan'), 11.0, 11.5, 12.166666666666666]
    }


@pytest.fixture
def known_ema_results() -> Dict[str, List[float]]:
    """
    EMA 已知结果（手动计算）

    基于 simple_prices_short = [10, 11, 12, 11.5, 13]

    EMA(period=3):
    - α = 2/(3+1) = 0.5
    - [0]: 10.0 (首值初始化)
    - [1]: 11*0.5 + 10*0.5 = 10.5
    - [2]: 12*0.5 + 10.5*0.5 = 11.25
    - [3]: 11.5*0.5 + 11.25*0.5 = 11.375
    - [4]: 13*0.5 + 11.375*0.5 = 12.1875
    """
    return {
        'period_3': [10.0, 10.5, 11.25, 11.375, 12.1875]
    }


# ==================== 边界测试数据 ====================

@pytest.fixture
def empty_array() -> List[float]:
    """空数组（测试边界条件）"""
    return []


@pytest.fixture
def single_value() -> List[float]:
    """单个值（测试不足周期情况）"""
    return [100.0]


@pytest.fixture
def array_with_nan() -> List[float]:
    """包含 NaN 的数组（测试 NaN 传播）"""
    return [10.0, 11.0, float('nan'), 12.0, 13.0]


@pytest.fixture
def all_nan_array() -> List[float]:
    """全 NaN 数组（极端边界）"""
    return [float('nan')] * 10


# ==================== 特殊场景数据 ====================

@pytest.fixture
def monotonic_increasing() -> List[float]:
    """单调递增序列（测试趋势指标）"""
    return [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]


@pytest.fixture
def monotonic_decreasing() -> List[float]:
    """单调递减序列（测试趋势指标）"""
    return [10.0, 9.0, 8.0, 7.0, 6.0, 5.0, 4.0, 3.0, 2.0, 1.0]


@pytest.fixture
def constant_values() -> List[float]:
    """常数序列（测试零波动情况）"""
    return [50.0] * 10


@pytest.fixture
def high_volatility() -> List[float]:
    """高波动序列（测试波动率指标）"""
    return [100.0, 95.0, 105.0, 92.0, 108.0, 90.0, 110.0, 88.0, 112.0, 85.0]


# ==================== 蜡烛图形态数据 ====================

@pytest.fixture
def doji_pattern() -> Dict[str, List[float]]:
    """
    Doji 形态（开盘价 ≈ 收盘价）

    特征：
    - Open ≈ Close（差异 < 0.1%）
    - 上下影线存在
    - 表示市场犹豫不决
    """
    return {
        'open': [10.0, 11.0, 12.0],
        'high': [10.5, 11.5, 12.5],
        'low': [9.5, 10.5, 11.5],
        'close': [10.0, 11.0, 12.0]  # Close = Open
    }


@pytest.fixture
def hammer_pattern() -> Dict[str, List[float]]:
    """
    Hammer 形态（锤子线，看涨反转）

    特征：
    - 小实体在上部
    - 长下影线（≥ 2倍实体）
    - 无上影线或很短
    """
    return {
        'open': [10.0, 10.0, 10.5],
        'high': [10.2, 10.3, 10.8],
        'low': [8.0, 8.5, 8.0],  # 长下影线
        'close': [10.1, 10.2, 10.7]
    }


# ==================== 数学运算测试数据 ====================

@pytest.fixture
def math_test_values() -> List[float]:
    """
    数学运算测试数据（完全平方数和特殊值）

    用于测试：SQRT, LN, LOG10, EXP, SIN, COS 等

    已知结果：
    - SQRT: [1, 2, 3, 4, 5]
    - LN: [0, 0.693, 1.099, 1.386, 1.609]
    """
    return [1.0, 4.0, 9.0, 16.0, 25.0]


# ==================== 辅助函数 ====================

def assert_arrays_almost_equal(
    result: List[float],
    expected: List[float],
    tolerance: float = 1e-10,
    allow_nan: bool = True
) -> None:
    """
    断言两个数组近似相等（处理 NaN）

    Args:
        result: 计算结果
        expected: 预期结果
        tolerance: 允许误差（默认 1e-10）
        allow_nan: 是否允许 NaN（默认 True）

    Raises:
        AssertionError: 如果数组不匹配
    """
    assert len(result) == len(expected), \
        f"数组长度不一致: {len(result)} vs {len(expected)}"

    for i, (r, e) in enumerate(zip(result, expected)):
        if np.isnan(e):
            if allow_nan:
                assert np.isnan(r), f"Index {i}: 期望 NaN，实际为 {r}"
            else:
                raise AssertionError(f"Index {i}: 不允许 NaN 值")
        else:
            assert not np.isnan(r), f"Index {i}: 期望 {e}，实际为 NaN"
            assert abs(r - e) < tolerance, \
                f"Index {i}: 期望 {e}，实际为 {r}，误差 {abs(r - e)} > {tolerance}"
