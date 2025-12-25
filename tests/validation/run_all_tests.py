#!/usr/bin/env python3
"""
完整验证测试运行器
==================

运行所有指标验证测试并生成报告

用法:
    python run_all_tests.py              # 运行所有测试
    python run_all_tests.py --quick      # 快速测试 (跳过慢测试)
    python run_all_tests.py --report     # 生成详细报告

Author: Haze Team
Date: 2025-12-26
"""

import sys
import argparse
from pathlib import Path
from datetime import datetime

# 确保路径正确
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))
TESTS_ROOT = PROJECT_ROOT / "tests"
sys.path.insert(0, str(TESTS_ROOT))

from pandas_ta_compat import import_pandas_ta

from .core import (
    IndicatorValidator,
    ReferenceLibrary,
    generate_market_data,
    TOLERANCE_NANO,
)


def check_dependencies():
    """检查依赖状态"""
    deps = {}

    try:
        import haze_library as haze
        deps["haze-library"] = True
        deps["haze_version"] = getattr(haze, "__version__", "unknown")
    except ImportError:
        deps["haze-library"] = False
        print("ERROR: haze-library not installed!")
        print("Run: cd rust && maturin develop")
        return None

    try:
        import talib
        deps["TA-Lib"] = True
    except ImportError:
        deps["TA-Lib"] = False
        print("WARNING: TA-Lib not installed, some tests will skip")

    pta, used_stub = import_pandas_ta()
    deps["pandas-ta"] = pta is not None
    if pta is None:
        print("WARNING: pandas-ta not installed, some tests will skip")
    elif used_stub:
        print("WARNING: pandas-ta using numba stub (no JIT)")

    return deps


def run_volatility_tests(validator, df, haze, talib=None, pta=None):
    """运行波动率指标测试"""
    print("\n" + "=" * 60)
    print("VOLATILITY INDICATORS")
    print("=" * 60)

    if talib:
        # ATR
        validator.validate(
            "ATR",
            lambda: haze.py_atr(df["high"].tolist(), df["low"].tolist(), df["close"].tolist(), 14),
            lambda: talib.ATR(df["high"].values, df["low"].values, df["close"].values, timeperiod=14),
            ReferenceLibrary.TALIB
        )

        # NATR
        validator.validate(
            "NATR",
            lambda: haze.py_natr(df["high"].tolist(), df["low"].tolist(), df["close"].tolist(), 14),
            lambda: talib.NATR(df["high"].values, df["low"].values, df["close"].values, timeperiod=14),
            ReferenceLibrary.TALIB
        )

        # True Range
        validator.validate(
            "TRANGE",
            lambda: haze.py_true_range(df["high"].tolist(), df["low"].tolist(), df["close"].tolist()),
            lambda: talib.TRANGE(df["high"].values, df["low"].values, df["close"].values),
            ReferenceLibrary.TALIB
        )

        # Bollinger Bands
        validator.validate_multi_output(
            "BBANDS",
            lambda: haze.py_bollinger_bands(df["close"].tolist(), 20, 2.0),
            lambda: talib.BBANDS(df["close"].values, timeperiod=20, nbdevup=2.0, nbdevdn=2.0),
            ["upper", "middle", "lower"],
            ReferenceLibrary.TALIB
        )


