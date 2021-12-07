'''
Web Application Scanning
========================

The following API's are available for interaction under Web Application
Scanning

Methods available on ``tio.v3.was``:


.. rst-class:: hide-signature
.. autoclass:: WebApplicationScanning
    :members:

.. toctree::
    :hidden:
    :glob:

    configurations
'''
from restfly.endpoint import APIEndpoint

from tenable.io.v3.was.configurations import ConfigurationsAPI


class WebApplicationScanning(APIEndpoint):  # noqa: PLR0904
    '''
    This class will contain property for all resources under Web Application
    Scanning i.e plugins, scans, folders etc.
    '''

    @property
    def configurations(self):
        '''
        The interface object for the
        :doc:`Configurations API <configurations>`
        '''
        return ConfigurationsAPI(self._api)
