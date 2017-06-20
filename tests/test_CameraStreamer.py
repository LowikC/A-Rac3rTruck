import unittest
import time
from Queue import Queue
from context import atruck
from atruck.CameraStreamer import CameraStreamer


class TestCameraStreamer(unittest.TestCase):
    def test_start(self):
        queue = Queue(4)
        streamer = CameraStreamer(queue, resolution=(160, 120))
        time.sleep(2)
        self.assertTrue(queue.empty())

    def test_fill_queue(self):
        queue = Queue(4)
        streamer = CameraStreamer(queue, resolution=(160, 120))

        streamer.start()
        time.sleep(2)
        streamer.join()

        self.assertFalse(queue.empty())

    def test_join(self):
        queue = Queue(4)
        streamer = CameraStreamer(queue, resolution=(160, 120))

        streamer.start()
        time.sleep(2)
        streamer.join()
        self.assertFalse(queue.empty())

        while not queue.empty():
            _ = queue.get_nowait()

        time.sleep(2)
        self.assertTrue(queue.empty())

    def test_queue(self):
        queue = Queue(2)
        streamer = CameraStreamer(queue, resolution=(160, 120))

        streamer.start()
        time.sleep(3)
        self.assertFalse(queue.empty())

        for _ in xrange(4):
            _ = queue.get(True, 1)

        streamer.join()

    def test_full(self):
        queue = Queue(1)
        streamer = CameraStreamer(queue, resolution=(160, 120))

        streamer.start()
        time.sleep(5)
        streamer.join()

    def test_resolution_640x480(self):
        queue = Queue(2)
        streamer = CameraStreamer(queue, resolution=(640, 480))

        streamer.start()
        time.sleep(3)
        streamer.join()

        im, _ = queue.get_nowait()
        self.assertEquals((480, 640, 3), im.shape)

    def test_resolution_320x240(self):
        queue = Queue(2)
        streamer = CameraStreamer(queue, resolution=(320, 240))

        streamer.start()
        time.sleep(3)
        streamer.join()

        im, _ = queue.get_nowait()
        self.assertEquals((240, 320, 3), im.shape)

    def test_resolution_160x120(self):
        queue = Queue(2)
        streamer = CameraStreamer(queue, resolution=(160, 120))

        streamer.start()
        time.sleep(3)
        streamer.join()

        im, _ = queue.get_nowait()
        self.assertEquals((120, 160, 3), im.shape)

    def test_timestamp(self):
        queue = Queue(4)
        streamer = CameraStreamer(queue, resolution=(160, 120))

        start_time = time.time()
        streamer.start()
        time.sleep(4)
        streamer.join()

        while not queue.empty():
            _, ts = queue.get_nowait()
            self.assertGreater(ts, start_time)
            start_time = ts

if __name__ == '__main__':
    unittest.main()
