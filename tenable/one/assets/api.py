"""
Assets
=============

Methods described in this section relate to the assets API.
These methods can be accessed at ``TenableOne.assets``.

.. rst-class:: hide-signature
.. autoclass:: AssetsAPI
    :members:
"""
from typing import Optional

from tenable.base.endpoint import APIEndpoint
from tenable.one.assets.schema import AssetProperties, AssetClass, AssetField


class AssetsAPI(APIEndpoint):

    def list_properties(self, asset_classes: Optional[list[AssetClass]] = None):
        """
         Retrieve assets properties

         Args:
            asset_classes (list, optional):
                 Getting properties for specifc asset classes
                 If this parameter is omitted,
                 Tenable returns properties for all asset classes.
                 For example: asset_classes=[AssetClass.DEVICE].

        Returns:
            :obj:`AssetProperties`:
                The asset properties.

         Examples:
             >>> tone_asset_properties = tone.assets.list_properties()
             >>> for asset_property in tone_asset_properties:
             ...     pprint(asset_property)

        """
        payload = {}
        if asset_classes is not None:
            asset_classes: str = ",".join([asset_class.value for asset_class in asset_classes])
            payload["asset_classes"] = asset_classes
        asset_properties_response: dict[str, list[dict]] = self._get(path="one/api/v1/assets/properties", params=payload)
        return AssetProperties(**asset_properties_response).properties

    def list(
            self,
            query_text: str,
            query_mode: str = "simple",
            filters: Optional[list[dict]] = None,
            extra_properties: Optional[list[str]] = None,
            skip: int = 0,
            max_page_size: int = 100,
            sort_by: str = "aes",
            sort_direction: str = "desc",
            timezone: str = "America/Chicago",
    ):
        """
         Retrieve assets

         Args:
            query_text (str):
                The text to search for.
            query_mode (str, optional):
                The search mode. Defaults to "simple".
            filters (list, optional):
                A list of filters to apply. Defaults to None.
            extra_properties (list, optional):
                Additional properties to include in the response. Defaults to None.
            skip (int, optional):
                Number of records to skip. Defaults to 0.
            max_page_size (int, optional):
                Maximum number of records per page. Defaults to 100.
            sort_by (str, optional):
                Field to sort by. Defaults to "aes".
            sort_direction (str, optional):
                Sorting direction, either "asc" or "desc". Defaults to "desc".
            timezone (str, optional):
                Timezone setting for the query. Defaults to "America/Chicago".

        Returns:
            :obj:`AssetProperties`:
                The asset properties.

         Examples:
             >>> tone_assets = tone.assets.list()
             >>> for asset_property in tone_asset_properties:
             ...     pprint(asset_property)

        """
        # payload = {}
        # if asset_classes is not None:
        #     asset_classes: str = ",".join([asset_class.value for asset_class in asset_classes])
        #     payload["asset_classes"] = asset_classes
        # asset_properties_response: dict[str, list[dict]] = self._get(path="one/api/v1/assets/properties", params=payload)
        # return AssetProperties(**asset_properties_response).properties

        payload = {
            "search": {
                "query": {
                    "text": query_text,
                    "mode": query_mode
                },
                "filters": filters if filters is not None else []
            },
            "extra_properties": extra_properties if extra_properties is not None else [],
            "skip": skip,
            "max_page_size": max_page_size,
            "sort_by": sort_by,
            "sort_direction": sort_direction,
            "timezone": timezone
        }
        self._post(path="one/api/v1/assets", json=payload)
