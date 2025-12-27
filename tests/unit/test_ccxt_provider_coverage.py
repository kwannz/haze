from __future__ import annotations

import types

import pytest

from haze_library.execution.errors import ExecutionProviderError
from haze_library.execution.models import (
    AmendOrderRequest,
    CancelOrderRequest,
    CreateOrderRequest,
    Order,
    OrderSide,
    OrderStatus,
    OrderType,
)
from haze_library.execution.providers import ccxt_provider as cp


class FakeExchange:
    def __init__(self, config):
        self.config = config
        self.options = {"defaultSubType": "inverse"}
        self.has = {"editOrder": True, "fetchPositions": True}
        self.last_open_params = None
        self.last_position_params = None

    def set_sandbox_mode(self, enabled):
        self.sandbox = enabled

    def _order(self, symbol, order_type, side, amount, price, status="open"):
        return {
            "id": "order_1",
            "symbol": symbol,
            "side": side,
            "type": order_type,
            "status": status,
            "amount": amount,
            "filled": 0.0,
            "remaining": amount,
            "price": price,
            "average": price,
            "clientOrderId": "client_1",
            "timestamp": 1700000000000,
            "info": {"exchange": "fake"},
        }

    def create_order(self, symbol, order_type, side, amount, price, params):
        return self._order(symbol, order_type, side, amount, price)

    def cancel_order(self, order_id, symbol, params):
        return self._order(symbol, "limit", "buy", 1.0, 10.0, status="canceled")

    def edit_order(self, order_id, symbol, order_type, side, amount, price, params):
        return self._order(symbol, order_type, side, amount, price, status="open")

    def fetch_order(self, order_id, symbol):
        return self._order(symbol or "BTC/USDT", "limit", "buy", 1.0, 10.0, status="open")

    def fetch_open_orders(self, symbol, since, limit, params):
        self.last_open_params = params
        return [
            self._order(symbol or "BTC/USDT", "limit", "buy", 1.0, 10.0, status="open"),
        ]

    def fetch_balance(self):
        return {
            "free": {"BTC": 1.0},
            "used": {"BTC": 0.5},
            "total": {"BTC": 1.5},
        }

    def fetch_positions(self, symbols, params):
        self.last_position_params = params
        return [
            {
                "symbol": "BTC/USDT",
                "contracts": 1.0,
                "side": "long",
                "entryPrice": 100.0,
                "unrealizedPnl": 0.1,
            },
            {"symbol": ""},
            "skip",
        ]

    def fetch_ticker(self, symbol):
        return {"last": 123.45}


class SandboxFailExchange(FakeExchange):
    def set_sandbox_mode(self, enabled):
        raise RuntimeError("sandbox unsupported")


class OptionsFailExchange(FakeExchange):
    def __init__(self, config):
        super().__init__(config)

        class BadOptions:
            def get(self, *_args, **_kwargs):
                raise RuntimeError("bad options")

        self.options = BadOptions()


def _install_ccxt(monkeypatch, exchange_class=FakeExchange):
    fake_ccxt = types.SimpleNamespace(binance=exchange_class, bitget=exchange_class)
    monkeypatch.setitem(__import__("sys").modules, "ccxt", fake_ccxt)


def test_safe_float_and_mappings() -> None:
    assert cp._safe_float(None) is None
    assert cp._safe_float("1.25") == 1.25
    assert cp._safe_float("bad") is None

    assert cp._order_status_from_ccxt("open") == OrderStatus.OPEN
    assert cp._order_status_from_ccxt("filled") == OrderStatus.CLOSED
    assert cp._order_status_from_ccxt("canceled") == OrderStatus.CANCELED
    assert cp._order_status_from_ccxt("rejected") == OrderStatus.REJECTED
    assert cp._order_status_from_ccxt(123) == OrderStatus.UNKNOWN
    assert cp._order_status_from_ccxt("weird") == OrderStatus.UNKNOWN

    assert cp._order_side_from_ccxt("buy") == OrderSide.BUY
    assert cp._order_side_from_ccxt("sell") == OrderSide.SELL
    assert cp._order_side_from_ccxt(123) is None
    assert cp._order_side_from_ccxt("hold") is None

    assert cp._order_type_from_ccxt("market") == OrderType.MARKET
    assert cp._order_type_from_ccxt("limit") == OrderType.LIMIT
    assert cp._order_type_from_ccxt(123) is None
    assert cp._order_type_from_ccxt("stop") is None


