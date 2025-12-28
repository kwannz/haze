"""
Execution Engine Tests
======================

验证 execution 引擎的权限控制、风控校验、以及基础下单/撤单/改单流程。

注意：这里使用 InMemoryExecutionProvider，避免任何真实交易/网络依赖。
"""

from __future__ import annotations

import pytest

from haze_library.execution.engine import ExecutionEngine
from haze_library.execution.errors import (
    ExecutionPermissionError,
    ExecutionProviderError,
    ExecutionRiskError,
)
from haze_library.execution.models import (
    AmendOrderRequest,
    CancelOrderRequest,
    CreateOrderRequest,
    OrderSide,
    OrderType,
)
from haze_library.execution.permissions import ExecutionPermissions, Scope
from haze_library.execution.providers.memory import InMemoryExecutionProvider


class TestExecutionPermissions:
    def test_symbol_allowlist(self) -> None:
        perms = ExecutionPermissions.from_scopes(
            [Scope.READ],
            allowed_symbols={"BTC/USDT"},
        )
        assert perms.is_symbol_allowed("BTC/USDT")
        assert not perms.is_symbol_allowed("ETH/USDT")


class TestExecutionEngine:
    def _engine(self, *, live: bool, max_notional: float | None = None) -> ExecutionEngine:
        provider = InMemoryExecutionProvider(reference_prices={"BTC/USDT": 10.0})
        perms = ExecutionPermissions.from_scopes(
            [Scope.READ, Scope.TRADE, Scope.CANCEL, Scope.AMEND],
            live_trading=live,
            allowed_symbols={"BTC/USDT"},
            max_notional_per_order=max_notional,
        )
        return ExecutionEngine(provider=provider, permissions=perms)

    def test_place_order_requires_live_unless_dry_run(self) -> None:
        engine = self._engine(live=False)
        req = CreateOrderRequest(
            symbol="BTC/USDT",
            side=OrderSide.BUY,
            order_type=OrderType.LIMIT,
            amount=1.0,
            price=10.0,
        )

        _order, _notional = engine.place_order(req, dry_run=True)

        with pytest.raises(ExecutionPermissionError):
            engine.place_order(req, dry_run=False)

    def test_limit_order_notional_risk_check(self) -> None:
        engine = self._engine(live=True, max_notional=100.0)
        req = CreateOrderRequest(
            symbol="BTC/USDT",
            side=OrderSide.BUY,
            order_type=OrderType.LIMIT,
            amount=2.0,
            price=60.0,
        )
        with pytest.raises(ExecutionRiskError):
            engine.place_order(req, dry_run=False)

    def test_market_order_notional_uses_reference_price(self) -> None:
        engine = self._engine(live=True, max_notional=100.0)
        req = CreateOrderRequest(
            symbol="BTC/USDT",
            side=OrderSide.BUY,
            order_type=OrderType.MARKET,
            amount=2.0,
            price=None,
        )
        order, notional = engine.place_order(req, dry_run=False)
        assert order.id
        assert notional is not None
        assert notional.notional == pytest.approx(20.0)

    def test_cancel_and_amend(self) -> None:
        engine = self._engine(live=True)
        req = CreateOrderRequest(
            symbol="BTC/USDT",
            side=OrderSide.BUY,
            order_type=OrderType.LIMIT,
            amount=1.0,
            price=10.0,
        )
        order, _ = engine.place_order(req, dry_run=False)

        amended = engine.amend_order(
            AmendOrderRequest(order_id=order.id, symbol="BTC/USDT", price=11.0),
            dry_run=False,
        )
        assert amended.price == pytest.approx(11.0)

        canceled = engine.cancel_order(
            CancelOrderRequest(order_id=order.id, symbol="BTC/USDT"),
            dry_run=False,
        )
        assert canceled.status.value == "canceled"


class TestEngineAmendFallback:
    def test_amend_fallback_cancel_and_recreate(self) -> None:
        class NoAmendProvider(InMemoryExecutionProvider):
            @property
            def supports_amend(self) -> bool:  # type: ignore[override]
                return False

        provider = NoAmendProvider(reference_prices={"BTC/USDT": 10.0})
        perms = ExecutionPermissions.from_scopes(
            [Scope.READ, Scope.TRADE, Scope.CANCEL, Scope.AMEND],
            live_trading=True,
            allowed_symbols={"BTC/USDT"},
        )
        engine = ExecutionEngine(provider=provider, permissions=perms)

        created, _ = engine.place_order(
            CreateOrderRequest(
                symbol="BTC/USDT",
                side=OrderSide.BUY,
                order_type=OrderType.LIMIT,
                amount=1.0,
                price=10.0,
            ),
            dry_run=False,
        )

        amended = engine.amend_order(
            AmendOrderRequest(order_id=created.id, symbol="BTC/USDT", price=12.0),
            dry_run=False,
        )
        assert amended.id != created.id
        old = provider.fetch_order(created.id, symbol="BTC/USDT")
        assert old.status.value == "canceled"

    def test_amend_fallback_create_failure(self) -> None:
        class FailingCreateProvider(InMemoryExecutionProvider):
            @property
            def supports_amend(self) -> bool:  # type: ignore[override]
                return False

            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.fail_next_create = False

            def create_order(self, req: CreateOrderRequest):  # type: ignore[override]
                if self.fail_next_create:
                    raise RuntimeError("boom")
                return super().create_order(req)

        provider = FailingCreateProvider(reference_prices={"BTC/USDT": 10.0})
        perms = ExecutionPermissions.from_scopes(
            [Scope.READ, Scope.TRADE, Scope.CANCEL, Scope.AMEND],
            live_trading=True,
            allowed_symbols={"BTC/USDT"},
        )
        engine = ExecutionEngine(provider=provider, permissions=perms)

        created, _ = engine.place_order(
            CreateOrderRequest(
                symbol="BTC/USDT",
                side=OrderSide.BUY,
                order_type=OrderType.LIMIT,
                amount=1.0,
                price=10.0,
            ),
            dry_run=False,
        )

        provider.fail_next_create = True
        with pytest.raises(ExecutionProviderError, match="CRITICAL: Order"):
            engine.amend_order(
                AmendOrderRequest(order_id=created.id, symbol="BTC/USDT", price=12.0),
                dry_run=False,
            )
