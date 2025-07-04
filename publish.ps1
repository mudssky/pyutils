# Windows PowerShell 发布脚本
# 用于在 Windows 系统上发布 Python 包到 PyPI

param(
    [switch]$TestOnly,
    [switch]$SkipTests,
    [switch]$Force
)

# 设置错误处理
$ErrorActionPreference = "Stop"

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
    try {
        uv run twine upload --repository testpypi dist/*
        Write-Host "✓ 成功发布到 TestPyPI" -ForegroundColor Green
        Write-Host "测试安装命令：" -ForegroundColor Yellow
        Write-Host "pip install --index-url https://test.pypi.org/simple/ mudssky-pyutils" -ForegroundColor Cyan
    } catch {
        Write-Host "✗ 发布到 TestPyPI 失败：$_" -ForegroundColor Red
        exit 1
    }
} else {
    # 先发布到 TestPyPI
    Write-Host "发布到 TestPyPI 进行测试..." -ForegroundColor Green
    try {
        uv run twine upload --repository testpypi dist/*
        Write-Host "✓ 成功发布到 TestPyPI" -ForegroundColor Green
    } catch {
        Write-Host "✗ 发布到 TestPyPI 失败：$_" -ForegroundColor Red
        if (-not $Force) {
            exit 1
        }
        Write-Host "强制继续..." -ForegroundColor Yellow
    }
    
    Write-Host ""
    Write-Host "请在 TestPyPI 上验证包是否正常：" -ForegroundColor Yellow
    Write-Host "https://test.pypi.org/project/mudssky-pyutils/" -ForegroundColor Cyan
    Write-Host "测试安装命令：" -ForegroundColor Yellow
    Write-Host "pip install --index-url https://test.pypi.org/simple/ mudssky-pyutils" -ForegroundColor Cyan
    Write-Host ""
    
    # 确认发布到正式 PyPI
    if (-not $Force) {
        $confirm = Read-Host "确认发布到正式 PyPI？(y/N)"
        if ($confirm -ne 'y' -and $confirm -ne 'Y') {
            Write-Host "取消发布到正式 PyPI" -ForegroundColor Yellow
            exit 0
        }
    }
    
    Write-Host "发布到正式 PyPI..." -ForegroundColor Green
    try {
        uv run twine upload dist/*
        Write-Host "✓ 成功发布到正式 PyPI" -ForegroundColor Green
        Write-Host "安装命令：" -ForegroundColor Yellow
        Write-Host "pip install mudssky-pyutils" -ForegroundColor Cyan
        Write-Host "项目页面：" -ForegroundColor Yellow
        Write-Host "https://pypi.org/project/mudssky-pyutils/" -ForegroundColor Cyan
    } catch {
        Write-Host "✗ 发布到正式 PyPI 失败：$_" -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
Write-Host "=== 发布完成 ===" -ForegroundColor Magenta
Write-Host "时间：$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Cyan