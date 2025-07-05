# GitHub Actions 快速参考

## 🚀 工作流概览

| 工作流 | 触发条件 | 主要功能 | 状态徽章 |
|--------|----------|----------|----------|
| **CI/CD** (`ci.yml`) | Push, PR, Manual | 测试、检查、发布 | ![CI](https://github.com/your-username/pyutils/workflows/CI/badge.svg) |
| **版本管理** (`version-bump.yml`) | Manual | 自动版本更新 | ![Version Bump](https://github.com/your-username/pyutils/workflows/Version%20Bump/badge.svg) |
| **预发布** (`pre-release.yml`) | Pre-release tags, Manual | TestPyPI 发布 | ![Pre-release](https://github.com/your-username/pyutils/workflows/Pre-release/badge.svg) |
| **依赖更新** (`dependency-update.yml`) | Schedule, Manual | 自动依赖更新 | ![Dependencies](https://github.com/your-username/pyutils/workflows/Dependencies/badge.svg) |

## 📋 快速设置清单

### ✅ 仓库配置
- [ ] 启用 GitHub Actions
- [ ] 配置 PyPI Trusted Publishing
- [ ] 设置环境保护规则 (`production`)
- [ ] 配置分支保护规则 (`main`)
- [ ] 添加仓库密钥 (如果不使用 Trusted Publishing)

### ✅ 本地配置
- [ ] 复制 `.env.template` 到 `.env`
- [ ] 配置 PyPI API tokens
- [ ] 验证 `pyproject.toml` 配置
- [ ] 运行配置检查脚本

## 🔧 常用命令

### 本地开发
```powershell
# PowerShell 构建脚本
./make.ps1 test                  # 运行测试
./make.ps1 lint                  # 代码检查
./make.ps1 format                # 代码格式化
./make.ps1 ci                    # 运行所有 CI 检查（包含覆盖率）

# 或使用 Makefile (Linux/macOS)
make test                        # 运行测试
make lint                        # 代码检查
make format                      # 代码格式化
make ci                          # 运行所有 CI 检查

# GitHub Actions 配置
./scripts/setup-github-actions.ps1 -Check     # 检查配置
./scripts/setup-github-actions.ps1 -Setup     # 设置向导
./scripts/setup-github-actions.ps1 -Validate  # 验证语法
```

### 发布流程
```powershell
# 本地发布 (测试)
./scripts/publish.ps1 -TestPyPI

# 本地发布 (正式)
./scripts/publish.ps1 -PyPI

# GitHub Actions 发布
# 1. 手动触发版本更新
# 2. 推送标签自动发布
# 3. 创建 Release 自动发布
```

## 🎯 工作流详解

### 1. CI/CD 工作流 (`ci.yml`)

**触发条件:**
- `push` 到 `main` 分支
- `pull_request` 到 `main` 分支
- `release` 发布事件
- 手动触发 (`workflow_dispatch`)

**智能优化:**
- 文件变更检测 (跳过不相关的作业)
- 并发控制 (取消重复运行)
- 缓存优化 (uv 缓存)
- 矩阵测试 (多 Python 版本和操作系统)

**作业流程:**
```
changes → test → lint → docs → performance → publish → notify
```

### 2. 版本管理工作流 (`version-bump.yml`)

**功能:**
- 自动更新版本号 (`patch`, `minor`, `major`)
- 更新 `pyproject.toml` 和 `__init__.py`
- 创建 Git 标签
- 生成变更日志
- 创建 GitHub Release (可选)

**使用方法:**
1. 在 GitHub Actions 页面手动触发
2. 选择版本类型 (`patch`, `minor`, `major`)
3. 选择是否创建 Release

### 3. 预发布工作流 (`pre-release.yml`)

**触发条件:**
- 推送预发布标签 (`v*-alpha*`, `v*-beta*`, `v*-rc*`)
- 手动触发

**功能:**
- 发布到 TestPyPI
- 验证安装
- 创建 GitHub 预发布版本

### 4. 依赖更新工作流 (`dependency-update.yml`)

**触发条件:**
- 每周一自动运行
- 手动触发

**功能:**
- 检查过时依赖
- 自动更新依赖
- 运行测试验证
- 创建 Pull Request (可选)
- 安全审计

## 🔐 安全配置

### PyPI Trusted Publishing (推荐)

1. **在 PyPI 中配置:**
   - 项目设置 → Trusted Publishers
   - 添加 GitHub Actions publisher
   - 仓库: `your-username/pyutils`
   - 工作流: `ci.yml`
   - 环境: `production` (可选)

2. **在 GitHub 中配置:**
   - Settings → Environments → New environment: `production`
   - 添加保护规则 (需要审批、等待时间等)

### 传统 API Token 方式

如果不使用 Trusted Publishing，需要配置以下密钥:

```
TWINE_USERNAME=__token__
TWINE_PASSWORD=pypi-xxx...  # PyPI API Token
TWINE_USERNAME_TEST=__token__
TWINE_PASSWORD_TEST=pypi-xxx...  # TestPyPI API Token
```

## 📊 监控和维护

### 状态检查
- 工作流运行状态: GitHub Actions 页面
- 测试覆盖率: 作业输出或集成 Codecov
- 依赖安全: Dependabot 警报
- 包下载统计: PyPI 项目页面

### 定期维护
- [ ] 每月检查依赖更新
- [ ] 每季度审查工作流性能
- [ ] 及时处理安全警报
- [ ] 更新文档和配置

## 🐛 故障排除

### 常见问题

**1. 工作流权限错误**
```yaml
permissions:
  contents: read
  id-token: write  # Trusted Publishing 需要
```

**2. 版本号不匹配**
- 检查 `pyproject.toml` 和 `__init__.py` 中的版本
- 确保 Git 标签格式正确 (`v1.2.3`)

**3. PyPI 发布失败**
- 验证 Trusted Publishing 配置
- 检查包名是否已存在
- 确认版本号未重复

**4. 测试失败**
- 检查依赖兼容性
- 验证测试环境配置
- 查看详细错误日志

### 调试技巧

1. **启用调试日志:**
   ```yaml
   env:
     ACTIONS_STEP_DEBUG: true
   ```

2. **本地测试工作流:**
   ```bash
   # 使用 act 工具本地运行
   act -j test
   ```

3. **验证配置:**
   ```powershell
   ./scripts/setup-github-actions.ps1 -Validate
   ```

## 📚 相关资源

### 文档
- [GITHUB_ACTIONS_SETUP.md](./GITHUB_ACTIONS_SETUP.md) - 详细设置指南
- [PUBLISH_SCRIPT_FIX.md](./PUBLISH_SCRIPT_FIX.md) - 发布脚本修复记录
- [CODE_QUALITY_IMPROVEMENTS.md](./CODE_QUALITY_IMPROVEMENTS.md) - 代码质量改进建议

### 外部链接
- [GitHub Actions 文档](https://docs.github.com/en/actions)
- [PyPI Trusted Publishing](https://docs.pypi.org/trusted-publishers/)
- [Python 打包指南](https://packaging.python.org/)
- [uv 文档](https://docs.astral.sh/uv/)

### 工具
- [GitHub CLI](https://cli.github.com/) - 命令行工具
- [act](https://github.com/nektos/act) - 本地运行 Actions
- [actionlint](https://github.com/rhymond/actionlint) - 工作流语法检查

---

💡 **提示:** 使用 `./scripts/setup-github-actions.ps1 -Setup` 运行交互式设置向导获取个性化配置指导。