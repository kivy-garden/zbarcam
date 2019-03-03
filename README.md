# garden.zbarcam

[![Build Status](https://secure.travis-ci.org/kivy-garden/garden.zbarcam.png?branch=develop)](http://travis-ci.org/kivy-garden/garden.zbarcam)

Real time Barcode and QR Code scanner using the camera.
It's built on top of [Kivy](https://github.com/kivy/kivy) and [pyzbar](https://github.com/NaturalHistoryMuseum/pyzbar).

<img src="https://raw.githubusercontent.com/AndreMiras/garden.zbarcam/develop/screenshot.gif" align="right" width="256" alt="screenshot" />

## How to use
Simply import and instanciate `ZBarCam` in your kvlang file and access its `symbols` property.
```yaml
#:import ZBarCam kivy.garden.zbarcam
#:import ZBarSymbol pyzbar.pyzbar.ZBarSymbol
BoxLayout:
    orientation: 'vertical'
    ZBarCam:
        id: zbarcam
        # optional, by default checks all types
        code_types: ZBarSymbol.QRCODE, ZBarSymbol.EAN13
    Label:
        size_hint: None, None
        size: self.texture_size[0], 50
        text: ', '.join([str(symbol.data) for symbol in zbarcam.symbols])
```

## Install

### Ubuntu
Install system requirements (Ubuntu 18.04):
```sh
sudo apt install libzbar-dev
```

Install garden requirements:
```sh
garden install xcamera
```

Install zbarcam:
Via `garden`:
```sh
garden install --upgrade zbarcam
```
Via `pip`:
```sh
pip install --upgrade https://github.com/kivy-garden/garden.zbarcam/archive/develop.zip
```

You may also need to compile/install OpenCV manually, see [OpenCV.md](OpenCV.md).

### Android
Build for Android via buildozer, see [buildozer.spec](buildozer.spec).

## Contribute
To play with the project, install system dependencies and Python requirements using the [Makefile](Makefile).
```sh
make
```
Then verify everything is OK by running tests.
```sh
make test
make uitest
```

## Troubleshooting

### Install `Unable to import package 'kivy.garden.xcamera.XCamera'`
Missing the `xcamera` dependency, install it with:
```sh
garden install xcamera
```

### Android `ValueError: Empty module name`
More likely an import issue in your `.kv` file.
Try to `from zbarcam import ZBarCam` in your `main.py` to see the exact error.
It's common to forget `Pillow` in `buildozer.spec` `requirements` section.

## Credits
I borrowed a lot of code from [tito/android-zbar-qrcode](https://github.com/tito/android-zbar-qrcode).
