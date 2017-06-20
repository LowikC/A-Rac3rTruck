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
        self.green_flag = GreenFlag()
        pass

    def get_command(self, im_bgr, timestamp_ms, status):
        im_hsv = median_hsv(im_bgr)

        if not status.go:
            logging.info("Truck not started, check for green flag")
            (ready, go) = self.green_flag.update(im_hsv)
            if ready:
                logging.info("Return ready command")
                return ReadyCommand()
            elif go:
                logging.info("Return Go command")
                return GoCommand()
            else:
                logging.info("Return No command")
                return NoCommand()

        elif not status.collision and not status.over:
            logging.info("Truck is not stopped, apply usual process")
            return StraightRun(speed_rps=1, time_ms=4000)
        else:
            logging.info("Truck is stopped, do nothing")
            return NoCommand()

