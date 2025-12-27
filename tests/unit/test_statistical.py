"""
Statistical Indicators Unit Tests
==================================

测试所有13个统计指标的核心功能。

测试策略：
- 基本计算：验证输出格式和范围
- 已知结果：使用可验证的数学结果
- 边界条件：空数组、不足周期、单值

测试的指标：
1. Linear Regression - 线性回归
2. Correlation - 相关性
3. Z-Score - Z分数
4. Covariance - 协方差
5. Beta - 贝塔系数
6. Standard Error - 标准误差
7. CORREL - 相关系数（TA-Lib）
8. LINEARREG - 线性回归（TA-Lib）
9. LINEARREG_SLOPE - 线性回归斜率
10. LINEARREG_ANGLE - 线性回归角度
11. LINEARREG_INTERCEPT - 线性回归截距
12. VAR - 方差
13. TSF - 时间序列预测

Author: Haze Team
Date: 2025-12-26
"""

import pytest
import numpy as np
import haze_library as haze


# ==================== 1. Linear Regression ====================

class TestLinearRegression:
    """Linear Regression (线性回归) 单元测试

    算法：y = a + bx，最小二乘法拟合
    特点：预测趋势线，返回拟合值
    """

    def test_basic_calculation(self, simple_prices):
        """测试基本线性回归计算

        Returns: (slope, intercept, r_squared) - 3 lists
        """
        slope, intercept, r_squared = haze.py_linear_regression(simple_prices, period=5)

        assert isinstance(slope, list)
        assert isinstance(intercept, list)
        assert isinstance(r_squared, list)
        assert len(slope) == len(simple_prices)
        assert all(isinstance(x, (int, float)) or np.isnan(x) for x in slope)

    def test_perfect_linear(self):
        """测试完美线性数据"""
        # y = 2x + 1: [1, 3, 5, 7, 9]
        linear_data = [1.0, 3.0, 5.0, 7.0, 9.0]

        slope, intercept, r_squared = haze.py_linear_regression(linear_data, period=5)

        # For perfect linear data, r_squared should be 1.0 (perfect fit)
        assert abs(r_squared[-1] - 1.0) < 0.01

    def test_different_periods(self, simple_prices):
        """测试不同周期参数"""
        slope_3, _, _ = haze.py_linear_regression(simple_prices, period=3)
        slope_5, _, _ = haze.py_linear_regression(simple_prices, period=5)

        assert len(slope_3) == len(slope_5)

    def test_empty_array(self):
        """测试空数组"""
        with pytest.raises(ValueError):
            haze.py_linear_regression([], period=5)


# ==================== 2. Correlation ====================

class TestCorrelation:
    """Correlation (相关性) 单元测试

    算法：Pearson相关系数 r = Cov(X,Y) / (σX × σY)
    特点：-1到1范围，衡量线性相关程度
    """

    def test_basic_calculation(self, simple_prices):
        """测试基本相关性计算"""
        prices_x = simple_prices
        prices_y = [x * 1.1 for x in simple_prices]  # 正相关

        result = haze.py_correlation(prices_x, prices_y, period=5)

        assert isinstance(result, list)
        assert len(result) == len(prices_x)
        assert all(isinstance(x, (int, float)) or np.isnan(x) for x in result)

    def test_perfect_positive_correlation(self):
        """测试完美正相关"""
        x = [1.0, 2.0, 3.0, 4.0, 5.0]
        y = [2.0, 4.0, 6.0, 8.0, 10.0]  # y = 2x

        result = haze.py_correlation(x, y, period=5)

        # 最后一个值应该接近1.0
        assert abs(result[-1] - 1.0) < 0.01

    def test_perfect_negative_correlation(self):
        """测试完美负相关"""
        x = [1.0, 2.0, 3.0, 4.0, 5.0]
        y = [10.0, 8.0, 6.0, 4.0, 2.0]  # y = -2x + 12

        result = haze.py_correlation(x, y, period=5)

        # 最后一个值应该接近-1.0
        assert abs(result[-1] - (-1.0)) < 0.01

    def test_correlation_range(self, simple_prices):
        """测试相关系数在-1到1范围内"""
        prices_x = simple_prices
        prices_y = [x * 0.9 for x in simple_prices]

        result = haze.py_correlation(prices_x, prices_y, period=5)

        for corr in result:
            if not np.isnan(corr):
                assert -1.0 <= corr <= 1.0


# ==================== 3. Z-Score ====================

