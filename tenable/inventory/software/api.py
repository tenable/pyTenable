"""
Software
=============

Methods described in this section relate to the software API.
These methods can be accessed at ``TenableInventory.software``.

.. rst-class:: hide-signature
.. autoclass:: SoftwareAPI
    :members:
"""
from typing import Optional

from tenable.base.endpoint import APIEndpoint
from tenable.inventory.schema import Properties, Field, QueryMode, PropertyFilter, SortDirection
from tenable.inventory.software.schema import SoftwareValues


class SoftwareAPI(APIEndpoint):

    def list_properties(self) -> list[Field]:
        """
         Retrieve software properties

        Returns:
            :list:`Field`:
                The software properties.

         Examples:
             >>> tenable_inventory_software_properties = tenable_inventory.software.list_properties()
             >>> for software_property in software_properties:
             ...     pprint(software_property)

        """
        asset_properties_response: dict[str, list[dict]] = self._get(path="inventory/api/v1/software/properties")
        return Properties(**asset_properties_response).properties

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
    ) -> SoftwareValues:
        """
         Retrieve software

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
                Maximum number of records per page. Defaults to 100.
            sort_by (str, optional):
                Field to sort by.
            sort_direction (SortDirection, optional):
                Sorting direction, either SortDirection.ASC or SortDirection.DESC.
            timezone (str, optional):
                Timezone setting for the query. Defaults to "UTC".

        Returns:
            :obj:`SoftwareValues`:
                The request assets.

         Examples:
             >>> tenable_inventory_software = tenable_inventory.software.list()
             >>> for software in tenable_inventory_software:
             ...     pprint(software)

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

        software_response: dict = self._post("inventory/api/v1/software", json=payload)
        return SoftwareValues(**software_response)
