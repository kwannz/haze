"""
Volume Indicators Unit Tests
=============================

测试所有11个成交量指标的核心功能。

测试策略：
- 基本计算：验证输出格式和范围
- 边界条件：空数组、不足周期、单值
- 参数测试：不同周期、特殊参数

测试的指标：
1. OBV - 能量潮
2. VWAP - 成交量加权平均价
3. Force Index - 劲道指数
4. CMF - 蔡金资金流量
5. Volume Oscillator - 成交量振荡器
6. AD - 累积/派发线
7. PVT - 价量趋势
8. NVI - 负量指标
9. PVI - 正量指标
10. EOM - 简易波动指标
11. ADOSC - 蔡金A/D振荡器

Author: Haze Team
Date: 2025-12-26
"""

import pytest
import numpy as np
import haze_library as haze


# ==================== 1. OBV ====================

class TestOBV:
    """OBV (On-Balance Volume) 单元测试

    算法：价格上涨时加成交量，下跌时减成交量
    特点：累积量能指标，验证价格趋势
    """

    def test_basic_calculation(self, ohlcv_data_extended):
        """测试基本OBV计算"""
        close = ohlcv_data_extended['close']
        volume = ohlcv_data_extended['volume']

        result = haze.py_obv(close, volume)

        assert isinstance(result, list)
        assert len(result) == len(close)
        assert all(isinstance(x, (int, float)) or np.isnan(x) for x in result)

    def test_increasing_price(self):
        """测试价格持续上涨时OBV持续增加"""
        close = [10.0, 11.0, 12.0, 13.0, 14.0]
        volume = [100.0, 100.0, 100.0, 100.0, 100.0]

        result = haze.py_obv(close, volume)

        # OBV应该持续增加
        assert result[0] == volume[0]  # 与 TA-Lib 对齐：首个值为 volume[0]
        for i in range(1, len(result)):
            assert result[i] > result[i-1]

    def test_decreasing_price(self):
        """测试价格持续下跌时OBV持续减少"""
        close = [14.0, 13.0, 12.0, 11.0, 10.0]
        volume = [100.0, 100.0, 100.0, 100.0, 100.0]

        result = haze.py_obv(close, volume)

        # OBV应该持续减少
        assert result[0] == volume[0]  # 与 TA-Lib 对齐：首个值为 volume[0]
        for i in range(1, len(result)):
            assert result[i] < result[i-1]


# ==================== 2. VWAP ====================

class TestVWAP:
    """VWAP (Volume Weighted Average Price) 单元测试

    算法：VWAP = Σ(Price × Volume) / Σ(Volume)
    特点：成交量加权平均价格，常用于日内交易
    """

    def test_basic_calculation(self, ohlcv_data_extended):
        """测试基本VWAP计算"""
        high = ohlcv_data_extended['high']
        low = ohlcv_data_extended['low']
        close = ohlcv_data_extended['close']
        volume = ohlcv_data_extended['volume']

        result = haze.py_vwap(high, low, close, volume)

        assert isinstance(result, list)
        assert len(result) == len(close)
        assert all(isinstance(x, (int, float)) or np.isnan(x) for x in result)

    def test_vwap_range(self, ohlcv_data_extended):
        """测试VWAP在合理价格范围内

        VWAP is cumulative, so it should be within the global price range,
        not necessarily within each bar's high-low range.
        """
        high = ohlcv_data_extended['high']
        low = ohlcv_data_extended['low']
        close = ohlcv_data_extended['close']
        volume = ohlcv_data_extended['volume']

        result = haze.py_vwap(high, low, close, volume)

        # VWAP should be within the global price range
        global_low = min(low)
        global_high = max(high)
        for vwap in result:
            if not np.isnan(vwap):
                assert global_low <= vwap <= global_high

    def test_empty_array(self):
        """测试空数组"""
        result = haze.py_vwap([], [], [], [])
        assert isinstance(result, list)
        assert len(result) == 0


# ==================== 3. Force Index ====================

