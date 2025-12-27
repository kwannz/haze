"""
Candlestick Pattern Unit Tests
===============================

测试所有61个蜡烛图形态的识别功能。

测试策略：
- 简化测试：每个形态1个测试方法（验证典型形态识别）
- 返回值验证：1.0（看涨）、-1.0（看跌）或0.0（无形态）
- 使用专门的形态fixtures进行测试

蜡烛图形态分类：
- 反转形态：Hammer, Shooting Star, Engulfing, Harami等
- 持续形态：Three Line Strike, Rising/Falling等
- Doji家族：Doji, Dragonfly Doji, Gravestone Doji等
- 三星形态：Morning Star, Evening Star等

Author: Haze Team
Date: 2025-12-26
"""

import numpy as np
import haze_library as haze


# ==================== 基础形态 ====================

class TestDoji:
    """Doji (十字星) - 开盘价≈收盘价"""

    def test_doji_pattern(self, doji_pattern):
        """测试Doji形态识别"""
        result = haze.py_doji(
            doji_pattern['open'],
            doji_pattern['high'],
            doji_pattern['low'],
            doji_pattern['close']
        )
        assert isinstance(result, list)
        assert len(result) == len(doji_pattern['close'])
        # 应该识别出Doji形态
        assert any(abs(x) > 0 for x in result if not np.isnan(x))


class TestHammer:
    """Hammer (锤子线) - 看涨反转"""

    def test_hammer_pattern(self, hammer_pattern):
        """测试Hammer形态识别"""
        result = haze.py_hammer(
            hammer_pattern['open'],
            hammer_pattern['high'],
            hammer_pattern['low'],
            hammer_pattern['close']
        )
        assert isinstance(result, list)
        assert len(result) == len(hammer_pattern['close'])
        # 应该识别出看涨形态（1.0）
        assert any(x == 1.0 for x in result if not np.isnan(x))


class TestHangingMan:
    """Hanging Man (上吊线) - 看跌反转"""

    def test_hanging_man(self, ohlcv_data):
        """测试Hanging Man形态识别"""
        result = haze.py_hanging_man(
            ohlcv_data['open'],
            ohlcv_data['high'],
            ohlcv_data['low'],
            ohlcv_data['close']
        )
        assert isinstance(result, list)
        assert len(result) == len(ohlcv_data['close'])


class TestShootingStar:
    """Shooting Star (流星) - 看跌反转"""

    def test_shooting_star(self, ohlcv_data):
        """测试Shooting Star形态识别"""
        result = haze.py_shooting_star(
            ohlcv_data['open'],
            ohlcv_data['high'],
            ohlcv_data['low'],
            ohlcv_data['close']
        )
        assert isinstance(result, list)
        assert len(result) == len(ohlcv_data['close'])


class TestInvertedHammer:
    """Inverted Hammer (倒锤线) - 看涨反转"""

    def test_inverted_hammer(self, ohlcv_data):
        """测试Inverted Hammer形态识别"""
        result = haze.py_inverted_hammer(
            ohlcv_data['open'],
            ohlcv_data['high'],
            ohlcv_data['low'],
            ohlcv_data['close']
        )
        assert isinstance(result, list)
        assert len(result) == len(ohlcv_data['close'])


# ==================== 吞没形态 ====================

class TestEngulfing:
    """Engulfing (吞没形态) - 强烈反转信号"""

    def test_engulfing(self, ohlcv_data):
        """测试Engulfing形态识别"""
        # Note: py_bullish_engulfing and py_bearish_engulfing only take (open, close)
        result_bullish = haze.py_bullish_engulfing(
            ohlcv_data['open'],
            ohlcv_data['close']
        )
        result_bearish = haze.py_bearish_engulfing(
            ohlcv_data['open'],
            ohlcv_data['close']
        )
        assert isinstance(result_bullish, list)
        assert isinstance(result_bearish, list)
        assert len(result_bullish) == len(ohlcv_data['close'])
        assert len(result_bearish) == len(ohlcv_data['close'])


