# Windows PowerShell 发布脚本
# 用于在 Windows 系统上发布 Python 包到 PyPI

param(
    [switch]$TestOnly,
    [switch]$SkipTests,
    [switch]$Force
)

# 设置错误处理
$ErrorActionPreference = "Stop"

# 加载环境变量
function Load-EnvFile {
    param($FilePath)
    if (Test-Path $FilePath) {
        Write-Host "加载环境变量文件: $FilePath" -ForegroundColor Green
        Get-Content $FilePath | ForEach-Object {
            if ($_ -match '^([^#][^=]+)=(.*)$') {
                $name = $matches[1].Trim()
                $value = $matches[2].Trim()
                # 移除值两端的引号（如果存在）
                if ($value -match '^["\''](.*)["\'']$') {
                    $value = $matches[1]
                }
                [Environment]::SetEnvironmentVariable($name, $value, "Process")
                Write-Host "  设置环境变量: $name" -ForegroundColor Cyan
            }
        }
    } else {
        Write-Host "警告：未找到环境变量文件 $FilePath" -ForegroundColor Yellow
    }
}

# 加载 .env 文件
Load-EnvFile ".env"

# 验证必需的环境变量
function Test-RequiredEnvironmentVariables {
    $required = @(
        "TWINE_USERNAME",
        "TWINE_PASSWORD",
        "TWINE_USERNAME_TESTPYPI",
        "TWINE_PASSWORD_TESTPYPI",
        "TWINE_USERNAME_PYPI",
        "TWINE_PASSWORD_PYPI"
    )
    
    $missing = @()
    foreach ($var in $required) {
        $value = [Environment]::GetEnvironmentVariable($var)
        if (-not $value -or $value.Trim() -eq "") {
            $missing += $var
        }
    }
    
    if ($missing.Count -gt 0) {
        Write-Host "✗ 缺少必需的环境变量：" -ForegroundColor Red
        $missing | ForEach-Object { Write-Host "  - $_" -ForegroundColor Yellow }
        Write-Host "请检查 .env 文件配置，参考 .env.template 文件" -ForegroundColor Yellow
        return $false
    }
    
    # 验证用户名是否正确设置为 __token__
    $usernameVars = @("TWINE_USERNAME", "TWINE_USERNAME_TESTPYPI", "TWINE_USERNAME_PYPI")
    foreach ($var in $usernameVars) {
        $value = [Environment]::GetEnvironmentVariable($var)
        if ($value -ne "__token__") {
            Write-Host "✗ $var 应该设置为 '__token__'，当前值：$value" -ForegroundColor Red
            Write-Host "使用 API Token 时，用户名必须设置为 '__token__'" -ForegroundColor Yellow
            return $false
        }
    }
    
    Write-Host "✓ 环境变量验证通过" -ForegroundColor Green
    return $true
}

Write-Host "=== Python 包发布脚本 ===" -ForegroundColor Magenta
Write-Host "项目：mudssky-pyutils" -ForegroundColor Cyan
Write-Host "时间：$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Cyan
Write-Host ""

# 检查必要工具
function Test-Command {
    param($Command)
    try {
        Get-Command $Command -ErrorAction Stop | Out-Null
        return $true
    } catch {
        return $false
    }
}

Write-Host "检查必要工具..." -ForegroundColor Green

if (-not (Test-Command "uv")) {
    Write-Host "错误：未找到 uv 命令，请先安装 uv" -ForegroundColor Red
    exit 1
}

if (-not (Test-Command "python")) {
    Write-Host "错误：未找到 python 命令" -ForegroundColor Red
    exit 1
}

Write-Host "✓ 工具检查通过" -ForegroundColor Green
Write-Host ""

# 验证环境变量
if (-not (Test-RequiredEnvironmentVariables)) {
    exit 1
}
Write-Host ""

