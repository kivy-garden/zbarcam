VENV_NAME=venv
ACTIVATE_PATH=$(VENV_NAME)/bin/activate
PIP=`. $(ACTIVATE_PATH); which pip`
TOX=`. $(ACTIVATE_PATH); which tox`
GARDEN=`. $(ACTIVATE_PATH); which garden`
PYTHON=$(VENV_NAME)/bin/python
SYSTEM_DEPENDENCIES=virtualenv build-essential libzbar-dev cmake python-numpy tox
OS=$(shell lsb_release -si)
OPENCV_VERSION=2.4.13.6
OPENCV_BASENAME=opencv-$(OPENCV_VERSION)
OPENCV_BUILD=$(OPENCV_BASENAME)/build/lib/cv2.so
OPENCV_DEPLOY=$(VENV_NAME)/lib/python2.7/site-packages/cv2.so


all: system_dependencies opencv virtualenv

virtualenv:
	test -d venv || virtualenv -p python2 venv
	. venv/bin/activate
	$(PIP) install Cython==0.26.1
	$(PIP) install -r requirements/requirements.txt
	$(GARDEN) install xcamera

system_dependencies:
ifeq ($(OS), Ubuntu)
	sudo apt install --yes --no-install-recommends $(SYSTEM_DEPENDENCIES)
endif

$(OPENCV_BUILD):
	wget --continue https://github.com/opencv/opencv/archive/$(OPENCV_VERSION).tar.gz \
		--output-document $(OPENCV_BASENAME).tar.gz
	tar -xvf $(OPENCV_BASENAME).tar.gz
	cmake -DBUILD_opencv_python=ON -B$(OPENCV_BASENAME)/build -H$(OPENCV_BASENAME)
	cmake --build $(OPENCV_BASENAME)/build -- -j4

opencv_build: $(OPENCV_BUILD)

$(OPENCV_DEPLOY): opencv_build virtualenv
	cp $(OPENCV_BUILD) $(OPENCV_DEPLOY)

opencv: $(OPENCV_DEPLOY)

clean:
	rm -rf $(VENV_NAME) .tox/ $(OPENCV_BASENAME)

test:
	$(TOX)