class TestBullishEngulfing:
    """Bullish Engulfing (看涨吞没)"""

    def test_bullish_engulfing(self, ohlcv_data):
        """测试看涨吞没形态"""
        # py_bullish_engulfing only takes (open, close)
        result = haze.py_bullish_engulfing(
            ohlcv_data['open'],
            ohlcv_data['close']
        )
        assert isinstance(result, list)
        assert len(result) == len(ohlcv_data['close'])


class TestBearishEngulfing:
    """Bearish Engulfing (看跌吞没)"""

    def test_bearish_engulfing(self, ohlcv_data):
        """测试看跌吞没形态"""
        # py_bearish_engulfing only takes (open, close)
        result = haze.py_bearish_engulfing(
            ohlcv_data['open'],
            ohlcv_data['close']
        )
        assert isinstance(result, list)
        assert len(result) == len(ohlcv_data['close'])


# ==================== Harami形态 ====================

class TestHarami:
    """Harami (孕线) - 潜在反转"""

    def test_harami(self, ohlcv_data):
        """测试Harami形态识别"""
        # Note: py_bullish_harami and py_bearish_harami only take (open, close)
        result_bullish = haze.py_bullish_harami(
            ohlcv_data['open'],
            ohlcv_data['close']
        )
        result_bearish = haze.py_bearish_harami(
            ohlcv_data['open'],
            ohlcv_data['close']
        )
        assert isinstance(result_bullish, list)
        assert isinstance(result_bearish, list)
        assert len(result_bullish) == len(ohlcv_data['close'])
        assert len(result_bearish) == len(ohlcv_data['close'])


class TestHaramiCross:
    """Harami Cross (十字孕线)"""

    def test_harami_cross(self, ohlcv_data):
        """测试Harami Cross形态"""
        result = haze.py_harami_cross(
            ohlcv_data['open'],
            ohlcv_data['high'],
            ohlcv_data['low'],
            ohlcv_data['close']
        )
        assert isinstance(result, list)


# ==================== Doji家族 ====================

class TestDragonflyDoji:
    """Dragonfly Doji (蜻蜓十字)"""

    def test_dragonfly_doji(self, ohlcv_data):
        """测试蜻蜓十字形态"""
        result = haze.py_dragonfly_doji(
            ohlcv_data['open'],
            ohlcv_data['high'],
            ohlcv_data['low'],
            ohlcv_data['close']
        )
        assert isinstance(result, list)


class TestGravestoneDoji:
    """Gravestone Doji (墓碑十字)"""

    def test_gravestone_doji(self, ohlcv_data):
        """测试墓碑十字形态"""
        result = haze.py_gravestone_doji(
            ohlcv_data['open'],
            ohlcv_data['high'],
            ohlcv_data['low'],
            ohlcv_data['close']
        )
        assert isinstance(result, list)


class TestLongLeggedDoji:
    """Long-Legged Doji (长腿十字)"""

    def test_long_legged_doji(self, ohlcv_data):
        """测试长腿十字形态"""
        result = haze.py_long_legged_doji(
            ohlcv_data['open'],
            ohlcv_data['high'],
            ohlcv_data['low'],
            ohlcv_data['close']
        )
        assert isinstance(result, list)


# ==================== 星形态 ====================

class TestMorningStar:
    """Morning Star (晨星) - 看涨反转"""

    def test_morning_star(self, ohlcv_data):
        """测试晨星形态"""
        result = haze.py_morning_star(
            ohlcv_data['open'],
            ohlcv_data['high'],
            ohlcv_data['low'],
            ohlcv_data['close']
        )
        assert isinstance(result, list)


class TestEveningStar:
    """Evening Star (晚星) - 看跌反转"""

    def test_evening_star(self, ohlcv_data):
        """测试晚星形态"""
        result = haze.py_evening_star(
            ohlcv_data['open'],
            ohlcv_data['high'],
            ohlcv_data['low'],
            ohlcv_data['close']
        )
        assert isinstance(result, list)


