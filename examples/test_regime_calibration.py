#!/usr/bin/env python3
"""
市场状态检测校准测试

使用极端行情和真实市场模拟数据，测试并优化：
1. ADX阈值
2. ATR%阈值
3. 各市场状态的指标权重

目标：找到最优的检测参数和权重配置
"""

import haze_library as haze
import math


def generate_extreme_bull_market(n=500):
    """
    生成极端牛市：
    - 持续上涨，涨幅 > 100%
    - 高ADX（强趋势）
    - 中等波动
    """
    close = []
    high = []
    low = []
    volume = []

    base = 100.0
    for i in range(n):
        # 指数型上涨 + 偶尔回调
        if i % 30 < 28:  # 93%时间上涨
            trend = base * math.exp(i / 200)  # 指数上涨
            noise = math.sin(i * 0.3) * (trend * 0.02)  # 2%噪音
        else:  # 7%时间回调
            trend = base * math.exp(i / 200) * 0.97
            noise = -trend * 0.03

        c = trend + noise
        close.append(c)
        high.append(c * 1.015)  # 1.5%上影线
        low.append(c * 0.99)    # 1%下影线

        # 上涨时成交量放大
        vol_mult = 1.5 if i % 30 < 28 else 2.0  # 回调时恐慌放量
        volume.append(1000.0 * (1 + i / 100) * vol_mult)

    return high, low, close, volume


def generate_extreme_bear_market(n=500):
    """
    生成极端熊市：
    - 持续下跌，跌幅 > 50%
    - 高ADX（强趋势）
    - 高波动（恐慌）
    """
    close = []
    high = []
    low = []
    volume = []

    base = 150.0
    for i in range(n):
        # 指数型下跌 + 偶尔反弹
        if i % 25 < 23:  # 92%时间下跌
            trend = base * math.exp(-i / 150)  # 指数下跌
            noise = math.sin(i * 0.4) * (trend * 0.03)  # 3%噪音
        else:  # 8%时间反弹
            trend = base * math.exp(-i / 150) * 1.05
            noise = trend * 0.04

        c = trend + noise
        close.append(c)
        high.append(c * 1.02)   # 2%上影线
        low.append(c * 0.975)   # 2.5%下影线（恐慌跳水）

        # 下跌时成交量激增
        vol_mult = 2.0 if i % 25 < 23 else 1.5
        volume.append(1000.0 * (1 + i / 80) * vol_mult)

    return high, low, close, volume


def generate_tight_consolidation(n=500):
    """
    生成窄幅震荡：
    - 价格在2%区间内波动
    - 低ADX（无趋势）
    - 低ATR（低波动）
    """
    close = []
    high = []
    low = []
    volume = []

    base = 100.0
    range_size = 2.0  # 2%区间

    for i in range(n):
        # 窄幅震荡
        c = base + (range_size / 2) * math.sin(i * 0.2)
        close.append(c)
        high.append(c + 0.3)  # 0.3%上影线
        low.append(c - 0.3)   # 0.3%下影线

        # 成交量萎缩
        volume.append(500.0 + 100.0 * abs(math.sin(i * 0.15)))

    return high, low, close, volume


def generate_wide_consolidation(n=500):
    """
    生成宽幅震荡：
    - 价格在15-20%区间内波动
    - 低ADX（无趋势）
    - 中等ATR
    """
    close = []
    high = []
    low = []
    volume = []

    base = 100.0
    range_size = 18.0  # 18%区间

    for i in range(n):
        # 宽幅震荡（类似箱体）
        phase = (i % 100) / 100  # 0-1循环
        if phase < 0.25:  # 上升阶段
            c = base + range_size * phase * 4
        elif phase < 0.5:  # 高位震荡
            c = base + range_size * (1 - (phase - 0.25) * 2)
        elif phase < 0.75:  # 下跌阶段
            c = base + range_size * (1 - (phase - 0.25) * 2)
        else:  # 低位震荡
            c = base + range_size * (phase - 0.75) * 4

        close.append(c)
        high.append(c + 1.0)
        low.append(c - 1.0)

        # 成交量在突破区间边界时放大
        vol_mult = 1.5 if (phase < 0.1 or phase > 0.9) else 1.0
        volume.append(800.0 + 200.0 * vol_mult)

    return high, low, close, volume


