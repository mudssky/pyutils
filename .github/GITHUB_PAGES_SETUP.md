# GitHub Pages 文档部署配置

## 📚 概述

本项目已配置自动将 Sphinx 文档部署到 GitHub Pages，提供在线文档访问功能。

## 🚀 功能特性

- ✅ **自动构建**: 每次推送到 `main` 分支时自动构建文档
- ✅ **自动部署**: 构建完成后自动部署到 GitHub Pages
- ✅ **链接检查**: 自动检查文档中的链接有效性
- ✅ **PR 预览**: 在 Pull Request 中自动评论文档预览链接
- ✅ **并发控制**: 避免多个部署任务冲突

## ⚙️ 配置步骤

### 1. 启用 GitHub Pages

1. 进入 GitHub 仓库页面
2. 点击 **Settings** 标签
3. 在左侧菜单中选择 **Pages**
4. 在 **Source** 部分选择 **GitHub Actions**
5. 保存设置

### 2. 验证权限配置

确保工作流具有必要的权限（已在 `ci.yml` 中配置）：

```yaml
permissions:
  contents: read
  pages: write
  id-token: write
```

### 3. 测试部署

1. 推送代码到 `main` 分支
2. 在 **Actions** 标签中查看工作流运行状态
3. 部署完成后，访问 `https://<username>.github.io/<repository>`

## 📖 文档访问

### 在线文档地址

```
https://<username>.github.io/<repository>
```

### 文档结构

- **首页**: 项目概述和快速开始
- **API 文档**: 完整的 API 参考
- **使用指南**: 详细的使用说明
- **贡献指南**: 开发和贡献说明

## 🔧 自定义配置

### 自定义域名（可选）

1. 在仓库根目录创建 `CNAME` 文件
2. 在文件中添加你的自定义域名
3. 在域名提供商处配置 DNS 记录

### 文档主题自定义

编辑 `docs/conf.py` 文件来自定义文档主题和配置：

```python
# 主题配置
html_theme = 'sphinx_rtd_theme'
html_theme_options = {
    'navigation_depth': 4,
    'collapse_navigation': False,
    'sticky_navigation': True,
    'includehidden': True,
    'titles_only': False
}
```

## 📊 监控和维护

### 部署状态检查

- **工作流状态**: GitHub Actions 页面
- **部署历史**: Settings → Pages → 查看部署历史
- **链接检查**: 工作流输出中的 linkcheck 结果

### 常见问题排查

**1. 部署失败**
- 检查工作流日志中的错误信息
- 确认 Sphinx 配置文件 `docs/conf.py` 正确
- 验证文档源文件语法

**2. 页面无法访问**
- 确认 GitHub Pages 已启用
- 检查仓库是否为公开仓库
- 等待 DNS 传播（可能需要几分钟）

**3. 文档内容未更新**
- 确认推送到了 `main` 分支
- 检查工作流是否成功运行
- 清除浏览器缓存

## 🔄 工作流详解

### 触发条件

文档部署在以下情况下触发：

- 推送到 `main` 分支（且文档文件有变更）
- 手动触发工作流
- 文档相关文件发生变更

### 部署流程

```mermaid
graph LR
    A[代码推送] --> B[检测文档变更]
    B --> C[构建 Sphinx 文档]
    C --> D[链接检查]
    D --> E[上传到 GitHub Pages]
    E --> F[部署完成]
    F --> G[评论 PR 预览链接]
```

### 并发控制

为避免多个部署任务冲突，配置了并发控制：

```yaml
concurrency:
  group: "pages"
  cancel-in-progress: false
```

## 📝 最佳实践

1. **文档编写**:
   - 使用清晰的标题结构
   - 添加代码示例和用法说明
   - 保持文档与代码同步更新

2. **链接管理**:
   - 使用相对链接引用项目内文件
   - 定期检查外部链接有效性
   - 避免使用绝对路径

3. **性能优化**:
   - 优化图片大小和格式
   - 使用 CDN 加速静态资源
   - 启用 GZIP 压缩

## 🆘 获取帮助

如果遇到问题，可以：

1. 查看 [GitHub Pages 官方文档](https://docs.github.com/en/pages)
2. 查看 [Sphinx 官方文档](https://www.sphinx-doc.org/)
3. 在项目 Issues 中提问
4. 查看工作流运行日志获取详细错误信息