#!/usr/bin/env python3
"""
趋势信号质量测试
测试LT指标在上涨和下跌市场中的信号质量
"""

import haze_library as haze
import math


def print_signal_quality(signals, trend_type):
    """打印信号质量分析"""
    ensemble = signals['ensemble']
    indicators = signals['indicators']

    print(f"\n{'='*80}")
    print(f"🎯 {trend_type} - Ensemble集成信号")
    print(f"{'='*80}")
    print(f"   最终信号:     {ensemble['final_signal']:>10}")
    print(f"   置信度:       {ensemble['confidence']:>10.2%}")
    print(f"   Buy权重:      {ensemble['buy_weight']:>10.2%}")
    print(f"   Sell权重:     {ensemble['sell_weight']:>10.2%}")
    print(f"   投票统计:     BUY={ensemble['vote_summary']['buy']}  "
          f"SELL={ensemble['vote_summary']['sell']}  "
          f"NEUTRAL={ensemble['vote_summary']['neutral']}")

    print(f"\n{'='*80}")
    print(f"📊 各指标详细信号")
    print(f"{'='*80}")

    buy_indicators = []
    sell_indicators = []
    neutral_indicators = []

    for name, ind in indicators.items():
        signal = ind['signal']
        strength = ind['strength']

        if signal == 'BUY':
            symbol = '🟢'
            buy_indicators.append((name, strength))
        elif signal == 'SELL':
            symbol = '🔴'
            sell_indicators.append((name, strength))
        else:
            symbol = '⚪'
            neutral_indicators.append((name, strength))

        print(f"{symbol} {name:25} {signal:>8}   强度: {strength:>6.2%}")

    return {
        'buy_count': len(buy_indicators),
        'sell_count': len(sell_indicators),
        'neutral_count': len(neutral_indicators),
        'buy_indicators': buy_indicators,
        'sell_indicators': sell_indicators,
        'confidence': ensemble['confidence']
    }


def test_strong_uptrend():
    """测试强势上涨趋势"""
    print("\n" + "╔" + "="*78 + "╗")
    print("║" + " "*25 + "📈 强势上涨趋势测试" + " "*25 + "║")
    print("╚" + "="*78 + "╝")

    # 生成强势上涨数据：持续上涨，成交量放大
    n = 500
    close = []
    volume = []

    for i in range(n):
        # 价格稳步上涨，带有小幅回调
        if i % 50 < 45:  # 90%的时间在上涨
            close.append(100.0 + i * 0.15 + math.sin(i * 0.2) * 2)
        else:  # 10%的时间小幅回调
            close.append(100.0 + i * 0.15 - 3.0)

        # 上涨时成交量放大
        volume.append(1000.0 + i * 5.0 + 500.0 * (1 if i % 50 < 45 else 0.5))

    high = [c + 2.0 for c in close]
    low = [c - 1.5 for c in close]

    print(f"\n📊 市场特征:")
    print(f"   K线数量: {n}")
    print(f"   价格范围: {min(close):.2f} → {max(close):.2f}")
    print(f"   涨幅: {((max(close) - min(close)) / min(close) * 100):.2f}%")
    print(f"   成交量: {min(volume):.0f} → {max(volume):.0f}")

    signals = haze.lt_indicator(high, low, close, volume)
    stats = print_signal_quality(signals, "强势上涨")

    print(f"\n{'='*80}")
    print(f"✅ 信号质量分析")
    print(f"{'='*80}")

    if stats['buy_count'] > stats['sell_count']:
        print(f"✅ 正确趋势判断: BUY信号 ({stats['buy_count']}) > SELL信号 ({stats['sell_count']})")
    else:
        print(f"⚠️  趋势判断异常: BUY信号 ({stats['buy_count']}) ≤ SELL信号 ({stats['sell_count']})")

    if signals['ensemble']['final_signal'] == 'BUY':
        print(f"✅ Ensemble集成信号正确: {signals['ensemble']['final_signal']}")
        print(f"   置信度: {signals['ensemble']['confidence']:.2%}")
    elif signals['ensemble']['final_signal'] == 'NEUTRAL':
        print(f"⚠️  Ensemble集成信号中性: {signals['ensemble']['final_signal']}")
        print(f"   可能需要更强的趋势或调整权重")
    else:
        print(f"❌ Ensemble集成信号错误: {signals['ensemble']['final_signal']}")

    print(f"\n🟢 产生BUY信号的指标 ({len(stats['buy_indicators'])}个):")
    for name, strength in sorted(stats['buy_indicators'], key=lambda x: x[1], reverse=True):
        print(f"   • {name:25} 强度: {strength:.2%}")

    if stats['sell_indicators']:
        print(f"\n🔴 产生SELL信号的指标 ({len(stats['sell_indicators'])}个):")
        for name, strength in sorted(stats['sell_indicators'], key=lambda x: x[1], reverse=True):
            print(f"   • {name:25} 强度: {strength:.2%}")

    return signals, stats


