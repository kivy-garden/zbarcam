VIRTUAL_ENV ?= venv
PIP=$(VIRTUAL_ENV)/bin/pip
TOX=`which tox`
GARDEN=$(VIRTUAL_ENV)/bin/garden
PYTHON=$(VIRTUAL_ENV)/bin/python
ISORT=$(VIRTUAL_ENV)/bin/isort
FLAKE8=$(VIRTUAL_ENV)/bin/flake8
TWINE=`which twine`
SOURCES=src/ tests/ setup.py setup_meta.py
# using full path so it can be used outside the root dir
SPHINXBUILD=$(shell realpath venv/bin/sphinx-build)
DOCS_DIR=doc
SYSTEM_DEPENDENCIES= \
	build-essential \
	ccache \
	cmake \
	curl \
	libsdl2-dev \
	libsdl2-image-dev \
	libsdl2-mixer-dev \
	libsdl2-ttf-dev \
	libpython3.6-dev \
	libpython$(PYTHON_VERSION)-dev \
	libzbar-dev \
	lsb-release \
	make \
	pkg-config \
	python3.6 \
	python3.6-dev \
	python$(PYTHON_VERSION) \
	python$(PYTHON_VERSION)-dev \
	sudo \
	tox \
	virtualenv
OS=$(shell lsb_release -si)
PYTHON_MAJOR_VERSION=3
PYTHON_MINOR_VERSION=7
PYTHON_VERSION=$(PYTHON_MAJOR_VERSION).$(PYTHON_MINOR_VERSION)
PYTHON_WITH_VERSION=python$(PYTHON_VERSION)


all: system_dependencies virtualenv

system_dependencies:
ifeq ($(OS), Ubuntu)
	sudo apt install --yes --no-install-recommends $(SYSTEM_DEPENDENCIES)
endif

$(VIRTUAL_ENV):
	virtualenv -p $(PYTHON_WITH_VERSION) $(VIRTUAL_ENV)

virtualenv: $(VIRTUAL_ENV)
	$(PIP) install Cython==0.28.6
	$(PIP) install -r requirements/requirements.txt

virtualenv/test: virtualenv
	$(PIP) install -r requirements/requirements-test.txt

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
	rm -rf $(VIRTUAL_ENV) .tox/

docker/build:
	docker build --tag=zbarcam-linux --file=dockerfiles/Dockerfile-linux .

docker/run/test:
	docker run --env-file dockerfiles/env.list -v /tmp/.X11-unix:/tmp/.X11-unix zbarcam-linux 'make test'

docker/run/app:
	docker run --env-file dockerfiles/env.list -v /tmp/.X11-unix:/tmp/.X11-unix --device=/dev/video0:/dev/video0 zbarcam-linux 'make run'

docker/run/shell:
	docker run --env-file dockerfiles/env.list -v /tmp/.X11-unix:/tmp/.X11-unix --device=/dev/video0:/dev/video0 -it --rm zbarcam-linux