def generate_flash_crash(n=500):
    """
    生成闪崩行情：
    - 前期稳定
    - 中期急速下跌
    - 后期快速恢复
    - 极高ATR（高波动）
    """
    close = []
    high = []
    low = []
    volume = []

    base = 100.0

    for i in range(n):
        if i < 200:  # 前期稳定
            c = base + i * 0.05 + math.sin(i * 0.1) * 2
            h_offset, l_offset = 1.0, 1.0
            vol_mult = 1.0

        elif i < 250:  # 闪崩（50根K线暴跌30%）
            crash_progress = (i - 200) / 50
            c = base + 200 * 0.05 - crash_progress * 35  # 暴跌35
            h_offset, l_offset = 2.0, 5.0  # 长下影线
            vol_mult = 5.0  # 恐慌放量

        else:  # 快速恢复
            recovery_progress = (i - 250) / 250
            c = (base + 200 * 0.05 - 35) + recovery_progress * 30  # 恢复30
            h_offset, l_offset = 3.0, 2.0
            vol_mult = 2.0

        close.append(c)
        high.append(c + h_offset)
        low.append(c - l_offset)
        volume.append(1000.0 + i * 2.0 * vol_mult)

    return high, low, close, volume


def generate_steady_uptrend_with_pullbacks(n=500):
    """
    生成稳健上涨趋势+回调：
    - 整体上涨30-40%
    - 每隔一段时间有10-15%的回调
    - 中等ADX
    """
    close = []
    high = []
    low = []
    volume = []

    base = 100.0
    trend_angle = 0.08  # 每根K线涨0.08

    for i in range(n):
        # 趋势线
        trend = base + i * trend_angle

        # 周期性回调
        cycle = i % 80
        if cycle < 60:  # 75%时间上涨
            pullback = 0
        else:  # 25%时间回调
            pullback = -((cycle - 60) / 20) * 8  # 回调最多8个点

        c = trend + pullback + math.sin(i * 0.15) * 1.0  # 日内波动
        close.append(c)
        high.append(c + 1.5)
        low.append(c - 1.0)

        # 上涨放量，回调缩量
        vol_mult = 1.0 if cycle < 60 else 0.6
        volume.append(1000.0 + i * 3.0 * vol_mult)

    return high, low, close, volume


def analyze_market_characteristics(high, low, close, volume, name):
    """分析市场特征并计算关键指标（包含整体和近期200根K线统计）"""
    import haze_library as _ext

    # 与detect_market_regime默认值一致
    REGIME_DETECTION_PERIOD = 200

    n = len(close)

    # ===== 整体统计（所有K线） =====
    price_change = ((close[-1] - close[0]) / close[0]) * 100
    price_range_pct = ((max(close) - min(close)) / min(close)) * 100

    # ===== 近期统计（最近200根K线） =====
    period = min(REGIME_DETECTION_PERIOD, n)
    recent_high = max(high[-period:])
    recent_low = min(low[-period:])
    recent_range_pct = ((recent_high - recent_low) / recent_low) * 100 if recent_low > 0 else 0.0
    recent_price_change = ((close[-1] - close[-period]) / close[-period]) * 100 if period > 0 else 0.0

    # 计算ADX
    try:
        adx = _ext.py_adx(high, low, close, REGIME_DETECTION_PERIOD)
        adx_val = adx[-1] if len(adx) > 0 and not math.isnan(adx[-1]) else 0.0
    except:
        adx_val = 0.0

    # 计算ATR%
    try:
        atr = _ext.py_atr(high, low, close, REGIME_DETECTION_PERIOD)
        atr_val = atr[-1] if len(atr) > 0 else 0.0
        atr_pct = (atr_val / close[-1]) * 100 if close[-1] > 0 else 0.0
    except:
        atr_pct = 0.0

    # 计算波动率
    volatility = 0.0
    if n > 1:
        returns = [(close[i] - close[i-1]) / close[i-1] for i in range(1, n)]
        mean_return = sum(returns) / len(returns)
        variance = sum((r - mean_return) ** 2 for r in returns) / len(returns)
        volatility = math.sqrt(variance) * math.sqrt(252) * 100  # 年化波动率

    return {
        'name': name,
        'bars': n,
        # 整体统计
        'price_change': price_change,
        'price_range': price_range_pct,
        # 近期统计（与detection函数一致）
        'recent_range': recent_range_pct,
        'recent_change': recent_price_change,
        # 技术指标
        'adx': adx_val,
        'atr_pct': atr_pct,
        'volatility': volatility,
    }


