#!/usr/bin/env python3
"""
市场状态感知测试
测试LT指标的自动市场状态检测和动态权重调整功能

这是haze库的增强特性，超出SFG原始PDF规范，提供全自动的市场状态识别。
"""

import haze_library as haze
import math


def generate_trending_market(n=500):
    """生成趋势市场数据：强势上涨 + 高ADX + 大价格区间"""
    close = []
    high = []
    low = []
    volume = []

    for i in range(n):
        # 持续上涨趋势
        trend = 100.0 + i * 0.2
        noise = math.sin(i * 0.1) * 1.0  # 小幅噪音

        c = trend + noise
        close.append(c)
        high.append(c + 2.0)
        low.append(c - 1.5)

        # 趋势中成交量稳定放大
        volume.append(1000.0 + i * 3.0)

    return high, low, close, volume


def generate_ranging_market(n=500):
    """生成震荡市场数据：在区间内来回波动 + 低ADX + 小价格区间"""
    close = []
    high = []
    low = []
    volume = []

    base = 100.0
    range_size = 10.0

    for i in range(n):
        # 在100-110之间震荡
        c = base + range_size / 2 + (range_size / 2) * math.sin(i * 0.15)
        close.append(c)
        high.append(c + 1.0)
        low.append(c - 1.0)

        # 成交量波动
        volume.append(1000.0 + 200.0 * abs(math.sin(i * 0.2)))

    return high, low, close, volume


def generate_volatile_market(n=500):
    """生成高波动市场数据：剧烈波动 + 高ATR"""
    close = []
    high = []
    low = []
    volume = []

    for i in range(n):
        # 基础价格
        base = 100.0 + i * 0.05

        # 剧烈波动
        volatility = 10.0 * math.sin(i * 0.3)
        c = base + volatility

        close.append(c)
        high.append(c + abs(volatility) * 0.5)
        low.append(c - abs(volatility) * 0.5)

        # 波动时成交量激增
        volume.append(1000.0 + abs(volatility) * 100.0)

    return high, low, close, volume


def print_regime_analysis(market_name, signals):
    """打印市场状态分析结果"""
    print(f"\n{'='*80}")
    print(f"📊 {market_name}")
    print(f"{'='*80}")

    # 检查是否检测到市场状态
    if 'market_regime' in signals:
        regime = signals['market_regime']
        print(f"\n🎯 检测到的市场状态: {regime}")

        # 显示状态说明
        regime_desc = {
            'TRENDING': '趋势市场 - ADX > 25 且 价格区间 > 15%',
            'RANGING': '震荡市场 - 低ADX 且 小价格区间',
            'VOLATILE': '高波动市场 - ATR% > 5%'
        }
        print(f"   定义: {regime_desc.get(regime, '未知')}")
    else:
        print("\n⚠️  未启用自动市场状态检测")

    # 显示Ensemble结果
    ensemble = signals['ensemble']
    print(f"\n📈 Ensemble集成信号:")
    print(f"   最终信号:     {ensemble['final_signal']:>10}")
    print(f"   置信度:       {ensemble['confidence']:>10.2%}")
    print(f"   Buy权重:      {ensemble['buy_weight']:>10.2%}")
    print(f"   Sell权重:     {ensemble['sell_weight']:>10.2%}")
    print(f"   投票统计:     BUY={ensemble['vote_summary']['buy']}  "
          f"SELL={ensemble['vote_summary']['sell']}  "
          f"NEUTRAL={ensemble['vote_summary']['neutral']}")

    # 显示各指标信号
    print(f"\n{'='*80}")
    print(f"📊 各指标信号详情")
    print(f"{'='*80}")

    indicators = signals['indicators']

    # 分类统计
    buy_indicators = []
    sell_indicators = []
    neutral_indicators = []

    for name, ind in indicators.items():
        signal = ind['signal']
        strength = ind['strength']

        if signal == 'BUY':
            buy_indicators.append((name, strength))
        elif signal == 'SELL':
            sell_indicators.append((name, strength))
        else:
            neutral_indicators.append((name, strength))

    # 按强度排序显示
    if buy_indicators:
        print(f"\n🟢 BUY信号 ({len(buy_indicators)}个):")
        for name, strength in sorted(buy_indicators, key=lambda x: x[1], reverse=True):
            print(f"   • {name:25} 强度: {strength:.2%}")

    if sell_indicators:
        print(f"\n🔴 SELL信号 ({len(sell_indicators)}个):")
        for name, strength in sorted(sell_indicators, key=lambda x: x[1], reverse=True):
            print(f"   • {name:25} 强度: {strength:.2%}")

    if neutral_indicators:
        print(f"\n⚪ NEUTRAL ({len(neutral_indicators)}个):")
        for name, strength in sorted(neutral_indicators, key=lambda x: x[1], reverse=True):
            print(f"   • {name:25} 强度: {strength:.2%}")


