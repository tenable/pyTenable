'''
Welcome to pyTenable's documentation!
=====================================

.. image:: https://travis-ci.org/tenable/pyTenable.svg?branch=master
   :target: https://travis-ci.org/tenable/pyTenable
.. image:: https://img.shields.io/pypi/v/pytenable.svg
   :target: https://pypi.org/project/pyTenable/
.. image:: https://img.shields.io/pypi/pyversions/pyTenable.svg
   :target: https://pypi.org/project/pyTenable/
.. image:: https://img.shields.io/pypi/dm/pyTenable.svg
   :target: https://github.com/tenable/pytenable
.. image:: https://img.shields.io/github/license/tenable/pyTenable.svg
   :target: https://github.com/tenable/pytenable

pyTenable is intended to be a pythonic interface into the Tenable application 
APIs.  Further by providing a common interface and a common structure between 
all of the various applications, we can ease the transition from the vastly 
different APIs between some of the products.

Installation
------------

To install the most recent published version to pypi, its simply a matter of 
installing via pip:

.. code-block:: bash
   
   pip install pytenable

If your looking for bleeding-edge, then feel free to install directly from the 
github repository like so:

.. code-block:: bash

   pip install git+git://github.com/tenable/pytenable.git#egg=pytenable

Getting Started
---------------

Lets assume that we want to get the list of scans that have been run on our 
Tenable.io application.  Performing this action is as simple as the following:

.. code-block:: python
   :linenos:

   from tenable.io import TenableIO
   tio = TenableIO('TIO_ACCESS_KEY', 'TIO_SECRET_KEY')
   for scan in tio.scans.list():
      print('{status}: {id}/{uuid} - {name}'.format(**scan))

Getting started with SecurityCenter is equally as easy:

.. code-block:: python
   :linenos:

   from tenable.sc import TenableSC
   sc = TenableSC('SECURITYCENTER_NETWORK_ADDRESS')
   sc.login('SC_USERNAME', 'SC_PASSWORD')
   for vuln in sc.analysis.vulns():
      print('{ip}:{pluginID}:{pluginName}'.format(**vuln))

For more detailed information on whats available, please refer to the navigation
section for the Tenable application you're looking 

Contribute
----------

- Issue Tracker: https://github.com/tenable/pyTenable/issues
- Github Repository: https://github.com/tenable/pyTenable

License
-------

The project is licensed under the MIT license.
'''
from .base import __version__

__author__ = 'Steve McGrath <smcgrath@tenable.com>'
__license__ = 'MIT'