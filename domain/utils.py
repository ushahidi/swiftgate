from mongokit import *
import re

con = Connection()

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

def get_api_wrapper_by_identifier(identifier):
    return con.APIWrapper.find_one({'url_identifier':identifier})

def get_api_method_wrapper_by_url_pattern(path, api_wrapper):
    path = re.sub(api_wrapper.url_identifier, '', path.lstrip('/').rstrip('/'))
    for element in api_wrapper.api_methods:
        if bool(re.match(element.url_pattern, path, re.IGNORECASE)) :
            return element
    return None
