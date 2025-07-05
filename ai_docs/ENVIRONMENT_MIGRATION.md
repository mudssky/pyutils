# 环境变量迁移说明

## 迁移概述

本项目已从使用 `.pypirc` 文件配置 PyPI 认证信息迁移到使用环境变量的方式。这种改变带来了更好的安全性和灵活性。

## 主要变更

### 1. 删除 `.pypirc` 文件
- 已删除用户目录下的 `~/.pypirc` 文件
- 不再依赖传统的 `.pypirc` 配置方式

### 2. 使用 `.env` 文件
- 在项目根目录创建 `.env` 文件
- 包含所有必要的 PyPI 认证环境变量
- 已添加到 `.gitignore` 确保不会被提交到版本控制

### 3. 更新发布脚本
- `publish.ps1` 脚本现在自动加载 `.env` 文件
- 使用环境变量进行 PyPI 和 TestPyPI 认证
- 移除了对 `--repository` 参数的依赖

## 环境变量配置

### 必需的环境变量

```bash
# PyPI 认证配置
TWINE_USERNAME=mudssky

# TestPyPI 配置
TWINE_REPOSITORY_URL_TESTPYPI=https://test.pypi.org/legacy/
TWINE_USERNAME_TESTPYPI=mudssky
TWINE_PASSWORD_TESTPYPI=pypi-your_testpypi_token_here

# 正式 PyPI 配置
TWINE_REPOSITORY_URL_PYPI=https://upload.pypi.org/legacy/
TWINE_USERNAME_PYPI=mudssky
TWINE_PASSWORD_PYPI=pypi-your_pypi_token_here

# 默认配置（用于向后兼容）
TWINE_PASSWORD=pypi-your_default_token_here
```

### 配置步骤

1. **获取 API Tokens**
   - TestPyPI: https://test.pypi.org/manage/account/
   - 正式 PyPI: https://pypi.org/manage/account/

2. **更新 `.env` 文件**
   - 将占位符替换为实际的 API tokens
   - 确保 tokens 以 `pypi-` 开头

3. **验证配置**
   - 运行 `./publish.ps1 -TestOnly` 测试 TestPyPI 发布
   - 确认环境变量正确加载

## 脚本改进

### 环境变量加载功能
- 新增 `Load-EnvFile` 函数自动解析 `.env` 文件
- 支持注释行（以 `#` 开头）
- 自动去除值两端的引号
- 提供详细的加载日志

### 动态环境变量设置
- TestPyPI 发布时自动设置相应的环境变量
- 正式 PyPI 发布时自动切换到正式环境变量
- 避免了硬编码的仓库配置

## 优势

### 安全性
- 环境变量不会被意外提交到版本控制
- 更容易管理敏感信息
- 支持不同环境使用不同配置

### 灵活性
- 可以轻松切换不同的 PyPI 账户
- 支持 CI/CD 环境的环境变量注入
- 更好的跨平台兼容性

### 维护性
- 集中管理所有认证信息
- 减少配置文件的复杂性
- 更清晰的配置结构

## 故障排除

### 常见问题

1. **环境变量未加载**
   - 检查 `.env` 文件是否存在于项目根目录
   - 确认文件格式正确（UTF-8，无 BOM）
   - 验证变量名拼写

2. **认证失败**
   - 确认 API tokens 正确且未过期
   - 检查 token 格式（应以 `pypi-` 开头）
   - 验证用户名正确

3. **权限错误**
   - 确认 API token 有足够的权限
   - 检查项目名称是否正确
   - 验证包名在 PyPI 上是否可用

### 调试技巧

在脚本执行过程中，会显示环境变量加载的详细信息：

```
加载环境变量文件: .env
  设置环境变量: TWINE_USERNAME
  设置环境变量: TWINE_REPOSITORY_URL_TESTPYPI
  设置环境变量: TWINE_USERNAME_TESTPYPI
  ...
```

如果看不到这些信息，说明 `.env` 文件可能存在问题。

## 相关文档

- [ENV_SETUP.md](ENV_SETUP.md) - 详细的环境变量配置指南
- [RELEASE_GUIDE.md](RELEASE_GUIDE.md) - 完整的发布流程指南
- [README.rst](README.rst) - 项目基本信息

## 迁移检查清单

- [x] 删除 `~/.pypirc` 文件
- [x] 创建 `.env` 文件
- [x] 更新 `publish.ps1` 脚本
- [x] 添加环境变量加载功能
- [x] 更新文档
- [ ] 配置实际的 API tokens
- [ ] 测试 TestPyPI 发布
- [ ] 测试正式 PyPI 发布

完成迁移后，请按照 [ENV_SETUP.md](ENV_SETUP.md) 中的说明配置实际的 API tokens。