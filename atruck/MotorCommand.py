from BaseCommand import BaseCommand
from ev3dev.ev3 import LargeMotor


class LargeMotorTimed(BaseCommand):
    def __init__(self, uid, speed_rps, time_ms=None):
        self.motor = LargeMotor(address=uid)
        self.time_ms = time_ms
        self.speed_sp = speed_rps * self.motor.count_per_rot
        super(LargeMotorTimed, self).__init__()

    def stop(self):
        self.motor.stop()
        self.motor.

    def run(self):
        self.running = True
        if self.time_ms is None:
            self.motor.run_forever(speed_sp=self.speed_sp)
        else:
            self.motor.run_timed(speed_sp=self.speed_sp,
                                 time_sp=self.time_ms)