class TestZScore:
    """Z-Score (Z分数) 单元测试

    算法：z = (x - μ) / σ
    特点：标准化分数，衡量偏离均值的程度
    """

    def test_basic_calculation(self, simple_prices):
        """测试基本Z-Score计算"""
        result = haze.py_zscore(simple_prices, period=5)

        assert isinstance(result, list)
        assert len(result) == len(simple_prices)
        assert all(isinstance(x, (int, float)) or np.isnan(x) for x in result)

    def test_zero_mean_unit_variance(self):
        """测试标准正态分布数据"""
        # 标准正态分布数据
        np.random.seed(42)
        data = np.random.normal(0, 1, 100).tolist()

        result = haze.py_zscore(data, period=20)

        # Z-score应该在合理范围内（大部分在-3到3之间）
        valid_results = [z for z in result if not np.isnan(z)]
        assert len(valid_results) > 0
        assert all(-5 < z < 5 for z in valid_results)  # 允许一些极端值

    def test_different_periods(self, simple_prices):
        """测试不同周期参数"""
        result_3 = haze.py_zscore(simple_prices, period=3)
        result_5 = haze.py_zscore(simple_prices, period=5)

        assert len(result_3) == len(result_5)

    def test_empty_array(self):
        """测试空数组"""
        with pytest.raises(ValueError):
            haze.py_zscore([], period=5)


# ==================== 4. Covariance ====================

class TestCovariance:
    """Covariance (协方差) 单元测试

    算法：Cov(X,Y) = E[(X - μX)(Y - μY)]
    特点：衡量两变量联合变化程度
    """

    def test_basic_calculation(self, simple_prices):
        """测试基本协方差计算"""
        prices_x = simple_prices
        prices_y = [x * 1.1 for x in simple_prices]

        result = haze.py_covariance(prices_x, prices_y, period=5)

        assert isinstance(result, list)
        assert len(result) == len(prices_x)
        assert all(isinstance(x, (int, float)) or np.isnan(x) for x in result)

    def test_positive_covariance(self):
        """测试正协方差"""
        x = [1.0, 2.0, 3.0, 4.0, 5.0]
        y = [2.0, 4.0, 6.0, 8.0, 10.0]  # 正相关

        result = haze.py_covariance(x, y, period=5)

        # 协方差应该为正
        assert result[-1] > 0

    def test_negative_covariance(self):
        """测试负协方差"""
        x = [1.0, 2.0, 3.0, 4.0, 5.0]
        y = [10.0, 8.0, 6.0, 4.0, 2.0]  # 负相关

        result = haze.py_covariance(x, y, period=5)

        # 协方差应该为负
        assert result[-1] < 0

    def test_empty_array(self):
        """测试空数组"""
        with pytest.raises(ValueError):
            haze.py_covariance([], [], period=5)


# ==================== 5. Beta ====================

class TestBeta:
    """Beta (贝塔系数) 单元测试

    算法：β = Cov(Stock, Market) / Var(Market)
    特点：衡量股票相对市场的系统风险
    """

    def test_basic_calculation(self, simple_prices):
        """测试基本Beta计算"""
        stock = simple_prices
        market = [x * 0.9 for x in simple_prices]

        result = haze.py_beta(stock, market, period=5)

        assert isinstance(result, list)
        assert len(result) == len(stock)
        assert all(isinstance(x, (int, float)) or np.isnan(x) for x in result)

    def test_beta_one(self):
        """测试Beta=1的情况（股票=市场）"""
        stock = [1.0, 2.0, 3.0, 4.0, 5.0]
        market = [1.0, 2.0, 3.0, 4.0, 5.0]

        result = haze.py_beta(stock, market, period=5)

        # Beta应该接近1.0
        assert abs(result[-1] - 1.0) < 0.01

    def test_beta_two(self):
        """测试Beta=2的情况（股票波动是市场2倍）"""
        market = [1.0, 2.0, 3.0, 4.0, 5.0]
        stock = [1.0, 3.0, 5.0, 7.0, 9.0]  # 2倍波动

        result = haze.py_beta(stock, market, period=5)

        # Beta应该接近2.0
        assert abs(result[-1] - 2.0) < 0.01

    def test_different_periods(self, simple_prices):
        """测试不同周期参数"""
        stock = simple_prices
        market = [x * 0.9 for x in simple_prices]

        result_5 = haze.py_beta(stock, market, period=5)
        result_10 = haze.py_beta(stock, market, period=10)

        assert len(result_5) == len(result_10)


# ==================== 6. Standard Error ====================

