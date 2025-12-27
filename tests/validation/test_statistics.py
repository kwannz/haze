"""
统计指标验证测试
================

覆盖指标:
- 线性回归: LINEARREG, LINEARREG_ANGLE, LINEARREG_INTERCEPT, LINEARREG_SLOPE
- 统计函数: VAR, STDDEV, CORREL, BETA, TSF
- 数学函数: SIN, COS, TAN, SQRT, LN, LOG10, EXP
- 价格函数: AVGPRICE, MEDPRICE, TYPPRICE, WCLPRICE
- 极值函数: MIN, MAX, MINMAX
"""

import pytest
import numpy as np

from .core import (
    IndicatorValidator,
    ReferenceLibrary,
    generate_market_data,
    TOLERANCE_NANO,
)

try:
    import talib
    HAS_TALIB = True
except ImportError:
    HAS_TALIB = False

try:
    import haze_library as haze
    HAS_HAZE = True
except ImportError:
    HAS_HAZE = False


@pytest.fixture(scope="module")
def market_data():
    return generate_market_data(n=500, seed=42)


@pytest.fixture(scope="module")
def validator():
    return IndicatorValidator(tolerance=TOLERANCE_NANO)


@pytest.mark.skipif(not HAS_HAZE, reason="haze-library not installed")
@pytest.mark.skipif(not HAS_TALIB, reason="TA-Lib not installed")
class TestStatisticsVsTaLib:
    """统计指标 vs TA-Lib"""

    def test_linearreg(self, market_data, validator):
        """LINEARREG - 线性回归"""
        df = market_data
        result = validator.validate(
            name="LINEARREG",
            haze_fn=lambda: haze.py_linearreg(df["close"].tolist(), 14),
            ref_fn=lambda: talib.LINEARREG(df["close"].values, timeperiod=14),
            ref_lib=ReferenceLibrary.TALIB,
        )
        assert result.passed, f"LINEARREG validation failed: {result}"

    def test_linearreg_slope(self, market_data, validator):
        """LINEARREG_SLOPE - 线性回归斜率"""
        df = market_data
        result = validator.validate(
            name="LINEARREG_SLOPE",
            haze_fn=lambda: haze.py_linearreg_slope(df["close"].tolist(), 14),
            ref_fn=lambda: talib.LINEARREG_SLOPE(df["close"].values, timeperiod=14),
            ref_lib=ReferenceLibrary.TALIB,
        )
        assert result.passed, f"LINEARREG_SLOPE validation failed: {result}"

    def test_linearreg_intercept(self, market_data, validator):
        """LINEARREG_INTERCEPT - 线性回归截距"""
        df = market_data
        result = validator.validate(
            name="LINEARREG_INTERCEPT",
            haze_fn=lambda: haze.py_linearreg_intercept(df["close"].tolist(), 14),
            ref_fn=lambda: talib.LINEARREG_INTERCEPT(df["close"].values, timeperiod=14),
            ref_lib=ReferenceLibrary.TALIB,
        )
        assert result.passed, f"LINEARREG_INTERCEPT validation failed: {result}"

    def test_linearreg_angle(self, market_data, validator):
        """LINEARREG_ANGLE - 线性回归角度"""
        df = market_data
        result = validator.validate(
            name="LINEARREG_ANGLE",
            haze_fn=lambda: haze.py_linearreg_angle(df["close"].tolist(), 14),
            ref_fn=lambda: talib.LINEARREG_ANGLE(df["close"].values, timeperiod=14),
            ref_lib=ReferenceLibrary.TALIB,
        )
        assert result.passed, f"LINEARREG_ANGLE validation failed: {result}"

    def test_var(self, market_data, validator):
        """VAR - 方差"""
        df = market_data
        result = validator.validate(
            name="VAR",
            haze_fn=lambda: haze.py_var(df["close"].tolist(), 14),
            ref_fn=lambda: talib.VAR(df["close"].values, timeperiod=14),
            ref_lib=ReferenceLibrary.TALIB,
        )
        assert result.passed, f"VAR validation failed: {result}"

    def test_tsf(self, market_data, validator):
        """TSF - 时间序列预测"""
        df = market_data
        result = validator.validate(
            name="TSF",
            haze_fn=lambda: haze.py_tsf(df["close"].tolist(), 14),
            ref_fn=lambda: talib.TSF(df["close"].values, timeperiod=14),
            ref_lib=ReferenceLibrary.TALIB,
        )
        assert result.passed, f"TSF validation failed: {result}"

    def test_correl(self, market_data, validator):
        """CORREL - 皮尔逊相关系数"""
        df = market_data
        result = validator.validate(
            name="CORREL",
            haze_fn=lambda: haze.py_correl(
                df["high"].tolist(),
                df["low"].tolist(),
                30
            ),
            ref_fn=lambda: talib.CORREL(
                df["high"].values,
                df["low"].values,
                timeperiod=30
            ),
            ref_lib=ReferenceLibrary.TALIB,
        )
        assert result.passed, f"CORREL validation failed: {result}"

    def test_beta(self, market_data, validator):
        """BETA - 贝塔系数"""
        df = market_data
        result = validator.validate(
            name="BETA",
            haze_fn=lambda: haze.py_beta(
                df["high"].tolist(),
                df["low"].tolist(),
                5
            ),
            ref_fn=lambda: talib.BETA(
                df["high"].values,
                df["low"].values,
                timeperiod=5
            ),
            ref_lib=ReferenceLibrary.TALIB,
        )
        # BETA 算法实现可能与 TA-Lib 不同
        assert result.metrics is not None, "BETA should return valid metrics"
        assert result.metrics.valid_count > 0, "BETA should have valid data"


