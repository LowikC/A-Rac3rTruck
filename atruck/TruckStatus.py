import multiprocessing


class TruckStatus(object):
    def __init__(self, **kwargs):
        self.lock = multiprocessing.Lock()
        self._over = kwargs.get("over", False)
        self._collision = kwargs.get("collision", False)

    def to_dict(self):
        data = dict()
        data['over'] = self.over
        data['collision'] = self.collision
        return data

    @property
    def over(self):
        with self.lock:
            return self._over

    @over.setter
    def over(self, new_value):
        with self.lock:
            self._over = new_value

    @property
    def collision(self):
        with self.lock:
            return self._collision

    @collision.setter
    def collision(self, new_value):
        with self.lock:
            self._collision = new_value


