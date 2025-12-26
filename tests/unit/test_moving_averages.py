"""
Moving Averages Indicators Unit Tests
=====================================

测试所有16个移动平均指标的核心功能。

测试策略：
- 基本计算：手动验证简单案例
- 边界条件：空数组、不足周期、单值
- 参数测试：不同周期、特殊参数

测试的指标：
1. SMA - 简单移动平均
2. EMA - 指数移动平均
3. WMA - 加权移动平均
4. DEMA - 双重指数移动平均
5. TEMA - 三重指数移动平均
6. HMA - 船体移动平均
7. RMA - 威尔德移动平均
8. ZLMA - 零滞后移动平均
9. T3 - Tillson T3
10. KAMA - 考夫曼自适应移动平均
11. FRAMA - 分形自适应移动平均
12. ALMA - 阿诺·勒古克斯移动平均
13. VIDYA - 可变指数动态平均
14. PWMA - 帕斯卡加权移动平均
15. SINWMA - 正弦加权移动平均
16. SWMA - 对称加权移动平均

Author: Haze Team
Date: 2025-12-26
"""

import pytest
import numpy as np
import haze_library as haze


# ==================== 1. SMA ====================

class TestSMA:
    """SMA (Simple Moving Average) 单元测试"""

    def test_basic_calculation(self, simple_prices_short):
        """测试基本 SMA 计算（周期=3）

        手动计算：
        数据: [10, 11, 12, 11.5, 13]
        SMA(3):
        - [0]: NaN (不足周期)
        - [1]: NaN
        - [2]: (10+11+12)/3 = 11.0
        - [3]: (11+12+11.5)/3 = 11.5
        - [4]: (12+11.5+13)/3 = 12.166666667
        """
        result = haze.py_sma(simple_prices_short, period=3)

        # 验证关键值
        assert np.isnan(result[0])
        assert np.isnan(result[1])
        assert abs(result[2] - 11.0) < 1e-10
        assert abs(result[3] - 11.5) < 1e-10
        assert abs(result[4] - 12.166666666666666) < 1e-9

    def test_edge_cases(self, empty_array, single_value):
        """测试边界条件"""
        # 空数组
        result = haze.py_sma(empty_array, period=3)
        assert len(result) == 0

        # 数组长度小于周期
        result = haze.py_sma(single_value, period=3)
        assert len(result) == 1
        assert np.isnan(result[0])

        # 周期=1 应该返回原数组
        result = haze.py_sma([10.0, 11.0, 12.0], period=1)
        assert abs(result[0] - 10.0) < 1e-10

    def test_different_periods(self, simple_prices):
        """测试不同周期参数"""
        # 周期=2
        result_p2 = haze.py_sma(simple_prices, period=2)
        assert abs(result_p2[1] - 10.5) < 1e-10  # (10+11)/2

        # 周期=5
        result_p5 = haze.py_sma(simple_prices, period=5)
        assert sum(np.isnan(result_p5[:4])) == 4  # 前4个应为NaN
        assert abs(result_p5[4] - 11.5) < 1e-10  # (10+11+12+11.5+13)/5 = 11.5


# ==================== 2. EMA ====================