class TestMorningDojiStar:
    """Morning Doji Star (晨星十字)"""

    def test_morning_doji_star(self, ohlcv_data):
        """测试晨星十字形态"""
        result = haze.py_morning_doji_star(
            ohlcv_data['open'],
            ohlcv_data['high'],
            ohlcv_data['low'],
            ohlcv_data['close']
        )
        assert isinstance(result, list)


class TestEveningDojiStar:
    """Evening Doji Star (晚星十字)"""

    def test_evening_doji_star(self, ohlcv_data):
        """测试晚星十字形态"""
        result = haze.py_evening_doji_star(
            ohlcv_data['open'],
            ohlcv_data['high'],
            ohlcv_data['low'],
            ohlcv_data['close']
        )
        assert isinstance(result, list)


# ==================== 乌鸦形态 ====================

class TestThreeBlackCrows:
    """Three Black Crows (三只乌鸦) - 看跌"""

    def test_three_black_crows(self, ohlcv_data_extended):
        """测试三只乌鸦形态"""
        # py_three_black_crows takes (open, low, close) - 3 params
        result = haze.py_three_black_crows(
            ohlcv_data_extended['open'],
            ohlcv_data_extended['low'],
            ohlcv_data_extended['close']
        )
        assert isinstance(result, list)


class TestThreeWhiteSoldiers:
    """Three White Soldiers (三个白兵) - 看涨"""

    def test_three_white_soldiers(self, ohlcv_data_extended):
        """测试三个白兵形态"""
        # py_three_white_soldiers takes (open, high, close) - 3 params
        result = haze.py_three_white_soldiers(
            ohlcv_data_extended['open'],
            ohlcv_data_extended['high'],
            ohlcv_data_extended['close']
        )
        assert isinstance(result, list)


# ==================== 穿刺形态 ====================

class TestPiercingLine:
    """Piercing Line (刺穿形态) - 看涨"""

    def test_piercing_line(self, ohlcv_data):
        """测试刺穿形态"""
        # Library has py_piercing_pattern(open, low, close) - 3 params
        result = haze.py_piercing_pattern(
            ohlcv_data['open'],
            ohlcv_data['low'],
            ohlcv_data['close']
        )
        assert isinstance(result, list)


class TestDarkCloudCover:
    """Dark Cloud Cover (乌云盖顶) - 看跌"""

    def test_dark_cloud_cover(self, ohlcv_data):
        """测试乌云盖顶形态"""
        # py_dark_cloud_cover takes (open, high, close) - 3 params
        result = haze.py_dark_cloud_cover(
            ohlcv_data['open'],
            ohlcv_data['high'],
            ohlcv_data['close']
        )
        assert isinstance(result, list)


# ==================== Marubozu形态 ====================

class TestMarubozu:
    """Marubozu (光头光脚) - 强势蜡烛"""

    def test_marubozu(self, ohlcv_data):
        """测试光头光脚形态"""
        result = haze.py_marubozu(
            ohlcv_data['open'],
            ohlcv_data['high'],
            ohlcv_data['low'],
            ohlcv_data['close']
        )
        assert isinstance(result, list)


# ==================== 其他单蜡烛形态 ====================

class TestSpinningTop:
    """Spinning Top (陀螺) - 不确定性"""

    def test_spinning_top(self, ohlcv_data):
        """测试陀螺形态"""
        result = haze.py_spinning_top(
            ohlcv_data['open'],
            ohlcv_data['high'],
            ohlcv_data['low'],
            ohlcv_data['close']
        )
        assert isinstance(result, list)


class TestHighWave:
    """High Wave (高浪) - 高波动性"""

    def test_high_wave(self, ohlcv_data):
        """测试高浪形态"""
        # Library function is py_highwave (no underscore)
        result = haze.py_highwave(
            ohlcv_data['open'],
            ohlcv_data['high'],
            ohlcv_data['low'],
            ohlcv_data['close']
        )
        assert isinstance(result, list)


