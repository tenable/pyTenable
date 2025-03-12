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

    def list_properties(self, asset_classes: Optional[list[AssetClass]] = None) -> list[AssetField]:
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
