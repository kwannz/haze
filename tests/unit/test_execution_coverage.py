from __future__ import annotations

from dataclasses import replace

import pytest

from haze_library.execution.engine import ExecutionEngine
from haze_library.execution.errors import (
    ExecutionPermissionError,
    ExecutionProviderError,
    ExecutionRiskError,
)
from haze_library.execution.models import (
    AmendOrderRequest,
    Balance,
    CancelOrderRequest,
    CreateOrderRequest,
    Order,
    OrderSide,
    OrderType,
    Position,
)
from haze_library.execution.permissions import ExecutionPermissions, Scope
from haze_library.execution.providers.base import ExecutionProvider
from haze_library.execution.providers.memory import InMemoryExecutionProvider
from haze_library.execution.risk import validate_create_order_request


def test_permissions_and_models() -> None:
    perms = ExecutionPermissions.from_scopes(["read", Scope.TRADE], live_trading=True)
    assert perms.is_symbol_allowed("BTC/USDT")

    with pytest.raises(ExecutionPermissionError):
        perms.require(Scope.CANCEL)

    order = Order(id="1")
    data = order.to_dict()
    assert data["side"] is None
    assert data["type"] is None

    balance = Balance(asset="USD", free=1.0)
    assert balance.to_dict()["asset"] == "USD"

    position = Position(symbol="BTC/USDT", size=1.0)
    assert position.to_dict()["symbol"] == "BTC/USDT"


def test_execution_error_str() -> None:
    assert str(ExecutionPermissionError("nope")) == "nope"
    assert str(ExecutionRiskError("risk")) == "risk"
    assert str(ExecutionProviderError("bad")) == "bad"
    assert str(ExecutionProviderError("bad", provider="ccxt")) == "ccxt: bad"


def test_validate_create_order_request_branches() -> None:
    perms = ExecutionPermissions.from_scopes([Scope.TRADE], allowed_symbols={"BTC/USDT"})
    req = CreateOrderRequest(
        symbol="BTC/USDT",
        side=OrderSide.BUY,
        order_type=OrderType.MARKET,
        amount=1.0,
    )

    assert validate_create_order_request(req, perms) is None

    with pytest.raises(ExecutionRiskError):
        validate_create_order_request(
            CreateOrderRequest(
                symbol="BTC/USDT",
                side=OrderSide.BUY,
                order_type=OrderType.MARKET,
                amount=0.0,
            ),
            perms,
        )

    with pytest.raises(ExecutionRiskError):
        validate_create_order_request(
            CreateOrderRequest(
                symbol="BTC/USDT",
                side=OrderSide.BUY,
                order_type=OrderType.LIMIT,
                amount=1.0,
                price=0.0,
            ),
            perms,
        )

    with pytest.raises(ExecutionRiskError):
        validate_create_order_request(
            CreateOrderRequest(
                symbol="",
                side=OrderSide.BUY,
                order_type=OrderType.MARKET,
                amount=1.0,
            ),
            perms,
        )

    perms_deny = ExecutionPermissions.from_scopes([Scope.TRADE], allowed_symbols={"ETH/USDT"})
    with pytest.raises(ExecutionRiskError):
        validate_create_order_request(req, perms_deny)

    perms_limit = ExecutionPermissions.from_scopes(
        [Scope.TRADE], allowed_symbols={"BTC/USDT"}, max_notional_per_order=5.0
    )
    with pytest.raises(ExecutionRiskError):
        validate_create_order_request(
            CreateOrderRequest(
                symbol="BTC/USDT",
                side=OrderSide.BUY,
                order_type=OrderType.LIMIT,
                amount=2.0,
                price=10.0,
            ),
            perms_limit,
        )

    with pytest.raises(ExecutionRiskError):
        validate_create_order_request(
            CreateOrderRequest(
                symbol="BTC/USDT",
                side=OrderSide.BUY,
                order_type=OrderType.MARKET,
                amount=2.0,
            ),
            perms_limit,
            reference_price=None,
        )

    perms_limit_zero = ExecutionPermissions.from_scopes(
        [Scope.TRADE], allowed_symbols={"BTC/USDT"}, max_notional_per_order=0.0
    )
    with pytest.raises(ExecutionRiskError):
        validate_create_order_request(req, perms_limit_zero)

    perms_limit_market = ExecutionPermissions.from_scopes(
        [Scope.TRADE], allowed_symbols={"BTC/USDT"}, max_notional_per_order=1.0
    )
    with pytest.raises(ExecutionRiskError):
        validate_create_order_request(
            CreateOrderRequest(
                symbol="BTC/USDT",
                side=OrderSide.BUY,
                order_type=OrderType.MARKET,
                amount=2.0,
            ),
            perms_limit_market,
            reference_price=1.0,
        )


