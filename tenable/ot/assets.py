"""
Assets
======

Methods described in this section relate to the assets API.
These methods can be accessed at ``TenableOT.assets``.

.. rst-class:: hide-signature
.. autoclass:: AssetsAPI
    :members:
"""
from typing import List, Optional

from tenable.ot.api import OTAPIBase
from tenable.ot.graphql.iterators import OTGraphIterator
from tenable.ot.graphql.query import ASSETS_QUERY
from tenable.ot.graphql.schema.assets import AssetsSchema


class AssetsAPI(OTAPIBase):
    _path = "assets"
    query = ASSETS_QUERY
    schema_class = AssetsSchema

    def list(
        self,
        query_filter: Optional[dict] = None,
        search: Optional[str] = None,
        sort: Optional[List[dict]] = None,
        start_at: Optional[str] = None,
        limit: Optional[int] = 200,
        **kwargs,
    ) -> OTGraphIterator:
        """
        Retrieves a list of assets via the GraphQL API.

        Args:
            query_filter(dict, optional):
                A document as defined by Tenable OT Security online documentation.
            search(str, optional):
                A search string to further limit the response.
            sort(List[dict], optional):
                A list of order documents, each of which must contain both the
                ``field`` and ``direction`` keys and may also contain the
                optional ``function`` key. Default sort is by descending id
                order. Please refer to Tenable OT Security online documentation for more
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
        """
        if not sort:
            sort = [{"field": "id", "direction": "DescNullLast"}]

        if not query_filter:
            query_filter = {
                "op": "Equal",
                "field": "hidden",
                "values": "false"
            }

        return super().list(
            query=ASSETS_QUERY,
            query_filter=query_filter,
            search=search,
            sort=sort,
            start_at=start_at,
            limit=limit,
            **kwargs,
        )

    def asset(
        self,
        asset_id: int,
        **kwargs,
    ) -> OTGraphIterator:
        """
        Retrieve a specific asset by ID.

        Args:
            asset_id (int):

        Returns:
            :obj:`OTGraphIterator`:
                An iterator object handling data pagination.
        Example:
            >>>     tot.plugins.plugin(1)

        """
        return super().list(
            query_filter={
                "field": "id",
                "op": "Equal",
                "values": asset_id,
            },
            query=ASSETS_QUERY,
            **kwargs,
        )
