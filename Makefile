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

ALLURE_RESULT_FOLDER := ./deployments/data/allure-results
TEST_SEED_DATA_FOLDER := ./tests/seed_data
TEST_GENERATE_DATA_FILE := $(TEST_SEED_DATA_FOLDER)/test_generate_all_data.py
TEST_CREATE_DATA_FILE := $(TEST_SEED_DATA_FOLDER)/test_create_all_data.py
TEST_CLEAR_DATA_FILE := $(TEST_SEED_DATA_FOLDER)/test_clear_all_data.py

# command
POETRY_RUN := poetry run
DOCKER_COMPOSE := docker compose

# Start the application
run:
	$(POETRY_RUN) uvicorn $(APP_NAME).main:$(MAIN_NAME) --reload --port $(PORT)

# Install project dependencies
install:
	poetry install

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
	make pytest-clear-data
	make pytest-create-data
	$(POETRY_RUN) pytest -v --tb=short --no-header --no-summary --strict-markers -ra --clean-alluredir --alluredir=$(ALLURE_RESULT_FOLDER) --ignore=$(TEST_SEED_DATA_FOLDER)
	make pytest-clear-data

# Pytest: generate data json
pytest-generate-data:
	$(POETRY_RUN) pytest $(TEST_GENERATE_DATA_FILE) -v

# Pytest: create data in db pytest
pytest-create-data:
	$(POETRY_RUN) pytest $(TEST_CREATE_DATA_FILE) -v

# Pytest: clear data in db pytest
pytest-clear-data:
	$(POETRY_RUN) pytest $(TEST_CLEAR_DATA_FILE) -v

check-all: lint-check alembic-check opa-check pytest
	@echo All checks passed!

# Clean up cache and temporary files
clean:
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete
ifeq ($(OS), Windows)
	del /s /q *.pyc
	del /s /q __pycache__
endif
