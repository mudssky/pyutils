#!/usr/bin/env python3
# ruff: noqa: S602, T201
"""生成changelog脚本.

用法:
  python scripts/generate-changelog.py                    # 生成自上次tag以来的changelog
  python scripts/generate-changelog.py --from v1.0.0     # 从指定tag生成changelog
  python scripts/generate-changelog.py --all             # 生成完整的changelog
  python scripts/generate-changelog.py --output CHANGELOG.md  # 输出到文件
"""

import argparse
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def run_command(cmd: str, check: bool = True) -> subprocess.CompletedProcess:
    """运行shell命令."""
    result = subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if check and result.returncode != 0:
        print(f"❌ Command failed: {cmd}", file=sys.stderr)
        print(f"Error: {result.stderr}", file=sys.stderr)
        sys.exit(1)
    return result


def get_tags() -> list[str]:
    """获取所有tags, 按版本排序."""
    result = run_command("git tag --sort=-version:refname", check=False)
    if result.returncode != 0 or not result.stdout:
        return []
    return [tag.strip() for tag in result.stdout.split("\n") if tag and tag.strip()]


def get_commits_between(from_ref: str, to_ref: str = "HEAD") -> list[dict[str, str]]:
    """获取两个引用之间的commits,按版本排序."""
    if from_ref:
        commit_range = f"{from_ref}..{to_ref}"
    else:
        commit_range = to_ref

    # 获取commit信息: hash, date, subject, author
    cmd = f'git log --pretty=format:"%H|%ai|%s|%an" {commit_range}'
    result = run_command(cmd, check=False)

    if result.returncode != 0 or not result.stdout or not result.stdout.strip():
        return []

    commits = []
    for line in result.stdout.strip().split("\n"):
        if line and "|" in line:
            parts = line.split("|", 3)
            if len(parts) == 4:
                commits.append(
                    {
                        "hash": parts[0].strip(),
                        "date": parts[1].strip(),
                        "subject": parts[2].strip(),
                        "author": parts[3].strip(),
                    }
                )

    return commits


def categorize_commits(
    commits: list[dict[str, str]],
) -> dict[str, list[dict[str, str]]]:
    """将commits按类型分类."""
    categories = {
        "features": [],
        "fixes": [],
        "docs": [],
        "style": [],
        "refactor": [],
        "perf": [],
        "test": [],
        "build": [],
        "ci": [],
        "chore": [],
        "breaking": [],
        "others": [],
    }

    # 定义commit类型的正则表达式
    patterns = {
        "features": [r"^feat(\(.+\))?:", r"^feature(\(.+\))?:"],
        "fixes": [r"^fix(\(.+\))?:", r"^bugfix(\(.+\))?:"],
        "docs": [r"^docs?(\(.+\))?:"],
        "style": [r"^style(\(.+\))?:"],
        "refactor": [r"^refactor(\(.+\))?:"],
        "perf": [r"^perf(\(.+\))?:", r"^performance(\(.+\))?:"],
        "test": [r"^test(\(.+\))?:"],
        "build": [r"^build(\(.+\))?:"],
        "ci": [r"^ci(\(.+\))?:"],
        "chore": [r"^chore(\(.+\))?:"],
        "breaking": [r"BREAKING CHANGE", r"!:"],
    }

    for commit in commits:
        subject = commit["subject"]
        categorized = False

        # 检查是否为breaking change
        for pattern in patterns["breaking"]:
            if re.search(pattern, subject, re.IGNORECASE):
                categories["breaking"].append(commit)
                categorized = True
                break

        if categorized:
            continue

        # 检查其他类型
        for category, category_patterns in patterns.items():
            if category == "breaking":
                continue

            for pattern in category_patterns:
                if re.match(pattern, subject, re.IGNORECASE):
                    categories[category].append(commit)
                    categorized = True
                    break

            if categorized:
                break

        # 如果没有匹配到任何类型, 归类为others
        if not categorized:
            categories["others"].append(commit)

    return categories


def format_commit(
    commit: dict[str, str], include_hash: bool = True, include_author: bool = False
) -> str:
    """格式化单个commit."""
    subject = commit["subject"]

    # 移除conventional commit前缀以获得更清晰的描述
    clean_subject = re.sub(
        r"^(feat|fix|docs?|style|refactor|perf|test|build|ci|chore)(\(.+\))?:\s*",
        "",
        subject,
        flags=re.IGNORECASE,
    )

    parts = [f"- {clean_subject}"]

    if include_hash:
        short_hash = commit["hash"][:7]
        parts.append(
            f" ([{short_hash}](https://github.com/mudssky/pyutils/commit/{commit['hash']}))"
        )

    if include_author:
        parts.append(f" by {commit['author']}")

    return "".join(parts)


def generate_changelog_section(
    title: str,
    emoji: str,
    commits: list[dict[str, str]],
    include_hash: bool = True,
    include_author: bool = False,
) -> list[str]:
    """生成changelog的一个部分."""
    if not commits:
        return []

    lines = [f"### {emoji} {title}", ""]

    for commit in commits:
        lines.append(format_commit(commit, include_hash, include_author))

    lines.append("")
    return lines


