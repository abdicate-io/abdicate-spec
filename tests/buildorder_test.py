import unittest

from pathlib import Path
from ruamel.yaml import YAML

from abdicate.assembly import read_directory

from abdicate.weave import WeaveModel, Reference, InterfaceProvisioner
from abdicate.buildorder import BuildOrderModel


class BuildOrderTests(unittest.TestCase):
    def setUp(self):
        directory = Path(r"./examples/stafftracker")
        yaml=YAML(typ='safe')
        model = read_directory(directory)
        self.woven = WeaveModel.from_model(model)
        self.model = BuildOrderModel.from_model(self.woven)

        __import__('sys').modules['unittest.util']._MAX_LENGTH = 999999999

    def test_order(self):
        self.assertEqual(self.model.services, 
                         ['zipcodes-requires-databases-orm@mysql:5', 
                          'rooms-requires-databases-database@mysql:5', 
                          'staff-requires-databases-db@mysql:5', 
                          'frontend@cluster',
                          'shared-property@https-url', 
                          'geoservice-requires-properties-geo-url@https-url',
                          'rooms', 'staff', 'zipcodes', 'geo', 'stafftracker'])

if __name__ == '__main__':
    unittest.main()