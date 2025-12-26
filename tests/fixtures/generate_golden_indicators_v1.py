#!/usr/bin/env python3
"""
Generate golden indicator fixtures for regression testing.

This script overwrites `tests/fixtures/golden_indicators_v1.json`.
Run it only when you intentionally change indicator algorithms and want to
update the pinned expected outputs.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import haze_library as hz


def _to_jsonable(value):
    if isinstance(value, (list, tuple)):
        return [_to_jsonable(v) for v in value]
    if value is None:
        return None
    if isinstance(value, (int, float)):
        f = float(value)
        return None if math.isnan(f) else f
    return value


def main() -> int:
    base = [
        100.0,
        101.0,
        102.0,
        101.5,
        103.0,
        102.5,
        104.0,
        103.5,
        105.0,
        104.5,
        106.0,
        105.5,
        107.0,
        106.5,
        108.0,
        107.5,
        109.0,
        108.5,
        110.0,
        109.5,
        108.0,
        107.0,
        106.0,
        105.0,
        104.0,
        105.0,
        106.0,
        107.0,
        108.0,
        109.0,
    ]
    close = base + [c + 10.0 for c in base]
    open_ = [c - 0.2 for c in close]
    high = [c + 1.0 for c in close]
    low = [c - 1.0 for c in close]
    volume = [1000.0 + i * 10.0 for i in range(len(close))]

    expected = {
        "py_sma": {"params": {"period": 5}, "output": _to_jsonable(hz.py_sma(close, 5))},
        "py_ema": {"params": {"period": 5}, "output": _to_jsonable(hz.py_ema(close, 5))},
        "py_rsi": {"params": {"period": 14}, "output": _to_jsonable(hz.py_rsi(close, 14))},
        "py_macd": {
            "params": {"fast_period": 12, "slow_period": 26, "signal_period": 9},
            "output": _to_jsonable(hz.py_macd(close, 12, 26, 9)),
        },
        "py_bollinger_bands": {
            "params": {"period": 20, "std_multiplier": 2.0},
            "output": _to_jsonable(hz.py_bollinger_bands(close, 20, 2.0)),
        },
        "py_atr": {"params": {"period": 14}, "output": _to_jsonable(hz.py_atr(high, low, close, 14))},
        "py_supertrend": {
            "params": {"period": 10, "multiplier": 3.0},
            "output": _to_jsonable(hz.py_supertrend(high, low, close, 10, 3.0)),
        },
        "py_vwap": {
            "params": {"period": 0},
            "output": _to_jsonable(hz.py_vwap(high, low, close, volume, 0)),
        },
        "py_correlation": {
            "params": {"period": 10},
            "output": _to_jsonable(hz.py_correlation(close, volume, 10)),
        },
        "py_zscore": {"params": {"period": 10}, "output": _to_jsonable(hz.py_zscore(close, 10))},
    }

    payload = {
        "schema_version": 1,
        "haze_library_version": getattr(hz, "__version__", None),
        "inputs": {
            "open": open_,
            "high": high,
            "low": low,
            "close": close,
            "volume": volume,
        },
        "expected": expected,
    }

    out_path = Path(__file__).with_name("golden_indicators_v1.json")
    out_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Wrote {out_path} ({out_path.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
