#<-- ======= Developed Variables ======= -->
PORT ?= 8000
DB_NAME = page-analyzer
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

#<-- ======= Check ======= -->
lint:
	poetry run flake8 page_analyzer

selfcheck:
	poetry check

check: lint
#<-- End Check -->

.PHONY: dev install test lint selfcheck check build gendiff