def test_parse_ccxt_order() -> None:
    data = {
        "id": "1",
        "symbol": "BTC/USDT",
        "side": "buy",
        "type": "limit",
        "status": "open",
        "amount": "1.0",
        "filled": 0.0,
        "remaining": 1.0,
        "price": 10.0,
        "average": None,
        "clientOrderId": "abc",
        "timestamp": 1700000000000,
        "info": {"foo": "bar"},
    }
    order = cp._parse_ccxt_order(data)
    assert order.symbol == "BTC/USDT"
    assert order.client_order_id == "abc"

    data["info"] = "raw"
    order = cp._parse_ccxt_order(data)
    assert order.raw is not None
    assert order.raw["info"] == "raw"


def test_provider_init_options_and_sandbox_fallback(monkeypatch) -> None:
    _install_ccxt(monkeypatch, exchange_class=SandboxFailExchange)

    provider = cp.CCXTExecutionProvider(
        exchange_id="binance",
        api_key="k",
        api_secret="s",
        sandbox=True,
        options={"foo": "bar"},
        params={"adjustForTimeDifference": True},
    )

    assert provider._exchange.config["options"]["foo"] == "bar"
    assert provider._exchange.config["adjustForTimeDifference"] is True


def test_bitget_default_product_type_variants(monkeypatch) -> None:
    _install_ccxt(monkeypatch)

    provider = cp.CCXTExecutionProvider(
        exchange_id="binance",
        api_key="k",
        api_secret="s",
        sandbox=False,
    )
    assert provider._bitget_default_product_type() is None

    bitget = cp.CCXTExecutionProvider(
        exchange_id="bitget",
        api_key="k",
        api_secret="s",
        password="p",
        sandbox=False,
    )
    assert bitget._bitget_default_product_type() == "COIN-FUTURES"

    bitget._exchange.options = {}
    assert bitget._bitget_default_product_type() == "USDT-FUTURES"

    bitget_sandbox = cp.CCXTExecutionProvider(
        exchange_id="bitget",
        api_key="k",
        api_secret="s",
        password="p",
        sandbox=True,
    )
    bitget_sandbox._exchange.options = {"defaultSubType": "usdc"}
    assert bitget_sandbox._bitget_default_product_type() == "SUSDC-FUTURES"

    bitget_sandbox._exchange.options = {"defaultSubType": "foo-futures"}
    assert bitget_sandbox._bitget_default_product_type() == "FOO-FUTURES"

    _install_ccxt(monkeypatch, exchange_class=OptionsFailExchange)
    bitget = cp.CCXTExecutionProvider(
        exchange_id="bitget",
        api_key="k",
        api_secret="s",
        password="p",
        sandbox=True,
    )
    assert bitget._bitget_default_product_type() == "SUSDT-FUTURES"


def test_provider_init_errors(monkeypatch) -> None:
    _install_ccxt(monkeypatch)

    with pytest.raises(ExecutionProviderError):
        cp.CCXTExecutionProvider(exchange_id="", api_key="k", api_secret="s")

    with pytest.raises(ExecutionProviderError):
        cp.CCXTExecutionProvider(exchange_id="binance", api_key="", api_secret="s")

    with pytest.raises(ExecutionProviderError):
        cp.CCXTExecutionProvider(exchange_id="bitget", api_key="k", api_secret="s")

    fake_ccxt = types.SimpleNamespace()
    monkeypatch.setitem(__import__("sys").modules, "ccxt", fake_ccxt)
    with pytest.raises(ExecutionProviderError):
        cp.CCXTExecutionProvider(exchange_id="unknown", api_key="k", api_secret="s")


