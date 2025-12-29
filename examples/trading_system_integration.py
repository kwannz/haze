#!/usr/bin/env python3
"""
交易系统集成示例 - Trading System Integration Example
========================================================

本示例展示如何将 LT 指标集成到实际交易系统中，包括：
1. 信号解读和交易决策
2. 仓位管理和风险控制
3. 止损和止盈设置
4. 实时市场监控

This example shows how to integrate LT indicator into a real trading system, including:
1. Signal interpretation and trading decisions
2. Position management and risk control
3. Stop-loss and take-profit settings
4. Real-time market monitoring
"""

import haze_library as haze
from typing import Literal, Optional
from dataclasses import dataclass
from datetime import datetime


# ============================================================================
# 1. 简单信号提取 - Simple Signal Extraction
# ============================================================================

def get_simple_signal(
    high: list[float],
    low: list[float],
    close: list[float],
    volume: list[float],
    min_confidence: float = 0.6
) -> Literal["BUY", "SELL", "HOLD"]:
    """
    获取简化的交易信号（适合快速集成）

    Args:
        high, low, close, volume: OHLCV 数据
        min_confidence: 最小置信度阈值 (默认 60%)

    Returns:
        "BUY" - 建议做多
        "SELL" - 建议做空
        "HOLD" - 建议观望

    Example:
        >>> signal = get_simple_signal(high, low, close, volume)
        >>> if signal == "BUY":
        >>>     open_long_position()
    """
    result = haze.lt_indicator(high, low, close, volume)

    ensemble = result["ensemble"]
    final_signal = ensemble["final_signal"]
    confidence = ensemble["confidence"]

    # 信号过滤：只有高置信度信号才执行
    if confidence < min_confidence:
        return "HOLD"

    # BUY/SELL 映射为交易动作
    if final_signal == "BUY":
        return "BUY"
    elif final_signal == "SELL":
        return "SELL"
    else:
        return "HOLD"


# ============================================================================
# 2. 交易决策辅助 - Trading Decision Helper
# ============================================================================

@dataclass
class TradeDecision:
    """交易决策数据类"""
    action: Literal["BUY", "SELL", "HOLD", "CLOSE"]
    confidence: float
    reason: str
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None
    position_size: float = 0.0

    def __str__(self):
        return (
            f"TradeDecision(action={self.action}, confidence={self.confidence:.1%}, "
            f"reason={self.reason})"
        )


def should_enter_trade(
    result: dict,
    current_price: float,
    min_confidence: float = 0.65,
    min_active_indicators: int = 3
) -> TradeDecision:
    """
    判断是否应该进场交易（更严格的决策逻辑）

    Args:
        result: lt_indicator() 返回的完整结果
        current_price: 当前市场价格
        min_confidence: 最小置信度 (默认 65%)
        min_active_indicators: 最小活跃指标数量 (默认 3 个)

    Returns:
        TradeDecision 对象，包含详细的交易建议

    Example:
        >>> result = haze.lt_indicator(high, low, close, volume)
        >>> decision = should_enter_trade(result, current_price=50000)
        >>> if decision.action == "BUY":
        >>>     place_order(
        >>>         side="BUY",
        >>>         size=decision.position_size,
        >>>         stop_loss=decision.stop_loss,
        >>>         take_profit=decision.take_profit
        >>>     )
    """
    ensemble = result["ensemble"]
    final_signal = ensemble["final_signal"]
    confidence = ensemble["confidence"]
    active_indicators = ensemble["active_indicators"]
    market_regime = result.get("market_regime", "UNKNOWN")

    # 决策规则 1: 置信度不足
    if confidence < min_confidence:
        return TradeDecision(
            action="HOLD",
            confidence=confidence,
            reason=f"置信度不足: {confidence:.1%} < {min_confidence:.0%}"
        )

    # 决策规则 2: 活跃指标数量不足
    if active_indicators < min_active_indicators:
        return TradeDecision(
            action="HOLD",
            confidence=confidence,
            reason=f"活跃指标不足: {active_indicators} < {min_active_indicators}"
        )

    # 决策规则 3: NEUTRAL 信号 - 观望
    if final_signal == "NEUTRAL":
        return TradeDecision(
            action="HOLD",
            confidence=confidence,
            reason="信号中性，等待明确方向"
        )

    # 决策规则 4: BUY 信号
    if final_signal == "BUY":
        # 根据市场状态调整止损止盈
        sl_pct, tp_pct = get_sl_tp_by_regime(market_regime, side="BUY")

        return TradeDecision(
            action="BUY",
            confidence=confidence,
            reason=f"多头信号 ({market_regime} 市场)",
            stop_loss=current_price * (1 - sl_pct),
            take_profit=current_price * (1 + tp_pct),
            position_size=calculate_position_size(confidence, market_regime)
        )

    # 决策规则 5: SELL 信号
    if final_signal == "SELL":
        sl_pct, tp_pct = get_sl_tp_by_regime(market_regime, side="SELL")

        return TradeDecision(
            action="SELL",
            confidence=confidence,
            reason=f"空头信号 ({market_regime} 市场)",
            stop_loss=current_price * (1 + sl_pct),
            take_profit=current_price * (1 - tp_pct),
            position_size=calculate_position_size(confidence, market_regime)
        )

    return TradeDecision(
        action="HOLD",
        confidence=confidence,
        reason="未知信号"
    )


