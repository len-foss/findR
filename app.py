import os

import flask
from flask_caching import Cache

app = flask.Flask(__name__)
redis_url = os.environ.get("REDIS_URL", 'redis://127.0.0.1:6379')
cache = Cache(app, config={'CACHE_TYPE': 'redis', 'CACHE_REDIS_URL': redis_url})

from yelp import yelp_request

@app.route("/")
@cache.cached(timeout=900)
def hello():
    return "findR home; use /findr to start searching"


@app.route("/findr")
def find():
    return yelp_request.search_raw()


if __name__ == "__main__":
    app.run()
