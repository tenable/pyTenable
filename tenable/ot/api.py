"""
Tenable OT Security API Base
======

Methods described in this section relate to the Tenable OT Security API Base class.

.. rst-class:: hide-signature
.. autoclass:: OTAPIBase
    :members:
"""
from typing import List, Optional

from tenable.base.endpoint import APIEndpoint
from tenable.ot.graphql.definitions import GraphObject
from tenable.ot.graphql.iterators import OTGraphIterator


class OTAPIBase(APIEndpoint):
    query = None
    schema_class = None

    def list(
        self,
        query: str,
        query_filter: Optional[dict] = None,
        search: Optional[str] = None,
        sort: Optional[List[dict]] = None,
        start_at: Optional[str] = None,
        limit: Optional[int] = 200,
        **kwargs
    ) -> OTGraphIterator:
        if sort is None:
            sort = []

        query_variables = {
            "search": search,
            "sort": sort,
            "startAt": start_at,
            "limit": limit,
        }

        if query_filter is not None:
            query_variables["filter"] = query_filter

        graph_obj = GraphObject(
            object_name=self._path,
            query=query,
            resp_schema=self.schema_class,
            query_variables=query_variables,
        )

        return OTGraphIterator(api=self._api, graph_object=graph_obj, **kwargs)