def get_sl_tp_by_regime(
    regime: str,
    side: Literal["BUY", "SELL"]
) -> tuple[float, float]:
    """
    根据市场状态返回止损和止盈百分比

    Args:
        regime: 市场状态 (TRENDING/RANGING/VOLATILE)
        side: 交易方向 (BUY/SELL)

    Returns:
        (stop_loss_pct, take_profit_pct)

    Example:
        >>> sl_pct, tp_pct = get_sl_tp_by_regime("TRENDING", "BUY")
        >>> # TRENDING 市场：止损 2%, 止盈 5%
    """
    # 不同市场状态的风险参数
    params = {
        "TRENDING": {
            "stop_loss": 0.02,    # 2% 止损（趋势明确，可以紧止损）
            "take_profit": 0.05,  # 5% 止盈（趋势延续，目标远）
        },
        "RANGING": {
            "stop_loss": 0.015,   # 1.5% 止损（震荡市，快进快出）
            "take_profit": 0.025, # 2.5% 止盈（目标近）
        },
        "VOLATILE": {
            "stop_loss": 0.03,    # 3% 止损（波动大，需要宽止损）
            "take_profit": 0.04,  # 4% 止盈（波动带来机会）
        },
    }

    regime_params = params.get(regime, params["RANGING"])  # 默认使用 RANGING
    return regime_params["stop_loss"], regime_params["take_profit"]


def calculate_position_size(confidence: float, regime: str) -> float:
    """
    根据置信度和市场状态计算仓位大小（占总资金比例）

    Args:
        confidence: 信号置信度 [0.0, 1.0]
        regime: 市场状态

    Returns:
        仓位比例 [0.0, 1.0]

    Example:
        >>> size = calculate_position_size(confidence=0.8, regime="TRENDING")
        >>> # 高置信度 + 趋势市场 = 较大仓位 (如 0.4 = 40% 资金)
    """
    # 基础仓位（根据置信度线性调整）
    base_size = confidence * 0.5  # 最大 50% 资金

    # 市场状态调整系数
    regime_multiplier = {
        "TRENDING": 1.0,   # 趋势市场：正常仓位
        "RANGING": 0.7,    # 震荡市场：减小仓位
        "VOLATILE": 0.6,   # 波动市场：进一步减小
    }

    multiplier = regime_multiplier.get(regime, 0.7)
    return base_size * multiplier


# ============================================================================
# 3. 风险参数提取 - Risk Parameters Extraction
# ============================================================================

