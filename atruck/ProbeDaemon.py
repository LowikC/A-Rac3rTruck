import time
import multiprocessing
import urlparse
from requests import get, codes


class ProbeDaemon(multiprocessing.Process):
    def __init__(self, server_url, endpoint="/probe", period_s=1):
        """
        Probe a given server, and set down_event if the server doesn't respond.
        :param server_url: URL of the server
        :param endpoint: Endpoint on the server for probing
        :param period_s: Time between 2 probes
        """
        self.probe_url = urlparse.urljoin(server_url, endpoint)
        self.down_event = multiprocessing.Event()
        self.period_s = period_s
        self.daemon = True
        super(ProbeDaemon, self).__init__()

    def run(self):
        while True:
            probe = get(self.probe_url)
            if probe.status_code != codes.ok:
                self.down_event.set()
            else:
                self.down_event.clear()
            time.sleep(self.period_s)

    def up(self):
        """
        Get current server status (on last probe)
        :return: True is the server is up. 
        """
        return not self.down_event.is_set()
