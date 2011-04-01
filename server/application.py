from urllib2 import URLError
from werkzeug.wrappers import Request
from werkzeug.wsgi import ClosingIterator
from server.utils import local, local_manager, map_path_to_api_wrapper_identifier
from server import handlers
from server.handlers import generic_error_handler
from server.models import RequestUser
from domain.utils import get_api_wrapper_by_identifier
from domain.utils import get_api_method_wrapper_by_url_pattern
from domain.models import *
import re

class Server(object):

    def __init__(self):
        local.application = self

    def __call__(self, environ, start_response):
        local.application = self
        request = Request(environ)

        #extract the service identifier from the path
        service_identifier = map_path_to_api_wrapper_identifier(request.path)

        #Disallow access to the root
        if service_identifier is None:
            response = generic_error_handler(request, '403', 'Access to the root is not permitted')
            return ClosingIterator(response(environ, start_response), [local_manager.cleanup])

        #Check for XSS atacks that contain none word chars
        xss_atack_rule = re.compile("^\w+$", re.IGNORECASE)
        if not bool(xss_atack_rule.match(service_identifier)):
            #TODO: this should be logged as a possible attack
            response = generic_error_handler(request, '400', 'Humm, it looks like you are trying a XSS attack? If not, make sure you are encoding your request url.')
            return ClosingIterator(response(environ, start_response), [local_manager.cleanup])

        #Get the API Wrapper from the datastore
        api_wrapper = get_api_wrapper_by_identifier(service_identifier)

        #If the extracted service_identifier does not match
        if api_wrapper is None:
            response = generic_error_handler(request, '404', 'Sorry, we could not find a service that matches "%s". Please check our documentation.' % (service_identifier))
            return ClosingIterator(response(environ, start_response), [local_manager.cleanup])

        #use the util function to extract the correct APIMethodWrapper for the request path
        api_method_wrapper = get_api_method_wrapper_by_url_pattern(request.path, api_wrapper)

        #if no element found then retutn bad request
        if api_method_wrapper is None:
            response = generic_error_handler(request, "400", 'Sorry, we could not find the method you wanted on the service "%s". Please check our documentation.' % (service_identifier))
            return ClosingIterator(response(environ, start_response), [local_manager.cleanup])

        #check that the request method is supported by this api_method
        if not bool(re.match(r'^[\w|]*%s[\w|]*$' % (request.method), api_method_wrapper.accepted_http_methods)):
            response = generic_error_handler(request, "405", 'Sorry, the service you are trying to access doesn not support the request type "%s".' % (request.method))
            response.headers.add("Allow", re.sub(r'\|', ', ', api_method_wrapper.accepted_http_methods))
            return ClosingIterator(response(environ, start_response), [local_manager.cleanup])

        #build a new request user object
        user = RequestUser(request, api_wrapper)

        #assert that api access is ok and record it
        access_data = user.record_api_access(api_method_wrapper)

        #if the request user can not be granted access then return a 401
        if access_data.access_status is 'denied':
            response = generic_error_handler(request, '401', access_data.access_message)
            return ClosingIterator(response(environ, start_response), [local_manager.cleanup])

        #Try to match build the mapper
        handler = getattr(handlers, api_wrapper.request_handler)

        try:
            response = handler(request, api_method_wrapper)
        except URLError :
            #TODO this needs to be handled as this means there is an error in our endpoint mapping or a service is down!
            pass

        return ClosingIterator(response(environ, start_response), [local_manager.cleanup])