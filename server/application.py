from urllib2 import URLError
from werkzeug.wrappers import Request
from werkzeug.wsgi import ClosingIterator
from server.utils import local, local_manager, map_path_to_api_wrapper_identifier
from server import handlers
from server.handlers import generic_error_handler
from domain.utils import get_api_wrapper_by_identifier
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
            response = generic_error_handler(request, '403')
            return ClosingIterator(response(environ, start_response), [local_manager.cleanup])

        #Check for XSS atacks that contain none word chars
        xss_atack_rule = re.compile("^\w+$", re.IGNORECASE)
        if not bool(xss_atack_rule.match(service_identifier)):
            #TODO: this should be logged as a possible attack
            response = generic_error_handler(request, '400')
            return ClosingIterator(response(environ, start_response), [local_manager.cleanup])

        #Get the API Wrapper from the datastore
        api_wrapper = get_api_wrapper_by_identifier(service_identifier)

        #If the extracted service_identifier does not match
        if api_wrapper is None:
            response = generic_error_handler(request, '404')
            return ClosingIterator(response(environ, start_response), [local_manager.cleanup])

        #Try to match build the mapper
        handler = getattr(handlers, api_wrapper.request_handler)
        try:
            response = handler(request, api_wrapper)
        except URLError, e :
            #TODO this needs to be handled as this means there is an error in our endpoint mapping or a service is down!
            pass

        return ClosingIterator(response(environ, start_response), [local_manager.cleanup])