from collections import namedtuple


ColorHSV = namedtuple("ColorHSV",
                      ["hue_min", "hue_max",
                       "sat_min", "sat_max",
                       "val_min", "val_max"])


GREEN_HSV = ColorHSV(hue_min=33, hue_max=54,
                     sat_min=45, sat_max=200,
                     val_min=125, val_max=250)