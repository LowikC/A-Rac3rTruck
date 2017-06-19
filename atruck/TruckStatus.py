import threading


class TruckStatus(object):
    def __init__(self, **kwargs):
        """
        Thread safe structure to share the truck status (speed, position, ...)
        :param kwargs: 
        """
        # todo: One lock per field? Another threading structure?
        self.lock = threading.Lock()
        self._over = kwargs.get("over", False)
        self._collision = kwargs.get("collision", False)
        self._ready = kwargs.get("ready", False)
        self._go = kwargs.get("go", False)

    def to_dict(self):
        data = dict()
        data['over'] = self.over
        data['collision'] = self.collision
        data['ready'] = self.ready
        data['go'] = self.go
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

    @property
    def ready(self):
        with self.lock:
            return self._ready

    @ready.setter
    def ready(self, new_value):
        with self.lock:
            self._ready = new_value

    @property
    def go(self):
        with self.lock:
            return self._go

    @go.setter
    def go(self, new_value):
        with self.lock:
            self._go = new_value
