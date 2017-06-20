import logging
from TruckCommand import TruckCommand
from ev3dev.ev3 import Sound

description = {"name": "ReadyCommand", "kwargs": {}}


class ReadyCommand(TruckCommand):
    def __init__(self):
        super(ReadyCommand, self).__init__()

    def run(self, status):
        logging.info("Run ready command")
        status.ready = True
        Sound.speak("Ready!")

    def stop(self):
        pass
