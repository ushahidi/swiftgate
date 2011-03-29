from mongokit import ValidationError
from domain.utils import validate_generic_dispalyname
import unittest

class  Validate_generic_dispalyname_TestCase(unittest.TestCase):
    def test_pass(self):
        validate_generic_dispalyname('This is a valid display name 10')

    def test_fail_tooshort(self):
        with self.assertRaises(ValidationError):
            validate_generic_dispalyname('hi')

    def test_fail_toolong(self):
        with self.assertRaises(ValidationError):
            validate_generic_dispalyname('there are more that 50 characters in this sting, houest!!!!!!')

    def test_fail_invalidchars(self):
        with self.assertRaises(ValidationError):
            validate_generic_dispalyname('hi there $ %')
