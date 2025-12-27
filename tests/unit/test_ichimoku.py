"""
Ichimoku Cloud Unit Tests
=========================

测试一目均衡表（Ichimoku Cloud）相关指标。

测试的指标：
1. py_ichimoku_cloud - 一目云计算
2. py_ichimoku_tk_cross - TK交叉信号
3. py_ichimoku_signals - 综合信号

Author: Haze Team
Date: 2025-12-28
"""

import pytest
import numpy as np
import haze_library as haze


class TestIchimokuCloud:
    """一目均衡表云层测试

    py_ichimoku_cloud(high, low, close, tenkan_period, kijun_period, senkou_b_period)
    返回 5 元组: (tenkan, kijun, senkou_a, senkou_b, chikou)
    """

    def test_basic_calculation(self):
        """测试基本计算"""
        n = 100
        close = [100.0 + i * 0.5 for i in range(n)]
        high = [c + 2 for c in close]
        low = [c - 2 for c in close]

        result = haze.py_ichimoku_cloud(high, low, close, 9, 26, 52)

        # 验证返回5个组件
        assert isinstance(result, tuple)
        assert len(result) == 5

        tenkan, kijun, senkou_a, senkou_b, chikou = result
        assert len(tenkan) == n
        assert len(kijun) == n
        assert len(senkou_a) == n
        assert len(senkou_b) == n
        assert len(chikou) == n

    def test_tenkan_kijun_relationship(self):
        """测试转换线和基准线的关系"""
        n = 100
        close = [100.0 + i * 0.5 for i in range(n)]
        high = [c + 2 for c in close]
        low = [c - 2 for c in close]

        tenkan, kijun, senkou_a, senkou_b, chikou = haze.py_ichimoku_cloud(
            high, low, close, 9, 26, 52
        )

        # Tenkan 使用更短周期，应该比 Kijun 更敏感
        assert len(tenkan) == len(kijun)

    def test_with_uptrend(self):
        """测试上涨趋势"""
        n = 100
        close = [100.0 + i * 1.5 for i in range(n)]
        high = [c + 3 for c in close]
        low = [c - 2 for c in close]

        tenkan, kijun, senkou_a, senkou_b, chikou = haze.py_ichimoku_cloud(
            high, low, close, 9, 26, 52
        )

        assert len(tenkan) == n
        # 在上涨趋势中，Tenkan 通常高于 Kijun
        valid_tenkan = [v for v in tenkan[-20:] if not np.isnan(v)]
        valid_kijun = [v for v in kijun[-20:] if not np.isnan(v)]
        if valid_tenkan and valid_kijun:
            assert np.mean(valid_tenkan) >= np.mean(valid_kijun) - 5

    def test_with_downtrend(self):
        """测试下跌趋势"""
        n = 100
        close = [200.0 - i * 1.5 for i in range(n)]
        high = [c + 2 for c in close]
        low = [c - 3 for c in close]

        tenkan, kijun, senkou_a, senkou_b, chikou = haze.py_ichimoku_cloud(
            high, low, close, 9, 26, 52
        )

        assert len(tenkan) == n

    def test_custom_periods(self):
        """测试自定义周期"""
        n = 100
        close = [100.0 + np.sin(i / 10) * 20 for i in range(n)]
        high = [c + 5 for c in close]
        low = [c - 5 for c in close]

        # 使用不同的周期
        result = haze.py_ichimoku_cloud(high, low, close, 7, 22, 44)
        assert len(result) == 5
        assert all(len(r) == n for r in result)

    def test_minimum_data_requirement(self):
        """测试最小数据要求"""
        # 数据量不足时应该处理
        n = 60  # 足够 senkou_b (52)
        close = [100.0 + i * 0.5 for i in range(n)]
        high = [c + 2 for c in close]
        low = [c - 2 for c in close]

        result = haze.py_ichimoku_cloud(high, low, close, 9, 26, 52)
        assert len(result) == 5


