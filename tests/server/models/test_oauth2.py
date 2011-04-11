import oauth2 as oauth
import urllib
import unittest
from urlparse import parse_qs, parse_qsl

class Test_oauth_request(unittest.TestCase):
    def test_from_request(self):
        url = "http://sp.example.com/"

        params = {
            'oauth_version': "1.0",
            'oauth_nonce': "4572616e48616d6d65724c61686176",
            'oauth_timestamp': "137131200",
            'oauth_consumer_key': "0685bd9184jfhq22",
            'oauth_signature_method': "HMAC-SHA1",
            'oauth_signature': "wOJIO9A2W5mFwDgiDvZbTSMK%2FPY%3D",
        }

        req = oauth.Request("GET", url, params)
        headers = req.to_header()

        # Test from the headers
        req = oauth.Request.from_request("GET", url, headers)
        self.assertEquals(req.method, "GET")
        self.assertEquals(req.url, url)

        self.assertEquals(params, req.copy())

        # Test with bad OAuth headers
        bad_headers = {
            'Authorization' : 'OAuth this is a bad header'
        }

        self.assertRaises(oauth.Error, oauth.Request.from_request, "GET",
            url, bad_headers)

        # Test getting from query string
        qs = urllib.urlencode(params)
        req = oauth.Request.from_request("GET", url, query_string=qs)

        exp = parse_qs(qs, keep_blank_values=False)
        for k, v in exp.iteritems():
            exp[k] = urllib.unquote(v[0])

        self.assertEquals(exp, req.copy())

        # Test that a boned from_request() call returns None
        req = oauth.Request.from_request("GET", url)
        self.assertEquals(None, req)