import time
from TruckCommand import TruckCommand
from TruckMotors import direction_motor


class CalibrateDirection(TruckCommand):
    def __init__(self):
        self.motor = direction_motor
        # For unit testing
        self.zero_position = None
        super(CalibrateDirection, self).__init__()

    def stop(self):
        pass

    def run(self, status):
        self.motor.run_timed(speed_sp=300, time_sp=2000)
        time.sleep(1)
        right_pos = self.motor.position
        print(right_pos)

        self.motor.run_timed(speed_sp=-300, time_sp=2000)
        time.sleep(1)
        left_pos = self.motor.position
        print(left_pos)

        total = abs(left_pos - right_pos)
        print(total)
        self.zero_position = int(round(min(left_pos, right_pos) + total/2))
        print(self.zero_position)
        self.motor.run_to_abs_pos(speed_sp=300,
                                  position_sp=self.zero_position)
        time.sleep(3)
        self.motor.reset()
