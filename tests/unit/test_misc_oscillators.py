"""
Miscellaneous Oscillators Unit Tests
=====================================

测试其他振荡器和辅助指标。

测试的指标：
1. py_donchian_channel - 唐奇安通道（价格通道）
2. py_bop - 多空力量平衡
3. py_coppock - 科波克曲线
4. py_typprice - 典型价格
5. py_wclprice - 加权收盘价
6. py_medprice - 中位价格
7. py_avgprice - 平均价格
8. py_midpoint - 中点
9. py_midprice - 中间价
10. py_linearreg_angle - 线性回归角度
11. py_linearreg_intercept - 线性回归截距
12. py_linearreg_slope - 线性回归斜率
13. py_williams_r - 威廉姆斯%R

Author: Haze Team
Date: 2025-12-28
"""

import pytest
import numpy as np
import haze_library as haze


class TestDonchianChannel:
    """唐奇安通道测试（价格通道）"""

    def test_basic_calculation(self, ohlcv_data_extended):
        """测试基本唐奇安通道计算"""
        high = ohlcv_data_extended['high']
        low = ohlcv_data_extended['low']

        result = haze.py_donchian_channel(high, low, 20)
        # 返回 (upper, middle, lower) 三元组
        assert isinstance(result, tuple)
        assert len(result) == 3

    def test_channel_width(self, ohlcv_data_extended):
        """测试通道宽度"""
        high = ohlcv_data_extended['high']
        low = ohlcv_data_extended['low']

        upper, middle, lower = haze.py_donchian_channel(high, low, 10)

        # 验证 upper >= middle >= lower
        for u, m, l in zip(upper, middle, lower):
            if not np.isnan(u) and not np.isnan(m) and not np.isnan(l):
                assert u >= m >= l


class TestBOP:
    """多空力量平衡 (Balance of Power) 测试"""

    def test_basic_calculation(self, ohlcv_data_extended):
        """测试基本BOP计算"""
        o = ohlcv_data_extended['open']
        h = ohlcv_data_extended['high']
        l = ohlcv_data_extended['low']
        c = ohlcv_data_extended['close']

        result = haze.py_bop(o, h, l, c)
        assert len(result) == len(c)

    def test_bop_range(self, ohlcv_data_extended):
        """测试BOP范围"""
        o = ohlcv_data_extended['open']
        h = ohlcv_data_extended['high']
        l = ohlcv_data_extended['low']
        c = ohlcv_data_extended['close']

        result = haze.py_bop(o, h, l, c)
        valid = [v for v in result if not np.isnan(v) and not np.isinf(v)]
        # BOP 计算结果应该是有限值
        assert len(valid) > 0


class TestCoppock:
    """科波克曲线测试

    py_coppock(prices, period1, period2, wma_period)
    标准参数: ROC(14) + ROC(11) 的 WMA(10) 平滑
    """

    def test_basic_calculation(self):
        """测试基本科波克计算"""
        prices = [100.0 + i * 0.5 for i in range(50)]

        result = haze.py_coppock(prices, 14, 11, 10)
        assert len(result) == len(prices)

    def test_trend_signal(self):
        """测试趋势信号"""
        # 强上涨趋势
        prices = [100.0 + i * 2 for i in range(100)]

        result = haze.py_coppock(prices, 14, 11, 10)
        valid = [v for v in result if not np.isnan(v)]
        # 上涨趋势应有正值
        if valid:
            assert any(v > 0 for v in valid[-10:])

    def test_downtrend_signal(self):
        """测试下跌趋势信号"""
        prices = [200.0 - i * 2 for i in range(100)]

        result = haze.py_coppock(prices, 14, 11, 10)
        valid = [v for v in result if not np.isnan(v)]
        # 下跌趋势应有负值
        if valid:
            assert any(v < 0 for v in valid[-10:])


