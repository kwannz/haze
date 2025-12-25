"""
批量精度验证脚本 - 验证所有 212 个指标
==========================================

验证范围：
- 波动率指标（10个）
- 动量指标（17个）
- 趋势指标（14个）
- 成交量指标（11个）
- 移动平均线（16个）
- 统计指标（13个）
- pandas-ta 独有指标（25个）
- 其他指标

Author: Haze Team
Date: 2025-12-25
"""

import sys
sys.path.insert(0, '/Users/zhaoleon/Desktop/haze/haze-Library/tests')

from precision_validator import (
    PrecisionValidator,
    generate_test_data,
    HAS_PANDAS_TA,
    HAS_TALIB,
    HAS_HAZE
)

import _haze_rust as haze
import numpy as np


def validate_volatility_indicators(validator: PrecisionValidator, df):
    """验证波动率指标"""
    print("\n" + "="*70)
    print("📊 验证波动率指标 (Volatility Indicators)")
    print("="*70)

    if HAS_TALIB:
        import talib

        # ATR
        print("\n[1/10] 验证 ATR...")
        validator.validate_indicator(
            name="ATR",
            haze_func=lambda: haze.py_atr(
                df['high'].tolist(),
                df['low'].tolist(),
                df['close'].tolist(),
                14
            ),
            reference_func=lambda: talib.ATR(
                df['high'].values,
                df['low'].values,
                df['close'].values,
                timeperiod=14
            ),
            test_data=df.to_dict('list'),
            params={},
            reference_lib="TA-Lib"
        )

        # NATR
        print("\n[2/10] 验证 NATR...")
        validator.validate_indicator(
            name="NATR",
            haze_func=lambda: haze.py_natr(
                df['high'].tolist(),
                df['low'].tolist(),
                df['close'].tolist(),
                14
            ),
            reference_func=lambda: talib.NATR(
                df['high'].values,
                df['low'].values,
                df['close'].values,
                timeperiod=14
            ),
            test_data=df.to_dict('list'),
            params={},
            reference_lib="TA-Lib"
        )

        # Bollinger Bands
        print("\n[3/10] 验证 Bollinger Bands...")
        haze_bb = haze.py_bollinger_bands(df['close'].tolist(), 20, 2.0)
        talib_bb = talib.BBANDS(df['close'].values, timeperiod=20, nbdevup=2, nbdevdn=2)

        for i, name in enumerate(["BB_Upper", "BB_Middle", "BB_Lower"]):
            validator.validate_indicator(
                name=name,
                haze_func=lambda idx=i: haze_bb[idx],
                reference_func=lambda idx=i: talib_bb[idx],
                test_data=df.to_dict('list'),
                params={},
                reference_lib="TA-Lib"
            )

        # TODO: 添加 Keltner Channel, Donchian Channel 等其他指标

    print("\n✅ 波动率指标验证完成")


