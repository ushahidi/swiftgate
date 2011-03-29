from domain.utils import get_api_method_wrapper_by_url_pattern
from urllib import quote
import unittest

class Test_get_api_methodsper_by_url_pattern(unittest.TestCase):
    def test_pass_withbasicpattern(self):
        path = "/tagger/tag"
        api_method_wrapper = MockBuilder({"url_pattern":"/tag$", "mapper":1})
        api_wrapper = MockBuilder({"url_identifier":"tagger","api_methods":[api_method_wrapper]})
        element = get_api_method_wrapper_by_url_pattern(path, api_wrapper)
        self.assertEqual(1, element.mapper)

    def test_pass_withcomplexpattern(self):
        path = "/tagger/tag?text=" + quote("I am trying to test that this can be identifed by the regex")
        api_method_wrapper = MockBuilder({"url_pattern":"/tag\?text=[a-zA-Z0-9%]+$", "mapper":1})
        api_wrapper = MockBuilder({"url_identifier":"tagger","api_methods":[api_method_wrapper]})
        element = get_api_method_wrapper_by_url_pattern(path, api_wrapper)
        self.assertEqual(1, element.mapper)

class MockBuilder(dict):
    def __getattr__(self, attr):
        return self.get(attr, None)
    __setattr__= dict.__setitem__
    __delattr__= dict.__delitem__