# garden.zbarcam

Real time Barcode and QR Code scanner using the camera.
It's built on top of [Kivy](https://github.com/kivy/kivy) and [ZBar](https://github.com/ZBar/ZBar).

## How to use
Simply import and instanciate `ZBarCam` in your kvlang file and access its `symbols` property.
```
#:import ZBarCam zbarcam
BoxLayout:
    orientation: 'vertical'
    ZBarCam:
        id: zbarcam
    Label:
        size_y: 20
        size_hint_y: None
        text: ", ".join([str(symbol.data) for symbol in zbarcam.symbols])
```

## Install
Install system requirements (Ubuntu 16.04):
```
sudo apt install libzbar-dev
```

Install garden requirements:
```
garden install xcamera
```

Install zbarcam:
```
pip install https://github.com/AndreMiras/garden.zbarcam/archive/develop.zip
```

You may also need to compile/install OpenCV manually, see [OpenCV.md](OpenCV.md).

## Current limitations
  * Blurry image on Android [#2](https://github.com/AndreMiras/garden.zbarcam/issues/2)
  * Camera image rotated [#3](https://github.com/AndreMiras/garden.zbarcam/issues/3)
  * Upstream recipes integration [kivy/python-for-android#1145](https://github.com/kivy/python-for-android/pull/1145)

## Troubleshooting

### Android `ValueError: Empty module name`
More likely an import issue in your `.kv` file.
Try to `from zbarcam import ZBarCam` in your `main.py` to see the exact error.
It's common to forget `pil` in `buildozer.spec` `requirements` section.

## Credits
I borrowed a lot of code from [tito/android-zbar-qrcode](https://github.com/tito/android-zbar-qrcode).
