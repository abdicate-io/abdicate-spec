from pydantic import create_model, Field

from abdicate.model_1_1 import ExBaseModel
from abdicate.assembly import AssemblyModel
from abdicate.weave import WeaveModel
from abdicate.schema import create_model_interface, memoize

from typing import Union

class AutoWeave(ExBaseModel):
    ...

def create_configuration_model(assembly_model: AssemblyModel, weave_model: WeaveModel):
    create_model_interface2 = memoize(create_model_interface)

    fields = {'__base__': ExBaseModel}
    
    interface_name = 'web-service'
    n = 'test'

    i = create_model_interface2(interface_name, assembly_model.interfaces[interface_name])
    #fields[n] = (s, Field(..., title=n, description='dd'))


    weavables = {'__base__': ExBaseModel}
    for interfaceReference, weavable in weave_model.weavable.items():
        services = {'__base__': ExBaseModel}
        for s in weavable.services:
            services[s.service] = (Union[AutoWeave, i], Field(..., title=s.service))
        print('services', services)
        services_model = create_model(interfaceReference+'-services', **services)

        weavables[interfaceReference] = (services_model, Field(..., title=interfaceReference, description='Provided by '+weavable.providers[0].service))
    weavables_model = create_model('weavables', **weavables)
    fields['weavables'] = (weavables_model, Field(..., title='weavables'))

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