from TruckCommand import TruckCommand


class TrajectoryRun(TruckCommand):
    def __init__(self):
        """
        """
        super(TruckCommand, self).__init__()
        pass

    def stop(self):
        pass

    def run(self, status):
        if status.over or status.collision:
            return
