Welcome to pyTenable's documentation!
=====================================

.. image:: https://travis-ci.org/tenable/pyTenable.svg?branch=master
    :target: https://travis-ci.org/tenable/pyTenable

pyTenable is intended to be a pythonic interface into the Tenable application APIs.  Further by providing a common interface and a common structure between all of the various applications, we can ease the transition from the vastly different APIs between some of the products.

Installation
------------

To install the most recent published version to pypi, its simply a matter of installing via pip:

.. code-block:: bash
   
   pip install pytenable

If your looking for bleeding-edge, then feel free to install directly from the github repository like so:

.. code-block:: bash

   pip install git+git://github.com/tenable/pytenable.git#egg=pytenable

Getting Started
---------------

Lets assume that we want to get the list of scans that have been run on our Tenable.io application.  Performing this action is as simple as the following:

.. code-block:: python
   :linenos:

   from tenable.tenable_io import TenableIO
   tio = TenableIO('TIO_ACCESS_KEY', 'TIO_SECRET_KEY')
   for scan in tio.scans.list():
      print('{status}: {id}/{uuid} - {name}'.format(**scan))

Another example would be to export the vulnerability data that Tenable.io has stored.  Again, just a few lines:

.. code-block:: python
   :linenos:

   vulns = tio.exports.vulns()
   for item in vulns:
      print(item['plugin']['name'])

For more detailed examples, please refer to the specific applications listed below.

.. toctree::
   :maxdepth: 1
   :caption: Supported Applications:

   container_security
   nessus
   securitycenter
   tenable_io

Contribute
----------

- Issue Tracker: https://github.com/tenable/pyTenable/issues
- Github Repository: https://github.com/tenable/pyTenable

License
-------

The project is licensed under the BSD license.

