# PyPI 发布指南 / PyPI Upload Guide

## 📋 发布前检查清单

✅ 包名可用：`haze-library` 在 PyPI 上未被占用
✅ 包验证通过：twine check 通过
✅ 许可证：CC BY-NC 4.0 (非商业)
✅ 版本：v0.1.0

## 📦 待上传文件

1. **源码分发包** (推荐 - 支持所有平台)
   - 文件：`haze_library-0.1.0.tar.gz` (94KB)
   - 说明：用户可在任何平台从源码构建

2. **二进制 wheel** (可选 - 仅限 macOS ARM64 + Python 3.14)
   - 文件：`haze_library-0.1.0-cp314-cp314-macosx_11_0_arm64.whl` (463KB)
   - 说明：macOS ARM64 用户可直接安装，无需编译

## 🔐 步骤 1: 注册 PyPI 账号

### 1.1 注册账号
访问：https://pypi.org/account/register/

填写信息：
- Username（用户名）
- Email（邮箱）
- Password（密码）

### 1.2 验证邮箱
检查邮箱并点击验证链接。

### 1.3 启用双因素认证（可选但推荐）
访问：https://pypi.org/manage/account/

## 🔑 步骤 2: 创建 API Token

### 2.1 生成 Token
1. 访问：https://pypi.org/manage/account/token/
2. 点击 "Add API token"
3. Token 名称：`haze-library-upload`
4. Scope（范围）：选择 "Entire account (all projects)" 或创建后改为 "Project: haze-library"
5. 点击 "Add token"

### 2.2 保存 Token
**重要**：Token 只显示一次！立即复制保存到安全位置。

格式：`pypi-AgEIcH...很长的字符串...`

## 📤 步骤 3: 配置上传凭证

### 方法 1: 使用 .pypirc 文件（推荐）

创建或编辑 `~/.pypirc` 文件：

```bash
cat > ~/.pypirc << 'EOF'
[distutils]
index-servers =
    pypi

[pypi]
username = __token__
password = pypi-AgEI...你的完整token...
EOF

chmod 600 ~/.pypirc  # 设置文件权限
```

### 方法 2: 命令行输入（每次上传都需输入）

上传时会提示输入：
- Username: `__token__`
- Password: `pypi-AgEI...你的token...`

## 🚀 步骤 4: 上传到 PyPI

### 4.1 先上传到 TestPyPI 测试（推荐）

TestPyPI 是 PyPI 的测试环境，可以安全测试发布流程。

```bash
# 注册 TestPyPI 账号：https://test.pypi.org/account/register/
# 创建 TestPyPI Token：https://test.pypi.org/manage/account/token/

# 上传到 TestPyPI
/Users/zhaoleon/Library/Python/3.9/bin/twine upload --repository testpypi \
  /Users/zhaoleon/Desktop/haze/haze/rust/target/wheels/haze_library-0.1.0.tar.gz \
  /Users/zhaoleon/Desktop/haze/haze/rust/target/wheels/haze_library-0.1.0-cp314-cp314-macosx_11_0_arm64.whl

# 测试安装（从 TestPyPI）
pip install --index-url https://test.pypi.org/simple/ haze-library
```

### 4.2 上传到正式 PyPI

**一旦上传，无法删除或覆盖相同版本！**

```bash
# 上传源码包和 wheel
/Users/zhaoleon/Library/Python/3.9/bin/twine upload \
  /Users/zhaoleon/Desktop/haze/haze/rust/target/wheels/haze_library-0.1.0.tar.gz \
  /Users/zhaoleon/Desktop/haze/haze/rust/target/wheels/haze_library-0.1.0-cp314-cp314-macosx_11_0_arm64.whl
```

**或者只上传源码包**（推荐 - 支持所有平台）：

```bash
/Users/zhaoleon/Library/Python/3.9/bin/twine upload \
  /Users/zhaoleon/Desktop/haze/haze/rust/target/wheels/haze_library-0.1.0.tar.gz
```

