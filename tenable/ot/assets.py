'''
Assets
======

Methods described in this section relate to the the assets API.
These methods can be accessed at ``TenableOT.assets``.

.. rst-class:: hide-signature
.. autoclass:: AssetsAPI
    :members:
'''
from tenable.base.endpoint import APIEndpoint
from .schemas.paging import PaginationSchema
from .schemas.iterators import OTIterator
from box import BoxList


class AssetsAPI(APIEndpoint):
    _path = 'assets'

    def list(self, **kwargs):
        '''
        Retreives a list of assets.

        Args:
            filters (list[tuple], optional):
                A list of filter tuples.
            orderBy (list[dict], optional):
                A list of order documents, each of which must contain both the
                ``field`` and ``direction`` keys.
            search (str, optional):
                A search string to further limit the response.

        Returns:
            :obj:`OTIterator`:
                An iterator object that will handle pagination of the data.

        Example:
            >>> for asset in ot.assets.list():
            ...     print(asset)
        '''
        schema = PaginationSchema()
        kwargs['model'] = 'assets'
        return OTIterator(self._api,
            path=self._path,
            payload=schema.load(kwargs)
        )

    def details(self, id):
        '''
        Retreive the details of a given asset

        Args:
            id (str):
                The unique identifier for the asset.

        Returns:
            :obj:`dict`:
                The resource record for the asset

        Example:
            >>> asset = ot.assets.details(id)
        '''
        return self._get(id)

    def connections(self, id):
        '''
        Retreive the connections of a given asset

        Args:
            id (str):
                The unique identifier for the asset.

        Returns:
            :obj:`list`:
                The list of connections present on the given asset.

        Example:
            >>> connections = ot.assets.connections(id)
        '''
        return self._get('{}/connections'.format(id), box=BoxList)