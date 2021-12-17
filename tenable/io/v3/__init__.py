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

    groups
    users
    vm/index
    was/index
'''
from tenable.base.endpoint import APIEndpoint
from tenable.io.v3.groups.api import GroupsAPI
from tenable.io.v3.users.api import UsersAPI
from tenable.io.v3.vm import VulnerabilityManagement
from tenable.io.v3.was import WebApplicationScanning


class Version3API(APIEndpoint):  # noqa: PLR0904
    '''
    This will contain property for all resources/app under io
    i.e Container Security, Web Application Security.
    '''

    @property
    def groups(self):
        '''
        The interface object for the Groups APIs
        :doc:`tenable.io v3 groups APIs <groups>`.
        '''
        return GroupsAPI(self._api)

    @property
    def users(self):
        '''
        The interface object for the
        :doc:`Tenable.io v3 users APIs <users>`.
        '''
        return UsersAPI(self._api)

    @property
    def vm(self):
        '''
        The interface object for the
        :doc:`Vulnerability Management <vm/index>`
        '''
        return VulnerabilityManagement(self._api)

    @property
    def was(self):
        '''
        The interface object for the
         :doc:`Web Application Scanning <was/index>`
        '''
        return WebApplicationScanning(self._api)
