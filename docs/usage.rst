Usage
=====

.. _installation:

Installation
------------

To use Abdicate, first install it using pip:

.. code-block:: console

   (.venv) $ pip install abdicate

Generating a deployment model
-----------------------------

To generate a deployment model for a directory of definitions,
you can use the ``abdicate.deployment.read_directory()`` function:


Calling :py:func:`abdicate.deployment.read_directory` will return a :py:class:`abdicate.deployment.DeploymentModel`


For example:

>>> from abdicate.deployment import read_directory
>>> read_directory('deployments/')
DeploymentModel[services={}]
