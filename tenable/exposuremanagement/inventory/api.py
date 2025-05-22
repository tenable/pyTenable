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

    assets/index
    software/index
"""

from tenable.base.endpoint import APIEndpoint
from tenable.exposuremanagement.inventory.assets.api import AssetsAPI
from tenable.exposuremanagement.inventory.software.api import SoftwareAPI
from tenable.exposuremanagement.inventory.findings.api import FindingsAPI


class InventoryAPI(APIEndpoint):
    @property
    def assets(self):
        """
        The interface object for the
        :doc:`Tenable Exposure Management Inventory Assets APIs <assets/index>`.
        """
        return AssetsAPI(self._api)

    @property
    def software(self):
        """
        The interface object for the
        :doc:`Tenable Exposure Management Inventory Software APIs <software/index>`.
        """
        return SoftwareAPI(self._api)

    @property
    def findings(self):
        """
        The interface object for the
        :doc:`Tenable Exposure Management Inventory Finding APIs <findings/index>`.
        """
        return FindingsAPI(self._api)