def get_risk_parameters(
    result: dict,
    current_price: float,
    account_balance: float = 10000.0
) -> dict:
    """
    从 LT 指标结果中提取风险管理参数

    Args:
        result: lt_indicator() 返回结果
        current_price: 当前价格
        account_balance: 账户余额

    Returns:
        风险参数字典，包含：
        - position_size_usd: 建议仓位大小（美元）
        - stop_loss_price: 止损价格
        - take_profit_price: 止盈价格
        - risk_reward_ratio: 盈亏比
        - max_loss_usd: 最大亏损金额

    Example:
        >>> risk = get_risk_parameters(result, 50000, 10000)
        >>> print(f"建议仓位: ${risk['position_size_usd']:.2f}")
        >>> print(f"止损价: ${risk['stop_loss_price']:.2f}")
    """
    ensemble = result["ensemble"]
    confidence = ensemble["confidence"]
    final_signal = ensemble["final_signal"]
    regime = result.get("market_regime", "RANGING")

    # 计算仓位
    position_ratio = calculate_position_size(confidence, regime)
    position_size_usd = account_balance * position_ratio

    # 计算止损止盈
    if final_signal == "BUY":
        sl_pct, tp_pct = get_sl_tp_by_regime(regime, "BUY")
        stop_loss_price = current_price * (1 - sl_pct)
        take_profit_price = current_price * (1 + tp_pct)
    elif final_signal == "SELL":
        sl_pct, tp_pct = get_sl_tp_by_regime(regime, "SELL")
        stop_loss_price = current_price * (1 + sl_pct)
        take_profit_price = current_price * (1 - tp_pct)
    else:
        # NEUTRAL - 不建议交易
        return {
            "position_size_usd": 0.0,
            "stop_loss_price": None,
            "take_profit_price": None,
            "risk_reward_ratio": None,
            "max_loss_usd": 0.0,
            "recommendation": "HOLD - 信号中性，暂不交易"
        }

    # 计算盈亏比和最大亏损
    risk_per_unit = abs(current_price - stop_loss_price)
    reward_per_unit = abs(take_profit_price - current_price)
    risk_reward_ratio = reward_per_unit / risk_per_unit if risk_per_unit > 0 else 0

    max_loss_usd = (position_size_usd / current_price) * risk_per_unit

    return {
        "position_size_usd": position_size_usd,
        "stop_loss_price": stop_loss_price,
        "take_profit_price": take_profit_price,
        "risk_reward_ratio": risk_reward_ratio,
        "max_loss_usd": max_loss_usd,
        "recommendation": final_signal
    }


# ============================================================================
# 4. 完整交易系统示例 - Complete Trading System Example
# ============================================================================

class SimpleTradingBot:
    """
    简单交易机器人示例

    展示如何使用 LT 指标构建完整的交易循环
    """

    def __init__(
        self,
        initial_balance: float = 10000.0,
        min_confidence: float = 0.65,
        min_active_indicators: int = 3
    ):
        self.balance = initial_balance
        self.initial_balance = initial_balance
        self.position = None  # {"side": "BUY/SELL", "size": ..., "entry": ..., "sl": ..., "tp": ...}
        self.min_confidence = min_confidence
        self.min_active_indicators = min_active_indicators
        self.trade_history = []

    def on_new_bar(
        self,
        high: list[float],
        low: list[float],
        close: list[float],
        volume: list[float]
    ):
        """
        每根 K 线回调（实盘中由交易所 WebSocket 触发）

        Args:
            high, low, close, volume: 最近的 OHLCV 数据（建议至少 500 根）
        """
        current_price = close[-1]
        timestamp = datetime.now().isoformat()

        # 1. 获取 LT 指标分析
        result = haze.lt_indicator(high, low, close, volume)

        # 2. 如果有持仓，检查止损止盈
        if self.position is not None:
            self._check_exit_conditions(current_price, timestamp)

        # 3. 如果无持仓，检查入场信号
        if self.position is None:
            self._check_entry_conditions(result, current_price, timestamp)

        # 4. 打印当前状态
        self._print_status(result, current_price)

    def _check_entry_conditions(self, result: dict, current_price: float, timestamp: str):
        """检查入场条件"""
        decision = should_enter_trade(
            result,
            current_price,
            self.min_confidence,
            self.min_active_indicators
        )

        if decision.action in ["BUY", "SELL"]:
            # 开仓
            quantity = decision.position_size * self.balance / current_price

            self.position = {
                "side": decision.action,
                "entry_price": current_price,
                "quantity": quantity,
                "stop_loss": decision.stop_loss,
                "take_profit": decision.take_profit,
                "entry_time": timestamp,
            }

            print(f"\n🟢 开仓 {decision.action}")
            print(f"   价格: ${current_price:,.2f}")
            print(f"   数量: {quantity:.6f}")
            print(f"   止损: ${decision.stop_loss:,.2f}")
            print(f"   止盈: ${decision.take_profit:,.2f}")
            print(f"   理由: {decision.reason}")

    def _check_exit_conditions(self, current_price: float, timestamp: str):
        """检查出场条件（止损/止盈）"""
        pos = self.position

        # 止损检查
        if pos["side"] == "BUY" and current_price <= pos["stop_loss"]:
            self._close_position(current_price, timestamp, "止损")
        elif pos["side"] == "SELL" and current_price >= pos["stop_loss"]:
            self._close_position(current_price, timestamp, "止损")

        # 止盈检查
        elif pos["side"] == "BUY" and current_price >= pos["take_profit"]:
            self._close_position(current_price, timestamp, "止盈")
        elif pos["side"] == "SELL" and current_price <= pos["take_profit"]:
            self._close_position(current_price, timestamp, "止盈")

    def _close_position(self, exit_price: float, timestamp: str, reason: str):
        """平仓"""
        pos = self.position

        # 计算盈亏
        if pos["side"] == "BUY":
            pnl = (exit_price - pos["entry_price"]) * pos["quantity"]
        else:  # SELL
            pnl = (pos["entry_price"] - exit_price) * pos["quantity"]

        pnl_pct = (pnl / self.balance) * 100
        self.balance += pnl

        # 记录交易
        trade_record = {
            "entry_time": pos["entry_time"],
            "exit_time": timestamp,
            "side": pos["side"],
            "entry_price": pos["entry_price"],
            "exit_price": exit_price,
            "quantity": pos["quantity"],
            "pnl": pnl,
            "pnl_pct": pnl_pct,
            "reason": reason,
        }
        self.trade_history.append(trade_record)

        print(f"\n🔴 平仓 {pos['side']} ({reason})")
        print(f"   入场: ${pos['entry_price']:,.2f}")
        print(f"   出场: ${exit_price:,.2f}")
        print(f"   盈亏: ${pnl:+,.2f} ({pnl_pct:+.2f}%)")
        print(f"   余额: ${self.balance:,.2f}")

        self.position = None

    def _print_status(self, result: dict, current_price: float):
        """打印当前状态"""
        ensemble = result["ensemble"]
        regime = result.get("market_regime", "UNKNOWN")

        print(f"\n📊 市场状态: {regime}")
        print(f"   价格: ${current_price:,.2f}")
        print(f"   信号: {ensemble['final_signal']} (置信度: {ensemble['confidence']:.1%})")
        print(f"   活跃指标: {ensemble['active_indicators']}/10")
        print(f"   余额: ${self.balance:,.2f}")

        if self.position:
            pos = self.position
            unrealized_pnl = (
                (current_price - pos["entry_price"]) * pos["quantity"]
                if pos["side"] == "BUY"
                else (pos["entry_price"] - current_price) * pos["quantity"]
            )
            print(f"   持仓: {pos['side']} @ ${pos['entry_price']:,.2f}")
            print(f"   浮盈: ${unrealized_pnl:+,.2f}")


