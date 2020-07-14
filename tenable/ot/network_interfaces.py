'''
Network Interfaces
==================

Methods described in this section relate to the the network_interfaces API.
These methods can be accessed at ``TenableOT.network_interfaces``.

.. rst-class:: hide-signature
.. autoclass:: NetworkInterfacesAPI
    :members:
'''
from tenable.base.endpoint import APIEndpoint
from .schemas.paging import PaginationSchema
from box import BoxList


class NetworkInterfacesAPI(APIEndpoint):
    _path = 'networkinterfaces'

    def details(self, id):
        '''
        Retreives the details for the specified network interface

        Args:
            id (str):
                The unique identifier.

        Returns:
            :obj:`dict`:
                The network interface resource record.

        Example:
            >>> ot.network_interfaces.details(id)
        '''
        return self._get(id)

    def connections(self, id):
        '''
        Returns the connections for a given network interface.

        Args:
            id (str):
                The unique idenifier for the network interface.

        Returns:
            :obj:`list`:
                The list of connections associated to the network interface.

        Example:
            >>> ot.network_interfaces.connections(id)
        '''
        return self._get('{}/connections'.format(id), box=BoxList)