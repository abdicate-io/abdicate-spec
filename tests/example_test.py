import unittest

from pathlib import Path

from ruamel.yaml import YAML

from pydantic.error_wrappers import ValidationError
from abdicate import parse_object

class ExampleTests(unittest.TestCase):
    def test_parse_stafftracker(self):
        yaml=YAML(typ='safe')
        data = yaml.load(Path('examples/stafftracker/stafftracker.yaml'))
        item = parse_object(data)
        print(item)
        self.assertEqual(item.requires.queues.receive, {})
        self.assertEqual(item.requires.databases, {})

    def test_parse_interfaces(self):
        yaml=YAML(typ='safe')
        data = yaml.load_all(Path('examples/stafftracker/interfaces.yaml'))
        items = [parse_object(d) for d in data]
        print(items)
        self.assertEqual(items[0].name, 'mysql:5')

if __name__ == '__main__':
    unittest.main()