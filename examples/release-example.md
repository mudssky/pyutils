# 发布示例

本文档展示了如何使用项目的自动化发布工具。

## 🚀 快速开始

### 1. 使用Makefile（推荐）

```bash
# 查看所有可用命令
make help

# 查看发布相关命令
make release-help

# 预览发布（不实际执行）
make release-dry

# 发布补丁版本
make release-patch
```

### 2. 直接使用Python脚本

```bash
# 预览发布
python scripts/create-release.py --patch --dry-run

# 发布补丁版本
python scripts/create-release.py --patch --push

# 发布次版本
python scripts/create-release.py --minor --push

# 发布指定版本
python scripts/create-release.py --version 1.2.3 --push
```

## 📋 完整发布流程示例

### 场景1：修复Bug后发布补丁版本

```bash
# 1. 确保在main分支且代码是最新的
git checkout main
git pull origin main

# 2. 检查当前状态
make version
git status

# 3. 预览发布
make release-dry

# 4. 执行发布
make release-patch

# 5. 检查发布状态
make ci-status
```

### 场景2：添加新功能后发布次版本

```bash
# 1. 确保所有测试通过
make ci

# 2. 生成并查看changelog
make changelog

# 3. 发布次版本
make release-minor

# 4. 监控CI/CD流程
gh run list
gh run view  # 查看最新运行
```

### 场景3：重大更新发布主版本

```bash
# 1. 确保所有准备工作完成
make ci
make docs

# 2. 生成完整changelog
make changelog-file

# 3. 发布主版本
make release-major

# 4. 验证发布
echo "检查以下链接："
echo "- GitHub Release: https://github.com/mudssky/pyutils/releases"
echo "- PyPI: https://pypi.org/project/mudssky-pyutils/"
```

## 🔧 高级用法

### 自定义版本号

```bash
# 发布预发布版本
make release-version VERSION=1.0.0-beta.1

# 发布候选版本
make release-version VERSION=1.0.0-rc.1

# 发布特定版本
make release-version VERSION=2.1.0
```

### 生成Changelog

```bash
# 查看自上次tag以来的更改
make changelog

# 生成完整的changelog文件
make changelog-file

# 从特定tag生成changelog
python scripts/generate-changelog.py --from v1.0.0

# 生成特定范围的changelog
python scripts/generate-changelog.py --from v1.0.0 --to v1.1.0
```

### 监控和调试

```bash
# 查看CI/CD状态
make ci-status

# 查看详细日志
make ci-logs

# 查看所有tags
make tags

# 查看当前版本
make version
```

## 📝 Commit规范示例

### 功能开发
```bash
git commit -m "feat(auth): add OAuth2 authentication support"
git commit -m "feat(api): implement user profile endpoints"
git commit -m "feat!: remove deprecated v1 API endpoints"  # Breaking change
```

### Bug修复
```bash
git commit -m "fix(auth): handle expired tokens correctly"
git commit -m "fix(api): validate input parameters"
git commit -m "fix(deps): update vulnerable dependency"
```

### 文档和维护
```bash
git commit -m "docs: update installation instructions"
git commit -m "docs(api): add examples for new endpoints"
git commit -m "chore: bump version to 1.2.0"
git commit -m "ci: update GitHub Actions workflow"
```

### 性能和重构
```bash
git commit -m "perf(cache): optimize Redis connection pooling"
git commit -m "refactor(auth): simplify token validation logic"
git commit -m "style: format code with black"
```

## 🎯 最佳实践

### 发布前检查清单

- [ ] 所有测试通过 (`make test`)
- [ ] 代码质量检查通过 (`make lint`)
- [ ] 类型检查通过 (`make type-check`)
- [ ] 文档是最新的 (`make docs`)
- [ ] 版本号符合语义化版本规范
- [ ] Changelog准确反映了更改

### 发布后验证

- [ ] GitHub Release已创建
- [ ] PyPI包已发布
- [ ] CI/CD流程成功完成
- [ ] 文档网站已更新
- [ ] 安装测试：`pip install mudssky-pyutils==<new-version>`

### 紧急修复流程

```bash
# 1. 创建hotfix分支
git checkout -b hotfix/critical-bug main

# 2. 修复问题
# ... 编写修复代码 ...
git add .
git commit -m "fix(critical): resolve security vulnerability"

# 3. 测试修复
make test
make ci

# 4. 合并到main
git checkout main
git merge hotfix/critical-bug
git push origin main

# 5. 立即发布
make release-patch

# 6. 清理
git branch -d hotfix/critical-bug
```

## 🚨 故障排除

### 常见错误和解决方案

#### 1. 版本冲突
```bash
# 错误：版本已存在
# 解决：检查当前版本并递增
make version
python scripts/create-release.py --patch --dry-run
```

#### 2. Git状态不干净
```bash
# 错误：有未提交的更改
# 解决：提交或暂存更改
git status
git add .
git commit -m "chore: prepare for release"
```

#### 3. CI/CD失败
```bash
# 检查失败原因
make ci-logs

# 重新运行CI
gh run rerun
```

#### 4. PyPI发布失败
```bash
# 检查PyPI配置
# 确保trusted publishing已配置
# 检查环境保护规则
```

### 调试技巧

```bash
# 1. 使用dry-run模式测试
python scripts/create-release.py --patch --dry-run

# 2. 检查生成的changelog
python scripts/generate-changelog.py

# 3. 验证版本更新
grep -n "version" pyproject.toml src/pyutils/__init__.py

# 4. 检查git历史
git log --oneline -10
git tag --sort=-version:refname | head -5
```

## 📚 相关文档

- [完整发布指南](../docs/RELEASE.md)
- [项目README](../README.md)
- [贡献指南](../CONTRIBUTING.md)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Semantic Versioning](https://semver.org/)