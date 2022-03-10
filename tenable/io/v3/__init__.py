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

    assets
    groups
    mssp/index
    users
    vm/index
    was/index
'''
from tenable.base.endpoint import APIEndpoint
from tenable.io.v3.assets.api import AssetsAPI
from tenable.io.v3.groups.api import GroupsAPI
from tenable.io.v3.mssp import ManagedSecurityServiceProvider
from tenable.io.v3.users.api import UsersAPI
from tenable.io.v3.vm import VulnerabilityManagement
from tenable.io.v3.was import WebApplicationScanning


class Version3API(APIEndpoint):  # noqa: PLR0904
    '''
    This will contain property for all resources/app under io
    i.e Container Security, Web Application Security.
    '''

    @property
    def assets(self):
        """
        The interface object for the Assets APIs
        :doc:`Tenable.io.v3.assets Assets APIs <assets>`.
        """
        return AssetsAPI(self._api)

    @property
    def groups(self):
        '''
        The interface object for the Groups APIs
        :doc:`Tenable.io v3 Groups APIs <groups>`.
        '''
        return GroupsAPI(self._api)

    @property
    def mssp(self):
        '''
        The interface object for the
        :doc:`Tenable.io v3 Managed Security Service Provider APIs
        <mssp/index>`.
        '''
        return ManagedSecurityServiceProvider(self._api)

    @property
    def users(self):
        '''
        The interface object for the
        :doc:`Tenable.io v3 Users APIs <users>`.
        '''
        return UsersAPI(self._api)

    @property
    def vm(self):
        '''
        The interface object for the
        :doc:`Tenable.io v3 Vulnerability Management <vm/index>`
        '''
        return VulnerabilityManagement(self._api)

    @property
    def was(self):
        '''
        The interface object for the
         :doc:`Tenable.io v3 Web Application Scanning <was/index>`
        '''
        return WebApplicationScanning(self._api)
