from werkzeug.wrappers import Response
from server.utils import create_standard_json_response
from server.utils import add_standard_json_html_response_headers
from server.utils import versions
import re

def error_400(request):
    response = Response('Bad Request')
    response.status_code = 400
    return response

def error_404(request):
    response = Response('Not Found')
    response.status_code = 404
    return response

def error_403(request):
    response = Response('Forbidden')
    response.status_code = 403
    return response

def silcc_tag_view(api_response):
    rule = re.compile(r'^\d{3}', re.IGNORECASE)
    response_data = api_response.read()
    response_is_json = not bool(rule.match(response_data))
    if response_is_json :
        response_json = create_standard_json_response('tagger','tag','success','{"tags":%s}' % response_data)
    else :
        response_json = create_standard_json_response('tagger','tag','failure',response_data,False)
    response = Response(response_json)
    add_standard_json_html_response_headers(response)
    response.headers.add("Server", "SiLCC/%s Swiftriver/%s" % (versions["silcc"], versions["swiftriver"]))
    return response