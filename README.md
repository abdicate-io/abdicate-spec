## Abdicate

Abdicate is an opinionated technology-agnostic specification to model applications and their resource dependency relationships.
It makes no assumptions about the technical implementation of the deployment or target system,
allowing the same model throughout the entire life of the applications and without having to commit to a technology/tooling stack.

Knowledge encapsulation

Application model

Convention


## Help

See [examples](tree/master/examples) for more details.

## Installation

Install using `pip install -U abdicate-spec`.

Or `pip install git+https://github.com/abdicate-io/abdicate-spec.git`


## A Simple Example

```yaml
version: "1.0"

friendlyName: petstore-ws
domains:
  - ecommerce
components:
  - pets
requires:
  databases:
    orm:
      alias: db
      interface: mysql:5
provides:
  rest:
    interface: http
    x-url: /v1/
    x-swagger-url: /swagger-ui.html
```

## Inspiration
Docker compose, Helm charts, Terraform, Juju, ...