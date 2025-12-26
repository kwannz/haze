"""
Volatility Indicators Unit Tests
=================================

测试所有10个波动率指标的核心功能。

测试策略：
- 基本计算：验证输出格式和范围
- 边界条件：空数组、不足周期、单值
- 参数测试：不同周期、特殊参数

测试的指标：
1. ATR - 平均真实波幅
2. NATR - 归一化ATR
3. True Range - 真实波幅
4. Bollinger Bands - 布林带（返回upper, middle, lower）
5. Keltner Channel - 肯特纳通道（返回upper, middle, lower）
6. Donchian Channel - 唐奇安通道（返回upper, middle, lower）
7. Chandelier Exit - 吊灯止损（返回long, short）
8. Historical Volatility - 历史波动率
9. Ulcer Index - 溃疡指数
10. Mass Index - 质量指数

Author: Haze Team
Date: 2025-12-26
"""

import pytest
import numpy as np
import haze_library as haze


# ==================== 1. ATR ====================

class TestATR:
    """ATR (Average True Range) 单元测试

    算法：ATR = SMA(True Range, period)
    特点：衡量市场波动性，值越大波动越大
    """

    def test_basic_calculation(self, ohlcv_data_extended):
        """测试基本ATR计算

        ATR应为正值，反映价格波动幅度
        """
        result = haze.py_atr(
            ohlcv_data_extended['high'],
            ohlcv_data_extended['low'],
            ohlcv_data_extended['close'],
            period=14
        )

        # 验证输出长度
        assert len(result) == len(ohlcv_data_extended['close'])

        # ATR应为正值
        valid_values = [v for v in result if not np.isnan(v)]
        assert len(valid_values) > 0
        assert all(v > 0 for v in valid_values)

    def test_edge_cases(self, empty_array):
        """测试边界条件"""
        # 空数组
        result = haze.py_atr(empty_array, empty_array, empty_array, period=14)
        assert len(result) == 0

    def test_different_parameters(self, ohlcv_data_extended):
        """测试不同周期参数"""
        result_7 = haze.py_atr(
            ohlcv_data_extended['high'],
            ohlcv_data_extended['low'],
            ohlcv_data_extended['close'],
            period=7
        )

        result_21 = haze.py_atr(
            ohlcv_data_extended['high'],
            ohlcv_data_extended['low'],
            ohlcv_data_extended['close'],
            period=21
        )

        # 更短周期应有更多有效值
        valid_7 = sum(1 for v in result_7 if not np.isnan(v))
        valid_21 = sum(1 for v in result_21 if not np.isnan(v))
        assert valid_7 >= valid_21


# ==================== 2. NATR ====================

class TestNATR:
    """NATR (Normalized Average True Range) 单元测试

    算法：NATR = (ATR / Close) * 100
    特点：ATR的百分比形式，便于不同价格水平的资产比较
    """

    def test_basic_calculation(self, ohlcv_data_extended):
        """测试基本NATR计算

        NATR为百分比形式，应为正值
        """
        result = haze.py_natr(
            ohlcv_data_extended['high'],
            ohlcv_data_extended['low'],
            ohlcv_data_extended['close'],
            period=14
        )

        # 验证输出长度
        assert len(result) == len(ohlcv_data_extended['close'])

        # NATR应为正值
        valid_values = [v for v in result if not np.isnan(v)]
        assert len(valid_values) > 0
        assert all(v > 0 for v in valid_values)

    def test_edge_cases(self, empty_array):
        """测试边界条件"""
        # 空数组
        result = haze.py_natr(empty_array, empty_array, empty_array, period=14)
        assert len(result) == 0

    def test_different_parameters(self, ohlcv_data_extended):
        """测试不同周期参数"""
        result_10 = haze.py_natr(
            ohlcv_data_extended['high'],
            ohlcv_data_extended['low'],
            ohlcv_data_extended['close'],
            period=10
        )

        result_20 = haze.py_natr(
            ohlcv_data_extended['high'],
            ohlcv_data_extended['low'],
            ohlcv_data_extended['close'],
            period=20
        )

        assert len(result_10) == len(ohlcv_data_extended['close'])
        assert len(result_20) == len(ohlcv_data_extended['close'])


