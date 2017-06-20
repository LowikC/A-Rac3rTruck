from ev3dev.ev3 import LargeMotor, MediumMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C

left_motor = LargeMotor(address=OUTPUT_B)
right_motor = LargeMotor(address=OUTPUT_C)
direction_motor = MediumMotor(address=OUTPUT_A)