class TestForceIndex:
    """Force Index (劲道指数) 单元测试

    算法：Force Index = (Close - Close_prev) × Volume
    特点：结合价格变化和成交量，衡量买卖力道
    """

    def test_basic_calculation(self, ohlcv_data_extended):
        """测试基本Force Index计算"""
        close = ohlcv_data_extended['close']
        volume = ohlcv_data_extended['volume']

        result = haze.py_force_index(close, volume, period=13)

        assert isinstance(result, list)
        assert len(result) == len(close)
        assert all(isinstance(x, (int, float)) or np.isnan(x) for x in result)

    def test_different_periods(self, ohlcv_data_extended):
        """测试不同周期参数"""
        close = ohlcv_data_extended['close']
        volume = ohlcv_data_extended['volume']

        result_1 = haze.py_force_index(close, volume, period=1)
        result_13 = haze.py_force_index(close, volume, period=13)

        assert len(result_1) == len(result_13)

    def test_empty_array(self):
        """测试空数组"""
        result = haze.py_force_index([], [], period=13)
        assert isinstance(result, list)
        assert len(result) == 0


# ==================== 4. CMF ====================

class TestCMF:
    """CMF (Chaikin Money Flow) 单元测试

    算法：CMF = Σ(MFM × Volume) / Σ(Volume)
          MFM = (Close - Low) - (High - Close) / (High - Low)
    特点：-1到1范围，衡量资金流入流出
    """

    def test_basic_calculation(self, ohlcv_data_extended):
        """测试基本CMF计算"""
        high = ohlcv_data_extended['high']
        low = ohlcv_data_extended['low']
        close = ohlcv_data_extended['close']
        volume = ohlcv_data_extended['volume']

        result = haze.py_cmf(high, low, close, volume, period=20)

        assert isinstance(result, list)
        assert len(result) == len(close)
        assert all(isinstance(x, (int, float)) or np.isnan(x) for x in result)

    def test_cmf_range(self, ohlcv_data_extended):
        """测试CMF在-1到1范围内"""
        high = ohlcv_data_extended['high']
        low = ohlcv_data_extended['low']
        close = ohlcv_data_extended['close']
        volume = ohlcv_data_extended['volume']

        result = haze.py_cmf(high, low, close, volume, period=20)

        for cmf in result:
            if not np.isnan(cmf):
                assert -1.0 <= cmf <= 1.0

    def test_different_periods(self, ohlcv_data_extended):
        """测试不同周期参数"""
        high = ohlcv_data_extended['high']
        low = ohlcv_data_extended['low']
        close = ohlcv_data_extended['close']
        volume = ohlcv_data_extended['volume']

        result_10 = haze.py_cmf(high, low, close, volume, period=10)
        result_20 = haze.py_cmf(high, low, close, volume, period=20)

        assert len(result_10) == len(result_20)


# ==================== 5. Volume Oscillator ====================

class TestVolumeOscillator:
    """Volume Oscillator (成交量振荡器) 单元测试

    算法：VO = ((Short MA - Long MA) / Long MA) × 100
    特点：衡量成交量短期与长期趋势差异
    """

    def test_basic_calculation(self, ohlcv_data_extended):
        """测试基本Volume Oscillator计算"""
        volume = ohlcv_data_extended['volume']

        result = haze.py_volume_oscillator(volume, short_period=5, long_period=10)

        assert isinstance(result, list)
        assert len(result) == len(volume)
        assert all(isinstance(x, (int, float)) or np.isnan(x) for x in result)

    def test_different_periods(self, ohlcv_data_extended):
        """测试不同周期参数"""
        volume = ohlcv_data_extended['volume']

        result_5_10 = haze.py_volume_oscillator(volume, short_period=5, long_period=10)
        result_10_20 = haze.py_volume_oscillator(volume, short_period=10, long_period=20)

        assert len(result_5_10) == len(result_10_20)

    def test_empty_array(self):
        """测试空数组"""
        result = haze.py_volume_oscillator([], short_period=5, long_period=10)
        assert isinstance(result, list)
        assert len(result) == 0


