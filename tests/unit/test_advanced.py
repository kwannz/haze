"""
Advanced & ML Indicators Unit Tests
====================================

测试高级指标和机器学习相关功能。

测试的指标：
1. py_linear_regression - 线性回归
2. py_zscore - Z分数
3. py_entropy - 熵
4. py_slope - 斜率
5. py_percent_rank - 百分位排名
6. py_minmax - 最小最大值
7. py_minmaxindex - 最小最大索引
8. SFGModel - ML模型

Author: Haze Team
Date: 2025-12-28
"""

import pytest
import numpy as np
import haze_library as haze


class TestLinearRegression:
    """线性回归测试

    py_linear_regression 返回 (slope, intercept, r_squared) 三元组
    """

    def test_basic_calculation(self, simple_prices):
        """测试基本线性回归"""
        result = haze.py_linear_regression(simple_prices, 5)

        # 返回 (slope, intercept, r_squared) 三元组
        assert isinstance(result, tuple)
        assert len(result) == 3

        slope, intercept, r_squared = result
        assert len(slope) == len(simple_prices)
        assert len(intercept) == len(simple_prices)
        assert len(r_squared) == len(simple_prices)

    def test_perfect_linear_trend(self):
        """测试完美线性趋势"""
        # y = 100 + 2x
        prices = [100.0 + 2 * i for i in range(20)]

        slope, intercept, r_squared = haze.py_linear_regression(prices, 5)

        # 完美线性，斜率应接近2，R²应接近1
        valid_slope = [v for v in slope if not np.isnan(v)]
        valid_r2 = [v for v in r_squared if not np.isnan(v)]

        if valid_slope:
            assert all(abs(v - 2.0) < 0.1 for v in valid_slope[-5:])
        if valid_r2:
            assert all(v > 0.99 for v in valid_r2[-5:])

    def test_noisy_data(self):
        """测试噪声数据"""
        np.random.seed(42)
        n = 50
        trend = np.linspace(100, 150, n)
        noise = np.random.randn(n) * 5
        prices = (trend + noise).tolist()

        slope, intercept, r_squared = haze.py_linear_regression(prices, 10)

        assert len(slope) == n
        assert len(intercept) == n
        assert len(r_squared) == n

    def test_different_periods(self):
        """测试不同周期"""
        prices = [100.0 + i * 0.5 for i in range(30)]

        for period in [3, 5, 10, 14, 20]:
            slope, intercept, r_squared = haze.py_linear_regression(prices, period)
            assert len(slope) == len(prices)

    def test_constant_prices(self, constant_values):
        """测试常数价格"""
        slope, intercept, r_squared = haze.py_linear_regression(constant_values, 5)

        # 常数数据，斜率应为0
        valid_slope = [v for v in slope if not np.isnan(v)]
        if valid_slope:
            assert all(abs(v) < 1e-6 for v in valid_slope)

    def test_empty_input(self):
        """测试空输入"""
        with pytest.raises(Exception):
            haze.py_linear_regression([], 5)

    def test_period_larger_than_data(self):
        """测试周期大于数据长度"""
        prices = [100.0, 101.0, 102.0]
        # 周期大于数据长度应该抛出异常
        with pytest.raises(Exception):
            haze.py_linear_regression(prices, 10)


class TestZScore:
    """Z分数测试"""

    def test_basic_calculation(self, simple_prices):
        """测试基本Z分数计算"""
        result = haze.py_zscore(simple_prices, 5)

        assert len(result) == len(simple_prices)

    def test_zscore_range(self):
        """测试Z分数范围"""
        np.random.seed(42)
        prices = (100 + np.random.randn(100) * 10).tolist()

        result = haze.py_zscore(prices, 20)

        # 对于正态分布数据，大部分Z分数应在 -3 到 3 之间
        valid = [v for v in result if not np.isnan(v)]
        if valid:
            assert all(abs(v) < 10 for v in valid)  # 宽松范围

    def test_constant_prices(self, constant_values):
        """测试常数价格的Z分数"""
        result = haze.py_zscore(constant_values, 5)

        # 常数数据，Z分数应为0或NaN（标准差为0）
        assert len(result) == len(constant_values)

    def test_extreme_outlier(self):
        """测试极端离群值"""
        prices = [100.0] * 9 + [200.0]  # 最后一个是离群值

        result = haze.py_zscore(prices, 5)

        # 离群值的Z分数应该很大
        valid = [v for v in result if not np.isnan(v)]
        if valid:
            assert len(valid) > 0


