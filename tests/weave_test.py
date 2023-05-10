import unittest

import yaml

from abdicate import parse_object


class ParseTests(unittest.TestCase):
    def test_parse_databases(self):
        instance = {'version': '1.0', 'requires': {'databases': {'orm': {'alias': 'db'}}}}
        item = parse_object(instance)
        self.assertEqual(item.requires.databases.get('orm').alias, 'db')

if __name__ == '__main__':
    unittest.main()