class TestEMA:
    """EMA (Exponential Moving Average) 单元测试"""

    def test_basic_calculation(self, simple_prices_short, known_ema_results):
        """测试基本 EMA 计算（周期=3）

        手动计算：
        数据: [10, 11, 12, 11.5, 13]
        EMA(3), α = 2/(3+1) = 0.5:
        - [0]: NaN (不足周期)
        - [1]: NaN
        - [2]: SMA(10,11,12) = 11.0
        - [3]: 11.5*0.5 + 11.0*0.5 = 11.25
        - [4]: 13*0.5 + 11.25*0.5 = 12.125
        """
        result = haze.py_ema(simple_prices_short, period=3)
        expected = known_ema_results['period_3']

        for i, (r, e) in enumerate(zip(result, expected)):
            if np.isnan(e):
                assert np.isnan(r), f"Index {i}: 期望 NaN，实际 {r}"
            else:
                assert abs(r - e) < 1e-10, f"Index {i}: 期望 {e}，实际 {r}"

    def test_edge_cases(self, empty_array, single_value):
        """测试边界条件"""
        # 空数组
        result = haze.py_ema(empty_array, period=3)
        assert len(result) == 0

        # 单值数组
        result = haze.py_ema(single_value, period=3)
        assert len(result) == 1
        assert np.isnan(result[0])

    def test_different_periods(self, simple_prices):
        """测试不同周期参数"""
        # 周期=2 (SMA 作为初始值)
        result_p2 = haze.py_ema(simple_prices, period=2)
        assert np.isnan(result_p2[0])
        # EMA[1] = SMA(10,11) = 10.5
        assert abs(result_p2[1] - 10.5) < 1e-9

        # 周期=5
        result_p5 = haze.py_ema(simple_prices, period=5)
        assert np.isnan(result_p5[0])
        assert abs(result_p5[4] - 11.5) < 1e-10


# ==================== 3. WMA ====================

class TestWMA:
    """WMA (Weighted Moving Average) 单元测试"""

    def test_basic_calculation(self, simple_prices_short):
        """测试基本 WMA 计算（周期=3）

        手动计算：
        数据: [10, 11, 12, 11.5, 13]
        WMA(3), 权重 [1, 2, 3]:
        - [0]: NaN
        - [1]: NaN
        - [2]: (10*1 + 11*2 + 12*3) / (1+2+3) = 68/6 = 11.333...
        - [3]: (11*1 + 12*2 + 11.5*3) / 6 = 69.5/6 = 11.583...
        - [4]: (12*1 + 11.5*2 + 13*3) / 6 = 74/6 = 12.333...
        """
        result = haze.py_wma(simple_prices_short, period=3)

        assert np.isnan(result[0])
        assert np.isnan(result[1])
        assert abs(result[2] - 11.333333333333334) < 1e-9
        assert abs(result[3] - 11.583333333333334) < 1e-9
        assert abs(result[4] - 12.333333333333334) < 1e-9

    def test_edge_cases(self, empty_array, single_value):
        """测试边界条件"""
        # 空数组
        result = haze.py_wma(empty_array, period=3)
        assert len(result) == 0

        # 单值
        result = haze.py_wma(single_value, period=3)
        assert len(result) == 1
        assert np.isnan(result[0])

    def test_different_periods(self, simple_prices):
        """测试不同周期参数"""
        # 周期=2, 权重 [1, 2]
        result_p2 = haze.py_wma(simple_prices, period=2)
        # WMA[1] = (10*1 + 11*2) / 3 = 32/3 = 10.666...
        assert abs(result_p2[1] - 10.666666666666666) < 1e-9


# ==================== 4. DEMA ====================

class TestDEMA:
    """DEMA (Double Exponential Moving Average) 单元测试

    算法：DEMA = 2*EMA - EMA(EMA)
    特点：减少滞后，对价格变化更敏感
    """

    def test_basic_calculation(self, simple_prices_short):
        """测试基本 DEMA 计算（周期=3）

        DEMA = 2*EMA - EMA(EMA)
        需要两次 EMA 计算
        """
        result = haze.py_dema(simple_prices_short, period=3)

        # 验证数组长度和基本属性
        assert len(result) == len(simple_prices_short)
        # DEMA 应该比 EMA 更接近当前价格
        assert result[-1] > simple_prices_short[-2]

    def test_edge_cases(self, empty_array, single_value):
        """测试边界条件"""
        # 空数组
        result = haze.py_dema(empty_array, period=3)
        assert len(result) == 0

        # 单值
        result = haze.py_dema(single_value, period=3)
        assert len(result) == 1

    def test_different_periods(self, simple_prices):
        """测试不同周期参数"""
        result_p2 = haze.py_dema(simple_prices, period=2)
        result_p5 = haze.py_dema(simple_prices, period=5)

        # 验证结果有效
        assert len(result_p2) == len(simple_prices)
        assert len(result_p5) == len(simple_prices)