def test_scenario(scenario_name, generate_func, expected_regime=None):
    """测试单个市场场景"""
    print(f"\n{'='*80}")
    print(f"📊 场景: {scenario_name}")
    print(f"{'='*80}")

    # 生成数据
    high, low, close, volume = generate_func(500)

    # 分析市场特征
    chars = analyze_market_characteristics(high, low, close, volume, scenario_name)

    print(f"\n市场特征:")
    print(f"   整体统计（{chars['bars']}根K线）:")
    print(f"      价格变化: {chars['price_change']:>8.2f}%")
    print(f"      价格区间: {chars['price_range']:>8.2f}%")
    print(f"   近期统计（最近200根K线 - 与检测逻辑一致）:")
    print(f"      价格变化: {chars['recent_change']:>8.2f}%")
    print(f"      价格区间: {chars['recent_range']:>8.2f}%")
    print(f"   技术指标:")
    print(f"      ADX值:    {chars['adx']:>8.2f}")
    print(f"      ATR%:     {chars['atr_pct']:>8.2f}%")
    print(f"      年化波动: {chars['volatility']:>8.2f}%")

    # 测试市场状态检测
    signals = haze.lt_indicator(high, low, close, volume, auto_regime=True)

    detected_regime = signals.get('market_regime', 'N/A')
    ensemble = signals['ensemble']

    print(f"\n检测结果:")
    print(f"   检测状态: {detected_regime}")
    if expected_regime:
        is_correct = detected_regime == expected_regime
        print(f"   预期状态: {expected_regime}  {'✅' if is_correct else '❌'}")

        # 如果检测结果与预期不符，检查是否因为整体vs近期差异
        if not is_correct:
            range_diff = abs(chars['price_range'] - chars['recent_range'])
            if range_diff > 10:  # 差异超过10%
                print(f"   💡 注意: 整体区间({chars['price_range']:.1f}%) vs 近期区间({chars['recent_range']:.1f}%) 差异较大")
                print(f"          检测基于近期50根K线，可能处于不同阶段")

    print(f"\n集成信号:")
    print(f"   最终信号: {ensemble['final_signal']}")
    print(f"   置信度:   {ensemble['confidence']:.2%}")
    print(f"   投票:     BUY={ensemble['vote_summary']['buy']} "
          f"SELL={ensemble['vote_summary']['sell']} "
          f"NEUTRAL={ensemble['vote_summary']['neutral']}")

    # 统计信号分布
    indicators = signals['indicators']
    buy_count = sum(1 for ind in indicators.values() if ind['signal'] == 'BUY')
    sell_count = sum(1 for ind in indicators.values() if ind['signal'] == 'SELL')

    print(f"\n信号分布:")
    print(f"   BUY信号数:  {buy_count}/10")
    print(f"   SELL信号数: {sell_count}/10")

    return {
        'scenario': scenario_name,
        'chars': chars,
        'detected_regime': detected_regime,
        'expected_regime': expected_regime,
        'final_signal': ensemble['final_signal'],
        'confidence': ensemble['confidence'],
        'buy_count': buy_count,
        'sell_count': sell_count,
    }


