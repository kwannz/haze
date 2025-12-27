"""
核心验证器 - 精度对比引擎
==========================

设计原则 (SOLID + KISS):
- 单一职责: 每个类只做一件事
- 开闭原则: 易于扩展新指标, 无需修改核心逻辑
- 简单直接: 最小化抽象层次
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Tuple
from enum import Enum
import warnings

warnings.filterwarnings("ignore")

# ==================== 精度常量 ====================

TOLERANCE_NANO = 1e-9   # 纳米级 (金融计算标准)
TOLERANCE_MICRO = 1e-6  # 微级 (一般精度)
TOLERANCE_MILLI = 1e-3  # 毫级 (宽松精度)


class ReferenceLibrary(Enum):
    """参考库枚举"""
    TALIB = "TA-Lib"
    PANDAS_TA = "pandas-ta"
    MANUAL = "manual"


@dataclass
class ComparisonMetrics:
    """对比指标"""
    mae: float          # 平均绝对误差
    rmse: float         # 均方根误差
    max_error: float    # 最大误差
    correlation: float  # 皮尔逊相关系数
    pass_rate: float    # 通过率
    valid_count: int    # 有效数据点数
    total_count: int    # 总数据点数

    def is_passed(
        self,
        tolerance: float = TOLERANCE_NANO,
        min_correlation: float = 0.99999,
        use_correlation_only: bool = False
    ) -> bool:
        """
        判断是否通过验证

        Args:
            tolerance: 最大误差阈值
            min_correlation: 最小相关系数要求
            use_correlation_only: 仅使用相关系数判断 (用于算法差异场景)
        """
        if use_correlation_only:
            return self.correlation > min_correlation
        return self.max_error < tolerance and self.correlation > min_correlation

    def __str__(self) -> str:
        status = "PASS" if self.is_passed() else "FAIL"
        return (
            f"[{status}] MAE={self.mae:.2e} RMSE={self.rmse:.2e} "
            f"MaxErr={self.max_error:.2e} Corr={self.correlation:.8f} "
            f"PassRate={self.pass_rate:.2%} ({self.valid_count}/{self.total_count})"
        )


@dataclass
class ValidationResult:
    """验证结果"""
    indicator_name: str
    reference_lib: ReferenceLibrary
    metrics: Optional[ComparisonMetrics] = None
    error: Optional[str] = None
    haze_result: Optional[np.ndarray] = None
    reference_result: Optional[np.ndarray] = None

    @property
    def passed(self) -> bool:
        if self.error:
            return False
        if self.metrics is None:
            return False
        return self.metrics.is_passed()

    def __str__(self) -> str:
        if self.error:
            return f"[ERROR] {self.indicator_name}: {self.error}"
        return f"{self.indicator_name} vs {self.reference_lib.value}: {self.metrics}"


class IndicatorValidator:
    """
    指标验证器

    使用示例:
        validator = IndicatorValidator(tolerance=1e-9)
        result = validator.validate(
            name="RSI",
            haze_fn=lambda: haze.py_rsi(close, 14),
            ref_fn=lambda: talib.RSI(close, timeperiod=14),
            ref_lib=ReferenceLibrary.TALIB
        )
        assert result.passed
    """

    def __init__(self, tolerance: float = TOLERANCE_NANO):
        self.tolerance = tolerance
        self.results: List[ValidationResult] = []

    def _compute_metrics(
        self,
        haze_arr: np.ndarray,
        ref_arr: np.ndarray
    ) -> ComparisonMetrics:
        """计算对比指标"""
        # 处理 NaN: 仅比较两者都有效的位置
        valid_mask = ~(np.isnan(haze_arr) | np.isnan(ref_arr))
        valid_count = int(np.sum(valid_mask))
        total_count = len(haze_arr)

        if valid_count == 0:
            return ComparisonMetrics(
                mae=float("nan"),
                rmse=float("nan"),
                max_error=float("nan"),
                correlation=float("nan"),
                pass_rate=0.0,
                valid_count=0,
                total_count=total_count,
            )

        h_valid = haze_arr[valid_mask]
        r_valid = ref_arr[valid_mask]
        errors = np.abs(h_valid - r_valid)

        mae = float(np.mean(errors))
        rmse = float(np.sqrt(np.mean(errors**2)))
        max_error = float(np.max(errors))

        # 相关系数
        if valid_count > 1 and np.std(h_valid) > 0 and np.std(r_valid) > 0:
            correlation = float(np.corrcoef(h_valid, r_valid)[0, 1])
        else:
            correlation = 1.0 if np.allclose(h_valid, r_valid, atol=self.tolerance) else 0.0

        pass_count = int(np.sum(errors < self.tolerance))
        pass_rate = pass_count / valid_count

        return ComparisonMetrics(
            mae=mae,
            rmse=rmse,
            max_error=max_error,
            correlation=correlation,
            pass_rate=pass_rate,
            valid_count=valid_count,
            total_count=total_count,
        )

    def validate(
        self,
        name: str,
        haze_fn: Callable[[], Any],
        ref_fn: Callable[[], Any],
        ref_lib: ReferenceLibrary = ReferenceLibrary.TALIB,
    ) -> ValidationResult:
        """
        验证单个指标

        Args:
            name: 指标名称
            haze_fn: haze-library 计算函数 (无参 lambda)
            ref_fn: 参考库计算函数 (无参 lambda)
            ref_lib: 参考库类型

        Returns:
            ValidationResult
        """
        try:
            haze_raw = haze_fn()
            ref_raw = ref_fn()

            # 标准化为 numpy 数组
            haze_arr = self._to_array(haze_raw)
            ref_arr = self._to_array(ref_raw)

            # 长度对齐 (取最小长度)
            min_len = min(len(haze_arr), len(ref_arr))
            haze_arr = haze_arr[:min_len]
            ref_arr = ref_arr[:min_len]

            metrics = self._compute_metrics(haze_arr, ref_arr)

            result = ValidationResult(
                indicator_name=name,
                reference_lib=ref_lib,
                metrics=metrics,
                haze_result=haze_arr,
                reference_result=ref_arr,
            )

        except Exception as e:
            result = ValidationResult(
                indicator_name=name,
                reference_lib=ref_lib,
                error=str(e),
            )

        self.results.append(result)
        return result

    def validate_multi_output(
        self,
        name: str,
        haze_fn: Callable[[], Tuple],
        ref_fn: Callable[[], Tuple],
        output_names: List[str],
        ref_lib: ReferenceLibrary = ReferenceLibrary.TALIB,
    ) -> List[ValidationResult]:
        """
        验证多输出指标 (如 MACD, Bollinger Bands)

        Args:
            name: 指标基础名称
            haze_fn: haze 函数 (返回元组)
            ref_fn: 参考函数 (返回元组)
            output_names: 各输出名称, 如 ["line", "signal", "histogram"]
            ref_lib: 参考库

        Returns:
            List[ValidationResult]
        """
        results = []
        try:
            haze_outputs = haze_fn()
            ref_outputs = ref_fn()

            for i, out_name in enumerate(output_names):
                full_name = f"{name}_{out_name}"
                h = self._to_array(haze_outputs[i])
                r = self._to_array(ref_outputs[i])

                min_len = min(len(h), len(r))
                h = h[:min_len]
                r = r[:min_len]

                metrics = self._compute_metrics(h, r)
                result = ValidationResult(
                    indicator_name=full_name,
                    reference_lib=ref_lib,
                    metrics=metrics,
                    haze_result=h,
                    reference_result=r,
                )
                self.results.append(result)
                results.append(result)

        except Exception as e:
            for out_name in output_names:
                result = ValidationResult(
                    indicator_name=f"{name}_{out_name}",
                    reference_lib=ref_lib,
                    error=str(e),
                )
                self.results.append(result)
                results.append(result)

        return results

    def _to_array(self, data: Any) -> np.ndarray:
        """转换为 numpy 数组"""
        if isinstance(data, np.ndarray):
            return data.astype(np.float64)
        if isinstance(data, pd.Series):
            return data.values.astype(np.float64)
        if isinstance(data, (list, tuple)):
            return np.array(data, dtype=np.float64)
        return np.array([data], dtype=np.float64)

    def summary(self) -> Dict[str, Any]:
        """生成汇总报告"""
        total = len(self.results)
        passed = sum(1 for r in self.results if r.passed)
        failed = total - passed

        by_lib: Dict[str, Dict[str, int]] = {}
        for r in self.results:
            lib = r.reference_lib.value
            if lib not in by_lib:
                by_lib[lib] = {"total": 0, "passed": 0}
            by_lib[lib]["total"] += 1
            if r.passed:
                by_lib[lib]["passed"] += 1

        return {
            "total": total,
            "passed": passed,
            "failed": failed,
            "pass_rate": passed / total if total > 0 else 0.0,
            "by_library": by_lib,
            "tolerance": self.tolerance,
        }

    def report(self) -> str:
        """生成文本报告"""
        s = self.summary()
        lines = [
            "=" * 70,
            " Haze-Library Precision Validation Report",
            "=" * 70,
            f" Total: {s['total']} | Passed: {s['passed']} | Failed: {s['failed']}",
            f" Pass Rate: {s['pass_rate']:.2%} | Tolerance: {s['tolerance']:.1e}",
            "-" * 70,
        ]

        for r in self.results:
            status = "PASS" if r.passed else "FAIL"
            if r.error:
                lines.append(f"[{status}] {r.indicator_name}: ERROR - {r.error}")
            else:
                m = r.metrics
                lines.append(
                    f"[{status}] {r.indicator_name} vs {r.reference_lib.value}: "
                    f"MaxErr={m.max_error:.2e} Corr={m.correlation:.8f}"
                )

        lines.append("=" * 70)
        return "\n".join(lines)


def generate_market_data(
    n: int = 500,
    seed: int = 42,
    base_price: float = 100.0,
    volatility: float = 0.02,
) -> pd.DataFrame:
    """
    生成模拟市场数据

    Args:
        n: 数据点数量
        seed: 随机种子 (确保可重复)
        base_price: 基础价格
        volatility: 波动率

    Returns:
        DataFrame with columns: open, high, low, close, volume
    """
    np.random.seed(seed)

    # 随机游走收盘价
    returns = np.random.normal(0.0001, volatility, n)
    close = base_price * np.exp(np.cumsum(returns))

    # OHLC
    high = close * (1 + np.abs(np.random.normal(0, volatility * 0.5, n)))
    low = close * (1 - np.abs(np.random.normal(0, volatility * 0.5, n)))
    open_ = np.roll(close, 1)
    open_[0] = close[0]

    # 确保 OHLC 约束
    high = np.maximum(high, np.maximum(open_, close))
    low = np.minimum(low, np.minimum(open_, close))

    # 成交量
    volume = np.random.lognormal(10, 1, n)

    return pd.DataFrame({
        "open": open_,
        "high": high,
        "low": low,
        "close": close,
        "volume": volume,
    })