def test_provider_success_and_methods(monkeypatch) -> None:
    _install_ccxt(monkeypatch)

    provider = cp.CCXTExecutionProvider(
        exchange_id="binance",
        api_key="k",
        api_secret="s",
        sandbox=False,
    )

    order = provider.create_order(
        CreateOrderRequest(
            symbol="BTC/USDT",
            side=OrderSide.BUY,
            order_type=OrderType.LIMIT,
            amount=1.0,
            price=10.0,
        )
    )
    assert order.id

    order = provider.create_order(
        CreateOrderRequest(
            symbol="BTC/USDT",
            side=OrderSide.BUY,
            order_type=OrderType.LIMIT,
            amount=1.0,
            price=10.0,
            client_order_id="client_2",
        )
    )
    assert order.client_order_id == "client_1"

    canceled = provider.cancel_order(CancelOrderRequest(order_id="1", symbol="BTC/USDT"))
    assert canceled.status == OrderStatus.CANCELED

    amended = provider.amend_order(AmendOrderRequest(order_id="1", symbol="BTC/USDT", price=11.0))
    assert amended.id

    fetched = provider.fetch_order("1", symbol="BTC/USDT")
    assert fetched.symbol == "BTC/USDT"

    open_orders = provider.get_open_orders()
    assert len(open_orders) == 1

    balances = provider.get_balances()
    assert balances[0].asset == "BTC"

    positions = provider.get_positions()
    assert len(positions) == 1

    assert provider.get_reference_price("BTC/USDT") == pytest.approx(123.45)


def test_provider_supports_amend_and_bitget_paths(monkeypatch) -> None:
    _install_ccxt(monkeypatch)

    provider = cp.CCXTExecutionProvider(
        exchange_id="bitget",
        api_key="k",
        api_secret="s",
        password="p",
        sandbox=True,
    )
    assert provider._bitget_default_product_type().startswith("S")
    assert provider.supports_amend is True

    _ = provider.get_open_orders(symbol=None)
    assert provider._exchange.last_open_params is not None

    positions = provider.get_positions()
    assert len(positions) == 1
    assert provider._exchange.last_position_params is not None

    provider._exchange.has = {}
    assert provider.get_positions() == []


