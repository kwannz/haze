#!/usr/bin/env python3
"""
市场状态感知功能使用示例

展示haze库的自动市场状态检测功能（超出SFG PDF规范的增强特性）
"""

import haze_library as haze


def example_basic_usage():
    """基础用法示例"""
    print("="*80)
    print("示例1: 基础用法 - 自动市场状态检测")
    print("="*80)

    # 模拟OHLCV数据（实际使用中从交易所获取）
    high = [100.0 + i * 0.1 + 2.0 for i in range(500)]
    low = [100.0 + i * 0.1 - 2.0 for i in range(500)]
    close = [100.0 + i * 0.1 for i in range(500)]
    volume = [1000.0 + i * 10.0 for i in range(500)]

    # 调用LT指标（自动检测市场状态）
    signals = haze.lt_indicator(high, low, close, volume)

    # 查看检测到的市场状态
    if 'market_regime' in signals:
        print(f"\n检测到的市场状态: {signals['market_regime']}")
        print(f"最终交易信号: {signals['ensemble']['final_signal']}")
        print(f"信号置信度: {signals['ensemble']['confidence']:.2%}")
    else:
        print("\n未启用市场状态检测")


def example_manual_regime():
    """手动指定市场状态"""
    print("\n"+"="*80)
    print("示例2: 手动指定市场状态")
    print("="*80)

    high = [100.0 + i * 0.1 + 2.0 for i in range(500)]
    low = [100.0 + i * 0.1 - 2.0 for i in range(500)]
    close = [100.0 + i * 0.1 for i in range(500)]
    volume = [1000.0 + i * 10.0 for i in range(500)]

    # 手动指定为趋势市场
    signals = haze.lt_indicator(high, low, close, volume, regime='TRENDING')

    print(f"\n指定的市场状态: {signals['market_regime']}")
    print(f"最终交易信号: {signals['ensemble']['final_signal']}")
    print(f"信号置信度: {signals['ensemble']['confidence']:.2%}")


def example_disable_auto():
    """禁用自动检测，使用固定权重"""
    print("\n"+"="*80)
    print("示例3: 禁用自动检测，使用固定权重")
    print("="*80)

    high = [100.0 + i * 0.1 + 2.0 for i in range(500)]
    low = [100.0 + i * 0.1 - 2.0 for i in range(500)]
    close = [100.0 + i * 0.1 for i in range(500)]
    volume = [1000.0 + i * 10.0 for i in range(500)]

    # 禁用自动检测
    signals = haze.lt_indicator(high, low, close, volume, auto_regime=False)

    print(f"\n市场状态检测: {'已禁用' if 'market_regime' not in signals else '已启用'}")
    print(f"最终交易信号: {signals['ensemble']['final_signal']}")
    print(f"信号置信度: {signals['ensemble']['confidence']:.2%}")


def example_custom_weights():
    """自定义权重"""
    print("\n"+"="*80)
    print("示例4: 自定义指标权重")
    print("="*80)

    high = [100.0 + i * 0.1 + 2.0 for i in range(500)]
    low = [100.0 + i * 0.1 - 2.0 for i in range(500)]
    close = [100.0 + i * 0.1 for i in range(500)]
    volume = [1000.0 + i * 10.0 for i in range(500)]

    # 自定义权重（优先Volume Profile和Pivot Points）
    custom_weights = {
        'volume_profile': 0.30,
        'pivot_points': 0.25,
        'ai_momentum': 0.20,
        'atr2_signals': 0.15,
        'linear_regression': 0.10,
    }

    signals = haze.lt_indicator(high, low, close, volume, weights=custom_weights)

    print(f"\n使用自定义权重")
    print(f"最终交易信号: {signals['ensemble']['final_signal']}")
    print(f"信号置信度: {signals['ensemble']['confidence']:.2%}")


def example_real_world_integration():
    """真实场景集成示例（伪代码）"""
    print("\n"+"="*80)
    print("示例5: 真实量化系统集成（伪代码）")
    print("="*80)

    print("""
# 与crypto-bot-py集成示例
import ccxt
import haze_library as haze

exchange = ccxt.binance()
ohlcv = exchange.fetch_ohlcv('BTC/USDT', '1m', limit=500)

high = [c[2] for c in ohlcv]
low = [c[3] for c in ohlcv]
close = [c[4] for c in ohlcv]
volume = [c[5] for c in ohlcv]

# 调用LT指标（自动适配市场状态）
signals = haze.lt_indicator(high, low, close, volume)

# 根据信号执行交易
if signals['ensemble']['final_signal'] == 'BUY' and signals['ensemble']['confidence'] > 0.6:
    # 高置信度买入信号
    print(f"检测到{signals['market_regime']}市场，执行买入")
    exchange.create_market_buy_order('BTC/USDT', 0.001)

elif signals['ensemble']['final_signal'] == 'SELL' and signals['ensemble']['confidence'] > 0.6:
    # 高置信度卖出信号
    print(f"检测到{signals['market_regime']}市场，执行卖出")
    exchange.create_market_sell_order('BTC/USDT', 0.001)

else:
    # 低置信度或中性信号，观望
    print(f"市场状态: {signals['market_regime']}, 信号: {signals['ensemble']['final_signal']}, 观望")
    """)


def main():
    """运行所有示例"""
    print("\n" + "╔" + "="*78 + "╗")
    print("║" + " "*20 + "市场状态感知功能使用示例" + " "*20 + "║")
    print("║" + " "*10 + "(haze库增强特性 - 超出SFG原始PDF规范)" + " "*10 + "║")
    print("╚" + "="*78 + "╝")

    # 示例1: 基础用法
    example_basic_usage()

    # 示例2: 手动指定
    example_manual_regime()

    # 示例3: 禁用自动检测
    example_disable_auto()

    # 示例4: 自定义权重
    example_custom_weights()

    # 示例5: 真实集成
    example_real_world_integration()

    print("\n" + "="*80)
    print("💡 使用建议总结")
    print("="*80)
    print("""
1. 量化系统推荐用法（全自动）：
   signals = haze.lt_indicator(high, low, close, volume)

2. 手动控制市场状态：
   signals = haze.lt_indicator(high, low, close, volume, regime='TRENDING')

3. 使用固定权重：
   signals = haze.lt_indicator(high, low, close, volume, auto_regime=False)

4. 完全自定义：
   custom_weights = {'volume_profile': 0.30, ...}
   signals = haze.lt_indicator(high, low, close, volume, weights=custom_weights)
""")

    print("="*80)
    print("✅ 示例演示完成")
    print("="*80)


if __name__ == "__main__":
    main()
