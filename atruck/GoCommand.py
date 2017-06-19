from TruckCommand import TruckCommand
from ev3dev.ev3 import Sound

description = {"name": "GoCommand", "kwargs": {}}


class ReadyCommand(TruckCommand):
    def __init__(self):
        super(ReadyCommand, self).__init__()

    def run(self, status):
        status.go = True
        Sound.speak("Go!")

    def stop(self):
        pass
