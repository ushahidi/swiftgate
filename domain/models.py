from mongokit import *
from domain.utils import con
from domain.utils import validate_apiwrapper_urlidentifier
from domain.utils import validate_generic_dispalyname
from domain.utils import validate_generic_description
from domain.utils import validate_api_wrapper_requesthandler

################################################################################
# API SERVICE OBJECTS                                                          #
################################################################################
@con.register
class APIMethodWrapper():
    """ Code facing object designed to offer dot access to dict properties """
    def __init__(self, values):
        self.method_identifier = values['method_identifier'] if 'method_identifier' in values else None
        self.accepted_http_methods = values['accepted_http_methods'] if 'accepted_http_methods' in values else 'GET|POST'
        self.mapper = values['mapper'] if 'mapper' in values else None
        self.url_pattern = values['url_pattern'] if 'url_pattern' in values else None
        self.endpoint = values['endpoint'] if 'endpoint' in values else None
        self.view = values['view'] if 'view' in values else None
        self.open_access_calls_per_hour = values['open_access_calls_per_hour'] if 'open_access_calls_per_hour' in values else None

@con.register
class APIMethodWrapper_CustomType(CustomType):
    """ MongoDB facing object used to offer dot access to dict properties """
    mongo_type = dict
    python_type = APIMethodWrapper

    def to_bson(self, value):
        return value.__dict__

    def to_python(self, value):
        return APIMethodWrapper(value)

@con.register
class APIWrapper(Document):

    #The MongoDB collection to store these object in
    __collection__ = 'api_wrappers'
    
    #The database used for all objects in this project
    __database__ = 'swift_gateway'

    #Allow access to properties via dot notation
    use_dot_notation = True
    
    #The JSON structure of this object
    structure = {
        'url_identifier': unicode,
        'request_handler': unicode,
        'display_name': unicode,
        'description': unicode,
        'api_methods' : [APIMethodWrapper_CustomType()]
    }

    #The required fields for this object
    required = [
        'url_identifier',
        'request_handler',
        'display_name',
        'description',
    ]

    #Validator methods used to validate fields
    validators = {
        'url_identifier': validate_apiwrapper_urlidentifier,
        'request_handler': validate_api_wrapper_requesthandler,
        'display_name': validate_generic_dispalyname,
        'description': validate_generic_description,
    }

    #Indices
    indexes = [
        {'fields': 'url_identifier', 'unique': True,}
    ]

################################################################################
# UNAUTHENTICATED USER OBJECTS                                                 #
################################################################################
@con.register
class APIUsageWrapper:
    """ Code facing object designed to offer dot access to dict properties """
    def __init__(self, values):
        self.service_identifier = values['service_identifier'] if 'service_identifier' in values else None
        self.method_identifier = values['method_identifier'] if 'method_identifier' in values else None
        self.usage_calls = values['usage_calls'] if 'usage_calls' in values else 0
        self.usage_since = values['usage_since'] if 'usage_since' in values else 0

    def __eq__(self, other):
        return self.service_identifier == other.service_identifier and self.method_identifier == other.method_identifier 

@con.register
class APIUsageWrapper_CustomType(CustomType):
    """ MongoDB facing object used to offer dot access to dict properties """
    mongo_type = dict
    python_type = APIUsageWrapper

    def to_bson(self, value):
        return value.__dict__

    def to_python(self, value):
        return APIUsageWrapper(value)

@con.register
class UnAuthenticatedUser(Document):

    #The MongoDB collection to store these object in
    __collection__ = 'un_authenticated_users'

    #The database used for all objects in this project
    __database__ = 'swift_gateway'

    #Allow access to properties via dot notation
    use_dot_notation = True

    #The JSON structure of this object
    structure = {
        'host':unicode,
        'api_usage':[APIUsageWrapper_CustomType()]
    }

    #Indices
    indexes = [
        {'fields': 'host', 'unique': True,}
    ]

################################################################################
# UNAUTHENTICATED RATE ABUSERS OBJECTS                                         #
################################################################################
@con.register
class APIRateAbuse:
    """ Code facing object designed to offer dot access to dict properties """
    def __init__(self, values):
        self.service_identifier = values['service_identifier'] if 'service_identifier' in values else None
        self.method_identifier = values['method_identifier'] if 'method_identifier' in values else None
        self.rate_abuses = values['rate_abuses'] if 'rate_abuses' in values else 0
        self.abuses_since = values['abuses_since'] if 'abuses_since' in values else 0

    def __eq__(self, other):
        return self.service_identifier == other.service_identifier and self.method_identifier == other.method_identifier

@con.register
class APIRateAbuse_CustomType(CustomType):
    """ MongoDB facing object used to offer dot access to dict properties """
    mongo_type = dict
    python_type = APIRateAbuse

    def to_bson(self, value):
        return value.__dict__

    def to_python(self, value):
        return APIRateAbuse(value)

@con.register
class UnAuthenticatedRateAbuser(Document):

    #The MongoDB collection to store these object in
    __collection__ = 'un_authenticated_rate_abusers'

    #The database used for all objects in this project
    __database__ = 'swift_gateway'

    #Allow access to properties via dot notation
    use_dot_notation = True

    #The JSON structure of this object
    structure = {
        'host':unicode,
        'api_rate_abuse':[APIRateAbuse_CustomType()]
    }

    #Indices
    indexes = [
        {'fields': 'host', 'unique': True,}
    ]

