# OpenCV

## Linux Camera support
In order to be able to use the camera on Linux, you need to compile OpenCV.
Simply installing `opencv-python` from pypi is not enough.
Currently only OpenCV2 works with Kivy on Linux (see https://github.com/kivy/kivy/issues/5404).

Use the [Makefile](Makefile) provided to compile and install OpenCV library.
```
make system_dependencies
make opencv_build
```
Then copy your compiled `cv2.so` to your virtualenv:
```
cp opencv-*/build/lib/cv2.so venv/lib/python2.7/site-packages/cv2.so
```
