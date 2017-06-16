from abc import ABCMeta, abstractmethod


class BaseCommand(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def run(self):
        pass