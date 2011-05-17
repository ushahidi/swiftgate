__author__ = "Matthew Kidza-Griffiths"
__copyright__ = "Copyright 2007, Swiftly.org"
__credits__ = ["Matthew Kidza-Griffiths", "Jon Gosier"]
__license__ = "LGPL"
__version__ = "0.0.1"
__maintainer__ = "Matthew Kidza-Griffiths"
__email__ = "mg@swiftly.org"
__status__ = "Development"


def validate_search_for_service_form(form):
    search = form.get('search')
    if not search:
        return False, ['You forgot to enter anything in the search box!']
    return True, []

def validate_change_rate_limit(form):
    ratelimit = form.get('ratelimit')
    if not ratelimit.isdigit():
        return False, ['The rate limit must be a positive whole number!']
    return True
