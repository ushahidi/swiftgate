from urllib2 import HTTPErrorProcessor
from urllib2 import URLError
from werkzeug.wrappers import Response
from server import views
from server import mappers
from domain.utils import get_api_method_wrapper_by_url_pattern
from urllib2 import urlopen, URLError, HTTPError

def generic_error_handler(request, error_code):
    error_view_name = "error_" + error_code
    error_view = getattr(views, error_view_name)
    return error_view(request)

def generic_api_request_handler(request, api_wrapper):
    """Maps and formats the incoming request and calls the underlying API service"""

    #us the util function to extract the correct APIMethodWrapper for the request path
    api_method_wrapper = get_api_method_wrapper_by_url_pattern(request.path, api_wrapper)

    #if no element found then retutn bad request
    if api_method_wrapper is None:
        return generic_error_handler(request, "400")

    #get the mapper function for this path
    mapper = getattr(mappers, api_method_wrapper.mapper)

    #map the original request onto the api_request
    api_request = mapper(request, api_method_wrapper.endpoint)

    try:
        #call the underying api
        response = urlopen(api_request)

        #extract which view should be used to process the api response
        view = getattr(views, api_method_wrapper.view)

        #use the view to render the response
        return view(response)
    except HTTPError, e:
        #TODO: This needs to be converted into a SwiftGateway error
        pass

    return Response(response.read())



