import time
from context import atruck
from atruck.RedButtonWatch import RedButtonWatch
from atruck.CollisionWatch import CollisionWatch
from atruck.TruckStatus import TruckStatus

if __name__ == "__main__":
    status = TruckStatus()
    rbw = RedButtonWatch(status)
    cw = CollisionWatch(status)
    rbw.start()
    cw.start()

    for _ in range(100):
        print(status.to_dict())
        time.sleep(0.2)

    rbw.join()
    cw.join()