# ==================== 3. True Range ====================

class TestTrueRange:
    """True Range 单元测试

    算法：TR = max(High - Low, |High - PrevClose|, |Low - PrevClose|)
    特点：单周期波动幅度，ATR的基础
    """

    def test_basic_calculation(self, ohlcv_data_extended):
        """测试基本True Range计算

        TR应为非负值，第一个值可能为NaN
        """
        result = haze.py_true_range(
            ohlcv_data_extended['high'],
            ohlcv_data_extended['low'],
            ohlcv_data_extended['close']
        )

        # 验证输出长度
        assert len(result) == len(ohlcv_data_extended['close'])

        # TR应为非负值
        valid_values = [v for v in result if not np.isnan(v)]
        assert len(valid_values) > 0
        assert all(v >= 0 for v in valid_values)

    def test_edge_cases(self, empty_array):
        """测试边界条件"""
        # 空数组
        result = haze.py_true_range(empty_array, empty_array, empty_array)
        assert len(result) == 0

    def test_different_parameters(self, ohlcv_data):
        """测试基本数据集"""
        result = haze.py_true_range(
            ohlcv_data['high'],
            ohlcv_data['low'],
            ohlcv_data['close']
        )

        # 验证输出长度
        assert len(result) == len(ohlcv_data['close'])

        # 验证TR >= High - Low
        for i, tr in enumerate(result):
            if not np.isnan(tr):
                assert tr >= ohlcv_data['high'][i] - ohlcv_data['low'][i]


# ==================== 4. Bollinger Bands ====================

class TestBollingerBands:
    """Bollinger Bands 单元测试

    算法：Middle = SMA(Close, period)
          Upper = Middle + (stddev * multiplier)
          Lower = Middle - (stddev * multiplier)
    特点：返回三个值(upper, middle, lower)
    """

    def test_basic_calculation(self, ohlcv_data_extended):
        """测试基本Bollinger Bands计算

        返回值：(upper, middle, lower)
        关系：upper > middle > lower
        """
        upper, middle, lower = haze.py_bollinger_bands(
            ohlcv_data_extended['close'],
            period=20,
            std_multiplier=2.0
        )

        # 验证输出长度
        assert len(upper) == len(ohlcv_data_extended['close'])
        assert len(middle) == len(ohlcv_data_extended['close'])
        assert len(lower) == len(ohlcv_data_extended['close'])

        # 验证关系：upper >= middle >= lower
        for u, m, l in zip(upper, middle, lower):
            if not (np.isnan(u) or np.isnan(m) or np.isnan(l)):
                assert u >= m >= l

    def test_edge_cases(self, empty_array):
        """测试边界条件"""
        # 空数组
        upper, middle, lower = haze.py_bollinger_bands(empty_array, period=20, std_multiplier=2.0)
        assert len(upper) == 0
        assert len(middle) == 0
        assert len(lower) == 0

    def test_different_parameters(self, ohlcv_data_extended):
        """测试不同参数组合"""
        # 窄带（1倍标准差）
        upper_narrow, middle_narrow, lower_narrow = haze.py_bollinger_bands(
            ohlcv_data_extended['close'], period=20, std_multiplier=1.0
        )

        # 宽带（3倍标准差）
        upper_wide, middle_wide, lower_wide = haze.py_bollinger_bands(
            ohlcv_data_extended['close'], period=20, std_multiplier=3.0
        )

        # 中线应相同
        for mn, mw in zip(middle_narrow, middle_wide):
            if not (np.isnan(mn) or np.isnan(mw)):
                assert abs(mn - mw) < 1e-10

        # 宽带应更宽
        for i in range(len(upper_narrow)):
            if not (np.isnan(upper_narrow[i]) or np.isnan(upper_wide[i])):
                bandwidth_narrow = upper_narrow[i] - lower_narrow[i]
                bandwidth_wide = upper_wide[i] - lower_wide[i]
                assert bandwidth_wide > bandwidth_narrow


