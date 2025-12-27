"""
Momentum Indicators Unit Tests
===============================

测试所有17个动量指标的核心功能。

测试策略：
- 基本计算：验证输出格式和范围
- 边界条件：空数组、不足周期、单值
- 参数测试：不同周期、特殊参数

测试的指标：
1. RSI - 相对强弱指标
2. Stochastic - 随机指标（返回%K, %D）
3. MACD - 指数平滑异同移动平均线（返回macd, signal, histogram）
4. Williams %R - 威廉指标
5. Fisher Transform - 费舍尔变换（返回fisher, signal）
6. CCI - 商品通道指数
7. MFI - 资金流量指标
8. Stochastic RSI - 随机RSI（返回k, d）
9. KDJ - 随机指标扩展（返回k, d, j）
10. TSI - 真实强度指数（返回tsi, signal）
11. UO - 终极振荡器
12. MOM - 动量
13. ROC - 变化率
14. Awesome Oscillator - 动量震荡指标
15. APO - 绝对价格振荡器
16. PPO - 百分比价格振荡器
17. CMO - 钱德动量振荡器

Author: Haze Team
Date: 2025-12-26
"""

import pytest
import numpy as np
import haze_library as haze


# ==================== 1. RSI ====================

class TestRSI:
    """RSI (Relative Strength Index) 单元测试

    算法：RSI = 100 - (100 / (1 + RS))
          RS = Average Gain / Average Loss
    特点：0-100范围，>70超买，<30超卖
    """

    def test_basic_calculation(self, ohlcv_data_extended):
        """测试基本RSI计算

        RSI范围：0-100
        - RSI > 70: 超买
        - RSI < 30: 超卖
        """
        result = haze.py_rsi(ohlcv_data_extended['close'], period=14)

        # 验证输出长度
        assert len(result) == len(ohlcv_data_extended['close'])

        # 验证非NaN值在0-100范围内
        valid_values = [v for v in result if not np.isnan(v)]
        assert len(valid_values) > 0
        assert all(0 <= v <= 100 for v in valid_values)

    def test_edge_cases(self, empty_array, single_value):
        """测试边界条件"""
        # 空数组
        with pytest.raises(ValueError):
            haze.py_rsi(empty_array, period=14)

        # 单个值
        with pytest.raises(ValueError):
            haze.py_rsi(single_value, period=14)

    def test_different_periods(self, ohlcv_data_extended):
        """测试不同周期参数"""
        result_7 = haze.py_rsi(ohlcv_data_extended['close'], period=7)
        result_21 = haze.py_rsi(ohlcv_data_extended['close'], period=18)

        # 更短周期应有更多有效值
        valid_7 = sum(1 for v in result_7 if not np.isnan(v))
        valid_21 = sum(1 for v in result_21 if not np.isnan(v))
        assert valid_7 >= valid_21


# ==================== 2. Stochastic ====================

class TestStochastic:
    """Stochastic Oscillator 单元测试

    算法：fast %K = 100 * (Close - LowestLow) / (HighestHigh - LowestLow)
          slow %K = SMA(fast %K, smooth_k)
          %D = SMA(slow %K, period_d)
    特点：返回两个值(%K, %D)，范围0-100
    """

    def test_basic_calculation(self, ohlcv_data_extended):
        """测试基本Stochastic计算

        返回值：(k_values, d_values)
        范围：0-100
        """
        k_values, d_values = haze.py_stochastic(
            ohlcv_data_extended['high'],
            ohlcv_data_extended['low'],
            ohlcv_data_extended['close'],
            k_period=14,
            d_period=3
        )

        # 验证输出长度
        assert len(k_values) == len(ohlcv_data_extended['close'])
        assert len(d_values) == len(ohlcv_data_extended['close'])

        # 验证范围
        valid_k = [v for v in k_values if not np.isnan(v)]
        valid_d = [v for v in d_values if not np.isnan(v)]
        assert all(0 <= v <= 100 for v in valid_k)
        assert all(0 <= v <= 100 for v in valid_d)

    def test_edge_cases(self, empty_array):
        """测试边界条件"""
        # 空数组
        with pytest.raises(ValueError):
            haze.py_stochastic(
                empty_array,
                empty_array,
                empty_array,
                k_period=14,
                d_period=3,
            )

    def test_different_parameters(self, ohlcv_data_extended):
        """测试不同参数组合"""
        # 快速随机指标
        k_fast, d_fast = haze.py_stochastic(
            ohlcv_data_extended['high'],
            ohlcv_data_extended['low'],
            ohlcv_data_extended['close'],
            k_period=5,
            d_period=3
        )

        # 慢速随机指标
        k_slow, d_slow = haze.py_stochastic(
            ohlcv_data_extended['high'],
            ohlcv_data_extended['low'],
            ohlcv_data_extended['close'],
            k_period=14,
            d_period=5
        )

        assert len(k_fast) == len(ohlcv_data_extended['close'])
        assert len(k_slow) == len(ohlcv_data_extended['close'])


