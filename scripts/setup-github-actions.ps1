#!/usr/bin/env pwsh
<#
.SYNOPSIS
    GitHub Actions 配置和验证脚本

.DESCRIPTION
    这个脚本帮助设置和验证 GitHub Actions 工作流配置，包括：
    - 检查必要的文件和配置
    - 验证工作流语法
    - 设置环境和密钥
    - 提供配置指导

.PARAMETER Check
    检查当前配置状态

.PARAMETER Validate
    验证工作流文件语法

.PARAMETER Setup
    交互式设置向导

.PARAMETER Help
    显示详细帮助信息

.EXAMPLE
    ./scripts/setup-github-actions.ps1 -Check
    检查当前 GitHub Actions 配置状态

.EXAMPLE
    ./scripts/setup-github-actions.ps1 -Validate
    验证所有工作流文件语法

.EXAMPLE
    ./scripts/setup-github-actions.ps1 -Setup
    运行交互式设置向导
#>

param(
    [switch]$Check,
    [switch]$Validate,
    [switch]$Setup,
    [switch]$Help
)

# 颜色输出函数
function Write-ColorOutput {
    param(
        [string]$Message,
        [string]$Color = "White"
    )

    $colors = @{
        "Red" = "Red"
        "Green" = "Green"
        "Yellow" = "Yellow"
        "Blue" = "Blue"
        "Magenta" = "Magenta"
        "Cyan" = "Cyan"
        "White" = "White"
    }

    Write-Host $Message -ForegroundColor $colors[$Color]
}

function Write-Success { param([string]$Message) Write-ColorOutput "✅ $Message" "Green" }
function Write-Warning { param([string]$Message) Write-ColorOutput "⚠️  $Message" "Yellow" }
function Write-Error { param([string]$Message) Write-ColorOutput "❌ $Message" "Red" }
function Write-Info { param([string]$Message) Write-ColorOutput "ℹ️  $Message" "Blue" }
function Write-Header { param([string]$Message) Write-ColorOutput "\n🚀 $Message" "Cyan" }

# 检查是否在 Git 仓库中
function Test-GitRepository {
    try {
        git rev-parse --git-dir | Out-Null
        return $true
    }
    catch {
        return $false
    }
}

# 检查工作流文件
function Test-WorkflowFiles {
    Write-Header "检查工作流文件"

    $workflowDir = ".github/workflows"
    $expectedFiles = @(
        "ci.yml",
        "version-bump.yml",
        "pre-release.yml",
        "dependency-update.yml"
    )

    $allExists = $true

    if (-not (Test-Path $workflowDir)) {
        Write-Error "工作流目录不存在: $workflowDir"
        return $false
    }

    foreach ($file in $expectedFiles) {
        $filePath = Join-Path $workflowDir $file
        if (Test-Path $filePath) {
            Write-Success "找到工作流文件: $file"
        } else {
            Write-Error "缺少工作流文件: $file"
            $allExists = $false
        }
    }

    return $allExists
}

# 检查项目配置文件
function Test-ProjectFiles {
    Write-Header "检查项目配置文件"

    $requiredFiles = @(
        "pyproject.toml",
        "src/pyutils/__init__.py",
        ".env.template",
        ".github/GITHUB_ACTIONS_SETUP.md"
    )

    $allExists = $true

    foreach ($file in $requiredFiles) {
        if (Test-Path $file) {
            Write-Success "找到配置文件: $file"
        } else {
            Write-Error "缺少配置文件: $file"
            $allExists = $false
        }
    }

    return $allExists
}

