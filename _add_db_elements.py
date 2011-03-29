from domain.models import *
from domain.utils import *

con.register([APIWrapper])

method = {
    "mapper":u'direct_get_request_mapper',
    "url_pattern":u'/tag',
    "endpoint":u'http://opensilcc.com/api/tag',
    "view":u'silcc_tag_view',
}

a = con.APIWrapper()
a.display_name = u'Swift Tagger'
a.description = u'Swift Tagger Service'
a.request_handler = u'generic_api_request_handler'
a.url_identifier = u'tagger'
a.api_methods.append(method)
a.save()

