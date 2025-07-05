# GitHub Actions 配置指南

## 📋 概述

本项目已配置了完整的 GitHub Actions CI/CD 流水线，包括：

- 🧪 多平台多版本测试
- 🔍 代码质量检查
- 📚 文档构建
- 🚀 自动发布到 PyPI
- 📊 性能基准测试

## 🛠️ 当前配置状态

### 已配置的工作流

**文件位置**: `.github/workflows/ci.yml`

**触发条件**:

- `push` 到 `main` 分支
- `pull_request` 到 `main` 分支
- `release` 发布时

**包含的作业**:

1. **test** - 多平台多版本测试
2. **lint** - 代码质量检查
3. **docs** - 文档构建
4. **performance** - 性能基准测试
5. **publish** - 自动发布到 PyPI

## 🔧 配置步骤

### 1. 仓库设置

#### 启用 GitHub Actions

1. 进入 GitHub 仓库页面
2. 点击 **Settings** 标签
3. 在左侧菜单中选择 **Actions** → **General**
4. 确保选择 **Allow all actions and reusable workflows**

#### 配置分支保护规则

1. 在 **Settings** → **Branches** 中
2. 为 `main` 分支添加保护规则：
   - ✅ Require status checks to pass before merging
   - ✅ Require branches to be up to date before merging
   - 选择必需的状态检查：
     - `test (ubuntu-latest, 3.11)`
     - `lint`
     - `docs`

#### 配置 GitHub Pages

1. 在 **Settings** → **Pages** 中
2. 配置 Pages 设置：
   - **Source**: Deploy from a branch
   - **Branch**: `gh-pages` 或选择 **GitHub Actions**
   - **Folder**: `/ (root)`
3. 如果选择 GitHub Actions 作为源：
   - ✅ 确保工作流有 `pages: write` 和 `id-token: write` 权限
   - ✅ 文档将自动部署到 `https://<username>.github.io/<repository>`
4. 可选配置：
   - 自定义域名（如果有）
   - 强制 HTTPS

### 2. 环境和密钥配置

#### 创建 PyPI 发布环境

1. 进入 **Settings** → **Environments**
2. 创建名为 `pypi` 的环境
3. 配置环境保护规则：
   - ✅ Required reviewers（可选）
   - ✅ Deployment branches: Selected branches
   - 添加 `main` 分支

#### 配置 PyPI Trusted Publishing