# ============================================================================
# 5. 使用示例 - Usage Examples
# ============================================================================

def example_1_quick_start():
    """示例 1: 快速开始 - 5 分钟集成"""
    print("\n" + "=" * 80)
    print("示例 1: 快速开始 - 获取简单信号")
    print("=" * 80)

    # 模拟市场数据（实际使用时从交易所获取）
    n = 500
    high = [50000.0 + i * 10 for i in range(n)]
    low = [49000.0 + i * 10 for i in range(n)]
    close = [49500.0 + i * 10 for i in range(n)]
    volume = [100.0] * n

    # 一行代码获取交易信号
    signal = get_simple_signal(high, low, close, volume, min_confidence=0.6)

    print(f"\n交易信号: {signal}")

    if signal == "BUY":
        print("✅ 建议: 开多单")
    elif signal == "SELL":
        print("✅ 建议: 开空单")
    else:
        print("⏸️  建议: 观望等待")


def example_2_with_risk_management():
    """示例 2: 带风险管理的决策"""
    print("\n" + "=" * 80)
    print("示例 2: 带风险管理的交易决策")
    print("=" * 80)

    # 模拟市场数据
    n = 500
    high = [50000.0 + i * 10 for i in range(n)]
    low = [49000.0 + i * 10 for i in range(n)]
    close = [49500.0 + i * 10 for i in range(n)]
    volume = [100.0] * n

    current_price = close[-1]
    account_balance = 10000.0

    # 获取完整分析
    result = haze.lt_indicator(high, low, close, volume)

    # 交易决策
    decision = should_enter_trade(result, current_price, min_confidence=0.65)

    print(f"\n{decision}")

    if decision.action in ["BUY", "SELL"]:
        # 提取风险参数
        risk = get_risk_parameters(result, current_price, account_balance)

        print(f"\n风险管理参数:")
        print(f"  建议仓位: ${risk['position_size_usd']:,.2f}")
        print(f"  止损价格: ${risk['stop_loss_price']:,.2f}")
        print(f"  止盈价格: ${risk['take_profit_price']:,.2f}")
        print(f"  盈亏比: {risk['risk_reward_ratio']:.2f}:1")
        print(f"  最大亏损: ${risk['max_loss_usd']:,.2f}")