class TestStandardError:
    """Standard Error (标准误差) 单元测试

    算法：SE = σ / √n
    特点：衡量样本均值的离散程度
    """

    def test_basic_calculation(self, simple_prices):
        """测试基本标准误差计算"""
        result = haze.py_stderr(simple_prices, period=5)

        assert isinstance(result, list)
        assert len(result) == len(simple_prices)
        assert all(isinstance(x, (int, float)) or np.isnan(x) for x in result)

    def test_stderr_positive(self, simple_prices):
        """测试标准误差为正值"""
        result = haze.py_stderr(simple_prices, period=5)

        for se in result:
            if not np.isnan(se):
                assert se >= 0

    def test_constant_values(self):
        """测试常数序列的标准误差为0"""
        constant = [50.0] * 10

        result = haze.py_stderr(constant, period=5)

        for se in result:
            if not np.isnan(se):
                assert abs(se) < 1e-10

    def test_empty_array(self):
        """测试空数组"""
        with pytest.raises(ValueError):
            haze.py_stderr([], period=5)


# ==================== 7. CORREL (TA-Lib) ====================

class TestCORREL:
    """CORREL (相关系数 - TA-Lib) 单元测试

    算法：Pearson相关系数
    特点：TA-Lib实现的相关系数
    """

    def test_basic_calculation(self, simple_prices):
        """测试基本CORREL计算"""
        prices_x = simple_prices
        prices_y = [x * 1.1 for x in simple_prices]

        result = haze.py_correl(prices_x, prices_y, period=5)

        assert isinstance(result, list)
        assert len(result) == len(prices_x)
        assert all(isinstance(x, (int, float)) or np.isnan(x) for x in result)

    def test_correl_range(self, simple_prices):
        """测试CORREL在-1到1范围内"""
        prices_x = simple_prices
        prices_y = [x * 0.9 for x in simple_prices]

        result = haze.py_correl(prices_x, prices_y, period=5)

        for corr in result:
            if not np.isnan(corr):
                assert -1.0 <= corr <= 1.0

    def test_empty_array(self):
        """测试空数组"""
        with pytest.raises(ValueError):
            haze.py_correl([], [], period=5)


# ==================== 8. LINEARREG (TA-Lib) ====================

class TestLINEARREG:
    """LINEARREG (线性回归 - TA-Lib) 单元测试

    算法：线性回归预测值
    特点：TA-Lib实现的线性回归
    """

    def test_basic_calculation(self, simple_prices):
        """测试基本LINEARREG计算"""
        result = haze.py_linearreg(simple_prices, period=5)

        assert isinstance(result, list)
        assert len(result) == len(simple_prices)
        assert all(isinstance(x, (int, float)) or np.isnan(x) for x in result)

    def test_different_periods(self, simple_prices):
        """测试不同周期参数"""
        result_3 = haze.py_linearreg(simple_prices, period=3)
        result_5 = haze.py_linearreg(simple_prices, period=5)

        assert len(result_3) == len(result_5)

    def test_empty_array(self):
        """测试空数组"""
        with pytest.raises(ValueError):
            haze.py_linearreg([], period=5)


# ==================== 9. LINEARREG_SLOPE ====================

class TestLINEARREG_SLOPE:
    """LINEARREG_SLOPE (线性回归斜率) 单元测试

    算法：线性回归的斜率 b
    特点：衡量趋势强度和方向
    """

    def test_basic_calculation(self, simple_prices):
        """测试基本LINEARREG_SLOPE计算"""
        result = haze.py_linearreg_slope(simple_prices, period=5)

        assert isinstance(result, list)
        assert len(result) == len(simple_prices)
        assert all(isinstance(x, (int, float)) or np.isnan(x) for x in result)

    def test_positive_slope(self):
        """测试上升趋势的正斜率"""
        increasing = [1.0, 2.0, 3.0, 4.0, 5.0]

        result = haze.py_linearreg_slope(increasing, period=5)

        # 斜率应该为正
        assert result[-1] > 0

    def test_negative_slope(self):
        """测试下降趋势的负斜率"""
        decreasing = [5.0, 4.0, 3.0, 2.0, 1.0]

        result = haze.py_linearreg_slope(decreasing, period=5)

        # 斜率应该为负
        assert result[-1] < 0

    def test_zero_slope(self):
        """测试水平趋势的零斜率"""
        flat = [3.0] * 10

        result = haze.py_linearreg_slope(flat, period=5)

        # 斜率应该接近0
        for slope in result:
            if not np.isnan(slope):
                assert abs(slope) < 1e-10


# ==================== 10. LINEARREG_ANGLE ====================

