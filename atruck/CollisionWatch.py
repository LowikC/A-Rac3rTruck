import threading
import logging
import time
from ev3dev.ev3 import InfraredSensor, INPUT_4
from FullStop import FullStop


class CollisionWatch(threading.Thread):
    def __init__(self, status):
        """
        Look for collision using the infrared sensor.
        Below a given distance threshold, we trigger a full stop.
        :param status: Shared TruckStatus.
        """
        self.period_s = 0.1
        self.distance_threshold = 5.0
        self.time_below_threshold_s = 0.2
        self.time_above_threshold_s = 2.0
        self.ir_sensor = InfraredSensor(INPUT_4)
        self.ir_sensor.mode = InfraredSensor.MODE_IR_PROX
        self.last_below_threshold_time_s = None
        self.last_above_threshold_time_s = None
        self.status = status
        self.exit = threading.Event()
        super(CollisionWatch, self).__init__()

    def run(self):
        while not self.exit.is_set():
            distance = self.ir_sensor.value(0)
            if distance > self.distance_threshold:
                self.last_below_threshold_time_s = None
                if self.last_above_threshold_time_s is None:
                    self.last_above_threshold_time_s = time.time()
            else:
                self.last_above_threshold_time_s = None
                if self.last_below_threshold_time_s is None:
                    self.last_below_threshold_time_s = time.time()

            if not self.status.collision and self.last_below_threshold_time_s is not None:
                elapsed_time_s = time.time() - self.last_below_threshold_time_s
                if elapsed_time_s >= self.time_below_threshold_s:
                    self.status.collision = True
                    FullStop().run(self.status)
                    logging.info("Collision detected - Full stop")
            elif self.status.collision and self.last_above_threshold_time_s is not None:
                elapsed_time_s = time.time() - self.last_above_threshold_time_s
                if elapsed_time_s >= self.time_above_threshold_s:
                    self.status.collision = False
                    logging.info("Collision avoided - collision flag to false")

            time.sleep(self.period_s)

    def join(self, timeout=None):
        self.exit.set()
        super(CollisionWatch, self).join(timeout)
