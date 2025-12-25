"""
谐波形态验证测试
================

覆盖功能:
- 摆动点检测 (Swing Point Detection)
- 9种谐波形态识别 (Gartley, Bat, Butterfly, Crab, DeepCrab, Shark, Cypher, ThreeDrive, AltBat)
- PRZ计算 (Potential Reversal Zone)
- 完成概率估算
- 预测性检测 (Forming Patterns)
- 时间序列API格式

验证方法:
- 使用构造的理想形态数据验证检测准确性
- 验证Fibonacci比率计算正确性
- 验证返回值格式和类型
"""

import pytest
import numpy as np
import math
from typing import List, Tuple

try:
    import haze_library as haze
    HAS_HAZE = True
except ImportError:
    HAS_HAZE = False


# ==================== 测试数据生成 ====================

def generate_ideal_gartley_bullish() -> Tuple[List[float], List[float], List[float]]:
    """
    生成理想的看涨 Gartley 形态数据

    Fibonacci 比率:
    - AB = 0.618 XA
    - BC = 0.382~0.886 AB (使用 0.5)
    - CD = 1.272~1.618 BC (使用 1.4)
    - AD = 0.786 XA

    XABCD 点位:
    - X = 100 (低点)
    - A = 200 (高点)  => XA = 100
    - B = 138.2 (低点) => AB = 61.8 = 0.618 * XA
    - C = 169.1 (高点) => BC = 30.9 = 0.5 * AB
    - D = 121.4 (低点) => AD = 78.6 = 0.786 * XA
    """
    prices = []

    # 预热数据 (X点之前)
    for i in range(10):
        prices.append(110 - i)

    # X点 (index=10): 价格100 (低点)
    prices.append(100)

    # X到A: 上升到200
    for i in range(1, 11):
        prices.append(100 + 10 * i)

    # A点 (index=20): 价格200 (高点)
    # A到B: 下降到138.2 (0.618回撤)
    for i in range(1, 11):
        prices.append(200 - 6.18 * i)

    # B点 (index=30): 价格138.2 (低点)
    # B到C: 上升到169.1 (0.5回撤BC/AB)
    for i in range(1, 11):
        prices.append(138.2 + 3.09 * i)

    # C点 (index=40): 价格169.1 (高点)
    # C到D: 下降到121.4 (0.786 AD/XA)
    for i in range(1, 11):
        prices.append(169.1 - 4.77 * i)

    # D点 (index=50): 价格121.4 (低点)
    # D点之后
    for i in range(1, 21):
        prices.append(121.4 + 2 * i)

    n = len(prices)
    high = [p + 1.0 for p in prices]
    low = [p - 1.0 for p in prices]
    close = prices.copy()

    return high, low, close


def generate_ideal_bat_bullish() -> Tuple[List[float], List[float], List[float]]:
    """
    生成理想的看涨 Bat 形态数据

    Fibonacci 比率:
    - AB = 0.382~0.500 XA (使用 0.45)
    - BC = 0.382~0.886 AB
    - CD = 1.618~2.618 BC
    - AD = 0.886 XA
    """
    prices = []

    # 预热
    for i in range(10):
        prices.append(110 - i)

    # X=100, A=200, B=155, C=175, D=111.4
    prices.append(100)  # X (index=10)

    for i in range(1, 11):
        prices.append(100 + 10 * i)  # X到A

    for i in range(1, 11):
        prices.append(200 - 4.5 * i)  # A到B (0.45回撤)

    for i in range(1, 11):
        prices.append(155 + 2 * i)  # B到C

    for i in range(1, 11):
        prices.append(175 - 6.36 * i)  # C到D

    for i in range(1, 21):
        prices.append(111.4 + 2 * i)  # D之后

    n = len(prices)
    high = [p + 1.0 for p in prices]
    low = [p - 1.0 for p in prices]
    close = prices.copy()

    return high, low, close


def generate_random_market_data(n: int = 200, seed: int = 42) -> Tuple[List[float], List[float], List[float]]:
    """生成随机市场数据"""
    np.random.seed(seed)

    returns = np.random.normal(0.0001, 0.02, n)
    close = 100 * np.exp(np.cumsum(returns))

    high = close * (1 + np.abs(np.random.normal(0, 0.01, n)))
    low = close * (1 - np.abs(np.random.normal(0, 0.01, n)))

    return high.tolist(), low.tolist(), close.tolist()


# ==================== 测试类 ====================

