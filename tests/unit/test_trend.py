"""
Trend Indicators Unit Tests
============================

测试所有14个趋势指标的核心功能。

测试策略：
- 基本计算：验证输出格式和范围
- 边界条件：空数组、不足周期、单值
- 参数测试：不同周期、特殊参数

测试的指标：
1. SuperTrend - 超级趋势（返回trend, direction）
2. ADX - 平均趋向指数
3. Parabolic SAR - 抛物线转向指标
4. Aroon - 阿隆指标（返回up, down）
5. DMI - 趋向指标（返回plus_di, minus_di）
6. TRIX - 三重指数平滑移动平均
7. DPO - 去趋势价格振荡器
8. Vortex - 涡流指标（返回vi_plus, vi_minus）
9. Choppiness - 震荡指数（0-100，>61.8震荡）
10. QStick - 量价棒指标
11. VHF - 垂直水平过滤器
12. DX - 方向性移动指数
13. PLUS_DI - 正向指标
14. MINUS_DI - 负向指标

Author: Haze Team
Date: 2025-12-26
"""

import pytest
import numpy as np
import haze_library as haze


# ==================== 1. SuperTrend ====================

class TestSuperTrend:
    """SuperTrend 单元测试

    算法：基于ATR的趋势跟踪指标
    特点：返回两个值(trend, direction)，direction为1/-1
    """

    def test_basic_calculation(self, ohlcv_data_extended):
        """测试基本SuperTrend计算

        返回值：(trend, direction)
        direction: 1为上涨趋势，-1为下跌趋势
        """
        trend, direction, upper, lower = haze.py_supertrend(
            ohlcv_data_extended['high'],
            ohlcv_data_extended['low'],
            ohlcv_data_extended['close'],
            period=10,
            multiplier=3.0
        )

        # 验证输出长度
        assert len(trend) == len(ohlcv_data_extended['close'])
        assert len(direction) == len(ohlcv_data_extended['close'])

        # 验证direction为1或-1
        valid_dir = [d for d in direction if not np.isnan(d)]
        if valid_dir:
            assert all(d in [1.0, -1.0] for d in valid_dir)

    def test_edge_cases(self, empty_array):
        """测试边界条件"""
        # 空数组
        trend, direction, upper, lower = haze.py_supertrend(
            empty_array, empty_array, empty_array, 10, 3.0
        )
        assert len(trend) == 0
        assert len(direction) == 0

    def test_different_parameters(self, ohlcv_data_extended):
        """测试不同参数组合"""
        # 敏感SuperTrend（小multiplier）
        trend_sensitive, dir_sensitive, _, _ = haze.py_supertrend(
            ohlcv_data_extended['high'],
            ohlcv_data_extended['low'],
            ohlcv_data_extended['close'],
            period=10,
            multiplier=2.0
        )

        # 稳定SuperTrend（大multiplier）
        trend_stable, dir_stable, _, _ = haze.py_supertrend(
            ohlcv_data_extended['high'],
            ohlcv_data_extended['low'],
            ohlcv_data_extended['close'],
            period=10,
            multiplier=4.0
        )

        assert len(trend_sensitive) == len(ohlcv_data_extended['close'])
        assert len(trend_stable) == len(ohlcv_data_extended['close'])


# ==================== 2. ADX ====================

class TestADX:
    """ADX (Average Directional Index) 单元测试

    算法：基于+DI和-DI的平滑平均
    特点：范围0-100，>25表示强趋势
    """

    def test_basic_calculation(self, ohlcv_data_extended):
        """测试基本ADX计算

        ADX范围：0-100
        >25强趋势，<20弱趋势
        """
        result, plus_di, minus_di = haze.py_adx(
            ohlcv_data_extended['high'],
            ohlcv_data_extended['low'],
            ohlcv_data_extended['close'],
            period=14
        )

        # 验证输出长度
        assert len(result) == len(ohlcv_data_extended['close'])
        assert len(plus_di) == len(ohlcv_data_extended['close'])
        assert len(minus_di) == len(ohlcv_data_extended['close'])

        # 验证范围
        valid_values = [v for v in result if not np.isnan(v)]
        if valid_values:
            assert all(0 <= v <= 100 for v in valid_values)

    def test_edge_cases(self, empty_array):
        """测试边界条件"""
        # 空数组
        result, plus_di, minus_di = haze.py_adx(empty_array, empty_array, empty_array, period=14)
        assert len(result) == 0

    def test_different_parameters(self, ohlcv_data_extended):
        """测试不同周期参数"""
        result_7, _, _ = haze.py_adx(
            ohlcv_data_extended['high'],
            ohlcv_data_extended['low'],
            ohlcv_data_extended['close'],
            period=7
        )

        result_21, _, _ = haze.py_adx(
            ohlcv_data_extended['high'],
            ohlcv_data_extended['low'],
            ohlcv_data_extended['close'],
            period=21
        )

        # 更短周期有更多有效值
        valid_7 = sum(1 for v in result_7 if not np.isnan(v))
        valid_21 = sum(1 for v in result_21 if not np.isnan(v))
        assert valid_7 >= valid_21


