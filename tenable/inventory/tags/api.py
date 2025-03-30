"""
Tags
=============

Methods described in this section relate to the tags API.
These methods can be accessed at ``TenableInventory.tags``.

.. rst-class:: hide-signature
.. autoclass:: TagsAPI
    :members:
"""

from tenable.base.endpoint import APIEndpoint
from tenable.inventory.schema import Properties, Field


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
