import os
import shutil
import threading
import time
import unittest
from functools import partial
from tempfile import mkdtemp
# from unittest import mock
# 
# from hexbytes import HexBytes
from kivy.clock import Clock
# from requests.exceptions import ConnectionError
# 
from zbarcam.zbarcam import DemoApp, ZBarCam


class UITestCase(unittest.TestCase):

    # sleep function that catches `dt` from Clock
    def pause(*args):
        time.sleep(0.000001)

    def advance_frames(self, count):
        """
        Borrowed from Kivy 1.10.0+ /kivy/tests/common.py
        GraphicUnitTest.advance_frames()
        Makes it possible to to wait for UI to process, refs #110.
        """
        from kivy.base import EventLoop
        for i in range(count):
            EventLoop.idle()

    def helper_test_open_application(self, app):
        """
        Makes sure the ZBarCam widget is rendered, hence the application
        started without crashing.
        """
        self.assertEqual(app.root.ids.zbarcam.__class__, ZBarCam)

    # main test function
    def run_test(self, app, *args):
        Clock.schedule_interval(self.pause, 0.000001)
        # lets it finish to init
        self.advance_frames(1)
        self.helper_test_open_application(app)
        # Comment out if you are editing the test, it'll leave the
        # Window opened.
        # app.stop()

    # same named function as the filename(!)
    def test_ui_base(self):
        app = DemoApp()
        p = partial(self.run_test, app)
        Clock.schedule_once(p, 0.000001)
        app.run()


if __name__ == '__main__':
    unittest.main()