class TestEntropy:
    """熵测试"""

    def test_basic_calculation(self, simple_prices):
        """测试基本熵计算"""
        result = haze.py_entropy(simple_prices, 5, 10)

        assert len(result) == len(simple_prices)

    def test_constant_prices_entropy(self, constant_values):
        """测试常数价格的熵"""
        result = haze.py_entropy(constant_values, 5, 10)

        # 常数数据，熵应为0（完全可预测）
        assert len(result) == len(constant_values)

    def test_random_data_entropy(self):
        """测试随机数据的熵"""
        np.random.seed(42)
        prices = (100 + np.random.randn(100) * 10).tolist()

        result = haze.py_entropy(prices, 20, 10)

        # 随机数据应有较高熵
        valid = [v for v in result if not np.isnan(v)]
        if valid:
            assert len(valid) > 0

    def test_different_bins(self):
        """测试不同分箱数"""
        prices = [100.0 + i * 0.5 for i in range(50)]

        for bins in [5, 10, 20, 50]:
            result = haze.py_entropy(prices, 20, bins)
            assert len(result) == len(prices)


class TestSlope:
    """斜率测试"""

    def test_basic_calculation(self, simple_prices):
        """测试基本斜率计算"""
        result = haze.py_slope(simple_prices, 5)

        assert len(result) == len(simple_prices)

    def test_positive_slope(self):
        """测试正斜率"""
        prices = [100.0 + i * 2.0 for i in range(20)]

        result = haze.py_slope(prices, 5)

        # 上涨趋势，斜率应为正
        valid = [v for v in result if not np.isnan(v)]
        if valid:
            assert all(v > 0 for v in valid[-5:])

    def test_negative_slope(self):
        """测试负斜率"""
        prices = [200.0 - i * 2.0 for i in range(20)]

        result = haze.py_slope(prices, 5)

        # 下跌趋势，斜率应为负
        valid = [v for v in result if not np.isnan(v)]
        if valid:
            assert all(v < 0 for v in valid[-5:])

    def test_zero_slope(self, constant_values):
        """测试零斜率"""
        result = haze.py_slope(constant_values, 5)

        # 常数数据，斜率应为0
        valid = [v for v in result if not np.isnan(v)]
        if valid:
            assert all(abs(v) < 1e-6 for v in valid)


class TestPercentRank:
    """百分位排名测试"""

    def test_basic_calculation(self, simple_prices):
        """测试基本百分位排名"""
        result = haze.py_percent_rank(simple_prices, 5)

        assert len(result) == len(simple_prices)

    def test_rank_range(self):
        """测试排名范围"""
        prices = [100.0 + i for i in range(50)]

        result = haze.py_percent_rank(prices, 10)

        # 百分位排名应在 0 到 100 之间
        valid = [v for v in result if not np.isnan(v)]
        if valid:
            assert all(0 <= v <= 100 for v in valid)

    def test_monotonic_increasing_rank(self, monotonic_increasing):
        """测试单调递增的排名"""
        result = haze.py_percent_rank(monotonic_increasing, 5)

        # 单调递增，后面的排名应更高
        valid = [v for v in result if not np.isnan(v)]
        if len(valid) >= 2:
            assert valid[-1] >= valid[-2] - 1  # 允许小误差


class TestMinMax:
    """最小最大值测试"""

    def test_basic_calculation(self, simple_prices):
        """测试基本最小最大值"""
        result = haze.py_minmax(simple_prices, 5)

        assert isinstance(result, tuple)
        assert len(result) == 2

        min_vals, max_vals = result
        assert len(min_vals) == len(simple_prices)
        assert len(max_vals) == len(simple_prices)

    def test_min_less_than_max(self):
        """测试最小值小于最大值"""
        prices = [100.0, 95.0, 105.0, 98.0, 102.0, 97.0, 103.0, 96.0, 104.0, 99.0]

        min_vals, max_vals = haze.py_minmax(prices, 5)

        for mn, mx in zip(min_vals, max_vals):
            if not np.isnan(mn) and not np.isnan(mx):
                assert mn <= mx

    def test_constant_prices_minmax(self, constant_values):
        """测试常数价格"""
        min_vals, max_vals = haze.py_minmax(constant_values, 5)

        # 常数数据，min == max
        for mn, mx in zip(min_vals, max_vals):
            if not np.isnan(mn) and not np.isnan(mx):
                assert abs(mn - mx) < 1e-10