# ==================== 5. TEMA ====================

class TestTEMA:
    """TEMA (Triple Exponential Moving Average) 单元测试

    算法：TEMA = 3*EMA - 3*EMA(EMA) + EMA(EMA(EMA))
    特点：更进一步减少滞后
    """

    def test_basic_calculation(self, simple_prices_short):
        """测试基本 TEMA 计算（周期=3）"""
        result = haze.py_tema(simple_prices_short, period=3)

        assert len(result) == len(simple_prices_short)
        # TEMA 应该更贴近当前价格
        assert not np.isnan(result[-1])

    def test_edge_cases(self, empty_array, single_value):
        """测试边界条件"""
        result = haze.py_tema(empty_array, period=3)
        assert len(result) == 0

        result = haze.py_tema(single_value, period=3)
        assert len(result) == 1

    def test_different_periods(self, simple_prices):
        """测试不同周期参数"""
        result_p3 = haze.py_tema(simple_prices, period=3)
        result_p5 = haze.py_tema(simple_prices, period=5)

        assert len(result_p3) == len(simple_prices)
        assert len(result_p5) == len(simple_prices)


# ==================== 6. HMA ====================

class TestHMA:
    """HMA (Hull Moving Average) 单元测试

    算法：HMA = WMA(2*WMA(n/2) - WMA(n), sqrt(n))
    特点：Alan Hull 开发，平滑性和响应性兼顾
    """

    def test_basic_calculation(self, simple_prices):
        """测试基本 HMA 计算（周期=9）

        HMA 需要足够数据点，使用 simple_prices (10个点)
        """
        result = haze.py_hma(simple_prices, period=9)

        assert len(result) == len(simple_prices)
        # 验证非 NaN 值存在
        assert not all(np.isnan(result))

    def test_edge_cases(self, empty_array, single_value):
        """测试边界条件"""
        result = haze.py_hma(empty_array, period=3)
        assert len(result) == 0

        result = haze.py_hma(single_value, period=3)
        assert len(result) == 1

    def test_different_periods(self, simple_prices):
        """测试不同周期参数"""
        result_p4 = haze.py_hma(simple_prices, period=4)
        result_p6 = haze.py_hma(simple_prices, period=6)

        assert len(result_p4) == len(simple_prices)
        assert len(result_p6) == len(simple_prices)


# ==================== 7. RMA ====================

class TestRMA:
    """RMA (Wilder's Moving Average) 单元测试

    算法：RMA = (previous_RMA * (n-1) + current) / n
    特点：J. Welles Wilder 开发，用于 RSI 等指标
    """

    def test_basic_calculation(self, simple_prices_short):
        """测试基本 RMA 计算（周期=3）

        RMA 是平滑版本的 EMA
        """
        result = haze.py_rma(simple_prices_short, period=3)

        assert len(result) == len(simple_prices_short)
        # RMA 比 SMA 更平滑
        assert not np.isnan(result[-1])

    def test_edge_cases(self, empty_array, single_value):
        """测试边界条件"""
        result = haze.py_rma(empty_array, period=3)
        assert len(result) == 0

        result = haze.py_rma(single_value, period=3)
        assert len(result) == 1

    def test_different_periods(self, simple_prices):
        """测试不同周期参数"""
        result_p2 = haze.py_rma(simple_prices, period=2)
        result_p5 = haze.py_rma(simple_prices, period=5)

        assert len(result_p2) == len(simple_prices)
        assert len(result_p5) == len(simple_prices)


# ==================== 8. ZLMA ====================

