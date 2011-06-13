__author__ = "Matthew Kidza-Griffiths"
__copyright__ = "Copyright 2007, Swiftly.org"
__credits__ = ["Matthew Kidza-Griffiths", "Jon Gosier"]
__license__ = "LGPL"
__version__ = "0.0.1"
__maintainer__ = "Matthew Kidza-Griffiths"
__email__ = "mg@swiftly.org"
__status__ = "Development"


from werkzeug.wrappers import Response
from server import views
from server import mappers
from urllib2 import urlopen, HTTPError
from domain.models import *
from domain.utils import get_all_price_plans_for_app_template
from domain.utils import get_authenticated_user_by_id
from domain.utils import create_new_subscription
from domain.utils import get_authenticated_user_by_riverid
from server.mashups.swiftmeme import run_swiftmeme_authentication_adapter
from server.mashups.swiftmeme import run_swiftmeme_memeoverview_adapter
from server.mashups.swiftmeme import run_swiftmeme_analytics_adapter
import hashlib
import json
import time
import re

def generic_error_handler(request, error_code, error_message):
    #TODO: Pass the error_message to the view
    error_view_name = "error_" + error_code
    error_view = getattr(views, error_view_name)
    return error_view(request, error_message)

def generic_api_request_handler(request, api_method_wrapper):
    """Maps and formats the incoming request and calls the underlying API service"""

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

def swiftmeme_request_handler(request, api_method_wrapper):
    
    method_id = api_method_wrapper.method_identifier
    
    if method_id == "authenticate" or method_id == "register":
        return run_swiftmeme_authentication_adapter(request, api_method_wrapper)
    elif method_id == "getmemeoverview":
        return run_swiftmeme_memeoverview_adapter(request, api_method_wrapper)
    elif method_id == "getmemeanalytics":
        return run_swiftmeme_analytics_adapter(request, api_method_wrapper)
    else:
        view = getattr(views, "error_404")
        return view(request, "The method you request is not allowed")
        
        



