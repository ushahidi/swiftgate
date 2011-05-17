__author__ = "Matthew Kidza-Griffiths"
__copyright__ = "Copyright 2007, Swiftly.org"
__credits__ = ["Matthew Kidza-Griffiths", "Jon Gosier"]
__license__ = "LGPL"
__version__ = "0.0.1"
__maintainer__ = "Matthew Kidza-Griffiths"
__email__ = "mg@swiftly.org"
__status__ = "Development"


from urllib import quote
from urllib2 import Request

def direct_get_request_mapper(request, api_endpoint):
    """
    Method to map the GET parameters from one request on to a new urllib2.request
    all parameters will be encoded and any trailing slashes on the api_endpoint
    will be removed
    """

    #Set up the new quey string
    new_query = ""

    #Loop over the query parametes of the werkzeug.wrappers.Request object
    for key in request.args.keys():
        new_query += key + "=" + quote(request.args[key]) + "&"

    #remove any trainling amphastands
    new_query = new_query.rstrip('&')

    #remove any trailing slashes on the api_endpoint
    uri = api_endpoint.rstrip('/')

    #if thete is a new query string then append it to the api_endpoint to create a uri
    if len(new_query) :
        uri = uri + "?" + new_query

    #Create a new urllib2.Request object from the url
    new_request = Request(uri)

    #TODO: Add request headers
    return new_request



