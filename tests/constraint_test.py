import unittest

import re

from pydantic import parse_obj_as
from pydantic.error_wrappers import ValidationError
from abdicate.model_1_0 import ARTIFACT_REGEX, DNSNAME_REGEX, IMAGE_TAG_REGEX

class ConstraintTests(unittest.TestCase):
    def test_valid_artifact_ids(self):
        for i, string in enumerate(['com.org.package:artifact', 'artifact', 'test:test', 'test_test', 'test-test']):
            with self.subTest(i=i, msg=string):
                self.assertTrue(re.match(ARTIFACT_REGEX, string), '{} does not match {}'.format(string, ARTIFACT_REGEX))


    def test_invalid_artifact_ids(self):
        for i, string in enumerate(['com.org.package/artifact', 'Artifact', 'test@test']):
            with self.subTest(i=i, msg=string):
                self.assertFalse(re.match(ARTIFACT_REGEX, string), '{} does match {}'.format(string, ARTIFACT_REGEX))


    def test_dnsnames(self):
        tests = [
            ('01010', False),
            ('abc', True),
            ('A0c', True),
            ('A0c-', False),
            ('-A0c', False),
            ('A-0c', True),
            ('o123456701234567012345670123456701234567012345670123456701234567', False),
            ('o12345670123456701234567012345670123456701234567012345670123456', True),
            ('', True),
            ('a', True),
            ('0--0', True),
        ]

        for i, (string, expected) in enumerate(tests):
            with self.subTest(i=i, msg=string):
                self.assertEquals(re.match(DNSNAME_REGEX, string) is not None, expected, '{} {} match {}'.format(string, ("doesn't" if expected else "does"), DNSNAME_REGEX))


    def test_imagetags(self):
        tests = [
            ('FOO', False),
            ('myregistryhost:5000/fedora/httpd:version1.0', True),
            ('fedora/httpd:version1.0.test', True),
            ('fedora/httpd:version1.0', True),
            ('rabbit:3', True),
            ('rabbit', True),
            ('registry/rabbit:3', True),
            ('registry/rabbit', True),
            ('rabbit@sha256:3235326357dfb65f1781dbc4df3b834546d8bf914e82cce58e6e6b6', True),
            ('registry/rabbit@sha256:3235326357dfb65f1781dbc4df3b834546d8bf914e82cce58e6e6b6', True),
            ('rabbit@sha256:3235326357dfb65f1781dbc4df3b834546d8bf914e82cce58e.6e6b6', False),
        ]

        for i, (string, expected) in enumerate(tests):
            with self.subTest(i=i, msg=string):
                self.assertEquals(re.match(IMAGE_TAG_REGEX, string) is not None, expected, '{} {} match {}'.format(string, ("doesn't" if expected else "does"), IMAGE_TAG_REGEX))


if __name__ == '__main__':
    unittest.main()