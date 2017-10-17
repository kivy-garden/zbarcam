# OpenCV

## Linux Camera support
In order to be able to use the camera on Linux, you need to compile OpenCV.
Simply installing `opencv-python` from pypi is not enough.
Currently only OpenCV2 works with Kivy on Linux (see https://github.com/kivy/kivy/issues/5404).
Download and extract the OpenCV2 archive:
```
wget https://github.com/opencv/opencv/archive/2.4.13.3.tar.gz -O opencv-2.4.13.3.tar.gz
tar -xvzf opencv-2.4.13.3.tar.gz
```
Prepare and build:
```
cd opencv-2.4.13.3/
mkdir build && cd build/
cmake ..
make -j4
```
Copy your compiled `cv2.so` to your virtualenv:
```
cp lib/cv2.so venv/lib/python2.7/site-packages/cv2.so
```