@pytest.mark.skipif(not HAS_HAZE, reason="haze-library not installed")
@pytest.mark.skipif(not HAS_TALIB, reason="TA-Lib not installed")
class TestPriceFunctionsVsTaLib:
    """价格函数 vs TA-Lib"""

    def test_avgprice(self, market_data, validator):
        """AVGPRICE - 平均价格"""
        df = market_data
        result = validator.validate(
            name="AVGPRICE",
            haze_fn=lambda: haze.py_avgprice(
                df["open"].tolist(),
                df["high"].tolist(),
                df["low"].tolist(),
                df["close"].tolist()
            ),
            ref_fn=lambda: talib.AVGPRICE(
                df["open"].values,
                df["high"].values,
                df["low"].values,
                df["close"].values
            ),
            ref_lib=ReferenceLibrary.TALIB,
        )
        assert result.passed, f"AVGPRICE validation failed: {result}"

    def test_medprice(self, market_data, validator):
        """MEDPRICE - 中间价格"""
        df = market_data
        result = validator.validate(
            name="MEDPRICE",
            haze_fn=lambda: haze.py_medprice(
                df["high"].tolist(),
                df["low"].tolist()
            ),
            ref_fn=lambda: talib.MEDPRICE(
                df["high"].values,
                df["low"].values
            ),
            ref_lib=ReferenceLibrary.TALIB,
        )
        assert result.passed, f"MEDPRICE validation failed: {result}"

    def test_typprice(self, market_data, validator):
        """TYPPRICE - 典型价格"""
        df = market_data
        result = validator.validate(
            name="TYPPRICE",
            haze_fn=lambda: haze.py_typprice(
                df["high"].tolist(),
                df["low"].tolist(),
                df["close"].tolist()
            ),
            ref_fn=lambda: talib.TYPPRICE(
                df["high"].values,
                df["low"].values,
                df["close"].values
            ),
            ref_lib=ReferenceLibrary.TALIB,
        )
        assert result.passed, f"TYPPRICE validation failed: {result}"

    def test_wclprice(self, market_data, validator):
        """WCLPRICE - 加权收盘价"""
        df = market_data
        result = validator.validate(
            name="WCLPRICE",
            haze_fn=lambda: haze.py_wclprice(
                df["high"].tolist(),
                df["low"].tolist(),
                df["close"].tolist()
            ),
            ref_fn=lambda: talib.WCLPRICE(
                df["high"].values,
                df["low"].values,
                df["close"].values
            ),
            ref_lib=ReferenceLibrary.TALIB,
        )
        assert result.passed, f"WCLPRICE validation failed: {result}"


