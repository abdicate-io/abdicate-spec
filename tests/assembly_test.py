import unittest

from pathlib import Path

from ruamel.yaml import YAML
from ruamel.yaml.compat import StringIO

from abdicate.assembly import read_directory

import logging

log = logging.getLogger(__name__)

class AssemblyModelTests(unittest.TestCase):
    def test_parse_stafftracker(self):
        directory = Path("examples/stafftracker")
        item = read_directory(directory)

        yaml = YAML()
        stream = StringIO()
        yaml.dump(item.dict(), stream)
        log.warning(f'test_parse_stafftracker\n {stream.getvalue()}')
        #self.assertEqual(item, {})

if __name__ == '__main__':
    unittest.main()