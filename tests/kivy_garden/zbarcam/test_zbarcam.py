import os
from unittest import mock

import pytest
from kivy.base import EventLoop
from kivy.core.image import Image

from kivy_garden.zbarcam import ZBarCam
from kivy_garden.zbarcam.zbarcam import XZbarDecoder, ZBarDecoder

FIXTURE_DIR = os.path.join(
    os.path.abspath(
        os.path.join(__file__, os.pardir, os.pardir, os.pardir, 'fixtures')
    )
)
# https://github.com/kivy/kivy/blob/1.11.1/doc/sources/faq.rst
EventLoop.ensure_window()


def patch_is_usable(implementation, m_is_usable):
    return mock.patch(
        f'kivy_garden.zbarcam.zbarcam.{implementation}.is_usable', m_is_usable)


class TestZBarDecoder:
    """Tests the ZBarDecoder "abstract" class."""

    def test_validate_code_types(self):
        """
        Checks `validate_code_types()` properly relies on
        `get_available_code_types()` for valid types.
        """
        zbar_decoder = ZBarDecoder()
        m_get_available_code_types = mock.Mock(
            return_value=["QRCODE", "EAN13", "DATABAR"])
        zbar_decoder.get_available_code_types = m_get_available_code_types
        code_types = ["QRCODE", "EAN13"]
        assert zbar_decoder.validate_code_types(code_types) is None
        code_types = ["QRCODE", "EAN13", "DOES_NOT_EXIST"]
        with pytest.raises(ValueError, match="Invalid code types"):
            zbar_decoder.validate_code_types(code_types)


class TestZBarCam:

    def setup_method(self):
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
        assert symbols == []

    def test_detect_qrcode_frame_one_qrcode(self):
        """
        Checks `_detect_qrcode_frame()` can detect one qrcode.
        """
        fixture_path = os.path.join(FIXTURE_DIR, 'one_qr_code.png')
        texture = Image(fixture_path).texture
        code_types = self.zbarcam.code_types
        symbols = self.zbarcam._detect_qrcode_frame(texture, code_types)
        assert symbols == [
            ZBarCam.Symbol(type='QRCODE', data=b'zbarlight test qr code')
        ]

    def test_detect_qrcode_frame_one_qrcode_one_ean(self):
        """
        Checks `_detect_qrcode_frame()` can detect one qrcode and one ean.
        """
        fixture_path = os.path.join(FIXTURE_DIR, 'one_qr_code_and_one_ean.png')
        texture = Image(fixture_path).texture
        code_types = self.zbarcam.code_types
        symbols = self.zbarcam._detect_qrcode_frame(texture, code_types)
        assert symbols == [
            ZBarCam.Symbol(type='QRCODE', data=b'zbarlight test qr code'),
            ZBarCam.Symbol(type='UPCA', data=b'012345678905')
        ]

    def test_detect_qrcode_frame_two_qrcodes(self):
        """
        Checks `_detect_qrcode_frame()` can detect two qrcodes.
        """
        fixture_path = os.path.join(FIXTURE_DIR, 'two_qr_codes.png')
        texture = Image(fixture_path).texture
        code_types = self.zbarcam.code_types
        symbols = self.zbarcam._detect_qrcode_frame(texture, code_types)
        Symbol = ZBarCam.Symbol
        assert symbols == [
            Symbol(type='QRCODE', data=b'second zbarlight test qr code'),
            Symbol(type='QRCODE', data=b'zbarlight test qr code'),
        ]


class TestXZbarDecoder:

    def test_singleton(self):
        """
        New instances of XZbarDecoder should share the same instance of
        zbar_decoder.
        """
        xzbar_decoder = XZbarDecoder()
        zbar_decoder = xzbar_decoder.zbar_decoder
        assert zbar_decoder == XZbarDecoder().zbar_decoder

    def test_no_zbar_implementation_available(self):
        """
        Makes sure `ImportError` is raised on no available implementations.
        """
        # resets the singleton instance to force reprobing
        XZbarDecoder.zbar_decoder = None
        m_is_usable = mock.Mock(return_value=False)
        with patch_is_usable("PyZBarDecoder", m_is_usable), \
                patch_is_usable("ZBarLightDecoder", m_is_usable), \
                pytest.raises(
                    ImportError, match="No zbar implementation available"):
            XZbarDecoder()
