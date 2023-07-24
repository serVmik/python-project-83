#<!-- ======= Developed Variables ======= -->
PORT ?= 8000
DB_NAME = page_analyzer
#<!-- End Developed Variables -->


#<!-- ======= Start Project ======= -->
dev:
	poetry run flask --app page_analyzer:app --debug run

start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app
#<!-- End Start Project -->


#<!-- ======= Database ======= -->
schema-db:
	psql $(DB_NAME) < database.sql
#<!-- End Database -->


#<!-- ======= Poetry Project ======= -->
build:
	poetry build

install:
	poetry install

publish:
	poetry publish --dry-run

package-install:
	python3 -m pip install dist/*.whl
#<!-- End Poetry Project -->


#<!-- ======= Checks ======= -->
lint:
	poetry run flake8 page_analyzer tests

test-url:
	poetry run pytest tests/test_urls.py -vv -s

test-pw:
	poetry run pytest tests/test_by_playwright.py

test-coverage:
	poetry run pytest --cov=page_analyzer --cov-report xml

selfcheck:
	poetry check

check: lint test-url
#<!-- End Check -->


#<!-- ======= render.com ======= -->
build-render: install schema-db
#<!-- End render.com -->


.PHONY: dev install test lint selfcheck check build test-url