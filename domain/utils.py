from mongokit import *
import re

con = Connection()

################################################################################
# Utility functions to acees APIWrapper objects and properties                 #
################################################################################
def get_api_wrapper_by_identifier(identifier):
    return con.APIWrapper.find_one({'url_identifier':identifier})

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



################################################################################
# Validation functions for APIWrapper objects and properties                   #
################################################################################
def validate_apiwrapper_urlidentifier(value):
    rule = re.compile(r'^\w{4,10}$', re.IGNORECASE)
    if bool(rule.match(value)):
        return True
    else:
        raise ValidationError('%s must contain only letters and between 4 and 10 characters')

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

