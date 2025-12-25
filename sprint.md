# Sprint 开发计划 - Haze-Library 重构（整合所有指标）

## 项目概述
**项目名称**：Haze-Library（独立量化交易指标库）  
**重构目标**：基于 TA-Lib (150+ 指标)、pandas-ta-kw (212 指标)和 pyharmonics (谐波模式检测，无预测能力) 的核心算法逻辑，整合复制所有指标到 Haze-Library，形成完全独立的库。避免直接复制代码，通过 Rust 重写计算路径，实现性能优化和统一接口。移除 ML 模块，确保确定性算法。最终产出可 pip 安装的 Python 包，支持 Python 3.14+。  
**用户价值**：提供高性能、统一 API 的本地指标库，支持 Binance 数据源，用于回测和实时交易。  
**当前状态**：基础结构就绪，参考库分析完成。  
**预计周期**：12-16 周，分 4 个 Sprint 阶段。  
**注意事项**：Python 包装使用 PyO3，确保无缝集成；Rust 支持所有数值计算和模式检测（包括谐波），但 pyharmonics 有预测能力。Rust 可通过 ndarray 和 rayon 支持向量化计算。

## 重构原则
- **KISS**：简单实现核心逻辑，避免复杂抽象。  
- **YAGNI**：仅整合现有指标，无额外预测。  
- **SOLID**：单一职责（每个指标模块独立）、开闭原则（抽象基类扩展）。  
- **奥卡姆剃刀**：最小依赖，仅必要组件。  
- **胶水开发**：参考算法逻辑，用 Rust 重写，不复制代码。

## 输入输出规范
- **输入**：pandas.DataFrame（OHLCV 列，datetime 索引）；参数字典。  
- **输出**：SignalResult（values: pd.Series/DataFrame, signals: pd.Series, metadata: dict）。  
- **数据结构**：SFGData（DataFrame 扩展）；Candle（Rust struct）。

## 模块划分与系统结构
```
haze-library/  
├── pyproject.toml          # maturin 配置  
├── Cargo.toml              # Rust 依赖  
├── src/                    # Python 源代码  
│   ├── __init__.py  
│   ├── core.py             # SFGData, utils  
│   ├── indicators/         # 所有指标模块（分类子目录）  
│   │   ├── ta_lib/         # TA-Lib 150+ 指标  
│   │   ├── pandas_ta/      # pandas-ta-kw 212 指标  
│   │   └── harmonics/      # pyharmonics 谐波检测  
│   └── data/  
│       └── binance.py      # 数据获取  
├── rust/                   # Rust 内核  
│   ├── src/  
│   │   ├── lib.rs          # PyO3 入口  
│   │   ├── calculations.rs # 所有计算函数  
│   │   └── types.rs        # 类型定义  
└── tests/                  # 测试  
    ├── unit/  
    └── integration/  
```
- **指标整合**：TA-Lib 指标（如 SMA、RSI）；pandas-ta-kw 扩展（如蜡烛图模式）；pyharmonics 谐波（XABCD 等检测，无预测）。  
- **数据流**：DF → Rust Vec<Candle> → 计算 → Python 结果。

## 实现步骤与开发规划
### Sprint 1: 环境准备与算法提取（Week 1-3）
- 提取参考算法：分析 TA-Lib C 代码、pandas-ta-kw Python 逻辑、pyharmonics 检测比例（无预测），记录公式（不复制代码）。  
- 配置 pyproject.toml/Cargo.toml：添加依赖，确保 Rust 支持（ndarray 向量化）。  
- 实现 core.py：SFGData、IndicatorConfig。  
- Rust 基础：types.rs、lib.rs 测试绑定。  
- 测试：pytest 配置，数据验证。  
- 里程碑：提取所有指标逻辑并分类。

### Sprint 2: Rust 内核重构（Week 4-8）
- 重写计算：calculations.rs 中实现 TA-Lib 150+（如 fn sma(...)）、pandas-ta-kw 212（蜡烛图 fn doji(...)）、pyharmonics 谐波（fn detect_gartley(...)）。使用 rayon 并行。  
- 类型转换：PyO3 处理输入/输出。  
- 性能优化：SIMD 基准（5-10x 目标）。  
- 测试：Rust 单元测试，数值对比参考库。  
- 里程碑：Rust 覆盖所有指标内核。

### Sprint 3: Python 接口与指标包装（Week 9-13）
- 逐类包装：indicators/ 子目录中实现 Python API（调用 Rust），统一参数/输出。  
- 谐波包装：harmonics/ 中实现检测（无预测）。  
- 数据模块：binance.py 实现获取。  
- 接口统一：df.ta_like() 扩展风格。  
- 测试：集成测试，边界案例。  
- 里程碑：所有指标实现并验证。

### Sprint 4: 打包、优化与文档（Week 14-16）
- 打包：maturin 生成 wheel。  
- 优化：性能分析，Rust 扩展。  
- 文档：sphinx API，README 指标列表。  
- 最终测试：覆盖率 >90%。  
- 里程碑：pip 安装测试，发布测试 PyPI。  

## 辅助说明与注意事项
- **潜在问题**：精度差异 → epsilon 检查；内存 → 分批。  
- **风险管理**：Sprint 结束回归测试。  
- **Rust 支持**：全支持数值/模式计算，Python 包装无缝。