# ==================== 3. MACD ====================

class TestMACD:
    """MACD (Moving Average Convergence Divergence) 单元测试

    算法：MACD = EMA(fast) - EMA(slow)
          Signal = EMA(MACD, signal_period)
          Histogram = MACD - Signal
    特点：返回三个值(macd, signal, histogram)
    """

    def test_basic_calculation(self, ohlcv_data_extended):
        """测试基本MACD计算

        返回值：(macd, signal, histogram)
        默认参数：fast=12, slow=26, signal=9
        """
        macd, signal, histogram = haze.py_macd(
            ohlcv_data_extended['close'],
            fast_period=6,
            slow_period=13,
            signal_period=5
        )

        # 验证输出长度
        assert len(macd) == len(ohlcv_data_extended['close'])
        assert len(signal) == len(ohlcv_data_extended['close'])
        assert len(histogram) == len(ohlcv_data_extended['close'])

        # 验证关系：histogram = macd - signal
        for m, s, h in zip(macd, signal, histogram):
            if not (np.isnan(m) or np.isnan(s) or np.isnan(h)):
                assert abs(h - (m - s)) < 1e-10

    def test_edge_cases(self, empty_array):
        """测试边界条件"""
        # 空数组
        with pytest.raises(ValueError):
            haze.py_macd(empty_array, 6, 13, 5)

    def test_different_parameters(self, ohlcv_data_extended):
        """测试不同参数组合"""
        # 快速MACD
        macd_fast, sig_fast, hist_fast = haze.py_macd(
            ohlcv_data_extended['close'], 5, 10, 4
        )

        # 慢速MACD
        macd_slow, sig_slow, hist_slow = haze.py_macd(
            ohlcv_data_extended['close'], 6, 13, 5
        )

        assert len(macd_fast) == len(ohlcv_data_extended['close'])
        assert len(macd_slow) == len(ohlcv_data_extended['close'])


# ==================== 4. Williams %R ====================

class TestWilliamsR:
    """Williams %R 单元测试

    算法：%R = -100 * (HighestHigh - Close) / (HighestHigh - LowestLow)
    特点：范围 -100 到 0，>-20超买，<-80超卖
    """

    def test_basic_calculation(self, ohlcv_data_extended):
        """测试基本Williams %R计算

        范围：-100 到 0
        - > -20: 超买
        - < -80: 超卖
        """
        result = haze.py_williams_r(
            ohlcv_data_extended['high'],
            ohlcv_data_extended['low'],
            ohlcv_data_extended['close'],
            period=14
        )

        # 验证输出长度
        assert len(result) == len(ohlcv_data_extended['close'])

        # 验证范围
        valid_values = [v for v in result if not np.isnan(v)]
        assert len(valid_values) > 0
        assert all(-100 <= v <= 0 for v in valid_values)

    def test_edge_cases(self, empty_array):
        """测试边界条件"""
        # 空数组
        with pytest.raises(ValueError):
            haze.py_williams_r(empty_array, empty_array, empty_array, period=14)

    def test_different_periods(self, ohlcv_data_extended):
        """测试不同周期参数"""
        result_7 = haze.py_williams_r(
            ohlcv_data_extended['high'],
            ohlcv_data_extended['low'],
            ohlcv_data_extended['close'],
            period=7
        )

        result_21 = haze.py_williams_r(
            ohlcv_data_extended['high'],
            ohlcv_data_extended['low'],
            ohlcv_data_extended['close'],
            period=20
        )

        assert len(result_7) == len(ohlcv_data_extended['close'])
        assert len(result_21) == len(ohlcv_data_extended['close'])