def test_trending_market():
    """测试趋势市场的自动检测"""
    print("\n" + "╔" + "="*78 + "╗")
    print("║" + " "*22 + "测试1: 趋势市场自动检测" + " "*22 + "║")
    print("╚" + "="*78 + "╝")

    high, low, close, volume = generate_trending_market(500)

    print(f"\n📊 市场特征:")
    print(f"   价格范围: {min(close):.2f} → {max(close):.2f}")
    print(f"   涨幅: {((max(close) - min(close)) / min(close) * 100):.2f}%")
    print(f"   K线数量: {len(close)}")

    # 启用自动市场状态检测
    signals = haze.lt_indicator(high, low, close, volume, auto_regime=True)

    print_regime_analysis("趋势市场", signals)

    return signals


def test_ranging_market():
    """测试震荡市场的自动检测"""
    print("\n" + "╔" + "="*78 + "╗")
    print("║" + " "*22 + "测试2: 震荡市场自动检测" + " "*22 + "║")
    print("╚" + "="*78 + "╝")

    high, low, close, volume = generate_ranging_market(500)

    print(f"\n📊 市场特征:")
    print(f"   价格范围: {min(close):.2f} → {max(close):.2f}")
    print(f"   区间大小: {((max(close) - min(close)) / min(close) * 100):.2f}%")
    print(f"   K线数量: {len(close)}")

    # 启用自动市场状态检测
    signals = haze.lt_indicator(high, low, close, volume, auto_regime=True)

    print_regime_analysis("震荡市场", signals)

    return signals


def test_volatile_market():
    """测试高波动市场的自动检测"""
    print("\n" + "╔" + "="*78 + "╗")
    print("║" + " "*22 + "测试3: 高波动市场自动检测" + " "*22 + "║")
    print("╚" + "="*78 + "╝")

    high, low, close, volume = generate_volatile_market(500)

    print(f"\n📊 市场特征:")
    print(f"   价格范围: {min(close):.2f} → {max(close):.2f}")
    print(f"   波动幅度: {((max(close) - min(close)) / min(close) * 100):.2f}%")
    print(f"   K线数量: {len(close)}")

    # 启用自动市场状态检测
    signals = haze.lt_indicator(high, low, close, volume, auto_regime=True)

    print_regime_analysis("高波动市场", signals)

    return signals


def test_manual_regime_override():
    """测试手动指定市场状态"""
    print("\n" + "╔" + "="*78 + "╗")
    print("║" + " "*20 + "测试4: 手动指定市场状态" + " "*20 + "║")
    print("╚" + "="*78 + "╝")

    # 使用趋势数据
    high, low, close, volume = generate_trending_market(500)

    print("\n📌 场景：趋势市场数据 + 手动强制指定为RANGING")

    # 手动指定为震荡市场（即使数据是趋势）
    signals = haze.lt_indicator(high, low, close, volume, regime="RANGING")

    print_regime_analysis("手动指定市场状态", signals)

    return signals


def test_disable_auto_regime():
    """测试禁用自动检测"""
    print("\n" + "╔" + "="*78 + "╗")
    print("║" + " "*20 + "测试5: 禁用自动市场状态检测" + " "*18 + "║")
    print("╚" + "="*78 + "╝")

    high, low, close, volume = generate_trending_market(500)

    print("\n📌 场景：使用默认权重（不检测市场状态）")

    # 禁用自动检测
    signals = haze.lt_indicator(high, low, close, volume, auto_regime=False)

    print_regime_analysis("禁用自动检测", signals)

    return signals


