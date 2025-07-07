# GitHub Pages 设置指南

本文档说明如何为 pyutils 项目设置 GitHub Pages 来自动部署 Sphinx 文档。

## 启用 GitHub Pages

### 1. 在 GitHub 仓库中启用 Pages

1. 进入 GitHub 仓库页面
2. 点击 **Settings** 标签
3. 在左侧菜单中找到 **Pages** 选项
4. 在 **Source** 部分选择 **GitHub Actions**
5. 保存设置

### 2. 工作流程说明

我们的 `release.yml` 工作流程包含以下 GitHub Pages 相关步骤：

#### 文档构建步骤
```yaml
- name: Build documentation
  run: |
    cd docs
    uv run sphinx-build -b html . _build/html
    # Create .nojekyll file to allow files with underscores
    touch _build/html/.nojekyll
```

#### GitHub Pages 部署步骤
```yaml
- name: Deploy to GitHub Pages
  if: success()
  uses: peaceiris/actions-gh-pages@v3
  with:
    github_token: ${{ secrets.GITHUB_TOKEN }}
    publish_dir: ./docs/_build/html
    force_orphan: true
    user_name: 'github-actions[bot]'
    user_email: 'github-actions[bot]@users.noreply.github.com'
    commit_message: 'Deploy documentation to GitHub Pages'
```

### 3. 权限配置

工作流程需要以下权限：
```yaml
permissions:
  contents: write
  issues: write
  pull-requests: write
  id-token: write
  pages: write      # GitHub Pages 部署权限
  actions: read     # 读取 Actions 状态权限
```

## 文档访问

### 访问地址

文档部署成功后，可以通过以下地址访问：
- **主地址**: `https://{username}.github.io/{repository-name}/`
- **本项目**: `https://mudssky.github.io/pyutils/`

### 自动更新

- 每次发布新版本时，文档会自动重新构建和部署
- 文档内容基于最新的代码和 docstring
- 部署过程完全自动化，无需手动干预

## 文档结构

### Sphinx 配置

文档使用 Sphinx 构建，配置文件为 `docs/conf.py`：

- **主题**: `sphinx_rtd_theme` (Read the Docs 主题)
- **扩展**: 包含 autodoc、napoleon、viewcode 等
- **API 文档**: 自动从代码生成
- **类型提示**: 支持类型注解显示

### 文档内容

- **API 参考**: 自动生成的 API 文档
- **使用指南**: 安装和使用说明
- **示例代码**: 实际使用示例
- **更新日志**: 版本变更记录

## 故障排除

### 常见问题

1. **部署失败**
   - 检查 GitHub Pages 是否已启用
   - 确认工作流程权限配置正确
   - 查看 Actions 日志中的错误信息

2. **文档构建失败**
   - 检查 Sphinx 依赖是否正确安装
   - 确认 `docs/conf.py` 配置无误
   - 检查代码中的 docstring 格式

3. **页面显示异常**
   - 确认 `.nojekyll` 文件已创建
   - 检查静态文件路径是否正确
   - 验证 HTML 输出是否正常

### 调试步骤

1. **本地测试文档构建**:
   ```bash
   cd docs
   uv run sphinx-build -b html . _build/html
   ```

2. **检查构建输出**:
   ```bash
   ls -la docs/_build/html/
   ```

3. **本地预览文档**:
   ```bash
   cd docs/_build/html
   python -m http.server 8000
   ```

## 维护说明

### 定期维护

- 定期更新 Sphinx 和相关依赖
- 检查文档链接的有效性
- 更新文档内容以反映代码变更

### 监控部署

- 关注 GitHub Actions 的执行状态
- 检查 GitHub Pages 的部署日志
- 验证文档网站的可访问性

---

通过以上配置，pyutils 项目的文档将在每次发布时自动更新，为用户提供最新的 API 参考和使用指南。
