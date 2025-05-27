"""
Tenable Exposure Management
============================

This package covers the Tenable Exposure Management.

.. autoclass:: TenableExposureManagement
    :members:


.. toctree::
    :hidden:
    :glob:

    attack_path/index
    inventory/index
    tags/index
"""

from typing import Optional

from tenable.base.platform import APIPlatform
from tenable.exposuremanagement.attack_path.api import AttackPathAPI
from tenable.exposuremanagement.exposure_view.api import ExposureViewAPI
from tenable.exposuremanagement.inventory.api import InventoryAPI
from tenable.exposuremanagement.tags.api import TagsAPI


class TenableExposureManagement(APIPlatform):
    """
    The Tenable Exposure Management object is the primary interaction
    point for users to interface with Tenable Exposure Management
    via the pyTenable library.  All the API endpoint classes that have
    been written will be grafted onto this class.

    Environment Variables:
        ``TEM_ACCESS_KEY``: API Access Key for the Tenable Exposure Management Application.

        ``TEM_SECRET_KEY``: API Secret Key for the Tenable Exposure Management Application.

        ``TEM_URL``: The Application URL.  Defaults to `https://cloud.tenable.com`.

    Examples:
        Basic Example:

        >>> from tenable.exposuremanagement import TenableExposureManagement
        >>> tenable_exposure_management = TenableExposureManagement('ACCESS_KEY', 'SECRET_KEY')

        Example with proper identification:

        >>> tenable_inventory = TenableExposureManagement('ACCESS_KEY', 'SECRET_KEY',
        >>>     vendor='Company Name',
        >>>     product='My Awesome Widget',
        >>>     build='1.0.0')
    """

    _env_base = 'TEM'
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
        :doc:`Tenable Exposure Management Attack Path APIs <attack_path/index>`.
        """
        return AttackPathAPI(self)

    @property
    def inventory(self):
        """
        The interface object for the
        :doc:`Tenable Exposure Management Inventory APIs <inventory/index>`.
        """
        return InventoryAPI(self)

    @property
    def tags(self):
        """
        The interface object for the
        :doc:`Tenable Exposure Management Tags APIs <tags/index>`.
        """
        return TagsAPI(self)

    @property
    def exposure_view(self):
        """
        The interface object for the
        :doc:`Tenable Exposure Management Exposure view APIs <exposure_view/index>`.
        """
        return ExposureViewAPI(self)
