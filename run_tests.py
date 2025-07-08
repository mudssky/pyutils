#!/usr/bin/env python
# ruff: noqa: S603, T201

"""Test runner script for pyutils project."""

import argparse
import subprocess
import sys
from pathlib import Path


def run_command(cmd, description):
    """Run a command and handle errors."""
    print(f"\n{'=' * 60}")
    print(f"Running: {description}")
    print(f"Command: {' '.join(cmd)}")
    print(f"{'=' * 60}")

    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        return True
    except subprocess.CalledProcessError as e:
        print(f"ERROR: {description} failed with exit code {e.returncode}")
        print("STDOUT:", e.stdout)
        print("STDERR:", e.stderr)
        return False
    except FileNotFoundError:
        print("ERROR: Command not found. Make sure the required tools are installed.")
        return False


def main():
    """Main test runner function."""
    parser = argparse.ArgumentParser(description="Run tests for pyutils project")
    parser.add_argument(
        "--quick", action="store_true", help="Run quick tests only (skip slow tests)"
    )
    parser.add_argument(
        "--coverage", action="store_true", help="Run tests with coverage report"
    )
    parser.add_argument(
        "--module",
        type=str,
        help="Run tests for specific module (e.g., array, string, math)",
    )
    parser.add_argument(
        "--verbose", action="store_true", help="Run tests with verbose output"
    )
    parser.add_argument("--parallel", action="store_true", help="Run tests in parallel")
    parser.add_argument("--lint", action="store_true", help="Run linting checks")
    parser.add_argument("--type-check", action="store_true", help="Run type checking")
    parser.add_argument(
        "--all",
        action="store_true",
        help="Run all checks (tests, linting, type checking)",
    )

    args = parser.parse_args()

    # Change to project root directory
    project_root = Path(__file__).parent
    print(f"Project root: {project_root.absolute()}")

    success = True

    # Build pytest command
    if args.all or not any([args.lint, args.type_check]):
        pytest_cmd = [sys.executable, "-m", "pytest"]

        if args.quick:
            pytest_cmd.extend(["-m", "not slow"])

        if args.coverage:
            pytest_cmd.extend(
                [
                    "--cov=src/pyutils",
                    "--cov-report=term-missing",
                    "--cov-report=html:htmlcov",
                    "--cov-fail-under=90",
                ]
            )

        if args.module:
            pytest_cmd.append(f"tests/test_{args.module}.py")

        if args.verbose:
            pytest_cmd.append("-v")

        if args.parallel:
            pytest_cmd.extend(["-n", "auto"])

        # Add asyncio mode
        pytest_cmd.append("--asyncio-mode=auto")

        success &= run_command(pytest_cmd, "Running pytest")

    # Run linting checks
    if args.lint or args.all:
        # Ruff check
        ruff_cmd = [sys.executable, "-m", "ruff", "check", "src", "tests"]
        success &= run_command(ruff_cmd, "Running Ruff linting")

        # Ruff format check
        ruff_format_cmd = [
            sys.executable,
            "-m",
            "ruff",
            "format",
            "--check",
            "src",
            "tests",
        ]
        success &= run_command(ruff_format_cmd, "Checking code formatting")

    # Run type checking
    if args.type_check or args.all:
        mypy_cmd = [sys.executable, "-m", "mypy", "src/pyutils"]
        success &= run_command(mypy_cmd, "Running MyPy type checking")

    # Summary
    print(f"\n{'=' * 60}")
    if success:
        print("✅ All checks passed successfully!")

        if args.coverage:
            print("\n📊 Coverage report generated:")
            print("  - Terminal: See output above")
            print("  - HTML: Open htmlcov/index.html in your browser")
            print("  - XML: coverage.xml")

        print("\n🎉 Your code is ready for production!")
    else:
        print("❌ Some checks failed. Please review the output above.")
        sys.exit(1)

    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
