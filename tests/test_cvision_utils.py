import unittest
import numpy as np
import time
from context import atruck
from atruck.cvision_utils import threshold_hsv
from atruck.ColorHSV import GREEN_HSV


class TestCVisionUtils(unittest.TestCase):
    def test_threshold_hsv(self):
        im_hsv = np.zeros((480, 640, 3), dtype=np.uint8)
        m_h, m_w = 100, 150
        im_hsv[100:100+m_h, 150:150+m_w, 0] = np.random.randint(
            low=GREEN_HSV.hue_min + 1,
            high=GREEN_HSV.hue_max,
            size=(m_h, m_w),
            dtype=np.uint8)
        im_hsv[100:100 + m_h, 150:150 + m_w, 1] = np.random.randint(
            low=GREEN_HSV.sat_min + 1,
            high=GREEN_HSV.sat_max,
            size=(m_h, m_w),
            dtype=np.uint8)
        im_hsv[100:100 + m_h, 150:150 + m_w, 2] = np.random.randint(
            low=GREEN_HSV.val_min + 1,
            high=GREEN_HSV.val_max,
            size=(m_h, m_w),
            dtype=np.uint8)

        start_s = time.time()
        for _ in xrange(10):
            mask = threshold_hsv(im_hsv, GREEN_HSV)
        end_s = time.time()
        print("Time [ms]: ", round((end_s - start_s) * 1000))

        nz_area = np.count_nonzero(mask[100:100+m_h, 150:150+m_w])
        nz_total = np.count_nonzero(mask)

        self.assertEquals(nz_area, nz_total)
        self.assertEquals(nz_area, m_w * m_h)


if __name__ == '__main__':
    unittest.main()
