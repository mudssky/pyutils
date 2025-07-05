# 环境变量配置指南

本项目使用环境变量进行 PyPI 认证，替代传统的 `.pypirc` 文件配置方式。

## 配置步骤

### 1. 获取 API Tokens

#### TestPyPI Token
1. 访问 [TestPyPI Account Settings](https://test.pypi.org/manage/account/)
2. 登录你的账户
3. 滚动到 "API tokens" 部分
4. 点击 "Add API token"
5. 输入 token 名称（如：`mudssky-pyutils-testpypi`）
6. 选择 Scope（建议选择 "Entire account" 或特定项目）
7. 点击 "Add token"
8. **重要**：复制生成的 token（以 `pypi-` 开头），这是唯一一次显示

#### 正式 PyPI Token
1. 访问 [PyPI Account Settings](https://pypi.org/manage/account/)
2. 重复上述相同步骤
3. 复制生成的 token

### 2. 更新 .env 文件

编辑项目根目录下的 `.env` 文件，将占位符替换为实际的 API tokens：

```bash
# PyPI 认证配置
TWINE_USERNAME=__token__

# TestPyPI 配置
TWINE_REPOSITORY_URL_TESTPYPI=https://test.pypi.org/legacy/
TWINE_USERNAME_TESTPYPI=__token__
TWINE_PASSWORD_TESTPYPI=pypi-your_actual_testpypi_token_here

# 正式 PyPI 配置
TWINE_REPOSITORY_URL_PYPI=https://upload.pypi.org/legacy/
TWINE_USERNAME_PYPI=__token__
TWINE_PASSWORD_PYPI=pypi-your_actual_pypi_token_here

# 默认配置（用于向后兼容）
TWINE_PASSWORD=pypi-your_default_token_here
```

**重要提示**：使用 API Token 时，用户名必须设置为 `__token__`，这是 PyPI 的要求。

### 3. 安全注意事项

- **永远不要将 `.env` 文件提交到版本控制系统**
- `.env` 文件已添加到 `.gitignore` 中
- API tokens 具有完整的账户权限，请妥善保管
- 如果 token 泄露，立即在 PyPI/TestPyPI 网站上撤销并重新生成

### 4. 环境变量说明

| 变量名 | 用途 | 示例值 |
|--------|------|--------|
| `TWINE_USERNAME` | 默认用户名（API Token 时必须为 `__token__`） | `__token__` |
| `TWINE_PASSWORD` | 默认密码/token | `pypi-...` |
| `TWINE_REPOSITORY_URL_TESTPYPI` | TestPyPI 仓库地址 | `https://test.pypi.org/legacy/` |
| `TWINE_USERNAME_TESTPYPI` | TestPyPI 用户名（API Token 时必须为 `__token__`） | `__token__` |
| `TWINE_PASSWORD_TESTPYPI` | TestPyPI API token | `pypi-...` |
| `TWINE_REPOSITORY_URL_PYPI` | 正式 PyPI 仓库地址 | `https://upload.pypi.org/legacy/` |
| `TWINE_USERNAME_PYPI` | 正式 PyPI 用户名（API Token 时必须为 `__token__`） | `__token__` |
| `TWINE_PASSWORD_PYPI` | 正式 PyPI API token | `pypi-...` |

## 使用方法

配置完成后，直接运行发布脚本：

```powershell
# 仅发布到 TestPyPI
.\publish.ps1 -TestOnly

# 发布到 TestPyPI 和正式 PyPI
.\publish.ps1

# 强制发布（跳过测试失败）
.\publish.ps1 -Force
```

脚本会自动加载 `.env` 文件中的环境变量，无需手动配置。

## 故障排除

### 常见错误

1. **403 Forbidden**: API token 无效或权限不足
   - 检查 token 是否正确复制
   - 确认 token 未过期
   - 验证 token 权限范围

2. **401 Unauthorized**: 认证失败
   - 检查用户名是否设置为 `__token__`（使用 API Token 时必须）
   - 确认 token 格式正确（以 `pypi-` 开头）

3. **403 Forbidden - Username/Password authentication is no longer supported**: 
   - 这表示仍在使用用户名/密码认证而非 API Token
   - 确保 `TWINE_USERNAME` 设置为 `__token__`
   - 确保 `TWINE_PASSWORD` 设置为有效的 API Token

4. **环境变量未加载**: 
   - 确认 `.env` 文件存在于项目根目录
   - 检查文件格式（无 BOM，UTF-8 编码）
   - 验证变量名拼写正确

### 调试技巧

在脚本中添加调试输出（仅用于调试，不要提交到版本控制）：

```powershell
# 临时添加到脚本中进行调试
Write-Host "TWINE_USERNAME: $env:TWINE_USERNAME"
Write-Host "TWINE_REPOSITORY_URL: $env:TWINE_REPOSITORY_URL"
# 注意：永远不要输出密码/token
```

## 迁移说明

如果之前使用 `.pypirc` 文件，现在可以安全删除：

```powershell
Remove-Item $env:USERPROFILE\.pypirc -Force -ErrorAction SilentlyContinue
```

环境变量方式的优势：
- 更好的安全性（不会意外提交到版本控制）
- 更灵活的配置（可以针对不同环境使用不同配置）
- 更简单的 CI/CD 集成
- 更好的跨平台兼容性