import unittest

from pathlib import Path
from ruamel.yaml import YAML

from abdicate.deployment import read_directory

from abdicate.weave import WeaveModel, Reference, InterfaceProvisioner


class WeaveTests(unittest.TestCase):
    def setUp(self):
        directory = Path(r"./examples/stafftracker")
        yaml=YAML(typ='safe')
        model = read_directory(directory)
        self.woven = WeaveModel.from_model(model)
        __import__('sys').modules['unittest.util']._MAX_LENGTH = 999999999

    def test_weavable_providers_are_set(self):
        self.assertEqual(self.woven.weavable['zipcodes@web-service'].providers[0].service, 'zipcodes')

    def test_weavable_weaver_is_set(self):
        self.assertEqual(self.woven.weavable['zipcodes@web-service'].weaver.name, 'web-service')

    def test_weavable_services_are_set(self):
        self.assertEqual(self.woven.weavable['zipcodes@web-service'].services, 
                         [Reference(service='geo', path=['requires', 'services', 'zipcodes']), 
                          Reference(service='stafftracker', path=['requires', 'services', 'zipcodes'])])

    def test_provisionable_provisioner_is_set(self):
        self.assertEqual(self.woven.provisionable['zipcodes-requires-databases-orm@mysql:5'].provisioner, 
                         InterfaceProvisioner(name='mysql', implementation='abdicate.pulumi.rds', interfaces=['mysql:5']))
        
    def test_provisionable_services_are_set(self):
        self.assertEqual(self.woven.provisionable['zipcodes-requires-databases-orm@mysql:5'].services, 
                         [Reference(service='zipcodes', path=['requires', 'databases', 'orm'])])

    def test_required_are_set(self):
        self.assertEqual(self.woven.required['geoservice-requires-properties-geo-url@https-url'], 
                         [Reference(service='geo', path=['requires', 'properties', 'geo-url'])])

if __name__ == '__main__':
    unittest.main()