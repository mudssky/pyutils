# Semantic-Release 配置优化指南

## 问题1: 配置检查上个tag以来的变动进行发布

**当前状态**: Semantic-Release 默认就是检查上个tag以来的变动，而不是仅检查本次提交。

**工作原理**:
- `@semantic-release/commit-analyzer` 插件会分析从上一个发布标签到当前HEAD的所有提交
- 它使用 `git log <last-tag>..HEAD` 来获取提交历史
- 基于提交消息的类型（feat, fix, BREAKING CHANGE等）决定版本号增量

**当前配置已正确**:
```json
{
  "plugins": [
    "@semantic-release/commit-analyzer",  // 分析提交历史
    "@semantic-release/release-notes-generator",  // 生成发布说明
    // ... 其他插件
  ]
}
```

**验证方法**:
- 查看GitHub Actions日志中的 "Analysis of X commits" 信息
- Semantic-Release会显示分析了多少个提交（从上个tag到HEAD）

## 问题2: 移除冗余的构建产物上传

**建议**: 应该移除 `Upload build artifacts` 步骤，因为 `@semantic-release/github` 已经处理了构建产物。

**原因**:
1. `@semantic-release/github` 插件已配置上传 `dist/*.whl` 和 `dist/*.tar.gz` 到GitHub Release
2. GitHub Actions的 `upload-artifact` 是临时存储，而GitHub Release是永久的
3. 避免重复上传和存储成本

**当前冗余配置**:
```yaml
- name: Upload build artifacts
  if: success()
  uses: actions/upload-artifact@v4
  with:
    name: dist-files
    path: dist/
    retention-days: 30
```

**GitHub Pages部署保留**:
`peaceiris/actions-gh-pages@v3` 应该保留，因为它:
- 将文档部署到 `gh-pages` 分支
- 与 `@semantic-release/github` 功能不冲突
- 专门用于GitHub Pages部署

## 问题3: 在项目内生成CHANGELOG.md

**当前配置已支持**: 项目已正确配置了changelog生成。

```json
[
  "@semantic-release/changelog",
  {
    "changelogFile": "CHANGELOG.md"
  }
]
```

**工作流程**:
1. `@semantic-release/changelog` 在项目根目录生成/更新 `CHANGELOG.md`
2. 文件包含所有版本的变更记录
3. 每次发布时自动更新

**注意**: 需要确保 `CHANGELOG.md` 被提交到仓库。如果需要自动提交changelog，需要添加 `@semantic-release/git` 插件。

## 问题4: 发布后同步更新版本号

**当前配置已处理**: 通过 `@semantic-release/exec` 插件实现。

```json
[
  "@semantic-release/exec",
  {
    "prepareCmd": "uv run python scripts/update-version.py ${nextRelease.version}",
    "publishCmd": "uv build && uv run twine upload dist/*"
  }
]
```

**工作流程**:
1. **prepareCmd**: 在发布前更新项目文件中的版本号
   - 更新 `pyproject.toml` 中的版本
   - 更新 `src/pyutils/__init__.py` 中的版本
2. **publishCmd**: 构建并发布到PyPI

**版本同步机制**:
- Semantic-Release确定新版本号
- 执行 `prepareCmd` 更新本地文件
- 创建Git标签
- 执行 `publishCmd` 发布包
- 创建GitHub Release

## 已实施的配置优化

### 1. ✅ 移除冗余的构建产物上传

已从 `release.yml` 中移除冗余的构建产物上传步骤：
```yaml
# 已移除这个步骤，因为 @semantic-release/github 会自动上传到 GitHub Release
# - name: Upload build artifacts
#   if: success()
#   uses: actions/upload-artifact@v4
#   with:
#     name: dist-files
#     path: dist/
#     retention-days: 30
```

### 2. ✅ 添加自动提交changelog

已添加 `@semantic-release/git` 插件来自动提交changelog和版本更新：

```json
{
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
        "prepareCmd": "uv run python scripts/update-version.py ${nextRelease.version}",
        "publishCmd": "uv build && uv run twine upload dist/*"
      }
    ],
    [
      "@semantic-release/git",
      {
        "assets": ["CHANGELOG.md", "pyproject.toml", "src/pyutils/__init__.py"],
        "message": "chore(release): ${nextRelease.version} [skip ci]\n\n${nextRelease.notes}"
      }
    ],
    [
      "@semantic-release/github",
      {
        "assets": [
          {
            "path": "dist/*.whl",
            "label": "Python Wheel"
          },
          {
            "path": "dist/*.tar.gz",
            "label": "Source Distribution"
          }
        ],
        "successComment": false,
        "failComment": false,
        "releasedLabels": false
      }
    ]
  ]
}
```

### 3. 验证配置

运行以下命令验证配置：
```bash
# 本地测试（不会实际发布）
npx semantic-release --dry-run

# 查看将要分析的提交
git log $(git describe --tags --abbrev=0)..HEAD --oneline
```

## 总结

### ✅ 已完成的优化

1. **提交分析**: ✅ 配置正确，semantic-release会分析上个tag以来的所有提交
2. **构建产物**: ✅ 已移除Actions的冗余artifact上传，保留GitHub Release上传
3. **Changelog**: ✅ 已配置自动生成和提交CHANGELOG.md到仓库
4. **版本同步**: ✅ 已通过update-version.py脚本实现自动版本更新
5. **自动提交**: ✅ 已添加@semantic-release/git插件自动提交版本更改

### 🔧 需要执行的命令

在下次发布前，需要安装新的依赖：
```bash
npm install
```

### 📋 优化后的工作流程

1. 开发者推送符合约定式提交的代码到main分支
2. GitHub Actions触发release工作流
3. Semantic-Release分析提交历史，确定版本号
4. 执行prepareCmd更新项目文件版本号
5. 生成CHANGELOG.md
6. 自动提交版本更改到仓库（带[skip ci]标签）
7. 创建Git标签
8. 构建并发布到PyPI
9. 创建GitHub Release并上传构建产物
10. 部署文档到GitHub Pages

配置现已完全优化，实现了完整的自动化发布流程。