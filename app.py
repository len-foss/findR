import os
import requestr
import validate
import json, requests
from urllib import parse

import logging, traceback
_logger = logging.getLogger(__name__)

import flask
from flask_caching import Cache

app = flask.Flask(__name__)
redis_url = os.environ.get("REDIS_URL", 'redis://127.0.0.1:6379')
cache = Cache(app, config={'CACHE_TYPE': 'redis', 'CACHE_REDIS_URL': redis_url})


@app.route("/")
@cache.cached(timeout=900)
def hello():
    return "findR home; use /findr to start searching, /example to get an example of results"


@app.route("/example")
@cache.cached(timeout=900)  # restaurants don't change that quickly
def example():
    address = 'Flagey Building 29, rue du Belvédère 1050 Brussels Belgium'
    return requestr.find({'location': {'name': address}})


@app.route("/findr")
def find():
    try:
        args = dict(parse.parse_qsl(parse.urlsplit(flask.request.url).query))
        data = json.loads(args.get('data'))
        validate.validate_input(data)
    except Exception as e:
        return {'code': 2, 'messages': [e.args[0]], 'number_of_results': 0,}

    try:
        response = requestr.find(data)
    except requests.exceptions.HTTPError as e:
        return {'code': 1, 'messages': [e.args[0]], 'number_of_results': 0,}
    except Exception:
        traceback.print_stack()  # failure that should not happen, or exception to refine on
        return {'code': 4, 'messages': ['We messed up.'], 'number_of_results': 0,}

    try:
        validate.validate_output(response)
    except Exception as e:
        _logger.error(e.args[0])

    return response


if __name__ == "__main__":
    app.run()
