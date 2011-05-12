from thegateway.authentication import authentication_factory
from configuration.configuration import config
from domain.utils import get_api_usage_statistics_for_app_id as domain_get_api_usage_statistics_for_app_id
from datetime import datetime
import logging
import logging.handlers
import re


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

def build_app_stats_for_app_id(app_id):
    stats = {}
    raw_stats = get_service_usage_statistics_for_app_id(app_id)

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
    except Error, e:
        results = []
        thegatewaylogger.error("GET API USAGE ERROR, \"%s\"" % e)
    return results