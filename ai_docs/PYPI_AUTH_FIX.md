# PyPI 认证问题修复报告

## 问题描述

在发布包到 PyPI 时遇到以下错误：

```
ERROR    HTTPError: 403 Forbidden from https://upload.pypi.org/legacy/
         Username/Password authentication is no longer supported. Migrate to API Tokens or Trusted Publishers instead.
```

## 问题原因

虽然项目已经配置了 API Token，但是在环境变量配置中，用户名仍然设置为实际的用户名（`mudssky`），而不是 PyPI 要求的特殊值 `__token__`。

当使用 API Token 进行认证时，PyPI 要求：
- 用户名必须设置为 `__token__`
- 密码设置为实际的 API Token（以 `pypi-` 开头）

## 修复措施

### 1. 更新 .env 文件

将所有用户名配置从实际用户名改为 `__token__`：

```bash
# 修复前
TWINE_USERNAME=mudssky
TWINE_USERNAME_TESTPYPI=mudssky
TWINE_USERNAME_PYPI=mudssky

# 修复后
TWINE_USERNAME=__token__
TWINE_USERNAME_TESTPYPI=__token__
TWINE_USERNAME_PYPI=__token__
```

### 2. 更新文档

更新了 `ENV_SETUP.md` 文档，添加了以下内容：

- 明确说明使用 API Token 时用户名必须为 `__token__`
- 在环境变量说明表格中标注了这一要求
- 在故障排除部分添加了针对此错误的具体解决方案

### 3. 验证修复

通过命令验证 `.env` 文件中的配置已正确更新：

```powershell
Get-Content .env | Select-String 'TWINE_USERNAME'
```

输出确认所有用户名都已设置为 `__token__`：

```
TWINE_USERNAME=__token__
TWINE_USERNAME_TESTPYPI=__token__
TWINE_USERNAME_PYPI=__token__
```

## 预期结果

修复后，发布脚本应该能够：

1. 正确使用 API Token 进行认证
2. 成功发布到 TestPyPI 和正式 PyPI
3. 避免 "Username/Password authentication is no longer supported" 错误

## 相关文档

- `ENV_SETUP.md` - 环境变量配置详细指南
- `RELEASE_GUIDE.md` - 发布流程指南
- `ENVIRONMENT_MIGRATION.md` - 从 .pypirc 到环境变量的迁移记录

## 注意事项

1. **安全性**：确保 `.env` 文件不被提交到版本控制系统
2. **Token 管理**：定期检查和更新 API Token
3. **权限验证**：确保 API Token 具有发布包的权限

## 测试建议

在下次发布时，建议：

1. 先使用 `-TestOnly` 参数测试发布到 TestPyPI
2. 验证 TestPyPI 发布成功后再发布到正式 PyPI
3. 监控发布过程中的认证相关日志

---

**修复时间**: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')
**修复状态**: ✅ 已完成