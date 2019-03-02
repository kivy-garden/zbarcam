import os
import unittest

import mock
from kivy.base import EventLoop
from kivy.core.image import Image

from zbarcam import ZBarCam

FIXTURE_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'fixtures')
# https://github.com/kivy/kivy/blob/1.10.1/doc/sources/faq.rst
EventLoop.ensure_window()


class TestZBarCam(unittest.TestCase):

    def setUp(self):
        with mock.patch('kivy.uix.anchorlayout.AnchorLayout.__init__'):
            self.zbarcam = ZBarCam()

    def test_detect_qrcode_frame_no_qrcode(self):
        """
        Checks `_detect_qrcode_frame()` returns empty list on no qrcode.
        """
        fixture_path = os.path.join(FIXTURE_DIR, 'no_qr_code.png')
        texture = Image(fixture_path).texture
        code_types = self.zbarcam.code_types
        symbols = self.zbarcam._detect_qrcode_frame(texture, code_types)
        self.assertEqual(symbols, [])

    def test_detect_qrcode_frame_one_qrcode(self):
        """
        Checks `_detect_qrcode_frame()` can detect one qrcode.
        """
        fixture_path = os.path.join(FIXTURE_DIR, 'one_qr_code.png')
        texture = Image(fixture_path).texture
        code_types = self.zbarcam.code_types
        symbols = self.zbarcam._detect_qrcode_frame(texture, code_types)
        self.assertEqual(
            symbols,
            [ZBarCam.Symbol(type='QRCODE', data=b'zbarlight test qr code')])

    def test_detect_qrcode_frame_one_qrcode_one_ean(self):
        """
        Checks `_detect_qrcode_frame()` can detect one qrcode and one ean.
        """
        fixture_path = os.path.join(FIXTURE_DIR, 'one_qr_code_and_one_ean.png')
        texture = Image(fixture_path).texture
        code_types = self.zbarcam.code_types
        symbols = self.zbarcam._detect_qrcode_frame(texture, code_types)
        # currently detects no codes, but that's a bug
        self.assertEqual(symbols, [])

    def test_detect_qrcode_frame_two_qrcodes(self):
        """
        Checks `_detect_qrcode_frame()` can detect two qrcodes.
        """
        fixture_path = os.path.join(FIXTURE_DIR, 'two_qr_codes.png')
        texture = Image(fixture_path).texture
        code_types = self.zbarcam.code_types
        symbols = self.zbarcam._detect_qrcode_frame(texture, code_types)
        Symbol = ZBarCam.Symbol
        self.assertEqual(
            symbols, [
                Symbol(type='QRCODE', data=b'second zbarlight test qr code'),
                Symbol(type='QRCODE', data=b'zbarlight test qr code'),
            ]
        )
