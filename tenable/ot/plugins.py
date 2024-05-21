"""
Plugins
=======

Methods described in this section relate to the plugins API.
These methods can be accessed at ``TenableOT.plugins``.

.. rst-class:: hide-signature
.. autoclass:: PluginsAPI
    :members:
"""
from typing import List, Optional

from tenable.ot.api import OTAPIBase
from tenable.ot.graphql.iterators import OTGraphIterator
from tenable.ot.graphql.query import PLUGINS_QUERY, PLUGINS_DETAILS_QUERY
from tenable.ot.graphql.schema.plugins import PluginsSchema


class PluginsAPI(OTAPIBase):
    _path = "plugins"
    schema_class = PluginsSchema

    def list(
        self,
        query: str = PLUGINS_QUERY,
        query_filter: Optional[dict] = None,
        search: Optional[str] = None,
        sort: Optional[List[dict]] = None,
        start_at: Optional[str] = None,
        limit: Optional[int] = 200,
        **kwargs,
    ) -> OTGraphIterator:
        """
        Retrieves a list of plugins via the GraphQL API.

        Args:
            query(str):
                A GraphQL query .
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
            >>>     for plugin in tot.plugins.list(limit=500):
                        print(plugin)
        """
        if not sort:
            sort = [{"field": "id", "direction": "DescNullLast"}]

        return super().list(
            query=query,
            query_filter=query_filter,
            search=search,
            sort=sort,
            start_at=start_at,
            limit=limit,
            **kwargs,
        )

    def plugin(
        self,
        plugin_id: int,
        **kwargs,
    ) -> OTGraphIterator:
        """
        Retrieve a specific plugin with additionals details by ID.

        Args:
            plugin_id (int):

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
                "values": plugin_id,
            },
            query=PLUGINS_DETAILS_QUERY,
            **kwargs,
        )
