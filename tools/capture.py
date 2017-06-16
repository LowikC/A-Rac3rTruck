import cv2
from Queue import Queue

from context import atruck
from atruck.CameraStreamer import CameraStreamer


if __name__ == "__main__":
    camera_images = Queue(maxsize=4)
    camera_streamer = CameraStreamer(camera_images, device_id=0)
    camera_streamer.start()

    for _ in xrange(20):
        im, ts = camera_images.get(block=True, timeout=2)
        ts_str = str(int(ts))
        cv2.imwrite("/home/robot/im_{ts}.jpg".format(ts=ts_str), im)
        print("Capture at {ts}".format(ts=ts_str))

    camera_streamer.join()