def example_3_trading_bot():
    """示例 3: 完整交易机器人"""
    print("\n" + "=" * 80)
    print("示例 3: 完整交易机器人演示")
    print("=" * 80)

    # 创建交易机器人
    bot = SimpleTradingBot(
        initial_balance=10000.0,
        min_confidence=0.65,
        min_active_indicators=3
    )

    # 模拟 3 根 K 线的市场数据更新
    for i in range(3):
        print(f"\n{'─' * 80}")
        print(f"K线 #{i + 1}")
        print(f"{'─' * 80}")

        # 生成滑动窗口数据（实际使用时从交易所 API 获取）
        n = 500
        base_price = 50000.0 + i * 100
        high = [base_price + j * 2 for j in range(n)]
        low = [base_price + j * 2 - 100 for j in range(n)]
        close = [base_price + j * 2 - 50 for j in range(n)]
        volume = [100.0] * n

        # 触发交易逻辑
        bot.on_new_bar(high, low, close, volume)

    # 输出交易统计
    print("\n" + "=" * 80)
    print("交易统计")
    print("=" * 80)
    print(f"初始资金: ${bot.initial_balance:,.2f}")
    print(f"当前余额: ${bot.balance:,.2f}")
    print(f"总收益: ${bot.balance - bot.initial_balance:+,.2f}")
    print(f"总交易次数: {len(bot.trade_history)}")


def example_4_vote_analysis():
    """示例 4: 投票详情分析"""
    print("\n" + "=" * 80)
    print("示例 4: 指标投票详情分析")
    print("=" * 80)

    # 模拟市场数据
    n = 500
    high = [50000.0 + i * 10 for i in range(n)]
    low = [49000.0 + i * 10 for i in range(n)]
    close = [49500.0 + i * 10 for i in range(n)]
    volume = [100.0] * n

    result = haze.lt_indicator(high, low, close, volume)
    ensemble = result["ensemble"]

    print(f"\n最终信号: {ensemble['final_signal']}")
    print(f"置信度: {ensemble['confidence']:.1%}")
    print(f"市场状态: {result.get('market_regime', 'UNKNOWN')}")

    # 分析 BUY 票
    print(f"\n🟢 BUY 票 ({len(ensemble['buy_votes'])} 个):")
    for vote in ensemble["buy_votes"]:
        print(f"  - {vote['indicator']}: "
              f"强度 {vote['strength']:.2f} × 权重 {vote['weight']:.2f} "
              f"= 贡献 {vote['weighted_contribution']:.3f}")

    # 分析 SELL 票
    print(f"\n🔴 SELL 票 ({len(ensemble['sell_votes'])} 个):")
    for vote in ensemble["sell_votes"]:
        print(f"  - {vote['indicator']}: "
              f"强度 {vote['strength']:.2f} × 权重 {vote['weight']:.2f} "
              f"= 贡献 {vote['weighted_contribution']:.3f}")

    # 分析 NEUTRAL 票
    print(f"\n⚪ NEUTRAL 票 ({len(ensemble['neutral_votes'])} 个):")
    for vote in ensemble["neutral_votes"][:3]:  # 只显示前 3 个
        print(f"  - {vote['indicator']}: 强度 {vote['strength']:.2f}")


# ============================================================================
# 主程序 - Main Program
# ============================================================================

if __name__ == "__main__":
    print("\n" + "╔" + "=" * 78 + "╗")
    print("║" + " " * 20 + "LT 指标交易系统集成示例" + " " * 20 + "║")
    print("╚" + "=" * 78 + "╝")

    # 运行所有示例
    example_1_quick_start()
    example_2_with_risk_management()
    example_3_trading_bot()
    example_4_vote_analysis()

    print("\n" + "=" * 80)
    print("✅ 所有示例运行完成")
    print("=" * 80)
    print("\n💡 提示:")
    print("   1. 实盘使用时，用交易所 API 替换模拟数据")
    print("   2. 建议在模拟盘先测试至少 1 个月")
    print("   3. 根据实际资产和风险偏好调整参数")
    print("   4. 始终设置止损，控制单笔亏损在 2% 以内")
    print("   5. 关注市场状态(TRENDING/RANGING/VOLATILE)调整策略")