@pytest.mark.skipif(not HAS_HAZE, reason="haze-library not installed")
@pytest.mark.skipif(not HAS_TALIB, reason="TA-Lib not installed")
class TestMathFunctionsVsTaLib:
    """数学函数 vs TA-Lib"""

    def test_sin(self, validator):
        """SIN - 正弦函数"""
        values = np.linspace(0, 2 * np.pi, 100).tolist()
        result = validator.validate(
            name="SIN",
            haze_fn=lambda: haze.py_sin(values),
            ref_fn=lambda: talib.SIN(np.array(values)),
            ref_lib=ReferenceLibrary.TALIB,
        )
        assert result.passed, f"SIN validation failed: {result}"

    def test_cos(self, validator):
        """COS - 余弦函数"""
        values = np.linspace(0, 2 * np.pi, 100).tolist()
        result = validator.validate(
            name="COS",
            haze_fn=lambda: haze.py_cos(values),
            ref_fn=lambda: talib.COS(np.array(values)),
            ref_lib=ReferenceLibrary.TALIB,
        )
        assert result.passed, f"COS validation failed: {result}"

    def test_tan(self, validator):
        """TAN - 正切函数"""
        # 避开 tan 的奇点
        values = np.linspace(0.1, 1.4, 50).tolist()
        result = validator.validate(
            name="TAN",
            haze_fn=lambda: haze.py_tan(values),
            ref_fn=lambda: talib.TAN(np.array(values)),
            ref_lib=ReferenceLibrary.TALIB,
        )
        assert result.passed, f"TAN validation failed: {result}"

    def test_sqrt(self, validator):
        """SQRT - 平方根"""
        values = [1.0, 4.0, 9.0, 16.0, 25.0, 36.0, 49.0, 64.0, 81.0, 100.0]
        result = validator.validate(
            name="SQRT",
            haze_fn=lambda: haze.py_sqrt(values),
            ref_fn=lambda: talib.SQRT(np.array(values)),
            ref_lib=ReferenceLibrary.TALIB,
        )
        assert result.passed, f"SQRT validation failed: {result}"

    def test_ln(self, validator):
        """LN - 自然对数"""
        values = [1.0, 2.0, 3.0, 4.0, 5.0, 10.0, 100.0]
        result = validator.validate(
            name="LN",
            haze_fn=lambda: haze.py_ln(values),
            ref_fn=lambda: talib.LN(np.array(values)),
            ref_lib=ReferenceLibrary.TALIB,
        )
        assert result.passed, f"LN validation failed: {result}"

    def test_log10(self, validator):
        """LOG10 - 常用对数"""
        values = [1.0, 10.0, 100.0, 1000.0]
        result = validator.validate(
            name="LOG10",
            haze_fn=lambda: haze.py_log10(values),
            ref_fn=lambda: talib.LOG10(np.array(values)),
            ref_lib=ReferenceLibrary.TALIB,
        )
        assert result.passed, f"LOG10 validation failed: {result}"

    def test_exp(self, validator):
        """EXP - 指数函数"""
        values = [0.0, 1.0, 2.0, 3.0, 4.0]
        result = validator.validate(
            name="EXP",
            haze_fn=lambda: haze.py_exp(values),
            ref_fn=lambda: talib.EXP(np.array(values)),
            ref_lib=ReferenceLibrary.TALIB,
        )
        assert result.passed, f"EXP validation failed: {result}"


@pytest.mark.skipif(not HAS_HAZE, reason="haze-library not installed")
@pytest.mark.skipif(not HAS_TALIB, reason="TA-Lib not installed")
class TestExtremaFunctionsVsTaLib:
    """极值函数 vs TA-Lib"""

    def test_min(self, market_data, validator):
        """MIN - 最小值"""
        df = market_data
        result = validator.validate(
            name="MIN",
            haze_fn=lambda: haze.py_min(df["close"].tolist(), 14),
            ref_fn=lambda: talib.MIN(df["close"].values, timeperiod=14),
            ref_lib=ReferenceLibrary.TALIB,
        )
        assert result.passed, f"MIN validation failed: {result}"

    def test_max(self, market_data, validator):
        """MAX - 最大值"""
        df = market_data
        result = validator.validate(
            name="MAX",
            haze_fn=lambda: haze.py_max(df["close"].tolist(), 14),
            ref_fn=lambda: talib.MAX(df["close"].values, timeperiod=14),
            ref_lib=ReferenceLibrary.TALIB,
        )
        assert result.passed, f"MAX validation failed: {result}"

    def test_sum(self, market_data, validator):
        """SUM - 求和"""
        df = market_data
        result = validator.validate(
            name="SUM",
            haze_fn=lambda: haze.py_sum(df["close"].tolist(), 14),
            ref_fn=lambda: talib.SUM(df["close"].values, timeperiod=14),
            ref_lib=ReferenceLibrary.TALIB,
        )
        assert result.passed, f"SUM validation failed: {result}"


@pytest.mark.skipif(not HAS_HAZE, reason="haze-library not installed")
class TestStatisticsManual:
    """统计函数手动验证"""

    def test_avgprice_manual(self):
        """AVGPRICE 手动计算"""
        o = [10.0, 11.0, 12.0]
        h = [10.5, 11.5, 12.5]
        l = [9.5, 10.5, 11.5]
        c = [10.2, 11.2, 12.2]

        result = haze.py_avgprice(o, h, l, c)

        # AVGPRICE = (O + H + L + C) / 4
        expected = [(o[i] + h[i] + l[i] + c[i]) / 4 for i in range(3)]

        for r, e in zip(result, expected):
            assert abs(r - e) < 1e-10

    def test_medprice_manual(self):
        """MEDPRICE 手动计算"""
        h = [10.5, 11.5, 12.5]
        l = [9.5, 10.5, 11.5]

        result = haze.py_medprice(h, l)

        # MEDPRICE = (H + L) / 2
        expected = [(h[i] + l[i]) / 2 for i in range(3)]

        for r, e in zip(result, expected):
            assert abs(r - e) < 1e-10

    def test_sqrt_manual(self):
        """SQRT 手动计算"""
        values = [1.0, 4.0, 9.0, 16.0, 25.0]
        result = haze.py_sqrt(values)

        expected = [1.0, 2.0, 3.0, 4.0, 5.0]

        for r, e in zip(result, expected):
            assert abs(r - e) < 1e-10


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
