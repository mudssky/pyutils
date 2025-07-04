# Windows PowerShell 构建脚本
# 用于在 Windows 系统上构建 Python 包

Write-Host "开始清理构建目录..." -ForegroundColor Green

# 清理构建目录
if (Test-Path "build") {
    Remove-Item -Recurse -Force "build"
    Write-Host "已删除 build 目录"
}

if (Test-Path "dist") {
    Remove-Item -Recurse -Force "dist"
    Write-Host "已删除 dist 目录"
}

if (Test-Path ".eggs") {
    Remove-Item -Recurse -Force ".eggs"
    Write-Host "已删除 .eggs 目录"
}

# 清理 egg-info 文件
Get-ChildItem -Recurse -Name "*.egg-info" | ForEach-Object {
    if (Test-Path $_) {
        Remove-Item -Recurse -Force $_
        Write-Host "已删除 $_"
    }
}

# 清理 egg 文件
Get-ChildItem -Recurse -Name "*.egg" | ForEach-Object {
    if (Test-Path $_) {
        Remove-Item -Force $_
        Write-Host "已删除 $_"
    }
}

# 清理 Python 缓存文件
Get-ChildItem -Recurse -Name "__pycache__" | ForEach-Object {
    if (Test-Path $_) {
        Remove-Item -Recurse -Force $_
        Write-Host "已删除 $_"
    }
}

Get-ChildItem -Recurse -Name "*.pyc" | ForEach-Object {
    if (Test-Path $_) {
        Remove-Item -Force $_
        Write-Host "已删除 $_"
    }
}

Get-ChildItem -Recurse -Name "*.pyo" | ForEach-Object {
    if (Test-Path $_) {
        Remove-Item -Force $_
        Write-Host "已删除 $_"
    }
}

Write-Host "清理完成！" -ForegroundColor Green
Write-Host "开始构建包..." -ForegroundColor Green

# 构建包
try {
    uv build
    Write-Host "构建成功！" -ForegroundColor Green
    
    # 显示构建结果
    if (Test-Path "dist") {
        Write-Host "构建文件列表：" -ForegroundColor Yellow
        Get-ChildItem "dist" | ForEach-Object {
            $size = [math]::Round($_.Length / 1KB, 2)
            Write-Host "  $($_.Name) ($size KB)" -ForegroundColor Cyan
        }
    }
} catch {
    Write-Host "构建失败：$_" -ForegroundColor Red
    exit 1
}

Write-Host "构建完成！" -ForegroundColor Green