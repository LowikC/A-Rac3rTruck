# -*- coding: utf8 -*-
"""
This script is used to test upload on the sellit server.
"""
import cStringIO
from requests import post, get, codes
import sys
from PIL import Image
import cv2
import json
import time


if __name__ == '__main__' :
    import argparse
    # Define command line arguments
    parser = argparse.ArgumentParser(description='Send a POST request for image classification.')
    parser.add_argument('--image', '-i', type=str,
                        help='path to the image')
    parser.add_argument('--url', type=str, default="http://localhost",
                        help='Url of the server')
    parser.add_argument('--port', type=str, default="53117",
                        help='Port on the server')

    args = parser.parse_args()

    url_availability = args.url + ":" + args.port + "/probe"
    url_process = args.url + ":" + args.port + "/process"

    r = get(url_availability)
    if r.status_code != codes.ok:
        print "Service is not available on this url"
        sys.exit()

    im_bgr = cv2.imread(args.image)
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
