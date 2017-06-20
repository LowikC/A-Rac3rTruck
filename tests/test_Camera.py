import unittest
import time
from context import atruck
from atruck.Camera import Camera, NoCameraException


class TestCamera(unittest.TestCase):
    def test_resolution_640x480(self):
        cam = Camera(device_id=0, resolution=(640, 480))
        im, ts = cam.next_image()
        self.assertEquals((480, 640, 3), im.shape)

    def test_resolution_320x240(self):
        cam = Camera(device_id=0, resolution=(320, 240))
        im, ts = cam.next_image()
        self.assertEquals((240, 320, 3), im.shape)

    def test_resolution_160x120(self):
        cam = Camera(device_id=0, resolution=(160, 120))
        im, ts = cam.next_image()
        self.assertEquals((120, 160, 3), im.shape)

    def test_multiget(self):
        cam = Camera()
        previous_ts = time.time()
        for _ in range(5):
            im, ts = cam.next_image()
            self.assertGreater(ts, previous_ts)
            time.sleep(0.5)

    def test_no_camera(self):
        with self.assertRaises(NoCameraException) as context:
            _ = Camera(999)

        print(context.exception)

if __name__ == '__main__':
    unittest.main()