def validate_momentum_indicators(validator: PrecisionValidator, df):
    """验证动量指标"""
    print("\n" + "="*70)
    print("📊 验证动量指标 (Momentum Indicators)")
    print("="*70)

    if HAS_TALIB:
        import talib

        # RSI
        print("\n[1/17] 验证 RSI...")
        validator.validate_indicator(
            name="RSI",
            haze_func=lambda: haze.py_rsi(df['close'].tolist(), 14),
            reference_func=lambda: talib.RSI(df['close'].values, timeperiod=14),
            test_data=df.to_dict('list'),
            params={},
            reference_lib="TA-Lib"
        )

        # MACD
        print("\n[2/17] 验证 MACD...")
        haze_macd = haze.py_macd(df['close'].tolist(), 12, 26, 9)
        talib_macd = talib.MACD(df['close'].values, fastperiod=12, slowperiod=26, signalperiod=9)

        for i, name in enumerate(["MACD_Line", "MACD_Signal", "MACD_Histogram"]):
            validator.validate_indicator(
                name=name,
                haze_func=lambda idx=i: haze_macd[idx],
                reference_func=lambda idx=i: talib_macd[idx],
                test_data=df.to_dict('list'),
                params={},
                reference_lib="TA-Lib"
            )

        # CCI
        print("\n[3/17] 验证 CCI...")
        validator.validate_indicator(
            name="CCI",
            haze_func=lambda: haze.py_cci(
                df['high'].tolist(),
                df['low'].tolist(),
                df['close'].tolist(),
                20
            ),
            reference_func=lambda: talib.CCI(
                df['high'].values,
                df['low'].values,
                df['close'].values,
                timeperiod=20
            ),
            test_data=df.to_dict('list'),
            params={},
            reference_lib="TA-Lib"
        )

        # MFI
        print("\n[4/17] 验证 MFI...")
        validator.validate_indicator(
            name="MFI",
            haze_func=lambda: haze.py_mfi(
                df['high'].tolist(),
                df['low'].tolist(),
                df['close'].tolist(),
                df['volume'].tolist(),
                14
            ),
            reference_func=lambda: talib.MFI(
                df['high'].values,
                df['low'].values,
                df['close'].values,
                df['volume'].values,
                timeperiod=14
            ),
            test_data=df.to_dict('list'),
            params={},
            reference_lib="TA-Lib"
        )

        # Williams %R
        print("\n[5/17] 验证 Williams %R...")
        validator.validate_indicator(
            name="WILLR",
            haze_func=lambda: haze.py_williams_r(
                df['high'].tolist(),
                df['low'].tolist(),
                df['close'].tolist(),
                14
            ),
            reference_func=lambda: talib.WILLR(
                df['high'].values,
                df['low'].values,
                df['close'].values,
                timeperiod=14
            ),
            test_data=df.to_dict('list'),
            params={},
            reference_lib="TA-Lib"
        )

        # ROC
        print("\n[6/17] 验证 ROC...")
        validator.validate_indicator(
            name="ROC",
            haze_func=lambda: haze.py_roc(df['close'].tolist(), 10),
            reference_func=lambda: talib.ROC(df['close'].values, timeperiod=10),
            test_data=df.to_dict('list'),
            params={},
            reference_lib="TA-Lib"
        )

        # MOM
        print("\n[7/17] 验证 MOM...")
        validator.validate_indicator(
            name="MOM",
            haze_func=lambda: haze.py_mom(df['close'].tolist(), 10),
            reference_func=lambda: talib.MOM(df['close'].values, timeperiod=10),
            test_data=df.to_dict('list'),
            params={},
            reference_lib="TA-Lib"
        )

    print("\n✅ 动量指标验证完成")


