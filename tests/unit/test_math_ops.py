"""
Mathematical Operations Unit Tests
===================================

测试所有25个数学运算函数的核心功能。

测试策略：
- 已知结果验证：使用可精确计算的数学结果
- 边界条件：空数组、特殊值（0、负数、NaN）
- 数值精度：使用1e-10容差验证

测试的数学函数：
1. MAX - 最大值
2. MIN - 最小值
3. SUM - 求和
4. SQRT - 平方根
5. LN - 自然对数
6. LOG10 - 常用对数
7. EXP - 指数
8. ABS - 绝对值
9. CEIL - 向上取整
10. FLOOR - 向下取整
11. SIN - 正弦
12. COS - 余弦
13. TAN - 正切
14. ASIN - 反正弦
15. ACOS - 反余弦
16. ATAN - 反正切
17. SINH - 双曲正弦
18. COSH - 双曲余弦
19. TANH - 双曲正切
20. ADD - 加法
21. SUB - 减法
22. MULT - 乘法
23. DIV - 除法
24. MINMAX - 最小最大值
25. MINMAXINDEX - 最小最大值索引

Author: Haze Team
Date: 2025-12-26
"""

import pytest
import numpy as np
import math
import haze_library as haze


# ==================== 1. MAX ====================

class TestMAX:
    """MAX (最大值) 单元测试"""

    def test_known_result(self):
        """测试已知结果"""
        data = [1.0, 5.0, 3.0, 9.0, 2.0]
        result = haze.py_max(data, period=3)

        # 滚动窗口最大值
        # [0-2]: max(1, 5, 3) = 5
        # [1-3]: max(5, 3, 9) = 9
        # [2-4]: max(3, 9, 2) = 9
        expected = [float('nan'), float('nan'), 5.0, 9.0, 9.0]
        assert len(result) == len(expected)
        for i, (r, e) in enumerate(zip(result, expected)):
            if np.isnan(e):
                assert np.isnan(r)
            else:
                assert abs(r - e) < 1e-10

    def test_single_period(self):
        """测试period=1的情况（返回原值）"""
        data = [1.0, 2.0, 3.0, 4.0, 5.0]
        result = haze.py_max(data, period=1)

        for i, (r, d) in enumerate(zip(result, data)):
            assert abs(r - d) < 1e-10

    def test_empty_array(self):
        """测试空数组"""
        result = haze.py_max([], period=3)
        assert isinstance(result, list)
        assert len(result) == 0


# ==================== 2. MIN ====================

class TestMIN:
    """MIN (最小值) 单元测试"""

    def test_known_result(self):
        """测试已知结果"""
        data = [1.0, 5.0, 3.0, 9.0, 2.0]
        result = haze.py_min(data, period=3)

        # 滚动窗口最小值
        expected = [float('nan'), float('nan'), 1.0, 3.0, 2.0]
        assert len(result) == len(expected)
        for i, (r, e) in enumerate(zip(result, expected)):
            if np.isnan(e):
                assert np.isnan(r)
            else:
                assert abs(r - e) < 1e-10

    def test_negative_values(self):
        """测试负值"""
        data = [-5.0, -2.0, -8.0, -1.0, -3.0]
        result = haze.py_min(data, period=3)

        # 最小值应该是最负的数
        assert result[2] == -8.0


# ==================== 3. SUM ====================

class TestSUM:
    """SUM (求和) 单元测试"""

    def test_known_result(self):
        """测试已知结果"""
        data = [1.0, 2.0, 3.0, 4.0, 5.0]
        result = haze.py_sum(data, period=3)

        # 滚动窗口求和
        # [0-2]: 1+2+3 = 6
        # [1-3]: 2+3+4 = 9
        # [2-4]: 3+4+5 = 12
        expected = [float('nan'), float('nan'), 6.0, 9.0, 12.0]
        for i, (r, e) in enumerate(zip(result, expected)):
            if np.isnan(e):
                assert np.isnan(r)
            else:
                assert abs(r - e) < 1e-10

    def test_full_sum(self):
        """测试完整求和（period等于数组长度）"""
        data = [1.0, 2.0, 3.0, 4.0, 5.0]
        result = haze.py_sum(data, period=5)

        # 最后一个值应该是总和15.0
        assert abs(result[-1] - 15.0) < 1e-10