1. 登录 [PyPI](https://pypi.org/)
2. 进入项目管理页面
3. 在 **Publishing** 标签中添加 Trusted Publisher：
   - **Owner**: 你的 GitHub 用户名
   - **Repository name**: pyutils
   - **Workflow name**: ci.yml
   - **Environment name**: pypi

#### 配置 Codecov（可选）

1. 登录 [Codecov](https://codecov.io/)
2. 添加 GitHub 仓库
3. 获取 Upload Token
4. 在 GitHub 仓库的 **Settings** → **Secrets and variables** → **Actions** 中添加：
   - `CODECOV_TOKEN`: 你的 Codecov token

### 3. 版本管理配置

#### 语义化版本标签

确保使用语义化版本标签（如 `v1.0.0`）来触发发布：

```bash
# 创建并推送标签
git tag v1.0.0
git push origin v1.0.0

# 或者在 GitHub 网页上创建 Release
```

#### 版本同步检查

确保以下文件中的版本号保持一致：

- `pyproject.toml`
- `src/pyutils/__init__.py`

## 🚀 增强配置

### 1. 自动版本管理工作流配置

**文件位置**: `.github/workflows/version-bump.yml`

**使用方法**:

1. 在 GitHub 仓库页面进入 **Actions** 标签
2. 选择 **Version Bump** 工作流
3. 点击 **Run workflow**
4. 选择版本类型（patch/minor/major）
5. 选择是否创建 GitHub Release

**自动化功能**:

- ✅ 自动计算新版本号
- ✅ 更新所有相关文件中的版本
- ✅ 运行测试验证
- ✅ 创建 Git 标签
- ✅ 生成更新日志
- ✅ 创建 GitHub Release（可选）

### 2. 预发布工作流配置

**文件位置**: `.github/workflows/pre-release.yml`

**触发方式**:

```bash
# 创建预发布标签
git tag v1.2.0-alpha.1
git push origin v1.2.0-alpha.1

# 或使用 GitHub 网页创建预发布
```

**支持的预发布格式**:

- `v*-alpha*` (如: v1.0.0-alpha.1)
- `v*-beta*` (如: v1.0.0-beta.1)
- `v*-rc*` (如: v1.0.0-rc.1)

**自动化功能**:

- ✅ 验证预发布版本格式
- ✅ 运行完整测试套件
- ✅ 发布到 TestPyPI
- ✅ 从 TestPyPI 安装测试
- ✅ 创建 GitHub 预发布

### 3. 依赖更新工作流配置

**文件位置**: `.github/workflows/dependency-update.yml`

**自动执行**: 每周一上午 9:00 UTC

**手动触发**:

1. 进入 **Actions** → **Dependency Update**
2. 点击 **Run workflow**
3. 选择更新策略（patch/minor/major/all）

**功能特性**:

- 🔍 检测过期的 Python 包和 GitHub Actions
- 🔒 安全漏洞扫描和报告
- 🧪 更新后自动测试验证
- 📝 创建详细的 Pull Request
- 📊 生成依赖更新报告

**配置 TestPyPI 环境**:

1. 在 **Settings** → **Environments** 中创建 `testpypi` 环境
2. 在 [TestPyPI](https://test.pypi.org/) 配置 Trusted Publishing：
   - **Repository**: pyutils
   - **Workflow**: pre-release.yml
   - **Environment**: testpypi

## 📊 工作流详解

### 1. CI/CD 主工作流 (`ci.yml`)

**触发条件**:

- `push` 到 `main` 或 `develop` 分支（忽略文档文件）
- 对 `main` 分支的 `pull_request`（忽略文档文件）
- `release` 事件（类型为 `published`）
- 手动触发 (`workflow_dispatch`)

**智能优化特性**:

- 🎯 **路径过滤**: 自动检测变更类型，跳过不必要的作业
- 🚀 **并发控制**: 自动取消重复的工作流运行
- 💾 **缓存优化**: uv 缓存加速依赖安装
- 🔄 **矩阵优化**: 减少不必要的测试组合

**作业流程**:

1. **changes**: 检测文件变更类型（Python代码、文档、工作流）
2. **test**: 多平台多版本测试（Ubuntu/Windows/macOS + Python 3.9-3.12）
3. **lint**: 代码质量检查（ruff、mypy、bandit安全扫描）
4. **docs**: 文档构建和链接检查
5. **performance**: 性能基准测试（PR时或手动触发）
6. **publish**: 发布到 PyPI（仅 release 事件）
7. **notify**: 工作流结果汇总通知

### 2. 自动版本管理工作流 (`version-bump.yml`)

**功能**: 自动化版本更新和发布流程

**触发方式**: 手动触发 (`workflow_dispatch`)

**输入参数**:

- `version_type`: 版本类型（patch/minor/major）
- `create_release`: 是否创建 GitHub Release

**工作流程**:

1. 计算新版本号
2. 更新 `pyproject.toml` 和 `__init__.py` 中的版本
3. 运行测试验证
4. 提交版本更新
5. 创建并推送 Git 标签
6. 生成更新日志
7. 创建 GitHub Release（可选）

### 3. 预发布工作流 (`pre-release.yml`)

**功能**: 预发布版本测试和发布到 TestPyPI

**触发条件**:

- 推送预发布标签（`v*-alpha*`, `v*-beta*`, `v*-rc*`）
- 手动触发指定预发布标签

**工作流程**:

1. **validate**: 验证预发布版本格式
2. **test**: 运行完整测试套件
3. **build**: 构建包并验证
4. **publish-testpypi**: 发布到 TestPyPI
5. **test-installation**: 从 TestPyPI 安装测试
6. **create-prerelease**: 创建 GitHub 预发布
7. **notify**: 结果通知

### 4. 依赖更新工作流 (`dependency-update.yml`)

**功能**: 自动化依赖管理和安全审计

**触发条件**:

- 定时执行（每周一上午 9:00 UTC）
- 手动触发

**功能特性**:

- 🔍 **依赖检查**: 检测过期的 Python 包和 GitHub Actions
- 🔄 **智能更新**: 支持 patch/minor/major/all 更新策略
- 🧪 **自动测试**: 更新后自动运行测试验证
- 🔒 **安全审计**: 使用 safety 检查安全漏洞
- 📝 **自动 PR**: 创建包含详细更新报告的 Pull Request
- 📊 **报告生成**: 生成依赖更新和安全审计报告

## 🔄 发布流程

### 标准发布流程

#### 方式一：自动化版本管理（推荐）

1. **开发完成**

   ```bash
   # 确保代码质量
   ./scripts/dev.ps1 -All
   ```

2. **使用自动版本管理**
   - 在 GitHub Actions 中运行 **Version Bump** 工作流
   - 选择版本类型（patch/minor/major）
   - 选择创建 GitHub Release
   - 工作流自动完成版本更新、测试、标签创建和发布

#### 方式二：手动发布流程

1. **开发完成**

   ```bash
   # 确保代码质量
   ./scripts/dev.ps1 -All
   ```

2. **手动更新版本号**

   ```bash
   # 更新 pyproject.toml 和 __init__.py 中的版本
   # 提交版本更新
   git add .
   git commit -m "chore: bump version to v1.2.0"
   git push
   ```

3. **创建 Release**
   - 在 GitHub 网页上创建新的 Release
   - 使用语义化版本标签（如 `v1.2.0`）
   - 填写 Release Notes

4. **自动发布**
   - GitHub Actions 自动触发
   - 运行所有测试和检查
   - 自动发布到 PyPI

### 预发布流程

#### 方式一：使用预发布工作流（推荐）

1. **创建预发布标签**

   ```bash
   git tag v1.2.0-beta.1
   git push origin v1.2.0-beta.1
   ```

2. **自动预发布流程**
   - 预发布工作流自动触发
   - 运行完整测试套件
   - 发布到 TestPyPI
   - 从 TestPyPI 安装测试
   - 创建 GitHub 预发布

#### 方式二：手动触发预发布

1. **在 GitHub Actions 中手动触发**
   - 选择 **Pre-release** 工作流
   - 输入预发布标签名称
   - 工作流自动处理预发布流程

## 🛡️ 安全最佳实践

### 1. 权限最小化

- 使用 Trusted Publishing 而非 API Token
- 环境保护规则限制部署
- 只在必要时授予写权限

### 2. 密钥管理

- 使用 GitHub Secrets 存储敏感信息
- 定期轮换访问令牌
- 避免在日志中暴露敏感信息

### 3. 依赖安全

- 定期更新依赖
- 使用 Bandit 进行安全扫描
- 启用 Dependabot 安全更新

## 📈 监控和维护

### 工作流监控

- 📊 **状态监控**: 定期检查工作流运行状态和成功率
- 🔍 **失败分析**: 关注失败的构建并及时修复
- 📈 **覆盖率监控**: 监控测试覆盖率变化趋势
- 🚨 **通知设置**: 配置工作流失败时的通知机制

### 性能监控

- ⏱️ **构建时间**: 跟踪构建时间变化，识别性能瓶颈
- 🧪 **测试性能**: 监控测试执行时间，优化慢速测试用例
- 📊 **基准测试**: 定期运行性能基准测试，监控性能回归
- 💾 **缓存效率**: 监控缓存命中率，优化缓存策略

### 成本优化

- 🎯 **智能触发**: 使用路径过滤避免不必要的构建
- 🔄 **矩阵优化**: 合理配置测试矩阵，减少冗余组合
- 💾 **缓存策略**: 使用 uv 缓存和 GitHub Actions 缓存
- 🚀 **并发控制**: 自动取消重复的工作流运行
- ⚡ **快速失败**: 配置快速失败策略，节省计算资源

## 🚨 故障排除

### 常见问题

1. **发布失败**
   - ❌ **PyPI 发布失败**: 检查 Trusted Publishing 配置和环境名称
   - ❌ **版本冲突**: 确认版本号格式和是否已存在
   - ❌ **权限问题**: 验证环境保护规则和 OIDC 配置

2. **测试失败**
   - ❌ **依赖冲突**: 检查依赖版本兼容性和锁定文件
   - ❌ **环境问题**: 验证 Python 版本和操作系统兼容性
   - ❌ **测试超时**: 检查测试用例性能和超时设置

3. **工作流错误**
   - ❌ **权限不足**: 确认 GitHub Token 权限和仓库设置
   - ❌ **环境配置**: 检查环境保护规则和密钥配置
   - ❌ **并发冲突**: 验证并发控制组配置

4. **版本管理问题**
   - ❌ **版本不同步**: 确保所有文件中的版本号一致
   - ❌ **标签冲突**: 检查 Git 标签是否已存在
   - ❌ **更新日志**: 验证更新日志生成和格式

5. **依赖更新问题**
   - ❌ **更新失败**: 检查依赖兼容性和冲突
   - ❌ **安全漏洞**: 查看安全审计报告和修复建议
   - ❌ **PR 创建失败**: 验证 GitHub Token 权限和分支保护

### 调试技巧

1. **本地复现**

   ```bash
   # 使用相同的命令本地测试
   uv sync --dev
   uv run pytest --cov=src
   uv run ruff check .
   uv run mypy src
   ```

2. **详细日志分析**
   - 📋 在 GitHub Actions 页面查看完整日志
   - 🔍 使用 `set -x` 启用 Shell 详细输出
   - 📊 查看工作流运行时间和资源使用
   - 🚨 检查错误代码和退出状态

3. **本地工作流测试**

   ```bash
   # 使用 act 本地测试 GitHub Actions
   act -j test
   act -j lint
   act --list  # 查看所有可用作业
   ```

4. **环境调试**

   ```bash
   # 检查环境变量和配置
   uv --version
   python --version
   pip list

   # 验证包构建
   uv build
   twine check dist/*
   ```

5. **版本管理调试**

   ```bash
   # 检查版本一致性
   grep -r "version" pyproject.toml src/pyutils/__init__.py

   # 验证标签和提交
   git tag -l
   git log --oneline -10
   ```

6. **依赖问题调试**

   ```bash
   # 检查依赖冲突
   uv tree
   uv lock --resolution=highest

   # 安全审计
   uv run safety check
   ```

## 📚 相关文档

### 官方文档

- [GitHub Actions 官方文档](https://docs.github.com/en/actions)
- [PyPI Trusted Publishing](https://docs.pypi.org/trusted-publishers/)
- [uv 包管理器文档](https://docs.astral.sh/uv/)
- [Semantic Versioning](https://semver.org/)

### 项目文档

- [项目发布指南](./RELEASE_GUIDE.md)
- [开发环境设置](./DEVELOPMENT.md)
- [贡献指南](./CONTRIBUTING.md)
- [安全政策](./SECURITY.md)

### 工具文档

- [Ruff 代码检查](https://docs.astral.sh/ruff/)
- [MyPy 类型检查](https://mypy.readthedocs.io/)
- [pytest 测试框架](https://docs.pytest.org/)
- [Codecov 覆盖率](https://docs.codecov.com/)

### 最佳实践

- [GitHub Actions 最佳实践](https://docs.github.com/en/actions/learn-github-actions/security-hardening-for-github-actions)
- [Python 包发布最佳实践](https://packaging.python.org/en/latest/guides/publishing-package-distribution-releases-using-github-actions-ci-cd-workflows/)
- [CI/CD 安全指南](https://docs.github.com/en/actions/security-guides)

---

## 📋 配置检查清单

### 基础配置

- [ ] GitHub Actions 已启用
- [ ] 分支保护规则已配置
- [ ] PyPI Trusted Publishing 已设置
- [ ] 环境保护规则已配置

### 工作流文件

- [ ] `ci.yml` - 主 CI/CD 工作流
- [ ] `version-bump.yml` - 自动版本管理
- [ ] `pre-release.yml` - 预发布工作流
- [ ] `dependency-update.yml` - 依赖更新

### 可选配置

- [ ] Codecov 集成
- [ ] TestPyPI 环境
- [ ] 通知设置
- [ ] 性能监控

---

**配置状态**: ✅ 已完成
**工作流数量**: 4 个
**支持的 Python 版本**: 3.9-3.12
**支持的操作系统**: Ubuntu, Windows, macOS
**最后更新**: 2024-01-20
**维护者**: 项目团队
