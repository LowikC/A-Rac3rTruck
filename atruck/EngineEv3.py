import os
import cv2
import logging
from GreenFlag import GreenFlag
from cvision_utils import median_hsv
from ReadyCommand import ReadyCommand
from GoCommand import  GoCommand
from StraightRun import StraightRun
from NoCommand import NoCommand


class EngineEv3(object):
    def __init__(self):
        self.upload_dir = "/home/robot/atruck/data/tmp/"
        if not os.path.exists(self.upload_dir):
            os.makedirs(self.upload_dir)

        self.green_flag = GreenFlag()

    def get_command(self, im_bgr, timestamp_s, status):
        logging.info("Processing {ts}".format(ts=timestamp_s))
        self.save_image(im_bgr, timestamp_s)
        if not status.go:
            logging.debug("Truck not started, check for green flag")
            im_bgr_80x60 = cv2.resize(im_bgr, (80, 60),
                                      interpolation=cv2.INTER_LINEAR)
            im_hsv = median_hsv(im_bgr_80x60, blur_size=0)
            (ready, go) = self.green_flag.update(im_hsv)
            if ready:
                logging.debug("Return ready command")
                return ReadyCommand()
            elif go:
                logging.debug("Return Go command")
                return GoCommand()
            else:
                logging.debug("Return No command")
                return NoCommand()

        elif not status.collision and not status.over:
            logging.debug("Truck is not stopped, apply usual process")
            return StraightRun(speed_rps=1, time_ms=4000)
        else:
            logging.debug("Truck is stopped, do nothing")
            return NoCommand()

    def save_image(self, im_bgr, timestamp_s):
        timestamp_ms = int(round(timestamp_s * 1000))
        cv2.imwrite(os.path.join(self.upload_dir,
                                 "{tms}.jpg".format(tms=timestamp_ms)),
                    im_bgr)
