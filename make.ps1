# PowerShell 构建脚本，提供类似 Makefile 的功能
# 使用方法：.\make.ps1 [命令] [参数]

param(
    [Parameter(Position=0)]
    [ValidateSet('help', 'clean', 'build', 'test', 'lint', 'format', 'type-check', 'publish', 'publish-test', 'install', 'dev-setup', 'ci', 'docs', 'benchmark', 'security')]
    [string]$Command = 'help',
    
    [switch]$Verbose,
    [switch]$Force
)

# 设置错误处理
$ErrorActionPreference = "Stop"

# 颜色输出函数
function Write-ColorOutput {
    param(
        [string]$Message,
        [string]$Color = 'White'
    )
    Write-Host $Message -ForegroundColor $Color
}

function Write-Success {
    param([string]$Message)
    Write-ColorOutput "✓ $Message" -Color 'Green'
}

function Write-Error {
    param([string]$Message)
    Write-ColorOutput "✗ $Message" -Color 'Red'
}

function Write-Info {
    param([string]$Message)
    Write-ColorOutput "ℹ $Message" -Color 'Cyan'
}

function Write-Warning {
    param([string]$Message)
    Write-ColorOutput "⚠ $Message" -Color 'Yellow'
}

# 检查命令是否存在
function Test-Command {
    param([string]$CommandName)
    try {
        Get-Command $CommandName -ErrorAction Stop | Out-Null
        return $true
    } catch {
        return $false
    }
}

# 执行命令并处理错误
function Invoke-SafeCommand {
    param(
        [string]$Command,
        [string]$Description,
        [switch]$IgnoreErrors
    )
    
    if ($Verbose) {
        Write-Info "执行: $Command"
    }
    
    try {
        Invoke-Expression $Command
        if ($LASTEXITCODE -ne 0 -and -not $IgnoreErrors) {
            throw "命令执行失败，退出码: $LASTEXITCODE"
        }
        if ($Description) {
            Write-Success $Description
        }
    } catch {
        Write-Error "$Description 失败: $_"
        if (-not $IgnoreErrors) {
            exit 1
        }
    }
}

# 显示帮助信息
function Show-Help {
    Write-ColorOutput "`n=== Python 项目构建工具 ===" -Color 'Magenta'
    Write-ColorOutput "使用方法: .\make.ps1 [命令] [参数]`n" -Color 'Cyan'
    
    Write-ColorOutput "可用命令:" -Color 'Yellow'
    Write-Host "  help         显示此帮助信息"
    Write-Host "  clean        清理构建文件和缓存"
    Write-Host "  build        构建包"
    Write-Host "  test         运行测试套件"
    Write-Host "  lint         代码风格检查"
    Write-Host "  format       代码格式化"
    Write-Host "  type-check   类型检查"
    Write-Host "  publish      发布到 PyPI"
    Write-Host "  publish-test 发布到 TestPyPI"
    Write-Host "  install      安装依赖"
    Write-Host "  dev-setup    设置开发环境"
    Write-Host "  ci           运行所有 CI 检查"
    Write-Host "  docs         生成文档"
    Write-Host "  benchmark    运行性能基准测试"
    Write-Host "  security     运行安全检查"
    
    Write-ColorOutput "`n可用参数:" -Color 'Yellow'
    Write-Host "  -Verbose     显示详细输出"
    Write-Host "  -Force       强制执行（忽略某些错误）"
    
    Write-ColorOutput "`n示例:" -Color 'Yellow'
    Write-Host "  .\make.ps1 build"
    Write-Host "  .\make.ps1 test -Verbose"
    Write-Host "  .\make.ps1 ci -Force"
    Write-Host ""
}

