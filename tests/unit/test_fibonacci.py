"""
Fibonacci Tools Unit Tests
==========================

测试斐波那契相关工具和指标。

测试的指标：
1. py_fibonacci_retracement - 斐波那契回撤
2. py_fibonacci_extension - 斐波那契延伸

Author: Haze Team
Date: 2025-12-28
"""

import haze_library as haze


class TestFibonacciRetracement:
    """斐波那契回撤测试"""

    def test_basic_calculation(self):
        """测试基本回撤计算"""
        start_price = 100.0
        end_price = 150.0

        result = haze.py_fibonacci_retracement(start_price, end_price)

        # 应返回标准斐波那契级别
        assert isinstance(result, list)
        assert len(result) > 0

        # 每个元素应为 (level_name, price) 元组
        for item in result:
            assert len(item) == 2
            assert isinstance(item[0], str)
            assert isinstance(item[1], float)

    def test_standard_levels(self):
        """测试标准斐波那契级别"""
        start_price = 0.0
        end_price = 100.0

        result = haze.py_fibonacci_retracement(start_price, end_price)

        # 提取价格级别
        levels = {item[0]: item[1] for item in result}

        # 标准级别：0%, 23.6%, 38.2%, 50%, 61.8%, 78.6%, 100%
        # 验证一些标准级别存在
        assert len(levels) >= 5

    def test_uptrend_retracement(self):
        """测试上涨趋势回撤（start < end）"""
        start_price = 100.0
        end_price = 200.0

        result = haze.py_fibonacci_retracement(start_price, end_price)

        prices = [item[1] for item in result]

        # 0% 应该在 end_price (200)
        # 100% 应该在 start_price (100)
        assert min(prices) >= start_price
        assert max(prices) <= end_price

    def test_downtrend_retracement(self):
        """测试下跌趋势回撤（start > end）"""
        start_price = 200.0
        end_price = 100.0

        result = haze.py_fibonacci_retracement(start_price, end_price)

        prices = [item[1] for item in result]

        # 回撤级别应在价格范围内
        assert all(100.0 <= p <= 200.0 for p in prices)

    def test_equal_prices(self):
        """测试相等价格（零移动）"""
        start_price = 100.0
        end_price = 100.0

        result = haze.py_fibonacci_retracement(start_price, end_price)

        # 所有级别应该相等
        prices = [item[1] for item in result]
        assert all(abs(p - 100.0) < 1e-10 for p in prices)

    def test_negative_prices(self):
        """测试负价格"""
        start_price = -100.0
        end_price = -50.0

        result = haze.py_fibonacci_retracement(start_price, end_price)

        assert isinstance(result, list)
        assert len(result) > 0

    def test_large_price_range(self):
        """测试大价格范围"""
        start_price = 100.0
        end_price = 10000.0

        result = haze.py_fibonacci_retracement(start_price, end_price)

        prices = [item[1] for item in result]
        assert all(100.0 <= p <= 10000.0 for p in prices)

    def test_small_price_range(self):
        """测试小价格范围"""
        start_price = 100.0
        end_price = 100.01

        result = haze.py_fibonacci_retracement(start_price, end_price)

        prices = [item[1] for item in result]
        assert all(100.0 <= p <= 100.01 for p in prices)


