from TruckCommand import TruckCommand


class DummyCommand(TruckCommand):
    def __init__(self, dummy_args):
        self.dummy_args = dummy_args

    def run(self, status):
        print(self.dummy_args)
        pass

    def stop(self):
        pass
