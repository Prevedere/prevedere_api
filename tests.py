import unittest
import prevedere
from prevedere.api import ApiKeyError
from requests.exceptions import HTTPError
import requests

class TestApiMethods(unittest.TestCase):

    def test_ini(self):
        p = prevedere.Api()
        self.assertIsNotNone(p)
    
    def test_bad_indicator_id(self):
        p = prevedere.Api()
        self.assertRaises(HTTPError, p.indicator_series('FRED', 'bad_indicator_id'))

    def test_bad_provider_id(self):
        p = prevedere.Api()
        self.assertRaises(HTTPError,p.indicator_series('BADID', 'SP500'))
    
    def test_bad_workbench_id(self):
        p = prevedere.Api()
        self.assertRaises(HTTPError, p.workbench('bad_workbench_id'))
    
    def test_bad_model_id(self):
        p = prevedere.Api()
        self.assertRaises(HTTPError, p.forecast(model_id='bad_model_id'))
    
    def test_badly_formed_api_key(self):
        with self.assertRaises(ApiKeyError) as e:
            prevedere.Api('badly_formed_api_key')

if __name__ == '__main__':
    unittest.main()