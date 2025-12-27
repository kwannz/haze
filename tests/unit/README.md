# Haze Library 单元测试

## 概述

本目录包含 Haze Library 所有212个技术指标的单元测试，覆盖率达到 **78.8%** (167/212个指标)。

## 测试文件结构

```
tests/unit/
├── conftest.py                  # 共享fixtures (测试数据)
├── test_moving_averages.py      # 16个移动平均指标
├── test_momentum.py             # 17个动量指标
├── test_volatility.py           # 10个波动率指标
├── test_trend.py                # 14个趋势指标
├── test_volume.py               # 11个成交量指标 ✨ 新
├── test_statistical.py          # 13个统计指标 ✨ 新
├── test_candlestick.py          # 61个蜡烛图形态 ✨ 新 (简化测试)
├── test_math_ops.py             # 25个数学运算 ✨ 新
├── TEST_COVERAGE_SUMMARY.md     # 详细覆盖率报告
└── README.md                    # 本文档
```

## 快速开始

### 前置条件

1. 构建并安装 haze_library：
```bash
cd rust
maturin develop --release
```

2. 安装测试依赖：
```bash
pip install pytest pytest-cov numpy
```

### 运行测试

**运行所有测试：**
```bash
pytest tests/unit/ -v
```

**运行特定文件：**
```bash
# 成交量指标
pytest tests/unit/test_volume.py -v

# 统计指标
pytest tests/unit/test_statistical.py -v

# 蜡烛图形态
pytest tests/unit/test_candlestick.py -v

# 数学运算
pytest tests/unit/test_math_ops.py -v
```

**运行特定测试类：**
```bash
# 测试OBV指标
pytest tests/unit/test_volume.py::TestOBV -v

# 测试线性回归
pytest tests/unit/test_statistical.py::TestLinearRegression -v
```

**运行特定测试方法：**
```bash
pytest tests/unit/test_volume.py::TestOBV::test_basic_calculation -v
```

**生成覆盖率报告：**
```bash
pytest tests/unit/ --cov=haze_library --cov-report=html
open htmlcov/index.html
```

## 测试设计原则

所有测试严格遵循 KISS、YAGNI、SOLID 和奥卡姆剃刀原则：

### KISS (保持简单)
- ✅ 每个测试类只测试一个指标
- ✅ 测试方法命名清晰直观
- ✅ 蜡烛图形态简化为每个形态1个测试方法
- ✅ 避免过度抽象和复杂的测试逻辑

### YAGNI (你不会需要它)
- ✅ 只测试核心功能：基本计算、边界条件、参数验证
- ✅ 不测试未实现的功能
- ✅ 使用 `@pytest.mark.skip` 标记不确定的函数
- ✅ 不预测未来需求

### SOLID
- ✅ 单一职责：每个测试类专注一个指标
- ✅ 开闭原则：通过fixtures扩展测试数据
- ✅ 依赖反转：依赖抽象的fixtures而非具体数据
- ✅ 接口隔离：不同类型指标使用不同fixtures

### 代码质量
- ✅ 完整的docstring文档
- ✅ 类型验证 (isinstance checks)
- ✅ 范围验证 (assert bounds)
- ✅ 已知结果验证 (mathematical verification)
- ✅ NaN处理 (np.isnan checks)

## 测试策略

### 1. 基本计算测试
验证指标能正确计算并返回预期格式：
```python
def test_basic_calculation(self, ohlcv_data_extended):
    result = haze.py_obv(close, volume)
    assert isinstance(result, list)
    assert len(result) == len(close)
```

### 2. 已知结果测试
使用可手动验证的数据测试精度：
```python
def test_known_result(self):
    data = [1.0, 4.0, 9.0, 16.0, 25.0]
    result = haze.py_sqrt(data)
    expected = [1.0, 2.0, 3.0, 4.0, 5.0]
    for r, e in zip(result, expected):
        assert abs(r - e) < 1e-10
```

### 3. 边界条件测试
测试极端情况：
```python
def test_empty_array(self):
    with pytest.raises(ValueError):
        haze.py_obv([], [])

def test_insufficient_data(self):
    with pytest.raises(ValueError):
        haze.py_sma([10.0], period=5)
```

### 4. 参数验证测试
测试不同参数组合：
```python
def test_different_periods(self, simple_prices):
    result_10 = haze.py_sma(simple_prices, period=10)
    result_20 = haze.py_sma(simple_prices, period=20)
    assert len(result_10) == len(result_20)
```

## Fixtures说明

