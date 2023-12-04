.PHONY: all check clean dev format format-check lint lint-fix

PYMODULE:=kmicms
MANAGEPY:=$(CMD) ./$(PYMODULE)/manage.py
APPS:=kmicms accounts core integrations pages

all: format lint check

format:
	ruff format $(PYMODULE)
	cd $(PYMODULE) && find $(APPS) templates -name "*.html" | xargs djhtml

format-check:
	ruff format --check $(PYMODULE)
	cd $(PYMODULE) && find $(APPS) templates -name "*.html" | xargs djhtml --check

lint: 
	ruff check $(PYMODULE)

lint-fix: 
	ruff check --fix $(PYMODULE)

check:
	$(MANAGEPY) check

dev:
	$(MANAGEPY) runserver

clean:
	git clean -Xdf # Delete all files in .gitignore