#!/usr/bin/env python3
"""
BTC历史数据采集器 - 用于市场状态检测器的真实数据校准

从Binance采集14个代表性历史时间段的BTC/USDT 1小时K线数据
每个片段300-500根K线，覆盖6种市场状态：
- TRENDING_BULL (牛市趋势)
- TRENDING_BEAR (熊市趋势)
- RANGING_TIGHT (窄幅震荡)
- RANGING_WIDE (宽幅震荡)
- VOLATILE_CRASH (闪崩)
- VOLATILE_PUMP (暴涨)
"""

import ccxt
import json
import time
from datetime import datetime, timedelta
from typing import List, Dict, Any
import os


class BTCDataCollector:
    """BTC历史数据采集器"""

    def __init__(self):
        """初始化Binance交易所连接"""
        self.exchange = ccxt.binance({
            'enableRateLimit': True,  # 启用频率限制
            'options': {
                'defaultType': 'spot',  # 现货交易
            }
        })
        self.symbol = 'BTC/USDT'
        self.timeframe = '1h'

        # 24个代表性历史片段定义（14个常规 + 10个极端样本）
        self.data_requirements = {
            'TRENDING_BULL': [
                {
                    'label': 'bull_2023_q4',
                    'start': '2023-10-01 00:00:00',
                    'end': '2023-11-30 23:59:59',
                    'description': 'Q4 2023牛市启动',
                    'bars': 500
                },
                {
                    'label': 'accumulation_2023_recovery',
                    'start': '2023-01-01 00:00:00',
                    'end': '2023-03-31 23:59:59',
                    'description': '2023复苏上涨 $16k-$25k +36%（原标注为积累）',
                    'bars': 500
                },
                {
                    'label': 'ranging_wide_2023_spring',
                    'start': '2023-03-01 00:00:00',
                    'end': '2023-04-30 23:59:59',
                    'description': '银行危机后强势反弹（原标注为波动）',
                    'bars': 500
                },
                {
                    'label': 'bull_2024_q1',
                    'start': '2024-02-01 00:00:00',
                    'end': '2024-03-31 23:59:59',
                    'description': 'Q1 2024冲击历史新高',
                    'bars': 500
                },
                {
                    'label': 'pump_2024_ath',
                    'start': '2024-02-28 00:00:00',
                    'end': '2024-03-14 23:59:59',
                    'description': '突破历史新高（原标注为暴涨）',
                    'bars': 300
                },
                {
                    'label': 'bull_2024_q4',
                    'start': '2024-10-01 00:00:00',
                    'end': '2024-11-30 23:59:59',
                    'description': 'Q4 2024选举行情',
                    'bars': 500
                },
                {
                    'label': 'pump_2024_election',
                    'start': '2024-10-28 00:00:00',
                    'end': '2024-11-10 23:59:59',
                    'description': '选举上涨（原标注为暴涨）',
                    'bars': 300
                },
            ],
            'TRENDING_BEAR': [
                {
                    'label': 'bear_2022_luna',
                    'start': '2022-05-01 00:00:00',
                    'end': '2022-06-30 23:59:59',
                    'description': 'Luna崩盘引发熊市',
                    'bars': 500
                },
                {
                    'label': 'bear_2022_ftx',
                    'start': '2022-11-01 00:00:00',
                    'end': '2022-12-31 23:59:59',
                    'description': 'FTX崩盘',
                    'bars': 500
                },
                {
                    'label': 'crash_2024_yen_carry',
                    'start': '2024-08-01 00:00:00',
                    'end': '2024-08-10 23:59:59',
                    'description': '日元套利平仓急跌（原标注为闪崩）',
                    'bars': 300
                },
                {
                    'label': 'crash_2022_luna',
                    'start': '2022-05-05 00:00:00',
                    'end': '2022-05-15 23:59:59',
                    'description': 'Luna闪崩（原标注为崩盘）',
                    'bars': 300
                },
                {
                    'label': 'ranging_tight_2023_summer',
                    'start': '2023-08-01 00:00:00',
                    'end': '2023-09-30 23:59:59',
                    'description': '2023夏季下跌（原标注为震荡）',
                    'bars': 500
                },
                {
                    'label': 'ranging_wide_2024_summer',
                    'start': '2024-06-01 00:00:00',
                    'end': '2024-07-31 23:59:59',
                    'description': '2024夏季下跌（原标注为宽幅震荡）',
                    'bars': 500
                },
            ],
            'RANGING_TIGHT': [
                {
                    'label': 'ranging_tight_2024_spring',
                    'start': '2024-04-15 00:00:00',
                    'end': '2024-05-15 23:59:59',
                    'description': 'ATH后盘整',
                    'bars': 300
                },
            ],
            'RANGING_WIDE': [
                {
                    'label': 'bear_2024_summer',
                    'start': '2024-08-01 00:00:00',
                    'end': '2024-09-15 23:59:59',
                    'description': '2024夏季震荡（原标注为回调）',
                    'bars': 500
                },
            ],
            # ========== 极端市场样本 (Extreme Market Conditions) ==========
            'TRENDING_BULL_EXTREME': [
                {
                    'label': 'extreme_bull_2017_parabolic',
                    'start': '2017-11-01 00:00:00',
                    'end': '2017-12-17 23:59:59',
                    'description': '2017抛物线暴涨 $7k→$20k',
                    'bars': 500
                },
                {
                    'label': 'extreme_bull_2020_institutional',
                    'start': '2020-10-01 00:00:00',
                    'end': '2020-12-31 23:59:59',
                    'description': '2020机构FOMO $10k→$29k',
                    'bars': 500
                },
            ],
            'TRENDING_BEAR_EXTREME': [
                {
                    'label': 'extreme_bear_2020_covid',
                    'start': '2020-03-01 00:00:00',
                    'end': '2020-03-13 23:59:59',
                    'description': 'COVID黑天鹅 $10k→$3.8k',
                    'bars': 300
                },
                {
                    'label': 'extreme_bear_2018_capitulation',
                    'start': '2018-11-01 00:00:00',
                    'end': '2018-12-15 23:59:59',
                    'description': '2018熊市投降 $6k→$3.2k',
                    'bars': 500
                },
                {
                    'label': 'black_swan_2020_march12',
                    'start': '2020-02-20 00:00:00',
                    'end': '2020-03-20 23:59:59',
                    'description': '2020.3.12黑色星期四 -20%急跌（强方向性，Range<35%）',
                    'bars': 500
                },
                {
                    'label': 'black_swan_2021_leverage_flush',
                    'start': '2021-05-01 00:00:00',
                    'end': '2021-05-31 23:59:59',
                    'description': '2021.5.19杠杆清算 -25%暴跌（Range=98%, 方向效率0.25）',
                    'bars': 500
                },
            ],
            'RANGING_ACCUMULATION': [
                {
                    'label': 'accumulation_2018_bottom',
                    'start': '2018-12-15 00:00:00',
                    'end': '2019-03-31 23:59:59',
                    'description': '2018-2019熊市底部 $3k-$4k',
                    'bars': 500
                },
            ],
            'VOLATILE_BLACK_SWAN': [
                # Note: 原black_swan_2021_leverage_flush移至TRENDING_BEAR_EXTREME
                # 原因: Range=98%, Change=-25%, 方向效率=0.25 > 0.15阈值 → 强方向性崩盘
                # 真正的VOLATILE应该是高range但低效率的混乱震荡(efficiency < 0.15)
            ],
            'VOLATILE_CRASH': [
                # All crash samples relabeled as TRENDING_BEAR (strong directional movement takes priority)
            ],
            'VOLATILE_PUMP': [
                # All pump samples relabeled as TRENDING_BULL (strong directional movement takes priority)
            ],
        }

    def fetch_ohlcv(self, start_time: str, end_time: str, limit: int = 500) -> List[List]:
        """
        获取指定时间段的OHLCV数据

        Args:
            start_time: 开始时间 'YYYY-MM-DD HH:MM:SS'
            end_time: 结束时间 'YYYY-MM-DD HH:MM:SS'
            limit: 最大获取数量

        Returns:
            OHLCV数据列表，每个元素为 [timestamp, open, high, low, close, volume]
        """
        # 转换为时间戳（毫秒）
        start_ts = int(datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S').timestamp() * 1000)
        end_ts = int(datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S').timestamp() * 1000)

        all_ohlcv = []
        current_ts = start_ts

        print(f"   获取数据: {start_time} → {end_time}")

        # 分页获取数据
        while current_ts < end_ts:
            try:
                # 每次最多获取1000根K线
                ohlcv = self.exchange.fetch_ohlcv(
                    self.symbol,
                    self.timeframe,
                    since=current_ts,
                    limit=min(1000, limit)
                )

                if not ohlcv:
                    break

                # 过滤超出结束时间的数据
                filtered = [bar for bar in ohlcv if bar[0] <= end_ts]
                all_ohlcv.extend(filtered)

                # 更新时间戳
                current_ts = ohlcv[-1][0] + 3600000  # 1小时 = 3600000毫秒

                # 限流
                time.sleep(self.exchange.rateLimit / 1000)

                # 达到限制数量则停止
                if len(all_ohlcv) >= limit:
                    break

            except Exception as e:
                print(f"      错误: {str(e)}")
                time.sleep(5)
                continue

        # 限制数量
        result = all_ohlcv[:limit]
        print(f"      成功获取 {len(result)} 根K线")

        return result

    def format_ohlcv(self, ohlcv: List[List]) -> Dict[str, List[float]]:
        """
        将OHLCV数据格式化为字典

        Args:
            ohlcv: 原始OHLCV数据

        Returns:
            格式化后的字典 {high, low, close, volume, timestamps}
        """
        return {
            'timestamps': [bar[0] for bar in ohlcv],
            'open': [float(bar[1]) for bar in ohlcv],
            'high': [float(bar[2]) for bar in ohlcv],
            'low': [float(bar[3]) for bar in ohlcv],
            'close': [float(bar[4]) for bar in ohlcv],
            'volume': [float(bar[5]) for bar in ohlcv],
        }

    def collect_period(self, period_config: Dict[str, Any], regime_type: str) -> Dict[str, Any]:
        """
        采集单个时间段的数据

        Args:
            period_config: 时间段配置
            regime_type: 市场状态类型

        Returns:
            包含OHLCV数据和元数据的字典
        """
        label = period_config['label']
        print(f"\n📊 采集: {label}")
        print(f"   状态: {regime_type}")
        print(f"   描述: {period_config['description']}")

        # 获取OHLCV数据
        ohlcv = self.fetch_ohlcv(
            period_config['start'],
            period_config['end'],
            period_config['bars']
        )

        # 格式化数据
        formatted_data = self.format_ohlcv(ohlcv)

        # 添加元数据
        result = {
            'label': label,
            'regime': regime_type,
            'description': period_config['description'],
            'start_time': period_config['start'],
            'end_time': period_config['end'],
            'expected_bars': period_config['bars'],
            'actual_bars': len(ohlcv),
            'data': formatted_data,
        }

        return result

    def collect_all(self) -> Dict[str, List[Dict]]:
        """
        采集所有时间段的数据

        Returns:
            按市场状态分类的数据字典
        """
        print("=" * 80)
        print("BTC历史数据采集器")
        print("=" * 80)
        print(f"\n交易对: {self.symbol}")
        print(f"时间框架: {self.timeframe}")
        print(f"数据源: Binance")
        print(f"总片段数: {sum(len(periods) for periods in self.data_requirements.values())}")

        all_samples = {}
        total_bars = 0

        for regime_type, periods in self.data_requirements.items():
            samples = []

            for period_config in periods:
                sample = self.collect_period(period_config, regime_type)
                samples.append(sample)
                total_bars += sample['actual_bars']

            all_samples[regime_type] = samples

        print("\n" + "=" * 80)
        print("📊 采集完成")
        print("=" * 80)
        print(f"\n市场状态类型: {len(all_samples)}")
        print(f"总片段数: {sum(len(samples) for samples in all_samples.values())}")
        print(f"总K线数: {total_bars}")

        return all_samples

    def save_to_file(self, samples: Dict[str, List[Dict]], filename: str = 'btc_calibration_data.json'):
        """
        保存数据到JSON文件

        Args:
            samples: 采集的数据
            filename: 输出文件名
        """
        # 确保data目录存在
        data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
        os.makedirs(data_dir, exist_ok=True)

        filepath = os.path.join(data_dir, filename)

        # 添加元数据
        output = {
            'metadata': {
                'symbol': self.symbol,
                'timeframe': self.timeframe,
                'exchange': 'Binance',
                'collected_at': datetime.now().isoformat(),
                'total_samples': sum(len(samples_list) for samples_list in samples.values()),
                'total_bars': sum(
                    sample['actual_bars']
                    for samples_list in samples.values()
                    for sample in samples_list
                ),
            },
            'samples': samples,
        }

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)

        print(f"\n💾 数据已保存到: {filepath}")
        print(f"   文件大小: {os.path.getsize(filepath) / 1024:.2f} KB")


def main():
    """主函数"""
    try:
        # 创建采集器
        collector = BTCDataCollector()

        # 采集所有数据
        samples = collector.collect_all()

        # 保存到文件
        collector.save_to_file(samples)

        print("\n✅ 全部完成！")
        print("\n下一步:")
        print("   运行 python examples/test_regime_calibration_btc.py 进行校准分析")

    except KeyboardInterrupt:
        print("\n\n⚠️  用户中断")
    except Exception as e:
        print(f"\n❌ 错误: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
