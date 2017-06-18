from TruckCommand import TruckCommand
from ev3dev.ev3 import LargeMotor, OUTPUT_B, OUTPUT_C


class FullStop(TruckCommand):
    def __init__(self):
        """
        Stop the motors.
        """
        self.left_motor = LargeMotor(address=OUTPUT_B)
        self.right_motor = LargeMotor(address=OUTPUT_C)
        super(FullStop, self).__init__()

    def stop(self):
        pass

    def run(self, status):
        self.left_motor.stop()
        self.right_motor.stop()

