Concepts
========


Service Model
------------

:py:class:`abdicate.model_1_1.Service`

Resource references and interfaces

:py:class:`abdicate.model_1_1.ResourceReference`

Resource reference
------------------

When specifying a resource reference's interface can have two formats:
  * ``<identifier>@<interface>`` fully qualified name, in case you want to point multiple services to this single resource.
  * ``<interface>`` in case this resource is unique to this service (it will be expanded as ``<service_name>-<resource_type>-<resource_name>@<interface>`` internally)

:py:class:`abdicate.model_1_1.InterfaceReference`

Interfaces
----------

Interfaces are user defined models with properties and optional validation.

Say a simple interface for pointing to a webservice could look like

.. code-block:: yaml

    version: "1.1"
    kind: Interface
    name: web-service
    properties:
        url: str 

Or more complex for a database connection for example:

.. code-block:: yaml

    version: "1.1"
    kind: Interface
    name: mysql:5
    properties:
        host: str 
        port: int 
        database: Optional[str]
        username: str 
        password: str 

:py:class:`abdicate.model_1_1.Interface`


Deployment Model
----------------

All Service and Interface definitions form the Assembly Model.

:py:class:`abdicate.deployment.DeploymentModel`


Weaving
-------

If a resource reference with a certain interface is required and it also provided in the same AssemblyModel as is an InterfaceWeaver that supports that interface, 
then the required and provided can be automatically linked together, requiring no further configuration.

If a resource reference with a certain interface is required and an InterfaceProvisioner that supports that interface is present in the AssemblyModel,
then a resource providing that interface can automatically be added, requiring no further configuration.

Otherwise the inferface has to be manually configured for that resource.

:py:class:`abdicate.model_1_1.InterfaceWeaver`
:py:class:`abdicate.model_1_1.InterfaceProvisioner`

