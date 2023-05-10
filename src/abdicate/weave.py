from pathlib import Path
from glob import glob

from ruamel.yaml import YAML
from abdicate import parse_object

from abdicate.model_1_1 import Provided, Resource, Module, Interface, ExBaseModel, InterfaceReference, InterfaceWeaver, InterfaceProvisioner

from pydantic import BaseModel, create_model

from collections import defaultdict

import pprint
pp = pprint.PrettyPrinter(depth=4)

from abdicate.deployment import DeploymentModel, read_directory

class Weavable(BaseModel):
    weaver: InterfaceWeaver
    services: list[str]

class Provisionable(BaseModel):
    provisioner: InterfaceProvisioner
    services: list[str]

class WeaveModel(BaseModel):
    weavable: dict[InterfaceReference, Weavable]
    provisionable: dict[InterfaceReference, Provisionable]
    required: dict[InterfaceReference, list[Module]]

    @classmethod
    def from_model(cls, deployment_model: DeploymentModel) -> "WeaveModel":
        # Loop over all modules and get specific interface refs
        print('-'*40)
        required=defaultdict(list)
        provided=defaultdict(list)
        for module in deployment_model.services.values():
            resources = get_resources_for_module(module)
            for resource, parents in resources:
                to_add = required if not type(resource) == Provided else provided
                to_add[fully_qualified_interface_name(module, resource, parents)].append(module.friendlyName)

        weavable={}
        provisionable=defaultdict(list)
        for interface, modules in required.items():
            if interface in provided  and deployment_model.get_interface_weaver(interface):
                weavable[interface] = Weavable(weaver=deployment_model.get_interface_weaver(interface), services=modules)
            elif interface not in provided  and deployment_model.get_interface_provisioner(interface):
                provisionable[interface] = Provisionable(provisioner=deployment_model.get_interface_provisioner(interface), services=modules)
            

        pp.pprint(required)
        print('-'*40)
        pp.pprint(provided)
        print('-'*40)
        pp.pprint(weavable)
        print('-'*40)
        pp.pprint(provisionable)
        print('-'*40)
        pp.pprint(deployment_model.provisioners)

        return None


def get_resources_for_module(d, parents=[]):
    #print('_keyus', d.__class__.__name__,  list(map(lambda x: x.__name__, type.mro(type(d)))))
    derrived =  list(map(lambda x: x, type.mro(type(d))))
    if Resource in derrived or Provided in derrived:
        #print('resource', type(d), d, parents)
        yield d, parents
    else:
        for a, b in d.__fields__.items():
            value = getattr(d, a)
            #print('checking', a, isinstance(value, ExBaseModel), type(value))
            if isinstance(value, ExBaseModel):
                yield from get_resources_for_module(value, [*parents, d, a])
            if isinstance(value, dict):
                for k,v in value.items():
                    yield from get_resources_for_module(v, [*parents, a, k])
            if isinstance(value, list):
                for i in value:
                    yield from get_resources_for_module(i, [*parents, a, i])


def is_interface_specific(interface_name: InterfaceReference):
    return '@' in interface_name

def fully_qualified_interface_name(module, resource, parents):
    if is_interface_specific(resource.interface):
        return resource.interface
    else:
        return module.friendlyName+'-'+('-'.join(parents[1:]))+'@'+resource.interface


if __name__ == '__main__':
    directory = Path(r"C:/Local_Data/G000737/checkouts/aws/abdicate-spec/examples/stafftracker")

    yaml=YAML(typ='safe')

    model = read_directory(directory)

    woven = WeaveModel.from_model(model)
