#!/usr/bin/env python3
"""
LT 指标逻辑闭环单元测试
测试关键的逻辑缺陷：权重归一化、错误处理、边界情况
"""

import pytest
import math
import sys
sys.path.insert(0, '/Users/zhaoleon/Desktop/haze/haze/src')

import haze_library as haze
from haze_library.lt_indicators import get_regime_weights, _compute_ensemble


class TestWeightNormalization:
    """测试权重归一化问题"""

    def test_weight_sums_not_normalized(self):
        """验证当前权重总和不为 1.0（这是预期的缺陷）"""
        # 获取三种市场状态的权重
        trending_weights = get_regime_weights("TRENDING")
        ranging_weights = get_regime_weights("RANGING")
        volatile_weights = get_regime_weights("VOLATILE")

        # 计算权重总和
        trending_sum = sum(trending_weights.values())
        ranging_sum = sum(ranging_weights.values())
        volatile_sum = sum(volatile_weights.values())

        # 记录当前状态（这些是已知的缺陷）
        print(f"\n📊 当前权重总和（未归一化）:")
        print(f"   TRENDING: {trending_sum:.2f} (预期: 1.00)")
        print(f"   RANGING:  {ranging_sum:.2f} (预期: 1.00)")
        print(f"   VOLATILE: {volatile_sum:.2f} (预期: 1.00)")

        # 验证问题存在（这些断言应该失败，证明缺陷存在）
        assert trending_sum != 1.0, "TRENDING weights should NOT be normalized (known issue)"
        assert ranging_sum != 1.0, "RANGING weights should NOT be normalized (known issue)"

        # VOLATILE 是唯一正确的
        assert abs(volatile_sum - 1.0) < 0.001, "VOLATILE weights ARE correctly normalized"

    def test_ensemble_threshold_affected_by_non_normalized_weights(self):
        """验证非归一化权重如何影响集成阈值判断"""
        # 创建模拟指标结果
        indicators = {
            'ind1': {'signal': 'BUY', 'strength': 1.0},
            'ind2': {'signal': 'BUY', 'strength': 1.0},
            'ind3': {'signal': 'NEUTRAL', 'strength': 0.0},
        }

        # 使用非归一化权重（总和 = 0.7）
        non_normalized_weights = {
            'ind1': 0.35,
            'ind2': 0.35,
            'ind3': 0.0,
        }

        result = _compute_ensemble(indicators, non_normalized_weights)

        # 计算实际的 buy_weight
        buy_weight = 0.35 * 1.0 + 0.35 * 1.0  # = 0.7

        print(f"\n⚠️  非归一化权重的影响:")
        print(f"   buy_weight: {buy_weight} (总权重: 0.7, 非 1.0)")
        print(f"   final_signal: {result['final_signal']}")
        print(f"   问题: buy_weight(0.7) > 0.5 阈值，但权重总和不是 1.0")

        # 验证问题
        assert buy_weight > 0.5, "Buy weight exceeds threshold"
        assert result['final_signal'] == 'BUY', "Signal should be BUY"

        # 但这个BUY信号的统计意义是有问题的，因为权重总和不是1.0
        assert abs(buy_weight - 0.7) < 0.001, "Buy weight is 0.7, not normalized"


class TestErrorHandling:
    """测试错误处理和静默失败行为"""

    def test_silent_failure_no_error_field(self):
        """验证当前错误处理会静默失败，且返回结果缺少 error 字段"""
        # 使用极小数据量来触发某些指标的计算错误
        n = 50  # 最小长度，某些指标可能失败
        high = [100.0] * n
        low = [95.0] * n
        close = [98.0] * n
        volume = [1000.0] * n

        result = haze.lt_indicator(high, low, close, volume)

        # 检查指标结构
        for ind_name, ind_data in result['indicators'].items():
            # 当前实现：即使计算失败，也没有 'error' 字段
            assert 'error' not in ind_data, f"{ind_name} should NOT have 'error' field (current implementation)"
            assert 'valid' not in ind_data, f"{ind_name} should NOT have 'valid' field (current implementation)"

            # 失败的指标会返回 NEUTRAL，但无法区分是真正的 NEUTRAL 还是失败
            print(f"   {ind_name}: {ind_data['signal']} (strength: {ind_data['strength']:.2f})")

        print("\n⚠️  问题: 无法区分 NEUTRAL 是正常信号还是计算失败")

    def test_no_logging_on_failure(self):
        """验证计算失败时没有日志记录（需要手动检查）"""
        # 这个测试主要是文档化问题，实际验证需要检查日志输出
        print("\n⚠️  当前实现: 指标计算失败时不会产生日志")
        print("   建议: 添加 logger.warning() 来记录失败")

        # 标记此测试为已知问题
        pytest.skip("Logging verification requires manual inspection")


