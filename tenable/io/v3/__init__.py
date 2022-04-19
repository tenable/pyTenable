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

    connectors
    definitions
    mssp/index
    platform/index
    users
    vm/index
    was/index
'''
from tenable.base.endpoint import APIEndpoint
from tenable.io.v3.connectors.api import ConnectorsAPI
from tenable.io.v3.definitions.api import DefinitionsAPI
from tenable.io.v3.mssp import ManagedSecurityServiceProvider
from tenable.io.v3.platform import Platform
from tenable.io.v3.platform.groups.api import GroupsAPI
from tenable.io.v3.users.api import UsersAPI
from tenable.io.v3.vm import VulnerabilityManagement
from tenable.io.v3.vm.assets.api import AssetsAPI
from tenable.io.v3.was import WebApplicationScanning


class Version3API(APIEndpoint):
    '''
    This will contain property for all resources/app under io
    i.e Container Security, Web Application Security.
    '''

    @property
    def definitions(self):
        """
        The interface object for the Definitions APIs
        :doc:`Tenable.io v3 definitions APIs <definitions>`.
        """
        return DefinitionsAPI(self._api)

    @property
    def connectors(self):
        '''
        The interface object for the connectors APIs
        :doc:`Tenable.io v3 connectors APIs <connectors>`.
        '''
        return ConnectorsAPI(self._api)

    @property
    def platform(self):
        '''
        The interface object for the
        :doc:`Platform <platform/index>`
        '''
        return Platform(self._api)

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