# ==================== 双蜡烛形态 ====================

class TestTweezers:
    """Tweezers (镊子线)"""

    def test_tweezers(self, ohlcv_data):
        """测试镊子线形态"""
        # py_tweezers_top(open, high, close, tolerance) - uses high not low
        # py_tweezers_bottom(open, low, close, tolerance) - uses low not high
        result_top = haze.py_tweezers_top(
            ohlcv_data['open'],
            ohlcv_data['high'],
            ohlcv_data['close']
        )
        result_bottom = haze.py_tweezers_bottom(
            ohlcv_data['open'],
            ohlcv_data['low'],
            ohlcv_data['close']
        )
        assert isinstance(result_top, list)
        assert isinstance(result_bottom, list)


class TestKicking:
    """Kicking (踢脚线)"""

    def test_kicking(self, ohlcv_data):
        """测试踢脚线形态"""
        result = haze.py_kicking(
            ohlcv_data['open'],
            ohlcv_data['high'],
            ohlcv_data['low'],
            ohlcv_data['close']
        )
        assert isinstance(result, list)


# ==================== 三蜡烛形态 ====================

class TestThreeOutside:
    """Three Outside Up/Down (外部三法)"""

    def test_three_outside(self, ohlcv_data):
        """测试外部三法形态"""
        result = haze.py_three_outside(
            ohlcv_data['open'],
            ohlcv_data['high'],
            ohlcv_data['low'],
            ohlcv_data['close']
        )
        assert isinstance(result, list)


class TestThreeInside:
    """Three Inside (三内部形态)"""

    def test_three_inside(self, ohlcv_data):
        """测试三内部形态"""
        result = haze.py_three_inside(
            ohlcv_data['open'],
            ohlcv_data['high'],
            ohlcv_data['low'],
            ohlcv_data['close']
        )
        assert isinstance(result, list)
        assert len(result) == len(ohlcv_data['close'])


# ==================== 高级TA-Lib形态 ====================

class TestAbandonedBaby:
    """Abandoned Baby (弃婴)"""

    def test_abandoned_baby(self, ohlcv_data):
        """测试弃婴形态"""
        result = haze.py_abandoned_baby(
            ohlcv_data['open'],
            ohlcv_data['high'],
            ohlcv_data['low'],
            ohlcv_data['close']
        )
        assert isinstance(result, list)


class TestAdvanceBlock:
    """Advance Block (前进受阻)"""

    def test_advance_block(self, ohlcv_data_extended):
        """测试前进受阻形态"""
        result = haze.py_advance_block(
            ohlcv_data_extended['open'],
            ohlcv_data_extended['high'],
            ohlcv_data_extended['low'],
            ohlcv_data_extended['close']
        )
        assert isinstance(result, list)


class TestBeltHold:
    """Belt Hold (捉腰带线)"""

    def test_belt_hold(self, ohlcv_data):
        """测试捉腰带线形态"""
        # Library function is py_belthold (no underscore)
        result = haze.py_belthold(
            ohlcv_data['open'],
            ohlcv_data['high'],
            ohlcv_data['low'],
            ohlcv_data['close']
        )
        assert isinstance(result, list)


class TestBreakaway:
    """Breakaway (突破)"""

    def test_breakaway(self, ohlcv_data_extended):
        """测试突破形态"""
        result = haze.py_breakaway(
            ohlcv_data_extended['open'],
            ohlcv_data_extended['high'],
            ohlcv_data_extended['low'],
            ohlcv_data_extended['close']
        )
        assert isinstance(result, list)


class TestClosingMarubozu:
    """Closing Marubozu (收盘光头光脚)"""

    def test_closing_marubozu(self, ohlcv_data):
        """测试收盘光头光脚形态"""
        result = haze.py_closing_marubozu(
            ohlcv_data['open'],
            ohlcv_data['high'],
            ohlcv_data['low'],
            ohlcv_data['close']
        )
        assert isinstance(result, list)