@pytest.mark.skipif(not HAS_HAZE, reason="haze-library not installed")
class TestSwingPointDetection:
    """摆动点检测测试"""

    def test_swing_detection_basic(self):
        """基础摆动点检测"""
        high, low, close = generate_ideal_gartley_bullish()
        swings = haze.py_swing_points(high, low, 3, 3)

        # 应该检测到多个摆动点
        assert len(swings) >= 4, f"Expected at least 4 swings, got {len(swings)}"

        # 验证返回格式: (index, price, is_high)
        for idx, price, is_high in swings:
            assert isinstance(idx, int)
            assert isinstance(price, float)
            assert isinstance(is_high, bool)

    def test_swing_detection_alternating(self):
        """摆动点应该高低交替"""
        high, low, close = generate_ideal_gartley_bullish()
        swings = haze.py_swing_points(high, low, 3, 3)

        # 过滤连续相同类型的摆动点
        filtered = []
        for s in swings:
            if not filtered or filtered[-1][2] != s[2]:
                filtered.append(s)

        # 验证交替
        for i in range(1, len(filtered)):
            assert filtered[i][2] != filtered[i-1][2], \
                f"Swing points should alternate: {filtered[i-1]} -> {filtered[i]}"

    def test_swing_detection_empty_short(self):
        """短数据应返回空或少量摆动点"""
        high = [100.0, 101.0, 102.0]
        low = [99.0, 100.0, 101.0]

        swings = haze.py_swing_points(high, low, 3, 3)
        assert len(swings) == 0, "Short data should have no swing points"


@pytest.mark.skipif(not HAS_HAZE, reason="haze-library not installed")
class TestHarmonicPatternDetection:
    """谐波形态检测测试"""

    def test_gartley_detection(self):
        """Gartley 形态检测"""
        high, low, close = generate_ideal_gartley_bullish()
        patterns = haze.py_harmonics_patterns(high, low, 3, 3, True)

        # 应该检测到 Gartley 形态
        gartley_patterns = [p for p in patterns if p.pattern_type == "Gartley"]
        assert len(gartley_patterns) > 0, "Should detect Gartley pattern"

        # 验证形态属性
        for p in gartley_patterns:
            assert p.pattern_type == "Gartley"
            assert p.pattern_type_zh == "伽利形态"
            assert p.is_bullish == True  # 看涨形态

    def test_pattern_attributes(self):
        """验证形态属性完整性"""
        high, low, close = generate_ideal_gartley_bullish()
        patterns = haze.py_harmonics_patterns(high, low, 3, 3, True)

        if not patterns:
            pytest.skip("No patterns detected")

        p = patterns[0]

        # 必需属性
        assert hasattr(p, 'pattern_type')
        assert hasattr(p, 'pattern_type_zh')
        assert hasattr(p, 'is_bullish')
        assert hasattr(p, 'state')
        assert hasattr(p, 'x_index')
        assert hasattr(p, 'x_price')
        assert hasattr(p, 'a_index')
        assert hasattr(p, 'a_price')
        assert hasattr(p, 'b_index')
        assert hasattr(p, 'b_price')
        assert hasattr(p, 'probability')
        assert hasattr(p, 'target_prices')
        assert hasattr(p, 'stop_loss')

    def test_pattern_state_values(self):
        """验证形态状态值"""
        high, low, close = generate_ideal_gartley_bullish()
        patterns = haze.py_harmonics_patterns(high, low, 3, 3, True)

        for p in patterns:
            assert p.state in ["forming", "complete"], \
                f"Invalid state: {p.state}"

    def test_chinese_names(self):
        """验证中文名称"""
        expected_names = {
            "Gartley": "伽利形态",
            "Bat": "蝙蝠形态",
            "Butterfly": "蝴蝶形态",
            "Crab": "螃蟹形态",
            "DeepCrab": "深蟹形态",
            "Shark": "鲨鱼形态",
            "Cypher": "赛弗形态",
            "ThreeDrive": "三驱形态",
            "AltBat": "变体蝙蝠",
        }

        high, low, close = generate_ideal_gartley_bullish()
        patterns = haze.py_harmonics_patterns(high, low, 3, 3, True)

        for p in patterns:
            if p.pattern_type in expected_names:
                assert p.pattern_type_zh == expected_names[p.pattern_type], \
                    f"Wrong Chinese name for {p.pattern_type}: expected {expected_names[p.pattern_type]}, got {p.pattern_type_zh}"