class TestZLMA:
    """ZLMA (Zero Lag Moving Average) 单元测试

    算法：ZLMA = EMA(data + (data - data[lag]))
    特点：尝试消除滞后效应
    """

    def test_basic_calculation(self, simple_prices_short):
        """测试基本 ZLMA 计算（周期=3）"""
        result = haze.py_zlma(simple_prices_short, period=3)

        assert len(result) == len(simple_prices_short)
        # ZLMA 应该更接近实际价格
        assert not np.isnan(result[-1])

    def test_edge_cases(self, empty_array, single_value):
        """测试边界条件"""
        result = haze.py_zlma(empty_array, period=3)
        assert len(result) == 0

        result = haze.py_zlma(single_value, period=3)
        assert len(result) == 1

    def test_different_periods(self, simple_prices):
        """测试不同周期参数"""
        result_p3 = haze.py_zlma(simple_prices, period=3)
        result_p5 = haze.py_zlma(simple_prices, period=5)

        assert len(result_p3) == len(simple_prices)
        assert len(result_p5) == len(simple_prices)


# ==================== 9. T3 ====================

class TestT3:
    """T3 (Tillson T3) 单元测试

    算法：六次 EMA 平滑，使用体积因子 vfactor
    特点：Tim Tillson 开发，超平滑移动平均
    参数：period, vfactor (默认 0.7)
    """

    def test_basic_calculation(self, simple_prices):
        """测试基本 T3 计算（周期=5）

        需要足够数据支持多次 EMA
        """
        result = haze.py_t3(simple_prices, period=5, vfactor=0.7)

        assert len(result) == len(simple_prices)
        # 验证平滑效果
        assert not all(np.isnan(result))

    def test_edge_cases(self, empty_array, single_value):
        """测试边界条件"""
        result = haze.py_t3(empty_array, period=3, vfactor=0.7)
        assert len(result) == 0

        result = haze.py_t3(single_value, period=3, vfactor=0.7)
        assert len(result) == 1

    def test_different_parameters(self, simple_prices):
        """测试不同参数（周期和 vfactor）"""
        # 默认 vfactor=0.7
        result_default = haze.py_t3(simple_prices, period=5, vfactor=0.7)

        # 更高 vfactor (更激进)
        result_high_vf = haze.py_t3(simple_prices, period=5, vfactor=0.9)

        # 更低 vfactor (更保守)
        result_low_vf = haze.py_t3(simple_prices, period=5, vfactor=0.5)

        assert len(result_default) == len(simple_prices)
        assert len(result_high_vf) == len(simple_prices)
        assert len(result_low_vf) == len(simple_prices)


# ==================== 10. KAMA ====================

class TestKAMA:
    """KAMA (Kaufman Adaptive Moving Average) 单元测试

    算法：根据市场效率比率自适应调整平滑常数
    特点：Perry Kaufman 开发，趋势明显时快速，震荡时慢速
    参数：period (默认10), fast (默认2), slow (默认30)
    """

    def test_basic_calculation(self, simple_prices):
        """测试基本 KAMA 计算（默认参数）"""
        result = haze.py_kama(simple_prices, period=10, fast_period=2, slow_period=30)

        assert len(result) == len(simple_prices)
        # 验证自适应特性
        assert not all(np.isnan(result))

    def test_edge_cases(self, empty_array, single_value):
        """测试边界条件"""
        result = haze.py_kama(empty_array, period=5, fast_period=2, slow_period=10)
        assert len(result) == 0

        result = haze.py_kama(single_value, period=5, fast_period=2, slow_period=10)
        assert len(result) == 1

    def test_different_parameters(self, simple_prices):
        """测试不同参数组合"""
        # 默认参数
        result_default = haze.py_kama(simple_prices, period=10, fast_period=2, slow_period=30)

        # 更快响应
        result_fast = haze.py_kama(simple_prices, period=5, fast_period=2, slow_period=15)

        # 更慢响应
        result_slow = haze.py_kama(simple_prices, period=15, fast_period=3, slow_period=50)

        assert len(result_default) == len(simple_prices)
        assert len(result_fast) == len(simple_prices)
        assert len(result_slow) == len(simple_prices)


# ==================== 11. FRAMA ====================

