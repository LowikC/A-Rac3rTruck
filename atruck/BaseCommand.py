from abc import ABCMeta, abstractmethod
import multiprocessing


class BaseCommand(multiprocessing.Process):
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def stop(self):
        pass
