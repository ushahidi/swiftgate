__author__ = "Matthew Kidza-Griffiths"
__copyright__ = "Copyright 2007, Swiftly.org"
__credits__ = ["Matthew Kidza-Griffiths", "Jon Gosier"]
__license__ = "LGPL"
__version__ = "0.0.1"
__maintainer__ = "Matthew Kidza-Griffiths"
__email__ = "mg@swiftly.org"
__status__ = "Development"


from configuration.configuration import config
import logging
import logging.handlers
import oauth2
import time
import urllib2
import urllib
from urllib2 import URLError
from flask import json
import re


#thegateway logging
themanagerlogging_filename = config.get('themanagerlogging', 'filename')
themanagerlogger = logging.getLogger('themanagerlogger')
formatter = logging.Formatter('%(created)f, %(name)s, %(levelname)s, %(module)s, %(funcName)s, %(lineno)s, %(message)s')
logging_handler = logging.handlers.TimedRotatingFileHandler(themanagerlogging_filename, when='d', interval=1, backupCount=30, encoding=None, delay=False, utc=False)
logging_handler.setFormatter(formatter)
themanagerlogger.addHandler(logging_handler)

def validate_signin_form(form):
    riverId = form.get('riverId')
    password = form.get('password')
    if not riverId or not password:
        return False, ['You must enter your RiverID and password']
    authenticationProvider = authentication_factory()
    return authenticationProvider.authenticate(riverId, password)

def validate_edit_service_form(form):
    display_name = form.get('display_name')
    description = form.get('description')
    request_handler = form.get('request_handler')
    url_identifier = form.get('url_identifier')
    errors = []

    if not display_name: errors.append('You must choose a display name')
    if not description: errors.append('You must choose a discription')
    if request_handler == "0": errors.append('You must choose a request handler')
    if not url_identifier: errors.append('You must choose a url indetifier')
    if errors: return False, errors

    if not bool(re.search(r'^[A-Za-z\- ]+$', display_name)): errors.append('Display name must only be letters and hyphens')
    if not bool(re.search(r'^[\w ]+$', description)): errors.append('Description should only be word caracters')
    if not bool(re.search(r'^[a-z0-9\-/]+$', url_identifier)): errors.append('url identifier can only be lower case letters, numbers, hyphens and forward slashes')
    if errors: return False, errors

    return True, []

def validate_edit_method_form(form, method_id=None):
    if method_id:
        method_identifier = form.get('method_identifier_%s' % method_id)
        mapper = form.get('mapper_%s' % method_id)
        accepted_http_methods = form.get('accepted_http_methods_%s' % method_id)
        url_pattern = form.get('url_pattern_%s' % method_id)
        endpoint = form.get('endpoint_%s' % method_id)
        view = form.get('view_%s' % method_id)
        open_access_calls_per_hour = form.get('open_access_calls_per_hour_%s' % method_id)
    else:
        method_identifier = form.get('method_identifier')
        mapper = form.get('mapper')
        accepted_http_methods = form.get('accepted_http_methods')
        url_pattern = form.get('url_pattern')
        endpoint = form.get('endpoint')
        view = form.get('view')
        open_access_calls_per_hour = form.get('open_access_calls_per_hour')

    errors = []

    if not method_identifier: errors.append('You must enter a method id')
    if mapper == "0": errors.append('You must choose a mapper')
    if not accepted_http_methods: errors.append('You must enter HTTP methods to accept')
    if not url_pattern: errors.append('You must enter a url pattern')
    if not endpoint: errors.append('You must enter an endpoint')
    if view == "0": errors.append('You must choose a view')
    if not open_access_calls_per_hour: errors.append('You must enter a free rate limit')
    if errors: return False, errors

    if not bool(re.search(r'^\w+$', method_identifier)) : errors.append('The method identifier should only be letters')
    if not accepted_http_methods == 'GET' and not accepted_http_methods == 'POST' and not accepted_http_methods == 'GET|POST': errors.append('Accepted inputs for the HTTP methods are GET, POST and GET|POST only')
    if not bool(re.search(r'^[a-z0-9\-/]+$', url_pattern)): errors.append('url pattern can only be lower case letters, numbers, hyphens and forward slashes')
    if not bool(re.search(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', endpoint)) : errors.append('The url endpoint you entered doesnt look like a url')
    if not bool(re.search(r'^[0-9]+$', open_access_calls_per_hour)): errors.append('You can only enter number in to the rate limit box')
    if errors: return False, errors

    return True, []


def authentication_factory():
    class_name = config.get('authenticationprovision', 'authentication_provider')
    authentication_provider = getattr(AuthenticationProviders, class_name)
    return authentication_provider()

class AuthenticationProviders:
    class MockAuthenticationProvider(object):
        def authenticate(self, username, password):
            if not username == 'matt':
                return False, ['That RiverID was not found']
            if not password == 'password':
                return False, ['That password was wrong, sorry']
            return True, []

    class RiverIDAuthenticationProvider(object):
        def authenticate(self, username, password):
            key = config.get('oauthcredentials', 'oauth_consumer_key')
            secret = config.get('oauthcredentials', 'oauth_secret')
            url = config.get('services', 'river_id') + 'thegateway/validatecredentials'
            values = {
                'riverid':username,
                'password':password,
            }
            params = {
                'oauth_timestamp': int(time.time()),
                'oauth_nonce': None,
                'oauth_signature_method':'HMAC-SHA1',
            }
            params.update(values)
            consumer = oauth2.Consumer(key=key,secret=secret)
            oauth_request = oauth2.Request(method='POST', url=url, parameters=params)
            signature_method = oauth2.SignatureMethod_HMAC_SHA1()
            oauth_request.sign_request(signature_method, consumer, None)
            data = urllib.urlencode(values)
            try :
                request = urllib2.Request(url, headers=oauth_request.to_header(), data=data)
                u = urllib2.urlopen(request)
                response = json.loads(u.read())
                if response['status'] == 'Failed':
                    if response['errorcomponent'] == 'gateway':
                        for error in response['errors']:
                            themanagerlogger.error("OAUTH CREDENTIAL ERROR, |%s|" % error)
                        return False, ['Were sorry but a technical error provented us from siging you in, please try again a few minutes']
                    return False, response['errors']
                return True, []
            except URLError, e:
                themanagerlogger.error("HTTP ERROR, |%s|" % e)
                return False, ['Were sorry but a technical error provented us from siging you in, please try again a few minutes']