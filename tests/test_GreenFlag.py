import unittest
import os
import numpy as np
import cv2
import time
from context import atruck
from atruck.GreenFlag import GreenFlag, GREEN_HSV
from atruck.cvision_utils import median_hsv


class TestGreenFlag(unittest.TestCase):
    @staticmethod
    def get_image(with_flag):
        im = np.zeros((480, 640, 3), dtype=np.uint8)
        if with_flag:
            valid_hue = (GREEN_HSV.hue_min + GREEN_HSV.hue_max)/2
            valid_sat = (GREEN_HSV.sat_min + GREEN_HSV.sat_max) / 2
            valid_val = (GREEN_HSV.val_min + GREEN_HSV.val_max) / 2

            im[100:180, 200:300, 0] = valid_hue
            im[100:180, 200:300, 1] = valid_sat
            im[100:180, 200:300, 2] = valid_val
        return im

    def check_sequence(self, gf, with_flag, expect_ready, expect_go):
        for frame in xrange(len(with_flag)):
            ready, go = gf.update(self.get_image(with_flag[frame]))
            self.assertEquals(ready, expect_ready[frame])
            self.assertEquals(go, expect_go[frame])

    def test_ready_go(self):
        green_flag = GreenFlag()
        self.check_sequence(green_flag,
                            with_flag=[True, False, True, True, True],
                            expect_ready=[False, False, False, False, True],
                            expect_go=[False, False, False, False, False])

        self.check_sequence(green_flag,
                            with_flag=[False, True, False, False, False],
                            expect_ready=[False, False, False, False, False],
                            expect_go=[False, False, False, False, True])

        self.check_sequence(green_flag,
                            with_flag=[True, True, True, False, False, False],
                            expect_ready=[False for _ in range(6)],
                            expect_go=[False for _ in range(6)])

    def test_detect_with_flag(self):
        current_dir = os.path.dirname(os.path.realpath(__file__))
        im_bgr = cv2.imread(os.path.join(current_dir,
                                         "data/GreenFlag_with_flag.jpg"))
        im_hsv = median_hsv(im_bgr)
        green_flag = GreenFlag()
        self.assertTrue(green_flag._contains_green_flag(im_hsv))

    def test_detect_no_flag(self):
        current_dir = os.path.dirname(os.path.realpath(__file__))
        im_bgr = cv2.imread(os.path.join(current_dir,
                                         "data/GreenFlag_no_flag.jpg"))
        im_hsv = median_hsv(im_bgr)
        green_flag = GreenFlag()
        self.assertFalse(green_flag._contains_green_flag(im_hsv))

    def test_detect_with_flag_160x120(self):
        current_dir = os.path.dirname(os.path.realpath(__file__))
        im_bgr = cv2.imread(os.path.join(current_dir,
                                         "data/GreenFlag_with_flag.jpg"))
        im_bgr = cv2.resize(im_bgr, (160, 120), interpolation=cv2.INTER_LINEAR)
        im_hsv = median_hsv(im_bgr, blur_size=5)
        green_flag = GreenFlag()
        self.assertTrue(green_flag._contains_green_flag(im_hsv))

    def test_detect_no_flag_160x120(self):
        current_dir = os.path.dirname(os.path.realpath(__file__))
        im_bgr = cv2.imread(os.path.join(current_dir,
                                         "data/GreenFlag_no_flag.jpg"))
        im_bgr = cv2.resize(im_bgr, (160, 120), interpolation=cv2.INTER_LINEAR)
        im_hsv = median_hsv(im_bgr, blur_size=5)
        green_flag = GreenFlag()
        self.assertFalse(green_flag._contains_green_flag(im_hsv))

    def test_detect_with_flag_80x60(self):
        current_dir = os.path.dirname(os.path.realpath(__file__))
        im_bgr = cv2.imread(os.path.join(current_dir,
                                         "data/GreenFlag_with_flag.jpg"))
        im_bgr = cv2.resize(im_bgr, (80, 60), interpolation=cv2.INTER_LINEAR)
        im_hsv = median_hsv(im_bgr, blur_size=0)
        green_flag = GreenFlag()
        self.assertTrue(green_flag._contains_green_flag(im_hsv))

    def test_detect_no_flag_80x60(self):
        current_dir = os.path.dirname(os.path.realpath(__file__))
        im_bgr = cv2.imread(os.path.join(current_dir,
                                         "data/GreenFlag_no_flag.jpg"))
        im_bgr = cv2.resize(im_bgr, (80, 60), interpolation=cv2.INTER_LINEAR)
        im_hsv = median_hsv(im_bgr, blur_size=0)
        green_flag = GreenFlag()
        self.assertFalse(green_flag._contains_green_flag(im_hsv))


if __name__ == '__main__':
    unittest.main()
