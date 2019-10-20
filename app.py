import flask

app = flask.Flask(__name__)

from yelp import yelp_request

@app.route("/")
def hello():
  return "findR home; use /findr to start searching"

@app.route("/findr")
def find():
  return yelp_request.search_raw()

if __name__ == "__main__":
  app.run()