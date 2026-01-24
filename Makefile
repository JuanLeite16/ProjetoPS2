SRC = src/Python/cli.py
DATA = $(wildcard data/*.ps2)
VENV = myenv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip
SHINY = $(VENV)/bin/shiny
REQS = $(VENV)/bin/pipreqs
shiny: install
	$(SHINY) run src/Python/app.py --reload

cli:
	$(PYTHON) $(SRC) $(DATA)

venv:
	python3 -m venv $(VENV)

install: venv
	$(PIP) install -r requirements.txt

docs:
	doxygen Doxyfile

reqs: venv
	$(REQS) . --force --ignore myenv,docs,data,__pycache___
