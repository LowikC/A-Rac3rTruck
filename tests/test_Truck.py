import time
from context import atruck
from atruck.Truck import Truck
from atruck.EngineClient import EngineClient

if __name__ == "__main__":
    engine = EngineClient(server_url="http://lowik.sytes.net", port=53117)
    print("Engine created")
    time.sleep(2)
    truck = Truck(engine)
    print("Starting truck")