# 运行测试（除非跳过）
if (-not $SkipTests) {
    Write-Host "运行测试套件..." -ForegroundColor Green
    try {
        uv run pytest tests/ -v
        Write-Host "✓ 测试通过" -ForegroundColor Green
    } catch {
        Write-Host "✗ 测试失败" -ForegroundColor Red
        if (-not $Force) {
            Write-Host "使用 -Force 参数可强制继续发布" -ForegroundColor Yellow
            exit 1
        }
        Write-Host "强制继续..." -ForegroundColor Yellow
    }
    Write-Host ""
}

# 运行代码质量检查
Write-Host "运行代码质量检查..." -ForegroundColor Green
try {
    Write-Host "  - Ruff 检查..."
    uv run ruff check src/ tests/

    Write-Host "  - 类型检查..."
    uv run mypy src/

    Write-Host "✓ 代码质量检查通过" -ForegroundColor Green
} catch {
    Write-Host "✗ 代码质量检查失败" -ForegroundColor Red
    if (-not $Force) {
        Write-Host "使用 -Force 参数可强制继续发布" -ForegroundColor Yellow
        exit 1
    }
    Write-Host "强制继续..." -ForegroundColor Yellow
}
Write-Host ""

# 清理和构建
Write-Host "清理构建目录..." -ForegroundColor Green

# 清理构建目录
@("build", "dist", ".eggs") | ForEach-Object {
    if (Test-Path $_) {
        Remove-Item -Recurse -Force $_
        Write-Host "  已删除 $_"
    }
}

# 清理 egg-info 文件
Get-ChildItem -Recurse -Name "*.egg-info" | ForEach-Object {
    if (Test-Path $_) {
        Remove-Item -Recurse -Force $_
        Write-Host "  已删除 $_"
    }
}

Write-Host "✓ 清理完成" -ForegroundColor Green
Write-Host ""

# 构建包
Write-Host "构建包..." -ForegroundColor Green
try {
    uv build
    Write-Host "✓ 构建成功" -ForegroundColor Green
} catch {
    Write-Host "✗ 构建失败：$_" -ForegroundColor Red
    exit 1
}

# 显示构建结果
if (Test-Path "dist") {
    Write-Host "构建文件：" -ForegroundColor Yellow
    Get-ChildItem "dist" | ForEach-Object {
        $size = [math]::Round($_.Length / 1KB, 2)
        Write-Host "  $($_.Name) ($size KB)" -ForegroundColor Cyan
    }
}
Write-Host ""

