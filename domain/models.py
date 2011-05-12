import time
from mongokit import *
from domain.utils import con
from domain.utils import validate_apiwrapper_urlidentifier
from domain.utils import validate_generic_dispalyname
from domain.utils import validate_generic_description
from domain.utils import validate_api_wrapper_requesthandler
import MySQLdb
import md5
from configuration.configuration import config

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

################################################################################
# AUTHENTICATED USER OBJECTS                                                   #
################################################################################
@con.register
class AuthenticatedUserApp(object):
    """ Code facing object designed to offer dot access to dict properties """
    def __init__(self, values):
        self.key = values['key'] if 'key' in values else None
        self.secret = values['secret'] if 'secret' in values else None
        self.name = values['name'] if 'name' in values else None
        self.subscription_ids = values['subscription_ids'] if 'subscription_ids' in values else []

@con.register
class AuthenticatedUserApp_CustomType(CustomType):
    """ MongoDB facing object used to offer dot access to dict properties """
    mongo_type = dict
    python_type = AuthenticatedUserApp

    def to_bson(self, value):
        return value.__dict__

    def to_python(self, value):
        return AuthenticatedUserApp(value)

@con.register
class AuthenticatedUser(Document):

    #The MongoDB collection to store these object in
    __collection__ = 'authenticated_users'

    #The database used for all objects in this project
    __database__ = 'swift_gateway'

    #Allow access to properties via dot notation
    use_dot_notation = True

    #The JSON structure of this object
    structure = {
        'username':unicode,
        'apps':[AuthenticatedUserApp_CustomType()],
    }

    #Indices
    indexes = [
        {'fields': 'username', 'unique': True,}
    ]


################################################################################
# PRICE PLANS - The price plans offered                                        #
################################################################################
@con.register
class PricePlanRule(object):
    """ Code facing object designed to offer dot access to dict properties """
    def __init__(self, values):
        self.service = values['service'] if 'service' in values else None
        self.api_method = values['api_method'] if 'api_method' in values else None
        self.permitted_calls = values['permitted_calls'] if 'permitted_calls' in values else None
        self.per = values['per'] if 'per' in values else None

@con.register
class PricePlanRule_CustomType(CustomType):
    """ MongoDB facing object used to offer dot access to dict properties """
    mongo_type = dict
    python_type = PricePlanRule

    def to_bson(self, value):
        return value.__dict__

    def to_python(self, value):
        return PricePlanRule(value)

@con.register
class PricePlan(Document):

    #The MongoDB collection to store these object in
    __collection__ = 'price_plans'

    #The database used for all objects in this project
    __database__ = 'swift_gateway'

    #Allow access to properties via dot notation
    use_dot_notation = True

    #The JSON structure of this object
    structure = {
        'name':unicode,
        'active':bool,
        'price':float,
        'rules':[PricePlanRule_CustomType()]
    }

################################################################################
# APP SUBSCRIPTIONS - the subscription properties that are allocated to an app #
################################################################################
@con.register
class Subscription(Document):

    #The MongoDB collection to store these object in
    __collection__ = 'subscriptions'

    #The database used for all objects in this project
    __database__ = 'swift_gateway'

    #Allow access to properties via dot notation
    use_dot_notation = True

    #Allows auto linking back to the price plan
    use_autorefs = True

    #The JSON structure of this object
    structure = {
        'start_date':int,
        'validity_period':int,
        'usage_plan':PricePlan,
        'usage':dict
    }


################################################################################
# SERVICE USER STATISTICS - Not implemented with Mongo, just plain old sql     #
################################################################################
@con.register
class APIUsageStatistics(dict):
    def save_stage_one(self):
        self['save_stage_one'] = True
        id = md5.md5("%s %d" % (self['remote_ip'], self['start_time'])).hexdigest()
        if not 'state' in self:
            self['state'] = 'none'
        if 'service_id' in self and 'method_id' in self and 'app_id' in self:
            sql = "INSERT INTO requests_current VALUES('%s','%s','%s','%s','%s','%s','%s',%f,NULL)" % (
                id,
                self['state'],
                self['remote_ip'],
                self['app_id'],
                self['service_id'],
                self['method_id'],
                self['service_name'],
                self['start_time'])
        elif 'service_id' in self and 'method_id' in self:
            sql = "INSERT INTO requests_current VALUES('%s','%s','%s',NULL,'%s','%s','%s',%f,NULL)" % (
                id,
                self['state'],
                self['remote_ip'],
                self['service_id'],
                self['method_id'],
                self['service_name'],
                self['start_time'])
        elif 'service_id' in self:
            sql = "INSERT INTO requests_current VALUES('%s','%s','%s',NULL,'%s',NULL,'%s',%f,NULL)" % (
                id,
                self['state'],
                self['remote_ip'],
                self['service_id'],
                self['service_name'],
                self['start_time'])
        else:
            sql = "INSERT INTO requests_current VALUES('%s','%s','%s',NULL,NULL,NULL,NULL,%f,NULL)" % (
                id,
                self['state'],
                self['remote_ip'],
                self['start_time'])
        self['sql_stage_one'] = sql
        con = MySQLdb.connect(
            host=config.get('mysql', 'host'),
            user=config.get('mysql', 'user'),
            passwd=config.get('mysql', 'password'),
            db=config.get('mysql', 'database'))
        cur = con.cursor()
        cur.execute(sql)
        cur.close()
        con.close()

    def save_stage_two(self):
        if 'save_stage_one' not in self:
            self.save_stage_one()
        if 'end_time' not in self:
            self['end_time'] = time.time()
        id = md5.md5("%s %d" % (self['remote_ip'], self['start_time'])).hexdigest()
        if 'app_id' in self:
            sql = "UPDATE requests_current SET app_id = '%s', end_time = '%f' WHERE id = '%s'" % (
                self['app_id'],
                self['end_time'],
                id)
        else:
            sql = "UPDATE requests_current SET end_time = '%f' WHERE id = '%s'" % (
                self['end_time'],
                id)
        self['sql_stage_two'] = sql
        con = MySQLdb.connect(
            host=config.get('mysql', 'host'),
            user=config.get('mysql', 'user'),
            passwd=config.get('mysql', 'password'),
            db=config.get('mysql', 'database'))
        cur = con.cursor()
        cur.execute(sql)
        cur.close()
        con.close()

    def sql_dump(self):
        sql_one = self['sql_stage_one'] if 'sql_stage_one' in self else ''
        sql_two = self['sql_stage_two'] if 'sql_stage_two' in self else ''
        return sql_one + " | " + sql_two

