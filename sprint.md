### Haze-Library 功能增强 Sprint 计划（中文版）

本 Sprint 计划针对 Haze-Library 仓库（https://github.com/kwannz/haze）进行功能增强开发。该仓库是一个由 Rust 驱动的高性能量化交易技术指标库，目前实现 215 个指标（误差 < 1e-9），采用核心指标算法零外部依赖、基础设施依赖最小化策略，通过 PyO3 提供 Python 绑定，性能较纯 Python 实现提升 5-10 倍。计划采用敏捷开发模式，适用于小型团队（1-3 名开发者），以 2 周 Sprint 为周期，强调迭代交付、每日站会、中期评审和 Sprint 回顾。开发过程充分利用 AI 辅助工具（如 Claude 或 Codex）加速代码生成和原型设计，同时确保与项目“Rust 核心算法自研、依赖最小化”的定位一致。

#### Sprint 总览
- **Sprint 名称**：增强 Sprint 1 - 可用性与功能提升  
- **周期**：2 周（例如：2025 年 12 月 29 日 - 2026 年 1 月 11 日）  
- **团队角色**：  
  - 主开发者：负责 Rust/Python 核心实现。  
  - 测试/评审者：专注 CI/CD 与质量保障。  
  - AI 助手：利用 Claude/Codex 生成代码草稿（例如 Prompt：“使用 PyO3 生成支持 Polars 的 Rust 代码”）。  
- **Sprint 目标**：实现多框架适配、API 优化、测试/CI 增强、AI 自研指标集成以及实时流支持，将项目从当前状态提升至 v0.2.0，突出 Rust 驱动的自研特色。  
- **完成定义（DoD）**：代码合并至 main 分支；测试覆盖率 >100% 并全部通过；文档更新；基准测试完成；添加示例脚本；无破坏性变更（若有则添加废弃警告）。  
- **容量估算**：每位开发者每周 40-60 小时；优先处理高优先级任务。  
- **工具与环境**：  
  - IDE：VS Code + Rust Analyzer + PyO3 插件。  
  - AI 工具：Claude 用于结构化代码生成，Codex/GPT 用于快速片段。  
  - 版本控制：GitHub（每个功能独立分支，PR 评审）。  
  - 构建工具：Maturin（Rust-Python 绑定）。  
  - 测试工具：Cargo（Rust）、pytest（Python）、cargo-tarpaulin/pytest-cov（覆盖率）。  
- **风险与缓解**：  
  - 依赖膨胀（如 tch-rs）：通过 Cargo feature 设为可选依赖解决。  
  - 异步复杂度：借助 Claude 生成验证示例。  
  - 向后兼容性：添加废弃警告并进行集成测试。  
  - 时间超支：每日站会及时调整优先级。  

#### Sprint 待办事项（Backlog）
待办事项拆分为用户故事与具体任务，使用故事点（SP，1 SP ≈ 4 小时）估算，按优先级排序。每项标注 AI 工具使用方式。总估算努力：54 SP。

1. **用户故事：多框架适配（Pandas、Polars、NumPy、PyTorch）** – 高优先级（13 SP）  
   作为用户，我希望无缝集成多种数据框架，避免数据转换开销。  
   - 任务 1：调研并规划绑定方案（pyo3-polars、ndarray 等） – 2 SP。执行：使用 Claude 总结当前 rust/ 与 src/ 结构的集成指南。  
   - 任务 2：实现 Pandas/Polars DataFrame 访问器（例如 df.ta.sma()） – 4 SP。执行：利用 Codex 生成 src/haze/__init__.py 中的 Python 包装器，先覆盖 10+ 个指标。  
   - 任务 3：在 PyO3 中添加 NumPy ndarray 与 PyTorch tensor 支持（例如 &PyArray1<f64>） – 3 SP。执行：Prompt Claude：“在 momentum.rs 中生成基于 ndarray 的 RSI 计算代码，并通过 PyO3 导出。”  
   - 任务 4：使用样本数据测试集成（更新 tests/） – 2 SP。执行：利用 Codex 生成测试用例；运行性能基准。  
   - 任务 5：更新文档（README.md、IMPLEMENTED_INDICATORS.md）添加使用示例 – 2 SP。  
   依赖：基于现有 py_* 函数。AI 使用比例：约 60%。时间线：第 1 周（第 1-5 天）。

2. **用户故事：API 优化与错误处理** – 高优先级（8 SP）  
   作为开发者，我希望拥有更优雅、更健壮的 Pythonic API，减少使用错误。  
   - 任务 1：重命名函数（例如 sma() 替代 py_sma()），在 __init__.py 中隐藏底层实现 – 2 SP。执行：利用 Codex 编写自动化重命名脚本。  
   - 任务 2：为全部 215 个函数添加类型提示（typing）和异常处理（例如数据长度不足抛 ValueError） – 3 SP。执行：Prompt Claude：“为此 Rust-PyO3 函数添加类型提示和输入校验：py_rsi(prices: list[float], period: int)。”  
   - 任务 3：使用 Sphinx 优化文档（配置 conf.py，自动生成 API 文档） – 2 SP。执行：利用 Codex 从 docstring 生成 Sphinx 配置。  
   - 任务 4：测试向后兼容性（添加废弃警告） – 1 SP。  
   依赖：与多框架访问器保持一致。AI 使用比例：Claude 用于校验逻辑，Codex 用于文档生成。时间线：第 1 周（第 6-7 天）。