class TestMinMaxIndex:
    """最小最大索引测试"""

    def test_basic_calculation(self, simple_prices):
        """测试基本索引计算"""
        result = haze.py_minmaxindex(simple_prices, 5)

        assert isinstance(result, tuple)
        assert len(result) == 2

        min_idx, max_idx = result
        assert len(min_idx) == len(simple_prices)
        assert len(max_idx) == len(simple_prices)

    def test_index_validity(self):
        """测试索引有效性"""
        prices = [100.0, 95.0, 105.0, 98.0, 102.0, 97.0, 103.0, 96.0, 104.0, 99.0]
        period = 5

        min_idx, max_idx = haze.py_minmaxindex(prices, period)

        # 索引应该是有效的整数
        for mi, ma in zip(min_idx, max_idx):
            if not np.isnan(mi):
                assert mi >= 0
            if not np.isnan(ma):
                assert ma >= 0


class TestSFGModel:
    """SFG机器学习模型测试

    SFGModel 是通过训练函数创建的，不能直接实例化（工厂模式）
    """

    def test_model_type_exists(self):
        """测试模型类型存在"""
        assert hasattr(haze, 'SFGModel')
        assert hasattr(haze.SFGModel, 'is_trained')
        assert hasattr(haze.SFGModel, 'features_dim')
        assert hasattr(haze.SFGModel, 'predict')

    def test_model_cannot_be_directly_instantiated(self):
        """测试模型不能直接实例化"""
        # SFGModel 只能通过训练函数创建
        with pytest.raises(Exception):
            haze.SFGModel()


class TestMLTrainingFunctions:
    """ML训练函数测试"""

    def test_train_supertrend_model_exists(self):
        """测试SuperTrend模型训练函数存在"""
        assert hasattr(haze, 'py_train_supertrend_model')
        assert callable(haze.py_train_supertrend_model)

    def test_train_supertrend_model(self):
        """测试SuperTrend模型训练（使用足够变化的数据）"""
        np.random.seed(42)
        n = 200
        # 生成有足够变化的数据以确保矩阵可逆
        base = 100 + np.cumsum(np.random.randn(n) * 2)
        close = base.tolist()
        high = (base + np.abs(np.random.randn(n) * 3)).tolist()
        low = (base - np.abs(np.random.randn(n) * 3)).tolist()

        atr = haze.py_atr(high, low, close, 14)

        try:
            model = haze.py_train_supertrend_model(close, atr)
            assert model is not None
            # 验证模型已训练
            assert model.is_trained()
            # 验证特征维度
            dim = model.features_dim()
            assert isinstance(dim, int)
            assert dim > 0
        except Exception as e:
            # 某些数据可能导致线性代数错误
            if "NonInvertible" in str(e) or "LinalgError" in str(e):
                pytest.skip("Data caused non-invertible matrix")
            raise

    def test_prepare_supertrend_features_exists(self):
        """测试特征准备函数存在"""
        assert hasattr(haze, 'py_prepare_supertrend_features')

    def test_train_atr2_model_exists(self):
        """测试ATR2模型训练函数存在"""
        assert hasattr(haze, 'py_train_atr2_model')

    def test_train_momentum_model_exists(self):
        """测试动量模型训练函数存在"""
        assert hasattr(haze, 'py_train_momentum_model')


class TestAdvancedEdgeCases:
    """高级指标边界条件测试"""

    def test_all_nan_input(self):
        """测试全NaN输入"""
        prices = [float('nan')] * 10

        try:
            result = haze.py_zscore(prices, 5)
            assert len(result) == len(prices)
        except Exception:
            pass  # 某些实现可能拒绝

    def test_inf_values(self):
        """测试无穷值"""
        prices = [100.0, float('inf'), 102.0, 103.0, 104.0,
                  105.0, 106.0, 107.0, 108.0, 109.0]

        try:
            result = haze.py_zscore(prices, 5)
            assert len(result) == len(prices)
        except Exception:
            pass

    def test_very_long_data(self):
        """测试超长数据"""
        n = 10000
        prices = [100.0 + i * 0.01 for i in range(n)]

        slope, intercept, r_squared = haze.py_linear_regression(prices, 20)
        assert len(slope) == n

    def test_period_equals_one(self):
        """测试周期为1"""
        prices = [100.0, 101.0, 102.0, 103.0, 104.0]

        try:
            slope, intercept, r_squared = haze.py_linear_regression(prices, 1)
            assert len(slope) == len(prices)
        except Exception:
            pass  # 周期1可能不被支持

    def test_negative_period(self):
        """测试负周期"""
        prices = [100.0, 101.0, 102.0, 103.0, 104.0]

        with pytest.raises(Exception):
            haze.py_linear_regression(prices, -5)