# 验证工作流语法
function Test-WorkflowSyntax {
    Write-Header "验证工作流语法"

    # 检查是否安装了 GitHub CLI
    try {
        gh --version | Out-Null
        $hasGH = $true
    }
    catch {
        $hasGH = $false
        Write-Warning "未安装 GitHub CLI，跳过语法验证"
        Write-Info "安装 GitHub CLI: https://cli.github.com/"
    }

    $workflowDir = ".github/workflows"
    $allValid = $true

    if (Test-Path $workflowDir) {
        $workflowFiles = Get-ChildItem -Path $workflowDir -Filter "*.yml" -File

        foreach ($file in $workflowFiles) {
            Write-Info "检查文件: $($file.Name)"

            # 基本 YAML 语法检查
            try {
                $content = Get-Content $file.FullName -Raw

                # 检查基本的 YAML 结构
                if ($content -match "^name:\s*" -and $content -match "^on:\s*" -and $content -match "^jobs:\s*") {
                    Write-Success "基本结构正确: $($file.Name)"
                } else {
                    Write-Error "基本结构错误: $($file.Name)"
                    $allValid = $false
                }

                # 如果有 GitHub CLI，进行更详细的验证
                if ($hasGH) {
                    $result = gh workflow view $file.FullName 2>&1
                    if ($LASTEXITCODE -eq 0) {
                        Write-Success "语法验证通过: $($file.Name)"
                    } else {
                        Write-Error "语法验证失败: $($file.Name)"
                        Write-Info "错误详情: $result"
                        $allValid = $false
                    }
                }
            }
            catch {
                Write-Error "无法读取文件: $($file.Name)"
                $allValid = $false
            }
        }
    }

    return $allValid
}

# 检查环境配置
function Test-EnvironmentConfig {
    Write-Header "检查环境配置"

    $issues = @()

    # 检查 .env.template
    if (Test-Path ".env.template") {
        $envTemplate = Get-Content ".env.template" -Raw

        $requiredVars = @(
            "TWINE_USERNAME",
            "TWINE_PASSWORD",
            "TWINE_USERNAME_TEST",
            "TWINE_PASSWORD_TEST"
        )

        foreach ($var in $requiredVars) {
            if ($envTemplate -match $var) {
                Write-Success "环境变量模板包含: $var"
            } else {
                Write-Warning "环境变量模板缺少: $var"
                $issues += "缺少环境变量: $var"
            }
        }
    } else {
        Write-Error "缺少 .env.template 文件"
        $issues += "缺少 .env.template 文件"
    }

    # 检查 pyproject.toml 中的项目信息
    if (Test-Path "pyproject.toml") {
        $pyproject = Get-Content "pyproject.toml" -Raw

        if ($pyproject -match 'name\s*=\s*"([^"]+)"') {
            $projectName = $matches[1]
            Write-Success "项目名称: $projectName"
        } else {
            Write-Warning "pyproject.toml 中未找到项目名称"
            $issues += "pyproject.toml 缺少项目名称"
        }

        if ($pyproject -match 'version\s*=\s*"([^"]+)"') {
            $version = $matches[1]
            Write-Success "当前版本: $version"
        } else {
            Write-Warning "pyproject.toml 中未找到版本信息"
            $issues += "pyproject.toml 缺少版本信息"
        }
    }

    return $issues
}

