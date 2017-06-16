from BaseCommand import BaseCommand
from ev3dev.ev3 import LargeMotor

class MotorCommand(BaseCommand):
    def __init__(self, motor, speed_sp, time_sp=None):
        self.motor = LargeMotor(motor)
        self.time_sp = time_sp
        self.speed_sp = speed_sp

    def stop(self):
        pass

    def run(self):
        if self.time_sp is None:
            self.motor.run_forever(speed_sp=)
        self.motor.run_timed()
        m.run_timed(time_sp=3000, speed_sp=500)