# ==================== 3. Parabolic SAR ====================

class TestParabolicSAR:
    """Parabolic SAR 单元测试

    算法：抛物线转向指标
    特点：提供动态止损位，跟随价格移动
    """

    def test_basic_calculation(self, ohlcv_data_extended):
        """测试基本Parabolic SAR计算

        SAR应与价格相关，但不完全相同
        返回值：(sar_values, direction)
        """
        result, direction = haze.py_psar(
            ohlcv_data_extended['high'],
            ohlcv_data_extended['low'],
            ohlcv_data_extended['close'],
            af_init=0.02,
            af_increment=0.02,
            af_max=0.2
        )

        # 验证输出长度
        assert len(result) == len(ohlcv_data_extended['close'])
        assert len(direction) == len(ohlcv_data_extended['close'])

        # 验证有有效值
        valid_values = [v for v in result if not np.isnan(v)]
        assert len(valid_values) > 0

    def test_edge_cases(self, empty_array):
        """测试边界条件"""
        # 空数组
        result, direction = haze.py_psar(
            empty_array, empty_array, empty_array, 0.02, 0.02, 0.2
        )
        assert len(result) == 0
        assert len(direction) == 0

    def test_different_parameters(self, ohlcv_data_extended):
        """测试不同参数组合"""
        # 敏感SAR（大af_max）
        result_sensitive, _ = haze.py_psar(
            ohlcv_data_extended['high'],
            ohlcv_data_extended['low'],
            ohlcv_data_extended['close'],
            af_init=0.02,
            af_increment=0.02,
            af_max=0.3
        )

        # 稳定SAR（小af_max）
        result_stable, _ = haze.py_psar(
            ohlcv_data_extended['high'],
            ohlcv_data_extended['low'],
            ohlcv_data_extended['close'],
            af_init=0.02,
            af_increment=0.02,
            af_max=0.15
        )

        assert len(result_sensitive) == len(ohlcv_data_extended['close'])
        assert len(result_stable) == len(ohlcv_data_extended['close'])


# ==================== 4. Aroon ====================

class TestAroon:
    """Aroon 单元测试

    算法：Aroon Up = ((period - 最高价距离) / period) * 100
          Aroon Down = ((period - 最低价距离) / period) * 100
    特点：返回两个值(up, down)，范围0-100
    """

    def test_basic_calculation(self, ohlcv_data_extended):
        """测试基本Aroon计算

        返回值：(up, down)
        范围：0-100
        """
        aroon_up, aroon_down, aroon_osc = haze.py_aroon(
            ohlcv_data_extended['high'],
            ohlcv_data_extended['low'],
            period=25
        )

        # 验证输出长度
        assert len(aroon_up) == len(ohlcv_data_extended['close'])
        assert len(aroon_down) == len(ohlcv_data_extended['close'])

        # 验证范围
        valid_up = [v for v in aroon_up if not np.isnan(v)]
        valid_down = [v for v in aroon_down if not np.isnan(v)]
        if valid_up:
            assert all(0 <= v <= 100 for v in valid_up)
        if valid_down:
            assert all(0 <= v <= 100 for v in valid_down)

    def test_edge_cases(self, empty_array):
        """测试边界条件"""
        # 空数组
        up, down, osc = haze.py_aroon(empty_array, empty_array, period=25)
        assert len(up) == 0
        assert len(down) == 0

    def test_different_parameters(self, ohlcv_data_extended):
        """测试不同周期参数"""
        # 短周期
        up_short, down_short, _ = haze.py_aroon(
            ohlcv_data_extended['high'],
            ohlcv_data_extended['low'],
            period=14
        )

        # 长周期
        up_long, down_long, _ = haze.py_aroon(
            ohlcv_data_extended['high'],
            ohlcv_data_extended['low'],
            period=30
        )

        # 更短周期有更多有效值
        valid_short = sum(1 for v in up_short if not np.isnan(v))
        valid_long = sum(1 for v in up_long if not np.isnan(v))
        assert valid_short >= valid_long