def test_base_provider_defaults() -> None:
    class DummyProvider(ExecutionProvider):
        @property
        def name(self) -> str:
            return "dummy"

        def create_order(self, req: CreateOrderRequest) -> Order:
            return Order(id="dummy")

        def cancel_order(self, req: CancelOrderRequest) -> Order:
            return Order(id=req.order_id)

        def fetch_order(self, order_id: str, *, symbol: str | None = None) -> Order:
            return Order(id=order_id)

        def get_open_orders(self, *, symbol: str | None = None) -> list[Order]:
            return []

        def get_balances(self) -> list[Balance]:
            return []

        def get_positions(self, *, symbol: str | None = None) -> list[Position]:
            return []

    provider = DummyProvider()
    assert provider.supports_amend is False
    assert provider.get_reference_price("BTC/USDT") is None

    with pytest.raises(NotImplementedError):
        provider.amend_order(AmendOrderRequest(order_id="1"))


def test_memory_provider_error_branches() -> None:
    provider = InMemoryExecutionProvider()

    with pytest.raises(ExecutionProviderError):
        provider.create_order(
            CreateOrderRequest(
                symbol="BTC/USDT",
                side=OrderSide.BUY,
                order_type=OrderType.LIMIT,
                amount=0.0,
                price=10.0,
            )
        )

    with pytest.raises(ExecutionProviderError):
        provider.cancel_order(CancelOrderRequest(order_id="missing"))

    with pytest.raises(ExecutionProviderError):
        provider.amend_order(AmendOrderRequest(order_id="missing", amount=1.0))

    order = provider.create_order(
        CreateOrderRequest(
            symbol="BTC/USDT",
            side=OrderSide.BUY,
            order_type=OrderType.LIMIT,
            amount=1.0,
            price=10.0,
        )
    )
    with pytest.raises(ExecutionProviderError):
        provider.amend_order(AmendOrderRequest(order_id=order.id, amount=-1.0))
    with pytest.raises(ExecutionProviderError):
        provider.amend_order(AmendOrderRequest(order_id=order.id, price=-1.0))

    with pytest.raises(ExecutionProviderError):
        provider.fetch_order(order.id, symbol="ETH/USDT")

    with pytest.raises(ExecutionProviderError):
        provider.fetch_order("missing")

    updated = provider.amend_order(AmendOrderRequest(order_id=order.id, amount=2.0))
    assert updated.amount == 2.0

    provider._orders[order.id] = replace(updated, filled=0.5, remaining=0.5)
    updated = provider.amend_order(AmendOrderRequest(order_id=order.id, amount=3.0))
    assert updated.remaining is None

    open_orders = provider.get_open_orders(symbol="BTC/USDT")
    assert len(open_orders) == 1

    assert provider.get_balances() == []
    assert provider.get_positions() == []

    assert provider.get_reference_price("BTC/USDT") is None


def test_engine_capabilities_and_collections() -> None:
    class StaticProvider(InMemoryExecutionProvider):
        def __init__(self) -> None:
            super().__init__(reference_prices={"BTC/USDT": 10.0})
            self.position_calls: list[str | None] = []
            self.order_calls: list[str | None] = []

        def get_positions(self, *, symbol: str | None = None) -> list[Position]:
            self.position_calls.append(symbol)
            return [Position(symbol=symbol or "BTC/USDT", size=1.0)]

        def get_open_orders(self, *, symbol: str | None = None) -> list[Order]:
            self.order_calls.append(symbol)
            return [Order(id="1", symbol=symbol or "BTC/USDT")]

        def get_balances(self) -> list[Balance]:
            return [Balance(asset="USD", free=1.0)]

    provider = StaticProvider()
    perms = ExecutionPermissions.from_scopes(
        [Scope.READ, Scope.TRADE, Scope.CANCEL, Scope.AMEND],
        live_trading=True,
        allowed_symbols={"BTC/USDT", "ETH/USDT"},
        max_notional_per_order=100.0,
    )
    engine = ExecutionEngine(provider=provider, permissions=perms)

    caps = engine.capabilities()
    assert caps["provider"] == "memory"
    assert caps["live_trading"] is True

    positions = engine.get_positions()
    orders = engine.get_open_orders()
    balances = engine.get_balances()

    assert len(positions) == 2
    assert len(orders) == 2
    assert len(balances) == 1

    positions = engine.get_positions(symbol="BTC/USDT")
    orders = engine.get_open_orders(symbol="BTC/USDT")
    assert len(positions) == 1
    assert len(orders) == 1