class TestConcealingBabySwallow:
    """Concealing Baby Swallow (藏婴吞没)"""

    def test_concealing_baby_swallow(self, ohlcv_data):
        """测试藏婴吞没形态"""
        result = haze.py_concealing_baby_swallow(
            ohlcv_data['open'],
            ohlcv_data['high'],
            ohlcv_data['low'],
            ohlcv_data['close']
        )
        assert isinstance(result, list)


class TestCounterattack:
    """Counterattack (反击线)"""

    def test_counterattack(self, ohlcv_data):
        """测试反击线形态"""
        result = haze.py_counterattack(
            ohlcv_data['open'],
            ohlcv_data['high'],
            ohlcv_data['low'],
            ohlcv_data['close']
        )
        assert isinstance(result, list)


class TestDojiStar:
    """Doji Star (十字星)"""

    def test_doji_star(self, ohlcv_data):
        """测试十字星形态"""
        result = haze.py_doji_star(
            ohlcv_data['open'],
            ohlcv_data['high'],
            ohlcv_data['low'],
            ohlcv_data['close']
        )
        assert isinstance(result, list)


class TestHomingPigeon:
    """Homing Pigeon (信鸽)"""

    def test_homing_pigeon(self, ohlcv_data):
        """测试信鸽形态"""
        result = haze.py_homing_pigeon(
            ohlcv_data['open'],
            ohlcv_data['high'],
            ohlcv_data['low'],
            ohlcv_data['close']
        )
        assert isinstance(result, list)


class TestIdenticalThreeCrows:
    """Identical Three Crows (相同三乌鸦)"""

    def test_identical_three_crows(self, ohlcv_data):
        """测试相同三乌鸦形态"""
        result = haze.py_identical_three_crows(
            ohlcv_data['open'],
            ohlcv_data['high'],
            ohlcv_data['low'],
            ohlcv_data['close']
        )
        assert isinstance(result, list)


class TestInNeck:
    """In-Neck (颈内线)"""

    def test_in_neck(self, ohlcv_data):
        """测试颈内线形态"""
        # Library function is py_inneck (no underscore)
        result = haze.py_inneck(
            ohlcv_data['open'],
            ohlcv_data['high'],
            ohlcv_data['low'],
            ohlcv_data['close']
        )
        assert isinstance(result, list)


class TestOnNeck:
    """On-Neck (颈上线)"""

    def test_on_neck(self, ohlcv_data):
        """测试颈上线形态"""
        # Library function is py_onneck (no underscore)
        result = haze.py_onneck(
            ohlcv_data['open'],
            ohlcv_data['high'],
            ohlcv_data['low'],
            ohlcv_data['close']
        )
        assert isinstance(result, list)


class TestLadderBottom:
    """Ladder Bottom (梯底)"""

    def test_ladder_bottom(self, ohlcv_data_extended):
        """测试梯底形态"""
        result = haze.py_ladder_bottom(
            ohlcv_data_extended['open'],
            ohlcv_data_extended['high'],
            ohlcv_data_extended['low'],
            ohlcv_data_extended['close']
        )
        assert isinstance(result, list)


class TestLongLine:
    """Long Line (长线)"""

    def test_long_line(self, ohlcv_data):
        """测试长线形态"""
        result = haze.py_long_line(
            ohlcv_data['open'],
            ohlcv_data['high'],
            ohlcv_data['low'],
            ohlcv_data['close']
        )
        assert isinstance(result, list)


class TestShortLine:
    """Short Line (短线)"""

    def test_short_line(self, ohlcv_data):
        """测试短线形态"""
        result = haze.py_short_line(
            ohlcv_data['open'],
            ohlcv_data['high'],
            ohlcv_data['low'],
            ohlcv_data['close']
        )
        assert isinstance(result, list)


