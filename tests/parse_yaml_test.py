import unittest

from pathlib import Path
from ruamel.yaml import YAML

from pydantic.error_wrappers import ValidationError
from abdicate import parse_object

class ParseYamlTests(unittest.TestCase):
    def test_parse_petstore(self):
        petstore = Path(r"./examples/petstore.yaml")
        yaml=YAML(typ='safe')
        instance = yaml.load(petstore)
        item = parse_object(instance)
        self.assertEqual(item.requires.databases.get('orm').alias, 'db')

if __name__ == '__main__':
    unittest.main()