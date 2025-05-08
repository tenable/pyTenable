"""
Tags
=============

Methods described in this section relate to the tags API.
These methods can be accessed at ``TenableInventory.tags``.

.. rst-class:: hide-signature
.. autoclass:: TagsAPI
    :members:
"""
from typing import Optional

from tenable.base.endpoint import APIEndpoint
from tenable.exposure_management.inventory.schema import Properties, Field, QueryMode, PropertyFilter, SortDirection
from tenable.exposure_management.tags.schema import Tags


class TagsAPI(APIEndpoint):

    def list_properties(self) -> list[Field]:
        """
         Retrieve tags properties

        Returns:
            :list:`Field`:
                The tags properties.

         Examples:
             >>> tenable_inventory_tags_properties = tenable_inventory.tags.list_properties()
             >>> for tag_property in tenable_inventory_tags_properties:
             ...     pprint(tag_property)

        """
        tag_properties_response: dict[str, list[dict]] = self._get(path="inventory/api/v1/tags/properties")
        return Properties(**tag_properties_response).properties

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
            timezone: Optional[str] = None,
    ) -> Tags:
        """
         Retrieve assets

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
            timezone (str, optional):
                Timezone setting for the query. Defaults to "UTC".

        Returns:
            :obj:`Tag`:
                The request tags.

         Examples:
             >>> tags = tenable_inventory.tags.list()
             >>> for tag in tags:
             ...     pprint(tag)

        """
        payload = {}

        if query_text is not None and query_mode is not None and filters is not None:
            payload["search"] = {
                "query": {
                    "text": query_text,
                    "mode": query_mode.value
                },
                "filters": [filter.model_dump(mode='json') for filter in filters] if filters is not None else []
            }

        if extra_properties is not None:
            payload["extra_properties"] = extra_properties
        if offset is not None:
            payload["offset"] = offset
        if limit is not None:
            payload["limit"] = limit
        if sort_by is not None:
            payload["sort_by"] = sort_by
        if sort_direction is not None:
            payload["sort_direction"] = sort_direction.value
        if timezone is not None:
            payload["timezone"] = timezone

        tags_response: dict = self._post("inventory/api/v1/tags", json=payload)
        return Tags(**tags_response)