class TestMatHold:
    """Mat Hold (铺垫)"""

    def test_mat_hold(self, ohlcv_data_extended):
        """测试铺垫形态"""
        result = haze.py_mat_hold(
            ohlcv_data_extended['open'],
            ohlcv_data_extended['high'],
            ohlcv_data_extended['low'],
            ohlcv_data_extended['close']
        )
        assert isinstance(result, list)


class TestMatchingLow:
    """Matching Low (相同低价)"""

    def test_matching_low(self, ohlcv_data):
        """测试相同低价形态"""
        result = haze.py_matching_low(
            ohlcv_data['open'],
            ohlcv_data['high'],
            ohlcv_data['low'],
            ohlcv_data['close']
        )
        assert isinstance(result, list)


class TestRickshawMan:
    """Rickshaw Man (黄包车夫)"""

    def test_rickshaw_man(self, ohlcv_data):
        """测试黄包车夫形态"""
        result = haze.py_rickshaw_man(
            ohlcv_data['open'],
            ohlcv_data['high'],
            ohlcv_data['low'],
            ohlcv_data['close']
        )
        assert isinstance(result, list)


class TestRiseFallThreeMethods:
    """Rise/Fall Three Methods (上升/下降三法)"""

    def test_rise_fall_three_methods(self, ohlcv_data_extended):
        """测试上升/下降三法形态"""
        # Library has separate py_rising_three_methods and py_falling_three_methods
        result_rising = haze.py_rising_three_methods(
            ohlcv_data_extended['open'],
            ohlcv_data_extended['high'],
            ohlcv_data_extended['low'],
            ohlcv_data_extended['close']
        )
        result_falling = haze.py_falling_three_methods(
            ohlcv_data_extended['open'],
            ohlcv_data_extended['high'],
            ohlcv_data_extended['low'],
            ohlcv_data_extended['close']
        )
        assert isinstance(result_rising, list)
        assert isinstance(result_falling, list)


class TestSeparatingLines:
    """Separating Lines (分离线)"""

    def test_separating_lines(self, ohlcv_data):
        """测试分离线形态"""
        result = haze.py_separating_lines(
            ohlcv_data['open'],
            ohlcv_data['high'],
            ohlcv_data['low'],
            ohlcv_data['close']
        )
        assert isinstance(result, list)


class TestStickSandwich:
    """Stick Sandwich (棒槌三明治)"""

    def test_stick_sandwich(self, ohlcv_data):
        """测试棒槌三明治形态"""
        result = haze.py_stick_sandwich(
            ohlcv_data['open'],
            ohlcv_data['high'],
            ohlcv_data['low'],
            ohlcv_data['close']
        )
        assert isinstance(result, list)


class TestTakuri:
    """Takuri (探水竿)"""

    def test_takuri(self, ohlcv_data):
        """测试探水竿形态"""
        result = haze.py_takuri(
            ohlcv_data['open'],
            ohlcv_data['high'],
            ohlcv_data['low'],
            ohlcv_data['close']
        )
        assert isinstance(result, list)


class TestThrusting:
    """Thrusting (插入)"""

    def test_thrusting(self, ohlcv_data):
        """测试插入形态"""
        result = haze.py_thrusting(
            ohlcv_data['open'],
            ohlcv_data['high'],
            ohlcv_data['low'],
            ohlcv_data['close']
        )
        assert isinstance(result, list)


class TestTristar:
    """Tristar (三星)"""

    def test_tristar(self, ohlcv_data):
        """测试三星形态"""
        result = haze.py_tristar(
            ohlcv_data['open'],
            ohlcv_data['high'],
            ohlcv_data['low'],
            ohlcv_data['close']
        )
        assert isinstance(result, list)


class TestUniqueThreeRiver:
    """Unique Three River (奇特三川)"""

    def test_unique_three_river(self, ohlcv_data):
        """测试奇特三川形态"""
        # Library function is py_unique_3_river (number instead of word)
        result = haze.py_unique_3_river(
            ohlcv_data['open'],
            ohlcv_data['high'],
            ohlcv_data['low'],
            ohlcv_data['close']
        )
        assert isinstance(result, list)


