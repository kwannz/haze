from __future__ import annotations

import importlib
import os
import sys
from pathlib import Path
from types import ModuleType
from typing import Optional, Tuple


def _add_candidate_path(path: str) -> Optional[str]:
    if not path:
        return None

    p = Path(path).expanduser().resolve()
    if p.is_dir() and (p / "pandas_ta_classic").is_dir():
        if str(p) not in sys.path:
            sys.path.insert(0, str(p))
        return str(p)

    if p.is_dir() and p.name == "pandas_ta_classic":
        parent = str(p.parent)
        if parent not in sys.path:
            sys.path.insert(0, parent)
        return parent

    return None


def _default_candidates() -> Tuple[str, ...]:
    root = Path(__file__).resolve().parents[1]
    return (
        str(root / "pandas-ta-kw-main"),
        str(root / "pandas-ta-kw"),
        str(root / "vendor" / "pandas-ta-kw"),
    )


def import_pandas_ta_kw() -> Tuple[Optional[ModuleType], Optional[str], bool]:
    root = Path(__file__).resolve().parents[1]
    used_path = None
    custom_loaded = False
    module: Optional[ModuleType] = None

    try:
        module = importlib.import_module("pandas_ta_classic")
    except ModuleNotFoundError:
        pass

    if module is None:
        env_path = os.getenv("PANDAS_TA_KW_PATH") or os.getenv("PANDAS_TA_KW_HOME")
        used_path = _add_candidate_path(env_path) or used_path

        if used_path is None:
            for candidate in _default_candidates():
                used_path = _add_candidate_path(candidate)
                if used_path:
                    break

        if used_path is None:
            return None, None, False

        try:
            module = importlib.import_module("pandas_ta_classic")
        except ModuleNotFoundError:
            return None, used_path, False

    custom_dir = os.getenv("PANDAS_TA_KW_CUSTOM_DIR")
    if not custom_dir:
        default_custom = root / "tests" / "pandas_ta_kw_custom"
        if default_custom.is_dir():
            custom_dir = str(default_custom)
    if custom_dir:
        try:
            custom_module = importlib.import_module("pandas_ta_classic.custom")
            custom_module.import_dir(custom_dir, verbose=False)
            custom_loaded = True
        except Exception:
            custom_loaded = False

    return module, used_path, custom_loaded
