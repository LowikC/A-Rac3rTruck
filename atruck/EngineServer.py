import sys
import time
from werkzeug.exceptions import HTTPException
from flask import Flask, Response
from flask_utils import *
from Engine import Engine
from TruckStatus import TruckStatus

# Create the Flask app.
# We need to create it here, because we need the decorator app.route below.
try:
    initialize_log()
    logging.debug(u'Initializing Flask app ...')
    app = Flask(__name__)
    logging.debug(u'Flask app initialized!')
    app.engine = Engine()
except Exception as err:
    error = u"Can't initialize Flask app : %s" % err
    logging.error(error)
    sys.exit(error)


@app.route("/process", methods=['POST'])
def process():
    """Predict the object in an image.
    """
    try:
        image = get_image_in_request()
        data = get_json_data_in_request()
        command_desc = app.engine.process(
            image,
            data["image_timestamp_ms"],
            TruckStatus(**data["status"])
        )
    except HTTPException:
        raise
    except Exception as uncaught_err:
        error_desc = u"Uncaught error in process: {e}".format(e=uncaught_err)
        logging.error(error_desc)
        return Response(response=error_desc, status=500, mimetype="text/plain")

    return Response(response=json.dumps(command_desc), status=200, mimetype="application/json")


@app.route("/probe", methods=['GET'])
def probe():
    """ Check if the service is available.
    Returns:
        A response with a json {"time_us": <time on the server>} and status code 200 if the service is available.
    """
    server_time_us = int(round(time.time() * 1000000))
    return Response(response=json.dumps({"time_us": server_time_us}), status=200, mimetype="application/json")


# Only for test.
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=False)