def run_momentum_tests(validator, df, haze, talib=None, pta=None):
    """运行动量指标测试"""
    print("\n" + "=" * 60)
    print("MOMENTUM INDICATORS")
    print("=" * 60)

    if talib:
        # RSI
        validator.validate(
            "RSI",
            lambda: haze.py_rsi(df["close"].tolist(), 14),
            lambda: talib.RSI(df["close"].values, timeperiod=14),
            ReferenceLibrary.TALIB
        )

        # MACD
        validator.validate_multi_output(
            "MACD",
            lambda: haze.py_macd(df["close"].tolist(), 12, 26, 9),
            lambda: talib.MACD(df["close"].values, fastperiod=12, slowperiod=26, signalperiod=9),
            ["line", "signal", "histogram"],
            ReferenceLibrary.TALIB
        )

        # CCI
        validator.validate(
            "CCI",
            lambda: haze.py_cci(df["high"].tolist(), df["low"].tolist(), df["close"].tolist(), 20),
            lambda: talib.CCI(df["high"].values, df["low"].values, df["close"].values, timeperiod=20),
            ReferenceLibrary.TALIB
        )

        # MFI
        validator.validate(
            "MFI",
            lambda: haze.py_mfi(
                df["high"].tolist(), df["low"].tolist(),
                df["close"].tolist(), df["volume"].tolist(), 14
            ),
            lambda: talib.MFI(
                df["high"].values, df["low"].values,
                df["close"].values, df["volume"].values, timeperiod=14
            ),
            ReferenceLibrary.TALIB
        )

        # Williams %R
        validator.validate(
            "WILLR",
            lambda: haze.py_williams_r(df["high"].tolist(), df["low"].tolist(), df["close"].tolist(), 14),
            lambda: talib.WILLR(df["high"].values, df["low"].values, df["close"].values, timeperiod=14),
            ReferenceLibrary.TALIB
        )

        # ROC
        validator.validate(
            "ROC",
            lambda: haze.py_roc(df["close"].tolist(), 10),
            lambda: talib.ROC(df["close"].values, timeperiod=10),
            ReferenceLibrary.TALIB
        )

        # MOM
        validator.validate(
            "MOM",
            lambda: haze.py_mom(df["close"].tolist(), 10),
            lambda: talib.MOM(df["close"].values, timeperiod=10),
            ReferenceLibrary.TALIB
        )

        # CMO
        validator.validate(
            "CMO",
            lambda: haze.py_cmo(df["close"].tolist(), 14),
            lambda: talib.CMO(df["close"].values, timeperiod=14),
            ReferenceLibrary.TALIB
        )


def run_moving_average_tests(validator, df, haze, talib=None, pta=None):
    """运行移动平均线测试"""
    print("\n" + "=" * 60)
    print("MOVING AVERAGES")
    print("=" * 60)

    if talib:
        for name, period in [("SMA", 20), ("EMA", 20), ("WMA", 20), ("DEMA", 20), ("TEMA", 20)]:
            haze_fn = getattr(haze, f"py_{name.lower()}")
            talib_fn = getattr(talib, name)
            validator.validate(
                name,
                lambda fn=haze_fn, p=period: fn(df["close"].tolist(), p),
                lambda fn=talib_fn, p=period: fn(df["close"].values, timeperiod=p),
                ReferenceLibrary.TALIB
            )

        # T3
        validator.validate(
            "T3",
            lambda: haze.py_t3(df["close"].tolist(), 5, 0.7),
            lambda: talib.T3(df["close"].values, timeperiod=5, vfactor=0.7),
            ReferenceLibrary.TALIB
        )

        # KAMA
        validator.validate(
            "KAMA",
            lambda: haze.py_kama(df["close"].tolist(), 10, 2, 30),
            lambda: talib.KAMA(df["close"].values, timeperiod=10),
            ReferenceLibrary.TALIB
        )

        # TRIMA
        validator.validate(
            "TRIMA",
            lambda: haze.py_trima(df["close"].tolist(), 20),
            lambda: talib.TRIMA(df["close"].values, timeperiod=20),
            ReferenceLibrary.TALIB
        )


def run_trend_tests(validator, df, haze, talib=None, pta=None):
    """运行趋势指标测试"""
    print("\n" + "=" * 60)
    print("TREND INDICATORS")
    print("=" * 60)

    if talib:
        # ADX
        validator.validate(
            "ADX",
            lambda: haze.py_adx(df["high"].tolist(), df["low"].tolist(), df["close"].tolist(), 14),
            lambda: talib.ADX(df["high"].values, df["low"].values, df["close"].values, timeperiod=14),
            ReferenceLibrary.TALIB
        )

        # DX
        validator.validate(
            "DX",
            lambda: haze.py_dx(df["high"].tolist(), df["low"].tolist(), df["close"].tolist(), 14),
            lambda: talib.DX(df["high"].values, df["low"].values, df["close"].values, timeperiod=14),
            ReferenceLibrary.TALIB
        )

        # PLUS_DI
        validator.validate(
            "PLUS_DI",
            lambda: haze.py_plus_di(df["high"].tolist(), df["low"].tolist(), df["close"].tolist(), 14),
            lambda: talib.PLUS_DI(df["high"].values, df["low"].values, df["close"].values, timeperiod=14),
            ReferenceLibrary.TALIB
        )

        # MINUS_DI
        validator.validate(
            "MINUS_DI",
            lambda: haze.py_minus_di(df["high"].tolist(), df["low"].tolist(), df["close"].tolist(), 14),
            lambda: talib.MINUS_DI(df["high"].values, df["low"].values, df["close"].values, timeperiod=14),
            ReferenceLibrary.TALIB
        )

        # Aroon
        validator.validate_multi_output(
            "AROON",
            lambda: haze.py_aroon(df["high"].tolist(), df["low"].tolist(), 25),
            lambda: talib.AROON(df["high"].values, df["low"].values, timeperiod=25),
            ["down", "up"],
            ReferenceLibrary.TALIB
        )

        # TRIX
        validator.validate(
            "TRIX",
            lambda: haze.py_trix(df["close"].tolist(), 15),
            lambda: talib.TRIX(df["close"].values, timeperiod=15),
            ReferenceLibrary.TALIB
        )

        # SAR
        validator.validate(
            "SAR",
            lambda: haze.py_sar(df["high"].tolist(), df["low"].tolist(), 0.02, 0.2),
            lambda: talib.SAR(df["high"].values, df["low"].values, acceleration=0.02, maximum=0.2),
            ReferenceLibrary.TALIB
        )


