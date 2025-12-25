"""
Validation 测试配置
===================

提供共享的 fixtures 和测试配置
"""

import sys
from pathlib import Path
import pytest
import warnings

TESTS_ROOT = Path(__file__).resolve().parents[1]
if str(TESTS_ROOT) not in sys.path:
    sys.path.insert(0, str(TESTS_ROOT))

from pandas_ta_compat import import_pandas_ta

_PANDAS_TA_MODULE, _PANDAS_TA_STUB = import_pandas_ta()

# 忽略 pandas 和 numpy 的 FutureWarning
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)


def pytest_configure(config):
    """配置自定义 markers"""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "talib: marks tests that require TA-Lib"
    )
    config.addinivalue_line(
        "markers", "pandas_ta: marks tests that require pandas-ta"
    )


def pytest_collection_modifyitems(config, items):
    """自动添加 skip markers"""
    try:
        import talib
        has_talib = True
    except ImportError:
        has_talib = False

    has_pandas_ta = _PANDAS_TA_MODULE is not None

    try:
        import haze_library
        has_haze = True
    except ImportError:
        has_haze = False

    skip_talib = pytest.mark.skip(reason="TA-Lib not installed")
    skip_pandas_ta = pytest.mark.skip(reason="pandas-ta not installed")
    skip_haze = pytest.mark.skip(reason="haze-library not installed")

    for item in items:
        # 基于类名自动标记
        if "VsTaLib" in item.nodeid and not has_talib:
            item.add_marker(skip_talib)
        if "VsPandasTa" in item.nodeid and not has_pandas_ta:
            item.add_marker(skip_pandas_ta)
        if not has_haze:
            item.add_marker(skip_haze)
