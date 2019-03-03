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

## Troubleshooting

###  Makefile `cp: cannot stat 'opencv-4.0.1/build/lib/python3/cv2*.so': No such file or directory`
Log:
```
make[2]: Leaving directory '/tmp/trash/zbarcam/opencv-4.0.1/build'
make[1]: Leaving directory '/tmp/trash/zbarcam/opencv-4.0.1/build'
cp opencv-4.0.1/build/lib/python3/cv2*.so venv/lib/python3.7/site-packages
cp: cannot stat 'opencv-4.0.1/build/lib/python3/cv2*.so': No such file or directory
Makefile:97: recipe for target 'venv/lib/python3.7/site-packages/cv2*.so' failed
make: *** [venv/lib/python3.7/site-packages/cv2*.so] Error 1
```
Most likely you need to `pip install numpy` delete your opencv build and build again.
