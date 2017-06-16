from ev3dev.auto import *
import time

s = InfraredSensor(INPUT_3)
print("modes: ", s.modes)
print("commands: ", s.commands)

s.mode = 'IR-PROX'

print("units: ", s.units)
print("decimals: ", s.decimals)
print("bin: ", s.bin_data_format)
while True:
    print("b: ", s.bin_data)
    print("v: ", s.value())
    time.sleep(1)