def compare_auto_vs_manual():
    """对比自动检测 vs 默认权重的效果"""
    print("\n" + "╔" + "="*78 + "╗")
    print("║" + " "*18 + "对比：自动检测 vs 默认权重" + " "*18 + "║")
    print("╚" + "="*78 + "╝")

    # 使用同一组趋势数据
    high, low, close, volume = generate_trending_market(500)

    # 方案1：自动检测
    auto_signals = haze.lt_indicator(high, low, close, volume, auto_regime=True)

    # 方案2：默认权重
    manual_signals = haze.lt_indicator(high, low, close, volume, auto_regime=False)

    print(f"\n{'='*80}")
    print("📊 对比结果")
    print(f"{'='*80}")

    print("\n方案1: 自动市场状态检测")
    print(f"   检测状态: {auto_signals.get('market_regime', 'N/A')}")
    print(f"   最终信号: {auto_signals['ensemble']['final_signal']}")
    print(f"   置信度:   {auto_signals['ensemble']['confidence']:.2%}")
    print(f"   投票:     BUY={auto_signals['ensemble']['vote_summary']['buy']} "
          f"SELL={auto_signals['ensemble']['vote_summary']['sell']} "
          f"NEUTRAL={auto_signals['ensemble']['vote_summary']['neutral']}")

    print("\n方案2: 默认权重（无状态检测）")
    print(f"   检测状态: {manual_signals.get('market_regime', 'N/A')}")
    print(f"   最终信号: {manual_signals['ensemble']['final_signal']}")
    print(f"   置信度:   {manual_signals['ensemble']['confidence']:.2%}")
    print(f"   投票:     BUY={manual_signals['ensemble']['vote_summary']['buy']} "
          f"SELL={manual_signals['ensemble']['vote_summary']['sell']} "
          f"NEUTRAL={manual_signals['ensemble']['vote_summary']['neutral']}")

    print(f"\n{'='*80}")
    print("✅ 差异分析")
    print(f"{'='*80}")

    conf_diff = auto_signals['ensemble']['confidence'] - manual_signals['ensemble']['confidence']
    print(f"   置信度差异: {conf_diff:+.2%}")

    vote_diff_buy = (auto_signals['ensemble']['vote_summary']['buy'] -
                     manual_signals['ensemble']['vote_summary']['buy'])
    print(f"   BUY信号差异: {vote_diff_buy:+d}")

    if conf_diff > 0:
        print(f"\n   → 自动检测提高了 {abs(conf_diff):.2%} 的置信度")
    elif conf_diff < 0:
        print(f"\n   → 默认权重提高了 {abs(conf_diff):.2%} 的置信度")
    else:
        print(f"\n   → 两种方法置信度相同")


def run_all_tests():
    """运行所有测试"""
    print("\n" + "╔" + "="*78 + "╗")
    print("║" + " "*15 + "市场状态感知功能全面测试" + " "*15 + "║")
    print("║" + " "*10 + "(haze库增强特性 - 超出SFG原始PDF规范)" + " "*10 + "║")
    print("╚" + "="*78 + "╝")

    results = {}

    # 测试1: 趋势市场
    results['trending'] = test_trending_market()

    # 测试2: 震荡市场
    results['ranging'] = test_ranging_market()

    # 测试3: 高波动市场
    results['volatile'] = test_volatile_market()

    # 测试4: 手动指定
    results['manual'] = test_manual_regime_override()

    # 测试5: 禁用自动检测
    results['disabled'] = test_disable_auto_regime()

    # 对比分析
    compare_auto_vs_manual()

    # 总结
    print("\n" + "╔" + "="*78 + "╗")
    print("║" + " "*28 + "📊 测试总结" + " "*28 + "║")
    print("╚" + "="*78 + "╝")

    print(f"\n{'测试场景':<20} {'检测状态':<15} {'最终信号':<12} {'置信度':<10}")
    print("="*80)

    for test_name, result in results.items():
        regime = result.get('market_regime', 'N/A')
        final_signal = result['ensemble']['final_signal']
        confidence = result['ensemble']['confidence']

        print(f"{test_name:<20} {regime:<15} {final_signal:<12} {confidence:<10.2%}")

    print(f"\n{'='*80}")
    print("🎯 关键发现:")
    print(f"{'='*80}")

    # 验证检测准确性
    if results['trending'].get('market_regime') == 'TRENDING':
        print("✅ 趋势市场检测正确")
    else:
        print("⚠️  趋势市场检测异常")

    if results['ranging'].get('market_regime') == 'RANGING':
        print("✅ 震荡市场检测正确")
    else:
        print("⚠️  震荡市场检测异常")

    if results['volatile'].get('market_regime') in ['VOLATILE', 'RANGING']:
        print("✅ 高波动市场检测合理（VOLATILE或RANGING）")
    else:
        print("⚠️  高波动市场检测异常")

    print(f"\n{'='*80}")
    print("🚀 市场状态感知功能测试完成！")
    print("="*80)

    print("\n💡 使用建议:")
    print("   1. 默认启用auto_regime=True，让系统自动适配市场")
    print("   2. 如需手动控制，可指定regime='TRENDING'|'RANGING'|'VOLATILE'")
    print("   3. 如需使用固定权重，设置auto_regime=False")


if __name__ == "__main__":
    run_all_tests()
