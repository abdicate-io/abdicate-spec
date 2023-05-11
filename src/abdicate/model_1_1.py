import re
from enum import Enum
from typing import Dict, Optional, List
from pydantic import BaseModel, constr, Extra, root_validator, Field

DNSNAME_REGEX = r'^(?![0-9]+$)(?!-)[a-zA-Z0-9-]{,63}(?<!-)$'
ARTIFACT_REGEX = r'^([a-z\-_\.]+)(:([a-z\-_]+))?$'
IMAGE_TAG_REGEX = r'^(?:(?=[^:\/]{4,253})(?!-)[a-zA-Z0-9-]{1,63}(?<!-)(?:\.(?!-)[a-zA-Z0-9-]{1,63}(?<!-))*(?::[0-9]{1,5})?/)?((?![._-])(?:[a-z0-9._-]*)(?<![._-])(?:/(?![._-])[a-z0-9._-]*(?<![._-]))*)((?::(?![.-])[a-zA-Z0-9_.-]{1,128})|@sha256:[a-z0-9]+)?$'

InterfaceReference = str

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


class ResourceReference(ExBaseModel):
    alias: Optional[str] = None
    interface: InterfaceReference


class Functional(ExBaseModel):
    domains: Optional[List[str]] = Field(description='List of functional domains this application belongs to.')
    components: Optional[List[str]] = Field(description='List of functional components this application belongs to.')


class Database(ResourceReference):
    """
    A Database that will be utilized by the application
    These are databases for which the schema is managed by the application.
    """
    pass


class DataStore(ResourceReference):
    """
    A dataStore that will be utilized by the application
    These are databases for which the application isn't the owner of the schemas.
    """
    permission: DSPermissionEnum = DSPermissionEnum.read


class ServiceReference(ResourceReference):
    """
    A service that will be utilized by the application
    """
    pass


class Queue(ResourceReference):
    """
    A queue that will be utilized by the application
    """
    pass


class Queues(ExBaseModel):
    receive: Optional[Dict[constr(regex=ARTIFACT_REGEX), Queue]] = Field(default={}, description='List queues with incoming messages')
    send: Optional[Dict[constr(regex=ARTIFACT_REGEX), Queue]] = Field(default={}, description='List queues with outgoing messages')


class Property(ResourceReference):
    """
    A property that will be utilized by the application
    """
    pass


class Mount(ResourceReference):
    """
    A file or directory that will be utilized by the application
    """
    permission: MountPermissionEnum = MountPermissionEnum.read


class Requires(ExBaseModel):
    databases: Optional[Dict[constr(regex=ARTIFACT_REGEX), Database]] = {}
    datastores: Optional[Dict[constr(regex=ARTIFACT_REGEX), DataStore]] = {}
    services: Optional[Dict[constr(regex=ARTIFACT_REGEX), ServiceReference]] = {}
    queues: Optional[Queues] = Field(default=Queues())
    properties: Optional[Dict[constr(regex=ARTIFACT_REGEX), Property]] = {}
    mounts: Optional[Dict[constr(regex=ARTIFACT_REGEX), Mount]] = {}
    

class Provided(ExBaseModel):
    """
    A provided interface that will be exposed by the application
    """
    interface: Optional[str] = None


from typing import Literal, Union

class RootModel(ExBaseModel):
    version: str = Field('1.1', repr=False)

class Service(RootModel):
    """
    Dependencies and description of the service.
    """
    kind: Literal['Service'] = Field(default='Service', repr=False)
    
    name: str
    
    baseImage: Optional[constr(regex=IMAGE_TAG_REGEX)]
    friendlyName: Optional[constr(regex=DNSNAME_REGEX)]
    functional: Optional[Functional]

    requires: Optional[Requires]
    provides: Optional[Dict[constr(regex=ARTIFACT_REGEX), Provided]]


INTERFACE_REGEX = r'^([a-z])([a-z0-9\-_]+)(:[0-9\.]+)?$'

class PropertyValidation(ExBaseModel):
    __root__: str

    def __getattr__(self, name):
        return getattr(self.__root__, name)

class Outputs(ExBaseModel):
    properties: Optional[Dict[constr(regex=ARTIFACT_REGEX), PropertyValidation]] = {}

class Interface(RootModel):
    kind: Literal['Interface'] = Field(default='Interface', repr=False)
    name: constr(regex=INTERFACE_REGEX)
    outputs: Optional[Outputs]


class InterfaceWeaver(RootModel):
    kind: Literal['InterfaceWeaver'] = Field(default='InterfaceWeaver', repr=False)
    name: str
    implementation: str
    interfaces: list[constr(regex=INTERFACE_REGEX)]

class InterfaceProvisioner(RootModel):
    kind: Literal['InterfaceProvisioner'] = Field(default='InterfaceProvisioner', repr=False)
    name: str
    implementation: str
    interfaces: list[constr(regex=INTERFACE_REGEX)]

class Root(ExBaseModel): 
    __root__: Union[Service, Interface, InterfaceWeaver, InterfaceProvisioner] = Field(..., discriminator='kind')

    def __getattr__(self, name):
        return getattr(self.__root__, name)