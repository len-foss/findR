# findR
findRestaurants REST API

Return a list of 10 nearby restaurants for a given location.
Optional arguments include list of preferred categories for attendees, the maximal distance, etc.
The full input request schema (as well as the output) is defined in validate.
The list of categories can be found in data/categories.

The requestr should handle the app logic, and manage the different restaurant providers;
there is only Yelp for now, so the API closely mirrors it.

To generate example curl commands, head to generate_curl_command (pretty explicit right?).

# TODO:
 - authentication
 - ranking
 - localize error messages
 - frontend
 - define with statements to clean up the code
 - put validation in wrappers
 - facades would require to extract the parsing of values in validate
