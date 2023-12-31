.PHONY: all check clean dev format format-check lint lint-fix test test-cov

PYMODULE:=kmicms
MANAGEPY:=$(CMD) ./$(PYMODULE)/manage.py
APPS:=kmicms accounts core integrations pages
CMD:=poetry run

all: format lint check test

format:
	$(CMD) ruff format $(PYMODULE)
	cd $(PYMODULE) && find $(APPS) templates -name "*.html" | xargs $(CMD) djhtml

format-check:
	$(CMD) ruff format --check $(PYMODULE)
	cd $(PYMODULE) && find $(APPS) templates -name "*.html" | xargs $(CMD) djhtml --check

lint: 
	$(CMD) ruff check $(PYMODULE)

lint-fix: 
	$(CMD) ruff check --fix $(PYMODULE)

check:
	$(CMD) $(MANAGEPY) check

dev:
	$(CMD) $(MANAGEPY) runserver

clean:
	git clean -Xdf # Delete all files in .gitignore

test: | $(PYMODULE)
	cd kmicms && DJANGO_SETTINGS_MODULE=kmicms.settings $(CMD) pytest --cov=. $(APPS) $(PYMODULE)

test-cov:
	cd kmicms && DJANGO_SETTINGS_MODULE=kmicms.settings $(CMD) pytest --cov=. $(APPS) $(PYMODULE) --cov-report html