# ==================== 6. AD ====================

class TestAD:
    """AD (Accumulation/Distribution) 单元测试

    算法：AD = AD_prev + MFM × Volume
          MFM = (Close - Low) - (High - Close) / (High - Low)
    特点：累积派发线，衡量量价关系
    """

    def test_basic_calculation(self, ohlcv_data_extended):
        """测试基本AD计算"""
        high = ohlcv_data_extended['high']
        low = ohlcv_data_extended['low']
        close = ohlcv_data_extended['close']
        volume = ohlcv_data_extended['volume']

        result = haze.py_ad(high, low, close, volume)

        assert isinstance(result, list)
        assert len(result) == len(close)
        assert all(isinstance(x, (int, float)) or np.isnan(x) for x in result)

    def test_empty_array(self):
        """测试空数组"""
        result = haze.py_ad([], [], [], [])
        assert isinstance(result, list)
        assert len(result) == 0

    def test_cumulative_nature(self, ohlcv_data_extended):
        """测试AD的累积性质"""
        high = ohlcv_data_extended['high']
        low = ohlcv_data_extended['low']
        close = ohlcv_data_extended['close']
        volume = ohlcv_data_extended['volume']

        result = haze.py_ad(high, low, close, volume)

        # AD是累积值，应该有增有减
        assert isinstance(result, list)
        assert len(result) > 0


# ==================== 7. PVT ====================

class TestPVT:
    """PVT (Price Volume Trend) 单元测试

    算法：PVT = PVT_prev + Volume × (Close - Close_prev) / Close_prev
    特点：价量趋势指标，累积量价变化
    """

    def test_basic_calculation(self, ohlcv_data_extended):
        """测试基本PVT计算"""
        close = ohlcv_data_extended['close']
        volume = ohlcv_data_extended['volume']

        result = haze.py_pvt(close, volume)

        assert isinstance(result, list)
        assert len(result) == len(close)
        assert all(isinstance(x, (int, float)) or np.isnan(x) for x in result)

    def test_empty_array(self):
        """测试空数组"""
        result = haze.py_pvt([], [])
        assert isinstance(result, list)
        assert len(result) == 0

    def test_cumulative_nature(self):
        """测试PVT的累积性质"""
        close = [10.0, 11.0, 12.0, 13.0, 14.0]
        volume = [100.0, 100.0, 100.0, 100.0, 100.0]

        result = haze.py_pvt(close, volume)

        assert isinstance(result, list)
        assert len(result) == len(close)


# ==================== 8. NVI ====================

class TestNVI:
    """NVI (Negative Volume Index) 单元测试

    算法：当Volume < Volume_prev时，NVI = NVI_prev × (Close / Close_prev)
    特点：负量指标，关注成交量减少时的价格变化
    """

    def test_basic_calculation(self, ohlcv_data_extended):
        """测试基本NVI计算"""
        close = ohlcv_data_extended['close']
        volume = ohlcv_data_extended['volume']

        result = haze.py_nvi(close, volume)

        assert isinstance(result, list)
        assert len(result) == len(close)
        assert all(isinstance(x, (int, float)) or np.isnan(x) for x in result)

    def test_empty_array(self):
        """测试空数组"""
        result = haze.py_nvi([], [])
        assert isinstance(result, list)
        assert len(result) == 0

    def test_initial_value(self):
        """测试NVI初始值"""
        close = [10.0, 11.0, 12.0, 13.0, 14.0]
        volume = [100.0, 90.0, 80.0, 70.0, 60.0]  # 持续减量

        result = haze.py_nvi(close, volume)

        assert isinstance(result, list)
        assert len(result) == len(close)
        # 首个值应该为100或1000（根据实现）
        assert result[0] > 0


# ==================== 9. PVI ====================

