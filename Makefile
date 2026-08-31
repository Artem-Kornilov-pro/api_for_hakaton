.PHONY: help install install-dev run lint lint-fix format format-check typecheck check \
	docker-build docker-up docker-down docker-logs load-test clean

PYTHON ?= python3
VENV ?= .venv
PIP := $(VENV)/bin/pip
PY := $(VENV)/bin/python

help:
	@echo "Доступные команды:"
	@echo "  make install       - создать venv и установить зависимости проекта"
	@echo "  make install-dev   - установить зависимости для разработки (ruff, mypy, locust)"
	@echo "  make run           - запустить API локально (uvicorn, порт 8085)"
	@echo "  make lint          - проверить код линтером ruff"
	@echo "  make lint-fix      - исправить автоисправимые замечания ruff"
	@echo "  make format        - отформатировать код ruff format"
	@echo "  make format-check  - проверить форматирование без изменений"
	@echo "  make typecheck     - проверить типы через mypy"
	@echo "  make check         - lint + typecheck (быстрая проверка перед коммитом)"
	@echo "  make docker-build  - собрать Docker-образ"
	@echo "  make docker-up     - запустить проект в Docker (docker compose up -d)"
	@echo "  make docker-down   - остановить Docker-контейнеры"
	@echo "  make docker-logs   - показать логи контейнера"
	@echo "  make load-test     - нагрузочное тестирование через locust"
	@echo "  make clean         - удалить venv и кэши Python"

$(VENV)/bin/activate:
	$(PYTHON) -m venv $(VENV)

install: $(VENV)/bin/activate
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

install-dev: $(VENV)/bin/activate
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements-dev.txt

run:
	$(PY) main.py

lint:
	$(VENV)/bin/ruff check .

lint-fix:
	$(VENV)/bin/ruff check . --fix

format:
	$(VENV)/bin/ruff format .

format-check:
	$(VENV)/bin/ruff format . --check

typecheck:
	$(VENV)/bin/mypy main.py --ignore-missing-imports

check: lint typecheck

docker-build:
	docker compose build

docker-up:
	docker compose up --build -d

docker-down:
	docker compose down

docker-logs:
	docker compose logs -f

load-test:
	$(VENV)/bin/locust -f locustfile.py

clean:
	rm -rf $(VENV) .mypy_cache .ruff_cache
	find . -type d -name __pycache__ -exec rm -rf {} +
