.PHONY: all check clean dev format format-check lint lint-fix test test-cov

PYMODULE:=kmicms
MANAGEPY:=$(CMD) ./$(PYMODULE)/manage.py
APPS:=kmicms accounts core integrations pages

all: format lint check test

format:
	poetry run ruff format $(PYMODULE)
	cd $(PYMODULE) && find $(APPS) templates -name "*.html" | xargs poetry run djhtml

format-check:
	poetry run ruff format --check $(PYMODULE)
	cd $(PYMODULE) && find $(APPS) templates -name "*.html" | xargs poetry run djhtml --check

lint: 
	poetry run ruff check $(PYMODULE)

lint-fix: 
	poetry run ruff check --fix $(PYMODULE)

check:
	poetry run $(MANAGEPY) check

dev:
	poetry run $(MANAGEPY) runserver

clean:
	git clean -Xdf # Delete all files in .gitignore

test: | $(PYMODULE)
	cd kmicms && DJANGO_SETTINGS_MODULE=kmicms.settings poetry run pytest --cov=. $(APPS) $(PYMODULE)

test-cov:
	cd kmicms && DJANGO_SETTINGS_MODULE=kmicms.settings poetry run pytest --cov=. $(APPS) $(PYMODULE) --cov-report html