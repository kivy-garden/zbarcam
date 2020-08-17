import os
import threading
import queue
from collections import namedtuple

import PIL
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import ListProperty
from kivy.uix.anchorlayout import AnchorLayout
from pyzbar import pyzbar

from .utils import fix_android_image

MODULE_DIRECTORY = os.path.dirname(os.path.realpath(__file__))


class ZBarCam(AnchorLayout):
    """
    Widget that use the Camera and zbar to detect qrcode.
    When found, the `codes` will be updated.
    """
    resolution = ListProperty([640, 480])

    symbols = ListProperty([])
    Symbol = namedtuple('Symbol', ['type', 'data'])
    # checking all possible types by default
    code_types = ListProperty(set(pyzbar.ZBarSymbol))

    def __init__(self, **kwargs):
        # lazy loading the kv file rather than loading at module level,
        # that way the `XCamera` import doesn't happen too early
        Builder.load_file(os.path.join(MODULE_DIRECTORY, "zbarcam.kv"))
        super().__init__(**kwargs)

        self._decoding_frame = threading.Event()
        self._symbols_queue = queue.Queue()

        Clock.schedule_once(lambda dt: self._setup())

    def _setup(self):
        """
        Postpones some setup tasks that require self.ids dictionary.
        """
        self._remove_shoot_button()
        # `self.xcamera._camera` instance may not be available if e.g.
        # the `CAMERA` permission is not granted
        self.xcamera.bind(on_camera_ready=self._on_camera_ready)
        # camera may still be ready before we bind the event
        if self.xcamera._camera is not None:
            self._on_camera_ready(self.xcamera)

    def _on_camera_ready(self, xcamera):
        """
        Starts binding when the `xcamera._camera` instance is ready.
        """
        xcamera._camera.bind(on_texture=self._on_texture)
        Clock.schedule_interval(self._update_symbols, 0)

    def _remove_shoot_button(self):
        """
        Removes the "shoot button", see:
        https://github.com/kivy-garden/garden.xcamera/pull/3
        """
        xcamera = self.xcamera
        shoot_button = xcamera.children[0]
        xcamera.remove_widget(shoot_button)

    def _on_texture(self, xcamera):
        if not self._decoding_frame.is_set():
            self._decoding_frame.set()
            threading.Thread(
                target=self._detect_qrcode_frame,
                args=(
                    xcamera.texture,
                    xcamera.texture.pixels,
                    self.code_types,
                ),
            ).start()

    def _update_symbols(self, *args):
        try:
            self.symbols = self._symbols_queue.get_nowait()
        except queue.Empty:
            return

    def _detect_qrcode_frame(self, texture, pixels, code_types):
        image_data = pixels
        size = texture.size
        # Fix for mode mismatch between texture.colorfmt and data returned by
        # texture.pixels. texture.pixels always returns RGBA, so that should
        # be passed to PIL no matter what texture.colorfmt returns. refs:
        # https://github.com/AndreMiras/garden.zbarcam/issues/41
        pil_image = PIL.Image.frombytes(mode='RGBA', size=size,
                                        data=image_data)
        pil_image = fix_android_image(pil_image)
        symbols = []
        codes = pyzbar.decode(pil_image, symbols=code_types)

        for code in codes:
            symbol = ZBarCam.Symbol(type=code.type, data=code.data)
            symbols.append(symbol)

        self._symbols_queue.put(symbols)
        self._decoding_frame.clear()

    @property
    def xcamera(self):
        return self.ids['xcamera']

    def start(self):
        self.xcamera.play = True

    def stop(self):
        self.xcamera.play = False