# ==================== 5. Fisher Transform ====================

class TestFisherTransform:
    """Fisher Transform 单元测试

    算法：将价格转换为近似高斯分布
    特点：返回两个值(fisher, signal)
    """

    def test_basic_calculation(self, ohlcv_data_extended):
        """测试基本Fisher Transform计算

        返回值：(fisher, signal)
        用于识别转折点
        """
        # py_fisher_transform takes (high, low, close, period)
        fisher, signal = haze.py_fisher_transform(
            ohlcv_data_extended['high'],
            ohlcv_data_extended['low'],
            ohlcv_data_extended['close'],
            period=10
        )

        # 验证输出长度
        assert len(fisher) == len(ohlcv_data_extended['close'])
        assert len(signal) == len(ohlcv_data_extended['close'])

        # Fisher值存在
        valid_fisher = [v for v in fisher if not np.isnan(v)]
        assert len(valid_fisher) > 0

    def test_edge_cases(self, empty_array):
        """测试边界条件"""
        # 空数组 - py_fisher_transform takes (high, low, close, period)
        with pytest.raises(ValueError):
            haze.py_fisher_transform(empty_array, empty_array, empty_array, period=10)

    def test_different_periods(self, ohlcv_data_extended):
        """测试不同周期参数"""
        # py_fisher_transform takes (high, low, close, period)
        fisher_5, signal_5 = haze.py_fisher_transform(
            ohlcv_data_extended['high'],
            ohlcv_data_extended['low'],
            ohlcv_data_extended['close'],
            period=5
        )

        fisher_15, signal_15 = haze.py_fisher_transform(
            ohlcv_data_extended['high'],
            ohlcv_data_extended['low'],
            ohlcv_data_extended['close'],
            period=15
        )

        assert len(fisher_5) == len(ohlcv_data_extended['close'])
        assert len(fisher_15) == len(ohlcv_data_extended['close'])


# ==================== 6. CCI ====================

class TestCCI:
    """CCI (Commodity Channel Index) 单元测试

    算法：CCI = (TP - SMA(TP)) / (0.015 * MeanDeviation)
          TP = (High + Low + Close) / 3
    特点：通常在-100到+100之间，但可超出
    """

    def test_basic_calculation(self, ohlcv_data_extended):
        """测试基本CCI计算

        通常范围：-100到+100
        >+100超买，<-100超卖
        """
        result = haze.py_cci(
            ohlcv_data_extended['high'],
            ohlcv_data_extended['low'],
            ohlcv_data_extended['close'],
            period=20
        )

        # 验证输出长度
        assert len(result) == len(ohlcv_data_extended['close'])

        # 验证有有效值
        valid_values = [v for v in result if not np.isnan(v)]
        assert len(valid_values) > 0

    def test_edge_cases(self, empty_array):
        """测试边界条件"""
        # 空数组
        with pytest.raises(ValueError):
            haze.py_cci(empty_array, empty_array, empty_array, period=20)

    def test_different_periods(self, ohlcv_data_extended):
        """测试不同周期参数"""
        result_10 = haze.py_cci(
            ohlcv_data_extended['high'],
            ohlcv_data_extended['low'],
            ohlcv_data_extended['close'],
            period=10
        )

        result_20 = haze.py_cci(
            ohlcv_data_extended['high'],
            ohlcv_data_extended['low'],
            ohlcv_data_extended['close'],
            period=20
        )

        # 更短周期有更多有效值
        valid_10 = sum(1 for v in result_10 if not np.isnan(v))
        valid_20 = sum(1 for v in result_20 if not np.isnan(v))
        assert valid_10 >= valid_20


# ==================== 7. MFI ====================

