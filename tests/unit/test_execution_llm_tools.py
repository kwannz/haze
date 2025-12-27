from __future__ import annotations


import pytest

from haze_library.execution import llm_tools
from haze_library.execution.errors import ExecutionPermissionError
from haze_library.execution.models import (
    AmendOrderRequest,
    CancelOrderRequest,
    CreateOrderRequest,
    Order,
    OrderSide,
    OrderType,
)


class DummyProvider:
    def __init__(
        self,
        *,
        exchange_id: str,
        api_key: str,
        api_secret: str,
        password: str | None = None,
        sandbox: bool = False,
        enable_rate_limit: bool = True,
        options=None,
        params=None,
    ) -> None:
        self._exchange_id = exchange_id
        self.supports_amend = True
        self._reference_price = 10.0

    @property
    def name(self) -> str:
        return f"dummy:{self._exchange_id}"

    @classmethod
    def options_from_env_json(cls, value: str | None) -> dict:
        return {"opt": True} if value else {}

    def create_order(self, req: CreateOrderRequest) -> Order:
        return Order(
            id="dummy_order",
            symbol=req.symbol,
            side=req.side,
            order_type=req.order_type,
            amount=req.amount,
            price=req.price,
        )

    def cancel_order(self, req: CancelOrderRequest) -> Order:
        return Order(id=req.order_id, symbol=req.symbol)

    def amend_order(self, req: AmendOrderRequest) -> Order:
        return Order(id=req.order_id, symbol=req.symbol)

    def fetch_order(self, order_id: str, *, symbol: str | None = None) -> Order:
        return Order(id=order_id, symbol=symbol, side=OrderSide.BUY, order_type=OrderType.LIMIT)

    def get_positions(self, *, symbol: str | None = None):
        return []

    def get_balances(self):
        return []

    def get_open_orders(self, *, symbol: str | None = None):
        return []

    def get_reference_price(self, symbol: str):
        return self._reference_price


def test_parse_helpers(monkeypatch) -> None:
    assert llm_tools._parse_bool("true") is True
    assert llm_tools._parse_bool("0") is False
    assert llm_tools._parse_bool(None) is False

    assert llm_tools._parse_csv_set("BTC/USDT, ETH/USDT") == {"BTC/USDT", "ETH/USDT"}
    assert llm_tools._parse_csv_set("") is None

    assert llm_tools._parse_float("1.5") == 1.5
    assert llm_tools._parse_float(" ") is None
    assert llm_tools._parse_float(None) is None

    monkeypatch.setenv("FOO", "bar")
    assert llm_tools._get_env("FOO") == "bar"
    assert llm_tools._get_env("MISSING", "FOO") == "bar"


def test_default_engine_and_actions(monkeypatch) -> None:
    monkeypatch.setenv("HAZE_EXCHANGE_ID", "binance")
    monkeypatch.setenv("HAZE_EXCHANGE_API_KEY", "k")
    monkeypatch.setenv("HAZE_EXCHANGE_SECRET", "s")
    monkeypatch.setenv("HAZE_EXECUTION_SCOPES", "read,trade,cancel,amend")
    monkeypatch.setenv("HAZE_LIVE_TRADING", "1")
    monkeypatch.setenv("HAZE_ALLOWED_SYMBOLS", "BTC/USDT")
    monkeypatch.setenv("HAZE_MAX_NOTIONAL_PER_ORDER", "100")
    monkeypatch.setenv("HAZE_CCXT_OPTIONS", "{\"opt\": true}")

    llm_tools.reset_default_engine()
    monkeypatch.setattr(llm_tools, "CCXTExecutionProvider", DummyProvider)

    engine = llm_tools.get_default_engine()
    caps = engine.capabilities()
    assert caps["provider"] == "dummy:binance"
    assert caps["live_trading"] is True

    out = llm_tools.place_order(
        symbol="BTC/USDT",
        side="buy",
        order_type="limit",
        amount=1.0,
        price=10.0,
        dry_run=True,
    )
    assert "order" in out

    cancel = llm_tools.cancel_order(order_id="1", dry_run=True)
    assert "order" in cancel

    amend = llm_tools.amend_order(order_id="1", price=11.0, dry_run=True)
    assert "order" in amend

    assert llm_tools.get_positions() == {"positions": []}
    assert llm_tools.get_balances() == {"balances": []}
    assert llm_tools.get_open_orders() == {"open_orders": []}


def test_assert_live_ready(monkeypatch) -> None:
    monkeypatch.setenv("HAZE_EXCHANGE_ID", "binance")
    monkeypatch.setenv("HAZE_EXCHANGE_API_KEY", "k")
    monkeypatch.setenv("HAZE_EXCHANGE_SECRET", "s")
    monkeypatch.setenv("HAZE_EXECUTION_SCOPES", "read")
    monkeypatch.setenv("HAZE_LIVE_TRADING", "0")

    llm_tools.reset_default_engine()
    monkeypatch.setattr(llm_tools, "CCXTExecutionProvider", DummyProvider)

    with pytest.raises(ExecutionPermissionError):
        llm_tools.assert_live_ready()
