.PHONY: clean clean-build clean-pyc clean-test coverage dist docs help install lint test benchmark security pre-commit

.DEFAULT_GOAL := help

define BROWSER_PYSCRIPT
import os, webbrowser, sys

from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
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

BROWSER := uv run python -c "$$BROWSER_PYSCRIPT"

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

release: build ## package and upload a release
	uv run twine upload dist/*

install: ## install the package and dependencies with uv
	uv sync --all-extras --dev

ci: format lint type-check security test-cov ## run all CI checks
	@echo "All CI checks passed!"

dev-setup: install pre-commit ## setup development environment
	@echo "Development environment setup complete!"
	@echo "Run 'make help' to see available commands."

quick-check: format lint type-check ## quick pre-commit checks
	@echo "Quick checks completed!"
