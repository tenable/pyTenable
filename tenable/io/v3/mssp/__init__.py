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

    accounts
'''
from tenable.io.v3.base.endpoints.explore import ExploreBaseEndpoint
from tenable.io.v3.mssp.accounts.api import AccountsAPI


class ManagedSecurityServiceProvider(ExploreBaseEndpoint):  # noqa: PLR0904
    '''
    This class will contain property for all resources under Managed Security
    Service Provider.
    '''

    @property
    def accounts(self):
        '''
        The interface object for the
        :doc:`Tenable.io v3 Accounts APIs <accounts>`
        '''
        return AccountsAPI(self._api)
