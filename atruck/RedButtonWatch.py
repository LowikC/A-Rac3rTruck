import threading
import logging
import time
from ev3dev.ev3 import TouchSensor
from FullStop import FullStop


class RedButtonWatch(threading.Thread):
    def __init__(self, status):
        """
        Check if the red button if pressed.
        If yes, we set the status.over to True
        :param status: Shared TruckStatus.
        """
        self.period_s = 0.2
        self.min_pressed_time_s = 1.0
        self.touch = TouchSensor()
        self.last_pressed_time_s = None
        self.status = status
        self.exit = threading.Event()
        super(RedButtonWatch, self).__init__()

    def run(self):
        while not self.exit.is_set():
            if not self.touch.value(0):
                self.last_pressed_time_s = None
            elif self.last_pressed_time_s is None:
                self.last_pressed_time_s = time.time()

            if not self.status.over and self.last_pressed_time_s is not None:
                elapsed_time_s = time.time() - self.last_pressed_time_s
                if elapsed_time_s >= self.min_pressed_time_s:
                    self.status.over = True
                    FullStop().run(self.status)
                    logging.info("Red button pushed - Stop truck")
            time.sleep(self.period_s)

    def join(self, timeout=None):
        self.exit.set()
        super(RedButtonWatch, self).join(timeout)
