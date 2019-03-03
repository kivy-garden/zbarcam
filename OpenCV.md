# OpenCV

## Linux Camera support
In order to be able to use the camera on Linux, you need to compile OpenCV.
Simply installing `opencv-python` from pypi is not enough.

Use the [Makefile](Makefile) provided to compile and install OpenCV library.
```
make system_dependencies
make opencv
```
It would build OpenCV and deploy it to your virtualenv.
