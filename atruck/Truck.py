import time
from Queue import Queue
from CameraStreamer import CameraStreamer
import cv2


class Truck(object):
    def __init__(self):
        self.camera_images = Queue(maxsize=4)
        self.camera_streamer = CameraStreamer(self.camera_images, device_id=0)

    def run(self):
        self.camera_streamer.start()
        for i in range(10):
            try:
                timestamp_s, image_bgr = \
                    self.camera_images.get(block=True, timeout=0.5)
                print("Timestamp: ", timestamp_s)
                cv2.imwrite("/home/robot/{}.jpg".format(timestamp_s), image_bgr)
                time.sleep(0.1)
            except Queue.Empty:
                print("Can't get an image")
                self.stop()
        self.stop()

    def stop(self):
        self.camera_streamer.join()

    def find_checkpoint(self):
        pass

    def go_to(self, target, speed=None):
        pass


if __name__ == "__main__":
    truck = Truck()
    truck.run()