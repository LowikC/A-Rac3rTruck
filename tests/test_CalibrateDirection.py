import unittest
import time
from context import atruck
from atruck.CalibrateDirection import CalibrateDirection


class TestCalibrateDirection(unittest.TestCase):
    def test_calibrate(self):
        # Run two calibrations,
        # the second one should find the same zero position
        cd = CalibrateDirection()
        cd.run(None)
        cd.run(None)
        tolerance = 5
        self.assertLess(abs(cd.zero_position), tolerance)

if __name__ == '__main__':
    unittest.main()