# 检查 GitHub Pages 配置
function Test-GitHubPagesConfig {
    Write-Header "检查 GitHub Pages 配置"

    $issues = @()

    # 检查 docs 目录和配置
    if (Test-Path "docs") {
        Write-Success "找到文档目录: docs"

        # 检查 Sphinx 配置文件
        if (Test-Path "docs/conf.py") {
            Write-Success "找到 Sphinx 配置文件: docs/conf.py"
        } else {
            Write-Warning "缺少 Sphinx 配置文件: docs/conf.py"
            $issues += "缺少 Sphinx 配置文件"
        }

        # 检查文档源文件
        if (Test-Path "docs/index.rst") {
            Write-Success "找到文档首页: docs/index.rst"
        } else {
            Write-Warning "缺少文档首页: docs/index.rst"
            $issues += "缺少文档首页"
        }
    } else {
        Write-Error "缺少文档目录: docs"
        $issues += "缺少文档目录"
    }

    # 检查 CI 工作流中的 Pages 配置
    $ciWorkflow = ".github/workflows/ci.yml"
    if (Test-Path $ciWorkflow) {
        $ciContent = Get-Content $ciWorkflow -Raw

        # 检查 Pages 权限
        if ($ciContent -match "pages:\s*write") {
            Write-Success "CI 工作流包含 Pages 写权限"
        } else {
            Write-Warning "CI 工作流缺少 Pages 写权限"
            $issues += "CI 工作流缺少 Pages 权限"
        }

        # 检查 Pages 部署步骤
        if ($ciContent -match "actions/deploy-pages") {
            Write-Success "CI 工作流包含 Pages 部署步骤"
        } else {
            Write-Warning "CI 工作流缺少 Pages 部署步骤"
            $issues += "CI 工作流缺少 Pages 部署步骤"
        }

        # 检查 Pages 环境配置
        if ($ciContent -match "environment:\s*name:\s*github-pages") {
            Write-Success "CI 工作流包含 Pages 环境配置"
        } else {
            Write-Warning "CI 工作流缺少 Pages 环境配置"
            $issues += "CI 工作流缺少 Pages 环境配置"
        }
    }

    # 检查 GitHub Pages 设置文档
    if (Test-Path ".github/GITHUB_PAGES_SETUP.md") {
        Write-Success "找到 GitHub Pages 设置文档"
    } else {
        Write-Warning "缺少 GitHub Pages 设置文档"
        $issues += "缺少 GitHub Pages 设置文档"
    }

    # 提供配置建议
    if ($issues.Count -eq 0) {
        Write-Success "GitHub Pages 配置完整"
        Write-Info "请确保在 GitHub 仓库设置中启用 Pages (Settings → Pages → GitHub Actions)"
    } else {
        Write-Warning "GitHub Pages 配置不完整，请查看问题列表"
    }

    return $issues
}

# 检查 Git 配置
function Test-GitConfig {
    Write-Header "检查 Git 配置"

    $issues = @()

    # 检查远程仓库
    try {
        $remoteUrl = git remote get-url origin 2>$null
        if ($remoteUrl) {
            Write-Success "Git 远程仓库: $remoteUrl"

            # 检查是否是 GitHub 仓库
            if ($remoteUrl -match "github\.com") {
                Write-Success "检测到 GitHub 仓库"
            } else {
                Write-Warning "不是 GitHub 仓库，某些功能可能不可用"
                $issues += "不是 GitHub 仓库"
            }
        } else {
            Write-Error "未配置 Git 远程仓库"
            $issues += "未配置 Git 远程仓库"
        }
    }
    catch {
        Write-Error "无法获取 Git 远程仓库信息"
        $issues += "Git 配置错误"
    }

    # 检查当前分支
    try {
        $currentBranch = git branch --show-current 2>$null
        if ($currentBranch) {
            Write-Success "当前分支: $currentBranch"
        } else {
            Write-Warning "无法确定当前分支"
        }
    }
    catch {
        Write-Warning "无法获取分支信息"
    }

    return $issues
}

