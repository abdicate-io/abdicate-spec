Example
=======

This directory models the service model described here in Disnix
https://github.com/svanderburg/disnix-stafftracker-php-example/blob/master/deployment/DistributedDeployment/services.nix

but with abdicate.




disnix-stafftracker-php-example
===============================
This is an example case representing a system to manage staff of a university
department. The system uses data stored in several databases, such as a database
to store zipcodes, room numbers and staff members. A web application front-end is
provided for end-users to retrieve and edit staff members.

Architecture
============
![Stafftracker architecture](https://raw.githubusercontent.com/svanderburg/disnix-stafftracker-php-example/master/doc/architecture.png)

The above figure shows the architecture of this example, consisting of two
layers. The data layer contains various MySQL databases storing data sets. The
presentation layer contains a web application front-end which can be used by end
users to manage staff of a university. All the components in the figure are
*distributable* components (or *services*) which can deployed to various machines
in the network.