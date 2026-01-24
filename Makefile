# Makefile to run ruff and pyright (prefers poetry if available)
RUN := export PYTHONPATH=src && poetry run

.PHONY: lint typecheck check install-dev

format:
	$(RUN) ruff format

lint:
	$(RUN) ruff check . --fix
	$(RUN) pyright src tests

check: lint typecheck

install-dev:
ifeq ($(POETRY),)
	@echo "Poetry not found; please install ruff and pyright in your PATH or install poetry."
else
	poetry install --with dev
endif

create-migration:
	$(RUN) alembic revision --autogenerate -m "$(msg)"

apply-migrations:
	$(RUN) alembic upgrade head

down-migrations:
	$(RUN) alembic downgrade -1
