"""
Tenable Inventory
============================

This package covers the Inventory API.
These methods can be accessed at ``TenableExposureManagement.inventory``.

.. autoclass:: TenableInventory
    :members:


.. toctree::
    :hidden:
    :glob:

    assets
"""

from tenable.base.platform import APIPlatform
from .assets.api import AssetsAPI
from .software.api import SoftwareAPI


class InventoryAPI(APIPlatform):
    """
    The Tenable Inventory object is the primary interaction
    point for users to interface with Tenable Inventory
    via the pyTenable library.  All the API endpoint classes that have
     been written will be grafted onto this class.

    Examples:
        Basic Example:
        >>> tenable_inventory = tenable_exposure_management.inventory
        >>> tenable_inventory.assets.list()
    """

    @property
    def assets(self):
        """
        The interface object for the
        :doc:`Tenable Inventory Assets APIs <findings>`.
        """
        return AssetsAPI(self)

    @property
    def software(self):
        """
        The interface object for the
        :doc:`Tenable Inventory Software APIs <findings>`.
        """
        return SoftwareAPI(self)