# 清理构建文件
function Invoke-Clean {
    Write-Info "清理构建文件和缓存..."
    
    # 清理构建目录
    $dirsToClean = @('build', 'dist', '.eggs', '.tox', 'htmlcov', '.pytest_cache', '.ruff_cache')
    foreach ($dir in $dirsToClean) {
        if (Test-Path $dir) {
            Remove-Item -Recurse -Force $dir
            Write-Host "  已删除 $dir"
        }
    }
    
    # 清理特定文件模式
    $patterns = @('*.egg-info', '*.egg', '__pycache__', '*.pyc', '*.pyo', '*~', '.coverage')
    foreach ($pattern in $patterns) {
        Get-ChildItem -Recurse -Force -Name $pattern -ErrorAction SilentlyContinue | ForEach-Object {
            $fullPath = Join-Path $PWD $_
            if (Test-Path $fullPath) {
                if ((Get-Item $fullPath).PSIsContainer) {
                    Remove-Item -Recurse -Force $fullPath
                } else {
                    Remove-Item -Force $fullPath
                }
                Write-Host "  已删除 $_"
            }
        }
    }
    
    Write-Success "清理完成"
}

# 构建包
function Invoke-Build {
    Write-Info "构建包..."
    
    # 先清理
    Invoke-Clean
    
    # 检查 uv 命令
    if (-not (Test-Command "uv")) {
        Write-Error "未找到 uv 命令，请先安装 uv"
        exit 1
    }
    
    # 构建
    Invoke-SafeCommand "uv build" "包构建"
    
    # 显示构建结果
    if (Test-Path "dist") {
        Write-Info "构建文件:"
        Get-ChildItem "dist" | ForEach-Object {
            $size = [math]::Round($_.Length / 1KB, 2)
            Write-Host "  $($_.Name) ($size KB)" -ForegroundColor Cyan
        }
    }
}

# 运行测试
function Invoke-Test {
    Write-Info "运行测试套件..."
    Invoke-SafeCommand "uv run pytest tests/" "测试"
}

# 代码风格检查
function Invoke-Lint {
    Write-Info "代码风格检查..."
    Invoke-SafeCommand "uv run ruff check src/ tests/" "代码风格检查"
}

# 代码格式化
function Invoke-Format {
    Write-Info "代码格式化..."
    Invoke-SafeCommand "uv run ruff format src/ tests/" "代码格式化"
    Invoke-SafeCommand "uv run ruff check --fix src/ tests/" "代码修复" -IgnoreErrors
}

# 类型检查
function Invoke-TypeCheck {
    Write-Info "类型检查..."
    Invoke-SafeCommand "uv run mypy src/" "类型检查"
}

# 发布到 PyPI
function Invoke-Publish {
    Write-Info "发布到 PyPI..."
    
    if (Test-Path "publish.ps1") {
        & ".\publish.ps1"
    } else {
        Write-Warning "未找到 publish.ps1 脚本，使用基本发布流程"
        Invoke-Build
        Invoke-SafeCommand "uv run twine check dist/*" "包检查"
        Invoke-SafeCommand "uv run twine upload dist/*" "发布到 PyPI"
    }
}

# 发布到 TestPyPI
function Invoke-PublishTest {
    Write-Info "发布到 TestPyPI..."
    
    if (Test-Path "publish.ps1") {
        & ".\publish.ps1" -TestOnly
    } else {
        Write-Warning "未找到 publish.ps1 脚本，使用基本发布流程"
        Invoke-Build
        Invoke-SafeCommand "uv run twine check dist/*" "包检查"
        Invoke-SafeCommand "uv run twine upload --repository testpypi dist/*" "发布到 TestPyPI"
    }
}

# 安装依赖
function Invoke-Install {
    Write-Info "安装依赖..."
    Invoke-SafeCommand "uv sync --all-extras --dev" "依赖安装"
}

# 设置开发环境
function Invoke-DevSetup {
    Write-Info "设置开发环境..."
    
    # 安装依赖
    Invoke-Install
    
    # 安装 pre-commit 钩子
    Invoke-SafeCommand "uv run pre-commit install" "pre-commit 钩子安装" -IgnoreErrors
    Invoke-SafeCommand "uv run pre-commit install --hook-type commit-msg" "commit-msg 钩子安装" -IgnoreErrors
    
    Write-Success "开发环境设置完成！"
    Write-Info "运行 '.\make.ps1 help' 查看可用命令"
}

