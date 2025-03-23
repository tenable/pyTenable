"""
Software
=============

Methods described in this section relate to the software API.
These methods can be accessed at ``TenableInventory.software``.

.. rst-class:: hide-signature
.. autoclass:: SoftwareAPI
    :members:
"""

from tenable.base.endpoint import APIEndpoint
from tenable.inventory.schema import Properties, Field


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

    def list(self):
        pass
