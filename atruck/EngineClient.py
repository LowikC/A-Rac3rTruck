import cStringIO
from requests import post, codes
from PIL import Image
import multiprocessing
import urlparse
from ProbeDaemon import ProbeDaemon
from TruckCommand import TruckCommand


class NoServerException(Exception):
    pass


class FailedRequestException(Exception):
    pass


class EngineClient(object):
    def __init__(self, server_url, endpoint="/process"):
        self.process_url = urlparse.urljoin(server_url, endpoint)

        self.probe = ProbeDaemon(server_url)
        self.probe.start()

    def get_command(self, im_bgr, timestamp_s, status):
        if not self.probe.up():
            raise NoServerException("Server {url} not available".format(url=self.process_url))

        request_files = self.get_request_files(im_bgr)
        request_data = self.get_request_data(status, timestamp_s)
        request = post(self.process_url, data=request_data, files=request_files)
        if request.status_code != codes.ok:
            raise FailedRequestException()

        return TruckCommand(**request.json())

    @staticmethod
    def get_request_files(im_bgr):
        pil_image = Image.fromarray(im_bgr)
        im_buffer = cStringIO.StringIO()
        pil_image.save(im_buffer, format='JPEG')
        im_buffer.seek(0)
        return {'file': im_buffer}

    @staticmethod
    def get_request_data(status, timestamp_s):
        data = dict()
        data["image_timestamp_ms"] = int(timestamp_s * 1000)
        data["motor_speed"] = status.motor_speed
        return data