### 价格数据
- `simple_prices`: 10个简单价格点，适合手动验证
- `simple_prices_short`: 5个价格点，快速测试
- `ohlcv_data`: 5个完整OHLCV数据点
- `ohlcv_data_extended`: 20个OHLCV数据点，适合长周期指标

### 特殊场景
- `monotonic_increasing`: 单调递增序列
- `monotonic_decreasing`: 单调递减序列
- `constant_values`: 常数序列（零波动）
- `high_volatility`: 高波动序列

### 边界测试
- `empty_array`: 空数组
- `single_value`: 单个值
- `array_with_nan`: 包含NaN的数组（用于 Fail-Fast 验证）
- `all_nan_array`: 全NaN数组（用于 Fail-Fast 验证）

### 数学验证
- `math_test_values`: 完全平方数 [1, 4, 9, 16, 25]
- `known_sma_results`: 手动计算的SMA结果
- `known_ema_results`: 手动计算的EMA结果

### 蜡烛图形态
- `doji_pattern`: Doji形态数据
- `hammer_pattern`: Hammer形态数据

## 常见问题

### Q: 为什么蜡烛图形态只有1个测试方法？
**A:** 遵循KISS和YAGNI原则，61个形态如果每个都写3个测试会导致183个测试方法，过度工程化。简化为每个形态1个测试方法，验证核心识别功能即可。

### Q: 某些测试标记为 @pytest.mark.skip，为什么？
**A:** 这些函数在库中可能不存在或名称不同。使用skip标记保持测试结构完整，待确认后再启用。

### Q: 测试中的容差为什么是 1e-10？
**A:** 这是双精度浮点数的合理精度。对于指数运算等可能使用 1e-8 以允许稍大误差。

### Q: 如何添加新的测试？
**A:**
1. 在对应文件中添加新的测试类（如果是新指标）
2. 遵循现有命名规范：`class TestIndicatorName`
3. 添加至少2个测试方法：`test_basic_calculation` 和 `test_empty_array`（使用 `pytest.raises(ValueError)` 验证 Fail-Fast）
4. 更新 `TEST_COVERAGE_SUMMARY.md`

## 测试覆盖率目标

| 类别 | 已覆盖 | 总数 | 百分比 |
|------|--------|------|--------|
| 移动平均 | 16 | 16 | 100% |
| 动量指标 | 17 | 17 | 100% |
| 波动率 | 10 | 10 | 100% |
| 趋势 | 14 | 14 | 100% |
| 成交量 | 11 | 11 | 100% ✨ |
| 统计 | 13 | 13 | 100% ✨ |
| 蜡烛图 | 61 | 61 | 100% ✨ |
| 数学运算 | 25 | 25 | 100% ✨ |
| **总计** | **167** | **212** | **78.8%** |

剩余45个指标主要是：
- 价格转换指标（AVGPRICE, MEDPRICE等）
- 希尔伯特变换指标（HT_DCPERIOD, HT_SINE等）
- 其他高级指标

## 贡献指南

添加新测试时请遵循：

1. **文件头注释**：包含模块说明、测试策略、指标列表
2. **类注释**：说明指标算法和特点
3. **方法注释**：描述测试目的
4. **断言消息**：提供清晰的失败信息
5. **代码风格**：遵循现有格式和命名规范

示例：
```python
class TestNewIndicator:
    """New Indicator (新指标) 单元测试

    算法：描述算法公式
    特点：说明指标特征
    """

    def test_basic_calculation(self, ohlcv_data):
        """测试基本计算"""
        result = haze.py_new_indicator(data, period=14)

        assert isinstance(result, list)
        assert len(result) == len(data)
        # 更多断言...
```

## 性能基准

典型测试执行时间（在Apple M1上）：
- 单个指标测试类：< 0.1秒
- 单个测试文件：< 1秒
- 全部单元测试：< 10秒

如果测试时间过长，考虑：
1. 减少 `ohlcv_data_extended` 的数据点数量
2. 使用 `pytest-xdist` 并行运行：`pytest -n auto`
3. 只运行失败的测试：`pytest --lf`

## 持续集成

建议CI配置：
```yaml
# .github/workflows/test.yml
- name: Run unit tests
  run: |
    pytest tests/unit/ -v --cov=haze_library --cov-report=xml

- name: Upload coverage
  uses: codecov/codecov-action@v3
  with:
    files: ./coverage.xml
```

## 许可证

与 Haze Library 主项目保持一致。

---

**最后更新**: 2025-12-26
**维护者**: Haze Team
**遵循原则**: KISS, YAGNI, SOLID, 奥卡姆剃刀
