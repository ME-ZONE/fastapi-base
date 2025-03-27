# Application settings
APP_NAME := app
MAIN_NAME := app
PORT := 8000

ENV_FILE := .env.dev
DOCKER_FILE := ./deployments/docker-compose.dev.yml
DOCKER_PYTEST_FILE := ./deployments/docker-compose.pytest.dev.yml

ALEMBIC_HISTORY_FILE_CHECK := ./migrations/check_alembic.ps1
ALEMBIC_ENUM_FILE_CHECK=./migrations/check_alembic_enum.py
ALEMBIC_ENUM_FOLDER_CHECK=./migrations/versions

OPA_FILE := ./$(APP_NAME)/opa/opa.exe
OPA_RULE_FOLDER := ./$(APP_NAME)/opa/rules
OPA_REGAL_FILE := ./$(APP_NAME)/opa/regal.exe
OPA_REGAL_CONFIG := ./$(APP_NAME)/opa/regal.yml

TEST_TOOL_FOLDER := ./tests/tools
TEST_TOOL_MANAGE_FILE := $(TEST_TOOL_FOLDER)/manage.py
TEST_TOOL_MODEL_FOLDER := $(TEST_TOOL_FOLDER)/ui/models
TEST_TOOL_LIST_DB_TABLES_FILE := $(TEST_TOOL_FOLDER)/list_db_tables.py
TEST_TOOL_FIX_MODEL_FILE := $(TEST_TOOL_FOLDER)/fix_model.py
ALLURE_RESULT_FOLDER := ./deployments/data/allure-results

# command
POETRY_RUN := poetry run
DOCKER_COMPOSE := docker compose

# Start the application
run:
	$(POETRY_RUN) uvicorn $(APP_NAME).main:$(MAIN_NAME) --reload --port $(PORT)

# Install project dependencies
install:
	poetry install

# Install main dependencies
install-main:
	poetry install --no-dev

# Install dev dependencies
install-dev:
	poetry install --with dev

# Ruff: Check code issues with Ruff
lint-check:
	$(POETRY_RUN) ruff check .

# Ruff: Auto-fix issues using Ruff
lint-fix:
	$(POETRY_RUN) ruff check --fix .

# Docker: Build Docker compose
docker-build:
	$(DOCKER_COMPOSE) -f $(DOCKER_FILE) --env-file $(ENV_FILE) up --build -d

# Docker: Build Docker pytest compose
docker-pytest-build:
	$(DOCKER_COMPOSE) -f $(DOCKER_PYTEST_FILE) --env-file $(ENV_FILE) up --build -d

# Celery: Start Celery worker
celery-worker:
	$(POETRY_RUN) celery --app=$(APP_NAME).services.celery_service worker -l info

# Alembic: Generate automatic migration
alembic-migrate:
	$(POETRY_RUN) alembic revision --autogenerate -m "$(filter-out $@,$(MAKECMDGOALS))"

# Alembic: Generate an empty migration
alembic-migrate-empty:
	$(POETRY_RUN) alembic revision -m "$(filter-out $@,$(MAKECMDGOALS))"

# Alembic: Upgrade to the latest migration
alembic-upgrade:
	$(POETRY_RUN) alembic upgrade head

# Alembic: Downgrade to the previous migration
alembic-downgrade:
	$(POETRY_RUN) alembic downgrade -1

# Alembic: Downgrade to a specific revision
alembic-downgrade-to:
	$(POETRY_RUN) alembic downgrade $(filter-out $@,$(MAKECMDGOALS))

# Alembic: History
alembic-history:
	$(POETRY_RUN) alembic history

# Alembic: Check for multiple heads
alembic-check:
	@python $(ALEMBIC_ENUM_FILE_CHECK) $(ALEMBIC_ENUM_FOLDER_CHECK)
	@powershell -NoProfile -ExecutionPolicy Bypass -File "$(ALEMBIC_HISTORY_FILE_CHECK)"

# OPA: linter
opa-check:
	$(OPA_REGAL_FILE) lint -c $(OPA_REGAL_CONFIG) $(OPA_RULE_FOLDER)

# OPA: format
opa-format:
	$(OPA_FILE) fmt $(OPA_RULE_FOLDER) --write
	@echo OPA format success!

# Pytest: Run tests using Pytest
pytest:
	$(POETRY_RUN) pytest -v --tb=short --no-header --no-summary --strict-markers -ra --clean-alluredir --alluredir=$(ALLURE_RESULT_FOLDER)

# Pytest: Run tool
pytest-tool:
	python $(TEST_TOOL_MANAGE_FILE) runserver

# Pytest: Setup tool
pytest-tool-admin:
	python $(TEST_TOOL_MANAGE_FILE) migrate
	python $(TEST_TOOL_MANAGE_FILE) createsuperuser

# Pytest: List table from database
pytest-tool-list-tables:
	python $(TEST_TOOL_LIST_DB_TABLES_FILE)

# Pytest: Insect table from database
pytest-tool-inspectdb:
	@chcp 65001 >nul & \
	@if "$(TABLE)"=="" ( \
		echo Vui lòng cung cấp tên bảng. Ví dụ: make pytest-tool-inspectdb TABLE=pcs_users & exit /b 1 \
	) else ( \
		echo Inspecting table: $(TABLE) & \
		python $(TEST_TOOL_MANAGE_FILE) inspectdb $(TABLE) > $(TEST_TOOL_MODEL_FOLDER)/$(TABLE).py & \
		python $(TEST_TOOL_FIX_MODEL_FILE) \
	)

check-all: lint-check alembic-check opa-check pytest
	@echo All checks passed!

# Clean up cache and temporary files
clean:
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete
