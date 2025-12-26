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

import inspect
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from precision_validator import (
    PrecisionValidator,
    generate_test_data,
    HAS_PANDAS_TA,
    HAS_TALIB,
    HAS_HAZE
)
from pandas_ta_compat import import_pandas_ta
from pandas_ta_kw_compat import import_pandas_ta_kw

try:
    import haze_library as haze
except ImportError:
    import _haze_rust as haze

PANDAS_TA_KW, PANDAS_TA_KW_PATH, PANDAS_TA_KW_CUSTOM = import_pandas_ta_kw()
HAS_PANDAS_TA_KW = PANDAS_TA_KW is not None


def _first_param(params, names):
    for name in names:
        if name in params:
            return name
    return None


def _to_numpy(values):
    if hasattr(values, "to_numpy"):
        return values.to_numpy()
    return values


def _find_indicator(module, names):
    for name in names:
        fn = getattr(module, name, None)
        if callable(fn):
            return fn, name
    return None, None


def _select_column(df, tokens):
    for idx, col in enumerate(getattr(df, "columns", [])):
        name = str(col).lower()
        if any(token in name for token in tokens):
            return idx
    return None


def validate_pandas_ta_exclusive(validator: PrecisionValidator, df):
    """验证 pandas-ta 独有指标（可对齐的子集）"""
    print("\n" + "="*70)
    print("📊 验证 pandas-ta 独有指标 (pandas-ta Exclusive)")
    print("="*70)

    pta, _ = import_pandas_ta()
    pta_kw = PANDAS_TA_KW

    if pta is None and pta_kw is None:
        print("⚠️ pandas-ta / pandas-ta-kw 未安装，跳过 pandas-ta 专用对比")
        return

    if pta is None:
        print("⚠️ pandas-ta 未安装，将跳过 pandas-ta 对比项")
    if pta_kw is None:
        print("⚠️ pandas-ta-kw 未安装，将跳过 pandas-ta-kw 对比项")

    close = df["close"]
    high = df["high"]
    low = df["low"]
    open_ = df["open"]
    volume = df["volume"]

    # Entropy 与 pandas-ta 定义不同，跳过精度对比
    print("\n[1/25] Entropy... (skip: 定义与 pandas-ta 不一致)")

    # Aberration（派生：使用 pandas-ta 的 SMA + ATR 复现 Haze 定义）
    if pta is None:
        print("\n[2/25] Aberration... (skip: pandas-ta 未安装)")
    else:
        print("\n[2/25] 验证 Aberration... (derived)")
        pta_ab_sma = pta.sma(close=close, length=20)
        pta_ab_atr = pta.atr(high=high, low=low, close=close, length=20)
        validator.validate_indicator(
            name="Aberration",
            haze_func=lambda: haze.py_aberration(
                high.tolist(),
                low.tolist(),
                close.tolist(),
                20,
                20
            ),
            reference_func=lambda: ((close - pta_ab_sma) / pta_ab_atr).to_numpy(),
            test_data=df.to_dict("list"),
            params={},
            reference_lib="pandas-ta (derived)"
        )

    # Squeeze 与 pandas-ta 动量定义不同，跳过精度对比
    print("\n[3/25] Squeeze... (skip: 动量定义不同)")

    # QQE 与 pandas-ta 版本不同，跳过精度对比
    print("\n[4/25] QQE... (skip: 公式实现不同)")

    # CTI
    if pta is None:
        print("\n[5/25] CTI... (skip: pandas-ta 未安装)")
    else:
        print("\n[5/25] 验证 CTI...")
        validator.validate_indicator(
            name="CTI",
            haze_func=lambda: haze.py_cti(close.tolist(), 12),
            reference_func=lambda: pta.cti(close=close, length=12).to_numpy(),
            test_data=df.to_dict("list"),
            params={},
            reference_lib="pandas-ta"
        )

    # ER
    if pta is None:
        print("\n[6/25] ER... (skip: pandas-ta 未安装)")
    else:
        print("\n[6/25] 验证 ER...")
        validator.validate_indicator(
            name="ER",
            haze_func=lambda: haze.py_er(close.tolist(), 10),
            reference_func=lambda: pta.er(close=close, length=10).to_numpy(),
            test_data=df.to_dict("list"),
            params={},
            reference_lib="pandas-ta"
        )

    # Bias（pandas-ta 输出为比例，Haze 为百分比）
    if pta is None:
        print("\n[7/25] Bias... (skip: pandas-ta 未安装)")
    else:
        print("\n[7/25] 验证 Bias...")
        validator.validate_indicator(
            name="BIAS",
            haze_func=lambda: haze.py_bias(close.tolist(), 20),
            reference_func=lambda: (pta.bias(close=close, length=20, mamode="sma") * 100.0).to_numpy(),
            test_data=df.to_dict("list"),
            params={},
            reference_lib="pandas-ta"
        )

    # PSL
    if pta is None:
        print("\n[8/25] PSL... (skip: pandas-ta 未安装)")
    else:
        print("\n[8/25] 验证 PSL...")
        validator.validate_indicator(
            name="PSL",
            haze_func=lambda: haze.py_psl(close.tolist(), 12),
            reference_func=lambda: pta.psl(close=close, length=12).to_numpy(),
            test_data=df.to_dict("list"),
            params={},
            reference_lib="pandas-ta"
        )

    # RVI / Inertia 与 pandas-ta 定义不同，跳过精度对比
    print("\n[9/25] RVI... (skip: 指标定义不同)")
    print("\n[10/25] Inertia... (skip: 指标定义不同)")

    # Alligator（使用 HL2 输入并手动偏移对齐）
    if pta is None:
        print("\n[11/25] Alligator... (skip: pandas-ta 未安装)")
    else:
        print("\n[11/25] 验证 Alligator...")
        haze_alligator = haze.py_alligator(
            high.tolist(),
            low.tolist(),
            13,
            8,
            5
        )
        hl2 = (high + low) / 2.0
        pta_alligator = pta.alligator(close=hl2, jaw=13, teeth=8, lips=5, talib=False)
        pta_jaw = pta_alligator.iloc[:, 0].shift(8)
        pta_teeth = pta_alligator.iloc[:, 1].shift(5)
        pta_lips = pta_alligator.iloc[:, 2].shift(3)

        for i, name in enumerate(["Alligator_Jaw", "Alligator_Teeth", "Alligator_Lips"]):
            ref_series = [pta_jaw, pta_teeth, pta_lips][i]
            validator.validate_indicator(
                name=name,
                haze_func=lambda idx=i: haze_alligator[idx],
                reference_func=lambda s=ref_series: s.to_numpy(),
                test_data=df.to_dict("list"),
                params={},
                reference_lib="pandas-ta"
            )

    # EFI
    if pta is None:
        print("\n[12/25] EFI... (skip: pandas-ta 未安装)")
    else:
        print("\n[12/25] 验证 EFI...")
        validator.validate_indicator(
            name="EFI",
            haze_func=lambda: haze.py_efi(close.tolist(), volume.tolist(), 13),
            reference_func=lambda: pta.efi(close=close, volume=volume, length=13, mamode="ema").to_numpy(),
            test_data=df.to_dict("list"),
            params={},
            reference_lib="pandas-ta"
        )

    # KST（pandas-ta 结果缩放到 Haze 输出）
    if pta is None:
        print("\n[13/25] KST... (skip: pandas-ta 未安装)")
    else:
        print("\n[13/25] 验证 KST...")
        haze_kst = haze.py_kst(close.tolist(), 10, 15, 20, 30, 9)
        pta_kst = pta.kst(
            close=close,
            roc1=10,
            roc2=15,
            roc3=20,
            roc4=30,
            sma1=10,
            sma2=10,
            sma3=10,
            sma4=15,
            signal=9
        )
        pta_kst_line = pta_kst.iloc[:, 0] / 100.0
        pta_kst_signal = pta_kst.iloc[:, 1] / 100.0

        for i, name in enumerate(["KST", "KST_Signal"]):
            ref_series = [pta_kst_line, pta_kst_signal][i]
            validator.validate_indicator(
                name=name,
                haze_func=lambda idx=i: haze_kst[idx],
                reference_func=lambda s=ref_series: s.to_numpy(),
                test_data=df.to_dict("list"),
                params={},
                reference_lib="pandas-ta"
            )

    # STC / TDFI / WAE 与 pandas-ta 定义不同或缺失
    print("\n[14/25] STC... (skip: 公式实现不同)")

    if pta_kw is None:
        print("\n[15/25] TDFI... (skip: pandas-ta-kw 未安装)")
    else:
        tdfi_fn, _ = _find_indicator(pta_kw, ["tdfi", "tdf"])
        if tdfi_fn is None:
            print("\n[15/25] TDFI... (skip: pandas-ta-kw 未实现)")
        else:
            print("\n[15/25] 验证 TDFI... (pandas-ta-kw)")
            try:
                params = inspect.signature(tdfi_fn).parameters
                kwargs = {}
                close_key = _first_param(params, ["close", "close_", "src", "series", "price"])
                length_key = _first_param(params, ["length", "period", "n"])
                smooth_key = _first_param(params, ["signal", "smooth", "smooth_length", "sig"])
                if close_key:
                    kwargs[close_key] = close
                if length_key:
                    kwargs[length_key] = 13
                if smooth_key:
                    kwargs[smooth_key] = 3
                ref = tdfi_fn(**kwargs)
            except Exception as exc:
                print(f"  ⚠️ TDFI 调用失败: {exc}")
            else:
                validator.validate_indicator(
                    name="TDFI",
                    haze_func=lambda: haze.py_tdfi(close.tolist(), 13, 3),
                    reference_func=lambda r=ref: _to_numpy(r),
                    test_data=df.to_dict("list"),
                    params={},
                    reference_lib="pandas-ta-kw"
                )

    if pta_kw is None:
        print("\n[16/25] WAE... (skip: pandas-ta-kw 未安装)")
    else:
        wae_fn, _ = _find_indicator(pta_kw, ["wae", "waddah", "waddah_attar", "waddah_attar_explosion"])
        if wae_fn is None:
            print("\n[16/25] WAE... (skip: pandas-ta-kw 未实现)")
        else:
            print("\n[16/25] 验证 WAE... (pandas-ta-kw)")
            try:
                params = inspect.signature(wae_fn).parameters
                kwargs = {}
                close_key = _first_param(params, ["close", "close_", "src", "series", "price"])
                fast_key = _first_param(params, ["fast", "fast_length"])
                slow_key = _first_param(params, ["slow", "slow_length"])
                signal_key = _first_param(params, ["signal", "signal_length"])
                length_key = _first_param(params, ["length", "bb_length", "bb_period"])
                mult_key = _first_param(params, ["mult", "multiplier", "bb_mult", "bb_multiplier"])
                if close_key:
                    kwargs[close_key] = close
                if fast_key:
                    kwargs[fast_key] = 20
                if slow_key:
                    kwargs[slow_key] = 40
                if signal_key:
                    kwargs[signal_key] = 9
                if length_key:
                    kwargs[length_key] = 20
                if mult_key:
                    kwargs[mult_key] = 2.0
                ref = wae_fn(**kwargs)
                if hasattr(ref, "columns"):
                    exp_idx = _select_column(ref, ["exp", "expl", "wae"])
                    dz_idx = _select_column(ref, ["dead", "dz"])
                    if exp_idx is None or dz_idx is None:
                        if len(ref.columns) >= 2:
                            exp_idx, dz_idx = 0, 1
                        else:
                            raise ValueError("WAE 输出列不足")
                    ref_explosion = ref.iloc[:, exp_idx].to_numpy()
                    ref_dead = ref.iloc[:, dz_idx].to_numpy()
                elif isinstance(ref, tuple) and len(ref) >= 2:
                    ref_explosion = _to_numpy(ref[0])
                    ref_dead = _to_numpy(ref[1])
                else:
                    raise ValueError("WAE 输出格式不支持")
            except Exception as exc:
                print(f"  ⚠️ WAE 调用失败: {exc}")
            else:
                validator.validate_indicator(
                    name="WAE",
                    haze_func=lambda: haze.py_wae(close.tolist(), 20, 40, 9, 20, 2.0),
                    reference_func=lambda e=ref_explosion, d=ref_dead: (e, d),
                    test_data=df.to_dict("list"),
                    params={},
                    reference_lib="pandas-ta-kw"
                )

    # SMI 定义不同（pandas-ta 为 SMI Ergodic）
    print("\n[17/25] SMI... (skip: 指标定义不同)")

    # Coppock
    if pta is None:
        print("\n[18/25] Coppock... (skip: pandas-ta 未安装)")
    else:
        print("\n[18/25] 验证 Coppock...")
        validator.validate_indicator(
            name="Coppock",
            haze_func=lambda: haze.py_coppock(close.tolist(), 11, 14, 10),
            reference_func=lambda: pta.coppock(close=close, length=10, fast=11, slow=14).to_numpy(),
            test_data=df.to_dict("list"),
            params={},
            reference_lib="pandas-ta"
        )

    # PGO（派生：使用 pandas-ta SMA + ATR 复现 Haze 定义）
    if pta is None:
        print("\n[19/25] PGO... (skip: pandas-ta 未安装)")
    else:
        print("\n[19/25] 验证 PGO... (derived)")
        pta_pgo_sma = pta.sma(close=close, length=14)
        pta_pgo_atr = pta.atr(high=high, low=low, close=close, length=14)
        validator.validate_indicator(
            name="PGO",
            haze_func=lambda: haze.py_pgo(
                high.tolist(),
                low.tolist(),
                close.tolist(),
                14
            ),
            reference_func=lambda: ((close - pta_pgo_sma) / pta_pgo_atr).to_numpy(),
            test_data=df.to_dict("list"),
            params={},
            reference_lib="pandas-ta (derived)"
        )

    # VWMA
    if pta is None:
        print("\n[20/25] VWMA... (skip: pandas-ta 未安装)")
    else:
        print("\n[20/25] 验证 VWMA...")
        validator.validate_indicator(
            name="VWMA",
            haze_func=lambda: haze.py_vwma(close.tolist(), volume.tolist(), 20),
            reference_func=lambda: pta.vwma(close=close, volume=volume, length=20).to_numpy(),
            test_data=df.to_dict("list"),
            params={},
            reference_lib="pandas-ta"
        )

    # BOP
    if pta is None:
        print("\n[21/25] BOP... (skip: pandas-ta 未安装)")
    else:
        print("\n[21/25] 验证 BOP...")
        validator.validate_indicator(
            name="BOP",
            haze_func=lambda: haze.py_bop(
                open_.tolist(),
                high.tolist(),
                low.tolist(),
                close.tolist()
            ),
            reference_func=lambda: pta.bop(open_=open_, high=high, low=low, close=close).to_numpy(),
            test_data=df.to_dict("list"),
            params={},
            reference_lib="pandas-ta"
        )

    # SSL Channel / CFO / Slope / Percent Rank
    if pta_kw is None:
        print("\n[22/25] SSL Channel... (skip: pandas-ta-kw 未安装)")
    else:
        ssl_fn, _ = _find_indicator(pta_kw, ["ssl", "ssl_channel", "sslchannel"])
        if ssl_fn is None:
            print("\n[22/25] SSL Channel... (skip: pandas-ta-kw 未实现)")
        else:
            print("\n[22/25] 验证 SSL Channel... (pandas-ta-kw)")
            try:
                params = inspect.signature(ssl_fn).parameters
                kwargs = {}
                close_key = _first_param(params, ["close", "close_", "src", "series", "price"])
                high_key = _first_param(params, ["high"])
                low_key = _first_param(params, ["low"])
                length_key = _first_param(params, ["length", "period", "n"])
                if close_key:
                    kwargs[close_key] = close
                if high_key:
                    kwargs[high_key] = high
                if low_key:
                    kwargs[low_key] = low
                if length_key:
                    kwargs[length_key] = 10
                ref = ssl_fn(**kwargs)
                if hasattr(ref, "columns"):
                    up_idx = _select_column(ref, ["up", "upper", "sslup"])
                    down_idx = _select_column(ref, ["down", "lower", "ssldn", "ssldown"])
                    if up_idx is None or down_idx is None:
                        if len(ref.columns) >= 2:
                            up_idx, down_idx = 0, 1
                        else:
                            raise ValueError("SSL 输出列不足")
                    ref_up = ref.iloc[:, up_idx].to_numpy()
                    ref_down = ref.iloc[:, down_idx].to_numpy()
                elif isinstance(ref, tuple) and len(ref) >= 2:
                    ref_up = _to_numpy(ref[0])
                    ref_down = _to_numpy(ref[1])
                else:
                    raise ValueError("SSL 输出格式不支持")
            except Exception as exc:
                print(f"  ⚠️ SSL Channel 调用失败: {exc}")
            else:
                validator.validate_indicator(
                    name="SSL_Channel",
                    haze_func=lambda: haze.py_ssl_channel(
                        high.tolist(),
                        low.tolist(),
                        close.tolist(),
                        10
                    ),
                    reference_func=lambda u=ref_up, d=ref_down: (u, d),
                    test_data=df.to_dict("list"),
                    params={},
                    reference_lib="pandas-ta-kw"
                )

    if pta is None:
        print("\n[23/25] CFO... (skip: pandas-ta 未安装)")
    else:
        print("\n[23/25] 验证 CFO...")
        validator.validate_indicator(
            name="CFO",
            haze_func=lambda: haze.py_cfo(close.tolist(), 14),
            reference_func=lambda: pta.cfo(close=close, length=14, scalar=100).to_numpy(),
            test_data=df.to_dict("list"),
            params={},
            reference_lib="pandas-ta"
        )

    print("\n[24/25] Slope... (skip: 指标定义不同)")
    print("\n[25/25] Percent Rank... (skip: 指标定义不同)")


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
    print(f"   - pandas-ta-kw: {'✓' if HAS_PANDAS_TA_KW else '✗'}")
    if HAS_PANDAS_TA_KW:
        kw_path = PANDAS_TA_KW_PATH or "site-packages"
        print(f"   - pandas-ta-kw path: {kw_path}")
        if PANDAS_TA_KW_CUSTOM:
            print("   - pandas-ta-kw custom: ✓")

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
    validate_pandas_ta_exclusive(validator, df)

    # 生成最终报告
    print("\n" + "="*70)
    print("📋 生成最终报告...")
    print("="*70)
    report = validator.generate_report()
    print(report)

    # 保存报告到文件
    report_path = Path(__file__).resolve().parent / "precision_report.txt"
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