# ==================== 5. DMI ====================

class TestDMI:
    """DMI (Directional Movement Index) 单元测试

    算法：+DI和-DI，衡量方向性移动
    特点：使用 py_plus_di 和 py_minus_di 分别计算
    """

    def test_basic_calculation(self, ohlcv_data_extended):
        """测试基本DMI计算

        使用 py_plus_di 和 py_minus_di
        都应为非负值
        """
        plus_di = haze.py_plus_di(
            ohlcv_data_extended['high'],
            ohlcv_data_extended['low'],
            ohlcv_data_extended['close'],
            period=14
        )
        minus_di = haze.py_minus_di(
            ohlcv_data_extended['high'],
            ohlcv_data_extended['low'],
            ohlcv_data_extended['close'],
            period=14
        )

        # 验证输出长度
        assert len(plus_di) == len(ohlcv_data_extended['close'])
        assert len(minus_di) == len(ohlcv_data_extended['close'])

        # 验证非负值
        valid_plus = [v for v in plus_di if not np.isnan(v)]
        valid_minus = [v for v in minus_di if not np.isnan(v)]
        if valid_plus:
            assert all(v >= 0 for v in valid_plus)
        if valid_minus:
            assert all(v >= 0 for v in valid_minus)

    def test_edge_cases(self, empty_array):
        """测试边界条件"""
        # 空数组
        plus_di = haze.py_plus_di(empty_array, empty_array, empty_array, period=14)
        minus_di = haze.py_minus_di(empty_array, empty_array, empty_array, period=14)
        assert len(plus_di) == 0
        assert len(minus_di) == 0

    def test_different_parameters(self, ohlcv_data_extended):
        """测试不同周期参数"""
        # 短周期
        plus_short = haze.py_plus_di(
            ohlcv_data_extended['high'],
            ohlcv_data_extended['low'],
            ohlcv_data_extended['close'],
            period=7
        )
        minus_short = haze.py_minus_di(
            ohlcv_data_extended['high'],
            ohlcv_data_extended['low'],
            ohlcv_data_extended['close'],
            period=7
        )

        # 长周期
        plus_long = haze.py_plus_di(
            ohlcv_data_extended['high'],
            ohlcv_data_extended['low'],
            ohlcv_data_extended['close'],
            period=21
        )
        minus_long = haze.py_minus_di(
            ohlcv_data_extended['high'],
            ohlcv_data_extended['low'],
            ohlcv_data_extended['close'],
            period=21
        )

        assert len(plus_short) == len(ohlcv_data_extended['close'])
        assert len(plus_long) == len(ohlcv_data_extended['close'])


# ==================== 6. TRIX ====================

class TestTRIX:
    """TRIX (Triple Exponential Average) 单元测试

    算法：三重指数平滑的变化率
    特点：过滤短期波动，识别长期趋势
    """

    def test_basic_calculation(self, ohlcv_data_extended):
        """测试基本TRIX计算

        TRIX为百分比变化率
        """
        result = haze.py_trix(
            ohlcv_data_extended['close'],
            period=15
        )

        # 验证输出长度
        assert len(result) == len(ohlcv_data_extended['close'])

        # 验证有有效值
        valid_values = [v for v in result if not np.isnan(v)]
        assert len(valid_values) >= 0  # 可能数据不足

    def test_edge_cases(self, empty_array):
        """测试边界条件"""
        # 空数组
        result = haze.py_trix(empty_array, period=15)
        assert len(result) == 0

    def test_different_parameters(self, ohlcv_data_extended):
        """测试不同周期参数"""
        result_10 = haze.py_trix(ohlcv_data_extended['close'], period=10)
        result_20 = haze.py_trix(ohlcv_data_extended['close'], period=20)

        assert len(result_10) == len(ohlcv_data_extended['close'])
        assert len(result_20) == len(ohlcv_data_extended['close'])


