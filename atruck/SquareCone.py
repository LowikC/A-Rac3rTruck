import numpy as np
import cv2
from skimage import measure
from ColorHSV import PINK_HSV
from cvision_utils import threshold_hsv


class SquareConeDetector(object):
    def __init__(self):
        self._default_im_size = 160 * 120
        self._area_min = 180
        self._area_max = 1200
        self._area_filled_ratio_min = 0.9

        self._im_labels = None
        self._labels_sizes = None

    def detect(self, im_hsv):
        """
        Returns SquareCones detected in the image, by pairs.
        
        :param im_hsv: HSV image, with median filter applied. 
        :return Detected pairs of cones, sorted by increasing distance
        [[sc0_left, sc0_right], [sc1_left, sc1_right], ...]
        """
        mask = threshold_hsv(im_hsv, PINK_HSV)

        self._im_labels, n_labels = \
            measure.label(mask, background=0, return_num=True)
        # background is labelled with -1, and other label starts at 0
        # for np.bincount, we want values >= 0
        self._im_labels += 1
        self._labels_sizes = np.bincount(self._im_labels.ravel())
        im_size = mask.shape[0] * mask.shape[1]
        candidates = []
        for label in xrange(1, n_labels + 1):
            if not self._valid_size(label, im_size):
                continue
            if not self._valid_horizon(label, im_size):
                continue
            if not self._valid_filled(label):
                continue
            candidates.append(label)

        return self.match_by_pair(candidates)

    def _valid_size(self, label, im_size):
        ratio_size = float(im_size) / self._default_im_size
        area_min = self._area_min * ratio_size
        area_max = self._area_max * ratio_size
        return area_min < self._labels_sizes[label] < area_max

    def _get_rotated_rect(self, label):
        y, x = np.nonzero(self._im_labels == label)
        labeled_points = np.zeros((x.shape[0], 2), dtype=np.int32)
        labeled_points[:, 0] = x
        labeled_points[:, 1] = y
        return cv2.minAreaRect(labeled_points)

    def _valid_filled(self, label):
        area_filled_ratio_min = 0.85
        rbox = self._get_rotated_rect(label)
        area_box = float(rbox[0][0] * rbox[0][1])
        return area_box / self._labels_sizes[label] > area_filled_ratio_min

    def _contains_green_flag(self, im_hsv):
        mask = threshold_hsv(im_hsv, GREEN_HSV)
        cross = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, cross)

        self._im_labels, n_labels = measure.label(mask, background=0,
                                                  return_num=True)
        # background is labelled with -1, and other label starts at 0
        # for np.bincount, we want values >= 0
        self._im_labels += 1
        self._labels_sizes = np.bincount(
            self._im_labels.ravel())
        im_size = mask.shape[0] * mask.shape[1]
        for label in xrange(1, n_labels + 1):
            if not self._valid_size(label, im_size):
                continue

            if self._valid_filled(label):
                return True

        return False

