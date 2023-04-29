# zbarcam

[![Tests](https://github.com/kivy-garden/zbarcam/actions/workflows/tests.yml/badge.svg)](https://github.com/kivy-garden/zbarcam/actions/workflows/tests.yml)
[![Coverage Status](https://coveralls.io/repos/github/kivy-garden/zbarcam/badge.svg?branch=develop)](https://coveralls.io/github/kivy-garden/zbarcam?branch=develop)
[![PyPI version](https://badge.fury.io/py/zbarcam.svg)](https://badge.fury.io/py/zbarcam)
[![Documentation Status](https://readthedocs.org/projects/zbarcam/badge/?version=latest)](https://zbarcam.readthedocs.io/en/latest/?badge=latest)

Real time Barcode and QR Code scanner using the camera.
It's built on top of [Kivy](https://github.com/kivy/kivy) and works with both [pyzbar](https://github.com/NaturalHistoryMuseum/pyzbar) or [zbarlight](https://github.com/Polyconseil/zbarlight).

<img src="https://raw.githubusercontent.com/AndreMiras/garden.zbarcam/develop/screenshot.gif" align="right" width="256" alt="screenshot" />

## How to use
Simply import and instanciate `ZBarCam` in your kvlang file and access its `symbols` property.
```yaml
#:import ZBarCam kivy_garden.zbarcam.ZBarCam
BoxLayout:
    orientation: 'vertical'
    ZBarCam:
        id: zbarcam
        # optional, by default checks all types
        code_types: 'QRCODE', 'EAN13'
    Label:
        size_hint: None, None
        size: self.texture_size[0], 50
        text: ', '.join([str(symbol.data) for symbol in zbarcam.symbols])
```
A full working demo is available in [src/main.py](https://github.com/kivy-garden/zbarcam/blob/master/src/main.py).

## Install

### Ubuntu
Install system requirements (Ubuntu 18.04):
```sh
make system_dependencies
```

Install zbarcam:
```sh
pip install zbarcam
```
Then import it in your Python code via:
```python
from kivy_garden.zbarcam import ZBarCam
```

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

### Android `ValueError: Empty module name`
More likely an import issue in your `.kv` file.
Try to `from zbarcam import ZBarCam` in your `main.py` to see the exact error.
It's common to forget `Pillow` in `buildozer.spec` `requirements` section.
