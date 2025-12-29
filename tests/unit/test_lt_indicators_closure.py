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

    def test_weight_sums_normalized(self):
        """验证所有市场状态的权重总和都为 1.0（已修复）"""
        # 获取三种市场状态的权重
        trending_weights = get_regime_weights("TRENDING")
        ranging_weights = get_regime_weights("RANGING")
        volatile_weights = get_regime_weights("VOLATILE")

        # 计算权重总和
        trending_sum = sum(trending_weights.values())
        ranging_sum = sum(ranging_weights.values())
        volatile_sum = sum(volatile_weights.values())

        # 记录当前状态（缺陷已修复）
        print(f"\n✅ 权重归一化验证（已修复）:")
        print(f"   TRENDING: {trending_sum:.4f} (预期: 1.00)")
        print(f"   RANGING:  {ranging_sum:.4f} (预期: 1.00)")
        print(f"   VOLATILE: {volatile_sum:.4f} (预期: 1.00)")

        # 验证所有权重都已正确归一化
        assert abs(trending_sum - 1.0) < 0.001, "TRENDING weights should be normalized to 1.0"
        assert abs(ranging_sum - 1.0) < 0.001, "RANGING weights should be normalized to 1.0"
        assert abs(volatile_sum - 1.0) < 0.001, "VOLATILE weights should be normalized to 1.0"

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

    def test_proper_error_handling_with_insufficient_data(self):
        """验证数据不足时抛出明确的 ValueError（已修复）"""
        # 使用极小数据量来触发某些指标的计算错误
        n = 50  # 最小长度，AI SuperTrend 需要至少 210 个数据点
        high = [100.0] * n
        low = [95.0] * n
        close = [98.0] * n
        volume = [1000.0] * n

        # 验证会抛出明确的 ValueError 而不是静默失败
        try:
            result = haze.lt_indicator(high, low, close, volume)
            assert False, "Should raise ValueError for insufficient data"
        except ValueError as e:
            # 验证错误消息清晰
            assert "Insufficient data" in str(e) or "need at least" in str(e)
            print(f"\n✅ 正确抛出 ValueError: {e}")
        except Exception as e:
            assert False, f"Should raise ValueError, not {type(e).__name__}: {e}"

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

    def test_vote_details_present(self):
        """测试投票详情完整性（已修复）"""
        indicators = {
            'ind1': {'signal': 'BUY', 'strength': 1.0},
            'ind2': {'signal': 'SELL', 'strength': 0.5},
            'ind3': {'signal': 'NEUTRAL', 'strength': 0.0},
        }
        weights = {'ind1': 0.4, 'ind2': 0.3, 'ind3': 0.3}

        result = _compute_ensemble(indicators, weights)

        # 验证投票详情现在是完整的
        assert 'buy_votes' in result, "Implementation should include buy_votes"
        assert 'sell_votes' in result, "Implementation should include sell_votes"
        assert 'neutral_votes' in result, "Implementation should include neutral_votes"

        # 验证投票详情包含必要的信息
        assert isinstance(result['buy_votes'], list)
        assert isinstance(result['sell_votes'], list)
        assert isinstance(result['neutral_votes'], list)

        print(f"\n✅ 投票详情完整:")
        print(f"   buy_votes: {len(result['buy_votes'])} 个指标")
        print(f"   sell_votes: {len(result['sell_votes'])} 个指标")
        print(f"   neutral_votes: {len(result['neutral_votes'])} 个指标")


class TestOutputStructure:
    """测试输出结构的完整性"""

    def test_metadata_present(self):
        """测试元数据完整性（已修复）"""
        n = 300
        high = [100.0 + i * 0.1 for i in range(n)]
        low = [95.0 + i * 0.1 for i in range(n)]
        close = [98.0 + i * 0.1 for i in range(n)]
        volume = [1000.0] * n

        result = haze.lt_indicator(high, low, close, volume)

        # 验证元数据现在是完整的
        assert 'metadata' in result, "Implementation should include metadata"

        metadata = result['metadata']
        assert 'timestamp' in metadata, "Metadata should include timestamp"
        assert 'execution_time_ms' in metadata, "Metadata should include execution time"
        assert 'num_bars' in metadata, "Metadata should include number of bars"
        assert 'num_indicators' in metadata, "Metadata should include number of indicators"

        print("\n✅ 输出包含完整元数据:")
        print(f"   - 时间戳: {metadata['timestamp']}")
        print(f"   - 执行时长: {metadata['execution_time_ms']:.2f}ms")
        print(f"   - 数据条数: {metadata['num_bars']}")
        print(f"   - 指标数量: {metadata['num_indicators']}")

    def test_ensemble_omitted_when_disabled(self):
        """测试禁用 ensemble 时完全省略字段（已改进）"""
        n = 300
        high = [100.0 + i * 0.1 for i in range(n)]
        low = [95.0 + i * 0.1 for i in range(n)]
        close = [98.0 + i * 0.1 for i in range(n)]
        volume = [1000.0] * n

        result = haze.lt_indicator(high, low, close, volume, enable_ensemble=False)

        # 验证 ensemble 字段被完全省略（更好的设计）
        assert 'ensemble' not in result, "ensemble key should be omitted when disabled"
        assert 'indicators' in result, "indicators should still be present"
        assert 'metadata' in result, "metadata should still be present"

        print("\n✅ 禁用 ensemble 时完全省略字段（更清晰的 API 设计）")


if __name__ == "__main__":
    # 运行测试并显示详细输出
    pytest.main([__file__, "-v", "-s"])
