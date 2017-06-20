from TruckCommand import TruckCommand
from TruckMotors import left_motor, right_motor


class StraightRun(TruckCommand):
    def __init__(self, speed_rps, time_ms=None):
        """
        Run the left motor.
        :param speed_rps: Desired speed in rotations per second.
        :param time_ms: Desired time to run. If None, will run forever.
        """
        self.left_motor = left_motor
        self.right_motor = right_motor
        self.time_ms = time_ms
        self.left_speed_sp = -speed_rps * self.left_motor.count_per_rot
        self.right_speed_sp = -speed_rps * self.right_motor.count_per_rot
        super(StraightRun, self).__init__()

    def stop(self):
        self.left_motor.stop()
        self.right_motor.stop()

    def run(self, status):
        if status.over or status.collision:
            return
        if self.time_ms is None:
            self.left_motor.run_forever(speed_sp=self.left_speed_sp)
            self.right_motor.run_forever(speed_sp=self.right_speed_sp)
        else:
            self.left_motor.run_timed(speed_sp=self.left_speed_sp,
                                      time_sp=self.time_ms)
            self.right_motor.run_timed(speed_sp=self.right_speed_sp,
                                       time_sp=self.time_ms)

