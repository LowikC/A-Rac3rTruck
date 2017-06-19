# -*- coding: utf8 -*-
"""
This script is used to test upload on the sellit server.
"""
import cStringIO
from requests import post
from PIL import Image
import json
import time
from context import atruck
from atruck.Camera import Camera


if __name__ == '__main__' :
    cam = Camera(0)

    url = "http://lowik.sytes.net"
    port = 53117

    url_process = url + ":" + str(port) + "/process"

    im_bgr, ts = cam.next_image()
    im_bgr = Image.fromarray(im_bgr)
    im_buffer = cStringIO.StringIO()
    im_bgr.save(im_buffer, format='JPEG')
    im_buffer.seek(0)
    data = {
        "image_timestamp_ms": int(ts * 1000),
        "status": {
            "over": False,
            "collision": False
        }
    }

    files = {'file': im_buffer, 'data': json.dumps(data)}
    start_s = time.time()
    r = post(url_process, files=files)
    print("Request took {t:.1f} ms".format(t=(time.time() - start_s) * 1000))
    print 'Response from the server: \n{text}'.format(text=r.json())