# 生成配置报告
function New-ConfigReport {
    Write-Header "生成配置报告"

    $report = @"
# GitHub Actions 配置报告

生成时间: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')

## 配置状态

"@

    # 检查各个组件
    $workflowStatus = if (Test-WorkflowFiles) { "✅ 完整" } else { "❌ 不完整" }
    $projectStatus = if (Test-ProjectFiles) { "✅ 完整" } else { "❌ 不完整" }
    $envIssues = Test-EnvironmentConfig
    $envStatus = if ($envIssues.Count -eq 0) { "✅ 正常" } else { "⚠️ 有问题" }
    $pagesIssues = Test-GitHubPagesConfig
    $pagesStatus = if ($pagesIssues.Count -eq 0) { "✅ 正常" } else { "⚠️ 有问题" }
    $gitIssues = Test-GitConfig
    $gitStatus = if ($gitIssues.Count -eq 0) { "✅ 正常" } else { "⚠️ 有问题" }

    $report += @"
- **工作流文件**: $workflowStatus
- **项目配置**: $projectStatus
- **环境配置**: $envStatus
- **GitHub Pages**: $pagesStatus
- **Git 配置**: $gitStatus

"@

    if ($envIssues.Count -gt 0) {
        $report += "## 环境配置问题\n\n"
        foreach ($issue in $envIssues) {
            $report += "- $issue\n"
        }
        $report += "\n"
    }

    if ($pagesIssues.Count -gt 0) {
        $report += "## GitHub Pages 配置问题\n\n"
        foreach ($issue in $pagesIssues) {
            $report += "- $issue\n"
        }
        $report += "\n"
    }

    if ($gitIssues.Count -gt 0) {
        $report += "## Git 配置问题\n\n"
        foreach ($issue in $gitIssues) {
            $report += "- $issue\n"
        }
        $report += "\n"
    }

    $report += @"
## 下一步操作

1. 查看 [GITHUB_ACTIONS_SETUP.md](./GITHUB_ACTIONS_SETUP.md) 获取详细配置指南
2. 在 GitHub 仓库中配置 Trusted Publishing
3. 设置环境保护规则
4. 配置分支保护规则
5. 配置 GitHub Pages (Settings → Pages → GitHub Actions)
6. 查看 [GITHUB_PAGES_SETUP.md](./GITHUB_PAGES_SETUP.md) 了解文档部署
7. 测试工作流运行

## 有用的链接

- [GitHub Actions 文档](https://docs.github.com/en/actions)
- [PyPI Trusted Publishing](https://docs.pypi.org/trusted-publishers/)
- [GitHub Pages 文档](https://docs.github.com/en/pages)
- [项目发布指南](./RELEASE_GUIDE.md)
"@

    $reportFile = "github-actions-config-report.md"
    $report | Out-File -FilePath $reportFile -Encoding UTF8
    Write-Success "配置报告已保存到: $reportFile"

    return $reportFile
}

# 交互式设置向导
function Start-SetupWizard {
    Write-Header "GitHub Actions 设置向导"

    Write-Info "这个向导将帮助您配置 GitHub Actions 工作流。"
    Write-Info "请按照提示完成配置。\n"

    # 步骤 1: 检查基础环境
    Write-ColorOutput "步骤 1: 检查基础环境" "Cyan"

    if (-not (Test-GitRepository)) {
        Write-Error "当前目录不是 Git 仓库！"
        Write-Info "请在项目根目录运行此脚本。"
        return
    }

    Write-Success "Git 仓库检查通过"

    # 步骤 2: 检查工作流文件
    Write-ColorOutput "\n步骤 2: 检查工作流文件" "Cyan"

    if (-not (Test-WorkflowFiles)) {
        Write-Warning "工作流文件不完整！"
        $response = Read-Host "是否要查看缺少的文件列表？ (y/n)"
        if ($response -eq 'y' -or $response -eq 'Y') {
            Test-WorkflowFiles
        }
    }

    # 步骤 3: 环境配置
    Write-ColorOutput "\n步骤 3: 环境配置" "Cyan"

    $envIssues = Test-EnvironmentConfig
    if ($envIssues.Count -gt 0) {
        Write-Warning "发现环境配置问题:"
        foreach ($issue in $envIssues) {
            Write-Info "  - $issue"
        }
    }

    # 步骤 4: GitHub Pages 配置
    Write-ColorOutput "\n步骤 4: GitHub Pages 配置" "Cyan"

    $pagesIssues = Test-GitHubPagesConfig
    if ($pagesIssues.Count -gt 0) {
        Write-Warning "发现 GitHub Pages 配置问题:"
        foreach ($issue in $pagesIssues) {
            Write-Info "  - $issue"
        }
        $response = Read-Host "是否要查看 GitHub Pages 设置指南？ (y/n)"
        if ($response -eq 'y' -or $response -eq 'Y') {
            if (Test-Path ".github\GITHUB_PAGES_SETUP.md") {
                Start-Process ".github\GITHUB_PAGES_SETUP.md"
            } else {
                Write-Warning "未找到 GitHub Pages 设置指南文件"
            }
        }
    } else {
        Write-Success "GitHub Pages 配置检查通过"
    }

    # 步骤 5: GitHub 配置指导
    Write-ColorOutput "\n步骤 5: GitHub 配置" "Cyan"

    Write-Info "请在 GitHub 仓库中完成以下配置:"
    Write-Info "  1. 启用 GitHub Actions"
    Write-Info "  2. 配置 PyPI Trusted Publishing"
    Write-Info "  3. 设置环境保护规则"
    Write-Info "  4. 配置分支保护规则"
    Write-Info "  5. 配置 GitHub Pages (Settings → Pages → GitHub Actions)"

    $response = Read-Host "\n是否要打开 GitHub Actions 设置指南？ (y/n)"
    if ($response -eq 'y' -or $response -eq 'Y') {
        if (Test-Path "GITHUB_ACTIONS_SETUP.md") {
            Start-Process "GITHUB_ACTIONS_SETUP.md"
        } else {
            Write-Warning "未找到设置指南文件"
        }
    }

    # 步骤 6: 生成配置报告
    Write-ColorOutput "\n步骤 6: 生成配置报告" "Cyan"

    $reportFile = New-ConfigReport

    $response = Read-Host "\n是否要打开配置报告？ (y/n)"
    if ($response -eq 'y' -or $response -eq 'Y') {
        Start-Process $reportFile
    }

    Write-Success "\n设置向导完成！"
    Write-Info "请查看生成的报告并按照指南完成剩余配置。"
}

# 显示帮助信息
function Show-Help {
    Write-Header "GitHub Actions 配置脚本帮助"

    Write-Info @"
这个脚本帮助您设置和验证 GitHub Actions 工作流配置。

可用参数:
  -Check      检查当前配置状态
  -Validate   验证工作流文件语法
  -Setup      运行交互式设置向导
  -Help       显示此帮助信息

使用示例:
  ./scripts/setup-github-actions.ps1 -Check
  ./scripts/setup-github-actions.ps1 -Validate
  ./scripts/setup-github-actions.ps1 -Setup

工作流文件:
  - ci.yml              主 CI/CD 工作流
  - version-bump.yml    自动版本管理
  - pre-release.yml     预发布工作流
  - dependency-update.yml 依赖更新

更多信息请查看 GITHUB_ACTIONS_SETUP.md
"@
}

# 主函数
function Main {
    if ($Help) {
        Show-Help
        return
    }

    if (-not (Test-GitRepository)) {
        Write-Error "当前目录不是 Git 仓库！"
        Write-Info "请在项目根目录运行此脚本。"
        return
    }

    if ($Check) {
        Write-Header "检查 GitHub Actions 配置"

        Test-WorkflowFiles
        Test-ProjectFiles
        Test-EnvironmentConfig
        Test-GitHubPagesConfig
        Test-GitConfig

        Write-Info "\n检查完成。运行 -Setup 参数获取详细设置向导。"
    }
    elseif ($Validate) {
        Write-Header "验证工作流文件"

        if (Test-WorkflowSyntax) {
            Write-Success "所有工作流文件验证通过！"
        } else {
            Write-Error "工作流文件验证失败，请检查语法错误。"
        }
    }
    elseif ($Setup) {
        Start-SetupWizard
    }
    else {
        Write-Header "GitHub Actions 配置脚本"
        Write-Info "使用 -Help 参数查看可用选项。"
        Write-Info "使用 -Setup 参数运行交互式设置向导。"
    }
}

# 运行主函数
Main