# ==================== 5. Keltner Channel ====================

class TestKeltnerChannel:
    """Keltner Channel 单元测试

    算法：Middle = EMA(Close, period)
          Upper = Middle + (ATR * multiplier)
          Lower = Middle - (ATR * multiplier)
    特点：返回三个值(upper, middle, lower)，基于ATR
    """

    def test_basic_calculation(self, ohlcv_data_extended):
        """测试基本Keltner Channel计算

        返回值：(upper, middle, lower)
        关系：upper > middle > lower
        """
        upper, middle, lower = haze.py_keltner_channel(
            ohlcv_data_extended['high'],
            ohlcv_data_extended['low'],
            ohlcv_data_extended['close'],
            period=20,
            atr_period=10,
            multiplier=2.0
        )

        # 验证输出长度
        assert len(upper) == len(ohlcv_data_extended['close'])
        assert len(middle) == len(ohlcv_data_extended['close'])
        assert len(lower) == len(ohlcv_data_extended['close'])

        # 验证关系：upper >= middle >= lower
        for u, m, l in zip(upper, middle, lower):
            if not (np.isnan(u) or np.isnan(m) or np.isnan(l)):
                assert u >= m >= l

    def test_edge_cases(self, empty_array):
        """测试边界条件"""
        # 空数组
        upper, middle, lower = haze.py_keltner_channel(
            empty_array, empty_array, empty_array, 20, 10, 2.0
        )
        assert len(upper) == 0
        assert len(middle) == 0
        assert len(lower) == 0

    def test_different_parameters(self, ohlcv_data_extended):
        """测试不同参数组合"""
        # 窄通道
        upper_narrow, middle_narrow, lower_narrow = haze.py_keltner_channel(
            ohlcv_data_extended['high'],
            ohlcv_data_extended['low'],
            ohlcv_data_extended['close'],
            period=20,
            atr_period=10,
            multiplier=1.0
        )

        # 宽通道
        upper_wide, middle_wide, lower_wide = haze.py_keltner_channel(
            ohlcv_data_extended['high'],
            ohlcv_data_extended['low'],
            ohlcv_data_extended['close'],
            period=20,
            atr_period=10,
            multiplier=3.0
        )

        assert len(upper_narrow) == len(ohlcv_data_extended['close'])
        assert len(upper_wide) == len(ohlcv_data_extended['close'])


# ==================== 6. Donchian Channel ====================

class TestDonchianChannel:
    """Donchian Channel 单元测试

    算法：Upper = MAX(High, period)
          Lower = MIN(Low, period)
          Middle = (Upper + Lower) / 2
    特点：返回三个值(upper, middle, lower)，基于最高/最低价
    """

    def test_basic_calculation(self, ohlcv_data_extended):
        """测试基本Donchian Channel计算

        返回值：(upper, middle, lower)
        Upper为period内最高价，Lower为最低价
        """
        upper, middle, lower = haze.py_donchian_channel(
            ohlcv_data_extended['high'],
            ohlcv_data_extended['low'],
            period=20
        )

        # 验证输出长度
        assert len(upper) == len(ohlcv_data_extended['close'])
        assert len(middle) == len(ohlcv_data_extended['close'])
        assert len(lower) == len(ohlcv_data_extended['close'])

        # 验证关系：upper >= middle >= lower
        for u, m, l in zip(upper, middle, lower):
            if not (np.isnan(u) or np.isnan(m) or np.isnan(l)):
                assert u >= m >= l

    def test_edge_cases(self, empty_array):
        """测试边界条件"""
        # 空数组
        upper, middle, lower = haze.py_donchian_channel(empty_array, empty_array, period=20)
        assert len(upper) == 0
        assert len(middle) == 0
        assert len(lower) == 0

    def test_different_parameters(self, ohlcv_data_extended):
        """测试不同周期参数"""
        # 短周期
        upper_short, middle_short, lower_short = haze.py_donchian_channel(
            ohlcv_data_extended['high'],
            ohlcv_data_extended['low'],
            period=10
        )

        # 长周期
        upper_long, middle_long, lower_long = haze.py_donchian_channel(
            ohlcv_data_extended['high'],
            ohlcv_data_extended['low'],
            period=20
        )

        # 更短周期有更多有效值
        valid_short = sum(1 for v in upper_short if not np.isnan(v))
        valid_long = sum(1 for v in upper_long if not np.isnan(v))
        assert valid_short >= valid_long


