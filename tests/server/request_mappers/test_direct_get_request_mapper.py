from werkzeug.wrappers import Request
from server.mappers import direct_get_request_mapper
import unittest

class Test_direct_get_request_mapper(unittest.TestCase):
    def test_passwithnoparams(self):
        api_endpoint = "http://test/"
        request = Request.from_values();
        api_request = direct_get_request_mapper(request, api_endpoint)
        self.assertEqual("http://test", api_request.get_full_url())

    def test_passwithoneparameter(self):
        api_endpoint = "http://test/"
        request = Request.from_values(query_string='text=I%20Love%20This');
        api_request = direct_get_request_mapper(request, api_endpoint)
        self.assertEqual("http://test?text=I%20Love%20This", api_request.get_full_url())

    def test_passwithtwoparameter(self):
        api_endpoint = "http://test/"
        request = Request.from_values(query_string='text=I%20Love%20This&something=something_else');
        api_request = direct_get_request_mapper(request, api_endpoint)
        self.assertEqual("http://test?text=I%20Love%20This&something=something_else", api_request.get_full_url())

    def test_passandencodeqstring(self):
        api_endpoint = "http://test/"
        request = Request.from_values(query_string='text=I Love This');
        api_request = direct_get_request_mapper(request, api_endpoint)
        self.assertEqual("http://test?text=I%20Love%20This", api_request.get_full_url())


