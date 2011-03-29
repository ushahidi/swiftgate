from mongokit import ValidationError
from domain.utils import validate_api_wrapper_requesthandler
import unittest

class  Test_validate_api_wrapper_requesthandler(unittest.TestCase):
    def test_pass(self):
        validate_api_wrapper_requesthandler('test_fff')

    def test_fail_tooshort(self):
        with self.assertRaises(ValidationError):
            validate_api_wrapper_requesthandler('hi')

    def test_fail_toolong(self):
        with self.assertRaises(ValidationError):
            validate_api_wrapper_requesthandler('morethantenc kjkfjgkfjgklfdj glk jfgkl jfdklgj fdlkgj fdlharacters')

    def test_fail_nonewordchars(self):
        with self.assertRaises(ValidationError):
            validate_api_wrapper_requesthandler('hi ther')
        