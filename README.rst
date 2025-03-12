Welcome to pyTenable's documentation!
=====================================

.. image:: https://img.shields.io/pypi/v/pytenable.svg
.. image:: https://img.shields.io/badge/python-3.10%2B-blue
.. image:: https://img.shields.io/readthedocs/pytenable
.. image:: https://img.shields.io/pypi/dm/pytenable
.. image:: https://img.shields.io/github/license/tenable/pyTenable.svg
.. image:: https://sonarcloud.io/api/project_badges/measure?project=tenable_pyTenable&metric=alert_status

pyTenable is intended to be a pythonic interface into the Tenable application
APIs.  Further by providing a common interface and a common structure between
all of the various applications, we can ease the transition from the vastly
different APIs between some of the products.

- Issue Tracker: https://github.com/tenable/pyTenable/issues
- Github Repository: https://github.com/tenable/pyTenable
- Docs: https://pytenable.readthedocs.io

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
   tio = TenableIO(access_key='TIO_ACCESS_KEY', secret_key='TIO_SECRET_KEY')
   for scan in tio.scans.list():
      print('{status}: {id}/{uuid} - {name}'.format(**scan))

Getting started with Tenable.sc is equally as easy:

.. code-block:: python

   from tenable.sc import TenableSC
   sc = TenableSC(url='https://SC_URL', access_key='AKEY', secret_key='SKEY')
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
