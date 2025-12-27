# Haze-Library 测试框架

## 📂 测试结构

```
tests/
├── README.md                    # 本文档
├── precision_validator.py       # 精度验证框架核心
├── run_precision_tests.py       # 批量精度验证脚本
├── precision_report.txt         # 生成的精度验证报告（运行后）
├── unit/                        # 单元测试（待实现）
│   ├── test_volatility.py
│   ├── test_momentum.py
│   ├── test_trend.py
│   ├── test_volume.py
│   └── test_moving_averages.py
├── validation/                  # 验证测试（已实现）
│   └── test_harmonics.py        # 谐波形态验证（23 测试用例）
└── integration/                 # 集成测试（待实现）
    ├── test_real_data.py
    └── test_performance.py
```

## 🎯 测试目标

### 阶段 1: 精度验证 ✅（当前阶段）
- **目标**：验证所有 215 个指标与参考库（pandas-ta, TA-Lib）的精度一致性
- **标准**：最大误差 < 1e-9（纳米级精度）
- **覆盖率**：100% 指标覆盖

### 阶段 2: 单元测试 ⏳（待实施）
- **目标**：代码覆盖率 > 90%
- **标准**：每个指标至少 3 个测试用例（正常、边界、异常）
- **框架**：pytest + pytest-cov

### 阶段 3: 性能测试 ⏳（待实施）
- **目标**：性能基准 vs Python 实现
- **标准**：Rust 实现 > 10x 性能提升
- **框架**：pytest-benchmark

## 🚀 快速开始

### 1. 安装依赖

```bash
# 进入项目根目录
cd /Users/zhaoleon/Desktop/haze/haze-Library

# 安装测试依赖
pip install -e ".[test]"
```

**注意**：TA-Lib 需要先安装系统库：

```bash
# macOS
brew install ta-lib

# 然后安装 Python 包装器
pip install TA-Lib
```

**Python 3.14+ 与 pandas-ta**

pandas-ta 当前强依赖 numba（且版本锁定较严），在 Python 3.14+ 环境里可能没有可用的 numba 发行版或出现版本不匹配。兼容方案：

```bash
pip install pandas-ta --no-deps

# 如缺少依赖，再手动补齐
pip install numpy pandas tqdm
```

测试会自动启用 numba stub（无 JIT，仅用于对比）。

**pandas-ta-kw（可选补齐 tdfi/wae/ssl 对比）**

仓库已内置 `vendor/pandas-ta-kw`（git submodule，自动检测）。首次拉取后执行：

```bash
git submodule update --init --recursive
```

如需更新可用源码路径覆盖：

```bash
git clone https://github.com/kwannz/pandas-ta-kw.git /tmp/pandas-ta-kw
export PANDAS_TA_KW_PATH=/tmp/pandas-ta-kw
```

如需加载自定义指标目录（例如自定义实现 tdfi/wae/ssl），设置：

```bash
export PANDAS_TA_KW_CUSTOM_DIR=/path/to/custom-indicators
```

自定义目录需符合 pandas_ta_classic 的分类结构（参考 `pandas_ta_classic/custom.py`）。

仓库内置 `tests/pandas_ta_kw_custom`（tdfi/wae/ssl）会在检测到 pandas-ta-kw 时自动加载。

### 2. 编译 Rust 库

```bash
cd rust
maturin develop --release
```

### 3. 运行精度验证

```bash
# 返回项目根目录
cd ..

# 运行精度验证
python tests/run_precision_tests.py
```

## 📊 精度验证指标

### 计算指标

| 指标 | 说明 | 公式 |
|------|------|------|
| **MAE** | 平均绝对误差 | `mean(\|haze - ref\|)` |
| **RMSE** | 均方根误差 | `sqrt(mean((haze - ref)²))` |
| **Max Error** | 最大误差 | `max(\|haze - ref\|)` |
| **Correlation** | 皮尔逊相关系数 | `corrcoef(haze, ref)` |
| **Pass Rate** | 通过率 | `count(error < 1e-9) / total` |

### 验证标准

- ✅ **通过**：Max Error < 1e-9 且 Correlation > 0.9999
- ⚠️  **警告**：Max Error < 1e-6 且 Correlation > 0.999
- ❌ **失败**：Max Error >= 1e-6 或 Correlation < 0.999

## 📝 验证清单

### 波动率指标（10 个）
- [x] ATR - Average True Range ✅
- [x] NATR - Normalized ATR ✅
- [x] Bollinger Bands ✅
- [x] Keltner Channel ✅
- [x] Donchian Channel ✅
- [x] Chandelier Exit ✅
- [x] Historical Volatility ✅
- [x] Ulcer Index ✅
- [ ] Mass Index
- [x] True Range ✅

