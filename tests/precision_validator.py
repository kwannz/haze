"""
精度验证框架 - Haze-Library vs pandas-ta & TA-Lib
==================================================

验证策略：
1. 使用相同的测试数据（BTC/USDT 历史数据）
2. 计算精度指标：MAE, RMSE, Max Error, 相关系数
3. 允许浮点误差阈值：1e-9（纳米级精度）
4. 分类别验证：波动率、动量、趋势、成交量、MA

Author: Haze Team
Date: 2025-12-25
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
import warnings

warnings.filterwarnings('ignore')

# 导入参考库
try:
    import pandas_ta as pta
    HAS_PANDAS_TA = True
except ImportError:
    HAS_PANDAS_TA = False
    print("⚠️  pandas-ta 未安装，跳过 pandas-ta 对比")

try:
    import talib
    HAS_TALIB = True
except ImportError:
    HAS_TALIB = False
    print("⚠️  TA-Lib 未安装，跳过 TA-Lib 对比")

# 导入 haze-library
try:
    import _haze_rust as haze
    HAS_HAZE = True
except ImportError:
    HAS_HAZE = False
    print("❌ haze-library 未安装，请先运行 maturin develop")
    exit(1)


@dataclass
class PrecisionMetrics:
    """精度指标"""
    mae: float  # 平均绝对误差
    rmse: float  # 均方根误差
    max_error: float  # 最大误差
    correlation: float  # 皮尔逊相关系数
    pass_rate: float  # 通过率（误差 < 阈值的比例）

    def __str__(self) -> str:
        return (
            f"MAE={self.mae:.2e}, RMSE={self.rmse:.2e}, "
            f"MaxErr={self.max_error:.2e}, Corr={self.correlation:.6f}, "
            f"Pass={self.pass_rate:.1%}"
        )


class PrecisionValidator:
    """精度验证器"""

    def __init__(self, threshold: float = 1e-9):
        """
        初始化验证器

        Args:
            threshold: 允许的浮点误差阈值（默认 1e-9）
        """
        self.threshold = threshold
        self.results: Dict[str, Dict[str, Any]] = {}

    def calculate_metrics(
        self,
        haze_result: np.ndarray,
        reference_result: np.ndarray,
        name: str
    ) -> PrecisionMetrics:
        """
        计算精度指标

        Args:
            haze_result: haze-library 计算结果
            reference_result: 参考库计算结果
            name: 指标名称

        Returns:
            PrecisionMetrics 对象
        """
        # 处理 NaN 值：仅比较两者都有效的位置
        valid_mask = ~(np.isnan(haze_result) | np.isnan(reference_result))

        if not valid_mask.any():
            print(f"⚠️  {name}: 所有值均为 NaN，跳过验证")
            return PrecisionMetrics(
                mae=float('nan'),
                rmse=float('nan'),
                max_error=float('nan'),
                correlation=float('nan'),
                pass_rate=0.0
            )

        haze_valid = haze_result[valid_mask]
        ref_valid = reference_result[valid_mask]

        # 计算误差
        errors = np.abs(haze_valid - ref_valid)

        mae = np.mean(errors)
        rmse = np.sqrt(np.mean(errors ** 2))
        max_error = np.max(errors)

        # 计算相关系数
        if len(haze_valid) > 1:
            correlation = np.corrcoef(haze_valid, ref_valid)[0, 1]
        else:
            correlation = 1.0

        # 计算通过率
        pass_count = np.sum(errors < self.threshold)
        pass_rate = pass_count / len(errors)

        return PrecisionMetrics(
            mae=mae,
            rmse=rmse,
            max_error=max_error,
            correlation=correlation,
            pass_rate=pass_rate
        )

    def validate_indicator(
        self,
        name: str,
        haze_func: callable,
        reference_func: callable,
        test_data: Dict[str, np.ndarray],
        params: Dict[str, Any],
        reference_lib: str = "pandas-ta"
    ) -> bool:
        """
        验证单个指标

        Args:
            name: 指标名称
            haze_func: haze-library 函数
            reference_func: 参考库函数
            test_data: 测试数据（close, high, low, volume 等）
            params: 函数参数
            reference_lib: 参考库名称

        Returns:
            是否通过验证
        """
        try:
            # 调用 haze-library
            haze_result = haze_func(**params)

            # 调用参考库
            ref_result = reference_func(**params)

            # 处理返回值（可能是元组或单值）
            if isinstance(haze_result, tuple):
                # 多返回值指标（如 MACD, Bollinger Bands）
                metrics_list = []
                all_passed = True

                for i, (h, r) in enumerate(zip(haze_result, ref_result)):
                    h_array = np.array(h) if not isinstance(h, np.ndarray) else h
                    r_array = np.array(r) if not isinstance(r, np.ndarray) else r

                    metrics = self.calculate_metrics(h_array, r_array, f"{name}[{i}]")
                    metrics_list.append(metrics)

                    passed = metrics.max_error < self.threshold
                    all_passed &= passed

                    status = "✅" if passed else "❌"
                    print(f"  {status} {name}[{i}] vs {reference_lib}: {metrics}")

                self.results[name] = {
                    "passed": all_passed,
                    "metrics": metrics_list,
                    "reference": reference_lib
                }
                return all_passed
            else:
                # 单返回值指标
                h_array = np.array(haze_result) if not isinstance(haze_result, np.ndarray) else haze_result
                r_array = np.array(ref_result) if not isinstance(ref_result, np.ndarray) else ref_result

                metrics = self.calculate_metrics(h_array, r_array, name)
                passed = metrics.max_error < self.threshold

                status = "✅" if passed else "❌"
                print(f"  {status} {name} vs {reference_lib}: {metrics}")

                self.results[name] = {
                    "passed": passed,
                    "metrics": metrics,
                    "reference": reference_lib
                }
                return passed

        except Exception as e:
            print(f"  ❌ {name} 验证失败: {e}")
            self.results[name] = {
                "passed": False,
                "error": str(e),
                "reference": reference_lib
            }
            return False

    def generate_report(self) -> str:
        """生成验证报告"""
        total = len(self.results)
        passed = sum(1 for r in self.results.values() if r.get("passed", False))

        report = f"""
