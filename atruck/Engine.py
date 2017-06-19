import os
import cv2
from GreenFlag import GreenFlag
from cvision_utils import median_hsv


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

        (ready, go) = self.green_flag.update(im_hsv)
        if ready:
            return {"cmd": "ReadyCommand",
                    "status": status.to_dict()}
        elif go:
            return {"cmd": "GoCommand",
                    "status": status.to_dict()}

        cmd = {
            "name": "StraightRun",
            "kwargs": {"speed_rps": 1, "time_ms": 4000}
        }

        return {"cmd": cmd,
                "status": status.to_dict()}

    def save_image(self, im_bgr, timestamp_ms):
        cv2.imwrite(os.path.join(self.upload_dir,
                                 "{tms}.jpg".format(tms=timestamp_ms)),
                    im_bgr)
