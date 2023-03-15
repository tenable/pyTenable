Welcome to pyTenable's documentation!
=====================================

.. image:: https://img.shields.io/endpoint.svg?url=https%3A%2F%2Factions-badge.atrox.dev%2Ftenable%2FpyTenable%2Fbadge&label=build
   :target: https://github.com/tenable/pyTenable/actions
.. image:: https://img.shields.io/pypi/v/pytenable.svg
   :target: https://pypi.org/project/pyTenable/
.. image:: https://img.shields.io/badge/python-3.7%203.8%203.9%203.10%203.11-blue
   :target: https://pypi.org/project/pyTenable/
.. image:: https://img.shields.io/pypi/dm/pytenable
   :target: https://github.com/tenable/pytenable
.. image:: https://img.shields.io/github/license/tenable/pyTenable.svg
   :target: https://github.com/tenable/pytenable
.. image:: https://sonarcloud.io/api/project_badges/measure?project=tenable_pyTenable&metric=alert_status
   :target: https://sonarcloud.io/project/overview?id=tenable_pyTenable

pyTenable is intended to be a pythonic interface into the Tenable application
APIs.  Further by providing a common interface and a common structure between
all of the various applications, we can ease the transition from the vastly
different APIs between some of the products.

- Issue Tracker: https://github.com/tenable/pyTenable/issues
- Github Repository: https://github.com/tenable/pyTenable

Installation
------------

To install the most recent published version to pypi, its simply a matter of
installing via pip:

.. code-block:: bash

   pip install pytenable

If you're looking for bleeding-edge, then feel free to install directly from the
github repository like so:

.. code-block:: bash

   pip install git+git://github.com/tenable/pytenable.git#egg=pytenable

Getting Started
---------------

Lets assume that we want to get the list of scans that have been run on our
Tenable.io application.  Performing this action is as simple as the following:

.. code-block:: python

   from tenable.io import TenableIO
   tio = TenableIO('TIO_ACCESS_KEY', 'TIO_SECRET_KEY')
   for scan in tio.scans.list():
      print('{status}: {id}/{uuid} - {name}'.format(**scan))

Getting started with Tenable.sc is equally as easy:

.. code-block:: python

   from tenable.sc import TenableSC
   sc = TenableSC('SECURITYCENTER_NETWORK_ADDRESS')
   sc.login('SC_USERNAME', 'SC_PASSWORD')
   for vuln in sc.analysis.vulns():
      print('{ip}:{pluginID}:{pluginName}'.format(**vuln))

For more detailed information on whats available, please refer to the
`pyTenable Documentation <https://pytenable.readthedocs.io/>`_

Logging
-------

Enabling logging for pyTenable is a simple matter of enabling debug logs through
the python logging package.  An easy example is detailed here:

.. code-block:: python

   import logging
   logging.basicConfig(level=logging.DEBUG)

License
-------

The project is licensed under the MIT license.
