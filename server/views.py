__author__ = "Matthew Kidza-Griffiths"
__copyright__ = "Copyright 2007, Swiftly.org"
__credits__ = ["Matthew Kidza-Griffiths", "Jon Gosier"]
__license__ = "LGPL"
__version__ = "0.0.1"
__maintainer__ = "Matthew Kidza-Griffiths"
__email__ = "mg@swiftly.org"
__status__ = "Development"


from werkzeug.wrappers import Response
from server.utils import create_standard_json_response
from server.utils import add_standard_json_html_response_headers
from server.utils import add_503_error_html_response_headers
from server.utils import add_error_html_response_headers
from server.utils import versions
import json
import re

def error_400(request, error_message):
    response = Response('Bad Request: ' + error_message)
    response.status_code = 400
    add_error_html_response_headers(response)
    return response

def error_401(request, error_message):
    response = Response('Unauthorized: ' + error_message)
    response.status_code = 401
    add_error_html_response_headers(response)
    return response

def error_404(request, error_message):
    response = Response('Not Found: ' + error_message)
    response.status_code = 404
    add_error_html_response_headers(response)
    return response

def error_403(request, error_message):
    response = Response('Forbidden: ' + error_message)
    response.status_code = 403
    add_error_html_response_headers(response)
    return response

def error_405(request, error_message):
    response = Response('Method Not Allowed: ' + error_message)
    response.status_code = 405
    add_error_html_response_headers(response)
    return response

def error_503(request, error_message):
    response = Response('Unavailable: ' + error_message)
    response.status_code = 503
    add_503_error_html_response_headers(response)
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

def riverid_register_view(api_response):
    json_string = api_response.read()
    data = json.loads(json_string)
    if data['status'] == 'Succeeded':
        response_json = create_standard_json_response('riverid','register','success')
    else:
        response_json = create_standard_json_response('riverid','register','failure', {'errors':data['errors']}, False)
    response = Response(response_json)
    add_standard_json_html_response_headers(response)
    response.headers.add("Server", "RiverID/%s Swiftriver/%s" % (versions["riverid"], versions["swiftriver"]))
    return response

def riverid_validatecredentials_view(api_response):
    json_string = api_response.read()
    data = json.loads(json_string)
    if data['status'] == 'Succeeded':
        response_json = create_standard_json_response('riverid','validatecredentials','success')
    else:
        response_json = create_standard_json_response('riverid','validatecredentials','failure', {'errors':data['errors']}, False)
    response = Response(response_json)
    add_standard_json_html_response_headers(response)
    response.headers.add("Server", "RiverID/%s Swiftriver/%s" % (versions["riverid"], versions["swiftriver"]))
    return response

def swiftmeme_authentication_view(method, result, data):
    response_json = create_standard_json_response("swiftmeme", method, result, data, False)
    response = Response(response_json)
    add_standard_json_html_response_headers(response)
    response.headers.add("Server", "SwiftMeme/%s Swiftriver/%s" % (versions["swiftmeme"], versions["swiftriver"]))
    return response

def swiftmeme_memeoverview_view(result, data):
    response_json = create_standard_json_response("swiftmeme", 'getmemeoverview', result, data, False)
    response = Response(response_json)
    add_standard_json_html_response_headers(response)
    response.headers.add("Server", "SwiftMeme/%s Swiftriver/%s" % (versions["swiftmeme"], versions["swiftriver"]))
    return response