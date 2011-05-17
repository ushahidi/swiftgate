__author__ = "Matthew Kidza-Griffiths"
__copyright__ = "Copyright 2007, Swiftly.org"
__credits__ = ["Matthew Kidza-Griffiths", "Jon Gosier"]
__license__ = "LGPL"
__version__ = "0.0.1"
__maintainer__ = "Matthew Kidza-Griffiths"
__email__ = "mg@swiftly.org"
__status__ = "Development"


from configuration.configuration import config
from domain.utils import get_api_usage_statistics_for_app_id as domain_get_api_usage_statistics_for_app_id
from datetime import datetime
import logging
import logging.handlers
import re
import oauth2
import time
import urllib2
import urllib
from urllib2 import URLError
from flask import json


#thegateway logging
thegatewaylogging_filename = config.get('thegatewaylogging', 'filename')
thegatewaylogger = logging.getLogger('thegatewaylogger')
formatter = logging.Formatter('%(created)f, %(name)s, %(levelname)s, %(module)s, %(funcName)s, %(lineno)s, %(message)s')
logging_handler = logging.handlers.TimedRotatingFileHandler(thegatewaylogging_filename, when='d', interval=1, backupCount=30, encoding=None, delay=False, utc=False)
logging_handler.setFormatter(formatter)
thegatewaylogger.addHandler(logging_handler)

def validate_signin_form(form):
    riverId = form.get('riverId')
    password = form.get('password')
    if not riverId or not password:
        return False, ['You must enter your RiverID and password']
    authenticationProvider = authentication_factory()
    return authenticationProvider.authenticate(riverId, password)

def validate_add_app_form(form, user):
    app_name = form.get('appName')
    if not app_name:
        return False, ['You need to choose a name for this app']
    app_template = form.get('appTemplate')
    if app_template == '0':
        return False, ['You need to select a template for this app']
    rule = re.compile(app_name, re.IGNORECASE)
    for app in user.apps:
        if bool(rule.match(app.name)):
            return False, ['You already have an app with that name, please choose another one']
    return True, []

def validate_signup_form(form, captchas):
    riverId = form.get('riverId')
    password = form.get('password')
    password2 = form.get('password2')
    emailaddress = form.get('emailaddress')
    captchas_password = form.get('captchas_password')
    errors = []
    if not riverId:
        errors.append('You need to choose a RIverID')
    if not password or not password2:
        errors.append('You need to enter your password twice')
    elif not password == password2:
        errors.append('The passwords you entered did not match')
    if not emailaddress:
        errors.append('You have to enter a valid email address')
    if not captchas_password:
        errors.append('You have to enter the letters you see in the picture below')
    if errors:
        return False, errors
    random_string = form.get('random')
    if not captchas.validate(random_string) or not captchas.verify(captchas_password):
        return False, ['The letter you typed did not match the picture shown, please try again']
    registration_provider = registration_factory()
    return registration_provider.register(riverId, password, emailaddress)

def build_app_stats_for_app_id(app_id):
    stats = {}
    raw_stats = get_service_usage_statistics_for_app_id(app_id)

    if len(raw_stats) == 0:
        return {'no_stats_found':True}

    #total count
    stats['total_count'] = len(raw_stats)

    #First Use
    first_use = 100000000000000000
    for s in raw_stats:
        if s['start_time'] < first_use:
            first_use = s['start_time']
    if first_use == 100000000000000000:
        stats['first_use'] = 'Not yet used'
    else:
        d = datetime.fromtimestamp(first_use)
        stats['first_use'] = d

    return stats

def get_service_usage_statistics_for_app_id(app_id):
    try:
        results = domain_get_api_usage_statistics_for_app_id(app_id)
    except Exception, e:
        results = []
        thegatewaylogger.error("GET API USAGE ERROR, |%s|" % e)
    return results

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
            key = config.get('riveridcredentials', 'oauth_consumer_key')
            secret = config.get('riveridcredentials', 'oauth_secret')
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
                            thegatewaylogger.error("OAUTH CREDENTIAL ERROR, |%s|" % error)
                        return False, ['Were sorry but a technical error provented us from siging you in, please try again a few minutes']
                    return False, response['errors']
                return True, []
            except URLError, e:
                thegatewaylogger.error("HTTP ERROR, |%s|" % e)
                return False, ['Were sorry but a technical error provented us from siging you in, please try again a few minutes']


def registration_factory():
    class_name = config.get('registrationprovision', 'registration_provider')
    registration_provider = getattr(RegistrationProviders, class_name)
    return registration_provider()

class RegistrationProviders:
    class MockRegistrationProvider(object):
        def register(self, username, password, emailaddress):
            if not username == 'matt':
                return False, ['That RiverID was not found']
            if not password == 'password':
                return False, ['That password was wrong, sorry']
            return True, []

    class RiverIDRegistrationProvider(object):
        def register(self, username, password, emailaddress):
            key = config.get('riveridcredentials', 'oauth_consumer_key')
            secret = config.get('riveridcredentials', 'oauth_secret')
            url = config.get('services', 'river_id') + 'thegateway/register'
            values = {
                'riverid':username,
                'password':password,
                'emailaddress':emailaddress
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
                            thegatewaylogger.error("OAUTH CREDENTIAL ERROR, |%s|" % error)
                        return False, ['Were sorry but a technical error provented us from siging you in, please try again a few minutes']
                    return False, response['errors']
                return True, []
            except URLError, e:
                thegatewaylogger.error("HTTP ERROR, |%s|" % e)
                return False, ['Were sorry but a technical error provented us from siging you in, please try again a few minutes']
