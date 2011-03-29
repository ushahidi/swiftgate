from server.utils import create_standard_json_response
import unittest
import simplejson as json

class Test_create_standard_json_response(unittest.TestCase):
    def test_pass_withsimplejson(self):
        result = create_standard_json_response('api', 'api_method', 'sucess', 'wow', False)
        data = json.loads(result)
        self.assertEqual(data['service'], 'api')
        self.assertEqual(data['method'], 'api_method')
        self.assertEqual(data['status'], 'sucess')
        self.assertEqual(data['response'], 'wow')

    def test_pass_withcomplexjson(self):
        response = '{"here":"is", "something":["once",  "twice"]}'
        result = create_standard_json_response('api', 'api_method', 'sucess', response)
        print result
        data = json.loads(result)
        print result
        self.assertEqual(data['service'], 'api')
        self.assertEqual(data['method'], 'api_method')
        self.assertEqual(data['status'], 'sucess')
        self.assertEqual(data['response']['here'], 'is')
        self.assertEqual(data['response']['something'][0], 'once')
        self.assertEqual(data['response']['something'][1], 'twice')



