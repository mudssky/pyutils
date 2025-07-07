.PHONY: clean clean-build clean-pyc clean-test coverage dist docs help install lint test benchmark security pre-commit

.DEFAULT_GOAL := help

define BROWSER_PYSCRIPT
import os, webbrowser, sys; from urllib.request import pathname2url; webbrowser.open('file://' + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

BROWSER := uv run python -c "$(BROWSER_PYSCRIPT)"

help:
	@uv run python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache

lint: ## check code style with ruff
	uv run ruff check src/ tests/

format: ## format code with ruff
	uv run ruff format src/ tests/
	uv run ruff check --fix src/ tests/

type-check: ## run type checking with mypy
	uv run mypy src/

security: ## run security checks with bandit
	uv run bandit -r src/

test: ## run tests quickly with pytest
	uv run pytest tests/

test-cov: ## run tests with coverage
	uv run pytest --cov=src --cov-report=html --cov-report=term
	$(BROWSER) htmlcov/index.html

benchmark: ## run performance benchmarks
	uv run python benchmark.py

pre-commit: ## install pre-commit hooks
	uv run pre-commit install
	uv run pre-commit install --hook-type commit-msg

docs: ## generate Sphinx HTML documentation, including API docs
	rm -f docs/pyutils.rst
	rm -f docs/modules.rst
	uv run sphinx-apidoc -o docs/ src/pyutils
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	$(BROWSER) docs/_build/html/index.html

servedocs: docs ## compile the docs watching for changes
	uv run watchmedo shell-command -p '*.rst' -c '$(MAKE) -C docs html' -R -D .

build: clean ## builds source and wheel package with uv
	uv build
	ls -l dist

release: build ## package and upload a release (manual)
	uv run twine upload dist/*

# Release automation commands
changelog: ## generate changelog from git commits
	python scripts/generate-changelog.py

changelog-file: ## generate changelog and save to CHANGELOG.md
	python scripts/generate-changelog.py --all --output CHANGELOG.md
	@echo "Changelog saved to CHANGELOG.md"

release-dry: ## dry run release (patch version)
	@echo "Dry run release (patch version)..."
	python scripts/create-release.py --patch --dry-run

release-patch: ## release patch version (x.x.X) and push tag
	@echo "Releasing patch version..."
	python scripts/create-release.py --patch --push
	@echo "Patch release completed!"

release-minor: ## release minor version (x.X.0) and push tag
	@echo "Releasing minor version..."
	python scripts/create-release.py --minor --push
	@echo "Minor release completed!"

release-major: ## release major version (X.0.0) and push tag
	@echo "Releasing major version..."
	python scripts/create-release.py --major --push
	@echo "Major release completed!"

release-version: ## release specific version (usage: make release-version VERSION=1.2.3)
	@if [ -z "$(VERSION)" ]; then \
		echo "Error: VERSION is required. Usage: make release-version VERSION=1.2.3"; \
		exit 1; \
	fi
	@echo "Releasing version $(VERSION)..."
	python scripts/create-release.py --version $(VERSION) --push
	@echo "Version $(VERSION) release completed!"

# Git and CI helpers
version: ## show current version
	@echo "Current version:"
	@grep 'version =' pyproject.toml | head -1
	@grep '__version__' src/pyutils/__init__.py

ci-status: ## show CI/CD status
	@echo "CI/CD runs:"
	gh run list --limit 5

ci-logs: ## show latest CI/CD logs
	@echo "Latest CI/CD logs:"
	gh run view

tags: ## show git tags
	@echo "Git tags:"
	git tag --sort=-version:refname

release-help: ## show release command help
	@echo "🚀 发布命令帮助:"
	@echo ""
	@echo "📦 Semantic Release (推荐):"
	@echo "  make semantic-release     - 使用semantic-release自动发布"
	@echo "  make semantic-release-dry - 预览semantic-release发布"
	@echo ""
	@echo "🔧 传统发布方式:"
	@echo "  make release-dry     - Preview what will be released (patch)"
	@echo "  make release-patch   - Release patch version (1.0.0 -> 1.0.1)"
	@echo "  make release-minor   - Release minor version (1.0.0 -> 1.1.0)"
	@echo "  make release-major   - Release major version (1.0.0 -> 2.0.0)"
	@echo "  make release-version VERSION=x.y.z - Release specific version"
	@echo ""
	@echo "Examples:"
	@echo "  make release-version VERSION=1.2.3"
	@echo "  make release-patch"
	@echo "  make semantic-release"
	@echo ""
	@echo "Note: All release commands will push tags and trigger CI/CD"

semantic-release: ## run semantic-release for automated versioning and publishing
	@echo "🚀 使用semantic-release自动发布..."
	@if ! command -v npm >/dev/null 2>&1; then \
		echo "❌ 错误: npm未安装，请先安装Node.js和npm"; \
		exit 1; \
	fi
	@if [ ! -f package.json ]; then \
		echo "❌ 错误: package.json不存在"; \
		exit 1; \
	fi
	npm install
	npx semantic-release

semantic-release-dry: ## preview semantic-release without publishing
	@echo "🔍 预览semantic-release发布..."
	@if ! command -v npm >/dev/null 2>&1; then \
		echo "❌ 错误: npm未安装，请先安装Node.js和npm"; \
		exit 1; \
	fi
	@if [ ! -f package.json ]; then \
		echo "❌ 错误: package.json不存在"; \
		exit 1; \
	fi
	npm install
	npx semantic-release --dry-run

install: ## install the package and dependencies with uv
	uv sync --all-extras --dev

ci: format lint type-check security test-cov ## run all CI checks
	@echo "All CI checks passed!"

dev-setup: install pre-commit ## setup development environment
	@echo "Development environment setup complete!"
	@echo "Run 'make help' to see available commands."

quick-check: format lint type-check ## quick pre-commit checks
	@echo "Quick checks completed!"