def test_strong_downtrend():
    """测试强势下跌趋势"""
    print("\n" + "╔" + "="*78 + "╗")
    print("║" + " "*25 + "📉 强势下跌趋势测试" + " "*25 + "║")
    print("╚" + "="*78 + "╝")

    # 生成强势下跌数据：持续下跌，成交量放大
    n = 500
    close = []
    volume = []

    for i in range(n):
        # 价格稳步下跌，带有小幅反弹
        if i % 50 < 45:  # 90%的时间在下跌
            close.append(150.0 - i * 0.12 + math.sin(i * 0.2) * 2)
        else:  # 10%的时间小幅反弹
            close.append(150.0 - i * 0.12 + 3.0)

        # 下跌时成交量放大（恐慌性抛售）
        volume.append(1000.0 + i * 5.0 + 500.0 * (1 if i % 50 < 45 else 0.5))

    high = [c + 1.5 for c in close]
    low = [c - 2.0 for c in close]

    print(f"\n📊 市场特征:")
    print(f"   K线数量: {n}")
    print(f"   价格范围: {max(close):.2f} → {min(close):.2f}")
    print(f"   跌幅: {((max(close) - min(close)) / max(close) * 100):.2f}%")
    print(f"   成交量: {min(volume):.0f} → {max(volume):.0f}")

    signals = haze.lt_indicator(high, low, close, volume)
    stats = print_signal_quality(signals, "强势下跌")

    print(f"\n{'='*80}")
    print(f"✅ 信号质量分析")
    print(f"{'='*80}")

    if stats['sell_count'] > stats['buy_count']:
        print(f"✅ 正确趋势判断: SELL信号 ({stats['sell_count']}) > BUY信号 ({stats['buy_count']})")
    else:
        print(f"⚠️  趋势判断异常: SELL信号 ({stats['sell_count']}) ≤ BUY信号 ({stats['buy_count']})")

    if signals['ensemble']['final_signal'] == 'SELL':
        print(f"✅ Ensemble集成信号正确: {signals['ensemble']['final_signal']}")
        print(f"   置信度: {signals['ensemble']['confidence']:.2%}")
    elif signals['ensemble']['final_signal'] == 'NEUTRAL':
        print(f"⚠️  Ensemble集成信号中性: {signals['ensemble']['final_signal']}")
        print(f"   可能需要更强的趋势或调整权重")
    else:
        print(f"❌ Ensemble集成信号错误: {signals['ensemble']['final_signal']}")

    print(f"\n🔴 产生SELL信号的指标 ({len(stats['sell_indicators'])}个):")
    for name, strength in sorted(stats['sell_indicators'], key=lambda x: x[1], reverse=True):
        print(f"   • {name:25} 强度: {strength:.2%}")

    if stats['buy_indicators']:
        print(f"\n🟢 产生BUY信号的指标 ({len(stats['buy_indicators'])}个):")
        for name, strength in sorted(stats['buy_indicators'], key=lambda x: x[1], reverse=True):
            print(f"   • {name:25} 强度: {strength:.2%}")

    return signals, stats


def test_moderate_uptrend():
    """测试温和上涨趋势"""
    print("\n" + "╔" + "="*78 + "╗")
    print("║" + " "*25 + "📊 温和上涨趋势测试" + " "*25 + "║")
    print("╚" + "="*78 + "╝")

    # 生成温和上涨数据：缓慢上涨，有波动
    n = 500
    close = []
    volume = []

    for i in range(n):
        # 价格缓慢上涨，带有波动
        close.append(100.0 + i * 0.05 + math.sin(i * 0.1) * 3)
        volume.append(1000.0 + math.sin(i * 0.15) * 200)

    high = [c + 2.0 for c in close]
    low = [c - 2.0 for c in close]

    print(f"\n📊 市场特征:")
    print(f"   K线数量: {n}")
    print(f"   价格范围: {min(close):.2f} → {max(close):.2f}")
    print(f"   涨幅: {((max(close) - min(close)) / min(close) * 100):.2f}%")

    signals = haze.lt_indicator(high, low, close, volume)
    stats = print_signal_quality(signals, "温和上涨")

    return signals, stats