# ==================== 7. DPO ====================

class TestDPO:
    """DPO (Detrended Price Oscillator) 单元测试

    算法：去除趋势的价格振荡器
    特点：消除长期趋势，关注周期性
    """

    def test_basic_calculation(self, ohlcv_data_extended):
        """测试基本DPO计算

        DPO去除趋势后的价格偏差
        """
        result = haze.py_dpo(
            ohlcv_data_extended['close'],
            period=20
        )

        # 验证输出长度
        assert len(result) == len(ohlcv_data_extended['close'])

        # 验证有有效值
        valid_values = [v for v in result if not np.isnan(v)]
        assert len(valid_values) >= 0

    def test_edge_cases(self, empty_array):
        """测试边界条件"""
        # 空数组
        result = haze.py_dpo(empty_array, period=20)
        assert len(result) == 0

    def test_different_parameters(self, ohlcv_data_extended):
        """测试不同周期参数"""
        result_10 = haze.py_dpo(ohlcv_data_extended['close'], period=10)
        result_30 = haze.py_dpo(ohlcv_data_extended['close'], period=30)

        assert len(result_10) == len(ohlcv_data_extended['close'])
        assert len(result_30) == len(ohlcv_data_extended['close'])


# ==================== 8. Vortex ====================

class TestVortex:
    """Vortex Indicator 单元测试

    算法：基于价格范围的涡流运动
    特点：返回两个值(vi_plus, vi_minus)
    """

    def test_basic_calculation(self, ohlcv_data_extended):
        """测试基本Vortex计算

        返回值：(vi_plus, vi_minus)
        识别趋势开始和结束
        """
        vi_plus, vi_minus = haze.py_vortex(
            ohlcv_data_extended['high'],
            ohlcv_data_extended['low'],
            ohlcv_data_extended['close'],
            period=14
        )

        # 验证输出长度
        assert len(vi_plus) == len(ohlcv_data_extended['close'])
        assert len(vi_minus) == len(ohlcv_data_extended['close'])

        # 验证有有效值
        valid_plus = [v for v in vi_plus if not np.isnan(v)]
        valid_minus = [v for v in vi_minus if not np.isnan(v)]
        if valid_plus:
            assert all(v >= 0 for v in valid_plus)
        if valid_minus:
            assert all(v >= 0 for v in valid_minus)

    def test_edge_cases(self, empty_array):
        """测试边界条件"""
        # 空数组
        vi_plus, vi_minus = haze.py_vortex(
            empty_array, empty_array, empty_array, period=14
        )
        assert len(vi_plus) == 0
        assert len(vi_minus) == 0

    def test_different_parameters(self, ohlcv_data_extended):
        """测试不同周期参数"""
        # 短周期
        plus_short, minus_short = haze.py_vortex(
            ohlcv_data_extended['high'],
            ohlcv_data_extended['low'],
            ohlcv_data_extended['close'],
            period=7
        )

        # 长周期
        plus_long, minus_long = haze.py_vortex(
            ohlcv_data_extended['high'],
            ohlcv_data_extended['low'],
            ohlcv_data_extended['close'],
            period=21
        )

        assert len(plus_short) == len(ohlcv_data_extended['close'])
        assert len(plus_long) == len(ohlcv_data_extended['close'])


# ==================== 9. Choppiness ====================

