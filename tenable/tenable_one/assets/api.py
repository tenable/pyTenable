"""
Assets
=============

Methods described in this section relate to the assets API.
These methods can be accessed at ``TenableOne.assets``.

.. rst-class:: hide-signature
.. autoclass:: AssetsAPI
    :members:
"""

from tenable.base.endpoint import APIEndpoint
from tenable.tenable_one.assets.schema import AssetsPropertiesSchema


class AssetsAPI(APIEndpoint):

    def list_properties(self) -> list[str]:
        """
         Retrieve assets properties

         Args:

        Returns:
            :obj:`list`:
                The list of assets properties.

         Examples:
             >>> tone_assets_properties = tone.assets.list_properties()
             >>> for asset_property in tone_assets_properties:
             ...     pprint(asset_property)

        """

        return AssetsPropertiesSchema().load(
            self._get(path="one/api/v1/assets/properties")
        )
