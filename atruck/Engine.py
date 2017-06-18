import cv2


class Engine(object):
    def __init__(self):
        pass

    def process(self, im_bgr, timestamp_ms, status):
        cv2.imwrite("/home/lowik/{tms}.jpg".format(tms=timestamp_ms), im_bgr)
        cmd = {
            "name": "StraightRun",
            "kwargs": {"speed_rps": 1, "time_ms": 2000}
        }

        return {"cmd": cmd,
                "status": status.to_dict()}