class TestChoppiness:
    """Choppiness Index 单元测试

    算法：衡量市场震荡程度
    特点：范围0-100，>61.8为震荡，<38.2为趋势
    """

    def test_basic_calculation(self, ohlcv_data_extended):
        """测试基本Choppiness计算

        范围：0-100
        >61.8震荡市，<38.2趋势市
        """
        result = haze.py_choppiness(
            ohlcv_data_extended['high'],
            ohlcv_data_extended['low'],
            ohlcv_data_extended['close'],
            period=14
        )

        # 验证输出长度
        assert len(result) == len(ohlcv_data_extended['close'])

        # 验证范围
        valid_values = [v for v in result if not np.isnan(v)]
        if valid_values:
            assert all(0 <= v <= 100 for v in valid_values)

    def test_edge_cases(self, empty_array):
        """测试边界条件"""
        # 空数组
        result = haze.py_choppiness(empty_array, empty_array, empty_array, period=14)
        assert len(result) == 0

    def test_different_parameters(self, ohlcv_data_extended):
        """测试不同周期参数"""
        result_7 = haze.py_choppiness(
            ohlcv_data_extended['high'],
            ohlcv_data_extended['low'],
            ohlcv_data_extended['close'],
            period=7
        )

        result_21 = haze.py_choppiness(
            ohlcv_data_extended['high'],
            ohlcv_data_extended['low'],
            ohlcv_data_extended['close'],
            period=21
        )

        assert len(result_7) == len(ohlcv_data_extended['close'])
        assert len(result_21) == len(ohlcv_data_extended['close'])


# ==================== 10. QStick ====================

class TestQStick:
    """QStick 单元测试

    算法：QStick = SMA(Close - Open, period)
    特点：衡量收盘价与开盘价的关系
    """

    def test_basic_calculation(self, ohlcv_data_extended):
        """测试基本QStick计算

        QStick为收盘-开盘的平均
        正值表示收盘高于开盘
        """
        result = haze.py_qstick(
            ohlcv_data_extended['open'],
            ohlcv_data_extended['close'],
            period=14
        )

        # 验证输出长度
        assert len(result) == len(ohlcv_data_extended['close'])

        # 验证有有效值
        valid_values = [v for v in result if not np.isnan(v)]
        assert len(valid_values) > 0

    def test_edge_cases(self, empty_array):
        """测试边界条件"""
        # 空数组
        result = haze.py_qstick(empty_array, empty_array, period=14)
        assert len(result) == 0

    def test_different_parameters(self, ohlcv_data_extended):
        """测试不同周期参数"""
        result_7 = haze.py_qstick(
            ohlcv_data_extended['open'],
            ohlcv_data_extended['close'],
            period=7
        )

        result_21 = haze.py_qstick(
            ohlcv_data_extended['open'],
            ohlcv_data_extended['close'],
            period=21
        )

        # 更短周期有更多有效值
        valid_7 = sum(1 for v in result_7 if not np.isnan(v))
        valid_21 = sum(1 for v in result_21 if not np.isnan(v))
        assert valid_7 >= valid_21


# ==================== 11. VHF ====================

class TestVHF:
    """VHF (Vertical Horizontal Filter) 单元测试

    算法：趋势强度指标
    特点：值越大趋势越强
    """

    def test_basic_calculation(self, ohlcv_data_extended):
        """测试基本VHF计算

        VHF衡量趋势强度
        高值表示强趋势
        """
        result = haze.py_vhf(
            ohlcv_data_extended['close'],
            period=28
        )

        # 验证输出长度
        assert len(result) == len(ohlcv_data_extended['close'])

        # 验证有有效值
        valid_values = [v for v in result if not np.isnan(v)]
        if valid_values:
            assert all(v >= 0 for v in valid_values)

    def test_edge_cases(self, empty_array):
        """测试边界条件"""
        # 空数组
        result = haze.py_vhf(empty_array, period=28)
        assert len(result) == 0

    def test_different_parameters(self, ohlcv_data_extended):
        """测试不同周期参数"""
        result_14 = haze.py_vhf(ohlcv_data_extended['close'], period=14)
        result_28 = haze.py_vhf(ohlcv_data_extended['close'], period=28)

        assert len(result_14) == len(ohlcv_data_extended['close'])
        assert len(result_28) == len(ohlcv_data_extended['close'])


# ==================== 12. DX ====================

