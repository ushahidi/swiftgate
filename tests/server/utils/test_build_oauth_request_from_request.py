from server.utils import build_oauth_request_from_request
import oauth2 as oauth
import unittest

class Test_build_oauth_request_from_request(unittest.TestCase):
    def test_pass_withfullheaderstring(self):
        header = {"Authorization" : 'OAuth realm="apis.swiftly.org", oauth_body_hash="2jmj7l5rSw0yVb%2FvlWAYkK%2FYBwk%3D", oauth_nonce="4572616e48616d6d65724c61686176", oauth_timestamp="137131200", oauth_consumer_key="test", oauth_signature_method="HMAC-SHA1", oauth_version="1.0", oauth_token="ad180jjd733klru7", oauth_signature="DMGKIfmjk5s4EbyG6qDT5zu0BRw%3D"'}
        method = "GET"
        url = "http://apis.swiftly.org/tagger/v1.0/tag?text=hi%20there"
        request = build_oauth_request_from_request(method, url, header)
        self.assertFalse(request == None)
        self.assertEqual(request.method, method)
        self.assertEqual(request.url, url)

    def test_pass_usinfoauth2request(self):
        params = {
            'realm' : 'apis.swiftly.org',
            'oauth_version': "1.0",
            'oauth_nonce': "4572616e48616d6d65724c61686176",
            'oauth_timestamp': "137131200",
            'oauth_consumer_key': "0685bd9184jfhq22",
            'oauth_signature_method': "HMAC-SHA1",
            'oauth_signature': "wOJIO9A2W5mFwDgiDvZbTSMK%2FPY%3D",
        }
        method = "GET"
        url = "http://apis.swiftly.org/tagger/v1.0/tag?text=hi%20there"
        original_request = oauth.Request(method, url, params)
        header = original_request.to_header()
        request = build_oauth_request_from_request(method, url, header)
        self.assertFalse(request == None)
        self.assertEqual(request.method, method)
        self.assertEqual(request.url, url)

    def test_fail_withemptyheaderstring(self):
        header = {} #{"Authorization" : 'OAuth realm="apis.swiftly.org", oauth_body_hash="2jmj7l5rSw0yVb%2FvlWAYkK%2FYBwk%3D", oauth_nonce="4572616e48616d6d65724c61686176", oauth_timestamp="137131200", oauth_consumer_key="test", oauth_signature_method="HMAC-SHA1", oauth_version="1.0", oauth_token="ad180jjd733klru7", oauth_signature="DMGKIfmjk5s4EbyG6qDT5zu0BRw%3D"'}
        method = "GET"
        url = "http://apis.swiftly.org/tagger/v1.0/tag?text=hi%20there"
        request = build_oauth_request_from_request(method, url, header)
        self.assertFalse(request == None)
        self.assertEqual(request.method, method)
        self.assertEqual(request.url, url)

