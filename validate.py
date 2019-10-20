from data import categories
from data import codes
from voluptuous import Schema, Required, All, Optional, ALLOW_EXTRA


LOCALES = ['en_BE', 'fr_BE', 'nl_BE']


def validate_location(d):
    if not d.get('name') and not d.get('coordinates'):
        raise ValueError("Must specify at least one of ['name', 'coordinates'].")
    return d.get('coordinates') or d['name']


def validate_price_range(s):
    try:
        all(c.strip() in ['1', '2', '3', '4'] for c in s.split(','))
    except Exception:
        raise ValueError("Price range should be of the form 'S(,S)*' with S being in (1, 2, 3, 4).")
    return s


def validate_locale(s):
    if s not in LOCALES:
        raise ValueError("The supported locales are %s".format(LOCALES))
    else:
        return s


def validate_preferences(s):
    try:
        all(c.strip() in categories.ALL for c in s.split(','))
    except Exception:
        raise ValueError("The preference should be of the form 'S(,S)*' "
                         "with S being a yelp restaurant category.")
    return s


def validate_input(data_dict):
    coordinates_schema = Schema({Required('lat'): float,
                                 Required('lon'): float})
    location_schema = Schema(All({Optional('name'): str,
                                  Optional('coordinates'): coordinates_schema},
                                  validate_location
                             ))
    attendees_schema = Schema([{Required('name'): str,
                               Optional('preferences'): validate_preferences,
                             }])
    input_schema = Schema({
        Required('location'): location_schema,
        Optional('attendees'): attendees_schema,
        Optional('max_distance'): int,
        Optional('price_range'): validate_price_range,
        Optional('locale'): validate_locale,
        Optional('open_now'): bool,
    })
    return input_schema(data_dict)


def validate_code(i):
    if i not in codes.ALL:
        raise ValueError("The returned code should be defined first.")
    return i


def validate_output(data_dict):
    restaurant_schema = Schema({Required('name'): str}, extra=ALLOW_EXTRA)
    input_schema = Schema({
        Required('code'): validate_code,
        Required('messages'): [str],
        Optional('restaurants'): [restaurant_schema],
        Required('number_of_results'): int,
        Optional('locale'): validate_locale,
    })
    return input_schema(data_dict)