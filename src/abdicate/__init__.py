from pydantic import parse_obj_as

from abdicate import model_1_0

_VERSIONS = {
    '1.0': model_1_0.Application,
}

def parse_object(object):
    version = object.get('version')
    if version not in _VERSIONS:
        raise ValueError('Version "{}" not supported, choice from: {}'.format(version, ', '.join(_VERSIONS.keys())))
    return parse_obj_as(_VERSIONS.get(version), object)