def run_calibration_tests():
    """运行所有校准测试"""
    print("\n" + "╔" + "="*78 + "╗")
    print("║" + " "*20 + "市场状态检测校准测试" + " "*20 + "║")
    print("╚" + "="*78 + "╝")

    results = []

    # 测试1: 极端牛市
    results.append(test_scenario(
        "极端牛市（指数上涨）",
        generate_extreme_bull_market,
        expected_regime='TRENDING'
    ))

    # 测试2: 极端熊市
    results.append(test_scenario(
        "极端熊市（指数下跌）",
        generate_extreme_bear_market,
        expected_regime='TRENDING'
    ))

    # 测试3: 窄幅震荡
    results.append(test_scenario(
        "窄幅震荡（2%区间）",
        generate_tight_consolidation,
        expected_regime='RANGING'
    ))

    # 测试4: 宽幅震荡
    results.append(test_scenario(
        "宽幅震荡（18%区间）",
        generate_wide_consolidation,
        expected_regime='RANGING'
    ))

    # 测试5: 闪崩行情
    results.append(test_scenario(
        "闪崩行情（极端波动）",
        generate_flash_crash,
        expected_regime='VOLATILE'
    ))

    # 测试6: 稳健上涨+回调
    results.append(test_scenario(
        "稳健上涨+周期回调",
        generate_steady_uptrend_with_pullbacks,
        expected_regime='TRENDING'
    ))

    # 汇总分析
    print("\n" + "╔" + "="*78 + "╗")
    print("║" + " "*28 + "📊 汇总分析" + " "*28 + "║")
    print("╚" + "="*78 + "╝")

    print(f"\n{'场景':<25} {'ADX':<8} {'ATR%':<8} {'检测':<12} {'预期':<12} {'准确':<6}")
    print("="*80)

    correct_count = 0
    total_count = 0

    for r in results:
        chars = r['chars']
        detected = r['detected_regime']
        expected = r['expected_regime']

        if expected:
            is_correct = detected == expected
            correct_count += is_correct
            total_count += 1
            check_mark = '✅' if is_correct else '❌'
        else:
            check_mark = '-'

        print(f"{r['scenario']:<25} {chars['adx']:<8.2f} {chars['atr_pct']:<8.2f} "
              f"{detected:<12} {expected or 'N/A':<12} {check_mark:<6}")

    accuracy = (correct_count / total_count * 100) if total_count > 0 else 0
    print(f"\n准确率: {correct_count}/{total_count} = {accuracy:.1f}%")

    # 阈值建议分析
    print(f"\n{'='*80}")
    print("🎯 阈值优化建议")
    print(f"{'='*80}")

    # 分析TRENDING场景的ADX
    trending_scenarios = [r for r in results if r['expected_regime'] == 'TRENDING']
    if trending_scenarios:
        trending_adx = [r['chars']['adx'] for r in trending_scenarios]
        min_trending_adx = min(trending_adx)
        print(f"\n📈 TRENDING场景:")
        print(f"   ADX范围: {min(trending_adx):.2f} - {max(trending_adx):.2f}")
        print(f"   当前阈值: ADX > 25")
        if min_trending_adx < 25:
            print(f"   ⚠️  建议降低ADX阈值至: {min_trending_adx * 0.9:.0f}")

    # 分析VOLATILE场景的ATR%
    volatile_scenarios = [r for r in results if r['expected_regime'] == 'VOLATILE']
    if volatile_scenarios:
        volatile_atr = [r['chars']['atr_pct'] for r in volatile_scenarios]
        print(f"\n💥 VOLATILE场景:")
        print(f"   ATR%范围: {min(volatile_atr):.2f}% - {max(volatile_atr):.2f}%")
        print(f"   当前阈值: ATR% > 5%")

    # 分析RANGING场景
    ranging_scenarios = [r for r in results if r['expected_regime'] == 'RANGING']
    if ranging_scenarios:
        ranging_adx = [r['chars']['adx'] for r in ranging_scenarios]
        ranging_range = [r['chars']['price_range'] for r in ranging_scenarios]
        print(f"\n📊 RANGING场景:")
        print(f"   ADX范围: {min(ranging_adx):.2f} - {max(ranging_adx):.2f}")
        print(f"   价格区间: {min(ranging_range):.2f}% - {max(ranging_range):.2f}%")

    # 信号质量分析
    print(f"\n{'='*80}")
    print("📊 信号质量分析")
    print(f"{'='*80}")

    for r in results:
        print(f"\n{r['scenario']}:")
        print(f"   最终信号: {r['final_signal']}")
        print(f"   置信度: {r['confidence']:.2%}")
        print(f"   信号数: BUY={r['buy_count']}, SELL={r['sell_count']}")

        # 分析信号合理性
        chars = r['chars']
        if chars['price_change'] > 50:  # 大幅上涨
            if r['buy_count'] > r['sell_count']:
                print(f"   ✅ 上涨市场产生更多BUY信号，合理")
            else:
                print(f"   ⚠️  上涨市场应产生更多BUY信号")
        elif chars['price_change'] < -30:  # 大幅下跌
            if r['sell_count'] > r['buy_count']:
                print(f"   ✅ 下跌市场产生更多SELL信号，合理")
            else:
                print(f"   ⚠️  下跌市场应产生更多SELL信号")

    return results


