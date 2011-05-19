from mongokit import ValidationError
from domain.utils import validate_generic_description
import unittest

class  Validate_generic_dispalyname_TestCase(unittest.TestCase):
    def test_pass(self):
        validate_generic_description('This is a valid descripton 10')

    def test_fail_tooshort(self):
        with self.assertRaises(ValidationError):
            validate_generic_description('hi')

    def test_fail_toolong(self):
        with self.assertRaises(ValidationError):
            validate_generic_description(
                'there are more that 50 characters in this sting, houest!!!!!!' +
                'there are more that 50 characters in this sting, houest!!!!!!' +
                'there are more that 50 characters in this sting, houest!!!!!!' +
                'there are more that 50 characters in this sting, houest!!!!!!' +
                'there are more that 50 characters in this sting, houest!!!!!!' +
                'there are more that 50 characters in this sting, houest!!!!!!' +
                'there are more that 50 characters in this sting, houest!!!!!!' +
                'there are more that 50 characters in this sting, houest!!!!!!' +
                'there are more that 50 characters in this sting, houest!!!!!!' +
                'there are more that 50 characters in this sting, houest!!!!!!' +
                'there are more that 50 characters in this sting, houest!!!!!!' +
                'there are more that 50 characters in this sting, houest!!!!!!'
            )

    def test_fail_invalidchars(self):
        with self.assertRaises(ValidationError):
            validate_generic_description('hi there $ %')