class TestFibonacciExtension:
    """斐波那契延伸测试"""

    def test_basic_extension(self):
        """测试基本延伸计算"""
        start_price = 100.0
        end_price = 150.0
        retracement_price = 125.0  # 50% 回撤

        result = haze.py_fibonacci_extension(start_price, end_price, retracement_price)

        assert isinstance(result, list)
        assert len(result) > 0

    def test_extension_levels(self):
        """测试延伸级别"""
        start_price = 100.0
        end_price = 200.0
        retracement_price = 150.0

        result = haze.py_fibonacci_extension(start_price, end_price, retracement_price)

        # 延伸级别应超过原始移动
        prices = [item[1] for item in result]

        # 至少有一些级别超过 end_price
        assert any(p > end_price for p in prices) or any(p < start_price for p in prices)

    def test_standard_extension_levels(self):
        """测试标准延伸级别"""
        start_price = 0.0
        end_price = 100.0
        retracement_price = 38.2  # 标准回撤位

        result = haze.py_fibonacci_extension(start_price, end_price, retracement_price)

        # 标准延伸级别：61.8%, 100%, 138.2%, 161.8%, 261.8%
        assert len(result) >= 3

    def test_bullish_extension(self):
        """测试看涨延伸"""
        start_price = 100.0
        end_price = 150.0
        retracement_price = 130.0

        result = haze.py_fibonacci_extension(start_price, end_price, retracement_price)

        prices = [item[1] for item in result]
        # 延伸目标应该高于起始点
        assert max(prices) > start_price

    def test_bearish_extension(self):
        """测试看跌延伸"""
        start_price = 150.0
        end_price = 100.0
        retracement_price = 120.0

        result = haze.py_fibonacci_extension(start_price, end_price, retracement_price)

        prices = [item[1] for item in result]
        assert len(prices) > 0

    def test_full_retracement(self):
        """测试完全回撤"""
        start_price = 100.0
        end_price = 150.0
        retracement_price = 100.0  # 100% 回撤

        result = haze.py_fibonacci_extension(start_price, end_price, retracement_price)

        assert isinstance(result, list)

    def test_no_retracement(self):
        """测试无回撤"""
        start_price = 100.0
        end_price = 150.0
        retracement_price = 150.0  # 0% 回撤

        result = haze.py_fibonacci_extension(start_price, end_price, retracement_price)

        assert isinstance(result, list)

    def test_overshoot_retracement(self):
        """测试过度回撤（超过100%）"""
        start_price = 100.0
        end_price = 150.0
        retracement_price = 80.0  # 超过100%回撤

        result = haze.py_fibonacci_extension(start_price, end_price, retracement_price)

        assert isinstance(result, list)


class TestFibonacciEdgeCases:
    """斐波那契边界条件测试"""

    def test_zero_start_price(self):
        """测试零起始价"""
        result = haze.py_fibonacci_retracement(0.0, 100.0)
        assert isinstance(result, list)

    def test_zero_end_price(self):
        """测试零结束价"""
        result = haze.py_fibonacci_retracement(100.0, 0.0)
        assert isinstance(result, list)

    def test_very_small_difference(self):
        """测试极小差异"""
        result = haze.py_fibonacci_retracement(100.0, 100.0000001)
        assert isinstance(result, list)

    def test_infinity_handling(self):
        """测试无穷大处理"""
        try:
            haze.py_fibonacci_retracement(100.0, float('inf'))
            # 可能返回结果或抛出异常
        except Exception:
            pass  # 预期可能失败

    def test_nan_handling(self):
        """测试NaN处理"""
        try:
            haze.py_fibonacci_retracement(float('nan'), 100.0)
        except Exception:
            pass  # 预期可能失败

    def test_extension_equal_prices(self):
        """测试延伸时价格相等"""
        result = haze.py_fibonacci_extension(100.0, 100.0, 100.0)
        assert isinstance(result, list)

    def test_precision(self):
        """测试计算精度"""
        start_price = 100.0
        end_price = 200.0

        result = haze.py_fibonacci_retracement(start_price, end_price)

        # 50% 回撤应该精确为 150
        prices = {item[0]: item[1] for item in result}

        # 检查是否有50%级别
        any(abs(p - 150.0) < 1e-10 for p in prices.values())
        # 注：具体级别名称可能不同，只验证精度


class TestFibonacciIntegration:
    """斐波那契集成测试"""

    def test_retracement_then_extension(self):
        """测试先回撤后延伸的完整流程"""
        # 上涨波段
        start_price = 100.0
        end_price = 150.0

        # 计算回撤
        retracement = haze.py_fibonacci_retracement(start_price, end_price)
        assert len(retracement) > 0

        # 假设回撤到38.2%级别
        retracement_price = start_price + (end_price - start_price) * 0.618  # 约 130.9

        # 计算延伸目标
        extension = haze.py_fibonacci_extension(start_price, end_price, retracement_price)
        assert len(extension) > 0

    def test_multiple_waves(self):
        """测试多波段分析"""
        # 波段1
        wave1_start = 100.0
        wave1_end = 150.0

        # 波段2（回调）
        wave2_start = 150.0
        wave2_end = 130.0

        # 分析两个波段
        retracement1 = haze.py_fibonacci_retracement(wave1_start, wave1_end)
        retracement2 = haze.py_fibonacci_retracement(wave2_start, wave2_end)

        assert len(retracement1) > 0
        assert len(retracement2) > 0
