'''
Version3 API
============

The following sub-package allows for interaction with the Tenable.io
Version3API APIs.

Methods available on ``tio.v3``:

.. rst-class:: hide-signature
.. autoclass:: Version3API
    :members:

.. toctree::
    :hidden:
    :glob:

    was/index
'''
from tenable.base.endpoint import APIEndpoint
from tenable.io.v3.was import WebApplicationScanning


class Version3API(APIEndpoint):
    '''
    This will contain property for all resources/app under io- Web Application Security.
    '''

    @property
    def was(self):
        '''
        The interface object for the
         :doc:`Tenable.io v3 Web Application Scanning <was/index>`
        '''
        return WebApplicationScanning(self._api)
