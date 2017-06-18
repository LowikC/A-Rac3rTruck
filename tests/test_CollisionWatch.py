import time
from context import atruck
from atruck.CollisionWatch import CollisionWatch
from atruck.TruckStatus import TruckStatus

if __name__ == "__main__":
    status = TruckStatus()
    cw = CollisionWatch(status)
    cw.start()

    for _ in range(20):
        print(status.collision)
        time.sleep(1)

    cw.join()
