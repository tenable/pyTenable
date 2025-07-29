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
    findings/index
"""

from tenable.base.endpoint import APIEndpoint
from tenable.tenableone.inventory.assets.api import AssetsAPI
from tenable.tenableone.inventory.export.api import ExportAPI
from tenable.tenableone.inventory.findings.api import FindingsAPI
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

    @property
    def export(self):
        """
        The interface object for the
        :doc:`Tenable One Inventory Unified Export APIs <export/index>`.
        """
        return ExportAPI(self._api)

    @property
    def findings(self):
        """
        The interface object for the
        :doc:`Tenable Exposure Management Inventory Finding APIs <findings/index>`.
        """
        return FindingsAPI(self._api)