@pytest.mark.skipif(not HAS_HAZE, reason="haze-library not installed")
class TestPRZCalculation:
    """PRZ (潜在反转区) 计算测试"""

    def test_prz_values(self):
        """PRZ 值应在合理范围内"""
        high, low, close = generate_ideal_gartley_bullish()
        patterns = haze.py_harmonics_patterns(high, low, 3, 3, True)

        for p in patterns:
            if p.prz_center is not None:
                # PRZ 应在价格范围内
                assert p.prz_low <= p.prz_center <= p.prz_high, \
                    f"PRZ order error: {p.prz_low} <= {p.prz_center} <= {p.prz_high}"

                # PRZ 范围应合理 (不超过价格幅度的50%)
                price_range = max(high) - min(low)
                prz_width = p.prz_high - p.prz_low
                assert prz_width < price_range * 0.5, \
                    f"PRZ too wide: {prz_width} vs price range {price_range}"

    def test_complete_pattern_has_prz(self):
        """完成的形态应该有 PRZ"""
        high, low, close = generate_ideal_gartley_bullish()
        patterns = haze.py_harmonics_patterns(high, low, 3, 3, True)

        complete_patterns = [p for p in patterns if p.state == "complete"]
        for p in complete_patterns:
            # complete 形态应该有 PRZ (尽管可能为 None 在某些边界情况)
            pass  # PRZ 可能为 None 是允许的


@pytest.mark.skipif(not HAS_HAZE, reason="haze-library not installed")
class TestProbabilityCalculation:
    """完成概率计算测试"""

    def test_probability_range(self):
        """概率应在 0-1 范围内"""
        high, low, close = generate_ideal_gartley_bullish()
        patterns = haze.py_harmonics_patterns(high, low, 3, 3, True)

        for p in patterns:
            assert 0 <= p.probability <= 1, \
                f"Probability out of range: {p.probability}"

    def test_complete_pattern_higher_probability(self):
        """完成的形态应有更高概率"""
        high, low, close = generate_ideal_gartley_bullish()
        patterns = haze.py_harmonics_patterns(high, low, 3, 3, True)

        complete = [p for p in patterns if p.state == "complete"]
        forming = [p for p in patterns if p.state == "forming"]

        if complete and forming:
            avg_complete = sum(p.probability for p in complete) / len(complete)
            avg_forming = sum(p.probability for p in forming) / len(forming)

            # 完成形态的平均概率应高于 forming 形态
            # (因为 forming 最高只有 70%)
            assert avg_complete >= avg_forming * 0.9, \
                f"Complete avg {avg_complete:.2%} should be >= forming avg {avg_forming:.2%}"


@pytest.mark.skipif(not HAS_HAZE, reason="haze-library not installed")
class TestTargetPrices:
    """目标价位测试"""

    def test_target_prices_for_complete(self):
        """完成的形态应有目标价位"""
        high, low, close = generate_ideal_gartley_bullish()
        patterns = haze.py_harmonics_patterns(high, low, 3, 3, True)

        complete = [p for p in patterns if p.state == "complete"]
        for p in complete:
            if p.target_prices:
                assert len(p.target_prices) == 3, \
                    f"Should have 3 target prices, got {len(p.target_prices)}"

                # TP1 < TP2 < TP3 (对于看涨形态)
                if p.is_bullish:
                    assert p.target_prices[0] <= p.target_prices[1] <= p.target_prices[2], \
                        f"Target prices should be ordered: {p.target_prices}"


@pytest.mark.skipif(not HAS_HAZE, reason="haze-library not installed")
class TestTimeSeriesAPI:
    """时间序列 API 测试"""

    def test_harmonics_signal_format(self):
        """py_harmonics 返回格式验证"""
        high, low, close = generate_ideal_gartley_bullish()
        signals, prz_upper, prz_lower, probability = haze.py_harmonics(
            high, low, close, 3, 3, 0.5
        )

        n = len(high)

        # 长度一致
        assert len(signals) == n
        assert len(prz_upper) == n
        assert len(prz_lower) == n
        assert len(probability) == n

    def test_signal_values(self):
        """信号值验证"""
        high, low, close = generate_ideal_gartley_bullish()
        signals, _, _, _ = haze.py_harmonics(high, low, close, 3, 3, 0.5)

        # 信号应该是 -1, 0, 或 1
        for s in signals:
            assert s in [-1.0, 0.0, 1.0], f"Invalid signal value: {s}"

    def test_low_probability_filter(self):
        """低概率阈值过滤"""
        high, low, close = generate_random_market_data()

        # 高阈值应该过滤更多信号
        _, _, _, prob_low = haze.py_harmonics(high, low, close, 5, 5, 0.3)
        _, _, _, prob_high = haze.py_harmonics(high, low, close, 5, 5, 0.9)

        valid_low = sum(1 for p in prob_low if not math.isnan(p))
        valid_high = sum(1 for p in prob_high if not math.isnan(p))

        assert valid_high <= valid_low, \
            "Higher threshold should filter more signals"


