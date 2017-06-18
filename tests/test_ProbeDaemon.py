import time
from context import atruck
from atruck.ProbeDaemon import ProbeDaemon

if __name__ == "__main__":
    probe = ProbeDaemon(server_url="http://lowik.sytes.net", port=53117)
    probe.start()
    for _ in range(20):
        print(probe.up())
        time.sleep(1)
