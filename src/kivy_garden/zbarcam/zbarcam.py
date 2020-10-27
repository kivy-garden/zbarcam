import collections
import os
import queue
import threading

import PIL
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.logger import Logger
from kivy.properties import ListProperty
from kivy.uix.anchorlayout import AnchorLayout

from .utils import fix_android_image

MODULE_DIRECTORY = os.path.dirname(os.path.realpath(__file__))


class ZBarDecoder:
    def validate_code_types(self, code_types):
        available_code_types = self.get_available_code_types()

        if not all(
            code_type in available_code_types
            for code_type in code_types
        ):
            raise ValueError(
                f'Invalid code types: {code_types}. '
                f'Available code types: {available_code_types}'
            )


class PyZBarDecoder(ZBarDecoder):
    @classmethod
    def is_usable(cls):
        try:
            from pyzbar import pyzbar
            cls.pyzbar = pyzbar
            return True

        except ImportError:
            return False

    def get_available_code_types(self):
        return set(
            code_type.lower()
            for code_type in self.pyzbar.ZBarSymbol.__members__.keys()
        )

    def decode(self, image, code_types):
        self.validate_code_types(code_types)
        pyzbar_code_types = set(
            getattr(self.pyzbar.ZBarSymbol, code_type.upper())
            for code_type in code_types
        )
        return [
            ZBarCam.Symbol(type=code.type.lower(), data=code.data)
            for code in self.pyzbar.decode(
                image,
                symbols=pyzbar_code_types,
            )
        ]


class ZBarLightDecoder(ZBarDecoder):
    @classmethod
    def is_usable(cls):
        try:
            import zbarlight
            cls.zbarlight = zbarlight
            return True

        except ImportError:
            return False

    def get_available_code_types(self):
        return set(
            code_type.lower()
            for code_type in self.zbarlight.Symbologies.keys()
        )

    def decode(self, image, code_types):
        self.validate_code_types(code_types)
        codes = self.zbarlight.scan_codes(code_types, image)

        # zbarlight.scan_codes() returns None instead of []
        if not codes:
            return []

        return [
            ZBarCam.Symbol(type=None, data=code)
            for code in codes
        ]


available_implementations = {
    'pyzbar': PyZBarDecoder,
    'zbarlight': ZBarLightDecoder,
}


for name, implementation in available_implementations.items():
    if implementation.is_usable():
        zbar_decoder = implementation()
        Logger.info('ZBarCam: Using implementation %s', name)
        break
else:
    raise ImportError(
        'No zbar implementation available '
        f'(tried {", ".join(available_implementations.keys())})'
    )


class ZBarCam(AnchorLayout):
    """
    Widget that use the Camera and zbar to detect qrcode.
    When found, the `codes` will be updated.
    """
    resolution = ListProperty([640, 480])

    symbols = ListProperty([])
    Symbol = collections.namedtuple('Symbol', ['type', 'data'])
    # checking all possible types by default
    code_types = ListProperty(zbar_decoder.get_available_code_types())

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
                target=self._threaded_detect_qrcode_frame,
                args=(
                    xcamera.texture,
                    xcamera.texture.pixels,
                    self.code_types,
                ),
            ).start()

    def _threaded_detect_qrcode_frame(self, texture, pixels, code_types):
        self._symbols_queue.put(
            self._detect_qrcode_frame(texture, code_types, pixels)
        )
        self._decoding_frame.clear()

    def _update_symbols(self, *args):
        try:
            self.symbols = self._symbols_queue.get_nowait()
        except queue.Empty:
            return

    def _detect_qrcode_frame(self, texture, code_types, pixels=None):
        image_data = pixels or texture.pixels  # Use pixels kwarg for threading
        size = texture.size
        # Fix for mode mismatch between texture.colorfmt and data returned by
        # texture.pixels. texture.pixels always returns RGBA, so that should
        # be passed to PIL no matter what texture.colorfmt returns. refs:
        # https://github.com/AndreMiras/garden.zbarcam/issues/41
        pil_image = PIL.Image.frombytes(mode='RGBA', size=size,
                                        data=image_data)
        pil_image = fix_android_image(pil_image)
        return zbar_decoder.decode(pil_image, code_types)

    @property
    def xcamera(self):
        return self.ids['xcamera']

    def start(self):
        self.xcamera.play = True

    def stop(self):
        self.xcamera.play = False
