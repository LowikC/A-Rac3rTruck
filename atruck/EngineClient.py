import cStringIO
import logging
import json
from requests import post, codes
from PIL import Image
from ProbeDaemon import ProbeDaemon
from CommandFactory import CommandFactory
from NoCommand import NoCommand

class NoServerException(Exception):
    pass


class FailedRequestException(Exception):
    pass


class EngineClient(object):
    def __init__(self, server_url, port, endpoint="/process"):
        self.process_url = "{url}:{port}{endpoint}"\
            .format(url=server_url, port=port, endpoint=endpoint)
        self.probe = ProbeDaemon(server_url, port)
        self.probe.start()
        logging.debug("EngineClient running")

    def get_command(self, im_bgr, timestamp_s, status):
        try:
            if not self.probe.up():
                logging.error("Server seems down")
                raise NoServerException("Server {url} not available".format(url=self.process_url))

            im_buffer = self.get_im_buffer(im_bgr)
            json_data = self.get_data_json(status, timestamp_s)
            files = {'file': im_buffer, 'data': json_data}
            request = post(self.process_url, files=files)
            if request.status_code != codes.ok:
                raise FailedRequestException("Response: {r}".format(r=request.text))

            response = request.json()
            logging.info("Received json: {r}".format(r=response))
            return CommandFactory.from_dict(response["cmd"])
        except Exception as err:
            logging.error("Issue in the request: {err}".format(err=err))
            return NoCommand()

    @staticmethod
    def get_im_buffer(im_bgr):
        pil_image = Image.fromarray(im_bgr)
        im_buffer = cStringIO.StringIO()
        pil_image.save(im_buffer, format='JPEG')
        im_buffer.seek(0)
        return im_buffer

    @staticmethod
    def get_data_json(status, timestamp_s):
        data = dict()
        data["image_timestamp_ms"] = int(timestamp_s * 1000)
        data["status"] = status.to_dict()
        return json.dumps(data)
