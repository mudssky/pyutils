# PyUtils

一个实用的Python工具库，提供常用的工具函数和类。

## 🚀 快速开始

### 安装

```bash
pip install mudssky-pyutils
```

### 使用

```python
from pyutils import some_function

# 使用工具函数
result = some_function()
```

## 📦 功能特性

- 🛠️ **实用工具**：提供常用的工具函数
- 📚 **完整文档**：详细的API文档和使用示例
- 🧪 **全面测试**：高测试覆盖率，确保代码质量
- 🔄 **持续集成**：自动化测试和发布流程
- 📈 **性能优化**：经过性能测试和优化

## 🛠️ 开发

### 环境设置

```bash
# 克隆仓库
git clone https://github.com/mudssky/pyutils.git
cd pyutils

# 安装依赖
make install
# 或
uv sync --dev

# 设置开发环境
make dev-setup
```

### 开发命令

```bash
# 查看所有可用命令
make help

# 运行测试
make test

# 代码质量检查
make lint
make type-check

# 格式化代码
make format

# 构建文档
make docs

# 运行所有CI检查
make ci
```

## 🚀 发布

本项目支持两种发布方式：**Semantic Release（推荐）** 和传统发布方式。

### 🎯 Semantic Release（推荐）

使用 [semantic-release](https://github.com/semantic-release/semantic-release) 进行完全自动化的版本管理和发布。

#### 特性

- ✅ **完全自动化**：基于commit消息自动确定版本号
- 📋 **自动生成Changelog**：从commit历史自动生成
- 🏷️ **自动创建Tag和Release**：GitHub自动发布
- 📦 **自动发布到PyPI**：无需手动操作
- 📚 **自动部署文档**：自动构建并部署到GitHub Pages
- 🔄 **CI/CD集成**：推送到main分支自动触发

#### 快速开始

```bash
# 查看发布命令帮助
make release-help

# 预览semantic-release发布
make semantic-release-dry

# 执行semantic-release发布
make semantic-release
```

#### Commit规范

项目使用 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

```bash
# 新功能 (minor版本)
feat: add new utility function
feat(auth): add OAuth2 support

# Bug修复 (patch版本)
fix: handle null response
fix(api): resolve timeout issue

# 重大更改 (major版本)
feat!: remove deprecated API
fix!: change function signature

# 其他类型 (不影响版本)
docs: update README
style: fix formatting
refactor: improve code structure
test: add unit tests
chore: update dependencies
```

#### 自动化流程

1. **提交代码**：使用规范的commit消息
2. **推送到main**：触发GitHub Actions
3. **代码检查**：运行linting和测试
4. **构建文档**：使用Sphinx生成HTML文档
5. **自动分析**：semantic-release分析commit确定版本
6. **自动发布**：更新版本、生成changelog、创建tag、发布到PyPI
7. **部署文档**：自动部署到GitHub Pages

### 🔧 传统发布方式

如果需要手动控制版本号，可以使用传统发布方式：

```bash
# 预览发布（不实际执行）
make release-dry

# 发布补丁版本 (1.0.0 -> 1.0.1)
make release-patch

# 发布次版本 (1.0.0 -> 1.1.0)
make release-minor

# 发布主版本 (1.0.0 -> 2.0.0)
make release-major

# 发布指定版本
make release-version VERSION=1.2.3
```

### 发布工具特性

- ✅ **自动版本管理**：智能递增版本号
- 📋 **自动生成Changelog**：从git commit历史提取
- 🏷️ **自动创建Tag**：创建带有详细信息的git tag
- 🚀 **自动触发CI/CD**：推送tag自动触发发布流程
- 📦 **自动发布到PyPI**：通过GitHub Actions自动发布
- 📝 **自动创建GitHub Release**：包含changelog和构建产物

### Changelog生成

```bash
# 生成changelog
make changelog

# 生成完整changelog文件
make changelog-file

# 使用脚本生成
python scripts/generate-changelog.py --all --output CHANGELOG.md
```

### 发布流程

1. **Tag触发发布**：推送tag时自动触发完整发布流程
2. **自动化脚本**：使用 `scripts/create-release.py` 进行版本管理
3. **GitHub Actions**：`.github/workflows/tag-release.yml` 处理CI/CD
4. **PyPI发布**：通过trusted publishing自动发布

### Commit规范

项目使用[Conventional Commits](https://www.conventionalcommits.org/)规范：

```bash
# 新功能
git commit -m "feat(auth): add OAuth2 support"

# Bug修复
git commit -m "fix(api): handle null response"

# 文档更新
git commit -m "docs: update installation guide"

# 重大更改
git commit -m "feat!: remove deprecated API"
```

## 📚 文档

- [发布指南](docs/RELEASE.md) - 详细的发布流程和工具说明
- [发布示例](examples/release-example.md) - 实际使用示例
- [API文档](https://mudssky.github.io/pyutils/) - 完整的API参考（自动部署）
- [Semantic Release指南](docs/SEMANTIC_RELEASE.md) - 自动化发布配置和使用
- [迁移指南](docs/MIGRATION_GUIDE.md) - 从传统发布迁移到semantic-release
- [GitHub Pages设置](docs/GITHUB_PAGES_SETUP.md) - 文档自动部署配置
- [贡献指南](CONTRIBUTING.md) - 如何参与项目开发

## 🔧 项目结构

```
pyutils/
├── src/pyutils/          # 源代码
├── tests/                # 测试文件
├── docs/                 # 文档
├── scripts/              # 发布和工具脚本
│   ├── create-release.py # 自动化发布脚本
│   └── generate-changelog.py # Changelog生成器
├── .github/workflows/    # GitHub Actions
│   ├── ci.yml           # 主CI流程
│   └── tag-release.yml  # Tag触发的发布流程
├── examples/             # 使用示例
├── Makefile             # 开发命令
└── pyproject.toml       # 项目配置
```

## 🤝 贡献

欢迎贡献代码！请遵循以下步骤：

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'feat: add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

### 开发工作流

```bash
# 1. 设置开发环境
make dev-setup

# 2. 开发功能
# ... 编写代码 ...

# 3. 运行检查
make ci

# 4. 提交代码
git add .
git commit -m "feat: add new feature"

# 5. 推送并创建PR
git push origin feature-branch
```

## 📊 项目状态

[![CI](https://github.com/mudssky/pyutils/actions/workflows/ci.yml/badge.svg)](https://github.com/mudssky/pyutils/actions/workflows/ci.yml)
[![PyPI version](https://badge.fury.io/py/mudssky-pyutils.svg)](https://badge.fury.io/py/mudssky-pyutils)
[![Python versions](https://img.shields.io/pypi/pyversions/mudssky-pyutils.svg)](https://pypi.org/project/mudssky-pyutils/)
[![License](https://img.shields.io/github/license/mudssky/pyutils.svg)](https://github.com/mudssky/pyutils/blob/main/LICENSE)

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🔗 相关链接

- [PyPI包](https://pypi.org/project/mudssky-pyutils/)
- [GitHub仓库](https://github.com/mudssky/pyutils)
- [文档网站](https://mudssky.github.io/pyutils/)
- [问题反馈](https://github.com/mudssky/pyutils/issues)
- [更新日志](CHANGELOG.md)

## 💡 使用技巧

### 监控发布状态

```bash
# 查看CI/CD状态
make ci-status

# 查看最新日志
make ci-logs

# 查看版本信息
make version

# 查看所有tags
make tags
```

### 快速发布流程

```bash
# 完整的发布检查和发布
make ci && make release-patch

# 或使用组合命令
make quick-check  # lint + test
make quick-release  # test + patch release
```

---

**注意**：本项目使用自动化发布流程，推送tag会自动触发PyPI发布。请确保在发布前进行充分测试。
