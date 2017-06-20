import time
import logging
from TruckCommand import TruckCommand
from TruckMotors import direction_motor


class CalibrateDirection(TruckCommand):
    def __init__(self):
        self.motor = direction_motor
        self.speed_rps = 2
        self.speed_countps = self.motor.count_per_rot * self.speed_rps
        # For unit test
        self.zero_position = None
        super(CalibrateDirection, self).__init__()

    def stop(self):
        pass

    def run(self, status):
        # We want to turn by at most n_rots rotations
        # Then multiply by 2 to be sure it will block
        n_rots = 1.0
        time_ms = (n_rots / self.speed_rps * 2) * 1000
        # Sleep for the same time + 20% margin
        time_wait_s = time_ms * 1.2 / 1000

        logging.debug("Run direction to the right, until it blocks")
        self.motor.run_timed(speed_sp=self.speed_countps, time_sp=time_ms)
        time.sleep(time_wait_s)
        right_pos = self.motor.position

        logging.debug("Run direction to the left, until it blocks")
        self.motor.run_timed(speed_sp=-self.speed_countps, time_sp=time_ms)
        time.sleep(time_wait_s)
        left_pos = self.motor.position

        total = abs(left_pos - right_pos)
        self.zero_position = int(round(min(left_pos, right_pos) + total/2))

        logging.debug("Run to zero position + an offset to overshoot slightly")
        offset = 10
        self.motor.run_to_abs_pos(speed_sp=self.speed_countps,
                                  position_sp=self.zero_position + offset)
        time.sleep(time_wait_s)

        logging.debug("Run to exact zero position")
        self.motor.run_to_abs_pos(speed_sp=self.speed_countps,
                                  position_sp=self.zero_position)
        time.sleep(time_wait_s)

        logging.debug("Reset motor, so that current position is 0")
        self.motor.reset()
