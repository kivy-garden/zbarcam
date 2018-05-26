VENV_NAME=venv
ACTIVATE_PATH=$(VENV_NAME)/bin/activate
PIP=`. $(ACTIVATE_PATH); which pip`
TOX=`which tox`
GARDEN=`. $(ACTIVATE_PATH); which garden`
PYTHON=$(VENV_NAME)/bin/python
SYSTEM_DEPENDENCIES=virtualenv build-essential libpython2.7-dev libsdl2-dev libzbar-dev \
	cmake python-numpy tox wget curl
OS=$(shell lsb_release -si)
OPENCV_VERSION=2.4.13.6
OPENCV_BASENAME=opencv-$(OPENCV_VERSION)
OPENCV_BUILD=$(OPENCV_BASENAME)/build/lib/cv2.so
OPENCV_DEPLOY=$(VENV_NAME)/lib/python2.7/site-packages/cv2.so
NPROC=`grep -c '^processor' /proc/cpuinfo`


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
	curl --location https://github.com/opencv/opencv/archive/$(OPENCV_VERSION).tar.gz \
		--progress-bar --output $(OPENCV_BASENAME).tar.gz
	tar -xf $(OPENCV_BASENAME).tar.gz
	cmake \
		-D BUILD_DOCS=OFF -D BUILD_PACKAGE=OFF -D BUILD_PERF_TESTS=OFF \
		-D BUILD_TESTS=OFF -D BUILD_opencv_apps=OFF \
		-D BUILD_opencv_nonfree=OFF -D BUILD_opencv_stitching=OFF \
		-D BUILD_opencv_superres=OFF -D BUILD_opencv_ts=OFF \
		-D BUILD_WITH_DEBUG_INFO=OFF -D WITH_1394=OFF -D WITH_CUDA=OFF \
		-D WITH_CUFFT=OFF -D WITH_GIGEAPI=OFF -D WITH_JASPER=OFF \
		-D WITH_OPENEXR=OFF -D WITH_PVAPI=OFF -D WITH_GTK=OFF \
		-D BUILD_opencv_python=ON -B$(OPENCV_BASENAME)/build -H$(OPENCV_BASENAME)
	cmake --build $(OPENCV_BASENAME)/build -- -j$(NPROC)

opencv_build: $(OPENCV_BUILD)

$(OPENCV_DEPLOY): opencv_build virtualenv
	cp $(OPENCV_BUILD) $(OPENCV_DEPLOY)

opencv: $(OPENCV_DEPLOY)

clean:
	rm -rf $(VENV_NAME) .tox/ $(OPENCV_BASENAME)

test:
	$(TOX)
