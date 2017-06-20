import cv2
from Queue import Queue
import os
import argparse
from sys import stdout

from context import atruck
from atruck.CameraStreamer import CameraStreamer


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Capture images from the camera and store them on disk')
    parser.add_argument('--save_dir',
                        type=str, default="/home/robot/",
                        help='Directory to save thee images.')
    parser.add_argument('--period_s',
                        type=float, default=1,
                        help='Time between each image (in sec)')
    parser.add_argument('--num', type=int, default=10,
                        help='Number of images to save')
    parser.add_argument('--width',
                        type=int, default=640,
                        help='Width of the images.')
    parser.add_argument('--height',
                        type=int, default=480,
                        help='Height of the images')
    parser.add_argument('--device',
                        type=int, default=0,
                        help='Device ID')
    args = parser.parse_args()

    camera_images = Queue(maxsize=2)
    camera_streamer = CameraStreamer(camera_images,
                                     device_id=args.device,
                                     resolution=(args.width, args.height))
    camera_streamer.start()
    print("Start capture...")
    for n in xrange(args.num):
        im, ts = camera_images.get(block=True, timeout=2)
        tms = int(round(ts * 1000))
        cv2.imwrite(os.path.join(args.save_dir,
                                 "im_{tms}.jpg".format(tms=tms)),
                    im)
        stdout.write("\r{n}".format(n=n))
        stdout.flush()
    stdout.write("\rStop capture\n")
    camera_streamer.join()