def suggest_optimized_parameters(results):
    """基于测试结果建议优化参数"""
    print(f"\n{'='*80}")
    print("🔧 优化参数建议")
    print(f"{'='*80}")

    # 分析TRENDING检测失败的案例
    trending_cases = [r for r in results if r['expected_regime'] == 'TRENDING']
    failed_trending = [r for r in trending_cases if r['detected_regime'] != 'TRENDING']

    if failed_trending:
        print(f"\n❌ TRENDING检测失败的案例:")
        for r in failed_trending:
            chars = r['chars']
            print(f"   {r['scenario']}: ADX={chars['adx']:.2f}, 区间={chars['price_range']:.2f}%")

        # 建议新阈值
        all_trending_adx = [r['chars']['adx'] for r in trending_cases]
        suggested_adx = min(all_trending_adx) * 0.85  # 留15%余量

        all_trending_range = [r['chars']['price_range'] for r in trending_cases]
        suggested_range = min(all_trending_range) * 0.85

        print(f"\n   建议调整:")
        print(f"   - ADX阈值: 25 → {suggested_adx:.0f}")
        print(f"   - 价格区间: 15% → {suggested_range:.0f}%")
        print(f"   - 或使用OR逻辑: (ADX > {suggested_adx:.0f}) OR (区间 > {suggested_range:.0f}%)")

    # 权重优化建议
    print(f"\n{'='*80}")
    print("⚖️  权重配置优化建议")
    print(f"{'='*80}")

    print("""
当前权重配置可能需要调整，建议：

1. TRENDING市场（强趋势）：
   - 降低AI SuperTrend权重（ML模型在极端行情中可能滞后）
   - 提高Market Structure权重（BOS/CHoCH更可靠）
   当前: {'ai_supertrend': 0.35, 'market_structure_fvg': 0.25}
   建议: {'ai_supertrend': 0.25, 'market_structure_fvg': 0.35}

2. RANGING市场（震荡）：
   - 当前配置合理，保持不变
   当前: {'pivot_points': 0.25, 'volume_profile': 0.25}

3. VOLATILE市场（高波动）：
   - 提高ATR2权重（波动性指标）
   - 降低其他指标权重
   当前: {'atr2_signals': 0.30, 'ai_momentum': 0.25}
   建议: {'atr2_signals': 0.40, 'ai_momentum': 0.20}
""")


if __name__ == "__main__":
    results = run_calibration_tests()
    suggest_optimized_parameters(results)

    print(f"\n{'='*80}")
    print("✅ 校准测试完成")
    print(f"{'='*80}")
