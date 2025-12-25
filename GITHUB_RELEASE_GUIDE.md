# GitHub 发布指南 - Haze-Library v0.1.0

## 🎯 目标

将 Haze-Library 发布到 GitHub 公开仓库，使其可以通过 GitHub 访问并最终通过 pip 安装。

## ✅ 当前状态

- ✅ 代码已提交到本地 git 仓库
- ✅ 创建了 v0.1.0 标签
- ✅ 所有发布文档已准备完毕（README, CONTRIBUTING, CHANGELOG）
- ⏳ 待办：创建 GitHub 远程仓库并推送

## 📋 发布步骤

### Step 1: 在 GitHub 创建公开仓库

1. 访问 [GitHub](https://github.com/) 并登录
2. 点击右上角的 "+" 号，选择 "New repository"
3. 填写仓库信息：
   - **Repository name**: `haze-library`（或你喜欢的名字）
   - **Description**: `High-performance quantitative trading indicators library with Rust backend`
   - **Visibility**: ✅ **Public**（重要：必须选择公开）
   - **Initialize repository**:
     - ❌ **不要勾选** "Add a README file"
     - ❌ **不要勾选** "Add .gitignore"
     - ❌ **不要勾选** "Choose a license"
     （因为我们已经有这些文件了）
4. 点击 "Create repository"

### Step 2: 添加 GitHub 远程仓库

在你的终端中，进入项目目录并执行：

```bash
cd /Users/zhaoleon/Desktop/haze/haze-Library

# 添加 GitHub 远程仓库（替换 YOUR_USERNAME 为你的 GitHub 用户名）
git remote add origin https://github.com/YOUR_USERNAME/haze-library.git

# 验证 remote 配置
git remote -v
```

**输出示例**：
```
origin  https://github.com/YOUR_USERNAME/haze-library.git (fetch)
origin  https://github.com/YOUR_USERNAME/haze-library.git (push)
```

### Step 3: 推送代码到 GitHub

```bash
# 推送主分支
git push -u origin main

# 推送所有标签
git push origin --tags

# 或者一次性推送
git push -u origin main --tags
```

**预期输出**:
```
Enumerating objects: XX, done.
Counting objects: 100% (XX/XX), done.
...
To https://github.com/YOUR_USERNAME/haze-library.git
 * [new branch]      main -> main
 * [new tag]         v0.1.0 -> v0.1.0
Branch 'main' set up to track remote branch 'main' from 'origin'.
```

### Step 4: 在 GitHub 创建 Release

1. 访问你的 GitHub 仓库页面
2. 点击右侧的 "Releases" → "Create a new release"
3. 填写 Release 信息：
   - **Choose a tag**: 选择 `v0.1.0`
   - **Release title**: `v0.1.0: 212 Technical Analysis Indicators`
   - **Description**: 复制以下内容或自定义

```markdown
# 🎉 Haze-Library v0.1.0 - Initial Release

**High-performance quantitative trading indicators library with Rust backend**

## ✨ Highlights

- **212 Technical Indicators**: Complete coverage of TA-Lib, pandas-ta, and custom indicators
- **5-10x Performance**: Faster than pure Python implementations
- **High Precision**: < 1e-9 error tolerance vs reference libraries
- **Zero Dependencies**: All algorithms implemented from scratch in Rust

## 📊 Indicator Categories

- **Volatility (10)**: ATR, NATR, Bollinger Bands, Keltner Channel, etc.
- **Momentum (17)**: RSI, MACD, Stochastic, CCI, MFI, Williams %R, etc.
- **Trend (14)**: SuperTrend, ADX, Parabolic SAR, Aroon, DMI, etc.
- **Volume (11)**: OBV, VWAP, Force Index, CMF, AD, PVT, etc.
- **Moving Averages (16)**: SMA, EMA, WMA, DEMA, TEMA, T3, KAMA, ALMA, VIDYA, etc.
- **Candlestick Patterns (61)**: All TA-Lib patterns complete
- **Statistical (13)**: Linear Regression, Correlation, Z-Score, Beta, etc.
- **Math Operations (25)**: MAX, MIN, SQRT, LN, trigonometric functions, etc.
- **Cycle (5)**: Hilbert Transform indicators
- **pandas-ta Exclusive (25)**: Entropy, Aberration, Squeeze, QQE, etc.
- **Others (15)**: Fibonacci, Ichimoku, Pivots, Price Transform, etc.

## 📦 Installation

### From Source (Current)
```bash
git clone https://github.com/YOUR_USERNAME/haze-library.git
cd haze-library/rust
pip install maturin
maturin develop --release
```

### From PyPI (Coming Soon)
```bash
pip install haze-library
```

## 🚀 Quick Start

```python
import _haze_rust as haze

close_prices = [100.0, 101.0, 102.0, 101.5, 103.0, 102.5, 104.0]

# Moving Averages
sma = haze.py_sma(close_prices, period=3)
ema = haze.py_ema(close_prices, period=3)

# Momentum Indicators
rsi = haze.py_rsi(close_prices, period=3)

# Volatility Indicators
high = [101.0, 102.0, 103.0, 102.5, 104.0, 103.5, 105.0]
low = [99.0, 100.0, 101.0, 100.5, 102.0, 101.5, 103.0]
atr = haze.py_atr(high, low, close_prices, period=3)
```

## 📖 Documentation

- [Complete Indicator List](IMPLEMENTED_INDICATORS.md)
- [Contributing Guidelines](CONTRIBUTING.md)
- [Changelog](CHANGELOG.md)

## 🙏 Acknowledgments

- **TA-Lib**: Reference implementation for technical analysis
- **pandas-ta**: Inspiration for pandas integration patterns
- **PyO3**: Rust-Python bindings framework

## 📜 License

MIT License - See [LICENSE](LICENSE) for details.

---

**Made with ❤️ by the Haze Team**
```

4. ✅ 勾选 "Set as the latest release"
5. 点击 "Publish release"

### Step 5: 验证发布

1. 访问你的 GitHub 仓库主页
2. 验证以下内容：
   - ✅ README.md 正确显示
   - ✅ 代码目录结构完整
   - ✅ Release v0.1.0 可见
   - ✅ Tags 中包含 v0.1.0

### Step 6: 添加 GitHub Badges（可选）

编辑 README.md，将以下徽章中的 `YOUR_USERNAME` 替换为你的 GitHub 用户名：

```markdown
[![GitHub release](https://img.shields.io/github/v/release/YOUR_USERNAME/haze-library)](https://github.com/YOUR_USERNAME/haze-library/releases)
[![GitHub stars](https://img.shields.io/github/stars/YOUR_USERNAME/haze-library?style=social)](https://github.com/YOUR_USERNAME/haze-library)
[![GitHub forks](https://img.shields.io/github/forks/YOUR_USERNAME/haze-library?style=social)](https://github.com/YOUR_USERNAME/haze-library/fork)
```

## 🔄 后续工作：发布到 PyPI

完成 GitHub 发布后，下一步是发布到 PyPI，使项目可以通过 `pip install haze-library` 安装。

### PyPI 发布准备

1. **注册 PyPI 账号**:
   - 访问 [https://pypi.org/](https://pypi.org/)
   - 注册账号并验证邮箱

2. **安装发布工具**:
   ```bash
   pip install twine
   ```

3. **构建发布包**:
   ```bash
   cd rust
   maturin build --release
   ```

4. **上传到 PyPI**:
   ```bash
   # 首次上传到 TestPyPI（测试）
   twine upload --repository testpypi target/wheels/*

   # 验证无误后，上传到正式 PyPI
   twine upload target/wheels/*
   ```

5. **验证安装**:
   ```bash
   pip install haze-library
   python -c "import _haze_rust as haze; print(haze.py_sma([1,2,3,4,5], 3))"
   ```

## 📝 快速命令参考

### 推送代码到 GitHub（首次）
```bash
cd /Users/zhaoleon/Desktop/haze/haze-Library
git remote add origin https://github.com/YOUR_USERNAME/haze-library.git
git push -u origin main --tags
```

### 后续更新推送
```bash
git add .
git commit -m "feat: your feature description"
git push origin main
```

### 创建新版本标签
```bash
git tag -a v0.2.0 -m "Release v0.2.0: description"
git push origin v0.2.0
```

## ⚠️ 注意事项

1. **替换占位符**: 所有 `YOUR_USERNAME` 需要替换为你的实际 GitHub 用户名
2. **SSH vs HTTPS**: 如果配置了 SSH 密钥，可以使用 `git@github.com:YOUR_USERNAME/haze-library.git` 代替 HTTPS URL
3. **私有仓库**: 如果创建为私有仓库，需要配置访问令牌才能推送
4. **大文件警告**: 如果有超过 100MB 的文件，GitHub 会拒绝推送，需要使用 Git LFS

## 🆘 常见问题

### Q: 推送时提示 "Permission denied"
A: 确认你已经在 GitHub 网站上创建了仓库，并且用户名正确

### Q: 推送时提示 "failed to push some refs"
A: 可能 GitHub 仓库已有内容，尝试先 pull：
```bash
git pull origin main --allow-unrelated-histories
git push origin main --tags
```

### Q: 如何修改仓库名？
A: 在 GitHub 仓库设置中修改，然后更新本地 remote：
```bash
git remote set-url origin https://github.com/YOUR_USERNAME/NEW_NAME.git
```

---

**准备完毕！现在你可以按照上述步骤将 Haze-Library 发布到 GitHub 了。** 🚀
