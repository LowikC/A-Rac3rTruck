import os
import cv2
import time
from context import atruck
from atruck.GreenFlag import GreenFlag
from atruck.cvision_utils import median_hsv


if __name__ == "__main__"
    current_dir = os.path.dirname(os.path.realpath(__file__))
    im_bgr = cv2.imread(os.path.join(current_dir,
                                     "../tests/data/GreenFlag_with_flag.jpg"))
    im_bgr = cv2.resize(im_bgr, (160, 120), interpolation=cv2.INTER_LINEAR)
    im_hsv = median_hsv(im_bgr)
    green_flag = GreenFlag()

    n_loops = 10
    start_s = time.time()
    for _ in xrange(n_loops):
        _ = green_flag._contains_green_flag(im_hsv)
    elapsed_s = (time.time() - start_s ) /n_loops

    print("Average time: {t} [ms]".format(t=int(round(elapsed_s * 1000))))