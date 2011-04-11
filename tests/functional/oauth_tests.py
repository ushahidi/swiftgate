import oauth2
import urllib2
from urllib2 import URLError
import time

url = 'http://localhost:5000/tagger/v1.0/tag?text=this+is+a+test'


params = {
    'oauth_version': "1.0",
    'oauth_nonce': "4572616e48616d6d65724c61686176",
    'oauth_timestamp': "137131200",
    'oauth_consumer_key': "0685bd9184jfhq22",
    'oauth_signature_method': "HMAC-SHA1",
    'oauth_token': "ad180jjd733klru7",
    'oauth_signature': "wOJIO9A2W5mFwDgiDvZbTSMK%2FPY%3D",
}

req = oauth2.Request("GET", url, params)

signature_method = oauth2.SignatureMethod_HMAC_SHA1()

consumer = oauth2.Consumer(key='0685bd9184jfhq22',secret='secret')

req.sign_request(signature_method, consumer, None)

request = urllib2.Request('http://localhost:5000/tagger/v1.0/tag?text=this+is+a+test', headers=req.to_header())


try :
    u = urllib2.urlopen(request)
    print u.read()
except URLError, e:
    print e
