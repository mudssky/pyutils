# PyPI 发布故障排除指南

## 问题概述

根据 GitHub Actions 运行记录 `16133875817/job/45526329887`，Release 工作流在发布到 PyPI 过程中失败。

## 可能的问题原因

### 1. Twine 认证配置问题

**问题描述：** 
- 在 `release.yml` 中，PyPI 认证通过环境变量 `PYPI_TOKEN` 配置
- 但 twine 可能无法正确读取认证信息

**当前配置：**
```bash
# Configure PyPI authentication
echo "[pypi]" > ~/.pypirc
echo "username = __token__" >> ~/.pypirc
echo "password = $PYPI_TOKEN" >> ~/.pypirc
```

**可能的解决方案：**

#### 方案 1：使用 twine 环境变量（推荐）
```yaml
- name: Release
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
    TWINE_USERNAME: __token__
    TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
  run: |
    # Configure git for semantic-release
    git config --global user.name "github-actions[bot]"
    git config --global user.email "github-actions[bot]@users.noreply.github.com"
    
    # Run semantic-release
    npx semantic-release
```

#### 方案 2：修复 .pypirc 配置
```bash
# 确保正确的 .pypirc 格式
cat > ~/.pypirc << EOF
[distutils]
index-servers = pypi

[pypi]
username = __token__
password = $PYPI_TOKEN
EOF
```

### 2. 构建过程问题

**问题描述：**
- `uv build` 命令可能失败
- 生成的 dist 文件可能有问题

**诊断步骤：**
```bash
# 本地测试构建过程
uv build
ls -la dist/

# 检查生成的包
twine check dist/*
```

### 3. semantic-release 配置问题

**当前配置分析：**
```json
{
  "prepareCmd": "uv run python scripts/update-version.py ${nextRelease.version}",
  "publishCmd": "uv build && uv run twine upload dist/*"
}
```

**可能的问题：**
- `uv run twine upload` 可能无法正确读取环境变量
- 需要确保 twine 在正确的环境中运行

### 4. 权限和 Secret 配置问题

**检查清单：**
- [ ] `PYPI_API_TOKEN` secret 是否正确配置
- [ ] Token 是否有足够的权限
- [ ] Token 是否已过期

## 推荐解决方案

### 立即修复方案

1. **更新 release.yml 使用 TWINE 环境变量：**

```yaml
- name: Release
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
    TWINE_USERNAME: __token__
    TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
  run: |
    # Configure git for semantic-release
    git config --global user.name "github-actions[bot]"
    git config --global user.email "github-actions[bot]@users.noreply.github.com"
    
    # Run semantic-release
    npx semantic-release
```

2. **添加调试信息到 .releaserc.json：**

```json
{
  "prepareCmd": "uv run python scripts/update-version.py ${nextRelease.version}",
  "publishCmd": "uv build && echo 'Build completed, files:' && ls -la dist/ && uv run twine check dist/* && uv run twine upload dist/* --verbose"
}
```

### 长期优化方案

1. **使用 PyPA 官方 GitHub Action：**

```yaml
- name: Publish to PyPI
  uses: pypa/gh-action-pypi-publish@release/v1
  with:
    password: ${{ secrets.PYPI_API_TOKEN }}
    packages-dir: dist/
```

2. **分离构建和发布步骤：**

```json
{
  "prepareCmd": "uv run python scripts/update-version.py ${nextRelease.version} && uv build",
  "publishCmd": "uv run twine upload dist/* --verbose"
}
```

## 验证步骤

1. **本地测试：**
```bash
# 测试构建
uv build
twine check dist/*

# 测试上传到 TestPyPI
twine upload --repository testpypi dist/*
```

2. **检查 GitHub Secrets：**
- 确认 `PYPI_API_TOKEN` 已正确配置
- 验证 token 权限和有效期

3. **监控下次发布：**
- 查看详细的构建日志
- 确认每个步骤的输出

## 注意事项

1. **版本冲突：** 确保不会重复发布相同版本
2. **包名冲突：** 确认 PyPI 上的包名可用性
3. **依赖问题：** 确保所有依赖都正确安装

## 下一步行动

1. 立即应用推荐的修复方案
2. 创建一个测试 PR 验证修复效果
3. 监控下次自动发布的结果
4. 考虑添加更详细的错误处理和日志记录