"""
Events
======

Methods described in this section relate to the events API.
These methods can be accessed at ``TenableOT.events``.

.. rst-class:: hide-signature
.. autoclass:: EventsAPI
    :members:
"""
from typing import List, Optional

from tenable.ot.api import OTAPIBase
from tenable.ot.graphql.iterators import OTGraphIterator
from tenable.ot.graphql.query import EVENTS_QUERY
from tenable.ot.graphql.schema.events import EventsSchema


class EventsAPI(OTAPIBase):
    _path = "events"
    schema_class = EventsSchema

    def list(
        self,
        query_filter: Optional[dict] = None,
        search: Optional[str] = None,
        sort: Optional[List[dict]] = None,
        start_at: Optional[str] = None,
        limit: Optional[int] = 200,
        **kwargs
    ) -> OTGraphIterator:
        """
        Retrieves a list of events via the GraphQL API.

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
            >>>     for event in tot.events.list(limit=500):
                        print(event)
        """
        if not sort:
            sort = [{"field": "eventId", "direction": "DescNullLast"}]

        return super().list(
            query=EVENTS_QUERY,
            query_filter=query_filter,
            search=search,
            sort=sort,
            start_at=start_at,
            limit=limit,
            **kwargs
        )
