from mongokit import *
from domain.utils import con
from domain.utils import validate_apiwrapper_urlidentifier
from domain.utils import validate_generic_dispalyname
from domain.utils import validate_generic_description
from domain.utils import validate_api_wrapper_requesthandler

#Custom Types
class ObjectWrapper(dict):
    def __getattr__(self, attr):
        return self.get(attr, None)
    __setattr__= dict.__setitem__
    __delattr__= dict.__delitem__

class APIMethodWrapper(CustomType):
    mongo_type = dict
    python_type = dict

    def to_bson(self, value):
        return value;

    def to_python(self, value):
        return ObjectWrapper(value)

@con.register
class APIWrapper(Document):

    #The MongoDB collection to store these object in
    __collection__ = 'api_wrappers'
    
    #The database used for all objects in this project
    __database__ = 'swift_gateway'

    #Set to tru as this class has nested classes
    use_autorefs = True

    #Allow access to properties via dot notation
    use_dot_notation = True
    
    #The JSON structure of this object
    structure = {
        'url_identifier': unicode,
        'request_handler': unicode,
        'display_name': unicode,
        'description': unicode,
        'api_methods' : [APIMethodWrapper()]
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