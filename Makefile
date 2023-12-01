.PHONY: all clean lint

CMD:=
PYMODULE:=kmicms
MANAGEPY:=$(CMD) ./$(PYMODULE)/manage.py
APPS:=kmicms core pages

all: lint check

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