def test_engine_provider_error_passthrough() -> None:
    class ErrorProvider(InMemoryExecutionProvider):
        def create_order(self, req: CreateOrderRequest) -> Order:
            raise ExecutionProviderError("boom", provider=self.name)

    provider = ErrorProvider(reference_prices={"BTC/USDT": 10.0})
    perms = ExecutionPermissions.from_scopes(
        [Scope.TRADE], live_trading=True, allowed_symbols={"BTC/USDT"}
    )
    engine = ExecutionEngine(provider=provider, permissions=perms)

    with pytest.raises(ExecutionProviderError):
        engine.place_order(
            CreateOrderRequest(
                symbol="BTC/USDT",
                side=OrderSide.BUY,
                order_type=OrderType.MARKET,
                amount=1.0,
            ),
            dry_run=False,
        )


def test_engine_cancel_order_error_branch() -> None:
    class CancelErrorProvider(InMemoryExecutionProvider):
        def cancel_order(self, req: CancelOrderRequest) -> Order:
            raise ExecutionProviderError("cancel failed", provider=self.name)

    provider = CancelErrorProvider()
    perms = ExecutionPermissions.from_scopes([Scope.CANCEL], live_trading=True)
    engine = ExecutionEngine(provider=provider, permissions=perms)

    with pytest.raises(ExecutionProviderError):
        engine.cancel_order(CancelOrderRequest(order_id="1"), dry_run=False)


def test_engine_amend_order_branches() -> None:
    provider = InMemoryExecutionProvider()
    perms = ExecutionPermissions.from_scopes(
        [Scope.AMEND, Scope.CANCEL, Scope.TRADE], live_trading=True
    )
    engine = ExecutionEngine(provider=provider, permissions=perms)

    dry = engine.amend_order(AmendOrderRequest(order_id="1"), dry_run=True)
    assert dry.id == "1"

    class AmendErrorProvider(InMemoryExecutionProvider):
        def amend_order(self, req: AmendOrderRequest) -> Order:
            raise ExecutionProviderError("amend failed", provider=self.name)

    engine_error = ExecutionEngine(provider=AmendErrorProvider(), permissions=perms)
    with pytest.raises(ExecutionProviderError):
        engine_error.amend_order(AmendOrderRequest(order_id="1"), dry_run=False)


def test_engine_amend_fallback_missing_fields() -> None:
    class NoAmendProvider(InMemoryExecutionProvider):
        @property
        def supports_amend(self) -> bool:
            return False

        def fetch_order(self, order_id: str, *, symbol: str | None = None) -> Order:
            return Order(id=order_id, symbol=None, side=None, order_type=None)

    provider = NoAmendProvider()
    perms = ExecutionPermissions.from_scopes(
        [Scope.TRADE, Scope.CANCEL, Scope.AMEND],
        live_trading=True,
        allowed_symbols={"BTC/USDT"},
    )
    engine = ExecutionEngine(provider=provider, permissions=perms)

    with pytest.raises(ExecutionProviderError):
        engine.amend_order(AmendOrderRequest(order_id="1"), dry_run=False)


def test_engine_amend_fallback_missing_amount() -> None:
    class NoAmendProvider(InMemoryExecutionProvider):
        @property
        def supports_amend(self) -> bool:
            return False

        def fetch_order(self, order_id: str, *, symbol: str | None = None) -> Order:
            return Order(
                id=order_id,
                symbol="BTC/USDT",
                side=OrderSide.BUY,
                order_type=OrderType.LIMIT,
                amount=None,
                price=10.0,
            )

    provider = NoAmendProvider()
    perms = ExecutionPermissions.from_scopes(
        [Scope.TRADE, Scope.CANCEL, Scope.AMEND], live_trading=True
    )
    engine = ExecutionEngine(provider=provider, permissions=perms)

    with pytest.raises(ExecutionProviderError):
        engine.amend_order(AmendOrderRequest(order_id="1"), dry_run=False)


def test_engine_amend_fallback_dry_run() -> None:
    class NoAmendProvider(InMemoryExecutionProvider):
        @property
        def supports_amend(self) -> bool:
            return False

        def fetch_order(self, order_id: str, *, symbol: str | None = None) -> Order:
            return Order(
                id=order_id,
                symbol="BTC/USDT",
                side=OrderSide.BUY,
                order_type=OrderType.LIMIT,
                amount=1.0,
                price=10.0,
            )

    provider = NoAmendProvider()
    perms = ExecutionPermissions.from_scopes(
        [Scope.TRADE, Scope.CANCEL, Scope.AMEND], live_trading=True
    )
    engine = ExecutionEngine(provider=provider, permissions=perms)
    dry = engine.amend_order(AmendOrderRequest(order_id="1"), dry_run=True)
    assert dry.id == "DRY_RUN_AMEND"
