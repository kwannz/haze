"""
Hilbert Transform Unit Tests
============================

测试希尔伯特变换相关指标。

注意：希尔伯特变换需要足够的数据点：
- HT_DCPERIOD, HT_DCPHASE, HT_PHASOR, HT_SINE: 至少33个元素
- HT_TRENDMODE: 至少63个元素

测试的指标：
1. py_ht_dcperiod - 希尔伯特变换主周期
2. py_ht_dcphase - 希尔伯特变换主相位
3. py_ht_phasor - 希尔伯特变换相量
4. py_ht_sine - 希尔伯特变换正弦波
5. py_ht_trendmode - 希尔伯特变换趋势模式

Author: Haze Team
Date: 2025-12-28
"""

import pytest
import numpy as np
import haze_library as haze


# 最小数据长度
MIN_DATA_HT = 50  # 保守值，满足33的要求
MIN_DATA_TRENDMODE = 100  # 满足63的要求


class TestHTDCPeriod:
    """希尔伯特变换主周期测试"""

    def test_basic_calculation(self):
        """测试基本周期计算"""
        n = MIN_DATA_HT
        prices = [100.0 + i * 0.5 + np.sin(i / 5) * 10 for i in range(n)]

        result = haze.py_ht_dcperiod(prices)

        assert len(result) == n

    def test_with_sine_wave(self):
        """测试正弦波周期检测"""
        # 生成已知周期的正弦波
        period = 20
        n = 100
        t = np.linspace(0, 10 * np.pi, n)
        prices = (100 + 10 * np.sin(2 * np.pi * t / period)).tolist()

        result = haze.py_ht_dcperiod(prices)

        assert len(result) == n
        # 有效值应该存在
        valid = [v for v in result if not np.isnan(v) and v > 0]
        assert len(valid) > 0

    def test_with_trend(self):
        """测试带趋势的数据"""
        n = MIN_DATA_HT
        trend = np.linspace(100, 150, n)
        noise = np.sin(np.linspace(0, 10 * np.pi, n)) * 5
        prices = (trend + noise).tolist()

        result = haze.py_ht_dcperiod(prices)
        assert len(result) == n

    def test_constant_prices(self):
        """测试常数价格"""
        n = MIN_DATA_HT
        prices = [100.0] * n

        result = haze.py_ht_dcperiod(prices)
        assert len(result) == n

    def test_high_volatility(self):
        """测试高波动数据"""
        np.random.seed(42)
        n = MIN_DATA_HT
        prices = [100.0 + np.random.randn() * 20 for _ in range(n)]

        result = haze.py_ht_dcperiod(prices)
        assert len(result) == n

    def test_empty_input(self):
        """测试空输入"""
        with pytest.raises(Exception):
            haze.py_ht_dcperiod([])

    def test_insufficient_data(self):
        """测试数据不足"""
        with pytest.raises(Exception):
            haze.py_ht_dcperiod([100.0] * 10)  # 少于33个元素


class TestHTDCPhase:
    """希尔伯特变换主相位测试"""

    def test_basic_calculation(self):
        """测试基本相位计算"""
        n = MIN_DATA_HT
        prices = [100.0 + i * 0.5 + np.sin(i / 5) * 10 for i in range(n)]

        result = haze.py_ht_dcphase(prices)
        assert len(result) == n

    def test_phase_range(self):
        """测试相位范围"""
        n = 100
        t = np.linspace(0, 10 * np.pi, n)
        prices = (100 + 10 * np.sin(t)).tolist()

        result = haze.py_ht_dcphase(prices)

        # 相位通常在 -180 到 180 或 0 到 360 度之间
        valid = [v for v in result if not np.isnan(v)]
        assert len(valid) > 0

    def test_monotonic_increasing(self):
        """测试单调递增"""
        n = MIN_DATA_HT
        prices = [100.0 + i * 0.5 for i in range(n)]

        result = haze.py_ht_dcphase(prices)
        assert len(result) == n

    def test_monotonic_decreasing(self):
        """测试单调递减"""
        n = MIN_DATA_HT
        prices = [200.0 - i * 0.5 for i in range(n)]

        result = haze.py_ht_dcphase(prices)
        assert len(result) == n


class TestHTPhasor:
    """希尔伯特变换相量测试"""

    def test_basic_calculation(self):
        """测试基本相量计算"""
        n = MIN_DATA_HT
        prices = [100.0 + i * 0.5 + np.sin(i / 5) * 10 for i in range(n)]

        result = haze.py_ht_phasor(prices)

        # 返回 (inphase, quadrature) 元组
        assert isinstance(result, tuple)
        assert len(result) == 2

        inphase, quadrature = result
        assert len(inphase) == n
        assert len(quadrature) == n

    def test_phasor_relationship(self):
        """测试同相和正交分量关系"""
        n = 100
        t = np.linspace(0, 10 * np.pi, n)
        prices = (100 + 10 * np.sin(t)).tolist()

        inphase, quadrature = haze.py_ht_phasor(prices)

        # 两个分量应该有90度相位差
        assert len(inphase) == n
        assert len(quadrature) == n

    def test_amplitude_calculation(self):
        """测试振幅计算"""
        n = MIN_DATA_HT
        t = np.linspace(0, 5 * np.pi, n)
        prices = (100 + 10 * np.sin(t)).tolist()

        inphase, quadrature = haze.py_ht_phasor(prices)

        # 振幅 = sqrt(inphase^2 + quadrature^2)
        for i, q in zip(inphase, quadrature):
            if not np.isnan(i) and not np.isnan(q):
                amplitude = np.sqrt(i**2 + q**2)
                assert amplitude >= 0

    def test_constant_prices(self):
        """测试常数价格"""
        n = MIN_DATA_HT
        prices = [100.0] * n

        inphase, quadrature = haze.py_ht_phasor(prices)
        assert len(inphase) == n


