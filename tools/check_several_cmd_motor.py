import time
from ev3dev.ev3 import LargeMotor, OUTPUT_B

left_motor = LargeMotor(address=OUTPUT_B)
left_motor.run_timed(speed_sp=360, time_sp=5000)
time.sleep(3)
left_motor.run_timed(speed_sp=360, time_sp=5000)
time.sleep(3)
left_motor.run_timed(speed_sp=360, time_sp=5000)
time.sleep(3)
