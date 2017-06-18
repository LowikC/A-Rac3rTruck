import time
import logging
from Queue import Queue
from CameraStreamer import CameraStreamer
from RedButtonWatch import RedButtonWatch
from CollisionWatch import CollisionWatch
from TruckStatus import TruckStatus


class Truck(object):
    def __init__(self, engine):
        self.sleep_time_s = 0.01
        self.status = TruckStatus()
        self.camera_images = Queue(maxsize=2)
        self.camera_streamer = CameraStreamer(self.camera_images, device_id=0)
        self.camera_streamer.start()
        self.red_button_watch = RedButtonWatch(self.status)
        self.red_button_watch.start()
        self.collision_watch = CollisionWatch(self.status)
        self.collision_watch.start()
        self.engine = engine
        time.sleep(2)

    def run(self):
        logging.debug("Truck start running")
        while not self.status.over:
            im_bgr, timestamp_s = self.camera_images.get(block=True, timeout=1)
            logging.debug("Got image, ts=", timestamp_s)
            command = self.engine.get_command(im_bgr, timestamp_s, self.status)
            logging.debug("Received command: \n", command)
            command.run(self.status)
            time.sleep(self.sleep_time_s)

        self.stop_all()

    def stop_all(self):
        logging.debug("Stopping...")
        self.red_button_watch.join()
        self.collision_watch.join()
        self.camera_streamer.join()
        logging.debug("All threads joined")
