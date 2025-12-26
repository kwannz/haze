from __future__ import annotations

import importlib
import importlib.machinery
import sys
from types import ModuleType
from typing import Optional, Tuple


def _numba_stub() -> ModuleType:
    stub = ModuleType("numba")
    stub.__spec__ = importlib.machinery.ModuleSpec("numba", loader=None)

    def _passthrough(*args, **kwargs):
        if args and callable(args[0]) and len(args) == 1 and not kwargs:
            return args[0]

        def decorator(func):
            return func

        return decorator

    stub.njit = _passthrough
    stub.jit = _passthrough
    return stub


def ensure_numba_stub() -> bool:
    return ensure_numba_stub_force(force=False)


def ensure_numba_stub_force(*, force: bool) -> bool:
    if not force and "numba" in sys.modules:
        return False

    if not force:
        try:
            importlib.import_module("numba")
            return False
        except Exception:
            pass

    sys.modules["numba"] = _numba_stub()
    return True


def import_pandas_ta() -> Tuple[Optional[ModuleType], bool]:
    try:
        return importlib.import_module("pandas_ta"), False
    except Exception as exc:
        if isinstance(exc, ModuleNotFoundError):
            if exc.name != "numba":
                return None, False
        else:
            # pandas-ta can fail to import when its optional dependency `numba`
            # is present but broken (e.g. NumPy/Numba version mismatch). In that
            # case we treat `numba` as unavailable and fall back to a stub so the
            # rest of the suite can run.
            if "numba" not in str(exc).lower():
                return None, False

    stubbed = ensure_numba_stub_force(force=True)
    try:
        return importlib.import_module("pandas_ta"), stubbed
    except Exception:
        return None, stubbed
