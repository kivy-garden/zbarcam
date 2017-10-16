from collections import namedtuple
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, ListProperty, BooleanProperty, \
            NumericProperty
from kivy.uix.camera import Camera
import zbar
import PIL


class ZBarCam(AnchorLayout):
    """
    Widget that use the Camera and zbar to detect qrcode.
    When found, the `symbols` will be updated.
    """
    camera_size = ListProperty([640, 480])

    symbols = ListProperty([])

    Qrcode = namedtuple('Qrcode',
            ['type', 'data', 'bounds', 'quality', 'count'])

    def __init__(self, **kwargs):
        super(ZBarCam, self).__init__(**kwargs)
        self._camera = Camera(
                play=True,
                resolution=self.camera_size,
                size=self.camera_size,
                size_hint=(None, None))
        self._camera._camera.bind(on_texture=self._on_texture)
        # TODO
        self.add_widget(self._camera)
        # create a scanner used for detecting qrcode
        self.scanner = zbar.ImageScanner()
        # TODO
        # self.start()

    def _on_texture(self, instance):
        self._detect_qrcode_frame(instance=None, camera=instance, texture=instance.texture)

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
        for symbol in zimage:
            print("zbar found a symbol, " + repr(symbol.type) + ": " + symbol.data)
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