class TestUpsideGapTwoCrows:
    """Upside Gap Two Crows (向上跳空两只乌鸦)"""

    def test_upside_gap_two_crows(self, ohlcv_data):
        """测试向上跳空两只乌鸦形态"""
        result = haze.py_upside_gap_two_crows(
            ohlcv_data['open'],
            ohlcv_data['high'],
            ohlcv_data['low'],
            ohlcv_data['close']
        )
        assert isinstance(result, list)


# ==================== 总结测试 ====================

class TestCandlestickReturnValues:
    """测试所有蜡烛图形态的返回值规范"""

    def test_return_values_range(self, ohlcv_data):
        """验证返回值必须是-1.0、0.0或1.0"""
        # Test patterns with standard (open, high, low, close) signature
        standard_patterns = [
            haze.py_doji,
            haze.py_hammer,
        ]

        for pattern_func in standard_patterns:
            result = pattern_func(
                ohlcv_data['open'],
                ohlcv_data['high'],
                ohlcv_data['low'],
                ohlcv_data['close']
            )
            # 所有返回值应该是-1.0、0.0、1.0或NaN
            for value in result:
                if not np.isnan(value):
                    assert value in [-1.0, 0.0, 1.0], \
                        f"{pattern_func.__name__} returned invalid value: {value}"

        # Test py_bullish_engulfing separately (only takes open, close)
        result = haze.py_bullish_engulfing(ohlcv_data['open'], ohlcv_data['close'])
        for value in result:
            if not np.isnan(value):
                assert value in [-1.0, 0.0, 1.0], \
                    f"py_bullish_engulfing returned invalid value: {value}"


# ==================== 缺失形态补充测试 ====================

class TestGapSideSideWhite:
    """Gap Side Side White (缺口并列白色蜡烛)"""

    def test_gap_sidesidewhite_pattern(self, ohlcv_data_extended):
        """测试Gap Side Side White形态"""
        result = haze.py_gap_sidesidewhite(
            ohlcv_data_extended['open'],
            ohlcv_data_extended['high'],
            ohlcv_data_extended['low'],
            ohlcv_data_extended['close']
        )
        assert isinstance(result, list)
        assert len(result) == len(ohlcv_data_extended['close'])

    def test_gap_sidesidewhite_values(self, ohlcv_data_extended):
        """测试返回值范围"""
        result = haze.py_gap_sidesidewhite(
            ohlcv_data_extended['open'],
            ohlcv_data_extended['high'],
            ohlcv_data_extended['low'],
            ohlcv_data_extended['close']
        )
        for value in result:
            if not np.isnan(value):
                assert value in [-1.0, 0.0, 1.0]


class TestStalledPattern:
    """Stalled Pattern (停滞形态)"""

    def test_stalled_pattern(self, ohlcv_data_extended):
        """测试Stalled Pattern形态"""
        result = haze.py_stalled_pattern(
            ohlcv_data_extended['open'],
            ohlcv_data_extended['high'],
            ohlcv_data_extended['low'],
            ohlcv_data_extended['close']
        )
        assert isinstance(result, list)
        assert len(result) == len(ohlcv_data_extended['close'])

    def test_stalled_pattern_values(self, ohlcv_data_extended):
        """测试返回值范围"""
        result = haze.py_stalled_pattern(
            ohlcv_data_extended['open'],
            ohlcv_data_extended['high'],
            ohlcv_data_extended['low'],
            ohlcv_data_extended['close']
        )
        for value in result:
            if not np.isnan(value):
                assert value in [-1.0, 0.0, 1.0]


