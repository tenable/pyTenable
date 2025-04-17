"""
Assets
=============

Methods described in this section relate to the assets API.
These methods can be accessed at ``TenableInventory.assets``.

.. rst-class:: hide-signature
.. autoclass:: AssetsAPI
    :members:
"""
from typing import Optional

from tenable.base.endpoint import APIEndpoint
from tenable.inventory.assets.schema import AssetClass, Assets
from tenable.inventory.schema import Field, Properties, SortDirection, QueryMode, PropertyFilter


class AssetsAPI(APIEndpoint):

    def list_properties(self, asset_classes: Optional[list[AssetClass]] = None) -> list[Field]:
        """
         Retrieve assets properties

         Args:
            asset_classes (list, optional):
                 Getting properties for specifc asset classes
                 If this parameter is omitted,
                 Tenable returns properties for all asset classes.
                 For example: asset_classes=[AssetClass.DEVICE].

        Returns:
            :list:`Field`:
                The asset properties.

         Examples:
             >>> tenable_inventory_asset_properties = tenable_inventory.assets.list_properties()
             >>> for asset_property in asset_properties:
             ...     pprint(asset_property)

        """
        payload = {}
        if asset_classes is not None:
            asset_classes: str = ",".join([asset_class.value for asset_class in asset_classes])
            payload["asset_classes"] = asset_classes
        asset_properties_response: dict[str, list[dict]] = self._get(path="inventory/api/v1/assets/properties",
                                                                     params=payload)
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
    ) -> Assets:
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
                Maximum number of records per page. Defaults to 100.
            sort_by (str, optional):
                Field to sort by.
            sort_direction (SortDirection, optional):
                Sorting direction, either SortDirection.ASC or SortDirection.DESC.
            timezone (str, optional):
                Timezone setting for the query. Defaults to "UTC".

        Returns:
            :obj:`Asset`:
                The request assets.

         Examples:
             >>> assets = tenable_inventory.assets.list()
             >>> for asset in assets:
             ...     pprint(asset)

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

        assets_response: dict = self._post("inventory/api/v1/assets", json=payload)
        return Assets(**assets_response)
