import numpy as np
import cv2
from skimage import measure
from ColorHSV import GREEN_HSV
from cvision_utils import threshold_hsv


class GreenFlag(object):
    def __init__(self):
        self._default_im_size = 640 * 480
        self._area_min = 6000
        self._area_max = 64000
        self._area_filled_ratio_min = 0.85
        self._min_frames_ready = 2
        self._min_frames_go = 2

        self._im_labels = None
        self._labels_sizes = None
        self._ready = False
        self._go = False
        self._n_frames_flag = 0
        self._n_frames_no_flag = 0

    def update(self, im_hsv):
        """
        Returns updated ready and go flags if there value changed.
        :param im_hsv: HSV image, with median filter applied. 
        """
        if self._go:
            return False, False

        has_flag = self._contains_green_flag(im_hsv)

        if has_flag:
            self._n_frames_flag += 1
            self._n_frames_no_flag = 0
        else:
            self._n_frames_no_flag += 1
            self._n_frames_flag = 0

        if not self._ready and self._n_frames_flag > self._min_frames_ready:
            self._ready = True
            return self._ready, False

        if self._ready and self._n_frames_no_flag > self._min_frames_go:
            self._go = True
            return False, self._go
        return False, False

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

