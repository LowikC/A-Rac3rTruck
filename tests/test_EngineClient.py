# -*- coding: utf8 -*-
"""
This script is used to test upload on the sellit server.
"""
import cStringIO
from requests import post
from PIL import Image
import cv2
import json
import time


if __name__ == '__main__' :
    url = "http://lowik.sytes.net"
    port = 53117

    url_process = url + ":" + str(port) + "/process"

    im_bgr = cv2.imread("/home/robot/im_1497641529.jpg")
    im_bgr = Image.fromarray(im_bgr)
    im_buffer = cStringIO.StringIO()
    im_bgr.save(im_buffer, format='JPEG')
    im_buffer.seek(0)
    data = {
        "image_timestamp_ms": 1111111,
        "status": {
            "over": False
        }
    }

    files = {'file': im_buffer, 'data': json.dumps(data)}
    start_s = time.time()
    r = post(url_process, files=files)
    print("Request took {t:.1f} ms".format(t=(time.time() - start_s) * 1000))
    print 'Response from the server: \n{text}'.format(text=r.json())
