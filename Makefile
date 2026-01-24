SRC = src/cli.py
DATA = $(wildcard data/*.ps2)
VENV = myenv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip
SHINY = $(VENV)/bin/shiny
shiny: install
	$(SHINY) run src/app.py --reload

cli:
	$(PYTHON) $(SRC) $(DATA)

venv:
	python3 -m venv $(VENV)

install: venv
	$(PIP) install -r requirements.txt

docs:
	doxygen Doxyfile
