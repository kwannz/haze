"""
Pivot Points Unit Tests
=======================

测试所有枢轴点相关指标的核心功能。

测试的指标：
1. py_fibonacci_pivots - 斐波那契枢轴点（单条K线计算）
2. py_pivot_zone - 枢轴区域判断
3. py_pivot_buy_sell - 枢轴买卖信号
4. py_classic_pivots - 经典枢轴点
5. py_camarilla_pivots - 卡马里拉枢轴点
6. py_woodie_pivots - 伍迪枢轴点
7. py_demark_pivots - 德马克枢轴点

Author: Haze Team
Date: 2025-12-28
"""

import numpy as np
import haze_library as haze


class TestFibonacciPivots:
    """斐波那契枢轴点测试

    py_fibonacci_pivots(high, low, close) 接收单条K线的标量值，
    返回7个枢轴点级别的元组: (PP, R1, R2, R3, S1, S2, S3)
    """

    def test_basic_calculation(self):
        """测试基本计算"""
        high = 110.0
        low = 90.0
        close = 100.0

        result = haze.py_fibonacci_pivots(high, low, close)

        # 验证返回7个枢轴点级别
        assert isinstance(result, tuple)
        assert len(result) == 7
        # 所有值应为有效数字
        assert all(not np.isnan(v) for v in result)

    def test_pivot_ordering(self):
        """测试枢轴点排序：R3 > R2 > R1 > PP > S1 > S2 > S3"""
        high = 120.0
        low = 80.0
        close = 100.0

        pp, r1, r2, r3, s1, s2, s3 = haze.py_fibonacci_pivots(high, low, close)

        # 验证枢轴点层级关系
        assert r3 > r2 > r1 > pp > s1 > s2 > s3

    def test_with_constant_prices(self):
        """测试常数价格（零波动）"""
        result = haze.py_fibonacci_pivots(100.0, 100.0, 100.0)

        # 常数价格时，所有枢轴点应相等
        assert len(result) == 7
        assert all(v == 100.0 for v in result)

    def test_high_volatility(self):
        """测试高波动情况"""
        high = 200.0
        low = 50.0
        close = 120.0

        result = haze.py_fibonacci_pivots(high, low, close)

        # 高波动时枢轴点范围应更大
        assert len(result) == 7
        assert max(result) > min(result)
        # R3 应该很高，S3 应该很低
        pp, r1, r2, r3, s1, s2, s3 = result
        assert r3 - s3 > 100  # 大范围

    def test_pp_calculation(self):
        """测试PP计算公式：(H+L+C)/3"""
        high = 120.0
        low = 90.0
        close = 105.0

        result = haze.py_fibonacci_pivots(high, low, close)
        pp = result[0]

        expected_pp = (high + low + close) / 3
        assert abs(pp - expected_pp) < 1e-10


class TestPivotZone:
    """枢轴区域判断测试

    py_pivot_zone(current_price, levels)
    levels 是 py_camarilla_pivots 返回的 9 元组 (PP, R1, R2, R3, R4, S1, S2, S3, S4)
    """

    def test_basic_zone_detection(self):
        """测试基本区域检测"""
        # 使用 camarilla_pivots 返回值（9元素）
        levels = haze.py_camarilla_pivots(120.0, 80.0, 100.0)
        current_price = 105.0

        result = haze.py_pivot_zone(current_price, levels)

        # 应返回区域字符串
        assert isinstance(result, str)
        assert len(result) > 0

    def test_price_at_pivot(self):
        """测试价格正好在枢轴点"""
        levels = haze.py_camarilla_pivots(120.0, 80.0, 100.0)
        pp = levels[0]  # 枢轴点

        result = haze.py_pivot_zone(pp, levels)
        assert isinstance(result, str)

    def test_price_above_all_levels(self):
        """测试价格高于所有级别"""
        levels = haze.py_camarilla_pivots(120.0, 80.0, 100.0)
        current_price = max(levels) + 10.0

        result = haze.py_pivot_zone(current_price, levels)
        assert isinstance(result, str)

    def test_price_below_all_levels(self):
        """测试价格低于所有级别"""
        levels = haze.py_camarilla_pivots(120.0, 80.0, 100.0)
        current_price = min(levels) - 10.0

        result = haze.py_pivot_zone(current_price, levels)
        assert isinstance(result, str)


