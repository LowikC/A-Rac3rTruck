from abc import ABCMeta, abstractmethod


class TruckCommand(object):
    """
    Provides a uniform interface for all commands to run on the Truck.
    """
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def stop(self):
        """
        Stop all actuators run by the command.
        """
        pass

    @abstractmethod
    def run(self, status):
        """
        Start the command and update the truck status.
        This must be a non-blocking method.
        :param status: The current truck status.
        """
        pass
