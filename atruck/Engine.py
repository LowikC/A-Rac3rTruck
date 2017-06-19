import os
import cv2
import logging
from GreenFlag import GreenFlag
from cvision_utils import median_hsv
from ReadyCommand import description as ready_command_desc
from GoCommand import description as go_command_desc
from NoCommand import description as no_command_desc


class Engine(object):
    def __init__(self):
        self.upload_dir = "/home/lowik/atruck-local/data/tmp/"
        if not os.path.exists(self.upload_dir):
            os.makedirs(self.upload_dir)

        self.green_flag = GreenFlag()
        pass

    def process(self, im_bgr, timestamp_ms, status):
        self.save_image(im_bgr, timestamp_ms)
        im_hsv = median_hsv(im_bgr)

        if not status.go:
            logging.info("Truck not started, check for green flag")
            (ready, go) = self.green_flag.update(im_hsv)
            if ready:
                return {
                    "cmd": ready_command_desc,
                    "status": status.to_dict()}
            elif go:
                return {"cmd": go_command_desc,
                        "status": status.to_dict()}
            else:
                return {"cmd": no_command_desc,
                        "status": status.to_dict()}

        elif not status.collision and not status.over:
            logging.info("Truck is not stopped, apply usual process")
            cmd = {
                "name": "StraightRun",
                "kwargs": {"speed_rps": 1, "time_ms": 4000}
            }

            return {"cmd": cmd,
                    "status": status.to_dict()}
        else:
            logging.info("Truck is stopped, do nothing")
            return {"cmd": no_command_desc,
                    "status": status.to_dict()}

    def save_image(self, im_bgr, timestamp_ms):
        cv2.imwrite(os.path.join(self.upload_dir,
                                 "{tms}.jpg".format(tms=timestamp_ms)),
                    im_bgr)