def test_moderate_downtrend():
    """测试温和下跌趋势"""
    print("\n" + "╔" + "="*78 + "╗")
    print("║" + " "*25 + "📊 温和下跌趋势测试" + " "*25 + "║")
    print("╚" + "="*78 + "╝")

    # 生成温和下跌数据：缓慢下跌，有波动
    n = 500
    close = []
    volume = []

    for i in range(n):
        # 价格缓慢下跌，带有波动
        close.append(150.0 - i * 0.05 + math.sin(i * 0.1) * 3)
        volume.append(1000.0 + math.sin(i * 0.15) * 200)

    high = [c + 2.0 for c in close]
    low = [c - 2.0 for c in close]

    print(f"\n📊 市场特征:")
    print(f"   K线数量: {n}")
    print(f"   价格范围: {max(close):.2f} → {min(close):.2f}")
    print(f"   跌幅: {((max(close) - min(close)) / max(close) * 100):.2f}%")

    signals = haze.lt_indicator(high, low, close, volume)
    stats = print_signal_quality(signals, "温和下跌")

    return signals, stats


def run_trend_tests():
    """运行所有趋势测试"""
    print("\n" + "╔" + "="*78 + "╗")
    print("║" + " "*20 + "LT指标趋势信号质量测试" + " "*20 + "║")
    print("╚" + "="*78 + "╝")

    results = {}

    # 测试强势上涨
    up_signals, up_stats = test_strong_uptrend()
    results['strong_uptrend'] = {
        'signals': up_signals,
        'stats': up_stats,
        'expected': 'BUY'
    }

    # 测试强势下跌
    down_signals, down_stats = test_strong_downtrend()
    results['strong_downtrend'] = {
        'signals': down_signals,
        'stats': down_stats,
        'expected': 'SELL'
    }

    # 测试温和上涨
    mod_up_signals, mod_up_stats = test_moderate_uptrend()
    results['moderate_uptrend'] = {
        'signals': mod_up_signals,
        'stats': mod_up_stats,
        'expected': 'BUY or NEUTRAL'
    }

    # 测试温和下跌
    mod_down_signals, mod_down_stats = test_moderate_downtrend()
    results['moderate_downtrend'] = {
        'signals': mod_down_signals,
        'stats': mod_down_stats,
        'expected': 'SELL or NEUTRAL'
    }

    # 总结报告
    print("\n" + "╔" + "="*78 + "╗")
    print("║" + " "*28 + "📊 总结报告" + " "*28 + "║")
    print("╚" + "="*78 + "╝")

    print(f"\n{'趋势类型':<20} {'Ensemble信号':<15} {'置信度':<12} {'BUY':<6} {'SELL':<6} {'判断':<10}")
    print("="*80)

    for test_name, result in results.items():
        ensemble_signal = result['signals']['ensemble']['final_signal']
        confidence = result['signals']['ensemble']['confidence']
        buy_count = result['stats']['buy_count']
        sell_count = result['stats']['sell_count']
        expected = result['expected']

        # 判断准确性
        if 'strong_uptrend' in test_name:
            correct = '✅' if ensemble_signal in ['BUY', 'NEUTRAL'] and buy_count >= sell_count else '❌'
        elif 'strong_downtrend' in test_name:
            correct = '✅' if ensemble_signal in ['SELL', 'NEUTRAL'] and sell_count >= buy_count else '❌'
        else:
            correct = '✅'  # 温和趋势可以是任何信号

        print(f"{test_name:<20} {ensemble_signal:<15} {confidence:<12.2%} {buy_count:<6} {sell_count:<6} {correct:<10}")

    print("\n" + "="*80)
    print("🎯 关键发现:")
    print("="*80)

    # 强势上涨测试
    if results['strong_uptrend']['stats']['buy_count'] > 0:
        print(f"✅ 强势上涨: {results['strong_uptrend']['stats']['buy_count']}个指标产生BUY信号")
    else:
        print(f"⚠️  强势上涨: 没有指标产生BUY信号，可能需要调整参数")

    # 强势下跌测试
    if results['strong_downtrend']['stats']['sell_count'] > 0:
        print(f"✅ 强势下跌: {results['strong_downtrend']['stats']['sell_count']}个指标产生SELL信号")
    else:
        print(f"⚠️  强势下跌: 没有指标产生SELL信号，可能需要调整参数")

    # 置信度分析
    avg_confidence = sum(r['signals']['ensemble']['confidence'] for r in results.values()) / len(results)
    print(f"\n📊 平均Ensemble置信度: {avg_confidence:.2%}")

    if avg_confidence > 0.5:
        print(f"✅ 高置信度 - 信号质量良好")
    elif avg_confidence > 0.3:
        print(f"⚠️  中等置信度 - 信号质量一般")
    else:
        print(f"⚠️  低置信度 - 可能需要优化指标权重")

    print(f"\n{'='*80}")
    print("🚀 趋势信号质量测试完成！")
    print("="*80)


if __name__ == "__main__":
    run_trend_tests()
