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

    assets/index
    software/index
    export/index
"""

from tenable.base.endpoint import APIEndpoint
from tenable.tenableone.inventory.assets.api import AssetsAPI
from tenable.tenableone.inventory.software.api import SoftwareAPI
from tenable.tenableone.inventory.export.api import ExportAPI


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

    @property
    def export(self):
        """
        The interface object for the
        :doc:`Tenable One Inventory Unified Export APIs <export>`.
        """
        return ExportAPI(self._api)
