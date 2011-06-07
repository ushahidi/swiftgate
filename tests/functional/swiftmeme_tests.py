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

def test_authenticate():
    key = u'4e0ed29e0cb4abf252cb1cbf4d83a95df2318a5bd6f605b91268ecae'
    secret = u'f84eb46c788966b4b0f412cd8001d75f49a2b79daa9df9b749a045e3'
    url = "http://local.swiftgateway.com/swiftmeme/1/authenticate"
    #url = "http://localhost:5000/swiftmeme/1/authenticate"
    values = {
        'riverid':'test1',
        'password':'password',
    }
    request = build_request(key, secret, url, values=values)
    data = urllib.urlencode(values)
    try :
        req = urllib2.Request(url, headers=request.to_header(), data=data)
        u = urllib2.urlopen(req)
        print u.read()
    except URLError, e:
        print e
        
def test_get_memeoverview():
    key = u'e0f0868b2df990c1a802e9ea186f2f8b473aeebdb1ce171122b46157'
    secret = u'b0f1dfe52ce778646ec095b0e0fec9113fa437b7b3d9b58ac946b6fc'
    url = "http://local.swiftgateway.com/swiftmeme/1/getmemeoverview"
    values = {"some":"thing"}
    request = build_request(key, secret, url, values=values)
    data = urllib.urlencode(values)
    try :
        req = urllib2.Request(url, headers=request.to_header(), data=data)
        u = urllib2.urlopen(req)
        print u.read()
    except URLError, e:
        print e
        
#test_authenticate()
test_get_memeoverview()
    
