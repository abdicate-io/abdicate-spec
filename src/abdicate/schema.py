from pydantic import create_model, Field

from abdicate.model_1_1 import Interface, Service, ExBaseModel

from abdicate.deployment import DeploymentModel


from functools import wraps


def memoize(function):    
    memo = {}
        
    @wraps(function)
    def wrapper(name, interface):

        # add the new key to dict if it doesn't exist already  
        if name not in memo:
            memo[name] = function(interface)

        return memo[name]

    return wrapper


def create_model_interface(interface: Interface):
    fields = {}
    if interface.outputs:
        for property_name, property_type in getattr(interface.outputs, 'properties', {}).items():
            fields[property_name] = (property_type.__root__, ...)
    

    return create_model(interface.name, **fields)


def create_model_service(service: Service, deployment_model: DeploymentModel):
    create_model_interface2 = memoize(create_model_interface)
    
    fields = {'__base__': ExBaseModel}
    for resource in ['services', 'databases']:
        resource_fields = {'__base__': ExBaseModel}
        for n, ser in getattr(service.requires, resource, {}).items():
            interface_name = ser.interface.split('@', 1)[-1]
            s = create_model_interface2(interface_name, deployment_model.interfaces[interface_name])
            resource_fields[n] = (s, Field(..., title=n))
        if len(resource_fields) > 1:
            fields[resource.title()] = (create_model(resource.title(), **resource_fields), ...)

    return create_model(service.name, **fields)