3. **用户故事：测试与 CI/CD 优化** – 中优先级（10 SP）  
   作为维护者，我希望拥有自动化测试和 CI，及早发现问题。  
   - 任务 1：配置 GitHub Actions 工作流（.github/workflows/），支持矩阵测试（多 Python/Rust 版本） – 3 SP。执行：Prompt Claude：“为 Cargo test 和 pytest 创建 GitHub Actions YAML，包含 maturin 构建。”  
   - 任务 2：集成覆盖率工具（Rust 用 cargo-tarpaulin，Python 用 pytest-cov） – 2 SP。执行：利用 Codex 添加覆盖率报告至 tests/。  
   - 任务 3：为自研指标添加模糊测试（cargo fuzz，例如针对 harmonics.rs） – 3 SP。执行：Prompt Claude：“为 py_harmonics 函数编写 cargo fuzz target。”  
   - 任务 4：扩展 tests/，增加与 TA-Lib 的精度基准对比 – 1 SP。  
   - 任务 5：更新 CHANGELOG.md 并在 README.md 添加徽章 – 1 SP。  
   依赖：基于优化后的 API。AI 使用比例：约 50%。时间线：第 1 周（第 8-10 天）。

4. **用户故事：集成机器学习/AI 自研指标** – 高优先级（12 SP）  
   作为量化研究员，我希望拥有 AI 增强指标，以实现预测能力并与传统库差异化。  
   - 任务 1：将 tch-rs 作为可选 Cargo feature 引入 – 2 SP。执行：利用 Codex 修改 Cargo.toml 支持 feature flag。  
   - 任务 2：在新 ai.rs 模块中开发新指标（例如基于 LSTM 的 AI-RSI） – 4 SP。执行：Prompt Claude：“使用 tch-rs 生成 Rust 代码实现 LSTM 预测 RSI，通过 PyO3 导出为 py_ai_rsi。”  
   - 任务 3：添加预训练模型（models/ 目录）并支持 fine-tuning – 3 SP。执行：利用 Codex 编写模型加载脚本。  
   - 任务 4：更新 INDICATOR_PLAN.md 和 tests/，新增 AI 类别（目标 20+ 个指标） – 2 SP。  
   - 任务 5：与 Python ML 库进行性能基准对比 – 1 SP。  
   依赖：与 tensor 输入结合。AI 使用比例：约 70%。时间线：第 2 周（第 1-5 天）。

5. **用户故事：添加实时数据流支持与事件驱动计算** – 中优先级（11 SP）  
   作为交易者，我希望支持流式指标计算，用于实时/HFT 场景。  
   - 任务 1：在 Rust 侧使用 tokio 实现异步流（Stream<Item=f64>） – 3 SP。执行：Prompt Claude：“在 ma.rs 中创建基于 tokio 的增量 SMA 计算。”  
   - 任务 2：通过 PyO3 暴露异步 API（例如 async def sma_stream()） – 3 SP。执行：利用 Codex 生成 Python 异步包装器。  
   - 任务 3：添加示例脚本（例如结合 ccxt/websocket 实时获取数据） – 2 SP。执行：Claude 生成完整 demo：“编写 Python 脚本，使用 haze 与 ccxt 实时计算 RSI。”  
   - 任务 4：开发自研流式指标（例如 py_harmonics_stream） – 2 SP。  
   - 任务 5：测试线程安全并更新文档 – 1 SP。  
   依赖：可与 AI 集成，支持 ML 流式处理。AI 使用比例：约 60%。时间线：第 2 周（第 6-10 天）。

#### 执行流程
1. **Sprint 规划会议**（第 0 天，1 小时）：评审待办事项、分配任务、创建分支（如 feature/multi-framework）。  
2. **每日站会**（每天 15 分钟）：汇报进度、障碍、AI 生成代码评审情况。  
3. **代码开发流程**：AI 生成草稿 → 人工精炼/测试 → 提交。  
4. **中期评审**（第 1 周末）：展示进度，必要时调整 backlog。  
5. **测试与集成**：使用 maturin 完整构建，确保核心算法自研与依赖最小化。  
6. **Sprint 回顾**（第 2 周末）：总结经验，提升 AI Prompt 质量。  
7. **发布准备**：更新 CHANGELOG.md，如条件成熟推送至 PyPI。

#### 跟踪与指标
- **燃尽图**：每日通过 GitHub Issues 或 Trello 跟踪。  
- **速度目标**：完成 50+ SP。  
- **质量目标**：测试覆盖率 >90%；无严重 bug；基准显示 5-10 倍性能提升。  
- **AI 效率**：记录节省时间（预计 20-30%）。

本计划确保开发高效聚焦，利用 AI 加速迭代，同时维护 Haze-Library 的 Rust 核心优势。如需根据最新仓库状态调整，可在后续 Sprint 中优化。
