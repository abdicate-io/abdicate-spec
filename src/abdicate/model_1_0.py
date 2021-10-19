import re
from enum import Enum
from typing import Dict, Optional, List
from pydantic import BaseModel, constr, Extra, root_validator, Field

DNSNAME_REGEX = r'^(?![0-9]+$)(?!-)[a-zA-Z0-9-]{,63}(?<!-)$'
ARTIFACT_REGEX = r'^([a-z\-_\.]+)(:([a-z\-_]+))?$'
IMAGE_TAG_REGEX = r'^(?:(?=[^:\/]{4,253})(?!-)[a-zA-Z0-9-]{1,63}(?<!-)(?:\.(?!-)[a-zA-Z0-9-]{1,63}(?<!-))*(?::[0-9]{1,5})?/)?((?![._-])(?:[a-z0-9._-]*)(?<![._-])(?:/(?![._-])[a-z0-9._-]*(?<![._-]))*)((?::(?![.-])[a-zA-Z0-9_.-]{1,128})|@sha256:[a-z0-9]+)?$'


class MountPermissionEnum(str, Enum):
    read = 'read'
    write = 'write'
    read_write = 'read_write'


class DSPermissionEnum(str, Enum):
    read = 'read'
    read_write = 'read_write'


class ExBaseModel(BaseModel):
    class Config:
        extra = Extra.allow
        schema_extra = {
            'patternProperties': {'^x-': {}},
        }
    @root_validator
    def check_extra_fields(cls, values):
        """Make sure extra fields are only valid fields matching regex"""
        pattern_regex = r'^x-'

        for k, v in list(values.items()):
            if k in cls.__fields__:
                continue

            assert re.match(pattern_regex, k), 'extra field "{}" not allowed (custom properties can be set with prefix x-)'.format(k)
            values[re.sub(pattern_regex, 'x_', k)] = values.pop(k)

        return values


class Resource(ExBaseModel):
    alias: Optional[str] = None


class Functional(ExBaseModel):
    domains: Optional[List[str]] = Field(description='List of functional domains this application belongs to.')
    components: Optional[List[str]] = Field(description='List of functional components this application belongs to.')


class Database(Resource):
    """
    A Database that will be utilized by the application
    These are databases for which the schema is managed by the application.
    """
    interface: Optional[str] = None


class DataStore(Resource):
    """
    A dataStore that will be utilized by the application
    These are databases for which the application isn't the owner of the schemas.
    """
    permission: DSPermissionEnum = DSPermissionEnum.read


class Service(Resource):
    """
    A service that will be utilized by the application
    """
    pass


class Queue(Resource):
    """
    A queue that will be utilized by the application
    """
    pass


class Queues(Resource):
    receive: Optional[Dict[constr(regex=ARTIFACT_REGEX), Queue]] = Field(description='List queues with incoming messages')
    send: Optional[Dict[constr(regex=ARTIFACT_REGEX), Queue]] = Field(description='List queues with outgoing messages')


class Property(Resource):
    """
    A property that will be utilized by the application
    """
    pass


class Mount(Resource):
    """
    A file or directory that will be utilized by the application
    """
    permission: MountPermissionEnum = MountPermissionEnum.read


class Requires(ExBaseModel):
    databases: Optional[Dict[constr(regex=ARTIFACT_REGEX), Database]]
    datastores: Optional[Dict[constr(regex=ARTIFACT_REGEX), DataStore]]
    services: Optional[Dict[constr(regex=ARTIFACT_REGEX), Service]]
    queues: Optional[Queues]
    properties: Optional[Dict[constr(regex=ARTIFACT_REGEX), Property]]
    mounts: Optional[Dict[constr(regex=ARTIFACT_REGEX), Mount]]
    

class Provided(ExBaseModel):
    """
    A provided interface that will be exposed by the application
    """
    interface: Optional[str] = None


class Application(ExBaseModel): 
    """
    Dependencies and description of the application.
    """
    version: str
    
    baseImage: Optional[constr(regex=IMAGE_TAG_REGEX)]
    friendlyName: Optional[constr(regex=DNSNAME_REGEX)]
    functional: Optional[Functional]

    requires: Optional[Requires]
    provides: Optional[Dict[constr(regex=ARTIFACT_REGEX), Provided]]