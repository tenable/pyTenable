"""
Assets
=======

Methods described in this section relate to the assets API.
These methods can be accessed at ``TenableOne.inventory.assets``.

.. rst-class:: hide-signature
.. autoclass:: AssetsAPI
    :members:

"""

from typing import Optional

from tenable.base.endpoint import APIEndpoint
from tenable.tenableone.inventory.assets.schema import AssetClass, Assets
from tenable.tenableone.inventory.schema import (
    Field,
    Properties,
    PropertyFilter,
    QueryMode,
    SortDirection,
)


class AssetsAPI(APIEndpoint):
    def list_properties(
        self, asset_classes: Optional[list[AssetClass]] = None
    ) -> list[Field]:
        """
        Retrieve assets properties

        Args:
            asset_classes (list[str], optional):
                 Getting properties for specific asset classes
                 If this parameter is omitted,
                 Tenable returns properties for all asset classes.
                 For example: asset_classes=[AssetClass.DEVICE].

        Returns:
            list[Field]:
                The asset properties.

        Examples:
             >>> tenable_inventory_asset_properties = tenable_inventory.assets.list_properties()
             >>> for asset_property in asset_properties:
             ...     pprint(asset_property)

        """
        payload = {}
        if asset_classes is not None:
            asset_classes: str = ','.join(
                [asset_class.value for asset_class in asset_classes]
            )
            payload['asset_classes'] = asset_classes
        asset_properties_response: dict[str, list[dict]] = self._get(
            path='api/v1/t1/inventory/assets/properties', params=payload
        )
        return Properties(**asset_properties_response).data

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
                Maximum number of records per page. Defaults to 1000.
            sort_by (str, optional):
                Field to sort by.
            sort_direction (SortDirection, optional):
                Sorting direction, either SortDirection.ASC or SortDirection.DESC.

        Returns:
            :obj:`Asset`:
                The request assets.

        Examples:
             >>> assets = tenable_inventory.assets.list()
             >>> for asset in assets:
             ...     pprint(asset)

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

        assets_response: dict = self._post('api/v1/t1/inventory/assets/search', json=payload, params=params)
        return Assets(**assets_response)