# 生成文档
function Invoke-Docs {
    Write-Info "生成文档..."
    
    # 清理旧文档
    if (Test-Path "docs/pyutils.rst") { Remove-Item "docs/pyutils.rst" }
    if (Test-Path "docs/modules.rst") { Remove-Item "docs/modules.rst" }
    
    # 生成 API 文档
    Invoke-SafeCommand "uv run sphinx-apidoc -o docs/ src/pyutils" "API 文档生成"
    
    # 构建 HTML 文档
    Push-Location "docs"
    try {
        if (Test-Path "Makefile" -and (Test-Command "make")) {
            Invoke-SafeCommand "make clean" "文档清理"
            Invoke-SafeCommand "make html" "HTML 文档构建"
        } elseif (Test-Path "make.bat") {
            Invoke-SafeCommand "make.bat clean" "文档清理"
            Invoke-SafeCommand "make.bat html" "HTML 文档构建"
        } else {
            Invoke-SafeCommand "uv run sphinx-build -b html . _build/html" "HTML 文档构建"
        }
    } finally {
        Pop-Location
    }
    
    # 打开文档
    $docPath = "docs/_build/html/index.html"
    if (Test-Path $docPath) {
        Write-Info "文档已生成: $docPath"
        if (-not $Force) {
            $open = Read-Host "是否打开文档？(y/N)"
            if ($open -eq 'y' -or $open -eq 'Y') {
                Start-Process $docPath
            }
        }
    }
}

# 运行基准测试
function Invoke-Benchmark {
    Write-Info "运行性能基准测试..."
    
    if (Test-Path "benchmark.py") {
        Invoke-SafeCommand "uv run python benchmark.py" "基准测试"
    } else {
        Write-Warning "未找到 benchmark.py 文件"
    }
}

# 运行安全检查
function Invoke-Security {
    Write-Info "运行安全检查..."
    Invoke-SafeCommand "uv run bandit -r src/" "安全检查" -IgnoreErrors
}

# 运行所有 CI 检查
function Invoke-CI {
    Write-ColorOutput "`n=== 运行所有 CI 检查 ===" -Color 'Magenta'
    
    $steps = @(
        @{ Name = "代码格式化"; Action = { Invoke-Format } },
        @{ Name = "代码风格检查"; Action = { Invoke-Lint } },
        @{ Name = "类型检查"; Action = { Invoke-TypeCheck } },
        @{ Name = "安全检查"; Action = { Invoke-Security } },
        @{ Name = "运行测试"; Action = { 
            Invoke-SafeCommand "uv run pytest tests/ --cov=src --cov-report=term" "测试和覆盖率"
        }}
    )
    
    $stepCount = $steps.Count
    $currentStep = 0
    
    foreach ($step in $steps) {
        $currentStep++
        Write-ColorOutput "`n[$currentStep/$stepCount] $($step.Name)..." -Color 'Yellow'
        
        try {
            & $step.Action
        } catch {
            Write-Error "$($step.Name) 失败: $_"
            if (-not $Force) {
                Write-Error "CI 检查失败！使用 -Force 参数可忽略错误继续执行"
                exit 1
            }
            Write-Warning "强制继续执行..."
        }
    }
    
    Write-ColorOutput "`n✓ 所有 CI 检查完成！" -Color 'Green'
}

# 主执行逻辑
try {
    Write-ColorOutput "Python 项目构建工具 - PowerShell 版本" -Color 'Magenta'
    Write-ColorOutput "项目: mudssky-pyutils" -Color 'Cyan'
    Write-ColorOutput "时间: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -Color 'Cyan'
    Write-Host ""
    
    switch ($Command.ToLower()) {
        'help' { Show-Help }
        'clean' { Invoke-Clean }
        'build' { Invoke-Build }
        'test' { Invoke-Test }
        'lint' { Invoke-Lint }
        'format' { Invoke-Format }
        'type-check' { Invoke-TypeCheck }
        'publish' { Invoke-Publish }
        'publish-test' { Invoke-PublishTest }
        'install' { Invoke-Install }
        'dev-setup' { Invoke-DevSetup }
        'ci' { Invoke-CI }
        'docs' { Invoke-Docs }
        'benchmark' { Invoke-Benchmark }
        'security' { Invoke-Security }
        default { 
            Write-Error "未知命令: $Command"
            Show-Help
            exit 1
        }
    }
    
    Write-ColorOutput "`n操作完成！" -Color 'Green'
    
} catch {
    Write-Error "执行失败: $_"
    exit 1
}