import unittest
import time
from context import atruck
from atruck.Camera import Camera, NoCameraException


class TestCamera(unittest.TestCase):
    def test_resolution(self):
        cam = Camera()
        im, ts = cam.next_image()
        self.assertEquals((480, 640, 3), im.shape)

    def test_multiget(self):
        cam = Camera()
        previous_ts = time.time()
        for _ in range(5):
            im, ts = cam.next_image()
            self.assertGreater(ts, previous_ts)
            time.sleep(0.5)

    def test_no_camera(self):
        self.assertRaises(NoCameraException, Camera(999))

if __name__ == '__main__':
    unittest.main()
