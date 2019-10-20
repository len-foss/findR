from validate import validate_input

import unittest
import voluptuous

class TestStringMethods(unittest.TestCase):

    def test_input_minimal_example(self):
        minimal_example = {'location': {'name': 'Hannut'}}
        validate_input(minimal_example)

    def test_input_full_example(self):
        full_example = {
            'location': {
                'name': 'Hannut',
                'coordinates': {
                    'lat': 50.67215,
                    'lon': 5.07776
                }
            },
            'attendees': [
                {'name': 'Gilles', 'preferences': 'afghani,african,bbq'},
                {'name': 'Vincent'},
                {'name': 'Edwin', 'preferences': ''},
            ],
            'max_distance': 500,
            'price_range': "1,2",
            'locale': 'en_BE',
            'open_now': True,
        }
        validate_input(full_example)

    def test_input_missing_location(self):
        missing_location_example = {'price_range': "1,2"}
        with self.assertRaises(voluptuous.error.MultipleInvalid):
            validate_input(missing_location_example)
