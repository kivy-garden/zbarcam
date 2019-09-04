import os
from collections import namedtuple

import PIL
from kivy.clock import Clock, mainthread
from kivy.garden.xcamera import XCamera
from kivy.lang import Builder
from kivy.properties import ListProperty
from kivy.uix.anchorlayout import AnchorLayout
from pyzbar import pyzbar

from .utils import check_request_camera_permission, fix_android_image

MODULE_DIRECTORY = os.path.dirname(os.path.realpath(__file__))


class CustomXCamera(XCamera):
    """
    Inherits from `kivy.garden.xcamera.XCamera`.
    Overrides `_on_index()` to make sure the `kivy.core.camera.Camera` object
    is only created if permission are granted on Android.
    On other system, it's a noop calling the parent `_on_index()`.
    """

    def __init__(self, **kwargs):
        self.register_event_type('on_camera_ready')
        super().__init__(**kwargs)

    def _on_index(self, *largs):
        """
        Overrides `kivy.uix.camera.Camera._on_index()` to make sure
        `camera.open()` is not called unless Android `CAMERA` permission is
        granted, refs #12.
        """
        @mainthread
        def on_permissions_callback(permissions, grant_results):
            """
            On camera permission callback calls parent `_on_index()` method.
            """
            if all(grant_results):
                self._on_index_dispatch(*largs)
        if check_request_camera_permission(callback=on_permissions_callback):
            self._on_index_dispatch(*largs)

    def _on_index_dispatch(self, *largs):
        super()._on_index(*largs)
        self.dispatch('on_camera_ready')

    def on_camera_ready(self):
        """
        Fired when the camera is ready.
        """
        pass


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
        Clock.schedule_once(lambda dt: self._setup())

    def _setup(self):
        """
        Postpones some setup tasks that require self.ids dictionary.
        """
        self._remove_shoot_button()
        # `self.xcamera._camera` instance may not be available if e.g.
        # the `CAMERA` permission is not granted
        self.xcamera.bind(on_camera_ready=self._on_camera_ready)

    def _on_camera_ready(self, xcamera):
        """
        Starts binding when the `xcamera._camera` instance is ready.
        """
        xcamera._camera.bind(on_texture=self._on_texture)

    def _remove_shoot_button(self):
        """
        Removes the "shoot button", see:
        https://github.com/kivy-garden/garden.xcamera/pull/3
        """
        xcamera = self.xcamera
        shoot_button = xcamera.children[0]
        xcamera.remove_widget(shoot_button)

    def _on_texture(self, instance):
        self.symbols = self._detect_qrcode_frame(
            texture=instance.texture, code_types=self.code_types)

    @classmethod
    def _detect_qrcode_frame(cls, texture, code_types):
        image_data = texture.pixels
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
        return symbols

    @property
    def xcamera(self):
        return self.ids['xcamera']

    def start(self):
        self.xcamera.play = True

    def stop(self):
        self.xcamera.play = False
