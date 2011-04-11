from server.utils import extract_oauth_consumer_key_from_auth_header_string
import oauth2 as oauth
import unittest

class Test_extract_oauth_consumer_key_from_auth_header_string(unittest.TestCase):
    def test_pass_withjustconsumerkey(self):
        header = 'oauth_consumer_key="test"'
        result = extract_oauth_consumer_key_from_auth_header_string(header)
        self.assertEqual(result, 'test')

    def test_pass_withfullheaderstring(self):
        header = 'OAuth realm="", oauth_body_hash="2jmj7l5rSw0yVb%2FvlWAYkK%2FYBwk%3D", oauth_nonce="4572616e48616d6d65724c61686176", oauth_timestamp="137131200", oauth_consumer_key="test", oauth_signature_method="HMAC-SHA1", oauth_version="1.0", oauth_token="ad180jjd733klru7", oauth_signature="DMGKIfmjk5s4EbyG6qDT5zu0BRw%3D"'
        result = extract_oauth_consumer_key_from_auth_header_string(header)
        self.assertEqual(result, 'test')

    def test_pass_usingoauth2header(self):
        params = {
            'oauth_version': "1.0",
            'oauth_nonce': "4572616e48616d6d65724c61686176",
            'oauth_timestamp': "137131200",
            'oauth_consumer_key': "0685bd9184jfhq22",
            'oauth_signature_method': "HMAC-SHA1",
            'oauth_signature': "wOJIO9A2W5mFwDgiDvZbTSMK%2FPY%3D",
        }

        request = oauth.Request("GET", "http://SomeOtherUrl.com", params)
        header = request.to_header()
        auth_header_string = header['Authorization']
        result = extract_oauth_consumer_key_from_auth_header_string(auth_header_string)
        self.assertEqual(result, '0685bd9184jfhq22')
