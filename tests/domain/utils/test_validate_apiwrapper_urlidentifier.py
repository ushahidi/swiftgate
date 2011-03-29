from mongokit import ValidationError
from domain.utils import validate_apiwrapper_urlidentifier
import unittest

class  Validate_apiwrapper_urlidentifier_TestCase(unittest.TestCase):
    def test_pass(self):
        validate_apiwrapper_urlidentifier('testfff')

    def test_fail_tooshort(self):
        with self.assertRaises(ValidationError):
            validate_apiwrapper_urlidentifier('hi')

    def test_fail_toolong(self):
        with self.assertRaises(ValidationError):
            validate_apiwrapper_urlidentifier('morethantencharacters')

    def test_fail_nonewordchars(self):
        with self.assertRaises(ValidationError):
            validate_apiwrapper_urlidentifier('hi ther')
        