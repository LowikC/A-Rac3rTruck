from ev3dev.auto import *

m = Motor(OUTPUT_B)
print("Test")
m.run_timed(time_sp=20000, speed_sp=500)
print("Test")