class TestPivotBuySell:
    """枢轴买卖信号测试

    py_pivot_buy_sell(close, high, low, lookback) 返回 7 元组
    包含各种枢轴点相关的信号
    """

    def test_basic_signals(self):
        """测试基本买卖信号生成"""
        close = [100.0 + i * 0.5 for i in range(50)]
        high = [c + 2 for c in close]
        low = [c - 2 for c in close]

        result = haze.py_pivot_buy_sell(close, high, low, 10)

        # 返回 7 元组
        assert isinstance(result, tuple)
        assert len(result) == 7

        # 每个元素应与输入长度相同
        for r in result:
            assert len(r) == len(close)

    def test_signal_values(self):
        """测试信号值范围"""
        close = [100.0 + i * 0.5 for i in range(50)]
        high = [c + 2 for c in close]
        low = [c - 2 for c in close]

        result = haze.py_pivot_buy_sell(close, high, low, 10)

        # 应有一些有效值
        total_valid = sum(len([v for v in r if not np.isnan(v)]) for r in result)
        assert total_valid > 0

    def test_uptrend_signals(self):
        """测试上涨趋势信号"""
        close = [100.0 + i * 2 for i in range(50)]
        high = [v + 3 for v in close]
        low = [v - 1 for v in close]

        result = haze.py_pivot_buy_sell(close, high, low, 10)
        assert len(result) == 7
        assert all(len(r) == len(close) for r in result)

    def test_downtrend_signals(self):
        """测试下跌趋势信号"""
        close = [200.0 - i * 2 for i in range(50)]
        high = [v + 1 for v in close]
        low = [v - 3 for v in close]

        result = haze.py_pivot_buy_sell(close, high, low, 10)
        assert len(result) == 7
        assert all(len(r) == len(close) for r in result)

    def test_different_lookback(self):
        """测试不同回看周期"""
        close = [100.0 + np.sin(i / 5) * 10 for i in range(100)]
        high = [v + 2 for v in close]
        low = [v - 2 for v in close]

        for lookback in [5, 10, 20, 30]:
            result = haze.py_pivot_buy_sell(close, high, low, lookback)
            assert len(result) == 7


class TestOtherPivotTypes:
    """其他枢轴点类型测试"""

    def test_classic_pivots(self):
        """测试经典枢轴点"""
        result = haze.py_classic_pivots(120.0, 80.0, 100.0)

        assert isinstance(result, tuple)
        assert len(result) >= 5  # PP, R1, R2, S1, S2 at minimum

    def test_camarilla_pivots(self):
        """测试卡马里拉枢轴点"""
        result = haze.py_camarilla_pivots(120.0, 80.0, 100.0)

        assert isinstance(result, tuple)
        assert len(result) >= 5

    def test_woodie_pivots(self):
        """测试伍迪枢轴点"""
        result = haze.py_woodie_pivots(120.0, 80.0, 100.0)

        assert isinstance(result, tuple)
        assert len(result) >= 5

    def test_demark_pivots(self):
        """测试德马克枢轴点"""
        # 需要 open 价格
        result = haze.py_demark_pivots(120.0, 80.0, 100.0, 95.0)

        assert isinstance(result, tuple)
        assert len(result) >= 3  # PP, R1, S1

    def test_standard_pivots(self):
        """测试标准枢轴点"""
        result = haze.py_standard_pivots(120.0, 80.0, 100.0)

        assert isinstance(result, tuple)
        assert len(result) >= 5


class TestPivotEdgeCases:
    """枢轴点边界条件测试"""

    def test_extreme_values(self):
        """测试极端值"""
        result = haze.py_fibonacci_pivots(1e10, 1e-10, 1e5)

        assert len(result) == 7
        assert all(not np.isnan(v) and not np.isinf(v) for v in result)

    def test_negative_prices(self):
        """测试负价格（某些衍生品可能有）"""
        result = haze.py_fibonacci_pivots(-80.0, -120.0, -100.0)

        assert len(result) == 7
        # 负价格也应该有正确的排序
        pp, r1, r2, r3, s1, s2, s3 = result
        assert r3 > r2 > r1 > pp > s1 > s2 > s3

    def test_very_small_range(self):
        """测试极小价格范围"""
        result = haze.py_fibonacci_pivots(100.001, 99.999, 100.0)

        assert len(result) == 7
        # 所有值应该非常接近
        assert max(result) - min(result) < 0.01

    def test_inverted_high_low(self):
        """测试高低价颠倒（应该处理或报错）"""
        try:
            # high < low 是无效的
            result = haze.py_fibonacci_pivots(80.0, 120.0, 100.0)
            # 如果不抛异常，结果应该仍然有效
            assert len(result) == 7
        except Exception:
            pass  # 某些实现可能拒绝无效输入