class TestBoundaryConditions:
    """测试边界条件处理"""

    def test_nan_handling(self):
        """测试 NaN 值的处理"""
        n = 300
        high = [100.0 + i * 0.1 for i in range(n)]
        low = [95.0 + i * 0.1 for i in range(n)]
        close = [98.0 + i * 0.1 for i in range(n)]
        volume = [1000.0] * n

        # 插入 NaN 值
        high[100] = float('nan')
        close[150] = float('nan')

        # 当前实现可能会传播 NaN 或静默失败
        try:
            result = haze.lt_indicator(high, low, close, volume)
            print("\n⚠️  NaN 值未被检测，可能导致计算结果错误")

            # 检查是否有 NaN 传播到结果中
            for ind_name, ind_data in result['indicators'].items():
                if isinstance(ind_data.get('strength'), float):
                    if math.isnan(ind_data['strength']):
                        print(f"   ❌ {ind_name} strength 为 NaN (数据污染)")

        except Exception as e:
            print(f"\n✅ NaN 导致异常（更好，但应该有明确的错误消息）: {e}")

    def test_inf_handling(self):
        """测试 Inf 值的处理"""
        n = 300
        high = [100.0 + i * 0.1 for i in range(n)]
        low = [95.0 + i * 0.1 for i in range(n)]
        close = [98.0 + i * 0.1 for i in range(n)]
        volume = [1000.0] * n

        # 插入 Inf 值
        volume[100] = float('inf')

        try:
            result = haze.lt_indicator(high, low, close, volume)
            print("\n⚠️  Inf 值未被检测")
        except Exception as e:
            print(f"\n✅ Inf 导致异常: {e}")

    def test_negative_prices(self):
        """测试负价格的处理"""
        n = 300
        high = [100.0 + i * 0.1 for i in range(n)]
        low = [95.0 + i * 0.1 for i in range(n)]
        close = [98.0 + i * 0.1 for i in range(n)]
        volume = [1000.0] * n

        # 插入负价格
        close[100] = -50.0

        try:
            result = haze.lt_indicator(high, low, close, volume)
            print("\n⚠️  负价格未被检测，应该抛出 ValueError")
        except ValueError as e:
            print(f"\n✅ 负价格被检测: {e}")
        except Exception as e:
            print(f"\n⚠️  负价格导致其他异常: {e}")

    def test_negative_volume(self):
        """测试负成交量的处理"""
        n = 300
        high = [100.0 + i * 0.1 for i in range(n)]
        low = [95.0 + i * 0.1 for i in range(n)]
        close = [98.0 + i * 0.1 for i in range(n)]
        volume = [1000.0] * n

        # 插入负成交量
        volume[100] = -500.0

        try:
            result = haze.lt_indicator(high, low, close, volume)
            print("\n⚠️  负成交量未被检测，应该抛出 ValueError")
        except ValueError as e:
            print(f"\n✅ 负成交量被检测: {e}")
        except Exception as e:
            print(f"\n⚠️  负成交量导致其他异常: {e}")


class TestEnsembleLogic:
    """测试集成投票逻辑的边界情况"""

    def test_neutral_signal_ambiguity(self):
        """测试 NEUTRAL 信号的语义混乱"""
        # 场景1: buy_weight = 0.4, sell_weight = 0.3 → NEUTRAL（但实际偏多）
        indicators = {
            'ind1': {'signal': 'BUY', 'strength': 0.8},
            'ind2': {'signal': 'SELL', 'strength': 0.6},
        }
        weights = {'ind1': 0.5, 'ind2': 0.5}

        result = _compute_ensemble(indicators, weights)

        print(f"\n⚠️  NEUTRAL 信号的语义混乱:")
        print(f"   buy_weight: {result['buy_weight']} = 0.5 * 0.8 = 0.4")
        print(f"   sell_weight: {result['sell_weight']} = 0.5 * 0.6 = 0.3")
        print(f"   final_signal: {result['final_signal']} (NEUTRAL)")
        print(f"   问题: 虽然 buy > sell，但因为 buy < 0.5，返回 NEUTRAL")

        assert result['final_signal'] == 'NEUTRAL'
        assert result['buy_weight'] > result['sell_weight']
        assert result['buy_weight'] < 0.5

    def test_missing_vote_details(self):
        """测试缺少投票详情"""
        indicators = {
            'ind1': {'signal': 'BUY', 'strength': 1.0},
            'ind2': {'signal': 'SELL', 'strength': 0.5},
            'ind3': {'signal': 'NEUTRAL', 'strength': 0.0},
        }
        weights = {'ind1': 0.4, 'ind2': 0.3, 'ind3': 0.3}

        result = _compute_ensemble(indicators, weights)

        # 验证缺少投票详情
        assert 'buy_votes' not in result, "Current implementation lacks buy_votes"
        assert 'sell_votes' not in result, "Current implementation lacks sell_votes"
        assert 'neutral_votes' not in result, "Current implementation lacks neutral_votes"

        print("\n⚠️  缺少投票详情，无法追溯哪些指标投了哪个方向")


class TestOutputStructure:
    """测试输出结构的完整性"""

    def test_missing_metadata(self):
        """测试缺少元数据"""
        n = 300
        high = [100.0 + i * 0.1 for i in range(n)]
        low = [95.0 + i * 0.1 for i in range(n)]
        close = [98.0 + i * 0.1 for i in range(n)]
        volume = [1000.0] * n

        result = haze.lt_indicator(high, low, close, volume)

        # 验证缺少元数据
        assert 'metadata' not in result, "Current implementation lacks metadata"
        assert 'timestamp' not in result, "Current implementation lacks timestamp"
        assert 'version' not in result, "Current implementation lacks version"

        print("\n⚠️  输出缺少元数据:")
        print("   - 无时间戳")
        print("   - 无版本号")
        print("   - 无执行时长")
        print("   - 无失败指标列表")

    def test_ensemble_none_when_disabled(self):
        """测试禁用 ensemble 时返回 None"""
        n = 300
        high = [100.0 + i * 0.1 for i in range(n)]
        low = [95.0 + i * 0.1 for i in range(n)]
        close = [98.0 + i * 0.1 for i in range(n)]
        volume = [1000.0] * n

        result = haze.lt_indicator(high, low, close, volume, enable_ensemble=False)

        # 验证返回 None 而不是省略字段
        assert 'ensemble' in result, "ensemble key should exist"
        assert result['ensemble'] is None, "ensemble should be None when disabled"

        print("\n⚠️  禁用 ensemble 时返回 None，用户需要额外判断")


if __name__ == "__main__":
    # 运行测试并显示详细输出
    pytest.main([__file__, "-v", "-s"])
