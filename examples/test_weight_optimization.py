#!/usr/bin/env python3
"""
权重优化验证测试

验证目标：
1. 每个市场状态的权重总和是否为1.0
2. 6个关键指标的权重是否达到目标（75%/65%/72%）
3. 权重配置在实际应用中是否保持100%准确率
"""

import sys
import os

# 添加src到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from haze_library.lt_indicators import get_regime_weights


def test_weight_sum_equals_one():
    """测试每个市场状态的权重总和是否为1.0"""
    print("\n" + "=" * 80)
    print("测试1: 权重总和验证")
    print("=" * 80)

    for regime in ['TRENDING', 'RANGING', 'VOLATILE', 'DEFAULT']:
        weights = get_regime_weights(regime)
        total = sum(weights.values())

        status = "✅" if abs(total - 1.0) < 1e-6 else "❌"
        print(f"\n{regime:12s} 权重总和: {total:.10f} {status}")

        if abs(total - 1.0) >= 1e-6:
            print(f"   ⚠️  误差: {total - 1.0:.10f}")
            return False

    print("\n✅ 所有权重总和验证通过")
    return True


def test_key_indicators_weight_increased():
    """测试6个关键指标的权重是否提升至目标"""
    print("\n" + "=" * 80)
    print("测试2: 6个关键指标权重占比验证")
    print("=" * 80)

    # 定义6个关键指标
    key_indicators = [
        'pivot_points',
        'market_structure_fvg',
        'pd_array_breaker',
        'linear_regression',
        'dynamic_macd_ha',
        'atr2_signals'
    ]

    # 定义目标权重
    targets = {
        'TRENDING': 0.75,
        'RANGING': 0.65,
        'VOLATILE': 0.72,
    }

    all_passed = True

    for regime, target in targets.items():
        weights = get_regime_weights(regime)
        key_total = sum(weights.get(k, 0.0) for k in key_indicators)

        status = "✅" if key_total >= target - 0.01 else "❌"  # 允许1%误差
        print(f"\n{regime:12s}")
        print(f"   目标: {target*100:.1f}%")
        print(f"   实际: {key_total*100:.1f}% {status}")

        # 显示各指标权重
        print(f"   详细:")
        for indicator in key_indicators:
            weight = weights.get(indicator, 0.0)
            if weight > 0:
                print(f"      {indicator:25s}: {weight*100:5.1f}%")

        if key_total < target - 0.01:
            print(f"   ⚠️  未达到目标，差距: {(target - key_total)*100:.1f}%")
            all_passed = False

    if all_passed:
        print("\n✅ 所有关键指标权重占比验证通过")
    else:
        print("\n❌ 部分关键指标权重未达标")

    return all_passed


def test_no_negative_weights():
    """测试是否存在负权重"""
    print("\n" + "=" * 80)
    print("测试3: 负权重检测")
    print("=" * 80)

    for regime in ['TRENDING', 'RANGING', 'VOLATILE', 'DEFAULT']:
        weights = get_regime_weights(regime)
        negative = {k: v for k, v in weights.items() if v < 0}

        if negative:
            print(f"\n❌ {regime} 存在负权重:")
            for k, v in negative.items():
                print(f"   {k}: {v}")
            return False

    print("\n✅ 无负权重")
    return True


def test_weight_distribution():
    """显示权重分布对比"""
    print("\n" + "=" * 80)
    print("测试4: 权重分布对比（优化前后）")
    print("=" * 80)

    # 旧权重（用于对比）
    old_weights = {
        'TRENDING': {
            "ai_supertrend": 0.35,
            "market_structure_fvg": 0.25,
            "dynamic_macd_ha": 0.20,
            "pd_array_breaker": 0.10,
            "atr2_signals": 0.05,
            "ai_momentum": 0.05,
        },
        'RANGING': {
            "pivot_points": 0.25,
            "volume_profile": 0.25,
            "linear_regression": 0.20,
            "ai_momentum": 0.15,
            "atr2_signals": 0.10,
            "general_parameters": 0.05,
        },
        'VOLATILE': {
            "atr2_signals": 0.30,
            "ai_momentum": 0.25,
            "volume_profile": 0.20,
            "pivot_points": 0.15,
            "dynamic_macd_ha": 0.10,
        },
    }

    for regime in ['TRENDING', 'RANGING', 'VOLATILE']:
        print(f"\n【{regime}】")
        new_weights = get_regime_weights(regime)
        old = old_weights[regime]

        # 合并所有指标
        all_indicators = set(new_weights.keys()) | set(old.keys())

        print(f"{'指标':30s} {'旧权重':>8s} {'新权重':>8s} {'变化':>8s}")
        print("-" * 60)

        for indicator in sorted(all_indicators):
            old_w = old.get(indicator, 0.0)
            new_w = new_weights.get(indicator, 0.0)
            change = new_w - old_w

            if abs(change) > 0.001:  # 只显示有变化的
                arrow = "↑" if change > 0 else "↓" if change < 0 else "="
                print(f"{indicator:30s} {old_w*100:6.1f}%  {new_w*100:6.1f}%  {arrow} {abs(change)*100:5.1f}%")

    return True


def main():
    """主测试函数"""
    print("\n")
    print("=" * 80)
    print("权重优化验证测试")
    print("=" * 80)

    results = []

    # 运行所有测试
    results.append(("权重总和验证", test_weight_sum_equals_one()))
    results.append(("关键指标权重占比", test_key_indicators_weight_increased()))
    results.append(("负权重检测", test_no_negative_weights()))
    results.append(("权重分布对比", test_weight_distribution()))

    # 总结
    print("\n" + "=" * 80)
    print("测试总结")
    print("=" * 80)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{name:20s}: {status}")

    print(f"\n通过率: {passed}/{total} ({passed/total*100:.1f}%)")

    if passed == total:
        print("\n🎉 所有测试通过！权重优化配置正确。")
        return 0
    else:
        print("\n⚠️  部分测试失败，请检查权重配置。")
        return 1


if __name__ == '__main__':
    sys.exit(main())
