VENV_NAME=venv
PIP=$(VENV_NAME)/bin/pip
TOX=`which tox`
GARDEN=$(VENV_NAME)/bin/garden
PYTHON=$(VENV_NAME)/bin/python
ISORT=$(VENV_NAME)/bin/isort
FLAKE8=$(VENV_NAME)/bin/flake8
TWINE=`which twine`
SOURCES=src/ tests/ setup.py setup_meta.py
# using full path so it can be used outside the root dir
SPHINXBUILD=$(shell realpath venv/bin/sphinx-build)
DOCS_DIR=doc
SYSTEM_DEPENDENCIES= \
	libpython$(PYTHON_VERSION)-dev \
	libsdl2-dev \
	libzbar-dev \
	tox \
	virtualenv
OS=$(shell lsb_release -si)
PYTHON_MAJOR_VERSION=3
PYTHON_MINOR_VERSION=6
PYTHON_VERSION=$(PYTHON_MAJOR_VERSION).$(PYTHON_MINOR_VERSION)
PYTHON_WITH_VERSION=python$(PYTHON_VERSION)


all: system_dependencies virtualenv

venv:
	test -d venv || virtualenv -p $(PYTHON_WITH_VERSION) venv

virtualenv: venv
	$(PIP) install Cython==0.28.6
	$(PIP) install -r requirements/requirements.txt

virtualenv/test: virtualenv
	$(PIP) install -r requirements/requirements-test.txt

system_dependencies:
ifeq ($(OS), Ubuntu)
	sudo apt install --yes --no-install-recommends $(SYSTEM_DEPENDENCIES)
endif

run/linux: virtualenv
	$(PYTHON) src/main.py

run: run/linux

test:
	$(TOX)

uitest: virtualenv/test
	PYTHONPATH=src $(PYTHON) -m unittest discover --top-level-directory=. --start-directory=tests/ui/

lint/isort-check: virtualenv/test
	$(ISORT) --check-only --recursive --diff $(SOURCES)

lint/isort-fix: virtualenv/test
	$(ISORT) --recursive $(SOURCES)

lint/flake8: virtualenv/test
	$(FLAKE8) $(SOURCES)

lint: lint/isort-check lint/flake8

docs/clean:
	rm -rf $(DOCS_DIR)/build/

docs:
	cd $(DOCS_DIR) && SPHINXBUILD=$(SPHINXBUILD) make html

release/clean:
	rm -rf dist/ build/

release/build: release/clean
	$(PYTHON) setup.py sdist bdist_wheel
	$(PYTHON) setup_meta.py sdist bdist_wheel
	$(TWINE) check dist/*

release/upload:
	$(TWINE) upload dist/*

clean: release/clean docs/clean
	py3clean src/
	find src/ -type d -name "__pycache__" -exec rm -r {} +
	find src/ -type d -name "*.egg-info" -exec rm -r {} +

clean/all: clean
	rm -rf $(VENV_NAME) .tox/
