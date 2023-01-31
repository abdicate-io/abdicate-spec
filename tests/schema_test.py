import unittest

from pathlib import Path

from abdicate.deployment import read_directory

from abdicate.schema import create_model_interface, create_model_service

import logging

log = logging.getLogger(__name__)

class SchemaTests(unittest.TestCase):
    def test_interface(self):
        directory = Path("examples/stafftracker")
        item = read_directory(directory)

        mysql = item.interfaces['mysql:5']

        self.assertEqual(item.interfaces['mysql:5'].name, 'mysql:5')

        self.maxDiff = None
        __import__('sys').modules['unittest.util']._MAX_LENGTH = 999999999
        self.assertEqual(create_model_interface(mysql).schema(), {
            'properties': {
                'database': {'title': 'Database', 'type': 'string'},
                 'host': {'title': 'Host', 'type': 'string'},
                 'password': {'title': 'Password', 'type': 'string'},
                 'port': {'title': 'Port', 'type': 'integer'},
                 'username': {'title': 'Username', 'type': 'string'}},
            'required': ['host', 'port', 'database', 'username', 'password'],
            'title': 'mysql:5',
            'type': 'object'})

    def test_service(self):
        directory = Path("examples/stafftracker")
        item = read_directory(directory)

        stafftracker = item.services['rooms']

        service_model = create_model_service(stafftracker, item)

        Path('temp/schema-ui.json').write_text(service_model.schema_json(indent=4))

        self.maxDiff = None
        __import__('sys').modules['unittest.util']._MAX_LENGTH = 999999999
        self.assertEqual(service_model.schema(), {})

if __name__ == '__main__':
    unittest.main()