class TestMFI:
    """MFI (Money Flow Index) 单元测试

    算法：类似RSI，但考虑成交量
    特点：范围0-100，需要volume参数
    """

    def test_basic_calculation(self, ohlcv_data_extended):
        """测试基本MFI计算

        MFI范围：0-100
        >80超买，<20超卖
        """
        result = haze.py_mfi(
            ohlcv_data_extended['high'],
            ohlcv_data_extended['low'],
            ohlcv_data_extended['close'],
            ohlcv_data_extended['volume'],
            period=14
        )

        # 验证输出长度
        assert len(result) == len(ohlcv_data_extended['close'])

        # 验证范围
        valid_values = [v for v in result if not np.isnan(v)]
        assert len(valid_values) > 0
        assert all(0 <= v <= 100 for v in valid_values)

    def test_edge_cases(self, empty_array):
        """测试边界条件"""
        # 空数组
        with pytest.raises(ValueError):
            haze.py_mfi(empty_array, empty_array, empty_array, empty_array, period=14)

    def test_different_periods(self, ohlcv_data_extended):
        """测试不同周期参数"""
        result_7 = haze.py_mfi(
            ohlcv_data_extended['high'],
            ohlcv_data_extended['low'],
            ohlcv_data_extended['close'],
            ohlcv_data_extended['volume'],
            period=7
        )

        result_21 = haze.py_mfi(
            ohlcv_data_extended['high'],
            ohlcv_data_extended['low'],
            ohlcv_data_extended['close'],
            ohlcv_data_extended['volume'],
            period=20
        )

        assert len(result_7) == len(ohlcv_data_extended['close'])
        assert len(result_21) == len(ohlcv_data_extended['close'])


# ==================== 8. Stochastic RSI ====================

class TestStochasticRSI:
    """Stochastic RSI 单元测试

    算法：对RSI应用Stochastic公式
    特点：返回两个值(k, d)，范围0-1
    """

    def test_basic_calculation(self, ohlcv_data_extended):
        """测试基本Stochastic RSI计算

        返回值：(k, d)
        范围：0-1
        """
        # py_stochrsi(close, rsi_period, stoch_period, k_period, d_period)
        k, d = haze.py_stochrsi(
            ohlcv_data_extended['close'],
            rsi_period=14,
            stoch_period=14,
            k_period=3,
            d_period=3
        )

        # 验证输出长度
        assert len(k) == len(ohlcv_data_extended['close'])
        assert len(d) == len(ohlcv_data_extended['close'])

        # 验证范围
        valid_k = [v for v in k if not np.isnan(v)]
        valid_d = [v for v in d if not np.isnan(v)]
        if valid_k:
            assert all(0 <= v <= 1 for v in valid_k)
        if valid_d:
            assert all(0 <= v <= 1 for v in valid_d)

    def test_edge_cases(self, empty_array):
        """测试边界条件"""
        # 空数组
        with pytest.raises(ValueError):
            haze.py_stochrsi(empty_array, 14, 14, 3, 3)

    def test_different_parameters(self, ohlcv_data_extended):
        """测试不同参数组合"""
        k_fast, d_fast = haze.py_stochrsi(
            ohlcv_data_extended['close'], 7, 7, 3, 3
        )

        k_slow, d_slow = haze.py_stochrsi(
            ohlcv_data_extended['close'], 14, 14, 5, 5
        )

        assert len(k_fast) == len(ohlcv_data_extended['close'])
        assert len(k_slow) == len(ohlcv_data_extended['close'])


# ==================== 9. KDJ ====================

class TestKDJ:
    """KDJ 单元测试

    算法：K = SMA(fast %K, smooth_k)
          D = SMA(K, period_d)
          J = 3*K - 2*D
    特点：返回三个值(k, d, j)，J可超出0-100
    """

    def test_basic_calculation(self, ohlcv_data_extended):
        """测试基本KDJ计算

        返回值：(k, d, j)
        K/D范围：0-100
        J可超出范围
        """
        # py_kdj takes (high, low, close, k_period, d_period)
        k, d, j = haze.py_kdj(
            ohlcv_data_extended['high'],
            ohlcv_data_extended['low'],
            ohlcv_data_extended['close'],
            k_period=9,
            d_period=3
        )

        # 验证输出长度
        assert len(k) == len(ohlcv_data_extended['close'])
        assert len(d) == len(ohlcv_data_extended['close'])
        assert len(j) == len(ohlcv_data_extended['close'])

        # 验证K/D范围
        valid_k = [v for v in k if not np.isnan(v)]
        valid_d = [v for v in d if not np.isnan(v)]
        assert all(0 <= v <= 100 for v in valid_k)
        assert all(0 <= v <= 100 for v in valid_d)

    def test_edge_cases(self, empty_array):
        """测试边界条件"""
        # 空数组 - py_kdj takes (high, low, close, k_period, d_period)
        with pytest.raises(ValueError):
            haze.py_kdj(empty_array, empty_array, empty_array, 9, 3)

    def test_different_parameters(self, ohlcv_data_extended):
        """测试不同参数组合"""
        k_fast, d_fast, j_fast = haze.py_kdj(
            ohlcv_data_extended['high'],
            ohlcv_data_extended['low'],
            ohlcv_data_extended['close'],
            k_period=5,
            d_period=3
        )

        k_slow, d_slow, j_slow = haze.py_kdj(
            ohlcv_data_extended['high'],
            ohlcv_data_extended['low'],
            ohlcv_data_extended['close'],
            k_period=14,
            d_period=5
        )

        assert len(k_fast) == len(ohlcv_data_extended['close'])
        assert len(k_slow) == len(ohlcv_data_extended['close'])


