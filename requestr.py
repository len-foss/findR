from yelp import yelp_request
import itertools


def find(data_dict):
    """Generic interface;
       for now we have only Yelp so we won't really split the logic.
    """
    return find_from_yelp(data_dict)


def find_from_yelp(data_dict):
    """At this point data should have been validated.
       There are two main cases: less than two attendees have preferences,
       in which case on request is sufficient for all;
       or attendees have different preferences, so we should make as many
       queries and aggregate them.
       We need to clean up the dict so that the arguments match for calling Yelp.
    """
    args = {}
    loc = data_dict.pop('location')
    if loc.get('coordinates'):
        args.update({'latitude': loc['coordinates']['lat'],
                         'longitude': loc['coordinates']['lon']})
    else:
        args.update({'location': loc['name']})

    if data_dict.get('max_distance'):
        args.update(radius=data_dict.pop('max_distance'))

    attendees = data_dict.pop('attendees', [])
    args.update(data_dict)

    preferences = set(attendee.get('preferences', '') for attendee in attendees)
    if len(preferences) > 1:
        all_results = []
        for preference in preferences:
            response = yelp_request.search_raw(**args, categories=preference)
            all_results.append(response)
        results = aggregate_responses(all_results)
    else:
        categories = len(preferences) and list(preferences)[0] or ''
        results = yelp_request.search_raw(**args, categories=categories)['businesses']

    return format_from_yelp(results)


def aggregate_responses(response_list):
    """Here should be the secret sauce; how we determine how we rank the restaurants.
       We should be non-linear depending on the scoring system
       (bad results should be heavily penalised, so if we have restaurants
       that only one attendee like in each case, we should prioritise middlegrounds.)
       Anyway that's all hypothetical, for now it's basic.
    """
    all_b_dup = list(itertools.chain.from_iterable(r['businesses'] for r in response_list))
    all_businesses = [b for n, b in enumerate(all_b_dup) if b not in all_b_dup[:n]]
    all_businesses.sort(key=lambda b: sum(int(b in r['businesses']) for r in response_list), reverse=True)
    return all_businesses[:10]


def format_from_yelp(businesses):
    return {
        'code': 0,
        'restaurants': businesses,
        'number_of_results': len(businesses),
        'messages': [],
    }
