from server.utils import map_path_to_api_wrapper_identifier
import unittest

class Map_path_to_api_wrapper_identifier_tests(unittest.TestCase):
    def test_pass_withunicodeparam(self):
        result = map_path_to_api_wrapper_identifier(u'/foo/bar')
        self.assertTrue(result == u'foo')

    def test_pass_withnoneunicodeparam(self):
        result = map_path_to_api_wrapper_identifier('/foo/bar')
        self.assertTrue(result == u'foo')

    def test_pass_withnone(self):
        result = map_path_to_api_wrapper_identifier(None)
        self.assertTrue(result == None)

    def test_pass_withmalformedurl(self):
        result = map_path_to_api_wrapper_identifier('/kdjskdjdsa.dasdljasdlkjowjdc/aasdasdodkadljeafjelsafd')
        self.assertTrue(result == 'kdjskdjdsa.dasdljasdlkjowjdc')

    def test_pass_withemptystring(self):
        result = map_path_to_api_wrapper_identifier('')
        self.assertTrue(result == None)

    def test_pass_withjustslash(self):
        result = map_path_to_api_wrapper_identifier('/')
        self.assertTrue(result == None)




