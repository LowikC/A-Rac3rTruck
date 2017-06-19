from TruckCommand import TruckCommand
from ev3dev.ev3 import Sound


class ReadyCommand(TruckCommand):
    def __init__(self):
        super(ReadyCommand, self).__init__()

    def run(self, status):
        status.ready = True
        Sound.speak("Ready!")

    def stop(self):
        pass
