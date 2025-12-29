#!/usr/bin/env python3
"""
LT Indicator Demo
=================

演示如何使用haze库的LT (Long-Term)指标功能。
LT指标整合了10个SFG交易信号，返回统一的JSON格式。

适用场景：
- 量化交易系统快速集成
- LLM驱动的交易决策
- 信号组合策略回测
"""

import sys
from pathlib import Path

# 添加父目录到path以便导入haze_library
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import json
import haze_library as haze


def generate_sample_data(length: int = 500) -> tuple[list[float], list[float], list[float], list[float]]:
    """生成模拟的OHLCV数据（用于演示）

    生成一个简单的上升趋势 + 噪音的价格序列

    Args:
        length: 数据长度

    Returns:
        (high, low, close, volume)
    """
    import random
    import math

    random.seed(42)

    base_price = 100.0
    close_prices = []
    high_prices = []
    low_prices = []
    volumes = []

    for i in range(length):
        # 上升趋势 + 随机波动
        trend = i * 0.05  # 缓慢上升
        noise = random.gauss(0, 2.0)  # 随机波动
        close = base_price + trend + noise

        # High/Low 基于 Close
        high = close + random.uniform(0.5, 2.0)
        low = close - random.uniform(0.5, 2.0)

        # 成交量
        volume = random.uniform(800, 1200)

        close_prices.append(close)
        high_prices.append(high)
        low_prices.append(low)
        volumes.append(volume)

    return high_prices, low_prices, close_prices, volumes


def print_signal_summary(signals: dict) -> None:
    """打印信号摘要（美化输出）"""
    print("\n" + "=" * 80)
    print("📊 LT INDICATOR SIGNALS SUMMARY")
    print("=" * 80)

    # 1. 集成信号
    if "ensemble" in signals:
        ensemble = signals["ensemble"]
        print("\n🎯 ENSEMBLE SIGNAL (Weighted Voting)")
        print("-" * 80)
        print(f"   Final Signal:  {ensemble['final_signal']:>10}")
        print(f"   Confidence:    {ensemble['confidence']:>10.2%}")
        print(f"   Buy Weight:    {ensemble['buy_weight']:>10.2%}")
        print(f"   Sell Weight:   {ensemble['sell_weight']:>10.2%}")
        print(f"\n   Vote Summary:")
        summary = ensemble['vote_summary']
        print(f"      BUY:     {summary['buy']} indicators")
        print(f"      SELL:    {summary['sell']} indicators")
        print(f"      NEUTRAL: {summary['neutral']} indicators")

    # 2. 各指标详情
    print("\n📈 INDIVIDUAL INDICATORS")
    print("-" * 80)

    indicators = signals.get("indicators", {})
    for name, data in indicators.items():
        signal = data.get("signal", "N/A")
        strength = data.get("strength", 0.0)

        # 信号图标
        icon = "🟢" if signal == "BUY" else "🔴" if signal == "SELL" else "⚪"

        print(f"\n{icon} {name.upper().replace('_', ' ')}")
        print(f"   Signal:   {signal:>10}   Strength: {strength:.2%}")

        # 额外信息
        extra_keys = [k for k in data.keys() if k not in ["signal", "strength", "note"]]
        if extra_keys:
            for key in sorted(extra_keys)[:3]:  # 只显示前3个
                value = data[key]
                if isinstance(value, float):
                    print(f"   {key:20s}: {value:>10.4f}")
                else:
                    print(f"   {key:20s}: {value!s:>10}")

        # 注释（如果有）
        if "note" in data:
            print(f"   ℹ️  {data['note']}")

    print("\n" + "=" * 80 + "\n")


def demo_basic_usage():
    """基础使用演示"""
    print("\n🔹 Demo 1: Basic Usage")
    print("-" * 80)

    # 1. 生成模拟数据
    high, low, close, volume = generate_sample_data(500)
    print(f"Generated {len(close)} bars of sample data")
    print(f"Price range: {min(close):.2f} - {max(close):.2f}")

    # 2. 调用LT指标
    print("\nCalling haze.lt_indicator()...")
    signals = haze.lt_indicator(high, low, close, volume)

    # 3. 打印结果
    print_signal_summary(signals)

    # 4. JSON输出（用于LLM）
    print("📄 JSON Output (for LLM integration):")
    print("-" * 80)
    json_output = json.dumps(
        {
            "ensemble": signals.get("ensemble", {}),
            "indicators": {
                k: {
                    "signal": v["signal"],
                    "strength": v["strength"],
                }
                for k, v in signals.get("indicators", {}).items()
            },
        },
        indent=2,
    )
    print(json_output)


