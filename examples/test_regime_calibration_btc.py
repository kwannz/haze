#!/usr/bin/env python3
"""
BTC真实数据校准测试

使用真实BTC历史数据校准市场状态检测器的阈值参数
主要目标：
1. 验证ADX在真实数据中的有效性（合成数据全为0）
2. 计算各市场状态的指标分布（range%, ATR%, ADX等）
3. 基于统计分析提出优化阈值建议
4. 测试检测准确率
"""

import json
import os
import sys
import math
from typing import Dict, List, Any

# 添加src到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import haze_library as haze


# 使用400根K线窗口进行分析（与detect_market_regime的period参数一致）
ANALYSIS_PERIOD = 400


class BTCRegimeCalibrator:
    """BTC真实数据校准器"""

    def __init__(self, data_file: str = '../data/btc_calibration_data.json'):
        """加载BTC历史数据"""
        filepath = os.path.join(os.path.dirname(__file__), data_file)

        with open(filepath, 'r', encoding='utf-8') as f:
            self.data = json.load(f)

        self.metadata = self.data['metadata']
        self.samples = self.data['samples']

        # 统计数据存储
        self.metrics_by_regime = {
            'TRENDING': [],
            'RANGING': [],
            'VOLATILE': [],
        }

        self.test_results = []

    def calculate_metrics(self, high: List[float], low: List[float], close: List[float],
                         volume: List[float], period: int = ANALYSIS_PERIOD) -> Dict[str, float]:
        """
        计算技术指标（使用指定窗口期）

        Args:
            high, low, close, volume: OHLCV数据
            period: 分析窗口（默认300根K线）

        Returns:
            指标字典 {range_pct, atr_pct, adx, price_change_pct}
        """
        import haze_library as _ext

        n = len(close)
        period = min(period, n)

        # 1. 价格区间%
        recent_high = max(high[-period:]) if period > 0 else max(high)
        recent_low = min(low[-period:]) if period > 0 else min(low)
        range_pct = ((recent_high - recent_low) / recent_low) * 100 if recent_low > 0 else 0.0

        # 2. ATR%
        try:
            atr = _ext.py_atr(high, low, close, period)
            atr_val = atr[-1] if len(atr) > 0 else 0.0
            current_price = close[-1]
            atr_pct = (atr_val / current_price) * 100 if current_price > 0 else 0.0
        except Exception:
            atr_pct = 0.0

        # 3. 价格变化%
        price_change_pct = ((close[-1] - close[-period]) / close[-period]) * 100 if period > 0 else 0.0

        # 4. ADX (关键验证点：在真实数据中是否有效?)
        adx_val = 0.0
        try:
            adx = _ext.py_adx(high, low, close, period)
            adx_val = adx[-1] if len(adx) > 0 and not math.isnan(adx[-1]) else 0.0
        except Exception:
            pass

        return {
            'range_pct': range_pct,
            'atr_pct': atr_pct,
            'adx': adx_val,
            'price_change_pct': price_change_pct,
        }

    def map_regime_to_category(self, regime_label: str) -> str:
        """
        将详细的regime标签映射到三大类

        Args:
            regime_label: TRENDING_BULL, TRENDING_BEAR, RANGING_TIGHT等

        Returns:
            TRENDING | RANGING | VOLATILE
        """
        if 'TRENDING' in regime_label:
            return 'TRENDING'
        elif 'RANGING' in regime_label:
            return 'RANGING'
        elif 'VOLATILE' in regime_label:
            return 'VOLATILE'
        else:
            return 'UNKNOWN'

    def test_sample(self, sample: Dict[str, Any], expected_regime: str) -> Dict[str, Any]:
        """
        测试单个样本的检测准确性

        Args:
            sample: 样本数据
            expected_regime: 预期的市场状态（TRENDING/RANGING/VOLATILE）

        Returns:
            测试结果字典
        """
        data = sample['data']
        high = data['high']
        low = data['low']
        close = data['close']
        volume = data['volume']

        # 计算指标
        metrics = self.calculate_metrics(high, low, close, volume, ANALYSIS_PERIOD)

        # 调用haze的市场状态检测
        try:
            signals = haze.lt_indicator(high, low, close, volume, auto_regime=True)
            detected_regime = signals.get('market_regime', 'UNKNOWN')
        except Exception as e:
            detected_regime = 'ERROR'
            print(f"      检测错误: {str(e)}")

        # 判断准确性
        is_correct = (detected_regime == expected_regime)

        result = {
            'label': sample['label'],
            'description': sample['description'],
            'expected': expected_regime,
            'detected': detected_regime,
            'correct': is_correct,
            'metrics': metrics,
            'bars': sample['actual_bars'],
        }

        return result

    def analyze_all_samples(self):
        """分析所有样本并收集统计数据"""
        print("=" * 80)
        print("BTC真实数据校准测试")
        print("=" * 80)
        print(f"\n数据源: {self.metadata['exchange']}")
        print(f"交易对: {self.metadata['symbol']}")
        print(f"时间框架: {self.metadata['timeframe']}")
        print(f"分析窗口: {ANALYSIS_PERIOD}根K线")
        print(f"总样本数: {self.metadata['total_samples']}")
        print(f"总K线数: {self.metadata['total_bars']}")

        for regime_type, samples_list in self.samples.items():
            print(f"\n{'=' * 80}")
            print(f"📊 测试 {regime_type} ({len(samples_list)}个样本)")
            print(f"{'=' * 80}")

            expected_category = self.map_regime_to_category(regime_type)

            for sample in samples_list:
                print(f"\n   • {sample['label']}")
                print(f"     描述: {sample['description']}")
                print(f"     K线数: {sample['actual_bars']}")

                result = self.test_sample(sample, expected_category)
                self.test_results.append(result)

                # 收集指标统计
                self.metrics_by_regime[expected_category].append(result['metrics'])

                # 输出结果
                status = "✅" if result['correct'] else "❌"
                print(f"     预期: {result['expected']}")
                print(f"     检测: {result['detected']} {status}")
                print(f"     指标: Range={result['metrics']['range_pct']:.2f}%  "
                      f"PriceChange={result['metrics']['price_change_pct']:.2f}%  "
                      f"ATR={result['metrics']['atr_pct']:.2f}%  "
                      f"ADX={result['metrics']['adx']:.2f}")

    def calculate_statistics(self):
        """计算各市场状态的指标统计分布"""
        print(f"\n{'=' * 80}")
        print("📊 指标分布统计（基于真实BTC数据）")
        print(f"{'=' * 80}")

        import statistics

        for regime, metrics_list in self.metrics_by_regime.items():
            if not metrics_list:
                continue

            print(f"\n【{regime}】 (样本数: {len(metrics_list)})")

            # Range%统计
            range_values = [m['range_pct'] for m in metrics_list]
            print(f"   Range% 分布:")
            print(f"      Min:    {min(range_values):>8.2f}%")
            print(f"      20th:   {self._percentile(range_values, 20):>8.2f}%")
            print(f"      Median: {statistics.median(range_values):>8.2f}%")
            print(f"      80th:   {self._percentile(range_values, 80):>8.2f}%")
            print(f"      Max:    {max(range_values):>8.2f}%")

            # ATR%统计
            atr_values = [m['atr_pct'] for m in metrics_list]
            print(f"   ATR% 分布:")
            print(f"      Min:    {min(atr_values):>8.2f}%")
            print(f"      20th:   {self._percentile(atr_values, 20):>8.2f}%")
            print(f"      Median: {statistics.median(atr_values):>8.2f}%")
            print(f"      80th:   {self._percentile(atr_values, 80):>8.2f}%")
            print(f"      Max:    {max(atr_values):>8.2f}%")

            # ADX统计（关键验证点）
            adx_values = [m['adx'] for m in metrics_list]
            print(f"   ADX 分布:")
            print(f"      Min:    {min(adx_values):>8.2f}")
            print(f"      20th:   {self._percentile(adx_values, 20):>8.2f}")
            print(f"      Median: {statistics.median(adx_values):>8.2f}")
            print(f"      80th:   {self._percentile(adx_values, 80):>8.2f}")
            print(f"      Max:    {max(adx_values):>8.2f}")

            # 价格变化%统计
            price_change_values = [m['price_change_pct'] for m in metrics_list]
            print(f"   Price Change% 分布:")
            print(f"      Min:    {min(price_change_values):>8.2f}%")
            print(f"      Median: {statistics.median(price_change_values):>8.2f}%")
            print(f"      Max:    {max(price_change_values):>8.2f}%")

    def suggest_thresholds(self):
        """基于统计分析提出优化阈值建议"""
        print(f"\n{'=' * 80}")
        print("🎯 优化阈值建议（基于{ANALYSIS_PERIOD}根K线窗口）")
        print(f"{'=' * 80}")

        # TRENDING阈值建议
        if self.metrics_by_regime['TRENDING']:
            trending_ranges = [m['range_pct'] for m in self.metrics_by_regime['TRENDING']]
            trending_adx = [m['adx'] for m in self.metrics_by_regime['TRENDING']]

            suggested_range = self._percentile(trending_ranges, 20)
            suggested_adx = self._percentile(trending_adx, 20)

            print(f"\n【TRENDING 阈值】")
            print(f"   当前阈值: range_pct > 30%  或  adx > 20")
            print(f"   建议阈值: range_pct > {suggested_range:.1f}%  或  adx > {suggested_adx:.1f}")
            print(f"   理由: 基于20th百分位，确保捕获80%的TRENDING样本")

        # VOLATILE阈值建议
        if self.metrics_by_regime['VOLATILE']:
            volatile_atr = [m['atr_pct'] for m in self.metrics_by_regime['VOLATILE']]
            suggested_atr = self._percentile(volatile_atr, 20)

            print(f"\n【VOLATILE 阈值】")
            print(f"   当前阈值: atr_pct > 4.5%")
            print(f"   建议阈值: atr_pct > {suggested_atr:.1f}%")
            print(f"   理由: 基于20th百分位，确保捕获80%的VOLATILE样本")

        # RANGING默认值
        print(f"\n【RANGING 阈值】")
        print(f"   保持默认: 其他情况归为RANGING")

    def print_summary(self):
        """打印测试总结"""
        print(f"\n{'=' * 80}")
        print("📊 测试总结")
        print(f"{'=' * 80}")

        total = len(self.test_results)
        correct = sum(1 for r in self.test_results if r['correct'])
        accuracy = (correct / total * 100) if total > 0 else 0

        print(f"\n总样本数: {total}")
        print(f"检测正确: {correct}")
        print(f"检测错误: {total - correct}")
        print(f"准确率:   {accuracy:.1f}%")

        print(f"\n错误样本详情:")
        for result in self.test_results:
            if not result['correct']:
                print(f"   ❌ {result['label']}")
                print(f"      预期: {result['expected']}  检测: {result['detected']}")
                print(f"      Range={result['metrics']['range_pct']:.2f}%  "
                      f"ATR={result['metrics']['atr_pct']:.2f}%  "
                      f"ADX={result['metrics']['adx']:.2f}")

    def _percentile(self, values: List[float], percentile: int) -> float:
        """计算百分位数"""
        if not values:
            return 0.0

        sorted_values = sorted(values)
        index = int(len(sorted_values) * percentile / 100)
        index = min(index, len(sorted_values) - 1)
        return sorted_values[index]


def main():
    """主函数"""
    print("\n")

    try:
        # 创建校准器
        calibrator = BTCRegimeCalibrator()

        # 分析所有样本
        calibrator.analyze_all_samples()

        # 计算统计分布
        calibrator.calculate_statistics()

        # 提出阈值建议
        calibrator.suggest_thresholds()

        # 打印总结
        calibrator.print_summary()

        print(f"\n{'=' * 80}")
        print("✅ 校准分析完成")
        print(f"{'=' * 80}")

        print(f"\n💡 关键发现:")
        print(f"   1. ADX在真实数据中是否有效? (检查上方ADX分布)")
        print(f"   2. 300根K线窗口需要的阈值远低于30% (检查建议阈值)")
        print(f"   3. 当前准确率可能较低，需要应用新阈值后重新测试")

        print(f"\n下一步:")
        print(f"   根据建议阈值修改 src/haze_library/lt_indicators.py 中的 detect_market_regime 函数")

    except FileNotFoundError as e:
        print(f"\n❌ 错误: 找不到数据文件")
        print(f"   请先运行: python examples/btc_data_collector.py")
        sys.exit(1)

    except Exception as e:
        print(f"\n❌ 错误: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
