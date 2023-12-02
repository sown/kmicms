.PHONY: all check clean dev format format-check lint lint-fix

CMD:=
PYMODULE:=kmicms
MANAGEPY:=$(CMD) ./$(PYMODULE)/manage.py
APPS:=kmicms core pages

all: format lint check

format:
	$(CMD) ruff format $(PYMODULE)

format-check:
	$(CMD) ruff format --check $(PYMODULE)

lint: 
	$(CMD) ruff check $(PYMODULE)

lint-fix: 
	$(CMD) ruff check --fix $(PYMODULE)

check:
	$(MANAGEPY) check

dev:
	$(MANAGEPY) runserver

clean:
	git clean -Xdf # Delete all files in .gitignore