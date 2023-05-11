from abdicate.model_1_1 import Provided, Resource, ExBaseModel, InterfaceReference, InterfaceWeaver, InterfaceProvisioner

from pydantic import BaseModel

from collections import defaultdict

from abdicate.deployment import DeploymentModel


class Reference(BaseModel):
    service: str
    path: list[str]


class Weavable(BaseModel):
    providers: list[Reference]
    weaver: InterfaceWeaver
    services: list[Reference]


class Provisionable(BaseModel):
    provisioner: InterfaceProvisioner
    services: list[Reference]


class WeaveModel(BaseModel):
    weavable: dict[InterfaceReference, Weavable]
    provisionable: dict[InterfaceReference, Provisionable]
    required: dict[InterfaceReference, list[Reference]]

    @classmethod
    def from_model(cls, deployment_model: DeploymentModel) -> "WeaveModel":
        required=defaultdict(list)
        provided=defaultdict(list)
        for module in deployment_model.services.values():
            resources = get_resources_for_module(module)
            for resource, parents in resources:
                to_add = required if not type(resource) == Provided else provided
                to_add[fully_qualified_interface_name(module, resource, parents)].append((module, parents[1:]))

        weavable={}
        provisionable={}
        manual={}
        for interface, modules in required.items():
            references = list(map(lambda x: Reference(service=x[0].name, path=x[1]), modules))
            if interface in provided  and deployment_model.get_interface_weaver(interface):
                provider_references = list(map(lambda x: Reference(service=x[0].name, path=x[1]), provided[interface]))
                weavable[interface] = Weavable(providers=provider_references, weaver=deployment_model.get_interface_weaver(interface), services=references)
            elif interface not in provided  and deployment_model.get_interface_provisioner(interface):
                provisionable[interface] = Provisionable(provisioner=deployment_model.get_interface_provisioner(interface), services=references)
            else:
                manual[interface] = references

        return cls(**{
            'weavable': weavable,
            'provisionable': provisionable,
            'required': manual,
            })


def get_resources_for_module(d, parents=[]):
    derrived =  list(map(lambda x: x, type.mro(type(d))))
    if Resource in derrived or Provided in derrived:
        yield d, parents
    else:
        for a, b in d.__fields__.items():
            value = getattr(d, a)
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