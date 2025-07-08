# Semantic-Release 故障排除指南

## 问题分析

### 1. 为什么 Semantic-Release 没有发布新版本？

通过分析 GitHub Actions 日志和 Git 提交历史，发现问题原因：

**当前状态：**
- 最新标签：`v0.3.0` (commit: c1be67f)
- HEAD 位置：`e9514d8` (Merge pull request #9)
- 从 v0.3.0 到 HEAD 的提交：
  ```
  e9514d8 Merge pull request #9 from mudssky/dev
  c5ca539 Merge branch 'main' into dev  
  f54aaac refactor(ci): 使用 semantic-release 替代手动发布流程
  ```

**问题根因：**
1. **提交类型不触发发布**：唯一的功能性提交是 `refactor(ci)`，而 `refactor` 类型默认不触发版本发布
2. **Merge commits 被忽略**：Merge commits 通常不被 semantic-release 分析

### 2. Semantic-Release 默认发布规则

根据 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

| 提交类型 | 版本影响 | 说明 |
|---------|---------|------|
| `feat` | Minor (0.x.0) | 新功能 |
| `fix` | Patch (0.0.x) | Bug 修复 |
| `perf` | Patch (0.0.x) | 性能改进 |
| `refactor` | **无** | 代码重构（默认不发布）|
| `docs` | **无** | 文档更新 |
| `style` | **无** | 代码格式化 |
| `test` | **无** | 测试相关 |
| `chore` | **无** | 构建过程或辅助工具变动 |

## 解决方案

### 方案 1：修改提交类型配置（推荐）

如果希望 `refactor` 和 `ci` 类型的提交也能触发发布，需要自定义 commit-analyzer 配置：

```json
{
  "plugins": [
    [
      "@semantic-release/commit-analyzer",
      {
        "releaseRules": [
          {"type": "refactor", "release": "patch"},
          {"type": "ci", "release": "patch"},
          {"type": "perf", "release": "patch"},
          {"type": "revert", "release": "patch"}
        ]
      }
    ],
    // ... 其他插件
  ]
}
```

### 方案 2：手动触发发布

如果当前的 `refactor(ci)` 提交确实应该触发发布，可以：

1. **创建新的 feat 提交**：
   ```bash
   git commit --allow-empty -m "feat: 启用 semantic-release 自动化发布流程"
   git push origin main
   ```

2. **修改现有提交类型**（如果可以接受重写历史）：
   ```bash
   git rebase -i v0.3.0
   # 将 refactor(ci) 改为 feat(ci)
   ```

### 方案 3：配置 @semantic-release/git 权限

要解决 `@semantic-release/git` 在 main 分支提交代码的权限问题：

#### 3.1 更新 GitHub Actions 权限

在 `.github/workflows/release.yml` 中添加必要权限：

```yaml
permissions:
  contents: write  # 允许推送代码和创建标签
  issues: write    # 允许创建和更新 issues
  pull-requests: write  # 允许创建和更新 PR
  packages: write  # 允许发布包
```

#### 3.2 配置 checkout action

```yaml
- name: Checkout code
  uses: actions/checkout@v4
  with:
    fetch-depth: 0
    persist-credentials: false  # 重要：禁用默认凭据
    token: ${{ secrets.GITHUB_TOKEN }}  # 或使用 PAT
```

#### 3.3 处理受保护分支

如果 main 分支有保护规则：

1. **选项 A：调整分支保护规则**
   - 在 GitHub 仓库设置中，允许 GitHub Actions 绕过分支保护
   - 或者将 semantic-release bot 添加到允许推送的用户列表

2. **选项 B：使用 Personal Access Token (PAT)**
   ```yaml
   - name: Checkout code
     uses: actions/checkout@v4
     with:
       fetch-depth: 0
       token: ${{ secrets.SEMANTIC_RELEASE_TOKEN }}  # PAT with repo permissions
   ```

#### 3.4 安全考虑

使用 `@semantic-release/git` 自动提交到主分支存在风险：
- 可能绕过代码审查流程
- 增加了自动化失败的复杂性
- 可能与分支保护规则冲突

**替代方案**：考虑不使用 `@semantic-release/git`，而是：
- 让 CHANGELOG.md 和版本更新在发布后通过 PR 合并
- 使用专门的 bot 账户处理自动提交

## 推荐的配置更新

基于分析，建议采用方案 1，更新 `.releaserc.json`：

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
    [
      "@semantic-release/commit-analyzer",
      {
        "releaseRules": [
          {"type": "refactor", "release": "patch"},
          {"type": "ci", "release": "patch"},
          {"type": "perf", "release": "patch"},
          {"type": "revert", "release": "patch"}
        ]
      }
    ],
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

## 验证步骤

1. **本地测试**：
   ```bash
   npx semantic-release --dry-run
   ```

2. **检查提交历史**：
   ```bash
   git log v0.3.0..HEAD --oneline
   ```

3. **验证配置**：
   ```bash
   npx semantic-release --dry-run --debug
   ```

更新配置后，`refactor(ci): 使用 semantic-release 替代手动发布流程` 这个提交应该会触发一个 patch 版本发布（v0.3.1）。