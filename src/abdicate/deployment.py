from pathlib import Path
from collections import defaultdict

from pydantic import BaseModel

from ruamel.yaml import YAML

from abdicate.model_1_1 import RootModel, Interface, InterfaceReference, Service, InterfaceWeaver, InterfaceProvisioner
from abdicate import parse_object


def get_parent_interface(interface: InterfaceReference):
    return interface.split('@', 1)[1]

class DeploymentModel(BaseModel):
    interfaces: dict[str, Interface]
    services: dict[str, Service]
    weavers: dict[str, InterfaceWeaver]
    provisioners: dict[str, InterfaceProvisioner]

    @classmethod
    def from_objects(cls, objects: list[RootModel]) -> "DeploymentModel":
        types = defaultdict(list)
        for k, v in map(lambda x: (type(x), x), objects):
            types[k].append((v.name, v))

        return cls(**{
            'interfaces': dict(types.get(Interface, [])),
            'services': dict(types.get(Service, [])),
            'weavers': dict(types.get(InterfaceWeaver, [])),
            'provisioners': dict(types.get(InterfaceProvisioner, [])),
            })

    def get_interface_weaver(self, interface: str) -> InterfaceWeaver:
        parent_interface = get_parent_interface(interface)
        for name, weaver in self.weavers.items():
            if parent_interface in weaver.interfaces:
                return weaver
    
    def get_interface_provisioner(self, interface: str) -> InterfaceProvisioner:
        parent_interface = get_parent_interface(interface)
        for name, provisioner in self.provisioners.items():
            if parent_interface in provisioner.interfaces:
                return provisioner


def read_directory(directory: Path):
    yaml=YAML(typ='safe')
    objects = []
    for path in directory.glob('*.yaml'):
        data = yaml.load_all(path)
        for d in data:
            if 'name' not in d:
                d['name'] = str(path.stem)
            objects.append(parse_object(d))

    return DeploymentModel.from_objects(objects)