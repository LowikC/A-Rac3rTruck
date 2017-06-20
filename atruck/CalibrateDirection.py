import time
from TruckCommand import TruckCommand
from TruckMotors import direction_motor


class CalibrateDirection(TruckCommand):
    def __init__(self):
        self.motor = direction_motor
        super(CalibrateDirection, self).__init__()

    def stop(self):
        self.motor.stop()

    def run(self, status):
        self.motor.run_timed(speed_sp=100, time_sp=2000)
        time.sleep(2.5)
        right_pos = self.motor.position

        self.motor.run_timed(speed_sp=-100, time_sp=2000)
        time.sleep(2.5)
        left_pos = self.motor.position

        total = abs(left_pos - right_pos)
        center_pos = int(round(left_pos + total/2))

        self.motor.run_to_abs_pos(position_sp=center_pos)
        self.motor.reset()


