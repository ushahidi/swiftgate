from mongokit import *
from configuration.configuration import config
import re


con = Connection(config.get('mongodb', 'host'), config.getint('mongodb', 'port'))

################################################################################
# Utility functions to acees APIWrapper objects and properties                 #
################################################################################
def get_api_wrapper_by_identifier(identifier):
    return con.APIWrapper.find_one({'url_identifier':identifier})

def get_api_wrapper_by_id(id):
    return con.APIWrapper.find_one({'_id':ObjectId(id)})

def get_api_wrapper_by_free_text_search(search):
    rule = re.compile(search, re.IGNORECASE)
    api_wrappers = {}
    for wrapper in con.APIWrapper.fetch({"display_name": rule}):
        api_wrappers[wrapper.url_identifier] = wrapper
    for wrapper in con.APIWrapper.fetch({"description": rule}):
        if not wrapper.url_identifier in api_wrappers.keys():
            api_wrappers[wrapper.url_identifier] = wrapper
    return api_wrappers.values()

def get_api_method_wrapper_by_url_pattern(path, api_wrapper):
    path = re.sub(api_wrapper.url_identifier, '', path.lstrip('/').rstrip('/'))
    for element in api_wrapper.api_methods:
        if bool(re.match(element.url_pattern, path, re.IGNORECASE)) :
            return element
    return None

################################################################################
# Utility functions to acees user objects and properties                       #
################################################################################
def get_un_authenticated_user_by_host(host):
    existing_user = con.UnAuthenticatedUser.find_one({'host':host})
    if not existing_user is None :
        return existing_user
    new_user = con.UnAuthenticatedUser()
    new_user.host = unicode(host)
    new_user.save()
    return new_user

def get_un_authenticated_rate_abuser_by_host(host):
    existing_rate_abuser = con.UnAuthenticatedRateAbuser.find_one({'host':host})
    if not existing_rate_abuser is None:
        return existing_rate_abuser
    new_rate_abuser = con.UnAuthenticatedRateAbuser()
    new_rate_abuser.host = unicode(host)
    new_rate_abuser.save()
    return new_rate_abuser

def get_authenticated_user_app_by_key(key):
    return con.AuthenticatedUser.find_one({"apps.key":key})

################################################################################
# Utility functions to acees APIUsageStatisticsobjects and properties          #
################################################################################
def get_api_usage_statistics_by_api_wrapper_id(id):
    statistics = con.APIUsageStatistics.find_one({"api_wrapper_id":id})
    if not statistics is None:
        return statistics
    statistics = con.APIUsageStatistics()
    statistics.api_wrapper_id = id
    statistics.save()
    return statistics


################################################################################
# Validation functions for APIWrapper objects and properties                   #
################################################################################
def validate_apiwrapper_urlidentifier(value):
    if value.islower():
        rule = re.compile(r'^\w{4,10}/V\d\.\d$', re.IGNORECASE)
        if bool(rule.match(value)):
            return True
    raise ValidationError('%s must contain only lowercase letters and between 4 and 10 characters and cotain a version switch (eg: /V1.0')

def validate_api_wrapper_requesthandler(value):
    rule = re.compile(r'^\w{4,50}$', re.IGNORECASE)
    if bool(rule.match(value)):
        return True
    else:
        raise ValidationError('%s must contain only letters and between 4 and 50 characters')

def validate_generic_dispalyname(value):
    rule = re.compile(r'^[\w\d ]{4,50}$', re.IGNORECASE)
    if bool(rule.match(value)):
        return True
    else:
        raise ValidationError('%s must contain only letters, numbers and spaces and between 4 and 50 characters')

def validate_generic_description(value):
    rule = re.compile(r'^[\w\d ]{4,256}$', re.IGNORECASE)
    if bool(rule.match(value)):
        return True
    else:
        raise ValidationError('%s must contain only letters, numbers and spaces and between 4 and 256 characters')

