#!/usr/bin/env python
"""
This demo can be ran from the project root directory via:
```sh
python src/main.py
```
It can also be ran via p4a/buildozer.
"""
from kivy.app import App
from kivy.lang import Builder

DEMO_APP_KV_LANG = """
#:import ZBarCam kivy_garden.zbarcam.ZBarCam
BoxLayout:
    orientation: 'vertical'
    ZBarCam:
        id: zbarcam
        # optional, override the camera index (default 0)
        camera_index: 0     # or try a different value
        # optional, by default checks all types
        code_types: 'QRCODE', 'EAN13'
    Label:
        size_hint: None, None
        size: self.texture_size[0], 50
        text: ', '.join([str(symbol.data) for symbol in zbarcam.symbols])
"""


class DemoApp(App):

    def build(self):
        return Builder.load_string(DEMO_APP_KV_LANG)


if __name__ == '__main__':
    DemoApp().run()
