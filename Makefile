#<-- ======= Developed Variables ======= -->
PORT ?= 8000
DB_NAME = page_analyzer
#<-- End Developed Variables -->


#<-- ======= Start Project ======= -->
dev:
	poetry run flask --app page_analyzer:app --debug run

start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app
#<-- End Start Project -->


#<-- ======= Database ======= -->
schema-db:
	psql $(DB_NAME) < database.sql

show-db-urls:
	psql -d urls
#<-- End Database -->


#<-- ======= Poetry Project ======= -->
build:
	poetry build

install:
	poetry install

publish:
	poetry publish --dry-run

package-install:
	python3 -m pip install dist/*.whl
#<-- End Poetry Project -->


#<-- ======= Checks ======= -->
test-playwright:
	poetry run pytest tests/test_playwright.py -vv --cov -s

test-url:
	poetry run pytest tests/test_url.py -vv --cov -s

lint:
	poetry run flake8 page_analyzer

selfcheck:
	poetry check

check: lint test-url
#<-- End Check -->


.PHONY: dev install test lint selfcheck check build gendiff