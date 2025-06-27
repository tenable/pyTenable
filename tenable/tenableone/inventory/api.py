"""
Inventory
=========

The following sub-package allows for interaction with the Tenable One
Inventory APIs.

.. rst-class:: hide-signature
.. autoclass:: InventoryAPI
    :members:

.. toctree::
    :hidden:
    :glob:

    software/index
"""

from tenable.base.endpoint import APIEndpoint
from tenable.tenableone.inventory.assets.api import AssetsAPI
from tenable.tenableone.inventory.software.api import SoftwareAPI


class InventoryAPI(APIEndpoint):
    @property
    def assets(self):
        # """
        # The interface object for the
        # :doc:`Tenable One Inventory Assets APIs <assets/index>`.
        # """
        return AssetsAPI(self._api)

    @property
    def software(self):
        """
        The interface object for the
        :doc:`Tenable One Inventory Software APIs <software/index>`.
        """
        return SoftwareAPI(self._api)
