from pydantic import create_model, Field

from abdicate.model_1_1 import ExBaseModel
from abdicate.assembly import AssemblyModel, get_parent_interface
from abdicate.weave import WeaveModel
from abdicate.schema import create_model_interface, memoize

from typing import Union

class AutoWeave(ExBaseModel):
    ...


class AutoProvision(ExBaseModel):
    ...

def _create_weable_model(id: str, items: dict, assembly_model: AssemblyModel, create_model_interface2, auto, description):
    weavables = {'__base__': ExBaseModel}
    for interfaceReference, weavable in items:
        interface_name = get_parent_interface(interfaceReference)
        interface_model = create_model_interface2(interface_name, assembly_model.interfaces[interface_name])

        services = {'__base__': ExBaseModel}
        for s in weavable.services:
            types = Union[auto, interface_model] if auto else interface_model
            services[s.service] = (types, Field(..., title=s.service))
        services_model = create_model(interfaceReference+'-services', **services)

        weavables[interfaceReference] = (services_model, Field(..., title=interfaceReference, description=description(weavable)))
    weavables_model = create_model(id, **weavables)
    return weavables_model


def create_configuration_model(assembly_model: AssemblyModel, weave_model: WeaveModel):
    create_model_interface2 = memoize(create_model_interface)

    fields = {'__base__': ExBaseModel}
    #fields[n] = (s, Field(..., title=n, description='dd'))

    weavables_model = _create_weable_model('weavables', weave_model.weavable.items(), assembly_model, create_model_interface2, AutoWeave, lambda x: 'Provided by '+x.providers[0].service)
    provisionable_model = _create_weable_model('provisionables', weave_model.provisionable.items(), assembly_model, create_model_interface2, AutoProvision, lambda x: 'Provsioned by '+x.provisioner.name)
    required_model = _create_weable_model('required', weave_model.required.items(), assembly_model, create_model_interface2, None, lambda x: 'Required')
    
    fields['weavables'] = (weavables_model, Field(..., title='weavables'))
    fields['provisionables'] = (provisionable_model, Field(..., title='provisionables'))
    fields['required'] = (required_model, Field(..., title='required'))

    return create_model('Configuration', **fields)


if __name__ == '__main__':
    from pathlib import Path
    from ruamel.yaml import YAML
    from abdicate.assembly import read_directory

    directory = Path(r"./examples/stafftracker")
    yaml=YAML(typ='safe')
    model = read_directory(directory)
    woven = WeaveModel.from_model(model)
    Path('temp/woven.json').write_text(woven.json(indent=4))

    configuration_model = create_configuration_model(model, woven)

    Path('temp/schema-ui.json').write_text(configuration_model.schema_json(indent=4))