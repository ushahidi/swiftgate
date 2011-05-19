__author__ = "Matthew Kidza-Griffiths"
__copyright__ = "Copyright 2007, Swiftly.org"
__credits__ = ["Matthew Kidza-Griffiths", "Jon Gosier"]
__license__ = "LGPL"
__version__ = "0.0.1"
__maintainer__ = "Matthew Kidza-Griffiths"
__email__ = "mg@swiftly.org"
__status__ = "Development"


from domain.models import *
from domain.utils import *

con.register([APIWrapper, APIMethodWrapper, AuthenticatedUser, AuthenticatedUserApp])

method = APIMethodWrapper({
    "method_identifier":"tag",
    "mapper":u'direct_get_request_mapper',
    "accepted_http_methods":"GET|POST",
    "url_pattern":u'/tag',
    "endpoint":u'http://opensilcc.com/api/tag',
    "view":u'silcc_tag_view',
    "open_access_calls_per_hour":100,
})

a = con.APIWrapper()
a.display_name = u'Swift Tagger'
a.description = u'Swift Tagger Service'
a.request_handler = u'generic_api_request_handler'
a.url_identifier = u'tagger/1'
a.api_methods.append(method)
a.save()


method1 = APIMethodWrapper({
    "method_identifier":"riverid-register",
    "mapper":u'post_request_mapper_with_gateway_oauth_credentials',
    "accepted_http_methods":"POST",
    "url_pattern":u'/register',
    "endpoint":u'http://50.57.68.23/thegateway/register',
    "view":u'riverid_register_view',
    "open_access_calls_per_hour":100,
})
method2 = APIMethodWrapper({
    "method_identifier":"riverid-validatecredentials",
    "mapper":u'post_request_mapper_with_gateway_oauth_credentials',
    "accepted_http_methods":"POST",
    "url_pattern":u'/authenticate',
    "endpoint":u'http://50.57.68.23/thegateway/validatecredentials',
    "view":u'riverid_validatecredentials_view',
    "open_access_calls_per_hour":100,
})

a = con.APIWrapper()
a.display_name = u'RiverID'
a.description = u'RiverID'
a.request_handler = u'generic_api_request_handler'
a.url_identifier = u'riverid/1'
a.api_methods.append(method1)
a.api_methods.append(method2)
a.save()


con.register([PricePlan, PricePlanRule])

rule = PricePlanRule({
    "service":u'tagger/1',
    "group":"user",
    "api_method":None,
    "permitted_calls":10,
    "per":3600
})

p = con.PricePlan()
p.name = u'Free Access'
p.active = True
p.price = float(0)
p.rules.append(rule)
p.save()
