import unittest


from pydantic.error_wrappers import ValidationError
from abdicate import parse_object

class ParseTests(unittest.TestCase):
    def test_parse_databases(self):
        instance = {'version': '1.0', 'requires': {'databases': {'orm': {'alias': 'db'}}}}
        item = parse_object(instance)
        self.assertEqual(item.requires.databases.get('orm').alias, 'db')

    def test_parse_queues(self):
        instance = {'version': '1.0', 'requires': {'queues': {'send': {'io.abdicate.queues:functional_queue_name': {'alias': 'receiveQueue'}}}}}
        item = parse_object(instance)
        self.assertEqual(item.requires.queues.send.get('io.abdicate.queues:functional_queue_name').alias, 'receiveQueue')

if __name__ == '__main__':
    unittest.main()