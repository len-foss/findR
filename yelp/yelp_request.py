import os
import requests
from urllib.error import HTTPError
from urllib.parse import quote

# imports for main (testing purpose):
import sys, pprint
from argparse import ArgumentParser


API_KEY = os.environ['API_KEY_YELP']
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
TERM_RESTAURANTS = 'restaurants'
# default for example purposes
ADDRESS_LAB_BOX = "Flagey Building 29, rue du Belvédère 1050 Brussels Belgium"


def get_request(host=API_HOST, path=SEARCH_PATH, api_key=API_KEY, url_params=None):
    """Given your API_KEY, send a GET request to the API.
    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        API_KEY (str): Your API Key.
        url_params (dict): An optional set of query parameters in the request.
    Returns:
        dict: The JSON response from the request.
    Raises:
        HTTPError: An error occurs from the HTTP request.
    """
    url_params = url_params or {}
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    # https://www.yelp.com/developers/documentation/v3/authentication
    # To authenticate API calls with the API Key,
    # set the Authorization HTTP header value as Bearer API_KEY.
    headers = {'Authorization': 'Bearer %s' % api_key,}
    response = requests.request('GET', url, headers=headers, params=url_params)

    return response.json()


def search_raw(location=ADDRESS_LAB_BOX, latitude=False, longitude=False, radius=2000,
           price_range='1,2,3,4', categories='',
           locale='en_BE', open_now=False,
           limit=10):
    """Query the restaurants Search API by location
       (given either as an address string or latitude/longitude)
       sort_by defaults to best_match
    Returns:
        dict: The JSON response from the request.
    """
    url_params = {
        'term': TERM_RESTAURANTS,
        'limit': limit,
        'radius': radius,
        'price_range': price_range,
        'open_now': open_now,
        'locale': locale,
    }
    if latitude and longitude:
        url_params['latitude'] = latitude
        url_params['longitude'] = longitude
    else:
        url_params['location'] = location,
    if categories:
        url_params['categories'] = categories

    return get_request(url_params=url_params)


def main():
    """Simple query for a given address with default parameters"""
    parser = ArgumentParser()
    parser.add_argument('-l', '--location', dest='location',
                        default=ADDRESS_LAB_BOX, type=str,
                        help='Search location (default: %(default)s)')
    input_values = parser.parse_args()

    try:
        response = search_raw(input_values.location)
        pprint.pprint(response, indent=2)
    except HTTPError as error:
        sys.exit(
            'Encountered HTTP error {0} on {1}:\n {2}\nAbort program.'.format(
                error.code,
                error.url,
                error.read(),
            )
        )


if __name__ == '__main__':
    main()
