"""
Tenable Inventory
============================

This package covers the Tenable Inventory.

.. autoclass:: TenableInventory
    :members:


.. toctree::
    :hidden:
    :glob:

    assets
"""

from typing import Optional

from tenable.base.platform import APIPlatform
from .assets.api import AssetsAPI
from .software.api import SoftwareAPI


class TenableInventory(APIPlatform):
    """
    The Tenable Inventory object is the primary interaction
    point for users to interface with Tenable Inventory
    via the pyTenable library.  All the API endpoint classes that have
     been written will be grafted onto this class.

    Examples:
        Basic Example:

        >>> from tenable.inventory import TenableInventory
        >>> tenable_inventory = TenableInventory('ACCESS_KEY', 'SECRET_KEY')

        Example with proper identification:

        >>> tenable_inventory = TenableInventory('ACCESS_KEY', 'SECRET_KEY',
        >>>     vendor='Company Name',
        >>>     product='My Awesome Widget',
        >>>     build='1.0.0')
    """

    _env_base = "TENABLE_INVENTORY"
    _url = "https://cloud.tenable.com"
    _box = True

    def __init__(
            self,
            access_key: Optional[str] = None,
            secret_key: Optional[str] = None,
            **kwargs
    ):
        if access_key:
            kwargs["access_key"] = access_key
        if secret_key:
            kwargs["secret_key"] = secret_key
        super().__init__(**kwargs)

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