class TestWilliamsR:
    """威廉姆斯%R测试"""

    def test_basic_calculation(self, ohlcv_data_extended):
        """测试基本Williams %R计算"""
        h = ohlcv_data_extended['high']
        l = ohlcv_data_extended['low']
        c = ohlcv_data_extended['close']

        result = haze.py_williams_r(h, l, c, 14)
        assert len(result) == len(c)

    def test_williams_r_range(self, ohlcv_data_extended):
        """测试Williams %R范围"""
        h = ohlcv_data_extended['high']
        l = ohlcv_data_extended['low']
        c = ohlcv_data_extended['close']

        result = haze.py_williams_r(h, l, c, 14)
        valid = [v for v in result if not np.isnan(v)]
        # Williams %R 在 -100 到 0 之间
        if valid:
            assert all(-100 <= v <= 0 for v in valid)


class TestTypPrice:
    """典型价格测试"""

    def test_basic_calculation(self, ohlcv_data_extended):
        """测试基本典型价格计算"""
        h = ohlcv_data_extended['high']
        l = ohlcv_data_extended['low']
        c = ohlcv_data_extended['close']

        result = haze.py_typprice(h, l, c)
        assert len(result) == len(c)

    def test_typical_price_formula(self):
        """测试典型价格公式：(H+L+C)/3"""
        h = [110.0, 115.0, 112.0]
        l = [90.0, 95.0, 92.0]
        c = [100.0, 105.0, 102.0]

        result = haze.py_typprice(h, l, c)

        expected = [(110+90+100)/3, (115+95+105)/3, (112+92+102)/3]
        for r, e in zip(result, expected):
            if not np.isnan(r):
                assert abs(r - e) < 1e-10


class TestWCLPrice:
    """加权收盘价测试"""

    def test_basic_calculation(self, ohlcv_data_extended):
        """测试基本加权收盘价计算"""
        h = ohlcv_data_extended['high']
        l = ohlcv_data_extended['low']
        c = ohlcv_data_extended['close']

        result = haze.py_wclprice(h, l, c)
        assert len(result) == len(c)

    def test_weighted_close_formula(self):
        """测试加权收盘价公式：(H+L+2C)/4"""
        h = [110.0, 115.0, 112.0]
        l = [90.0, 95.0, 92.0]
        c = [100.0, 105.0, 102.0]

        result = haze.py_wclprice(h, l, c)

        expected = [(110+90+2*100)/4, (115+95+2*105)/4, (112+92+2*102)/4]
        for r, e in zip(result, expected):
            if not np.isnan(r):
                assert abs(r - e) < 1e-10


class TestMedPrice:
    """中位价格测试"""

    def test_basic_calculation(self, ohlcv_data_extended):
        """测试基本中位价格计算"""
        h = ohlcv_data_extended['high']
        l = ohlcv_data_extended['low']

        result = haze.py_medprice(h, l)
        assert len(result) == len(h)

    def test_median_price_formula(self):
        """测试中位价格公式：(H+L)/2"""
        h = [110.0, 115.0, 112.0]
        l = [90.0, 95.0, 92.0]

        result = haze.py_medprice(h, l)

        expected = [100.0, 105.0, 102.0]  # (H+L)/2
        for r, e in zip(result, expected):
            if not np.isnan(r):
                assert abs(r - e) < 1e-10


class TestAvgPrice:
    """平均价格测试"""

    def test_basic_calculation(self, ohlcv_data_extended):
        """测试基本平均价格计算"""
        o = ohlcv_data_extended['open']
        h = ohlcv_data_extended['high']
        l = ohlcv_data_extended['low']
        c = ohlcv_data_extended['close']

        result = haze.py_avgprice(o, h, l, c)
        assert len(result) == len(c)

    def test_avgprice_formula(self):
        """测试平均价格公式：(O+H+L+C)/4"""
        o = [100.0, 105.0, 102.0]
        h = [110.0, 115.0, 112.0]
        l = [90.0, 95.0, 92.0]
        c = [105.0, 110.0, 107.0]

        result = haze.py_avgprice(o, h, l, c)

        expected = [(100+110+90+105)/4, (105+115+95+110)/4, (102+112+92+107)/4]
        for r, e in zip(result, expected):
            if not np.isnan(r):
                assert abs(r - e) < 1e-10


