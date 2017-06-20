from TruckCommand import TruckCommand
from ev3dev.ev3 import Sound

description = {"name": "GoCommand", "kwargs": {}}


class GoCommand(TruckCommand):
    def __init__(self):
        super(GoCommand, self).__init__()

    def run(self, status):
        status.go = True
        Sound.speak("Go!")

    def stop(self):
        pass