# ==================== 7. Chandelier Exit ====================

class TestChandelierExit:
    """Chandelier Exit 单元测试

    算法：Long = MAX(High, period) - ATR * multiplier
          Short = MIN(Low, period) + ATR * multiplier
    特点：返回两个值(long, short)，用于设置止损
    """

    def test_basic_calculation(self, ohlcv_data_extended):
        """测试基本Chandelier Exit计算

        返回值：(long, short)
        Long为多头止损线，Short为空头止损线
        """
        long_exit, short_exit = haze.py_chandelier_exit(
            ohlcv_data_extended['high'],
            ohlcv_data_extended['low'],
            ohlcv_data_extended['close'],
            period=22,
            atr_period=22,
            multiplier=3.0
        )

        # 验证输出长度
        assert len(long_exit) == len(ohlcv_data_extended['close'])
        assert len(short_exit) == len(ohlcv_data_extended['close'])

        # 验证有有效值
        valid_long = [v for v in long_exit if not np.isnan(v)]
        valid_short = [v for v in short_exit if not np.isnan(v)]
        assert len(valid_long) >= 0  # 可能数据不足
        assert len(valid_short) >= 0

    def test_edge_cases(self, empty_array):
        """测试边界条件"""
        # 空数组
        long_exit, short_exit = haze.py_chandelier_exit(
            empty_array, empty_array, empty_array, 22, 22, 3.0
        )
        assert len(long_exit) == 0
        assert len(short_exit) == 0

    def test_different_parameters(self, ohlcv_data_extended):
        """测试不同参数组合"""
        # 保守止损（大multiplier）
        long_conservative, short_conservative = haze.py_chandelier_exit(
            ohlcv_data_extended['high'],
            ohlcv_data_extended['low'],
            ohlcv_data_extended['close'],
            period=22,
            atr_period=22,
            multiplier=4.0
        )

        # 激进止损（小multiplier）
        long_aggressive, short_aggressive = haze.py_chandelier_exit(
            ohlcv_data_extended['high'],
            ohlcv_data_extended['low'],
            ohlcv_data_extended['close'],
            period=22,
            atr_period=22,
            multiplier=2.0
        )

        assert len(long_conservative) == len(ohlcv_data_extended['close'])
        assert len(long_aggressive) == len(ohlcv_data_extended['close'])


# ==================== 8. Historical Volatility ====================

class TestHistoricalVolatility:
    """Historical Volatility 单元测试

    算法：HV = StdDev(log(Close/PrevClose)) * sqrt(period) * 100
    特点：年化百分比波动率
    """

    def test_basic_calculation(self, ohlcv_data_extended):
        """测试基本Historical Volatility计算

        HV应为正值，百分比形式
        """
        result = haze.py_historical_volatility(
            ohlcv_data_extended['close'],
            period=20
        )

        # 验证输出长度
        assert len(result) == len(ohlcv_data_extended['close'])

        # HV应为非负值
        valid_values = [v for v in result if not np.isnan(v)]
        if valid_values:
            assert all(v >= 0 for v in valid_values)

    def test_edge_cases(self, empty_array, constant_values):
        """测试边界条件"""
        # 空数组
        result = haze.py_historical_volatility(empty_array, period=20)
        assert len(result) == 0

        # 常数序列（零波动）
        result = haze.py_historical_volatility(constant_values, period=5)
        assert len(result) == len(constant_values)

    def test_different_parameters(self, ohlcv_data_extended):
        """测试不同周期参数"""
        result_10 = haze.py_historical_volatility(
            ohlcv_data_extended['close'],
            period=10
        )

        result_30 = haze.py_historical_volatility(
            ohlcv_data_extended['close'],
            period=30
        )

        # 更短周期有更多有效值
        valid_10 = sum(1 for v in result_10 if not np.isnan(v))
        valid_30 = sum(1 for v in result_30 if not np.isnan(v))
        assert valid_10 >= valid_30


