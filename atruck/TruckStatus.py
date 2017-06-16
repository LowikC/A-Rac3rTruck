import multiprocessing


class TruckStatus(object):
    def __init__(self):
        self.lock = multiprocessing.Lock()
        self._over = False

    @property
    def over(self):
        return self._over

    @over.setter
    def over(self, new_value):
        with self.lock.acquire():
            self._over = new_value


