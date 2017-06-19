from TruckCommand import TruckCommand

description = {"name": "NoCommand", "kwargs": {}}


class NoCommand(TruckCommand):
    def __init__(self):
        super(NoCommand, self).__init__()
        pass

    def run(self, status):
        pass

    def stop(self):
        pass
