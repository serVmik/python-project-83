PORT ?= 8000
DATABASE_URL = page_analyzer

dev:
	poetry run flask --app page_analyzer:app --debug run

start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

install:
	poetry install

schema-db:
	psql $(DATABASE_URL) < database.sql

build: install schema-db

publish:
	poetry publish --dry-run

package-install:
	python3 -m pip install dist/*.whl

lint:
	poetry run flake8 page_analyzer tests

test:
	poetry run pytest --cov=page_analyzer -vv -s

test-pw:
	poetry run pytest tests/test_by_playwright.py

test-coverage:
	poetry run pytest --cov=page_analyzer --cov-report xml

selfcheck:
	poetry check

check: lint test

.PHONY: dev install test lint selfcheck check build
