from urllib import parse
import json

data = {
            'location': {
                'name': 'Flagey Building 29, rue du Belvédère 1050 Brussels Belgium',
            },
            'attendees': [
                {'name': 'Gilles', 'preferences': 'afghani,african,bbq'},
                {'name': 'Vincent', 'preferences': 'asianfusion,burgers,brasseries'},
                {'name': 'Edwin', 'preferences': ''}
            ],
            'max_distance': 1000,
            'price_range': "1,2",
            'locale': 'en_BE',
            'open_now': True
}

args = parse.urlencode({'data': json.dumps(data)})

# print("curl -X GET 'http://localhost:5000/findr?'" + args)  # dev
print("curl -X GET 'https://lunchpickr.herokuapp.com/findr?" + args + "'")
