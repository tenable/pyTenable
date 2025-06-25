"""
Tenable One
============================

This package covers the Tenable One.

.. autoclass:: TenableOne
    :members:


.. toctree::
    :hidden:
    :glob:

    attack_path/index
    inventory/index
    tags/index
    exposure_view/index
"""

from typing import Optional

from tenable.base.platform import APIPlatform
from tenable.tenableone.attack_path.api import AttackPathAPI
from tenable.tenableone.exposure_view.api import ExposureViewAPI
from tenable.tenableone.inventory.api import InventoryAPI
from tenable.tenableone.tags.api import TagsAPI


class TenableOne(APIPlatform):
    """
    The Tenable One object is the primary interaction
    point for users to interface with Tenable One
    via the pyTenable library.  All the API endpoint classes that have
    been written will be grafted onto this class.

    Environment Variables:
        ``TO_ACCESS_KEY``: API Access Key for the Tenable One Application.

        ``TO_SECRET_KEY``: API Secret Key for the Tenable One Application.

        ``TO_URL``: The Application URL.  Defaults to `https://cloud.tenable.com`.

    Examples:
        Basic Example:

        >>> from tenable.tenableone import TenableOne
        >>> tenable_one = TenableOne('ACCESS_KEY', 'SECRET_KEY')

        Example with proper identification:

        >>> tenable_inventory = TenableOne('ACCESS_KEY', 'SECRET_KEY',
        >>>     vendor='Company Name',
        >>>     product='My Awesome Widget',
        >>>     build='1.0.0')
    """

    _env_base = 'TO'
    _url = 'https://cloud.tenable.com'
    _box = True

    def __init__(
        self,
        access_key: Optional[str] = None,
        secret_key: Optional[str] = None,
        **kwargs,
    ):
        if access_key:
            kwargs['access_key'] = access_key
        if secret_key:
            kwargs['secret_key'] = secret_key
        super().__init__(**kwargs)

    @property
    def attack_path(self):
        """
        The interface object for the
        :doc:`Tenable One Attack Path APIs <attack_path/index>`.
        """
        return AttackPathAPI(self)

    @property
    def inventory(self):
        """
        The interface object for the
        :doc:`Tenable One Inventory APIs <inventory/index>`.
        """
        return InventoryAPI(self)

    @property
    def tags(self):
        """
        The interface object for the
        :doc:`Tenable One Tags APIs <tags/index>`.
        """
        return TagsAPI(self)

    @property
    def exposure_view(self):
        """
        The interface object for the
        :doc:`Tenable One Exposure View APIs <exposure_view/index>`.
        """
        return ExposureViewAPI(self)
