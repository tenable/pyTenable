"""
Tags
=====

The following methods allow for interaction with the Tenable One
Tags APIs.

Methods available on ``TenableOne.tags``:

.. rst-class:: hide-signature
.. autoclass:: TagsAPI
    :members:
"""

from typing import Optional

from tenable.base.endpoint import APIEndpoint
from tenable.tenableone.inventory.schema import (
    Field,
    Properties,
    PropertyFilter,
    QueryMode,
    SortDirection,
)
from tenable.tenableone.tags.schema import Tags


class TagsAPI(APIEndpoint):
    def list_properties(self) -> list[Field]:
        """
        Retrieve tags properties

        Returns:
            The tags properties.

        Examples:
             >>> tenable_inventory_tags_properties = tenable_inventory.tags.list_properties()
             >>> for tag_property in tenable_inventory_tags_properties:
             ...     pprint(tag_property)

        """
        tag_properties_response: dict[str, list[dict]] = self._get(
            path='api/v1/t1/tags/properties'
        )
        return Properties(**tag_properties_response).data

    def list(
        self,
        query_text: Optional[str] = None,
        query_mode: Optional[QueryMode] = None,
        filters: Optional[list[PropertyFilter]] = None,
        extra_properties: Optional[list[str]] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        sort_by: Optional[str] = None,
        sort_direction: Optional[SortDirection] = None,
    ) -> Tags:
        """
        Retrieve tags

        Args:
            query_text (str, optional):
                The text to search for.
            query_mode (QueryMode, optional):
                The search mode. Defaults to QueryMode.SIMPLE.
            filters (list, optional):
                A list of filters to apply. Defaults to None.
            extra_properties (list, optional):
                Additional properties to include in the response. Defaults to None.
            offset (int, optional):
                Number of records to skip. Defaults to 0.
            limit (int, optional):
                Maximum number of records per page. Defaults to 1000.
            sort_by (str, optional):
                Field to sort by.
            sort_direction (SortDirection, optional):
                Sorting direction, either SortDirection.ASC or SortDirection.DESC.

        Returns:
            The request tags.

        Examples:
             >>> tags = tenable_inventory.tags.list()
             >>> for tag in tags:
             ...     pprint(tag)

        """
        # Build query parameters
        params = {}
        if extra_properties is not None:
            params['extra_properties'] = ','.join(extra_properties)
        if offset is not None:
            params['offset'] = offset
        if limit is not None:
            params['limit'] = limit
        if sort_by is not None and sort_direction is not None:
            params['sort'] = f"{sort_by}:{sort_direction.value}"

        # Build request body with flattened search/query params
        payload = {}
        if query_text is not None or query_mode is not None:
            payload['query'] = {}
            if query_text is not None:
                payload['query']['text'] = query_text
            if query_mode is not None:
                payload['query']['mode'] = query_mode.value
        if filters is not None:
            payload['filters'] = [filter.model_dump(mode='json') for filter in filters]

        tags_response: dict = self._post('api/v1/t1/tags/search', json=payload, params=params)
        return Tags(**tags_response)