# 检查包
Write-Host "检查包完整性..." -ForegroundColor Green
try {
    uv run twine check dist/*
    Write-Host "✓ 包检查通过" -ForegroundColor Green
} catch {
    Write-Host "✗ 包检查失败：$_" -ForegroundColor Red
    exit 1
}
Write-Host ""

# 发布到 TestPyPI 或正式 PyPI
if ($TestOnly) {
    Write-Host "发布到 TestPyPI..." -ForegroundColor Green
    $testOnlySuccess = $false
    try {
        # 设置 TestPyPI 环境变量
        $env:TWINE_REPOSITORY_URL = $env:TWINE_REPOSITORY_URL_TESTPYPI
        $env:TWINE_USERNAME = $env:TWINE_USERNAME_TESTPYPI
        $env:TWINE_PASSWORD = $env:TWINE_PASSWORD_TESTPYPI
        
        uv run twine upload dist/*
        Write-Host "✓ 成功发布到 TestPyPI" -ForegroundColor Green
        Write-Host "测试安装命令：" -ForegroundColor Yellow
        Write-Host "pip install --index-url https://test.pypi.org/simple/ mudssky-pyutils" -ForegroundColor Cyan
        $testOnlySuccess = $true
    } catch {
        Write-Host "✗ 发布到 TestPyPI 失败：$_" -ForegroundColor Red
        exit 1
    }
} else {
    # 先发布到 TestPyPI
    Write-Host "发布到 TestPyPI 进行测试..." -ForegroundColor Green
    $testPypiSuccess = $false
    try {
        # 设置 TestPyPI 环境变量
        $env:TWINE_REPOSITORY_URL = $env:TWINE_REPOSITORY_URL_TESTPYPI
        $env:TWINE_USERNAME = $env:TWINE_USERNAME_TESTPYPI
        $env:TWINE_PASSWORD = $env:TWINE_PASSWORD_TESTPYPI
        
        $uploadResult = uv run twine upload dist/* 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✓ 成功发布到 TestPyPI" -ForegroundColor Green
            $testPypiSuccess = $true
        } else {
            throw "Upload failed with exit code $LASTEXITCODE: $uploadResult"
        }
    } catch {
        Write-Host "✗ 发布到 TestPyPI 失败：$_" -ForegroundColor Red
        $testPypiSuccess = $false
        if (-not $Force) {
            Write-Host "使用 -Force 参数可以强制继续发布到正式 PyPI" -ForegroundColor Yellow
            exit 1
        }
        Write-Host "强制继续..." -ForegroundColor Yellow
    }

    Write-Host ""
    if ($testPypiSuccess) {
        Write-Host "请在 TestPyPI 上验证包是否正常：" -ForegroundColor Yellow
        Write-Host "https://test.pypi.org/project/mudssky-pyutils/" -ForegroundColor Cyan
        Write-Host "测试安装命令：" -ForegroundColor Yellow
        Write-Host "pip install --index-url https://test.pypi.org/simple/ mudssky-pyutils" -ForegroundColor Cyan
        Write-Host ""
    } else {
        Write-Host "注意：TestPyPI 上传失败，但将继续发布到正式 PyPI" -ForegroundColor Yellow
        Write-Host ""
    }

    # 确认发布到正式 PyPI
    if (-not $Force) {
        $confirm = Read-Host "确认发布到正式 PyPI？(y/N)"
        if ($confirm -ne 'y' -and $confirm -ne 'Y') {
            Write-Host "取消发布到正式 PyPI" -ForegroundColor Yellow
            exit 0
        }
    }

    Write-Host "发布到正式 PyPI..." -ForegroundColor Green
    $pypiSuccess = $false
    try {
        # 设置正式 PyPI 环境变量
        $env:TWINE_REPOSITORY_URL = $env:TWINE_REPOSITORY_URL_PYPI
        $env:TWINE_USERNAME = $env:TWINE_USERNAME_PYPI
        $env:TWINE_PASSWORD = $env:TWINE_PASSWORD_PYPI
        
        $uploadResult = uv run twine upload dist/* 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✓ 成功发布到正式 PyPI" -ForegroundColor Green
            Write-Host "安装命令：" -ForegroundColor Yellow
            Write-Host "pip install mudssky-pyutils" -ForegroundColor Cyan
            Write-Host "项目页面：" -ForegroundColor Yellow
            Write-Host "https://pypi.org/project/mudssky-pyutils/" -ForegroundColor Cyan
            $pypiSuccess = $true
        } else {
            throw "Upload failed with exit code $LASTEXITCODE: $uploadResult"
        }
    } catch {
        Write-Host "✗ 发布到正式 PyPI 失败：$_" -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
if ($TestOnly) {
    if ($testOnlySuccess) {
        Write-Host "=== 发布完成 ===" -ForegroundColor Magenta
        Write-Host "✓ TestPyPI 发布成功" -ForegroundColor Green
    } else {
        Write-Host "=== 发布失败 ===" -ForegroundColor Red
        Write-Host "✗ TestPyPI 发布失败" -ForegroundColor Red
    }
} else {
    if ($pypiSuccess) {
        if ($testPypiSuccess) {
            Write-Host "=== 发布完成 ===" -ForegroundColor Magenta
            Write-Host "✓ TestPyPI 和正式 PyPI 都发布成功" -ForegroundColor Green
        } else {
            Write-Host "=== 发布部分完成 ===" -ForegroundColor Yellow
            Write-Host "✗ TestPyPI 发布失败，但正式 PyPI 发布成功" -ForegroundColor Yellow
        }
    } else {
        Write-Host "=== 发布失败 ===" -ForegroundColor Red
    }
}
Write-Host "时间：$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Cyan
