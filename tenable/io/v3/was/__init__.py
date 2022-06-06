'''
Web Application Scanning
========================

The following API's are available for interaction under Web Application Scanning

Methods available on ``tio.v3.was``:


.. rst-class:: hide-signature
.. autoclass:: WebApplicationScanning
    :members:

.. toctree::
    :hidden:
    :glob:

    vulnerabilities
'''
from tenable.io.v3.base.endpoints.explore import ExploreBaseEndpoint
from tenable.io.v3.was.vulnerabilities.api import VulnerabilityAPI


class WebApplicationScanning(ExploreBaseEndpoint):  # noqa: PLR0904
    '''
    This class will contain property for all resources under Web Application Scanning - vulnerabilities (findings)
    '''

    @property
    def vulnerabilities(self):
        '''
        The interface object for the
        :doc:`Tenable.io v3 WAS Vulnerabilities APIs <vulnerabilities>`
        '''
        return VulnerabilityAPI(self._api)
