import unittest
import time
from context import atruck
from atruck.Camera import Camera, NoCameraException


class TestCamera(unittest.TestCase):
    def test_resolution(self):
        cam = Camera(device_id=0, resolution=(320, 240))
        im, ts = cam.next_image()
        self.assertEquals((240, 320, 3), im.shape)

    def test_multiget(self):
        cam = Camera()
        previous_ts = time.time()
        for _ in range(5):
            im, ts = cam.next_image()
            self.assertGreater(ts, previous_ts)
            time.sleep(0.5)

    def test_no_camera(self):
        try:
            cam = Camera(999)
        except NoCameraException:
            self.assertTrue(True)
            return
        self.assertTrue(False)

if __name__ == '__main__':
    unittest.main()
