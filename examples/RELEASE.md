# 发布指南

本文档介绍了项目的多种发布方法和自动化工具。

## 🚀 发布方法概览

### 1. 手动创建 GitHub Release（当前方法）

```bash
# 创建并推送tag
git tag v1.0.0
git push origin v1.0.0

# 在GitHub上手动创建release
# 或使用gh CLI
gh release create v1.0.0 --title "Release 1.0.0" --notes "Release notes..."
```

### 2. 自动化Tag发布（推荐）

使用 `.github/workflows/tag-release.yml` workflow，当推送tag时自动触发：

```bash
# 使用我们的发布脚本（推荐）
python scripts/create-release.py --patch --push

# 或手动创建tag
git tag v1.0.0
git push origin v1.0.0
```

### 3. PR合并时自动发布

可以配置在PR合并到main分支时自动创建tag并发布（需要额外配置）。

## 🛠️ 发布工具

### 1. 自动化发布脚本 (`scripts/create-release.py`)

这是最推荐的发布方法，提供完整的版本管理和发布流程：

#### 基本用法

```bash
# 自动递增补丁版本 (1.0.0 -> 1.0.1)
python scripts/create-release.py --patch

# 自动递增次版本 (1.0.0 -> 1.1.0)
python scripts/create-release.py --minor

# 自动递增主版本 (1.0.0 -> 2.0.0)
python scripts/create-release.py --major

# 指定具体版本
python scripts/create-release.py --version 1.2.3
```

#### 高级选项

```bash
# 预览模式（不实际执行）
python scripts/create-release.py --patch --dry-run

# 创建tag并立即推送（触发CI/CD）
python scripts/create-release.py --patch --push

# 跳过git状态检查
python scripts/create-release.py --patch --skip-checks
```

#### 脚本功能

- ✅ 自动检查git状态和分支
- ✅ 智能版本号递增
- ✅ 更新所有版本文件（`pyproject.toml`, `__init__.py`）
- ✅ 从git commit历史自动生成changelog
- ✅ 创建带有详细信息的git tag
- ✅ 可选择立即推送触发CI/CD

### 2. Changelog生成器 (`scripts/generate-changelog.py`)

独立的changelog生成工具，支持多种格式和选项：

#### 基本用法

```bash
# 生成自上次tag以来的changelog
python scripts/generate-changelog.py

# 从指定tag生成changelog
python scripts/generate-changelog.py --from v1.0.0

# 生成完整的项目changelog
python scripts/generate-changelog.py --all

# 输出到文件
python scripts/generate-changelog.py --all --output CHANGELOG.md
```

#### 高级选项

```bash
# 不包含commit hash
python scripts/generate-changelog.py --no-hash

# 包含作者信息
python scripts/generate-changelog.py --include-author

# 为特定版本生成changelog
python scripts/generate-changelog.py --version 1.2.0
```

#### Changelog特性

- 📋 **智能分类**：自动识别commit类型（feat, fix, docs等）
- 🎯 **Conventional Commits**：支持标准的commit格式
- 🔗 **GitHub集成**：自动生成commit和比较链接
- 📊 **统计信息**：显示commit数量和变更统计
- 🎨 **美观格式**：使用emoji和清晰的分类

## 🔄 CI/CD工作流

### Tag Release Workflow (`.github/workflows/tag-release.yml`)

当推送tag时自动触发的完整发布流程：

#### 触发条件
- 推送 `v*.*.*` 格式的tag
- 支持预发布版本（如 `v1.0.0-beta.1`）

#### 执行步骤
1. **代码检出**：获取完整的git历史
2. **环境设置**：安装Python和依赖
3. **质量检查**：运行测试和代码检查
4. **版本更新**：从tag提取版本并更新文件
5. **Changelog生成**：自动从commit历史生成发布说明
6. **包构建**：构建wheel和源码包
7. **GitHub Release**：创建GitHub release并上传文件
8. **PyPI发布**：自动发布到PyPI
9. **通知**：生成发布摘要

#### 环境要求
- 需要配置PyPI的trusted publishing
- 需要适当的GitHub权限

## 📝 Commit规范

为了更好地生成changelog，建议使用Conventional Commits格式：

### 基本格式
```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### 常用类型
- `feat`: 新功能
- `fix`: Bug修复
- `docs`: 文档更新
- `style`: 代码格式（不影响功能）
- `refactor`: 代码重构
- `perf`: 性能优化
- `test`: 测试相关
- `build`: 构建系统
- `ci`: CI/CD配置
- `chore`: 其他维护任务

### 示例
```bash
git commit -m "feat(auth): add OAuth2 authentication"
git commit -m "fix(api): handle null response in user endpoint"
git commit -m "docs: update installation instructions"
git commit -m "chore: bump version to 1.2.0"
```

### Breaking Changes
```bash
git commit -m "feat!: remove deprecated API endpoints"
# 或
git commit -m "feat: add new API\n\nBREAKING CHANGE: old API endpoints removed"
```

## 🎯 推荐工作流程

### 日常开发
1. 在feature分支开发
2. 使用规范的commit消息
3. 创建PR到main分支
4. 代码审查和测试通过后合并

### 发布流程
1. 确保main分支是最新的
2. 运行发布脚本：
   ```bash
   python scripts/create-release.py --patch --push
   ```
3. 脚本会自动：
   - 更新版本号
   - 生成changelog
   - 创建并推送tag
   - 触发CI/CD发布流程

### 紧急修复
1. 从main分支创建hotfix分支
2. 修复问题并测试
3. 合并到main分支
4. 立即发布patch版本：
   ```bash
   python scripts/create-release.py --patch --push
   ```

## 🔧 配置说明

### PyPI发布配置

项目使用PyPA的trusted publishing，需要在PyPI项目设置中配置：

1. 登录PyPI，进入项目设置
2. 添加trusted publisher：
   - Owner: `mudssky`
   - Repository: `pyutils`
   - Workflow: `tag-release.yml`
   - Environment: `pypi`

### GitHub环境保护

在GitHub仓库设置中配置环境保护规则：

1. 创建`pypi`环境
2. 设置保护规则（可选）：
   - 需要审查者批准
   - 限制部署分支

## 🚨 故障排除

### 常见问题

#### 1. PyPI发布失败
```
Tag 'v1.0.0' is not allowed to deploy to pypi due to environment protection rules
```
**解决方案**：检查GitHub环境保护设置，或手动批准部署。

#### 2. 版本冲突
```
File already exists on PyPI
```
**解决方案**：确保版本号是唯一的，不要重复发布相同版本。

#### 3. Git状态不干净
```
Working directory is not clean
```
**解决方案**：提交或暂存所有更改，或使用`--skip-checks`选项。

#### 4. 权限问题
```
Permission denied
```
**解决方案**：确保有推送tag的权限，检查GitHub token配置。

### 调试技巧

1. **使用dry-run模式**：
   ```bash
   python scripts/create-release.py --patch --dry-run
   ```

2. **检查CI/CD日志**：
   ```bash
   gh run list
   gh run view <run-id>
   ```

3. **手动测试changelog**：
   ```bash
   python scripts/generate-changelog.py
   ```

## 📚 相关资源

- [Conventional Commits](https://www.conventionalcommits.org/)
- [Semantic Versioning](https://semver.org/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [PyPI Trusted Publishing](https://docs.pypi.org/trusted-publishers/)
- [Keep a Changelog](https://keepachangelog.com/)
