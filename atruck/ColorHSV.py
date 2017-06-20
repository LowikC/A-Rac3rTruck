from collections import namedtuple


ColorHSV = namedtuple("ColorHSV",
                      ["hue_min", "hue_max",
                       "sat_min", "sat_max",
                       "val_min", "val_max"])


GREEN_HSV = ColorHSV(hue_min=30, hue_max=54,
                     sat_min=45, sat_max=200,
                     val_min=125, val_max=250)

PINK_HSV = ColorHSV(hue_min=148, hue_max=175,
                    sat_min=40, sat_max=170,
                    val_min=200, val_max=255)
