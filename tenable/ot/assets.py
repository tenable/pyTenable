'''
Assets
======

Methods described in this section relate to the the assets API.
These methods can be accessed at ``TenableOT.assets``.

.. rst-class:: hide-signature
.. autoclass:: AssetsAPI
    :members:
'''
from typing import List, Optional
from tenable.base.endpoint import APIEndpoint
from tenable.ot.graphql.assets import (
    ASSETS_QUERY,
    ASSETS_QUERY_OBJECT_NAME,
    AssetsSchema
)
from tenable.ot.graphql.definitions import GraphObject
from tenable.ot.graphql.iterators import OTGraphIterator


class AssetsAPI(APIEndpoint):
    _path = 'assets'

    def list(self,
             filter: Optional[dict] = None,
             search: Optional[str] = None,
             sort: Optional[List[dict]] = None,
             start_at: Optional[str] = None,
             limit: Optional[int] = 200,
             **kwargs):
        '''
        Retrieves a list of assets via the GraphQL API.

        Args:
            filter(dict, optional):
                A document as defined by Tenable.ot online documentation.
            search(str, optional):
                A search string to further limit the response.
            sort(list[dict], optional):
                A list of order documents, each of which must contain both the
                ``field`` and ``direction`` keys and may also contain the
                optional ``function`` key. Default sort is by descending id
                order. Please refer to Tenable.ot online documentation for more
                information.
            start_at(str, optional):
                The cursor to start the scan from (the default is an empty
                cursor).
            limit(int, optional):
                Max number of objects that get retrieved per page (the default
                is 200).

        Returns:
            :obj:`OTGraphIterator`:
                An iterator object that will handle pagination of the data.

        Example:
            >>>     for asset in tot.assets.list(limit=500):
                        print(asset)
        '''
        if not sort:
            sort = [{'field': 'id', 'direction': 'DescNullLast'}]

        query_variables = {
            'search': search,
            'sort': sort,
            'startAt': start_at,
            'limit': limit
        }
        if filter:
            query_variables['filter'] = filter

        graph_obj = GraphObject(
            object_name=ASSETS_QUERY_OBJECT_NAME,
            query=ASSETS_QUERY,
            resp_schema=AssetsSchema,
            query_variables=query_variables
        )

        return OTGraphIterator(self._api, graph_obj, **kwargs)
