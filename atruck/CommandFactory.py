import importlib
import logging


class InvalidCommandDict(Exception):
    pass


class CommandFactory(object):
    def __init__(self):
        pass

    @staticmethod
    def from_dict(cmd):
        """
        Build a TruckCommand based on its class name and parameters.
        :param cmd: A dict with two mandatory field: "name" and "kwargs"
        The name field must be a name of Command class.
        The kwargs must contains the parameters to instantiate this class.
        :return: A TruckCommand corresponding to the description
        """
        if "name" not in cmd or "kwargs" not in cmd:
            raise InvalidCommandDict("{c} misses mandatory fields"
                                     .format(c=cmd))

        name = cmd["name"]
        kwargs = cmd["kwargs"]
        TruckCommandSubClass = getattr(
            importlib.import_module("atruck." + name),
            name)
        return TruckCommandSubClass(**kwargs)
