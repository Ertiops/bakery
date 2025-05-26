PROJECT_NAME = challenge_bot
TEST_PATH = ./tests

PIP = .venv/bin/pip
POETRY = .venv/bin/poetry
PYTEST = .venv/bin/pytest
COVERAGE = .venv/bin/coverage
RUFF = .venv/bin/ruff
MYPY = .venv/bin/mypy


.PHONY: help lint develop clean_dev test ruff mypy clean_dev clean_pycache app

help:  ## Show this help
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*##' $(MAKEFILE_LIST) | sed 's/:.*##/ /'

lint:  ## Lint project code.
	$(POETRY) run $(RUFF) check --fix .

develop: clean_dev  ## Create project virtual environment
	python3.12 -m venv .venv
	$(PIP) install -U pip poetry
	$(POETRY) config virtualenvs.create false
	$(POETRY) install
	$(POETRY) run pre-commit install

test: ## Run tests
	$(POETRY) run $(PYTEST) -vx $(TEST_PATH)

ruff: ## Run ruff linter
	$(POETRY) run $(RUFF) check ./$(PROJECT_NAME)

mypy: ## Run mypy type checker
	$(POETRY) run $(MYPY) ./$(PROJECT_NAME)

clean_dev: ## Clean up development environment
	rm -rf .venv/

clean_pycache: ## Remove Python cache directories
	find . -type d -name __pycache__ -exec rm -r {} \+

app: ## Start the bot application
	.venv/bin/python -m challenge_bot


prod: ## Suild and start production image
	docker-compose up --build -d

logs: ## Show container logs
	docker-compose logs -f