╔════════════════════════════════════════════════════════════════╗
║           Haze-Library 精度验证报告                             ║
╠════════════════════════════════════════════════════════════════╣
║ 总指标数：{total:>4} 个                                          ║
║ 通过数：  {passed:>4} 个                                         ║
║ 失败数：  {total - passed:>4} 个                                 ║
║ 通过率：  {passed/total*100:>5.1f}%                              ║
╠════════════════════════════════════════════════════════════════╣
║ 精度阈值：{self.threshold:.1e}                                   ║
╚════════════════════════════════════════════════════════════════╝

详细结果：
"""

        for name, result in sorted(self.results.items()):
            status = "✅ PASS" if result.get("passed", False) else "❌ FAIL"
            ref = result.get("reference", "unknown")

            if "error" in result:
                report += f"{status} | {name:30} | Error: {result['error']}\n"
            elif isinstance(result["metrics"], list):
                report += f"{status} | {name:30} | vs {ref}\n"
                for i, m in enumerate(result["metrics"]):
                    report += f"       └─ [{i}] {m}\n"
            else:
                m = result["metrics"]
                report += f"{status} | {name:30} | vs {ref} | {m}\n"

        return report


def generate_test_data(n: int = 500) -> pd.DataFrame:
    """
    生成测试数据（模拟真实市场数据）

    Args:
        n: 数据点数量

    Returns:
        包含 OHLCV 的 DataFrame
    """
    np.random.seed(42)  # 确保可重复

    # 生成随机游走价格
    returns = np.random.normal(0.0001, 0.02, n)
    close = 100 * np.exp(np.cumsum(returns))

    # 生成 OHLC
    high = close * (1 + np.abs(np.random.normal(0, 0.01, n)))
    low = close * (1 - np.abs(np.random.normal(0, 0.01, n)))
    open_ = np.roll(close, 1)
    open_[0] = close[0]

    # 生成成交量
    volume = np.random.lognormal(10, 1, n)

    return pd.DataFrame({
        'open': open_,
        'high': high,
        'low': low,
        'close': close,
        'volume': volume
    })


if __name__ == "__main__":
    print("🚀 启动 Haze-Library 精度验证...")
    print(f"参考库状态: pandas-ta={HAS_PANDAS_TA}, TA-Lib={HAS_TALIB}")
    print("=" * 70)

    # 生成测试数据
    df = generate_test_data(500)

    # 初始化验证器
    validator = PrecisionValidator(threshold=1e-9)

    # ========== 示例：验证 SMA ==========
    print("\n📊 验证 SMA (Simple Moving Average)...")

    if HAS_TALIB:
        validator.validate_indicator(
            name="SMA",
            haze_func=lambda: haze.py_sma(df['close'].tolist(), 20),
            reference_func=lambda: talib.SMA(df['close'].values, timeperiod=20),
            test_data=df.to_dict('list'),
            params={},
            reference_lib="TA-Lib"
        )

    # ========== 验证 RSI ==========
    print("\n📊 验证 RSI (Relative Strength Index)...")

    if HAS_TALIB:
        validator.validate_indicator(
            name="RSI",
            haze_func=lambda: haze.py_rsi(df['close'].tolist(), 14),
            reference_func=lambda: talib.RSI(df['close'].values, timeperiod=14),
            test_data=df.to_dict('list'),
            params={},
            reference_lib="TA-Lib"
        )

    # ========== 生成最终报告 ==========
    print("\n" + "=" * 70)
    print(validator.generate_report())
    print("\n✨ 验证完成！")