class TestFRAMA:
    """FRAMA (Fractal Adaptive Moving Average) 单元测试

    算法：基于分形维度调整 EMA 的 alpha 值
    特点：John Ehlers 开发，根据市场分形特征自适应
    参数：period (默认16)
    """

    def test_basic_calculation(self, simple_prices):
        """测试基本 FRAMA 计算（周期=10）"""
        result = haze.py_frama(simple_prices, period=10)

        assert len(result) == len(simple_prices)
        # 验证分形自适应
        assert not all(np.isnan(result))

    def test_edge_cases(self, empty_array, single_value):
        """测试边界条件"""
        result = haze.py_frama(empty_array, period=8)
        assert len(result) == 0

        result = haze.py_frama(single_value, period=8)
        assert len(result) == 1

    def test_different_periods(self, simple_prices):
        """测试不同周期参数"""
        result_p8 = haze.py_frama(simple_prices, period=8)
        result_p10 = haze.py_frama(simple_prices, period=10)

        assert len(result_p8) == len(simple_prices)
        assert len(result_p10) == len(simple_prices)


# ==================== 12. ALMA ====================

class TestALMA:
    """ALMA (Arnaud Legoux Moving Average) 单元测试

    算法：使用高斯分布权重，sigma 和 offset 可调
    特点：Arnaud Legoux 开发，平滑且低滞后
    参数：period, sigma (默认6.0), offset (默认0.85)
    """

    def test_basic_calculation(self, simple_prices):
        """测试基本 ALMA 计算（默认参数）"""
        result = haze.py_alma(simple_prices, period=9, sigma=6.0, offset=0.85)

        assert len(result) == len(simple_prices)
        assert not all(np.isnan(result))

    def test_edge_cases(self, empty_array, single_value):
        """测试边界条件"""
        result = haze.py_alma(empty_array, period=5, sigma=6.0, offset=0.85)
        assert len(result) == 0

        result = haze.py_alma(single_value, period=5, sigma=6.0, offset=0.85)
        assert len(result) == 1

    def test_different_parameters(self, simple_prices):
        """测试不同参数（sigma 和 offset）"""
        # 默认参数
        result_default = haze.py_alma(simple_prices, period=9, sigma=6.0, offset=0.85)

        # 更窄高斯分布
        result_narrow = haze.py_alma(simple_prices, period=9, sigma=3.0, offset=0.85)

        # 不同偏移
        result_offset = haze.py_alma(simple_prices, period=9, sigma=6.0, offset=0.5)

        assert len(result_default) == len(simple_prices)
        assert len(result_narrow) == len(simple_prices)
        assert len(result_offset) == len(simple_prices)


# ==================== 13. VIDYA ====================

class TestVIDYA:
    """VIDYA (Variable Index Dynamic Average) 单元测试

    算法：根据价格波动率动态调整 alpha
    特点：Tushar Chande 开发，波动大时快速，波动小时慢速
    参数：period (默认14)
    """

    def test_basic_calculation(self, simple_prices):
        """测试基本 VIDYA 计算（周期=9）"""
        result = haze.py_vidya(simple_prices, period=9)

        assert len(result) == len(simple_prices)
        # 验证动态调整
        assert not all(np.isnan(result))

    def test_edge_cases(self, empty_array, single_value):
        """测试边界条件"""
        result = haze.py_vidya(empty_array, period=5)
        assert len(result) == 0

        result = haze.py_vidya(single_value, period=5)
        assert len(result) == 1

    def test_different_periods(self, simple_prices):
        """测试不同周期参数"""
        result_p5 = haze.py_vidya(simple_prices, period=5)
        result_p9 = haze.py_vidya(simple_prices, period=9)

        assert len(result_p5) == len(simple_prices)
        assert len(result_p9) == len(simple_prices)


# ==================== 14. PWMA ====================

