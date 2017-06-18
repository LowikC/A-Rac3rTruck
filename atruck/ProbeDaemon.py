import time
import multiprocessing
from requests import get, codes, exceptions


class ProbeDaemon(multiprocessing.Process):
    def __init__(self, server_url, port, endpoint="/probe", period_s=1):
        """
        Probe a given server, and set down_event if the server doesn't respond.
        :param server_url: URL of the server
        :param endpoint: Endpoint on the server for probing
        :param period_s: Time between 2 probes
        """
        self.probe_url = "{url}:{port}{endpoint}"\
            .format(url=server_url, port=port, endpoint=endpoint)
        self.down_event = multiprocessing.Event()
        self.period_s = period_s
        self.timeout = 0.2
        super(ProbeDaemon, self).__init__()
        # It seems we need to set the value after the call to base class __init__
        self.daemon = True

    def run(self):
        while True:
            try:
                probe = get(self.probe_url, timeout=self.timeout)
                if probe.status_code != codes.ok:
                    self.down_event.set()
                else:
                    self.down_event.clear()
            except exceptions.ConnectionError:
                self.down_event.set()
            except exceptions.ReadTimeout:
                self.down_event.set()

            time.sleep(self.period_s)

    def up(self):
        """
        Get current server status (on last probe)
        :return: True is the server is up. 
        """
        return not self.down_event.is_set()
