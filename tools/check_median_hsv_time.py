import os
import cv2
import time
from context import atruck
from atruck.cvision_utils import median_hsv


if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.realpath(__file__))
    im_bgr = cv2.imread(os.path.join(current_dir,
                                     "../tests/data/GreenFlag_with_flag.jpg"))
    im_bgr = cv2.resize(im_bgr, (160, 120), interpolation=cv2.INTER_LINEAR)

    for blur_size in [0, 3, 5]:
        n_loops = 10
        start_s = time.time()
        for i in xrange(n_loops):
            _ = median_hsv(im_bgr, blur_size=blur_size)
        elapsed_s = (time.time() - start_s) / n_loops

        print("{b} - Average time: {t} [ms]"
              .format(b=blur_size, t=int(round(elapsed_s * 1000))))
