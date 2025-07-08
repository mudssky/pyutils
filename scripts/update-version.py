#!/usr/bin/env python3
# ruff: noqa: T201
"""版本更新脚本 - 用于semantic-release自动更新版本号.

此脚本被semantic-release调用,用于更新项目中的版本号。
支持更新:
- pyproject.toml 中的版本号
- src/pyutils/__init__.py 中的 __version__ 变量
"""

import re
import sys
from pathlib import Path


def update_pyproject_toml(version: str, project_root: Path) -> None:
    """更新 pyproject.toml 中的版本号."""
    pyproject_path = project_root / "pyproject.toml"

    if not pyproject_path.exists():
        print(f"警告: {pyproject_path} 不存在")
        return

    content = pyproject_path.read_text(encoding="utf-8")

    # 使用正则表达式替换版本号
    pattern = r'version\s*=\s*"[^"]*"'
    replacement = f'version = "{version}"'

    new_content = re.sub(pattern, replacement, content)

    if new_content != content:
        pyproject_path.write_text(new_content, encoding="utf-8")
        print(f"✅ 已更新 pyproject.toml 版本号为: {version}")
    else:
        print("⚠️  pyproject.toml 中未找到版本号模式")


def update_init_py(version: str, project_root: Path) -> None:
    """更新 __init__.py 中的 __version__ 变量."""
    init_path = project_root / "src" / "pyutils" / "__init__.py"

    if not init_path.exists():
        print(f"警告: {init_path} 不存在")
        return

    content = init_path.read_text(encoding="utf-8")

    # 使用正则表达式替换版本号
    pattern = r'__version__\s*=\s*["\'][^"\']*["\']'
    replacement = f'__version__ = "{version}"'

    new_content = re.sub(pattern, replacement, content)

    if new_content != content:
        init_path.write_text(new_content, encoding="utf-8")
        print(f"✅ 已更新 __init__.py 版本号为: {version}")
    else:
        print("⚠️  __init__.py 中未找到版本号模式")


def main():
    """主函数."""
    if len(sys.argv) != 2:
        print("用法: python update-version.py <version>")
        print("示例: python update-version.py 1.2.3")
        sys.exit(1)

    version = sys.argv[1]
    project_root = Path(__file__).parent.parent

    print(f"🚀 开始更新版本号为: {version}")
    print(f"📁 项目根目录: {project_root}")

    # 验证版本号格式 (简单的语义化版本检查)
    version_pattern = r"^\d+\.\d+\.\d+(?:-[a-zA-Z0-9.-]+)?(?:\+[a-zA-Z0-9.-]+)?$"
    if not re.match(version_pattern, version):
        print(f"❌ 无效的版本号格式: {version}")
        print("版本号应符合语义化版本规范,如: 1.2.3, 1.2.3-beta.1, 1.2.3+build.1")
        sys.exit(1)

    try:
        # 更新版本号
        update_pyproject_toml(version, project_root)
        update_init_py(version, project_root)

        print(f"🎉 版本号更新完成: {version}")

    except Exception as e:
        print(f"❌ 更新版本号时发生错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
