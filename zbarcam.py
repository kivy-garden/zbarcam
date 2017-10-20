from collections import namedtuple

import PIL
import zbar
from kivy.app import App
from kivy.garden.xcamera import XCamera as Camera
from kivy.lang import Builder
from kivy.properties import ListProperty
from kivy.uix.anchorlayout import AnchorLayout
from kivy.utils import platform

# Pillow is not currently available for Android:
# https://github.com/kivy/python-for-android/pull/786
try:
    # Pillow
    PIL.Image.frombytes
    PIL.Image.Image.tobytes
except AttributeError:
    # PIL
    PIL.Image.frombytes = PIL.Image.frombuffer
    PIL.Image.Image.tobytes = PIL.Image.Image.tostring


class ZBarCam(AnchorLayout):
    """
    Widget that use the Camera and zbar to detect qrcode.
    When found, the `symbols` will be updated.
    """
    camera_size = ListProperty([640, 480])

    symbols = ListProperty([])

    Qrcode = namedtuple(
            'Qrcode', ['type', 'data', 'bounds', 'quality', 'count'])

    def __init__(self, **kwargs):
        super(ZBarCam, self).__init__(**kwargs)
        self._camera = Camera(
                play=True,
                resolution=self.camera_size,
                size=self.camera_size,
                size_hint=(None, None))
        self._remove_shoot_button()
        self._enable_android_autofocus()
        self._camera._camera.bind(on_texture=self._on_texture)
        # TODO
        self.add_widget(self._camera)
        # create a scanner used for detecting qrcode
        self.scanner = zbar.ImageScanner()
        # TODO
        # self.start()

    def _remove_shoot_button(self):
        """
        Removes the "shoot button", see:
        https://github.com/kivy-garden/garden.xcamera/pull/3
        """
        xcamera = self._camera
        shoot_button = xcamera.children[0]
        xcamera.remove_widget(shoot_button)

    def _enable_android_autofocus(self):
        """
        Enables autofocus on Android.
        """
        if platform != 'android':
            return
        camera = self._camera._camera._android_camera
        params = camera.getParameters()
        params.setFocusMode('continuous-video')
        camera.setParameters(params)

    def _on_texture(self, instance):
        self._detect_qrcode_frame(
            instance=None, camera=instance, texture=instance.texture)

    # TODO
    def start(self):
        self._camera.play = True
        # self._camera.start()

    # TODO
    def stop(self):
        self._camera.stop()

    def _detect_qrcode_frame(self, instance, camera, texture):
        image_data = texture.pixels
        size = texture.size
        fmt = texture.colorfmt.upper()
        pil_image = PIL.Image.frombytes(mode=fmt, size=size, data=image_data)
        # convert to greyscale; since zbar only works with it
        pil_image = pil_image.convert('L')
        width, height = pil_image.size
        raw_image = pil_image.tobytes()
        zimage = zbar.Image(width, height, "Y800", raw_image)
        result = self.scanner.scan(zimage)
        if result == 0:
            self.symbols = []
            return
        # we detected qrcode extract and dispatch them
        symbols = []
        for symbol in zimage:
            qrcode = ZBarCam.Qrcode(
                type=symbol.type,
                data=symbol.data,
                quality=symbol.quality,
                count=symbol.count,
                bounds=None)
            symbols.append(qrcode)
        self.symbols = symbols


DEMO_APP_KV_LANG = """
BoxLayout:
    orientation: 'vertical'
    ZBarCam:
        id: zbarcam
    Label:
        size_y: 20
        size_hint_y: None
        text: ", ".join([str(symbol.data) for symbol in zbarcam.symbols])
"""


class DemoApp(App):

    def build(self):
        return Builder.load_string(DEMO_APP_KV_LANG)


if __name__ == '__main__':
    DemoApp().run()