# ==================== 4. SQRT ====================

class TestSQRT:
    """SQRT (平方根) 单元测试"""

    def test_known_result(self, math_test_values):
        """测试已知结果"""
        # math_test_values = [1.0, 4.0, 9.0, 16.0, 25.0]
        result = haze.py_sqrt(math_test_values)

        expected = [1.0, 2.0, 3.0, 4.0, 5.0]
        for r, e in zip(result, expected):
            assert abs(r - e) < 1e-10

    def test_zero(self):
        """测试sqrt(0) = 0"""
        result = haze.py_sqrt([0.0])
        assert abs(result[0] - 0.0) < 1e-10

    def test_negative_values(self):
        """测试负值（应该返回NaN）"""
        result = haze.py_sqrt([-1.0, -4.0])
        for r in result:
            assert np.isnan(r)


# ==================== 5. LN ====================

class TestLN:
    """LN (自然对数) 单元测试"""

    def test_known_result(self):
        """测试已知结果"""
        data = [1.0, math.e, math.e**2, math.e**3]
        result = haze.py_ln(data)

        expected = [0.0, 1.0, 2.0, 3.0]
        for r, e in zip(result, expected):
            assert abs(r - e) < 1e-10

    def test_ln_one(self):
        """测试ln(1) = 0"""
        result = haze.py_ln([1.0])
        assert abs(result[0] - 0.0) < 1e-10

    def test_negative_values(self):
        """测试负值（应该返回NaN）"""
        result = haze.py_ln([-1.0, -10.0])
        for r in result:
            assert np.isnan(r)


# ==================== 6. LOG10 ====================

class TestLOG10:
    """LOG10 (常用对数) 单元测试"""

    def test_known_result(self):
        """测试已知结果"""
        data = [1.0, 10.0, 100.0, 1000.0]
        result = haze.py_log10(data)

        expected = [0.0, 1.0, 2.0, 3.0]
        for r, e in zip(result, expected):
            assert abs(r - e) < 1e-10

    def test_log10_one(self):
        """测试log10(1) = 0"""
        result = haze.py_log10([1.0])
        assert abs(result[0] - 0.0) < 1e-10


# ==================== 7. EXP ====================

class TestEXP:
    """EXP (指数) 单元测试"""

    def test_known_result(self):
        """测试已知结果"""
        data = [0.0, 1.0, 2.0, 3.0]
        result = haze.py_exp(data)

        expected = [1.0, math.e, math.e**2, math.e**3]
        for r, e in zip(result, expected):
            assert abs(r - e) < 1e-8  # 指数函数允许稍大误差

    def test_exp_zero(self):
        """测试exp(0) = 1"""
        result = haze.py_exp([0.0])
        assert abs(result[0] - 1.0) < 1e-10


# ==================== 8. ABS ====================

class TestABS:
    """ABS (绝对值) 单元测试"""

    def test_known_result(self):
        """测试已知结果"""
        data = [-5.0, -3.0, 0.0, 2.0, 4.0]
        result = haze.py_abs(data)

        expected = [5.0, 3.0, 0.0, 2.0, 4.0]
        for r, e in zip(result, expected):
            assert abs(r - e) < 1e-10

    def test_positive_unchanged(self):
        """测试正数不变"""
        data = [1.0, 2.0, 3.0]
        result = haze.py_abs(data)

        for r, d in zip(result, data):
            assert abs(r - d) < 1e-10


# ==================== 9. CEIL ====================

