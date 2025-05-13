"""
Inventory
=========

The following sub-package allows for interaction with the Tenable Exposure Management
Inventory APIs.

.. rst-class:: hide-signature
.. autoclass:: InventoryAPI
    :members:

.. toctree::
    :hidden:
    :glob:

    assets
    software
"""
from tenable.base.endpoint import APIEndpoint

from tenable.exposure_management.inventory.assets.api import AssetsAPI
from tenable.exposure_management.inventory.software.api import SoftwareAPI


class InventoryAPI(APIEndpoint):
    @property
    def assets(self):
        """
        The interface object for the
        :doc:`Tenable Exposure Management Inventory Assets APIs <assets>`.
        """
        return AssetsAPI(self._api)

    @property
    def software(self):
        """
        The interface object for the
        :doc:`Tenable Exposure Management Inventory Software APIs <software>`.
        """
        return SoftwareAPI(self._api)