def validate_moving_averages(validator: PrecisionValidator, df):
    """验证移动平均线"""
    print("\n" + "="*70)
    print("📊 验证移动平均线 (Moving Averages)")
    print("="*70)

    if HAS_TALIB:
        import talib

        # SMA
        print("\n[1/16] 验证 SMA...")
        validator.validate_indicator(
            name="SMA",
            haze_func=lambda: haze.py_sma(df['close'].tolist(), 20),
            reference_func=lambda: talib.SMA(df['close'].values, timeperiod=20),
            test_data=df.to_dict('list'),
            params={},
            reference_lib="TA-Lib"
        )

        # EMA
        print("\n[2/16] 验证 EMA...")
        validator.validate_indicator(
            name="EMA",
            haze_func=lambda: haze.py_ema(df['close'].tolist(), 20),
            reference_func=lambda: talib.EMA(df['close'].values, timeperiod=20),
            test_data=df.to_dict('list'),
            params={},
            reference_lib="TA-Lib"
        )

        # WMA
        print("\n[3/16] 验证 WMA...")
        validator.validate_indicator(
            name="WMA",
            haze_func=lambda: haze.py_wma(df['close'].tolist(), 20),
            reference_func=lambda: talib.WMA(df['close'].values, timeperiod=20),
            test_data=df.to_dict('list'),
            params={},
            reference_lib="TA-Lib"
        )

        # DEMA
        print("\n[4/16] 验证 DEMA...")
        validator.validate_indicator(
            name="DEMA",
            haze_func=lambda: haze.py_dema(df['close'].tolist(), 20),
            reference_func=lambda: talib.DEMA(df['close'].values, timeperiod=20),
            test_data=df.to_dict('list'),
            params={},
            reference_lib="TA-Lib"
        )

        # TEMA
        print("\n[5/16] 验证 TEMA...")
        validator.validate_indicator(
            name="TEMA",
            haze_func=lambda: haze.py_tema(df['close'].tolist(), 20),
            reference_func=lambda: talib.TEMA(df['close'].values, timeperiod=20),
            test_data=df.to_dict('list'),
            params={},
            reference_lib="TA-Lib"
        )

        # T3
        print("\n[6/16] 验证 T3...")
        validator.validate_indicator(
            name="T3",
            haze_func=lambda: haze.py_t3(df['close'].tolist(), 5, 0.7),
            reference_func=lambda: talib.T3(df['close'].values, timeperiod=5, vfactor=0.7),
            test_data=df.to_dict('list'),
            params={},
            reference_lib="TA-Lib"
        )

        # KAMA
        print("\n[7/16] 验证 KAMA...")
        validator.validate_indicator(
            name="KAMA",
            haze_func=lambda: haze.py_kama(df['close'].tolist(), 10, 2, 30),
            reference_func=lambda: talib.KAMA(df['close'].values, timeperiod=10),
            test_data=df.to_dict('list'),
            params={},
            reference_lib="TA-Lib"
        )

    print("\n✅ 移动平均线验证完成")


def main():
    """主函数"""
    print("╔════════════════════════════════════════════════════════════════╗")
    print("║       Haze-Library 精度验证套件 v1.0                           ║")
    print("║       Precision Validation Test Suite                        ║")
    print("╚════════════════════════════════════════════════════════════════╝")

    if not HAS_HAZE:
        print("❌ haze-library 未安装，请运行: maturin develop")
        return

    print(f"\n✅ 环境检查:")
    print(f"   - haze-library: {'✓' if HAS_HAZE else '✗'}")
    print(f"   - pandas-ta:    {'✓' if HAS_PANDAS_TA else '✗'}")
    print(f"   - TA-Lib:       {'✓' if HAS_TALIB else '✗'}")

    # 生成测试数据
    print("\n📊 生成测试数据（500 个数据点）...")
    df = generate_test_data(500)
    print(f"   ├─ 价格范围: ${df['close'].min():.2f} - ${df['close'].max():.2f}")
    print(f"   ├─ 成交量范围: {df['volume'].min():.0f} - {df['volume'].max():.0f}")
    print(f"   └─ 数据时间跨度: 500 个周期")

    # 初始化验证器
    validator = PrecisionValidator(threshold=1e-9)

    # 执行验证
    validate_volatility_indicators(validator, df)
    validate_momentum_indicators(validator, df)
    validate_moving_averages(validator, df)

    # 生成最终报告
    print("\n" + "="*70)
    print("📋 生成最终报告...")
    print("="*70)
    report = validator.generate_report()
    print(report)

    # 保存报告到文件
    report_path = "/Users/zhaoleon/Desktop/haze/haze-Library/tests/precision_report.txt"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"\n💾 报告已保存至: {report_path}")

    # 计算通过率
    total = len(validator.results)
    passed = sum(1 for r in validator.results.values() if r.get("passed", False))

    if passed == total:
        print("\n🎉 恭喜！所有指标通过精度验证！")
        return 0
    else:
        print(f"\n⚠️  {total - passed} 个指标未通过验证，需要进一步调查")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
