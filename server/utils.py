from werkzeug.local import Local, LocalManager
import simplejson as json
import urllib2
import re

#Basic wgis setup
local = Local()
local_manager = LocalManager([local])
application = local('application')

#version number
versions = {
    "python":"2.7.1",
    "werkzeug":"0.6.2",
    "swiftriver":"0.5.6",
    "swiftgateway":"0.1",
    "silcc":"0.1",
}

class DefaultErrorHandler(urllib2.HTTPDefaultErrorHandler):
    def http_error_default(self, req, fp, code, msg, headers):
        result = urllib2.HTTPError(req.get_full_url(), code, msg, headers, fp)
        result.status = code
        return result

def map_path_to_api_wrapper_identifier(path):
    if path == None or len(path) < 1 or unicode(path) == u'/':
        return None
    identifier_parts = path.lstrip('/').split('/')
    if len(identifier_parts) < 2:
        return None
    identifier = "%s/%s" % (identifier_parts[0], identifier_parts[1])
    return unicode(identifier)

def create_standard_json_response(api_identifier, api_method, status, response, response_is_json=True):
    if response_is_json :
        response_as_dict = json.loads(response)
        json_response = json.dumps({'service': api_identifier,'method': api_method,'status': status,'response':response_as_dict})
    else :
        json_response = json.dumps({'service': api_identifier,'method': api_method,'status': status,'response':response})
    return unicode(json_response, "utf-8")

def add_standard_html_response_headers(response):
    response.headers.add('Via', 'SwiftGateway/%s Werkzeug/%s Python/%s' % (versions['swiftgateway'], versions['werkzeug'], versions['python']))

def add_standard_json_html_response_headers(response):
    add_standard_html_response_headers(response)
    response.content_type = 'application/json; charset=utf-8'
    

def is_oauth_request(request):
    if not 'Authorization' in request.headers :
        return False
    oauth_rule = re.compile(r'^oauth', re.IGNORECASE)
    authorization = request.headers['Authorization'].strip()
    return bool(oauth_rule.match(authorization))