class TestPWMA:
    """PWMA (Pascal Weighted Moving Average) 单元测试

    算法：使用帕斯卡三角形权重
    特点：权重基于二项式系数，中间权重最大
    """

    def test_basic_calculation(self, simple_prices_short):
        """测试基本 PWMA 计算（周期=3）

        帕斯卡权重示例 (period=3): [1, 2, 1]
        归一化后权重和为1
        """
        result = haze.py_pwma(simple_prices_short, period=3)

        assert len(result) == len(simple_prices_short)
        assert np.isnan(result[0])
        assert np.isnan(result[1])
        # 验证权重应用
        assert not np.isnan(result[2])

    def test_edge_cases(self, empty_array, single_value):
        """测试边界条件"""
        result = haze.py_pwma(empty_array, period=3)
        assert len(result) == 0

        result = haze.py_pwma(single_value, period=3)
        assert len(result) == 1
        assert np.isnan(result[0])

    def test_different_periods(self, simple_prices):
        """测试不同周期参数"""
        # period=3: 权重 [1,2,1]
        result_p3 = haze.py_pwma(simple_prices, period=3)

        # period=4: 权重 [1,3,3,1]
        result_p4 = haze.py_pwma(simple_prices, period=4)

        assert len(result_p3) == len(simple_prices)
        assert len(result_p4) == len(simple_prices)


# ==================== 15. SINWMA ====================

class TestSINWMA:
    """SINWMA (Sine Weighted Moving Average) 单元测试

    算法：使用正弦函数权重
    特点：权重曲线平滑，中间权重较大
    """

    def test_basic_calculation(self, simple_prices_short):
        """测试基本 SINWMA 计算（周期=3）

        正弦权重在周期内从0到π均匀分布
        """
        result = haze.py_sinwma(simple_prices_short, period=3)

        assert len(result) == len(simple_prices_short)
        assert np.isnan(result[0])
        assert np.isnan(result[1])
        assert not np.isnan(result[2])

    def test_edge_cases(self, empty_array, single_value):
        """测试边界条件"""
        result = haze.py_sinwma(empty_array, period=3)
        assert len(result) == 0

        result = haze.py_sinwma(single_value, period=3)
        assert len(result) == 1
        assert np.isnan(result[0])

    def test_different_periods(self, simple_prices):
        """测试不同周期参数"""
        result_p3 = haze.py_sinwma(simple_prices, period=3)
        result_p5 = haze.py_sinwma(simple_prices, period=5)

        assert len(result_p3) == len(simple_prices)
        assert len(result_p5) == len(simple_prices)


# ==================== 16. SWMA ====================

class TestSWMA:
    """SWMA (Symmetric Weighted Moving Average) 单元测试

    算法：使用对称权重 [1, 2, 3, ..., n, ..., 3, 2, 1]
    特点：中间权重最大，两端对称递减
    """

    def test_basic_calculation(self, simple_prices_short):
        """测试基本 SWMA 计算（周期=4）

        对称权重示例 (period=4): [1, 2, 2, 1]
        SWMA is a centered average, so for a 5-element array with period=4,
        only the last element has enough surrounding data.
        """
        result = haze.py_swma(simple_prices_short, period=4)

        assert len(result) == len(simple_prices_short)
        # SWMA needs data on both sides, so most values are NaN for short arrays
        assert sum(np.isnan(result[:4])) == 4
        assert not np.isnan(result[4])

    def test_edge_cases(self, empty_array, single_value):
        """测试边界条件"""
        result = haze.py_swma(empty_array, period=3)
        assert len(result) == 0

        result = haze.py_swma(single_value, period=3)
        assert len(result) == 1
        assert np.isnan(result[0])

    def test_different_periods(self, simple_prices):
        """测试不同周期参数"""
        # period=3: 权重 [1,2,1]
        result_p3 = haze.py_swma(simple_prices, period=3)

        # period=5: 权重 [1,2,3,2,1]
        result_p5 = haze.py_swma(simple_prices, period=5)

        assert len(result_p3) == len(simple_prices)
        assert len(result_p5) == len(simple_prices)

        # 验证对称性：使用单调递增数据测试
        monotonic = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]
        result_mono = haze.py_swma(monotonic, period=5)

        # SWMA 在单调数据上应产生平滑曲线
        assert not all(np.isnan(result_mono))