class TestLINEARREG_ANGLE:
    """LINEARREG_ANGLE (线性回归角度) 单元测试

    算法：角度 = arctan(slope)
    特点：以角度表示趋势方向
    """

    def test_basic_calculation(self, simple_prices):
        """测试基本LINEARREG_ANGLE计算"""
        result = haze.py_linearreg_angle(simple_prices, period=5)

        assert isinstance(result, list)
        assert len(result) == len(simple_prices)
        assert all(isinstance(x, (int, float)) or np.isnan(x) for x in result)

    def test_angle_range(self, simple_prices):
        """测试角度在-90到90度范围内"""
        result = haze.py_linearreg_angle(simple_prices, period=5)

        for angle in result:
            if not np.isnan(angle):
                assert -90.0 <= angle <= 90.0

    def test_empty_array(self):
        """测试空数组"""
        with pytest.raises(ValueError):
            haze.py_linearreg_angle([], period=5)


# ==================== 11. LINEARREG_INTERCEPT ====================

class TestLINEARREG_INTERCEPT:
    """LINEARREG_INTERCEPT (线性回归截距) 单元测试

    算法：截距 a = ȳ - b·x̄
    特点：线性方程的截距项
    """

    def test_basic_calculation(self, simple_prices):
        """测试基本LINEARREG_INTERCEPT计算"""
        result = haze.py_linearreg_intercept(simple_prices, period=5)

        assert isinstance(result, list)
        assert len(result) == len(simple_prices)
        assert all(isinstance(x, (int, float)) or np.isnan(x) for x in result)

    def test_known_intercept(self):
        """测试已知截距的线性数据"""
        # y = 2x + 3: [3, 5, 7, 9, 11]
        linear_data = [3.0, 5.0, 7.0, 9.0, 11.0]

        result = haze.py_linearreg_intercept(linear_data, period=5)

        # 截距应该接近3.0
        assert abs(result[-1] - 3.0) < 0.1

    def test_empty_array(self):
        """测试空数组"""
        with pytest.raises(ValueError):
            haze.py_linearreg_intercept([], period=5)


# ==================== 12. VAR ====================

class TestVAR:
    """VAR (方差) 单元测试

    算法：Var = Σ(x - μ)² / n
    特点：衡量数据离散程度
    """

    def test_basic_calculation(self, simple_prices):
        """测试基本VAR计算"""
        result = haze.py_var(simple_prices, period=5)

        assert isinstance(result, list)
        assert len(result) == len(simple_prices)
        assert all(isinstance(x, (int, float)) or np.isnan(x) for x in result)

    def test_variance_positive(self, simple_prices):
        """测试方差为非负值"""
        result = haze.py_var(simple_prices, period=5)

        for var in result:
            if not np.isnan(var):
                assert var >= 0

    def test_constant_zero_variance(self):
        """测试常数序列的方差为0"""
        constant = [100.0] * 10

        result = haze.py_var(constant, period=5)

        for var in result:
            if not np.isnan(var):
                assert abs(var) < 1e-10

    def test_known_variance(self):
        """测试已知方差的数据"""
        # [1, 2, 3, 4, 5] 的方差 = 2.0
        data = [1.0, 2.0, 3.0, 4.0, 5.0]

        result = haze.py_var(data, period=5)

        # 样本方差应该接近2.0（或2.5，取决于是总体方差还是样本方差）
        assert 1.5 < result[-1] < 3.0


# ==================== 13. TSF ====================

class TestTSF:
    """TSF (Time Series Forecast) 单元测试

    算法：基于线性回归的时间序列预测
    特点：预测下一个时间点的值
    """

    def test_basic_calculation(self, simple_prices):
        """测试基本TSF计算"""
        result = haze.py_tsf(simple_prices, period=5)

        assert isinstance(result, list)
        assert len(result) == len(simple_prices)
        assert all(isinstance(x, (int, float)) or np.isnan(x) for x in result)

    def test_uptrend_forecast(self):
        """测试上升趋势的预测"""
        increasing = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]

        result = haze.py_tsf(increasing, period=5)

        # 预测值应该大于当前值（上升趋势）
        valid_results = [(r, increasing[i]) for i, r in enumerate(result) if not np.isnan(r)]
        if valid_results:
            last_forecast, last_actual = valid_results[-1]
            assert last_forecast > last_actual

    def test_downtrend_forecast(self):
        """测试下降趋势的预测"""
        decreasing = [10.0, 9.0, 8.0, 7.0, 6.0, 5.0, 4.0, 3.0, 2.0, 1.0]

        result = haze.py_tsf(decreasing, period=5)

        # 预测值应该小于当前值（下降趋势）
        valid_results = [(r, decreasing[i]) for i, r in enumerate(result) if not np.isnan(r)]
        if valid_results:
            last_forecast, last_actual = valid_results[-1]
            assert last_forecast < last_actual

    def test_empty_array(self):
        """测试空数组"""
        with pytest.raises(ValueError):
            haze.py_tsf([], period=5)