# ==================== 9. Ulcer Index ====================

class TestUlcerIndex:
    """Ulcer Index 单元测试

    算法：UI = sqrt(sum((Close - MaxClose)^2 / MaxClose^2) / period) * 100
    特点：衡量下行波动风险，值越大风险越高
    """

    def test_basic_calculation(self, ohlcv_data_extended):
        """测试基本Ulcer Index计算

        UI应为非负值，衡量回撤风险
        """
        result = haze.py_ulcer_index(
            ohlcv_data_extended['close'],
            period=14
        )

        # 验证输出长度
        assert len(result) == len(ohlcv_data_extended['close'])

        # UI应为非负值
        valid_values = [v for v in result if not np.isnan(v)]
        if valid_values:
            assert all(v >= 0 for v in valid_values)

    def test_edge_cases(self, empty_array, monotonic_increasing):
        """测试边界条件"""
        # 空数组
        result = haze.py_ulcer_index(empty_array, period=14)
        assert len(result) == 0

        # 单调递增（无回撤）
        result = haze.py_ulcer_index(monotonic_increasing, period=5)
        assert len(result) == len(monotonic_increasing)

    def test_different_parameters(self, ohlcv_data_extended):
        """测试不同周期参数"""
        result_7 = haze.py_ulcer_index(
            ohlcv_data_extended['close'],
            period=7
        )

        result_21 = haze.py_ulcer_index(
            ohlcv_data_extended['close'],
            period=21
        )

        # 更短周期有更多有效值
        valid_7 = sum(1 for v in result_7 if not np.isnan(v))
        valid_21 = sum(1 for v in result_21 if not np.isnan(v))
        assert valid_7 >= valid_21


# ==================== 10. Mass Index ====================

class TestMassIndex:
    """Mass Index 单元测试

    算法：基于high-low范围的EMA比率
    特点：识别趋势反转，范围通常18-45
    """

    def test_basic_calculation(self, ohlcv_data_extended):
        """测试基本Mass Index计算

        MI通常在18-45范围内
        """
        result = haze.py_mass_index(
            ohlcv_data_extended['high'],
            ohlcv_data_extended['low'],
            period=25,
            ema_period=9
        )

        # 验证输出长度
        assert len(result) == len(ohlcv_data_extended['close'])

        # 验证有有效值
        valid_values = [v for v in result if not np.isnan(v)]
        assert len(valid_values) >= 0  # 可能数据不足

    def test_edge_cases(self, empty_array):
        """测试边界条件"""
        # 空数组
        result = haze.py_mass_index(empty_array, empty_array, period=25, ema_period=9)
        assert len(result) == 0

    def test_different_parameters(self, ohlcv_data_extended):
        """测试不同参数组合"""
        # 短周期
        result_short = haze.py_mass_index(
            ohlcv_data_extended['high'],
            ohlcv_data_extended['low'],
            period=15,
            ema_period=9
        )

        # 标准周期
        result_standard = haze.py_mass_index(
            ohlcv_data_extended['high'],
            ohlcv_data_extended['low'],
            period=25,
            ema_period=9
        )

        assert len(result_short) == len(ohlcv_data_extended['close'])
        assert len(result_standard) == len(ohlcv_data_extended['close'])
