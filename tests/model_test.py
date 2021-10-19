import unittest

from pydantic import parse_obj_as
from pydantic.error_wrappers import ValidationError
from abdicate.model_1_0 import Application

class ModelTests(unittest.TestCase):
    def test_application_allows_extenions(self):
        instance = {'version': '1.0', 'x-test': 'something'}
        item = parse_obj_as(Application, instance)
        self.assertEqual(item.x_test, 'something')

    def test_application_does_not_allows_unknown_properties(self):
        instance = {'version': '1.0', 'unknown': True}
        with self.assertRaises(ValidationError):
            item = parse_obj_as(Application, instance)

if __name__ == '__main__':
    unittest.main()