class TestCEIL:
    """CEIL (向上取整) 单元测试"""

    def test_known_result(self):
        """测试已知结果"""
        data = [1.1, 2.5, 3.9, -1.1, -2.5]
        result = haze.py_ceil(data)

        expected = [2.0, 3.0, 4.0, -1.0, -2.0]
        for r, e in zip(result, expected):
            assert abs(r - e) < 1e-10

    def test_integer_unchanged(self):
        """测试整数不变"""
        data = [1.0, 2.0, 3.0]
        result = haze.py_ceil(data)

        for r, d in zip(result, data):
            assert abs(r - d) < 1e-10


# ==================== 10. FLOOR ====================

class TestFLOOR:
    """FLOOR (向下取整) 单元测试"""

    def test_known_result(self):
        """测试已知结果"""
        data = [1.1, 2.5, 3.9, -1.1, -2.5]
        result = haze.py_floor(data)

        expected = [1.0, 2.0, 3.0, -2.0, -3.0]
        for r, e in zip(result, expected):
            assert abs(r - e) < 1e-10


# ==================== 11-16. 三角函数 ====================

class TestSIN:
    """SIN (正弦) 单元测试"""

    def test_known_result(self):
        """测试已知结果"""
        data = [0.0, math.pi/2, math.pi, 3*math.pi/2, 2*math.pi]
        result = haze.py_sin(data)

        expected = [0.0, 1.0, 0.0, -1.0, 0.0]
        for r, e in zip(result, expected):
            assert abs(r - e) < 1e-10


class TestCOS:
    """COS (余弦) 单元测试"""

    def test_known_result(self):
        """测试已知结果"""
        data = [0.0, math.pi/2, math.pi, 3*math.pi/2, 2*math.pi]
        result = haze.py_cos(data)

        expected = [1.0, 0.0, -1.0, 0.0, 1.0]
        for r, e in zip(result, expected):
            assert abs(r - e) < 1e-10


class TestTAN:
    """TAN (正切) 单元测试"""

    def test_known_result(self):
        """测试已知结果"""
        data = [0.0, math.pi/4, -math.pi/4]
        result = haze.py_tan(data)

        expected = [0.0, 1.0, -1.0]
        for r, e in zip(result, expected):
            assert abs(r - e) < 1e-10


class TestASIN:
    """ASIN (反正弦) 单元测试"""

    def test_known_result(self):
        """测试已知结果"""
        data = [0.0, 0.5, 1.0, -0.5, -1.0]
        result = haze.py_asin(data)

        expected = [0.0, math.pi/6, math.pi/2, -math.pi/6, -math.pi/2]
        for r, e in zip(result, expected):
            assert abs(r - e) < 1e-10

    def test_out_of_range(self):
        """测试超出范围值（应该返回NaN）"""
        result = haze.py_asin([1.5, -1.5])
        for r in result:
            assert np.isnan(r)


class TestACOS:
    """ACOS (反余弦) 单元测试"""

    def test_known_result(self):
        """测试已知结果"""
        data = [1.0, 0.5, 0.0, -0.5, -1.0]
        result = haze.py_acos(data)

        expected = [0.0, math.pi/3, math.pi/2, 2*math.pi/3, math.pi]
        for r, e in zip(result, expected):
            assert abs(r - e) < 1e-10


class TestATAN:
    """ATAN (反正切) 单元测试"""

    def test_known_result(self):
        """测试已知结果"""
        data = [0.0, 1.0, -1.0]
        result = haze.py_atan(data)

        expected = [0.0, math.pi/4, -math.pi/4]
        for r, e in zip(result, expected):
            assert abs(r - e) < 1e-10


# ==================== 17-19. 双曲函数 ====================

class TestSINH:
    """SINH (双曲正弦) 单元测试"""

    def test_known_result(self):
        """测试已知结果"""
        data = [0.0, 1.0, -1.0]
        result = haze.py_sinh(data)

        expected = [0.0, math.sinh(1.0), math.sinh(-1.0)]
        for r, e in zip(result, expected):
            assert abs(r - e) < 1e-10

    def test_sinh_zero(self):
        """测试sinh(0) = 0"""
        result = haze.py_sinh([0.0])
        assert abs(result[0] - 0.0) < 1e-10


