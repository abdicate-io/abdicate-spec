from pydantic import parse_obj_as

from abdicate import model_1_0, model_1_1

_VERSIONS = {
    '1.0': model_1_0.Application,
    '1.1': model_1_1.Root,
}

def parse_object(object):
    version = object.get('version')
    if version not in _VERSIONS:
        raise ValueError('Version "{}" not supported, choice from: {}'.format(version, ', '.join(_VERSIONS.keys())))
    obj = parse_obj_as(_VERSIONS.get(version), object)
    if hasattr(obj, '__root__'):
        return obj.__root__
    return obj
