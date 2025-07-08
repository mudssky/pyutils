# Semantic Release 配置指南

本文档详细说明了项目中 semantic-release 的配置和使用方法。

## 📋 目录

- [概述](#概述)
- [配置文件](#配置文件)
- [工作流程](#工作流程)
- [Commit规范](#commit规范)
- [版本策略](#版本策略)
- [CI/CD集成](#cicd集成)
- [故障排除](#故障排除)

## 概述

[semantic-release](https://github.com/semantic-release/semantic-release) 是一个完全自动化的版本管理和包发布工具。它通过分析提交消息来确定下一个版本号，生成发布说明，并发布包。

### 主要优势

- 🤖 **完全自动化**：无需手动管理版本号
- 📊 **一致性**：基于约定的提交消息格式
- 🔄 **可重复**：每次发布都遵循相同的流程
- 📝 **文档化**：自动生成changelog和发布说明
- 🚀 **CI/CD友好**：与现代CI/CD工具完美集成

## 配置文件

### .releaserc.json

项目的主要配置文件：

```json
{
  "branches": [
    "main",
    "master",
    {
      "name": "develop",
      "prerelease": "beta"
    }
  ],
  "plugins": [
    "@semantic-release/commit-analyzer",
    "@semantic-release/release-notes-generator",
    [
      "@semantic-release/changelog",
      {
        "changelogFile": "CHANGELOG.md"
      }
    ],
    [
      "@semantic-release/exec",
      {
        "prepareCmd": "python scripts/update-version.py ${nextRelease.version}",
        "publishCmd": "python -m build && python -m twine upload dist/*"
      }
    ],
    [
      "@semantic-release/git",
      {
        "assets": [
          "CHANGELOG.md",
          "pyproject.toml",
          "src/pyutils/__init__.py"
        ],
        "message": "chore(release): ${nextRelease.version} [skip ci]\n\n${nextRelease.notes}"
      }
    ],
    "@semantic-release/github"
  ]
}
```

### package.json

定义 semantic-release 依赖：

```json
{
  "devDependencies": {
    "semantic-release": "^22.0.0",
    "@semantic-release/changelog": "^6.0.0",
    "@semantic-release/exec": "^6.0.0",
    "@semantic-release/git": "^10.0.0",
    "@semantic-release/github": "^9.0.0"
  }
}
```

## 工作流程

### 发布流程

1. **分析提交**：分析自上次发布以来的所有提交
2. **确定版本**：根据提交类型确定下一个版本号
3. **生成说明**：创建发布说明和changelog
4. **更新文件**：更新版本号相关文件
5. **构建包**：构建Python包
6. **发布包**：发布到PyPI
7. **创建标签**：创建Git标签
8. **GitHub发布**：创建GitHub Release
9. **提交更改**：提交changelog等文件更改

### 插件说明

- **commit-analyzer**：分析提交消息确定发布类型
- **release-notes-generator**：生成发布说明
- **changelog**：维护CHANGELOG.md文件
- **exec**：执行自定义命令（更新版本号、构建、发布）
- **git**：提交文件更改
- **github**：创建GitHub Release

## Commit规范

项目使用 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

### 基本格式

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### 提交类型

| 类型 | 描述 | 版本影响 |
|------|------|----------|
| `feat` | 新功能 | minor |
| `fix` | Bug修复 | patch |
| `docs` | 文档更新 | 无 |
| `style` | 代码格式 | 无 |
| `refactor` | 重构 | 无 |
| `test` | 测试相关 | 无 |
| `chore` | 构建/工具 | 无 |
| `perf` | 性能优化 | patch |
| `ci` | CI配置 | 无 |

### 重大更改

使用 `!` 或 `BREAKING CHANGE:` 表示重大更改（major版本）：

```bash
feat!: remove deprecated API
# 或
feat: add new feature

BREAKING CHANGE: remove support for Node 12
```

### 示例

```bash
# 新功能
feat(auth): add OAuth2 authentication support

# Bug修复
fix(api): handle timeout errors properly

# 文档更新
docs: update installation guide

# 重大更改
feat!: change API response format

# 带作用域的提交
fix(parser): resolve parsing issue with special characters
```

## 版本策略

### 语义化版本

项目遵循 [Semantic Versioning](https://semver.org/) 规范：

- **MAJOR** (x.0.0)：不兼容的API更改
- **MINOR** (0.x.0)：向后兼容的新功能
- **PATCH** (0.0.x)：向后兼容的Bug修复

### 分支策略

- **main/master**：生产发布分支
- **develop**：预发布分支（beta版本）

### 预发布版本

从 `develop` 分支发布的版本会带有 `beta` 标识：

```
1.2.0-beta.1
1.2.0-beta.2
```

## CI/CD集成

### GitHub Actions

`.github/workflows/release.yml` 配置了完整的发布流程：

```yaml
name: Release
on:
  push:
    branches: [main, master]
  workflow_dispatch:

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - name: Install dependencies
        run: npm install -g semantic-release @semantic-release/...
      - name: Release
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          PYPI_TOKEN: ${{ secrets.PYPI_API_TOKEN }}
        run: npx semantic-release
```

### 环境变量

需要配置以下环境变量：

- `GITHUB_TOKEN`：GitHub访问令牌（自动提供）
- `PYPI_API_TOKEN`：PyPI API令牌（需要手动配置）

## 故障排除

### 常见问题

#### 1. 没有新版本发布

**原因**：没有符合条件的提交

**解决**：确保提交消息符合约定格式，包含 `feat:` 或 `fix:` 等类型

#### 2. PyPI发布失败

**原因**：认证问题或包名冲突

**解决**：
- 检查 `PYPI_API_TOKEN` 是否正确配置
- 确认包名在PyPI上可用
- 检查包版本是否已存在

#### 3. Git推送失败

**原因**：权限不足或分支保护

**解决**：
- 确保GitHub Actions有写权限
- 检查分支保护规则
- 使用 `persist-credentials: false` 配置

#### 4. 版本号更新失败

**原因**：`update-version.py` 脚本问题

**解决**：
- 检查脚本路径和权限
- 验证文件格式和正则表达式
- 查看脚本执行日志

### 调试技巧

#### 1. 干运行模式

```bash
# 本地测试
make semantic-release-dry

# 或直接使用npx
npx semantic-release --dry-run
```

#### 2. 详细日志

```bash
# 启用调试日志
DEBUG=semantic-release:* npx semantic-release --dry-run
```

#### 3. 检查配置

```bash
# 验证配置文件
npx semantic-release --dry-run --debug
```

### 最佳实践

1. **提交前检查**：使用 `make semantic-release-dry` 预览
2. **规范提交**：始终使用约定的提交格式
3. **测试充分**：确保CI测试通过后再合并
4. **监控发布**：关注GitHub Actions执行状态
5. **文档更新**：及时更新相关文档

## 参考资源

- [semantic-release官方文档](https://semantic-release.gitbook.io/semantic-release/)
- [Conventional Commits规范](https://www.conventionalcommits.org/)
- [Semantic Versioning规范](https://semver.org/)
- [GitHub Actions文档](https://docs.github.com/en/actions)