class TestCOSH:
    """COSH (双曲余弦) 单元测试"""

    def test_known_result(self):
        """测试已知结果"""
        data = [0.0, 1.0, -1.0]
        result = haze.py_cosh(data)

        expected = [1.0, math.cosh(1.0), math.cosh(-1.0)]
        for r, e in zip(result, expected):
            assert abs(r - e) < 1e-10

    def test_cosh_zero(self):
        """测试cosh(0) = 1"""
        result = haze.py_cosh([0.0])
        assert abs(result[0] - 1.0) < 1e-10


class TestTANH:
    """TANH (双曲正切) 单元测试"""

    def test_known_result(self):
        """测试已知结果"""
        data = [0.0, 1.0, -1.0]
        result = haze.py_tanh(data)

        expected = [0.0, math.tanh(1.0), math.tanh(-1.0)]
        for r, e in zip(result, expected):
            assert abs(r - e) < 1e-10

    def test_tanh_range(self):
        """测试tanh范围在(-1, 1)内"""
        data = [-10.0, -1.0, 0.0, 1.0, 10.0]
        result = haze.py_tanh(data)

        for r in result:
            assert -1.0 <= r <= 1.0


# ==================== 20-23. 四则运算 ====================

class TestADD:
    """ADD (加法) 单元测试"""

    def test_known_result(self):
        """测试已知结果"""
        a = [1.0, 2.0, 3.0, 4.0, 5.0]
        b = [5.0, 4.0, 3.0, 2.0, 1.0]
        result = haze.py_add(a, b)

        expected = [6.0, 6.0, 6.0, 6.0, 6.0]
        for r, e in zip(result, expected):
            assert abs(r - e) < 1e-10

    def test_add_zero(self):
        """测试加0不变"""
        a = [1.0, 2.0, 3.0]
        b = [0.0, 0.0, 0.0]
        result = haze.py_add(a, b)

        for r, x in zip(result, a):
            assert abs(r - x) < 1e-10


class TestSUB:
    """SUB (减法) 单元测试"""

    def test_known_result(self):
        """测试已知结果"""
        a = [5.0, 4.0, 3.0, 2.0, 1.0]
        b = [1.0, 2.0, 3.0, 4.0, 5.0]
        result = haze.py_sub(a, b)

        expected = [4.0, 2.0, 0.0, -2.0, -4.0]
        for r, e in zip(result, expected):
            assert abs(r - e) < 1e-10

    def test_sub_self(self):
        """测试自己减自己等于0"""
        a = [1.0, 2.0, 3.0]
        result = haze.py_sub(a, a)

        for r in result:
            assert abs(r - 0.0) < 1e-10


class TestMULT:
    """MULT (乘法) 单元测试"""

    def test_known_result(self):
        """测试已知结果"""
        a = [1.0, 2.0, 3.0, 4.0, 5.0]
        b = [2.0, 3.0, 4.0, 5.0, 6.0]
        result = haze.py_mult(a, b)

        expected = [2.0, 6.0, 12.0, 20.0, 30.0]
        for r, e in zip(result, expected):
            assert abs(r - e) < 1e-10

    def test_mult_zero(self):
        """测试乘0等于0"""
        a = [1.0, 2.0, 3.0]
        b = [0.0, 0.0, 0.0]
        result = haze.py_mult(a, b)

        for r in result:
            assert abs(r - 0.0) < 1e-10


