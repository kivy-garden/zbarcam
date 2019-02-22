# garden.zbarcam

[![Build Status](https://secure.travis-ci.org/kivy-garden/garden.zbarcam.png?branch=develop)](http://travis-ci.org/kivy-garden/garden.zbarcam)

Real time Barcode and QR Code scanner using the camera.
It's built on top of [Kivy](https://github.com/kivy/kivy) and [ZbarLight](https://github.com/Polyconseil/zbarlight).

<img src="https://raw.githubusercontent.com/AndreMiras/garden.zbarcam/develop/screenshot.gif" align="right" width="256" alt="screenshot" />

## How to use
Simply import and instanciate `ZBarCam` in your kvlang file and access its `symbols` property.
```yaml
#:import ZBarCam kivy.garden.zbarcam
BoxLayout:
    orientation: 'vertical'
    ZBarCam:
        id: zbarcam
        # optional, by default checks all types
        code_types: 'qrcode', 'ean13'
    Label:
        size_y: 20
        size_hint_y: None
        text: ", ".join([str(code) for code in zbarcam.codes])
```

## Install
Install system requirements (Ubuntu 16.04):
```sh
sudo apt install libzbar-dev
```

Install garden requirements:
```sh
garden install xcamera
```

Install zbarcam:
```sh
garden install zbarcam
```

You may also need to compile/install OpenCV manually, see [OpenCV.md](OpenCV.md).

## Contribute
To play with the project, install system dependencies and Python requirements using the [Makefile](Makefile).
```sh
make
```
Then verify everything is OK by running tests.
```sh
make test
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
It's common to forget `pil` in `buildozer.spec` `requirements` section.

## Credits
I borrowed a lot of code from [tito/android-zbar-qrcode](https://github.com/tito/android-zbar-qrcode).
