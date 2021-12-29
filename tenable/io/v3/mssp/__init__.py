'''
Managed Security Service Provider
=================================
The following API's are available for interaction under Managed Security
Service Provider

Methods available on ``tio.v3.mssp``:

.. rst-class:: hide-signature
.. autoclass:: ManagedSecurityServiceProvider
    :members:

.. toctree::
    :hidden:
    :glob:

    logos
'''
from tenable.io.v3.base.endpoints.explore import ExploreBaseEndpoint
from tenable.io.v3.mssp.logos.api import LogosAPI


class ManagedSecurityServiceProvider(ExploreBaseEndpoint):  # noqa: PLR0904
    '''
    This class will contain property for all resources under Managed Security
    Service Provider.
    '''

    @property
    def logos(self):
        '''
        The interface object for the
        :doc:`Logos API <logos>`
        '''
        return LogosAPI(self._api)
