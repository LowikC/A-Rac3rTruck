import logging
from atruck.Truck import Truck
from atruck.EngineClient import EngineClient

if __name__ == "__main__":
    log_format = "[%(levelname)s] [%(asctime)s] [%(message)s] [%(funcName)s]"
    logging.basicConfig(format=log_format, filename="/home/robot/atruck/logs/log", level=logging.DEBUG)

    engine = EngineClient(server_url="http://lowik.sytes.net", port=53117)
    logging.debug("Engine created")
    time.sleep(2)
    truck = Truck(engine)
    logging.info("Starting truck")
    truck.run()