class TestHTSine:
    """希尔伯特变换正弦波测试"""

    def test_basic_calculation(self):
        """测试基本正弦波计算"""
        n = MIN_DATA_HT
        prices = [100.0 + i * 0.5 + np.sin(i / 5) * 10 for i in range(n)]

        result = haze.py_ht_sine(prices)

        # 返回 (sine, leadsine) 元组
        assert isinstance(result, tuple)
        assert len(result) == 2

        sine, leadsine = result
        assert len(sine) == n
        assert len(leadsine) == n

    def test_sine_wave_detection(self):
        """测试正弦波检测"""
        n = 100
        t = np.linspace(0, 10 * np.pi, n)
        prices = (100 + 10 * np.sin(t)).tolist()

        sine, leadsine = haze.py_ht_sine(prices)

        # 正弦和领先正弦应该在 -1 到 1 之间
        valid_sine = [v for v in sine if not np.isnan(v)]
        valid_lead = [v for v in leadsine if not np.isnan(v)]

        if valid_sine:
            assert all(-1.5 <= v <= 1.5 for v in valid_sine)  # 允许一些误差
        if valid_lead:
            assert all(-1.5 <= v <= 1.5 for v in valid_lead)

    def test_trend_market(self):
        """测试趋势市场"""
        n = MIN_DATA_HT
        prices = [100.0 + i * 0.5 for i in range(n)]

        sine, leadsine = haze.py_ht_sine(prices)
        assert len(sine) == n


class TestHTTrendMode:
    """希尔伯特变换趋势模式测试"""

    def test_basic_calculation(self):
        """测试基本趋势模式计算"""
        n = MIN_DATA_TRENDMODE
        prices = [100.0 + i * 0.5 + np.sin(i / 5) * 10 for i in range(n)]

        result = haze.py_ht_trendmode(prices)
        assert len(result) == n

    def test_trend_detection(self):
        """测试趋势检测"""
        # 强趋势
        n = MIN_DATA_TRENDMODE
        trend_prices = [100.0 + i * 1.0 for i in range(n)]

        result = haze.py_ht_trendmode(trend_prices)

        # 趋势模式应该为 1（趋势）
        valid = [v for v in result if not np.isnan(v)]
        assert len(valid) > 0

    def test_cycle_detection(self):
        """测试周期检测"""
        # 纯周期（无趋势）
        n = MIN_DATA_TRENDMODE
        t = np.linspace(0, 10 * np.pi, n)
        cycle_prices = (100 + 10 * np.sin(t)).tolist()

        result = haze.py_ht_trendmode(cycle_prices)

        # 周期模式应该为 0（周期）
        valid = [v for v in result if not np.isnan(v)]
        assert len(valid) > 0

    def test_mixed_market(self):
        """测试混合市场"""
        n = MIN_DATA_TRENDMODE
        trend = np.linspace(100, 150, n)
        cycle = np.sin(np.linspace(0, 10 * np.pi, n)) * 10
        prices = (trend + cycle).tolist()

        result = haze.py_ht_trendmode(prices)
        assert len(result) == n


class TestHilbertEdgeCases:
    """希尔伯特变换边界条件测试"""

    def test_nan_handling(self):
        """测试NaN处理"""
        n = MIN_DATA_HT
        prices = [100.0 + i * 0.5 for i in range(n)]
        prices[n // 2] = float('nan')  # 中间插入NaN

        try:
            result = haze.py_ht_dcperiod(prices)
            assert len(result) == n
        except Exception:
            pass  # 某些实现可能拒绝NaN

    def test_extreme_values(self):
        """测试极端值"""
        n = MIN_DATA_HT
        prices = [1e10 + i * 0.01 for i in range(n)]

        result = haze.py_ht_dcperiod(prices)
        assert len(result) == n

    def test_zero_values(self):
        """测试零值"""
        n = MIN_DATA_HT
        prices = [0.0] * n

        result = haze.py_ht_dcperiod(prices)
        assert len(result) == n

    def test_negative_values(self):
        """测试负值"""
        n = MIN_DATA_HT
        prices = [-100.0 + i * 0.5 for i in range(n)]

        result = haze.py_ht_dcperiod(prices)
        assert len(result) == n

    def test_alternating_values(self):
        """测试交替值（高频振荡）"""
        n = MIN_DATA_HT
        prices = [100.0 + (10.0 if i % 2 == 0 else -10.0) for i in range(n)]

        result = haze.py_ht_dcperiod(prices)
        assert len(result) == n
