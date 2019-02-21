import os
import time
import unittest
from functools import partial
import mock
from kivy.clock import Clock
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

    @staticmethod
    def get_camera_class():
        """
        Continuous integration providers don't have a camera available.
        """
        if os.environ.get('CI', False):
            Camera = None
        else:
            from kivy.core.camera import Camera
        return Camera

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
        app.stop()

    # same named function as the filename(!)
    def test_ui_base(self):
        # uses the `wraps` parameter to conditionally enable/disable mock
        Camera = self.get_camera_class()
        with mock.patch('kivy.core.camera.Camera', wraps=Camera):
            app = DemoApp()
            p = partial(self.run_test, app)
            Clock.schedule_once(p, 0.000001)
            app.run()


if __name__ == '__main__':
    unittest.main()
