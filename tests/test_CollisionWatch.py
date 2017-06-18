import time
from context import atruck
from atruck.CollisionWatch import CollisionWatch
from atruck.TruckStatus import TruckStatus

if __name__ == "__main__":
    status = TruckStatus()
    cw = CollisionWatch(status)
    cw.start()

    for _ in range(500):
        print(status.collision)
        time.sleep(0.2)

    cw.join()