### 动量指标（17 个）
- [x] RSI - Relative Strength Index ✅
- [x] MACD - Moving Average Convergence Divergence ✅
- [x] CCI - Commodity Channel Index ✅
- [x] MFI - Money Flow Index ✅
- [x] Williams %R ✅
- [x] ROC - Rate of Change ✅
- [x] MOM - Momentum ✅
- [x] Fisher Transform ✅
- [x] Stochastic ✅
- [x] Stochastic RSI ✅
- [x] KDJ ✅
- [x] TSI - True Strength Index ✅
- [x] Ultimate Oscillator ✅
- [x] Awesome Oscillator ✅
- [x] APO ✅
- [x] PPO ✅
- [x] CMO ✅

### 移动平均线（16 个）
- [x] SMA - Simple Moving Average ✅
- [x] EMA - Exponential Moving Average ✅
- [x] WMA - Weighted Moving Average ✅
- [x] DEMA - Double EMA ✅
- [x] TEMA - Triple EMA ✅
- [x] T3 - Tillson T3 ✅
- [x] KAMA - Kaufman Adaptive MA ✅
- [x] HMA - Hull MA ✅
- [x] RMA - Wilder's MA ✅
- [x] ZLMA - Zero Lag MA ✅
- [x] FRAMA - Fractal Adaptive MA ✅
- [x] ALMA - Arnaud Legoux MA ✅
- [x] VIDYA - Variable Index Dynamic Average ✅
- [x] PWMA - Pascal's Weighted MA ✅
- [x] SINWMA - Sine Weighted MA ✅
- [x] SWMA - Symmetric Weighted MA ✅

### 趋势指标（14 个）
- [x] SuperTrend ✅
- [x] ADX - Average Directional Index ✅
- [x] Parabolic SAR ✅
- [x] Aroon ✅
- [x] DMI ✅
- [x] TRIX ✅
- [x] DPO - Detrended Price Oscillator ✅
- [x] Vortex ✅
- [x] Choppiness ✅
- [x] QStick ✅
- [x] VHF ✅
- [x] DX ✅
- [x] +DI ✅
- [x] -DI ✅

### 成交量指标（11 个）
- [x] OBV - On Balance Volume ✅
- [x] VWAP - Volume Weighted Average Price ✅
- [x] Force Index ✅
- [x] CMF - Chaikin Money Flow ✅
- [x] Volume Oscillator ✅
- [x] AD - Accumulation/Distribution ✅
- [x] PVT - Price Volume Trend ✅
- [x] NVI - Negative Volume Index ✅
- [x] PVI - Positive Volume Index ✅
- [x] EOM - Ease of Movement ✅
- [ ] ADOSC - Chaikin A/D Oscillator

### 谐波形态指标（3 个）✅ 已完成
- [x] py_harmonics - 时间序列信号输出
- [x] py_harmonics_patterns - 详细形态对象
- [x] py_harmonics_prz - PRZ 计算

**测试覆盖**（23 个测试用例）：
- 基础功能测试：信号格式、PRZ 计算、概率范围
- 边界条件测试：空数据、单点数据、短数据
- 形态检测测试：9 种谐波形态识别
- 形成中形态测试：XABC 阶段检测
- 特殊情况测试：常数价格、极端波动

## 🐛 调试指南

### 常见问题

**Q: `ImportError: No module named 'haze_library'` 或 `_haze_rust`**

A: 请先编译 Rust 库：
```bash
cd rust
maturin develop --release
```

**Q: `ModuleNotFoundError: No module named 'talib'`**

A: 需要先安装 TA-Lib 系统库：
```bash
brew install ta-lib
pip install TA-Lib
```

**Q: 精度验证失败**

A: 检查以下几点：
1. 参数是否一致（period, multiplier 等）
2. NaN 处理是否正确（前导 NaN 应该被忽略）
3. 算法实现是否有误（参考 IMPLEMENTED_INDICATORS.md）

## 📈 进度追踪

- [x] 精度验证框架搭建
- [x] 测试数据生成器
- [x] 波动率指标验证（90% 完成）✅
- [x] 动量指标验证（85% 完成）✅
- [x] 移动平均验证（85% 完成）✅
- [x] 趋势指标验证（80% 完成）✅
- [x] 成交量指标验证（75% 完成）
- [ ] 统计指标验证（60% 完成）
- [ ] pandas-ta 独有指标验证（25% 完成）
- [x] 谐波形态验证（100% 完成）✅
- [x] 单元测试用例编写（90% 完成 - 833 tests passing）✅
- [ ] 性能基准测试（30% 完成）

**总体测试覆盖率**: 90%+ (目标: 90%+ ✅)

## 📚 参考资源

- [TA-Lib 官方文档](https://ta-lib.org/)
- [pandas-ta GitHub](https://github.com/twopirllc/pandas-ta)
- [pytest 文档](https://docs.pytest.org/)
- [numpy 测试最佳实践](https://numpy.org/doc/stable/reference/testing.html)

## 🤝 贡献指南

欢迎贡献！请遵循以下步骤：

1. 添加新指标验证到 `run_precision_tests.py`
2. 确保精度验证通过（Max Error < 1e-9）
3. 编写相应的单元测试
4. 更新本文档的验证清单

---

**Last Updated**: 2025-12-28
**Maintainer**: Haze Team
**Test Coverage**: 90%+ (833 tests passing, target: 90%+)