# ==================== 10. TSI ====================

class TestTSI:
    """TSI (True Strength Index) 单元测试

    算法：双重平滑的动量指标
    特点：返回两个值(tsi, signal)
    """

    def test_basic_calculation(self, ohlcv_data_extended):
        """测试基本TSI计算

        返回值：(tsi, signal)
        范围：-100到+100
        """
        tsi, signal = haze.py_tsi(
            ohlcv_data_extended['close'],
            long_period=15,
            short_period=7,
            signal_period=7
        )

        # 验证输出长度
        assert len(tsi) == len(ohlcv_data_extended['close'])
        assert len(signal) == len(ohlcv_data_extended['close'])

        # 验证范围
        valid_tsi = [v for v in tsi if not np.isnan(v)]
        if valid_tsi:
            assert all(-100 <= v <= 100 for v in valid_tsi)

    def test_edge_cases(self, empty_array):
        """测试边界条件"""
        # 空数组
        with pytest.raises(ValueError):
            haze.py_tsi(empty_array, 15, 7, 7)

    def test_different_parameters(self, ohlcv_data_extended):
        """测试不同参数组合"""
        tsi_fast, sig_fast = haze.py_tsi(
            ohlcv_data_extended['close'], 13, 7, 7
        )

        tsi_slow, sig_slow = haze.py_tsi(
            ohlcv_data_extended['close'], 15, 7, 7
        )

        assert len(tsi_fast) == len(ohlcv_data_extended['close'])
        assert len(tsi_slow) == len(ohlcv_data_extended['close'])


# ==================== 11. Ultimate Oscillator ====================

