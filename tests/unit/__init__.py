"""
haze-Library 单元测试模块
============================

本模块包含所有 212 个指标的单元测试，采用双重验证策略：
- 主要验证：手动计算预期值的单元测试（本目录）
- 辅助验证：精度对比 TA-Lib/pandas-ta（tests/precision_validator.py）

测试组织：
- conftest.py: pytest fixtures（共享测试数据）
- test_moving_averages.py: 16 个移动平均指标
- test_momentum.py: 17 个动量指标
- test_volatility.py: 10 个波动率指标
- test_trend.py: 14 个趋势指标
- test_volume.py: 11 个成交量指标
- test_statistical.py: 13 个统计指标
- test_candlestick.py: 61 个蜡烛图形态
- test_math_ops.py: 25 个数学运算

Author: Haze Team
Date: 2025-12-25
"""