## ✅ 步骤 5: 验证发布

### 5.1 检查 PyPI 页面
访问：https://pypi.org/project/haze-library/

### 5.2 测试安装
```bash
# 创建测试环境
python3 -m venv test_env
source test_env/bin/activate

# 从 PyPI 安装
pip install haze-library

# 测试导入
python -c "import haze_library as haze; print(haze.py_sma([1,2,3,4,5], period=3))"

# 清理
deactivate
rm -rf test_env
```

## 📝 常见问题

### Q1: 上传失败 - "File already exists"
**原因**：PyPI 不允许覆盖已发布的版本。
**解决**：修改 `pyproject.toml` 中的版本号（如 0.1.1），重新构建并上传。

### Q2: 为什么只有 macOS ARM64 wheel？
**原因**：当前只在 macOS ARM64 上构建。
**解决**：源码包 (.tar.gz) 已包含，其他平台用户会自动从源码构建。
**改进**：使用 GitHub Actions CI/CD 自动构建多平台 wheel（见下文）。

### Q3: 如何构建多平台 wheel？
**推荐方案**：GitHub Actions + cibuildwheel

创建 `.github/workflows/wheels.yml`：

```yaml
name: Build Wheels

on:
  release:
    types: [published]
  workflow_dispatch:

jobs:
  build_wheels:
    name: Build wheels on ${{ matrix.os }}
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]

    steps:
      - uses: actions/checkout@v4

      - uses: PyO3/maturin-action@v1
        with:
          command: build
          args: --release --out dist

      - uses: actions/upload-artifact@v3
        with:
          name: wheels
          path: dist

  upload_pypi:
    needs: [build_wheels]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/download-artifact@v3
      - uses: PyO3/maturin-action@v1
        with:
          command: upload
          args: --skip-existing *
        env:
          MATURIN_PYPI_TOKEN: ${{ secrets.PYPI_API_TOKEN }}
```

### Q4: 源码包安装需要什么？
用户需要：
- Rust 编译器（`curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh`）
- maturin（`pip install maturin`）

安装时 pip 会自动调用 maturin 构建。

## 🎯 推荐发布流程

1. **首次发布（v0.1.0）**
   - 上传源码包 (.tar.gz) 到 PyPI
   - 上传 macOS ARM64 wheel（可选）
   - 大多数用户会从源码自动构建

2. **后续版本（v0.2.0+）**
   - 设置 GitHub Actions 自动构建多平台 wheel
   - 每次 release 自动上传到 PyPI
   - 覆盖 Windows、Linux、macOS（x64 + ARM64）
   - 支持 Python 3.9-3.13

## 📊 发布后统计

发布成功后，您可以在 PyPI 查看：
- 下载统计：https://pypistats.org/packages/haze-library
- 项目页面：https://pypi.org/project/haze-library/
- 发布历史：https://pypi.org/project/haze-library/#history

## 🔒 安全提示

1. ❗ **永远不要将 API Token 提交到 Git**
2. ❗ **使用 .pypirc 后设置权限 600**
3. ❗ **定期轮换 API Token**
4. ❗ **为每个项目使用独立的 scoped token**

## 📚 参考文档

- PyPI 官方文档：https://packaging.python.org/
- Twine 文档：https://twine.readthedocs.io/
- Maturin 文档：https://www.maturin.rs/
- PyO3 指南：https://pyo3.rs/

---

**准备好上传了吗？**

执行以下命令开始上传：

```bash
# 测试环境（推荐先测试）
/Users/zhaoleon/Library/Python/3.9/bin/twine upload --repository testpypi \
  /Users/zhaoleon/Desktop/haze/haze/rust/target/wheels/haze_library-0.1.0.tar.gz

# 正式发布
/Users/zhaoleon/Library/Python/3.9/bin/twine upload \
  /Users/zhaoleon/Desktop/haze/haze/rust/target/wheels/haze_library-0.1.0.tar.gz
```

🎉 祝发布成功！