def run_volume_tests(validator, df, haze, talib=None, pta=None):
    """运行成交量指标测试"""
    print("\n" + "=" * 60)
    print("VOLUME INDICATORS")
    print("=" * 60)

    if talib:
        # OBV
        validator.validate(
            "OBV",
            lambda: haze.py_obv(df["close"].tolist(), df["volume"].tolist()),
            lambda: talib.OBV(df["close"].values, df["volume"].values),
            ReferenceLibrary.TALIB
        )

        # AD
        validator.validate(
            "AD",
            lambda: haze.py_ad(
                df["high"].tolist(), df["low"].tolist(),
                df["close"].tolist(), df["volume"].tolist()
            ),
            lambda: talib.AD(
                df["high"].values, df["low"].values,
                df["close"].values, df["volume"].values
            ),
            ReferenceLibrary.TALIB
        )

        # ADOSC
        validator.validate(
            "ADOSC",
            lambda: haze.py_adosc(
                df["high"].tolist(), df["low"].tolist(),
                df["close"].tolist(), df["volume"].tolist(), 3, 10
            ),
            lambda: talib.ADOSC(
                df["high"].values, df["low"].values,
                df["close"].values, df["volume"].values,
                fastperiod=3, slowperiod=10
            ),
            ReferenceLibrary.TALIB
        )


def main():
    parser = argparse.ArgumentParser(description="Haze-Library Precision Validator")
    parser.add_argument("--quick", action="store_true", help="Quick test mode")
    parser.add_argument("--report", action="store_true", help="Generate detailed report")
    parser.add_argument("--output", type=str, default=None, help="Report output file")
    args = parser.parse_args()

    print("=" * 70)
    print(" HAZE-LIBRARY PRECISION VALIDATION SUITE")
    print(" Date:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("=" * 70)

    # 检查依赖
    deps = check_dependencies()
    if deps is None:
        return 1

    print("\nDependencies:")
    for name, status in deps.items():
        symbol = "" if status else ""
        print(f"  {symbol} {name}: {status}")

    # 导入库
    import haze_library as haze

    talib = None
    pta = None

    if deps.get("TA-Lib"):
        import talib as _talib
        talib = _talib

    if deps.get("pandas-ta"):
        import pandas_ta as _pta
        pta = _pta

    # 生成测试数据
    n_samples = 200 if args.quick else 500
    print(f"\nGenerating test data ({n_samples} samples)...")
    df = generate_market_data(n=n_samples, seed=42)

    # 创建验证器
    validator = IndicatorValidator(tolerance=TOLERANCE_NANO)

    # 运行测试
    run_volatility_tests(validator, df, haze, talib, pta)
    run_momentum_tests(validator, df, haze, talib, pta)
    run_moving_average_tests(validator, df, haze, talib, pta)
    run_trend_tests(validator, df, haze, talib, pta)
    run_volume_tests(validator, df, haze, talib, pta)

    # 生成报告
    report = validator.report()
    print("\n" + report)

    summary = validator.summary()
    print(f"\nFINAL RESULT: {summary['passed']}/{summary['total']} passed ({summary['pass_rate']:.1%})")

    # 保存报告
    if args.report or args.output:
        output_file = args.output or f"validation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(output_file, "w") as f:
            f.write(report)
        print(f"\nReport saved to: {output_file}")

    return 0 if summary["pass_rate"] == 1.0 else 1


if __name__ == "__main__":
    sys.exit(main())