def test_provider_error_branches(monkeypatch) -> None:
    _install_ccxt(monkeypatch)
    provider = cp.CCXTExecutionProvider(
        exchange_id="binance",
        api_key="k",
        api_secret="s",
    )

    provider._exchange.has = object()
    assert provider.supports_amend is False
    provider._exchange.has = {"editOrder": True, "fetchPositions": True}

    provider._exchange.create_order = lambda *args, **kwargs: "bad"
    with pytest.raises(ExecutionProviderError):
        provider.create_order(
            CreateOrderRequest(
                symbol="BTC/USDT",
                side=OrderSide.BUY,
                order_type=OrderType.LIMIT,
                amount=1.0,
                price=10.0,
            )
        )

    provider._exchange.create_order = lambda *args, **kwargs: (_ for _ in ()).throw(RuntimeError("boom"))
    with pytest.raises(ExecutionProviderError):
        provider.create_order(
            CreateOrderRequest(
                symbol="BTC/USDT",
                side=OrderSide.BUY,
                order_type=OrderType.LIMIT,
                amount=1.0,
                price=10.0,
            )
        )

    provider._exchange.cancel_order = lambda *args, **kwargs: "bad"
    with pytest.raises(ExecutionProviderError):
        provider.cancel_order(CancelOrderRequest(order_id="1", symbol="BTC/USDT"))

    provider._exchange.cancel_order = lambda *args, **kwargs: (_ for _ in ()).throw(RuntimeError("boom"))
    with pytest.raises(ExecutionProviderError):
        provider.cancel_order(CancelOrderRequest(order_id="1", symbol="BTC/USDT"))

    provider._exchange.fetch_order = lambda *args, **kwargs: "bad"
    with pytest.raises(ExecutionProviderError):
        provider.fetch_order("1")

    provider._exchange.fetch_order = lambda *args, **kwargs: (_ for _ in ()).throw(RuntimeError("boom"))
    with pytest.raises(ExecutionProviderError):
        provider.fetch_order("1")

    provider._exchange.fetch_open_orders = lambda *args, **kwargs: "bad"
    with pytest.raises(ExecutionProviderError):
        provider.get_open_orders()

    provider._exchange.fetch_open_orders = lambda *args, **kwargs: (_ for _ in ()).throw(RuntimeError("boom"))
    with pytest.raises(ExecutionProviderError):
        provider.get_open_orders()

    provider._exchange.fetch_balance = lambda *args, **kwargs: "bad"
    with pytest.raises(ExecutionProviderError):
        provider.get_balances()

    provider._exchange.fetch_balance = lambda *args, **kwargs: (_ for _ in ()).throw(RuntimeError("boom"))
    with pytest.raises(ExecutionProviderError):
        provider.get_balances()

    provider._exchange.fetch_positions = lambda *args, **kwargs: "bad"
    with pytest.raises(ExecutionProviderError):
        provider.get_positions()

    provider._exchange.fetch_positions = lambda *args, **kwargs: (_ for _ in ()).throw(RuntimeError("boom"))
    with pytest.raises(ExecutionProviderError):
        provider.get_positions()

    provider._exchange.has = {"editOrder": False, "fetchPositions": True}
    with pytest.raises(ExecutionProviderError):
        provider.amend_order(AmendOrderRequest(order_id="1", symbol="BTC/USDT", price=11.0))

    provider._exchange.has = {"editOrder": True, "fetchPositions": True}
    provider.fetch_order = lambda *args, **kwargs: Order(id="1")
    with pytest.raises(ExecutionProviderError):
        provider.amend_order(AmendOrderRequest(order_id="1", symbol="BTC/USDT", price=11.0))

    provider.fetch_order = lambda *args, **kwargs: Order(
        id="1",
        symbol="BTC/USDT",
        side=OrderSide.BUY,
        order_type=OrderType.LIMIT,
        amount=None,
        price=10.0,
    )
    with pytest.raises(ExecutionProviderError):
        provider.amend_order(AmendOrderRequest(order_id="1", symbol="BTC/USDT", price=11.0))

    provider.fetch_order = lambda *args, **kwargs: Order(
        id="1",
        symbol="BTC/USDT",
        side=OrderSide.BUY,
        order_type=OrderType.LIMIT,
        amount=1.0,
        price=10.0,
    )
    provider._exchange.edit_order = lambda *args, **kwargs: "bad"
    with pytest.raises(ExecutionProviderError):
        provider.amend_order(AmendOrderRequest(order_id="1", symbol="BTC/USDT", price=11.0))

    provider._exchange.edit_order = lambda *args, **kwargs: (_ for _ in ()).throw(RuntimeError("boom"))
    with pytest.raises(ExecutionProviderError):
        provider.amend_order(AmendOrderRequest(order_id="1", symbol="BTC/USDT", price=11.0))

    provider._exchange.fetch_ticker = lambda *args, **kwargs: "bad"
    assert provider.get_reference_price("BTC/USDT") is None

    provider._exchange.fetch_ticker = lambda *args, **kwargs: {"last": None, "close": 12.0}
    assert provider.get_reference_price("BTC/USDT") == 12.0

    provider._exchange.fetch_ticker = lambda *args, **kwargs: (_ for _ in ()).throw(RuntimeError("boom"))
    assert provider.get_reference_price("BTC/USDT") is None


def test_options_from_env_json() -> None:
    assert cp.CCXTExecutionProvider.options_from_env_json(None) == {}
    assert cp.CCXTExecutionProvider.options_from_env_json(" ") == {}

    with pytest.raises(ValueError):
        cp.CCXTExecutionProvider.options_from_env_json("{")

    with pytest.raises(ValueError):
        cp.CCXTExecutionProvider.options_from_env_json("[1, 2]")

    assert cp.CCXTExecutionProvider.options_from_env_json("{\"a\": 1}") == {"a": 1}
