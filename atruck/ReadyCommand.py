import logging
import os
from TruckCommand import TruckCommand
from ev3dev.ev3 import Sound

description = {"name": "ReadyCommand", "kwargs": {}}


class ReadyCommand(TruckCommand):
    def __init__(self):
        current_dir = os.path.dirname(os.path.realpath(__file__))
        self.wav = os.path.join(current_dir, "../data/sounds/ready.wav")
        super(ReadyCommand, self).__init__()

    def run(self, status):
        Sound.play(self.wav)
        logging.info("Run ready command")
        status.ready = True

    def stop(self):
        pass
