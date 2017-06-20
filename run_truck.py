import logging
import argparse
from atruck.Truck import Truck
from atruck.EngineEv3 import EngineEv3 as EngineLocal


def setup_logging(log_filename):
    """
    Setup logging in log_filename and in the console.
    :param log_filename: Path to the log file.
    """
    logging.basicConfig(level=logging.DEBUG,
                        format='[%(levelname)s] [%(asctime)s] [%(message)s] [%(funcName)s]',
                        filename=log_filename,
                        filemode='w')

    # define a Handler which writes INFO messages or higher to
    #  the sys.stderr, with a simpler format.
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(levelname)-8s %(message)s')

    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Start Autonomous Rac3r Truck')
    parser.add_argument('--log',
                        type=str, default="/home/robot/atruck/logs/log",
                        help='Path to log file.')
    args = parser.parse_args()

    setup_logging(args.log)

    engine = EngineLocal()
    logging.debug("Engine created")
    truck = Truck(engine)
    logging.info("Starting truck")
    truck.run()
