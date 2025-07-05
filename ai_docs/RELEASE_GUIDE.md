## Python包发布到PyPI完整指南

基于您的pyutils项目配置，以下是发布Python包到PyPI需要的完整操作步骤：

### 1. 注册PyPI账号

**主要步骤：**
- 访问 [PyPI官网](https://pypi.org) 注册账号
- 访问 [TestPyPI](https://test.pypi.org) 注册测试账号（推荐先在测试环境验证）
- 验证邮箱地址

### 2. 配置API Token（推荐方式）

**生成API Token：**
- 登录PyPI → Account settings → API tokens
- 创建新token，选择"Entire account"或特定项目
- 复制生成的token（格式：`pypi-xxx`）

**配置认证（推荐使用环境变量）：**

本项目使用环境变量进行认证配置，更安全且便于管理。

1. 编辑项目根目录下的 `.env` 文件：
```bash
# PyPI 认证配置
TWINE_USERNAME=mudssky

# TestPyPI 配置
TWINE_REPOSITORY_URL_TESTPYPI=https://test.pypi.org/legacy/
TWINE_USERNAME_TESTPYPI=mudssky
TWINE_PASSWORD_TESTPYPI=pypi-your_testpypi_token_here

# 正式 PyPI 配置
TWINE_REPOSITORY_URL_PYPI=https://upload.pypi.org/legacy/
TWINE_USERNAME_PYPI=mudssky
TWINE_PASSWORD_PYPI=pypi-your_pypi_token_here

# 默认配置（用于向后兼容）
TWINE_PASSWORD=pypi-your_default_token_here
```

2. 将实际的 API tokens 替换占位符
3. 确保 `.env` 文件不被提交到版本控制（已在 `.gitignore` 中配置）

详细配置说明请参考 [ENV_SETUP.md](ENV_SETUP.md) 文件。

### 3. 项目配置检查

您的项目配置已经很完善，但需要完善以下内容：

**更新 pyproject.toml：**
```toml
[project]
name = "mudssky-pyutils"  # 建议加上用户名避免冲突
version = "0.1.0"
description = "Python通用工具库 - 提供丰富的实用函数和工具类"
keywords = ["utils", "utilities", "tools", "helpers"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
]
```

### 4. 构建和发布流程

**使用uv进行发布（推荐）：**
```bash
# 1. 确保所有测试通过
uv run pytest tests/

# 2. 代码质量检查
uv run ruff check src/
uv run mypy src/

# 3. 构建包
uv build

# 4. 先发布到TestPyPI测试
uv publish --repository testpypi

# 5. 测试安装
pip install --index-url https://test.pypi.org/simple/ pyutils-mudssky

# 6. 确认无误后发布到正式PyPI
uv publish
```

**传统方式发布：**
```bash
# 1. 构建分发包
python -m build

# 2. 检查包
twine check dist/*

# 3. 上传到TestPyPI
twine upload --repository testpypi dist/*

# 4. 上传到PyPI
twine upload dist/*
```

### 5. 发布前检查清单

- [ ] 版本号已更新（`__init__.py` 和 `pyproject.toml`）
- [ ] README.rst 内容完整
- [ ] 所有测试通过
- [ ] 代码质量检查通过
- [ ] LICENSE 文件存在
- [ ] 依赖关系正确
- [ ] 包名在PyPI上可用

### 6. 版本管理建议

**语义化版本控制：**
- `0.1.0` → `0.1.1`（补丁版本）
- `0.1.0` → `0.2.0`（次要版本）
- `0.1.0` → `1.0.0`（主要版本）

**发布流程：**
```bash
# 更新版本号
# 编辑 src/pyutils/__init__.py 和 pyproject.toml

# 提交更改
git add .
git commit -m "Bump version to 0.1.1"
git tag v0.1.1
git push origin main --tags

# 构建和发布
uv build
uv publish
```

### 7. Windows 系统发布到 PyPI 配置指南

#### 环境准备

**安装必要工具：**
```powershell
# 使用 pip 安装发布工具
pip install build twine

# 或者使用 uv（推荐）
pip install uv
uv add --dev build twine
```

**项目提供的 Windows 脚本：**
- `build.ps1` - Windows PowerShell 构建脚本
- `publish.ps1` - Windows PowerShell 发布脚本
- `make.bat` - 批处理文件，提供类似 Makefile 的功能

#### Windows 发布流程

**使用 PowerShell 脚本（推荐）：**
```powershell
# 1. 仅构建包
.\build.ps1

# 2. 发布到 TestPyPI（测试）
.\publish.ps1 -TestOnly

# 3. 完整发布流程（TestPyPI + PyPI）
.\publish.ps1

# 4. 跳过测试直接发布
.\publish.ps1 -SkipTests

# 5. 强制发布（忽略错误）
.\publish.ps1 -Force
```

**使用批处理文件：**
```cmd
# 查看所有可用命令
make.bat help

# 清理构建文件
make.bat clean

# 构建包
make.bat build

# 运行测试
make.bat test

# 代码检查
make.bat lint

# 代码格式化
make.bat format

# 类型检查
make.bat type-check

# 发布到测试环境
make.bat publish-test

# 发布到正式环境
make.bat publish

# 设置开发环境
make.bat dev-setup

# 运行所有 CI 检查
make.bat ci
```

#### Windows 特定配置

**PowerShell 执行策略：**
```powershell
# 如果遇到执行策略限制，运行：
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**环境变量配置：**
```powershell
# 设置 PyPI 凭据（推荐使用 API Token）
$env:TWINE_USERNAME = "__token__"
$env:TWINE_PASSWORD = "pypi-你的API令牌"

# 永久设置
[Environment]::SetEnvironmentVariable("TWINE_USERNAME", "__token__", "User")
[Environment]::SetEnvironmentVariable("TWINE_PASSWORD", "pypi-你的API令牌", "User")
```

**解决 Makefile 兼容性问题：**

原始的 Makefile 在 Windows 上会失败，因为：
1. `find` 命令在 Windows 上行为不同
2. `rm` 命令在 Windows 上不存在

解决方案：
- 使用提供的 `make.bat` 替代 Makefile
- 或者安装 Git Bash / WSL 来运行 Unix 命令
- 使用 PowerShell 脚本进行构建和发布

### 8. 后续维护

- 定期更新依赖版本
- 监控PyPI下载统计
- 处理用户反馈和issue
- 维护文档和示例

您的项目配置已经很完善，主要需要注册PyPI账号并配置认证信息即可开始发布流程。建议先在TestPyPI上测试发布流程。