"""
Haze-Library 精度验证测试模块
==============================

验证策略:
- TA-Lib: 金标准对比 (C 实现, 行业标准)
- pandas-ta: 补充验证 (Python 实现, 功能完整)
- 手动计算: 边界情况验证

精度要求:
- 默认阈值: 1e-9 (纳米级精度)
- 相关系数: > 0.99999
- 通过率: 100%
"""

from .core import (
    IndicatorValidator,
    ValidationResult,
    ComparisonMetrics,
    generate_market_data,
    TOLERANCE_NANO,
    TOLERANCE_MICRO,
    TOLERANCE_MILLI,
)

__all__ = [
    "IndicatorValidator",
    "ValidationResult",
    "ComparisonMetrics",
    "generate_market_data",
    "TOLERANCE_NANO",
    "TOLERANCE_MICRO",
    "TOLERANCE_MILLI",
]
