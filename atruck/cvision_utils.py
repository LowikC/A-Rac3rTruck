import cv2
import numpy as np


def median_hsv(im_bgr, blur_size=9):
    im_med = im_bgr
    if blur_size > 0:
        im_med = cv2.medianBlur(im_bgr, blur_size)
    im_hsv = cv2.cvtColor(im_med, code=cv2.COLOR_BGR2HSV)
    return im_hsv


def threshold_hsv(im_hsv, color):
    h = np.logical_and(im_hsv[..., 0] > color.hue_min,
                       im_hsv[..., 0] < color.hue_max)
    s = np.logical_and(im_hsv[..., 1] > color.sat_min,
                       im_hsv[..., 1] < color.sat_max)
    v = np.logical_and(im_hsv[..., 2] > color.val_min,
                       im_hsv[..., 2] < color.val_max)
    mask = np.logical_and(np.logical_and(h, s), v)
    return mask.astype(np.uint8)