# Installation

## Supported versions

* Python 3.5+

## Dependencies

* [Kivy](https://kivy.org/#download)


## Installation

Please see the [garden docs](https://kivy-garden.github.io/) for full installation instructions.

Install last zbarcam release from PyPI with:
```sh
pip install --upgrade zbarcam
```

Or develop branch directly from github with:
```sh
pip install https://github.com/kivy-garden/zbarcam/archive/develop.zip
```

You can also automatically install it using garden's pypi server with:
```sh
python -m pip install zbarcam --extra-index-url https://kivy-garden.github.io/simple/
```

You can permanently add our garden server to your [pip.conf](https://pip.pypa.io/en/stable/user_guide/#config-file)
so that you don't have to specify it with `--extra-index-url`:
```sh
[global]
timeout = 60
index-url = https://kivy-garden.github.io/simple/
```
