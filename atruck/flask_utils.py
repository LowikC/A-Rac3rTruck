import logging
import numpy as np
import uwsgi
import json
from PIL import Image
from flask import request, abort, make_response


class USWGIException(Exception):
    pass


def log_and_abort(msg, code):
    """
    Log an error and return an HTTP response with the given code.
    :param msg: Message to log as ERROR.
    :param code: HTTP code to return.
    :return: HTTP response with the status and msg given in parameters.
    """
    logging.error(msg)
    abort(make_response(msg, code))


def initialize_log():
    """
    Initializes the log file.
    The path to the log file must be defined in a uWSGI placeholder log_file.
    :raises: Raises an USWGIException if the uWSGI placeholder log_file doesn't exist.
    """
    log_format = "[%(levelname)s] [%(asctime)s] [%(message)s] [%(funcName)s]"
    if 'log_file' in uwsgi.opt:
        logging.basicConfig(format=log_format, filename=uwsgi.opt['log_file'], level=logging.DEBUG)
    else:
        raise USWGIException("log_file is not defined as uWSGI placeholder.")


def get_image_in_request():
    """
    Return the image sent in the request.
    """
    if 'file' not in request.files:
        log_and_abort(u"Missing field 'file' in request", 400)
    image_file = request.files['file']
    try:
        image = Image.open(image_file)
        return np.array(image)
    except IOError:
        log_and_abort(u"File is not readable", 403)


def get_json_data_in_request():
    """
    Return the TruckStatus sent in the request.
    """
    data = json.loads(request.files['data'].read())
    return data