def demo_custom_weights():
    """自定义权重演示"""
    print("\n🔹 Demo 2: Custom Weights")
    print("-" * 80)

    high, low, close, volume = generate_sample_data(500)

    # 自定义权重：更重视AI SuperTrend和ATR2
    custom_weights = {
        "ai_supertrend": 0.40,  # 40%
        "atr2_signals": 0.30,  # 30%
        "ai_momentum": 0.10,
        "pivot_points": 0.10,
        "market_structure_fvg": 0.10,
        # 其他指标权重为0（忽略）
    }

    print("Custom weights:")
    for name, weight in custom_weights.items():
        print(f"  {name:25s}: {weight:.0%}")

    signals = haze.lt_indicator(
        high, low, close, volume,
        weights=custom_weights,
    )

    print_signal_summary(signals)


def demo_disable_ensemble():
    """禁用集成信号演示"""
    print("\n🔹 Demo 3: Disable Ensemble (Individual Indicators Only)")
    print("-" * 80)

    high, low, close, volume = generate_sample_data(500)

    # 只返回各指标，不计算集成
    signals = haze.lt_indicator(
        high, low, close, volume,
        enable_ensemble=False,
    )

    print("Ensemble disabled. Only individual indicators returned.")
    print(f"Number of indicators: {len(signals.get('indicators', {}))}")

    # 简单列表
    for name, data in signals.get("indicators", {}).items():
        signal = data.get("signal", "N/A")
        strength = data.get("strength", 0.0)
        icon = "🟢" if signal == "BUY" else "🔴" if signal == "SELL" else "⚪"
        print(f"{icon} {name:30s}: {signal:>8} ({strength:.0%})")


def demo_trading_decision():
    """交易决策示例"""
    print("\n🔹 Demo 4: Trading Decision Logic")
    print("-" * 80)

    high, low, close, volume = generate_sample_data(500)
    signals = haze.lt_indicator(high, low, close, volume)

    ensemble = signals.get("ensemble", {})
    final_signal = ensemble.get("final_signal", "NEUTRAL")
    confidence = ensemble.get("confidence", 0.0)

    print(f"Current Price: {close[-1]:.2f}")
    print(f"Signal: {final_signal}, Confidence: {confidence:.2%}")
    print()

    # 决策逻辑
    if final_signal == "BUY" and confidence >= 0.70:
        print("✅ DECISION: EXECUTE BUY ORDER")
        print("   Reason: Strong buy signal with high confidence")

        # 获取止损/止盈建议
        ai_st = signals["indicators"]["ai_supertrend"]
        if ai_st.get("stop_loss") is not None:
            print(f"   Stop Loss:   {ai_st['stop_loss']:.2f}")
        if ai_st.get("take_profit") is not None:
            print(f"   Take Profit: {ai_st['take_profit']:.2f}")

    elif final_signal == "SELL" and confidence >= 0.70:
        print("✅ DECISION: EXECUTE SELL ORDER")
        print("   Reason: Strong sell signal with high confidence")

    elif confidence >= 0.50:
        print("⚠️  DECISION: MONITOR (Signal present but confidence moderate)")
        print(f"   Reason: {final_signal} signal with {confidence:.0%} confidence")

    else:
        print("⏸️  DECISION: NO ACTION")
        print("   Reason: Weak or neutral signal")

    # 投票详情
    summary = ensemble.get("vote_summary", {})
    print(f"\n   Voting: {summary.get('buy', 0)} BUY, {summary.get('sell', 0)} SELL, {summary.get('neutral', 0)} NEUTRAL")


def main():
    """主函数"""
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                        🚀 LT INDICATOR DEMO 🚀                               ║
║                                                                              ║
║        LT (Long-Term) 指标：10个SFG交易信号组合                                 ║
║        适用于量化交易系统、LLM驱动决策、策略回测                                    ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)

    try:
        # Demo 1: 基础使用
        demo_basic_usage()

        # Demo 2: 自定义权重
        demo_custom_weights()

        # Demo 3: 禁用集成
        demo_disable_ensemble()

        # Demo 4: 交易决策
        demo_trading_decision()

        print("\n✅ All demos completed successfully!")
        print("\n📚 Usage in crypto-bot-py:")
        print("""
    import ccxt
    import haze_library as haze

    # 1. 获取OHLCV数据
    exchange = ccxt.binance()
    ohlcv = exchange.fetch_ohlcv('BTC/USDT', '1m', limit=500)
    high = [c[2] for c in ohlcv]
    low = [c[3] for c in ohlcv]
    close = [c[4] for c in ohlcv]
    volume = [c[5] for c in ohlcv]

    # 2. 调用LT指标
    signals = haze.lt_indicator(high, low, close, volume)

    # 3. 使用信号
    if signals['ensemble']['final_signal'] == 'BUY':
        if signals['ensemble']['confidence'] >= 0.70:
            # 执行买入
            exchange.create_market_buy_order('BTC/USDT', 0.001)
        """)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
