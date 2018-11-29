'''
scan_instances
==============

The following methods allow for interaction into the Tenable.sc 
`Scan Result <https://docs.tenable.com/sccv/api/Scan-Result.html>`_ API.  While
the Tenable.sc API refers to the model these endpoints interact with as 
*ScanResult*, were actually interacting with an instance of a scan definition
stored within the *Scan* API endpoints.  These scan instances could be running
scans, stopped scans, errored scans, or completed scans.  These items are
typically seen under the **Scan Results** section of Tenable.sc.

Methods available on ``sc.scan_instances``:

.. rst-class:: hide-signature
.. autoclass:: ScanResultAPI

    .. automethod:: copy
    .. automethod:: create
    .. automethod:: delete
    .. automethod:: details
    .. automethod:: email
    .. automethod:: export
    .. automethod:: import
    .. automethod:: list
    .. automethod:: pause
    .. automethod:: resume
'''
from .base import SCEndpoint
from tenable.utils import dict_merge

class ScanResultAPI(SCEndpoint):
    pass