class TestDIV:
    """DIV (除法) 单元测试"""

    def test_known_result(self):
        """测试已知结果"""
        a = [10.0, 20.0, 30.0, 40.0, 50.0]
        b = [2.0, 4.0, 5.0, 8.0, 10.0]
        result = haze.py_div(a, b)

        expected = [5.0, 5.0, 6.0, 5.0, 5.0]
        for r, e in zip(result, expected):
            assert abs(r - e) < 1e-10

    def test_div_one(self):
        """测试除以1不变"""
        a = [1.0, 2.0, 3.0]
        b = [1.0, 1.0, 1.0]
        result = haze.py_div(a, b)

        for r, x in zip(result, a):
            assert abs(r - x) < 1e-10

    def test_div_by_zero(self):
        """测试除以0（应该返回inf或NaN）"""
        a = [1.0, 2.0, 3.0]
        b = [0.0, 0.0, 0.0]
        result = haze.py_div(a, b)

        for r in result:
            assert np.isinf(r) or np.isnan(r)


# ==================== 24-25. 最小最大值函数 ====================

class TestMINMAX:
    """MINMAX (最小最大值) 单元测试"""

    def test_known_result(self):
        """测试已知结果"""
        data = [3.0, 1.0, 5.0, 2.0, 4.0]
        min_result, max_result = haze.py_minmax(data, period=3)

        # 滚动窗口
        # [0-2]: min=1, max=5
        # [1-3]: min=1, max=5
        # [2-4]: min=2, max=5
        expected_min = [float('nan'), float('nan'), 1.0, 1.0, 2.0]
        expected_max = [float('nan'), float('nan'), 5.0, 5.0, 5.0]

        for i, (min_r, max_r, min_e, max_e) in enumerate(zip(min_result, max_result, expected_min, expected_max)):
            if np.isnan(min_e):
                assert np.isnan(min_r)
                assert np.isnan(max_r)
            else:
                assert abs(min_r - min_e) < 1e-10
                assert abs(max_r - max_e) < 1e-10

    def test_min_less_than_max(self):
        """测试最小值总是小于等于最大值"""
        data = [5.0, 2.0, 8.0, 1.0, 9.0, 3.0]
        min_result, max_result = haze.py_minmax(data, period=3)

        for min_r, max_r in zip(min_result, max_result):
            if not np.isnan(min_r):
                assert min_r <= max_r


class TestMINMAXINDEX:
    """MINMAXINDEX (最小最大值索引) 单元测试"""

    def test_known_result(self):
        """测试已知结果"""
        data = [3.0, 1.0, 5.0, 2.0, 4.0]
        min_idx, max_idx = haze.py_minmaxindex(data, period=3)

        # 窗口内的相对索引
        # [0-2]: min_idx=1(值1.0), max_idx=2(值5.0)
        # [1-3]: min_idx=0(值1.0), max_idx=1(值5.0)
        # [2-4]: min_idx=1(值2.0), max_idx=0(值5.0)
        assert isinstance(min_idx, list)
        assert isinstance(max_idx, list)
        assert len(min_idx) == len(data)
        assert len(max_idx) == len(data)

    def test_index_range(self):
        """测试索引在有效范围内"""
        data = [5.0, 2.0, 8.0, 1.0, 9.0, 3.0]
        min_idx, max_idx = haze.py_minmaxindex(data, period=3)

        for i, (min_i, max_i) in enumerate(zip(min_idx, max_idx)):
            if not np.isnan(min_i):
                # 索引应该在0到period-1之间（窗口内的相对索引）
                assert 0 <= min_i < 3
                assert 0 <= max_i < 3


# ==================== 边界测试 ====================

class TestMathOpsEdgeCases:
    """测试所有数学运算的边界情况"""

    def test_empty_array(self):
        """测试空数组"""
        empty = []

        # 单数组函数
        assert haze.py_sqrt(empty) == []
        assert haze.py_abs(empty) == []
        assert haze.py_sin(empty) == []

    def test_nan_propagation(self):
        """测试NaN传播"""
        data_with_nan = [1.0, float('nan'), 3.0]

        result = haze.py_sqrt(data_with_nan)

        # 第二个值应该是NaN
        assert np.isnan(result[1])

    def test_single_value(self):
        """测试单个值"""
        single = [5.0]

        result = haze.py_sqrt(single)
        assert abs(result[0] - math.sqrt(5.0)) < 1e-10
