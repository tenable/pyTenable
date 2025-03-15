"""
Tenable One
============================

This package covers the Tenable One.

.. autoclass:: TenableOne
    :members:


.. toctree::
    :hidden:
    :glob:

    assets
"""

from typing import Optional

from tenable.base.platform import APIPlatform
from .assets.api import AssetsAPI


class TenableInventory(APIPlatform):
    """
    The Tenable One object is the primary interaction
    point for users to interface with Tenable One
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

    _env_base = "TONE"
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
        :doc:`Tenable One Assets APIs <findings>`.
        """
        return AssetsAPI(self)