def generate_changelog(
    from_tag: str | None = None,
    to_tag: str = "HEAD",
    include_hash: bool = True,
    include_author: bool = False,
    version: str | None = None,
) -> str:
    """生成changelog."""
    commits = get_commits_between(from_tag, to_tag)

    if not commits:
        return "No commits found in the specified range."

    categories = categorize_commits(commits)

    # 生成标题
    if version:
        title = f"## 🚀 Release {version}"
    elif from_tag and to_tag != "HEAD":
        title = f"## Changes from {from_tag} to {to_tag}"
    elif from_tag:
        title = f"## Changes since {from_tag}"
    else:
        title = "## All Changes"

    lines = [title, ""]

    # 添加发布日期
    if version or to_tag != "HEAD":
        date = datetime.now().strftime("%Y-%m-%d")
        lines.extend([f"*Released on {date}*", ""])

    # 按重要性顺序添加各个部分
    sections = [
        ("Breaking Changes", "💥", categories["breaking"]),
        ("New Features", "✨", categories["features"]),
        ("Bug Fixes", "🐛", categories["fixes"]),
        ("Performance Improvements", "⚡", categories["perf"]),
        ("Documentation", "📚", categories["docs"]),
        ("Code Refactoring", "♻️", categories["refactor"]),
        ("Tests", "🧪", categories["test"]),
        ("Build System", "🏗️", categories["build"]),
        ("CI/CD", "👷", categories["ci"]),
        ("Code Style", "💄", categories["style"]),
        ("Maintenance", "🔧", categories["chore"]),
        ("Other Changes", "📦", categories["others"]),
    ]

    for title, emoji, commits in sections:
        lines.extend(
            generate_changelog_section(
                title, emoji, commits, include_hash, include_author
            )
        )

    # 添加统计信息
    total_commits = len(commits)
    if total_commits > 0:
        lines.extend(["---", "", f"**Total commits**: {total_commits}", ""])

        if from_tag and to_tag == "HEAD":
            lines.append(
                f"**Compare**: https://github.com/mudssky/pyutils/compare/{from_tag}...HEAD"
            )
        elif from_tag and to_tag != "HEAD":
            lines.append(
                f"**Compare**: https://github.com/mudssky/pyutils/compare/{from_tag}...{to_tag}"
            )

        lines.append("")

    return "\n".join(lines)


def generate_full_changelog(
    include_hash: bool = True, include_author: bool = False
) -> str:
    """生成完整的changelog."""
    tags = get_tags()

    if not tags:
        return generate_changelog(None, "HEAD", include_hash, include_author)

    lines = [
        "# Changelog",
        "",
        "All notable changes to this project will be documented in this file.",
        "",
    ]

    # 生成未发布的更改
    unreleased_commits = get_commits_between(tags[0], "HEAD")
    if unreleased_commits:
        lines.append("## [Unreleased]")
        lines.append("")
        unreleased_changelog = generate_changelog(
            tags[0], "HEAD", include_hash, include_author
        )
        # 移除标题行
        unreleased_lines = unreleased_changelog.split("\n")[2:]  # 跳过标题和空行
        lines.extend(unreleased_lines)
        lines.append("")

    # 为每个tag生成changelog
    for i, tag in enumerate(tags):
        version = tag.lstrip("v")

        if i < len(tags) - 1:
            from_tag = tags[i + 1]
        else:
            from_tag = None

        tag_changelog = generate_changelog(
            from_tag, tag, include_hash, include_author, version
        )
        lines.append(tag_changelog)
        lines.append("")

    return "\n".join(lines)


def main():
    """主函数, 解析命令行参数并生成changelog."""
    parser = argparse.ArgumentParser(description="Generate changelog from git commits")

    parser.add_argument(
        "--from", dest="from_tag", help="Generate changelog from this tag/commit"
    )
    parser.add_argument(
        "--to",
        dest="to_tag",
        default="HEAD",
        help="Generate changelog to this tag/commit (default: HEAD)",
    )
    parser.add_argument(
        "--all", action="store_true", help="Generate full changelog for all releases"
    )
    parser.add_argument("--output", "-o", help="Output file (default: stdout)")
    parser.add_argument(
        "--no-hash", action="store_true", help="Don't include commit hashes"
    )
    parser.add_argument(
        "--include-author", action="store_true", help="Include commit authors"
    )
    parser.add_argument("--version", help="Version number for the release")

    args = parser.parse_args()

    try:
        if args.all:
            changelog = generate_full_changelog(
                include_hash=not args.no_hash, include_author=args.include_author
            )
        else:
            # 如果没有指定from_tag, 使用最新的tag
            from_tag = args.from_tag
            if from_tag is None:
                tags = get_tags()
                from_tag = tags[0] if tags else None

            changelog = generate_changelog(
                from_tag=from_tag,
                to_tag=args.to_tag,
                include_hash=not args.no_hash,
                include_author=args.include_author,
                version=args.version,
            )

        if args.output:
            output_path = Path(args.output)
            output_path.write_text(changelog, encoding="utf-8")
            print(f"✅ Changelog written to {output_path}")
        else:
            print(changelog)

    except KeyboardInterrupt:
        print("\n❌ Interrupted by user", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