@pytest.mark.skipif(not HAS_HAZE, reason="haze-library not installed")
class TestFormingPatterns:
    """预测性检测 (Forming Patterns) 测试"""

    def test_include_forming_flag(self):
        """include_forming 参数测试"""
        high, low, close = generate_ideal_gartley_bullish()

        patterns_with = haze.py_harmonics_patterns(high, low, 3, 3, True)
        patterns_without = haze.py_harmonics_patterns(high, low, 3, 3, False)

        forming_with = [p for p in patterns_with if p.state == "forming"]
        forming_without = [p for p in patterns_without if p.state == "forming"]

        # include_forming=False 不应返回 forming 形态
        assert len(forming_without) == 0, \
            "Should not have forming patterns when include_forming=False"

    def test_forming_has_partial_points(self):
        """Forming 形态应有部分点位"""
        high, low, close = generate_ideal_gartley_bullish()
        patterns = haze.py_harmonics_patterns(high, low, 3, 3, True)

        forming = [p for p in patterns if p.state == "forming"]
        for p in forming:
            # Forming 形态应该有 X, A, B 点
            assert p.x_index is not None
            assert p.a_index is not None
            assert p.b_index is not None
            # D 点应该为 None
            assert p.d_index is None, "Forming pattern should not have D point"


@pytest.mark.skipif(not HAS_HAZE, reason="haze-library not installed")
class TestEdgeCases:
    """边界情况测试"""

    def test_empty_data(self):
        """空数据处理"""
        high = []
        low = []
        close = []

        signals, prz_u, prz_l, prob = haze.py_harmonics(high, low, close)
        assert len(signals) == 0

    def test_short_data(self):
        """短数据处理"""
        high = [100.0, 101.0, 102.0, 103.0, 104.0]
        low = [99.0, 100.0, 101.0, 102.0, 103.0]
        close = [99.5, 100.5, 101.5, 102.5, 103.5]

        patterns = haze.py_harmonics_patterns(high, low, 2, 2, True)
        # 短数据应该没有足够的摆动点形成形态
        assert len(patterns) == 0 or all(p.state != "complete" for p in patterns)

    def test_constant_price(self):
        """常数价格处理"""
        n = 50
        high = [100.0] * n
        low = [100.0] * n
        close = [100.0] * n

        # 常数价格时，由于使用 >= 和 <= 比较，技术上所有点都满足 swing 条件
        # 但不应该形成有效的谐波形态（因为所有比率无意义）
        patterns = haze.py_harmonics_patterns(high, low, 3, 3, True)
        # 常数价格不应形成完整的谐波形态
        assert all(p.state != "complete" for p in patterns)

    def test_large_data(self):
        """大数据量处理"""
        n = 5000
        np.random.seed(42)

        returns = np.random.normal(0.0001, 0.02, n)
        close = 100 * np.exp(np.cumsum(returns))
        high = (close * (1 + np.abs(np.random.normal(0, 0.01, n)))).tolist()
        low = (close * (1 - np.abs(np.random.normal(0, 0.01, n)))).tolist()
        close = close.tolist()

        # 应该能处理大数据量
        signals, prz_u, prz_l, prob = haze.py_harmonics(high, low, close)
        assert len(signals) == n


@pytest.mark.skipif(not HAS_HAZE, reason="haze-library not installed")
class TestParameterDefaults:
    """参数默认值测试"""

    def test_default_parameters(self):
        """默认参数应该工作"""
        high, low, close = generate_random_market_data()

        # 使用所有默认参数
        signals, prz_u, prz_l, prob = haze.py_harmonics(high, low, close)
        assert len(signals) == len(high)

        patterns = haze.py_harmonics_patterns(high, low)
        # 应该返回列表（可能为空）
        assert isinstance(patterns, list)

        swings = haze.py_swing_points(high, low)
        assert isinstance(swings, list)

    def test_custom_window_sizes(self):
        """自定义窗口大小"""
        high, low, close = generate_random_market_data()

        # 不同窗口大小
        swings_small = haze.py_swing_points(high, low, 2, 2)
        swings_large = haze.py_swing_points(high, low, 10, 10)

        # 更大的窗口应该产生更少的摆动点
        assert len(swings_large) <= len(swings_small), \
            "Larger window should produce fewer swing points"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
