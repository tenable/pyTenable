'''
scan_results
============

The following methods allow for interaction into the SecurityCenter 
`Scan Result <https://docs.tenable.com/sccv/api/Scan-Result.html>`_ API.

Methods available on ``sc.scan_results``:

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