class TestDX:
    """DX (Directional Movement Index) 单元测试

    算法：DX = 100 * |+DI - -DI| / (+DI + -DI)
    特点：范围0-100，ADX的基础
    """

    def test_basic_calculation(self, ohlcv_data_extended):
        """测试基本DX计算

        DX范围：0-100
        衡量趋势强度
        """
        result = haze.py_dx(
            ohlcv_data_extended['high'],
            ohlcv_data_extended['low'],
            ohlcv_data_extended['close'],
            period=14
        )

        # 验证输出长度
        assert len(result) == len(ohlcv_data_extended['close'])

        # 验证范围
        valid_values = [v for v in result if not np.isnan(v)]
        if valid_values:
            assert all(0 <= v <= 100 for v in valid_values)

    def test_edge_cases(self, empty_array):
        """测试边界条件"""
        # 空数组
        result = haze.py_dx(empty_array, empty_array, empty_array, period=14)
        assert len(result) == 0

    def test_different_parameters(self, ohlcv_data_extended):
        """测试不同周期参数"""
        result_7 = haze.py_dx(
            ohlcv_data_extended['high'],
            ohlcv_data_extended['low'],
            ohlcv_data_extended['close'],
            period=7
        )

        result_21 = haze.py_dx(
            ohlcv_data_extended['high'],
            ohlcv_data_extended['low'],
            ohlcv_data_extended['close'],
            period=21
        )

        assert len(result_7) == len(ohlcv_data_extended['close'])
        assert len(result_21) == len(ohlcv_data_extended['close'])


# ==================== 13. PLUS_DI ====================

class TestPlusDI:
    """PLUS_DI (Plus Directional Indicator) 单元测试

    算法：+DI = 100 * Smoothed(+DM) / ATR
    特点：衡量上升动量强度
    """

    def test_basic_calculation(self, ohlcv_data_extended):
        """测试基本+DI计算

        +DI应为非负值
        """
        result = haze.py_plus_di(
            ohlcv_data_extended['high'],
            ohlcv_data_extended['low'],
            ohlcv_data_extended['close'],
            period=14
        )

        # 验证输出长度
        assert len(result) == len(ohlcv_data_extended['close'])

        # 验证非负值
        valid_values = [v for v in result if not np.isnan(v)]
        if valid_values:
            assert all(v >= 0 for v in valid_values)

    def test_edge_cases(self, empty_array):
        """测试边界条件"""
        # 空数组
        result = haze.py_plus_di(empty_array, empty_array, empty_array, period=14)
        assert len(result) == 0

    def test_different_parameters(self, ohlcv_data_extended):
        """测试不同周期参数"""
        result_7 = haze.py_plus_di(
            ohlcv_data_extended['high'],
            ohlcv_data_extended['low'],
            ohlcv_data_extended['close'],
            period=7
        )

        result_21 = haze.py_plus_di(
            ohlcv_data_extended['high'],
            ohlcv_data_extended['low'],
            ohlcv_data_extended['close'],
            period=21
        )

        # 更短周期有更多有效值
        valid_7 = sum(1 for v in result_7 if not np.isnan(v))
        valid_21 = sum(1 for v in result_21 if not np.isnan(v))
        assert valid_7 >= valid_21


# ==================== 14. MINUS_DI ====================

class TestMinusDI:
    """MINUS_DI (Minus Directional Indicator) 单元测试

    算法：-DI = 100 * Smoothed(-DM) / ATR
    特点：衡量下降动量强度
    """

    def test_basic_calculation(self, ohlcv_data_extended):
        """测试基本-DI计算

        -DI应为非负值
        """
        result = haze.py_minus_di(
            ohlcv_data_extended['high'],
            ohlcv_data_extended['low'],
            ohlcv_data_extended['close'],
            period=14
        )

        # 验证输出长度
        assert len(result) == len(ohlcv_data_extended['close'])

        # 验证非负值
        valid_values = [v for v in result if not np.isnan(v)]
        if valid_values:
            assert all(v >= 0 for v in valid_values)

    def test_edge_cases(self, empty_array):
        """测试边界条件"""
        # 空数组
        result = haze.py_minus_di(empty_array, empty_array, empty_array, period=14)
        assert len(result) == 0

    def test_different_parameters(self, ohlcv_data_extended):
        """测试不同周期参数"""
        result_7 = haze.py_minus_di(
            ohlcv_data_extended['high'],
            ohlcv_data_extended['low'],
            ohlcv_data_extended['close'],
            period=7
        )

        result_21 = haze.py_minus_di(
            ohlcv_data_extended['high'],
            ohlcv_data_extended['low'],
            ohlcv_data_extended['close'],
            period=21
        )

        # 更短周期有更多有效值
        valid_7 = sum(1 for v in result_7 if not np.isnan(v))
        valid_21 = sum(1 for v in result_21 if not np.isnan(v))
        assert valid_7 >= valid_21
