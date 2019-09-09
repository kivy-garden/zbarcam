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
	build-essential \
	cmake \
	curl \
	libpython$(PYTHON_VERSION)-dev \
	libsdl2-dev \
	libzbar-dev \
	tox \
	virtualenv \
	wget
OS=$(shell lsb_release -si)
PYTHON_MAJOR_VERSION=3
PYTHON_MINOR_VERSION=6
PYTHON_VERSION=$(PYTHON_MAJOR_VERSION).$(PYTHON_MINOR_VERSION)
PYTHON_WITH_VERSION=python$(PYTHON_VERSION)
# python3 has a "m" suffix for both include path and library
PYTHON_M=$(PYTHON_WITH_VERSION)
SITE_PACKAGES_DIR=$(VENV_NAME)/lib/$(PYTHON_WITH_VERSION)/site-packages
NPROC=`grep -c '^processor' /proc/cpuinfo`


ifeq ($(PYTHON_MAJOR_VERSION), 3)
	PYTHON_M := $(PYTHON_M)m
endif


all: system_dependencies virtualenv

venv:
	test -d venv || virtualenv -p python$(PYTHON_MAJOR_VERSION) venv

virtualenv: venv
	$(PIP) install Cython==0.28.6
	$(PIP) install -r requirements/requirements.txt
	$(GARDEN) install xcamera

system_dependencies:
ifeq ($(OS), Ubuntu)
	sudo apt install --yes --no-install-recommends $(SYSTEM_DEPENDENCIES)
endif

run/linux: virtualenv
	$(PYTHON) src/main.py

run: run/linux

test:
	$(TOX)

uitest: virtualenv
	$(PIP) install -r requirements/test_requirements.txt
	PYTHONPATH=src $(PYTHON) -m unittest discover --top-level-directory=. --start-directory=tests/ui/

isort-check: virtualenv
	$(ISORT) --check-only --recursive --diff $(SOURCES)

isort-fix: virtualenv
	$(ISORT) --recursive $(SOURCES)

flake8: virtualenv
	$(FLAKE8) $(SOURCES)

lint: isort-check flake8

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