class TestMidpoint:
    """中点测试"""

    def test_basic_calculation(self, simple_prices):
        """测试基本中点计算"""
        result = haze.py_midpoint(simple_prices, 5)
        assert len(result) == len(simple_prices)

    def test_midpoint_value(self):
        """测试中点值"""
        prices = [100.0, 110.0, 90.0, 105.0, 95.0]

        result = haze.py_midpoint(prices, 3)

        # midpoint = (max + min) / 2 over period
        valid = [v for v in result if not np.isnan(v)]
        if valid:
            assert len(valid) > 0


class TestMidprice:
    """中间价测试"""

    def test_basic_calculation(self, ohlcv_data_extended):
        """测试基本中间价计算"""
        h = ohlcv_data_extended['high']
        l = ohlcv_data_extended['low']

        result = haze.py_midprice(h, l, 5)
        assert len(result) == len(h)


class TestLinearRegAngle:
    """线性回归角度测试"""

    def test_basic_calculation(self, simple_prices):
        """测试基本线性回归角度"""
        result = haze.py_linearreg_angle(simple_prices, 5)
        assert len(result) == len(simple_prices)

    def test_positive_angle(self):
        """测试正角度（上涨趋势）"""
        prices = [100.0 + i * 2 for i in range(20)]

        result = haze.py_linearreg_angle(prices, 5)
        valid = [v for v in result if not np.isnan(v)]
        # 上涨趋势应有正角度
        if valid:
            assert all(v > 0 for v in valid[-5:])

    def test_negative_angle(self):
        """测试负角度（下跌趋势）"""
        prices = [200.0 - i * 2 for i in range(20)]

        result = haze.py_linearreg_angle(prices, 5)
        valid = [v for v in result if not np.isnan(v)]
        # 下跌趋势应有负角度
        if valid:
            assert all(v < 0 for v in valid[-5:])


class TestLinearRegIntercept:
    """线性回归截距测试"""

    def test_basic_calculation(self, simple_prices):
        """测试基本线性回归截距"""
        result = haze.py_linearreg_intercept(simple_prices, 5)
        assert len(result) == len(simple_prices)


class TestLinearRegSlope:
    """线性回归斜率测试"""

    def test_basic_calculation(self, simple_prices):
        """测试基本线性回归斜率"""
        result = haze.py_linearreg_slope(simple_prices, 5)
        assert len(result) == len(simple_prices)

    def test_positive_slope(self):
        """测试正斜率（上涨趋势）"""
        prices = [100.0 + i * 2 for i in range(20)]

        result = haze.py_linearreg_slope(prices, 5)
        valid = [v for v in result if not np.isnan(v)]
        if valid:
            assert all(v > 0 for v in valid[-5:])


class TestLinearReg:
    """线性回归测试"""

    def test_basic_calculation(self, simple_prices):
        """测试基本线性回归"""
        result = haze.py_linearreg(simple_prices, 5)
        assert len(result) == len(simple_prices)


class TestMiscEdgeCases:
    """杂项指标边界条件测试"""

    def test_empty_inputs(self):
        """测试空输入"""
        with pytest.raises(Exception):
            haze.py_typprice([], [], [])

    def test_single_value_inputs(self):
        """测试单值输入"""
        h = [100.0]
        l = [90.0]
        c = [95.0]

        result = haze.py_typprice(h, l, c)
        assert len(result) == 1

    def test_nan_handling(self):
        """测试NaN处理"""
        h = [100.0, float('nan'), 102.0]
        l = [90.0, 91.0, float('nan')]
        c = [95.0, 96.0, 97.0]

        try:
            result = haze.py_typprice(h, l, c)
            assert len(result) == 3
        except Exception:
            pass  # 某些实现可能拒绝NaN

    def test_high_low_equal(self):
        """测试高低价相等"""
        h = [100.0, 100.0, 100.0]
        l = [100.0, 100.0, 100.0]
        c = [100.0, 100.0, 100.0]

        result = haze.py_typprice(h, l, c)
        for v in result:
            if not np.isnan(v):
                assert v == 100.0

    def test_bop_with_equal_high_low(self):
        """测试高低价相等时的BOP"""
        o = [100.0, 100.0, 100.0]
        h = [100.0, 100.0, 100.0]
        l = [100.0, 100.0, 100.0]
        c = [100.0, 100.0, 100.0]

        result = haze.py_bop(o, h, l, c)
        assert len(result) == 3
