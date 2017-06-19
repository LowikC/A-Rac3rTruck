import threading
import time
from Camera import Camera, NoImageException


class CameraStreamer(threading.Thread):
    def __init__(self, images_queue, device_id=0):
        """
        Process that will capture images from a video device and store them in a queue.
        When the queue is full, the oldest image is discarded.
        :param images_queue: Queue that will store the captured images and their timestamp.
        :param device_id: Id of the camera device used to grab images.
        """
        self.exit = threading.Event()
        self.camera = Camera(device_id)
        self.images_queue = images_queue
        self.time_between_frame_s = 0.002
        super(CameraStreamer, self).__init__()

    def run(self):
        while not self.exit.is_set():
            try:
                image_bgr, timestamp_s = self.camera.next_image()
                if self.images_queue.full():
                    _ = self.images_queue.get_nowait()
                self.images_queue.put((image_bgr, timestamp_s))
            except NoImageException:
                pass
            time.sleep(self.time_between_frame_s)

    def join(self, timeout=None):
        self.exit.set()
        super(CameraStreamer, self).join(timeout)
