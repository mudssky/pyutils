#!/usr/bin/env python3
"""
自动化发布脚本

用法:
  python scripts/create-release.py --version 1.0.0 [--dry-run] [--push]
  python scripts/create-release.py --patch [--dry-run] [--push]  # 自动递增补丁版本
  python scripts/create-release.py --minor [--dry-run] [--push]  # 自动递增次版本
  python scripts/create-release.py --major [--dry-run] [--push]  # 自动递增主版本
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path
from typing import Optional, Tuple


def run_command(cmd: str, check: bool = True) -> subprocess.CompletedProcess:
    """运行shell命令"""
    print(f"🔧 Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding='utf-8', errors='replace')
    if check and result.returncode != 0:
        print(f"❌ Command failed: {cmd}")
        print(f"Error: {result.stderr}")
        sys.exit(1)
    return result


def get_current_version() -> str:
    """从pyproject.toml获取当前版本"""
    pyproject_path = Path("pyproject.toml")
    if not pyproject_path.exists():
        print("❌ pyproject.toml not found")
        sys.exit(1)
    
    content = pyproject_path.read_text(encoding="utf-8")
    match = re.search(r'version = "([^"]+)"', content)
    if not match:
        print("❌ Version not found in pyproject.toml")
        sys.exit(1)
    
    return match.group(1)


def parse_version(version: str) -> Tuple[int, int, int]:
    """解析版本号"""
    match = re.match(r'^(\d+)\.(\d+)\.(\d+)', version)
    if not match:
        print(f"❌ Invalid version format: {version}")
        sys.exit(1)
    
    return int(match.group(1)), int(match.group(2)), int(match.group(3))


def increment_version(current: str, bump_type: str) -> str:
    """递增版本号"""
    major, minor, patch = parse_version(current)
    
    if bump_type == "major":
        return f"{major + 1}.0.0"
    elif bump_type == "minor":
        return f"{major}.{minor + 1}.0"
    elif bump_type == "patch":
        return f"{major}.{minor}.{patch + 1}"
    else:
        raise ValueError(f"Invalid bump type: {bump_type}")


def update_version_files(version: str, dry_run: bool = False) -> None:
    """更新版本文件"""
    files_to_update = [
        ("pyproject.toml", r'version = "[^"]+"', f'version = "{version}"'),
        ("src/pyutils/__init__.py", r'__version__ = "[^"]+"', f'__version__ = "{version}"'),
    ]
    
    for file_path, pattern, replacement in files_to_update:
        path = Path(file_path)
        if not path.exists():
            print(f"⚠️  File not found: {file_path}")
            continue
        
        content = path.read_text(encoding="utf-8")
        new_content = re.sub(pattern, replacement, content)
        
        if content != new_content:
            print(f"📝 Updating {file_path}")
            if not dry_run:
                path.write_text(new_content, encoding="utf-8")
        else:
            print(f"ℹ️  No changes needed in {file_path}")


def check_git_status() -> None:
    """检查git状态"""
    result = run_command("git status --porcelain")
    if result.stdout.strip():
        print("❌ Working directory is not clean. Please commit or stash changes.")
        print("Uncommitted changes:")
        print(result.stdout)
        sys.exit(1)
    print("✅ Working directory is clean")


def check_branch() -> None:
    """检查当前分支"""
    result = run_command("git branch --show-current")
    branch = result.stdout.strip()
    if branch != "main":
        print(f"⚠️  Current branch is '{branch}', not 'main'")
        response = input("Continue anyway? (y/N): ")
        if response.lower() != 'y':
            sys.exit(1)
    else:
        print("✅ On main branch")


def generate_changelog(version: str) -> str:
    """生成changelog"""
    print("📋 Generating changelog...")
    
    # 获取上一个tag
    result = run_command("git tag --sort=-version:refname", check=False)
    tags = [tag.strip() for tag in result.stdout.split('\n') if tag.strip()]
    
    if tags:
        previous_tag = tags[0]
        commit_range = f"{previous_tag}..HEAD"
        print(f"📊 Comparing {previous_tag} to HEAD")
    else:
        # 第一个release
        commit_range = "HEAD"
        print("📊 First release, including all commits")
    
    # 获取commit信息
    result = run_command(f'git log --pretty=format:"%s" {commit_range}')
    commits = [commit.strip() for commit in result.stdout.split('\n') if commit.strip()]
    
    if not commits:
        return f"## Release {version}\n\nNo changes since last release."
    
    # 分类commits
    features = []
    fixes = []
    docs = []
    others = []
    
    for commit in commits:
        if commit.startswith(('feat', 'feature')):
            features.append(commit)
        elif commit.startswith(('fix', 'bugfix')):
            fixes.append(commit)
        elif commit.startswith('docs'):
            docs.append(commit)
        else:
            others.append(commit)
    
    # 生成changelog
    changelog = [f"## 🚀 Release {version}", ""]
    
    if features:
        changelog.extend(["### ✨ New Features", ""])
        changelog.extend([f"- {commit}" for commit in features])
        changelog.append("")
    
    if fixes:
        changelog.extend(["### 🐛 Bug Fixes", ""])
        changelog.extend([f"- {commit}" for commit in fixes])
        changelog.append("")
    
    if docs:
        changelog.extend(["### 📚 Documentation", ""])
        changelog.extend([f"- {commit}" for commit in docs])
        changelog.append("")
    
    if others:
        changelog.extend(["### 🔧 Other Changes", ""])
        changelog.extend([f"- {commit}" for commit in others[:10]])  # 限制显示数量
        changelog.append("")
    
    return "\n".join(changelog)


def create_tag_and_push(version: str, dry_run: bool = False, push: bool = False) -> None:
    """创建tag并推送"""
    tag_name = f"v{version}"
    
    if dry_run:
        print(f"🏷️  Would create tag: {tag_name}")
        if push:
            print(f"📤 Would push tag: {tag_name}")
        return
    
    # 创建tag
    changelog = generate_changelog(version)
    print(f"🏷️  Creating tag: {tag_name}")
    
    # 将changelog写入临时文件
    changelog_file = Path(".tag_message.tmp")
    changelog_file.write_text(changelog, encoding="utf-8")
    
    try:
        run_command(f'git tag -a {tag_name} -F ".tag_message.tmp"')
        print(f"✅ Tag {tag_name} created")
        
        if push:
            print(f"📤 Pushing tag: {tag_name}")
            run_command(f"git push origin {tag_name}")
            print(f"✅ Tag {tag_name} pushed to origin")
            print(f"🚀 GitHub Actions will now build and publish the release")
        else:
            print(f"ℹ️  Tag created locally. Use --push to push to origin")
            print(f"ℹ️  Or run: git push origin {tag_name}")
    
    finally:
        # 清理临时文件
        if changelog_file.exists():
            changelog_file.unlink()


def main():
    parser = argparse.ArgumentParser(description="Create a new release")
    
    # 版本选项
    version_group = parser.add_mutually_exclusive_group(required=True)
    version_group.add_argument("--version", help="Specific version to release (e.g., 1.0.0)")
    version_group.add_argument("--patch", action="store_true", help="Increment patch version")
    version_group.add_argument("--minor", action="store_true", help="Increment minor version")
    version_group.add_argument("--major", action="store_true", help="Increment major version")
    
    # 其他选项
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done without making changes")
    parser.add_argument("--push", action="store_true", help="Push the tag to origin (triggers CI/CD)")
    parser.add_argument("--skip-checks", action="store_true", help="Skip git status and branch checks")
    
    args = parser.parse_args()
    
    print("🚀 Starting release process...")
    
    # 检查git状态
    if not args.skip_checks:
        check_git_status()
        check_branch()
    
    # 确定版本
    current_version = get_current_version()
    print(f"📋 Current version: {current_version}")
    
    if args.version:
        new_version = args.version
    elif args.patch:
        new_version = increment_version(current_version, "patch")
    elif args.minor:
        new_version = increment_version(current_version, "minor")
    elif args.major:
        new_version = increment_version(current_version, "major")
    
    print(f"🎯 Target version: {new_version}")
    
    # 更新版本文件
    if current_version != new_version:
        update_version_files(new_version, args.dry_run)
        
        if not args.dry_run:
            # 提交版本更改
            run_command("git add pyproject.toml src/pyutils/__init__.py")
            run_command(f'git commit -m "chore: bump version to {new_version}"')
            print(f"✅ Version updated and committed")
    
    # 创建tag
    create_tag_and_push(new_version, args.dry_run, args.push)
    
    if not args.dry_run:
        print(f"\n🎉 Release {new_version} process completed!")
        if args.push:
            print(f"🔗 Check the GitHub Actions workflow: https://github.com/mudssky/pyutils/actions")
            print(f"📦 PyPI package will be available at: https://pypi.org/project/mudssky-pyutils/{new_version}/")
        else:
            print(f"ℹ️  To trigger the release, push the tag: git push origin v{new_version}")
    else:
        print(f"\n🔍 Dry run completed. Use --push to actually create and push the tag.")


if __name__ == "__main__":
    main()