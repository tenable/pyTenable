'''
Service Provider

Methods available on ``tio.v3.mssp``:


.. rst-class:: hide-signature
.. autoclass:: ManagedSecurityServiceProvider
    :members:

.. toctree::
    :hidden:
    :glob:

    accounts
    definitions
    logos
'''
from tenable.io.v3.base.endpoints.explore import ExploreBaseEndpoint
from tenable.io.v3.mssp.accounts.api import AccountsAPI
from tenable.io.v3.mssp.logos.api import LogosAPI


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

    @property
    def logos(self):
        '''
        The interface object for the
        :doc:`Tenable.io v3 Logos APIs <logos>`
        '''
        return LogosAPI(self._api)
