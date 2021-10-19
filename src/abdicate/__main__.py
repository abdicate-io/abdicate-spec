import argparse

from abdicate import _VERSIONS

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Produce a json schema.')
    parser.add_argument('--version', help='version of the schema.', required=True, choices=_VERSIONS.keys())

    args = parser.parse_args()
    print(_VERSIONS.get(args.version).schema_json(indent=2))