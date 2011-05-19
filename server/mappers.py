__author__ = "Matthew Kidza-Griffiths"
__copyright__ = "Copyright 2007, Swiftly.org"
__credits__ = ["Matthew Kidza-Griffiths", "Jon Gosier"]
__license__ = "LGPL"
__version__ = "0.0.1"
__maintainer__ = "Matthew Kidza-Griffiths"
__email__ = "mg@swiftly.org"
__status__ = "Development"

from configuration.configuration import config
from urllib import quote, urlencode
from urllib2 import Request
import oauth2
import time

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

def post_request_mapper_with_gateway_oauth_credentials(request, api_endpoint):
    """
    Method to map the POST parameters from one request on to a new urllib2.request
    Also add the configured gateway oath credentials and siging
    """

    key = config.get('oauthcredentials', 'oauth_consumer_key')
    secret = config.get('oauthcredentials', 'oauth_secret')
    url = api_endpoint

    values = [(k,v) for k,v in request.values.iteritems()]

    params = {
        'oauth_timestamp': int(time.time()),
        'oauth_nonce': None,
        'oauth_signature_method':'HMAC-SHA1',
        'oauth_consumer_key':key,
    }
    params.update(values)
    consumer = oauth2.Consumer(key=key,secret=secret)
    oauth_request = oauth2.Request(method='POST', url=url, parameters=params)
    signature_method = oauth2.SignatureMethod_HMAC_SHA1()
    oauth_request.sign_request(signature_method, consumer, None)
    data = urlencode(values)

    new_request = Request(url, headers=oauth_request.to_header(), data=data)

    #TODO Add request headers
    return new_request




