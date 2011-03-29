from server.utils import is_oauth_request
from werkzeug.test import create_environ
from werkzeug.wrappers import Request
import unittest

class Test_is_oauth_request(unittest.TestCase):
    def test_pass_withemptyheader(self):
        mock = MockBuilder({"headers":{}})
        oauth = is_oauth_request(mock)
        self.assertFalse(oauth)

    def test_pass_withauthheadercorrectcase(self):
        mock = MockBuilder({"headers":{"Authorization":"Oauth something"}})
        oauth = is_oauth_request(mock)
        self.assertTrue(oauth)

    def test_pass_withauthheaderincorrectcase(self):
        mock = MockBuilder({"headers":{"Authorization":"Oauth something"}})
        oauth = is_oauth_request(mock)
        self.assertTrue(oauth)

    def test_pass_notmatchbasicauth(self):
        mock = MockBuilder({"headers":{"Authorization": "Basic sothing"}})
        oauth = is_oauth_request(mock)
        self.assertFalse(oauth)

    def test_pass_withspaceandwrongcaseinauthstring(self):
        mock = MockBuilder({"headers":{"Authorization": "  oauth something"}})
        oauth = is_oauth_request(mock)
        self.assertTrue(oauth)

    def test_pass_withfullrequestobjectwithauthorisation(self):
        environ = create_environ()
        environ.update(
            HTTP_USER_AGENT='Mozilla/5.0 (Macintosh; U; Mac OS X 10.5; en-US; ) Firefox/3.1',
            HTTP_ACCEPT='text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            HTTP_ACCEPT_LANGUAGE='de-at,en-us;q=0.8,en;q=0.5',
            HTTP_ACCEPT_ENCODING='gzip,deflate',
            HTTP_ACCEPT_CHARSET='ISO-8859-1,utf-8;q=0.7,*;q=0.7',
            HTTP_IF_MODIFIED_SINCE='Fri, 20 Feb 2009 10:10:25 GMT',
            HTTP_IF_NONE_MATCH='"e51c9-1e5d-46356dc86c640"',
            HTTP_CACHE_CONTROL='max-age=0',
            HTTP_AUTHORIZATION='OAuth realm="Photos", oauth_consumer_key="dpf43f3p2l4k3l03", oauth_signature_method="HMAC-SHA1", '
        )
        request = Request(environ)
        oauth = is_oauth_request(request)
        self.assertTrue(oauth)

    def test_pass_withfullrequestobjectwithoutauthorisation(self):
        environ = create_environ()
        environ.update(
            HTTP_USER_AGENT='Mozilla/5.0 (Macintosh; U; Mac OS X 10.5; en-US; ) Firefox/3.1',
            HTTP_ACCEPT='text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            HTTP_ACCEPT_LANGUAGE='de-at,en-us;q=0.8,en;q=0.5',
            HTTP_ACCEPT_ENCODING='gzip,deflate',
            HTTP_ACCEPT_CHARSET='ISO-8859-1,utf-8;q=0.7,*;q=0.7',
            HTTP_IF_MODIFIED_SINCE='Fri, 20 Feb 2009 10:10:25 GMT',
            HTTP_IF_NONE_MATCH='"e51c9-1e5d-46356dc86c640"',
            HTTP_CACHE_CONTROL='max-age=0',
        )
        request = Request(environ)
        oauth = is_oauth_request(request)
        self.assertFalse(oauth)




class MockBuilder(dict):
    def __getattr__(self, attr):
        return self.get(attr, None)
    __setattr__= dict.__setitem__
    __delattr__= dict.__delitem__