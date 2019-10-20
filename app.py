import os
import requestr
import validate
import json, requests
from urllib import parse

import logging, traceback
_logger = logging.getLogger(__name__)

from flask import Flask, request, redirect, url_for
from flask_dance.contrib.github import make_github_blueprint, github
from flask_caching import Cache

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY")
app.config["GITHUB_OAUTH_CLIENT_ID"] = os.environ.get("GITHUB_OAUTH_CLIENT_ID")
app.config["GITHUB_OAUTH_CLIENT_SECRET"] = os.environ.get("GITHUB_OAUTH_CLIENT_SECRET")
github_bp = make_github_blueprint()
app.register_blueprint(github_bp, url_prefix="/login")
redis_url = os.environ.get("REDIS_URL", 'redis://127.0.0.1:6379')
cache = Cache(app, config={'CACHE_TYPE': 'redis', 'CACHE_REDIS_URL': redis_url})


@app.route("/")
@cache.cached(timeout=900)
def hello():
    return ("findR home;\n"
            "login with Github then visit /example to get an example of results\n"
            "or use /findr to start searching")


@app.route("/example")
@cache.cached(timeout=900)  # restaurants don't change that quickly
def example():
    address = 'Flagey Building 29, rue du Belvédère 1050 Brussels Belgium'
    return requestr.find({'location': {'name': address}})


@app.route("/findr")
def find():
    if not github.authorized:
        return redirect(url_for("github.login"))
    try:
        args = dict(parse.parse_qsl(parse.urlsplit(request.url).query))
        data = json.loads(args.get('data'))
        validate.validate_input(data)
    except Exception as e:
        return {'code': 2, 'messages': [e.args[0]], 'number_of_results': 0,}

    try:
        response = requestr.find(data)
    except requests.exceptions.HTTPError as e:
        return {'code': 1, 'messages': [e.args[0]], 'number_of_results': 0,}
    except Exception as e:
        traceback.print_stack()  # failure that should not happen, or exception to refine on
        return {'code': 4, 'messages': ['We messed up.', e.args[0]], 'number_of_results': 0,}

    try:
        validate.validate_output(response)
    except Exception as e:
        _logger.error(e.args[0])

    return response


if __name__ == "__main__":
    app.run()
