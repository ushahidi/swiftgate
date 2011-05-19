from mongokit import ValidationError
from domain.utils import validate_apiwrapper_urlidentifier
import unittest

class  Validate_apiwrapper_urlidentifier_TestCase(unittest.TestCase):
    def test_pass(self):
        validate_apiwrapper_urlidentifier('testfff/v1.0')

    def test_fail_tooshort(self):
        with self.assertRaises(ValidationError):
            validate_apiwrapper_urlidentifier('hi')

    def test_fail_toolong(self):
        with self.assertRaises(ValidationError):
            validate_apiwrapper_urlidentifier('morethantencharacters')

    def test_fail_noneacceptabelchars(self):
        with self.assertRaises(ValidationError):
            validate_apiwrapper_urlidentifier('hi ther')

    def test_fail_noversion(self):
        with self.assertRaises(ValidationError):
            validate_apiwrapper_urlidentifier('tagger')

    def test_fail_notalllowercase(self):
        with self.assertRaises(ValidationError):
            validate_apiwrapper_urlidentifier('tagger/V1.0')
        