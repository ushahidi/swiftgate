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
a.url_identifier = u'tagger/v1.0'
a.api_methods.append(method)
a.save()