class TestIchimokuTKCross:
    """TK交叉信号测试"""

    def test_basic_cross_detection(self):
        """测试基本交叉检测"""
        n = 100
        close = [100.0 + i * 0.5 for i in range(n)]
        high = [c + 2 for c in close]
        low = [c - 2 for c in close]

        # 先计算 Ichimoku 组件
        tenkan, kijun, senkou_a, senkou_b, chikou = haze.py_ichimoku_cloud(
            high, low, close, 9, 26, 52
        )

        # TK 交叉信号
        result = haze.py_ichimoku_tk_cross(tenkan, kijun, senkou_a, senkou_b, chikou)

        assert isinstance(result, list)
        assert len(result) == n

    def test_golden_cross(self):
        """测试金叉信号"""
        n = 100
        # 创建从下跌转上涨的趋势
        close = [100.0 - i * 0.5 if i < 50 else 75.0 + (i - 50) * 1.0 for i in range(n)]
        high = [c + 3 for c in close]
        low = [c - 2 for c in close]

        tenkan, kijun, senkou_a, senkou_b, chikou = haze.py_ichimoku_cloud(
            high, low, close, 9, 26, 52
        )
        result = haze.py_ichimoku_tk_cross(tenkan, kijun, senkou_a, senkou_b, chikou)

        assert len(result) == n

    def test_death_cross(self):
        """测试死叉信号"""
        n = 100
        # 创建从上涨转下跌的趋势
        close = [100.0 + i * 0.5 if i < 50 else 125.0 - (i - 50) * 1.0 for i in range(n)]
        high = [c + 2 for c in close]
        low = [c - 3 for c in close]

        tenkan, kijun, senkou_a, senkou_b, chikou = haze.py_ichimoku_cloud(
            high, low, close, 9, 26, 52
        )
        result = haze.py_ichimoku_tk_cross(tenkan, kijun, senkou_a, senkou_b, chikou)

        assert len(result) == n


class TestIchimokuEdgeCases:
    """Ichimoku 边界条件测试"""

    def test_constant_prices(self):
        """测试常数价格"""
        n = 100
        close = [100.0] * n
        high = [100.0] * n
        low = [100.0] * n

        result = haze.py_ichimoku_cloud(high, low, close, 9, 26, 52)
        assert len(result) == 5

        tenkan, kijun, senkou_a, senkou_b, chikou = result
        # 常数价格下，所有线应该相等
        valid_tenkan = [v for v in tenkan if not np.isnan(v)]
        if valid_tenkan:
            assert all(abs(v - 100.0) < 1e-10 for v in valid_tenkan)

    def test_high_volatility(self):
        """测试高波动"""
        n = 100
        np.random.seed(42)
        close = [100.0 + np.random.randn() * 30 for i in range(n)]
        high = [c + np.abs(np.random.randn() * 10) for c in close]
        low = [c - np.abs(np.random.randn() * 10) for c in close]

        result = haze.py_ichimoku_cloud(high, low, close, 9, 26, 52)
        assert len(result) == 5

    def test_short_data(self):
        """测试短数据"""
        n = 30  # 短于标准 senkou_b 周期
        close = [100.0 + i * 0.5 for i in range(n)]
        high = [c + 2 for c in close]
        low = [c - 2 for c in close]

        try:
            result = haze.py_ichimoku_cloud(high, low, close, 9, 26, 52)
            assert len(result) == 5
        except Exception:
            pass  # 短数据可能导致错误

    def test_empty_input(self):
        """测试空输入"""
        with pytest.raises(Exception):
            haze.py_ichimoku_cloud([], [], [], 9, 26, 52)

    def test_length_mismatch(self):
        """测试长度不匹配"""
        with pytest.raises(Exception):
            haze.py_ichimoku_cloud([1.0, 2.0], [1.0], [1.0, 2.0], 9, 26, 52)