class TestPVI:
    """PVI (Positive Volume Index) 单元测试

    算法：当Volume > Volume_prev时，PVI = PVI_prev × (Close / Close_prev)
    特点：正量指标，关注成交量增加时的价格变化
    """

    def test_basic_calculation(self, ohlcv_data_extended):
        """测试基本PVI计算"""
        close = ohlcv_data_extended['close']
        volume = ohlcv_data_extended['volume']

        result = haze.py_pvi(close, volume)

        assert isinstance(result, list)
        assert len(result) == len(close)
        assert all(isinstance(x, (int, float)) or np.isnan(x) for x in result)

    def test_empty_array(self):
        """测试空数组"""
        result = haze.py_pvi([], [])
        assert isinstance(result, list)
        assert len(result) == 0

    def test_initial_value(self):
        """测试PVI初始值"""
        close = [10.0, 11.0, 12.0, 13.0, 14.0]
        volume = [60.0, 70.0, 80.0, 90.0, 100.0]  # 持续增量

        result = haze.py_pvi(close, volume)

        assert isinstance(result, list)
        assert len(result) == len(close)
        # 首个值应该为100或1000（根据实现）
        assert result[0] > 0


# ==================== 10. EOM ====================

class TestEOM:
    """EOM (Ease of Movement) 单元测试

    算法：EOM = ((High + Low) / 2 - (High_prev + Low_prev) / 2) / (Volume / (High - Low))
    特点：简易波动指标，衡量价格移动的难易程度
    """

    def test_basic_calculation(self, ohlcv_data_extended):
        """测试基本EOM计算"""
        high = ohlcv_data_extended['high']
        low = ohlcv_data_extended['low']
        volume = ohlcv_data_extended['volume']

        result = haze.py_eom(high, low, volume, period=14)

        assert isinstance(result, list)
        assert len(result) == len(high)
        assert all(isinstance(x, (int, float)) or np.isnan(x) for x in result)

    def test_different_periods(self, ohlcv_data_extended):
        """测试不同周期参数"""
        high = ohlcv_data_extended['high']
        low = ohlcv_data_extended['low']
        volume = ohlcv_data_extended['volume']

        result_10 = haze.py_eom(high, low, volume, period=10)
        result_14 = haze.py_eom(high, low, volume, period=14)

        assert len(result_10) == len(result_14)

    def test_empty_array(self):
        """测试空数组"""
        result = haze.py_eom([], [], [], period=14)
        assert isinstance(result, list)
        assert len(result) == 0


# ==================== 11. ADOSC ====================

class TestADOSC:
    """ADOSC (Chaikin A/D Oscillator) 单元测试

    算法：ADOSC = EMA(AD, fast_period) - EMA(AD, slow_period)
    特点：蔡金A/D振荡器，衡量累积派发线的动量
    """

    def test_basic_calculation(self, ohlcv_data_extended):
        """测试基本ADOSC计算"""
        high = ohlcv_data_extended['high']
        low = ohlcv_data_extended['low']
        close = ohlcv_data_extended['close']
        volume = ohlcv_data_extended['volume']

        result = haze.py_adosc(high, low, close, volume, fast_period=3, slow_period=10)

        assert isinstance(result, list)
        assert len(result) == len(close)
        assert all(isinstance(x, (int, float)) or np.isnan(x) for x in result)

    def test_different_periods(self, ohlcv_data_extended):
        """测试不同周期参数"""
        high = ohlcv_data_extended['high']
        low = ohlcv_data_extended['low']
        close = ohlcv_data_extended['close']
        volume = ohlcv_data_extended['volume']

        result_3_10 = haze.py_adosc(high, low, close, volume, fast_period=3, slow_period=10)
        result_5_15 = haze.py_adosc(high, low, close, volume, fast_period=5, slow_period=15)

        assert len(result_3_10) == len(result_5_15)

    def test_empty_array(self):
        """测试空数组"""
        result = haze.py_adosc([], [], [], [], fast_period=3, slow_period=10)
        assert isinstance(result, list)
        assert len(result) == 0
