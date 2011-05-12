
import oauth2
import time
import urllib2
from urllib2 import URLError

key = u'49fc138064349744dea151a2348d015a29bd6ebde7fb839873776248'
secret = u'5cc53eaa2d8d2d90590e7434c5e65c4576156f3b29c580941bffd067'
url = 'http://localhost:5000/tagger/1/tag?text=this+is+a+test'

def build_request(url, method='GET'):
    params = {
        'oauth_timestamp': int(time.time()),
        'oauth_nonce': None,
        'oauth_signature_method':'HMAC-SHA1'
    }
    consumer = oauth2.Consumer(key=key,secret=secret)
    params['oauth_consumer_key'] = consumer.key
    req = oauth2.Request(method=method, url=url, parameters=params)
    signature_method = oauth2.SignatureMethod_HMAC_SHA1()
    req.sign_request(signature_method, consumer, None)
    return req

request = build_request(url)

try :
    #req = urllib2.Request(url, headers=request.to_header())
    #u = urllib2.urlopen(req)
    u = urllib2.urlopen(request.to_url())
    print u.read()
except URLError, e:
    print e

"""
import httplib
import time
import oauth.oauth as oauth

key = u'57f31a0dd9b69c385c9c9703f8c8932adb60c896fc1c564204fa086d'
secret = u'159cdbb1841ccec4c3a409c62f981cb6f295f17a9a1d3b2ce8a9d58a'
url = 'http://localhost:5000/tagger/1/tag?text=this+is+a+test'


class SimpleOAuthClient(oauth.OAuthClient):
    def __init__(self, server, port=httplib.HTTP_PORT, request_token_url='', access_token_url='', authorization_url=''):
        self.server = server
        self.port = port
        self.request_token_url = request_token_url
        self.access_token_url = access_token_url
        self.authorization_url = authorization_url
        self.connection = httplib.HTTPConnection("%s:%d" % (self.server, self.port))

    def access_resource(self, oauth_request):
        self.connection.request(oauth_request.http_method, url, headers=oauth_request.to_header())
        response = self.connection.getresponse()
        return response.read()

consumer = oauth.OAuthConsumer(key, secret)
signature_method_hmac_sha1 = oauth.OAuthSignatureMethod_HMAC_SHA1()
oauth_request = oauth.OAuthRequest.from_consumer_and_token(consumer, token=None, http_method='GET', http_url=url, parameters=None)
oauth_request.sign_request(signature_method_hmac_sha1, consumer, None)
try :
    print client.access_resource(oauth_request)
except URLError, e:
    print e


import oauth2
import urllib2
from urllib2 import URLError
import time



params = {
    'oauth_version': "1.0",
    'oauth_nonce': "4572616e48616d6d65724c61686176",
    'oauth_timestamp': int(time.time()),
    'oauth_consumer_key': key,
    'oauth_signature_method': "HMAC-SHA1",
    'oauth_token': None,
}

req = oauth2.Request("GET", url, params)

signature_method = oauth2.SignatureMethod_HMAC_SHA1()

consumer = oauth2.Consumer(key=key,secret=secret)

req.sign_request(signature_method, consumer, None)

print req.to_header()

request = urllib2.Request(url, headers=req.to_header())

try :
    u = urllib2.urlopen(request)
    print u.read()
except URLError, e:
    print e
"""