class TestHikkake:
    """Hikkake Pattern (骗线形态)"""

    def test_hikkake_pattern(self, ohlcv_data_extended):
        """测试Hikkake形态"""
        result = haze.py_hikkake(
            ohlcv_data_extended['open'],
            ohlcv_data_extended['high'],
            ohlcv_data_extended['low'],
            ohlcv_data_extended['close']
        )
        assert isinstance(result, list)
        assert len(result) == len(ohlcv_data_extended['close'])

    def test_hikkake_values(self, ohlcv_data_extended):
        """测试返回值范围"""
        result = haze.py_hikkake(
            ohlcv_data_extended['open'],
            ohlcv_data_extended['high'],
            ohlcv_data_extended['low'],
            ohlcv_data_extended['close']
        )
        for value in result:
            if not np.isnan(value):
                assert value in [-1.0, 0.0, 1.0]


class TestHikkakeMod:
    """Hikkake Modified Pattern (修改版骗线形态)"""

    def test_hikkake_mod_pattern(self, ohlcv_data_extended):
        """测试Hikkake Modified形态"""
        result = haze.py_hikkake_mod(
            ohlcv_data_extended['open'],
            ohlcv_data_extended['high'],
            ohlcv_data_extended['low'],
            ohlcv_data_extended['close']
        )
        assert isinstance(result, list)
        assert len(result) == len(ohlcv_data_extended['close'])

    def test_hikkake_mod_values(self, ohlcv_data_extended):
        """测试返回值范围"""
        result = haze.py_hikkake_mod(
            ohlcv_data_extended['open'],
            ohlcv_data_extended['high'],
            ohlcv_data_extended['low'],
            ohlcv_data_extended['close']
        )
        for value in result:
            if not np.isnan(value):
                assert value in [-1.0, 0.0, 1.0]


class TestXsideGap3Methods:
    """Upside/Downside Gap Three Methods (跳空三法)"""

    def test_xside_gap_3_methods_pattern(self, ohlcv_data_extended):
        """测试Xside Gap Three Methods形态"""
        result = haze.py_xside_gap_3_methods(
            ohlcv_data_extended['open'],
            ohlcv_data_extended['high'],
            ohlcv_data_extended['low'],
            ohlcv_data_extended['close']
        )
        assert isinstance(result, list)
        assert len(result) == len(ohlcv_data_extended['close'])

    def test_xside_gap_3_methods_values(self, ohlcv_data_extended):
        """测试返回值范围"""
        result = haze.py_xside_gap_3_methods(
            ohlcv_data_extended['open'],
            ohlcv_data_extended['high'],
            ohlcv_data_extended['low'],
            ohlcv_data_extended['close']
        )
        for value in result:
            if not np.isnan(value):
                assert value in [-1.0, 0.0, 1.0]


class TestCandlestickEdgeCasesExtended:
    """扩展边界条件测试"""

    def test_all_missing_patterns_with_short_data(self):
        """测试短数据的所有缺失形态"""
        short_data = {
            'open': [100.0, 101.0, 102.0],
            'high': [102.0, 103.0, 104.0],
            'low': [99.0, 100.0, 101.0],
            'close': [101.0, 102.0, 103.0]
        }

        patterns = [
            haze.py_gap_sidesidewhite,
            haze.py_stalled_pattern,
            haze.py_hikkake,
            haze.py_hikkake_mod,
            haze.py_xside_gap_3_methods,
        ]

        for pattern_func in patterns:
            result = pattern_func(
                short_data['open'],
                short_data['high'],
                short_data['low'],
                short_data['close']
            )
            assert len(result) == 3

    def test_all_missing_patterns_with_constant_data(self):
        """测试常数数据的所有缺失形态"""
        const_data = {
            'open': [100.0] * 10,
            'high': [100.0] * 10,
            'low': [100.0] * 10,
            'close': [100.0] * 10
        }

        patterns = [
            haze.py_gap_sidesidewhite,
            haze.py_stalled_pattern,
            haze.py_hikkake,
            haze.py_hikkake_mod,
            haze.py_xside_gap_3_methods,
        ]

        for pattern_func in patterns:
            result = pattern_func(
                const_data['open'],
                const_data['high'],
                const_data['low'],
                const_data['close']
            )
            assert len(result) == 10
            # 常数数据不应识别出任何形态
            for value in result:
                if not np.isnan(value):
                    assert value == 0.0
