__author__ = "Matthew Kidza-Griffiths"
__copyright__ = "Copyright 2007, Swiftly.org"
__credits__ = ["Matthew Kidza-Griffiths", "Jon Gosier"]
__license__ = "LGPL"
__version__ = "0.0.1"
__maintainer__ = "Matthew Kidza-Griffiths"
__email__ = "mg@swiftly.org"
__status__ = "Development"

import oauth2
import time
import urllib2
import urllib
from urllib2 import URLError


def build_request(key, secret, url, method='POST', values={}):
    params = {
        'oauth_timestamp': int(time.time()),
        'oauth_nonce': None,
        'oauth_signature_method':'HMAC-SHA1',
    }
    params.update(values)
    consumer = oauth2.Consumer(key=key,secret=secret)
    req = oauth2.Request(method=method, url=url, parameters=params)
    signature_method = oauth2.SignatureMethod_HMAC_SHA1()
    req.sign_request(signature_method, consumer, None)
    return req


key = u'cbdc0b2dfb040772ba0cc6c93189d45a8eb84049f55cbef752c2cc2e'
secret = u'1dcc5bafe6a425a6f149604745299148f66eb1229e4146aad9b98cf7'
url = "http://local.swiftgateway.com/swiftmeme/1/authenticate"
#url = "http://localhost:5000/swiftmeme/1/authenticate"
values = {
    'riverid':'test1',
    'password':'password'
}
request = build_request(key, secret, url, values=values)
data = urllib.urlencode(values)
try :
    req = urllib2.Request(url, headers=request.to_header(), data=data)
    u = urllib2.urlopen(req)
    print u.read()
except URLError, e:
    print e