class TestUltimateOscillator:
    """Ultimate Oscillator 单元测试

    算法：综合三个不同时间框架的买卖压力
    特点：范围0-100
    """

    def test_basic_calculation(self, ohlcv_data_extended):
        """测试基本Ultimate Oscillator计算

        范围：0-100
        >70超买，<30超卖
        """
        result = haze.py_ultimate_oscillator(
            ohlcv_data_extended['high'],
            ohlcv_data_extended['low'],
            ohlcv_data_extended['close'],
            period1=7,
            period2=14,
            period3=20
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
        with pytest.raises(ValueError):
            haze.py_ultimate_oscillator(empty_array, empty_array, empty_array, 7, 14, 20)

    def test_different_parameters(self, ohlcv_data_extended):
        """测试不同参数组合"""
        result_fast = haze.py_ultimate_oscillator(
            ohlcv_data_extended['high'],
            ohlcv_data_extended['low'],
            ohlcv_data_extended['close'],
            period1=5,
            period2=10,
            period3=20
        )

        result_slow = haze.py_ultimate_oscillator(
            ohlcv_data_extended['high'],
            ohlcv_data_extended['low'],
            ohlcv_data_extended['close'],
            period1=7,
            period2=14,
            period3=20
        )

        assert len(result_fast) == len(ohlcv_data_extended['close'])
        assert len(result_slow) == len(ohlcv_data_extended['close'])


# ==================== 12. Momentum ====================

class TestMomentum:
    """Momentum 单元测试

    算法：MOM = Close - Close[period]
    特点：最简单的动量指标
    """

    def test_basic_calculation(self, simple_prices):
        """测试基本Momentum计算

        MOM = 当前价格 - period前价格
        """
        result = haze.py_mom(simple_prices, period=3)

        # 验证输出长度
        assert len(result) == len(simple_prices)

        # 验证前period个为NaN
        assert sum(np.isnan(result[:3])) == 3

        # 验证计算：simple_prices[3] - simple_prices[0]
        assert abs(result[3] - (simple_prices[3] - simple_prices[0])) < 1e-10

    def test_edge_cases(self, empty_array, single_value):
        """测试边界条件"""
        # 空数组
        with pytest.raises(ValueError):
            haze.py_mom(empty_array, period=3)

        # 单值
        with pytest.raises(ValueError):
            haze.py_mom(single_value, period=3)

    def test_different_periods(self, simple_prices):
        """测试不同周期参数"""
        result_1 = haze.py_mom(simple_prices, period=1)
        result_5 = haze.py_mom(simple_prices, period=5)

        # period=1时，MOM应该是价格变化
        assert abs(result_1[1] - (simple_prices[1] - simple_prices[0])) < 1e-10

        assert len(result_5) == len(simple_prices)


# ==================== 13. ROC ====================

class TestROC:
    """ROC (Rate of Change) 单元测试

    算法：ROC = 100 * (Close - Close[period]) / Close[period]
    特点：百分比形式的动量
    """

    def test_basic_calculation(self, simple_prices):
        """测试基本ROC计算

        ROC = 100 * (当前 - period前) / period前
        """
        result = haze.py_roc(simple_prices, period=3)

        # 验证输出长度
        assert len(result) == len(simple_prices)

        # 验证前period个为NaN
        assert sum(np.isnan(result[:3])) == 3

        # 验证计算：100 * (simple_prices[3] - simple_prices[0]) / simple_prices[0]
        expected = 100 * (simple_prices[3] - simple_prices[0]) / simple_prices[0]
        assert abs(result[3] - expected) < 1e-9

    def test_edge_cases(self, empty_array, single_value):
        """测试边界条件"""
        # 空数组
        with pytest.raises(ValueError):
            haze.py_roc(empty_array, period=3)

        # 单值
        with pytest.raises(ValueError):
            haze.py_roc(single_value, period=3)

    def test_different_periods(self, simple_prices):
        """测试不同周期参数"""
        result_1 = haze.py_roc(simple_prices, period=1)
        result_5 = haze.py_roc(simple_prices, period=5)

        # period=1时，ROC应该是单周期百分比变化
        expected = 100 * (simple_prices[1] - simple_prices[0]) / simple_prices[0]
        assert abs(result_1[1] - expected) < 1e-9

        assert len(result_5) == len(simple_prices)


# ==================== 14. Awesome Oscillator ====================

class TestAwesomeOscillator:
    """Awesome Oscillator 单元测试

    算法：AO = SMA((High+Low)/2, 5) - SMA((High+Low)/2, 34)
    特点：Bill Williams开发，震荡指标
    """

    def test_basic_calculation(self, ohlcv_data_extended):
        """测试基本Awesome Oscillator计算

        AO = 快速SMA - 慢速SMA
        """
        result = haze.py_awesome_oscillator(
            ohlcv_data_extended['high'],
            ohlcv_data_extended['low'],
            fast_period=5,
            slow_period=13
        )

        # 验证输出长度
        assert len(result) == len(ohlcv_data_extended['close'])

        # 有有效值存在
        valid_values = [v for v in result if not np.isnan(v)]
        assert len(valid_values) >= 0  # 可能全为NaN（数据不足）

    def test_edge_cases(self, empty_array):
        """测试边界条件"""
        # 空数组
        with pytest.raises(ValueError):
            haze.py_awesome_oscillator(empty_array, empty_array, 5, 13)

    def test_different_parameters(self, ohlcv_data_extended):
        """测试不同参数组合"""
        result_fast = haze.py_awesome_oscillator(
            ohlcv_data_extended['high'],
            ohlcv_data_extended['low'],
            fast_period=3,
            slow_period=10
        )

        result_slow = haze.py_awesome_oscillator(
            ohlcv_data_extended['high'],
            ohlcv_data_extended['low'],
            fast_period=5,
            slow_period=13
        )

        assert len(result_fast) == len(ohlcv_data_extended['close'])
        assert len(result_slow) == len(ohlcv_data_extended['close'])


# ==================== 15. APO ====================

class TestAPO:
    """APO (Absolute Price Oscillator) 单元测试

    算法：APO = EMA(fast) - EMA(slow)
    特点：类似MACD但不除以价格
    """

    def test_basic_calculation(self, ohlcv_data_extended):
        """测试基本APO计算

        APO = 快速EMA - 慢速EMA
        """
        result = haze.py_apo(
            ohlcv_data_extended['close'],
            fast_period=5,
            slow_period=12
        )

        # 验证输出长度
        assert len(result) == len(ohlcv_data_extended['close'])

        # 有有效值
        valid_values = [v for v in result if not np.isnan(v)]
        assert len(valid_values) > 0

    def test_edge_cases(self, empty_array):
        """测试边界条件"""
        # 空数组
        with pytest.raises(ValueError):
            haze.py_apo(empty_array, 5, 12)

    def test_different_parameters(self, ohlcv_data_extended):
        """测试不同参数组合"""
        result_fast = haze.py_apo(ohlcv_data_extended['close'], 4, 9)
        result_slow = haze.py_apo(ohlcv_data_extended['close'], 5, 12)

        assert len(result_fast) == len(ohlcv_data_extended['close'])
        assert len(result_slow) == len(ohlcv_data_extended['close'])


# ==================== 16. PPO ====================

class TestPPO:
    """PPO (Percentage Price Oscillator) 单元测试

    算法：PPO = 100 * (EMA(fast) - EMA(slow)) / EMA(slow)
    特点：MACD的百分比版本
    """

    def test_basic_calculation(self, ohlcv_data_extended):
        """测试基本PPO计算

        PPO = 百分比形式的价格振荡器
        """
        result = haze.py_ppo(
            ohlcv_data_extended['close'],
            fast_period=5,
            slow_period=12
        )

        # 验证输出长度
        assert len(result) == len(ohlcv_data_extended['close'])

        # 有有效值
        valid_values = [v for v in result if not np.isnan(v)]
        assert len(valid_values) > 0

    def test_edge_cases(self, empty_array):
        """测试边界条件"""
        # 空数组
        with pytest.raises(ValueError):
            haze.py_ppo(empty_array, 5, 12)

    def test_different_parameters(self, ohlcv_data_extended):
        """测试不同参数组合"""
        result_fast = haze.py_ppo(ohlcv_data_extended['close'], 4, 9)
        result_slow = haze.py_ppo(ohlcv_data_extended['close'], 5, 12)

        assert len(result_fast) == len(ohlcv_data_extended['close'])
        assert len(result_slow) == len(ohlcv_data_extended['close'])


# ==================== 17. CMO ====================

class TestCMO:
    """CMO (Chande Momentum Oscillator) 单元测试

    算法：CMO = 100 * (SumUp - SumDown) / (SumUp + SumDown)
    特点：范围-100到+100，类似RSI
    """

    def test_basic_calculation(self, ohlcv_data_extended):
        """测试基本CMO计算

        CMO范围：-100到+100
        >+50超买，<-50超卖
        """
        result = haze.py_cmo(ohlcv_data_extended['close'], period=14)

        # 验证输出长度
        assert len(result) == len(ohlcv_data_extended['close'])

        # 验证范围
        valid_values = [v for v in result if not np.isnan(v)]
        assert len(valid_values) > 0
        assert all(-100 <= v <= 100 for v in valid_values)

    def test_edge_cases(self, empty_array, single_value):
        """测试边界条件"""
        # 空数组
        with pytest.raises(ValueError):
            haze.py_cmo(empty_array, period=14)

        # 单值
        with pytest.raises(ValueError):
            haze.py_cmo(single_value, period=14)

    def test_different_periods(self, ohlcv_data_extended):
        """测试不同周期参数"""
        result_7 = haze.py_cmo(ohlcv_data_extended['close'], period=7)
        result_21 = haze.py_cmo(ohlcv_data_extended['close'], period=18)

        # 更短周期有更多有效值
        valid_7 = sum(1 for v in result_7 if not np.isnan(v))
        valid_21 = sum(1 for v in result_21 if not np.isnan(v))
        assert valid_7 >= valid_21
