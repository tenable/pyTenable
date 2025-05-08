"""
Tenable Attack Path Analysis
============================

This package covers the Tenable APA.

.. autoclass:: TenableAPA
    :members:


.. toctree::
    :hidden:
    :glob:

    findings
    vectors
"""

from typing import Optional

from tenable.base.platform import APIPlatform
from .findings.api import FindingsAPI
from .vectors.api import VectorsAPI


class TenableAPA(APIPlatform):
    """
    The Tenable Attack Path Analysis object is the primary interaction
    point for users to interface with Tenable Attack Path Analysis
    via the pyTenable library.  All the API endpoint classes that have
     been written will be grafted onto this class.

    Examples:
        Basic Example:

        >>> from tenable.apa import TenableAPA
        >>> tapa = TenableAPA('ACCESS_KEY', 'SECRET_KEY')

        Example with proper identification:

        >>> tapa = TenableAPA('ACCESS_KEY', 'SECRET_KEY',
        >>>     vendor='Company Name',
        >>>     product='My Awesome Widget',
        >>>     build='1.0.0')
    """

    _env_base = "TAPA"
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
    def findings(self):
        """
        The interface object for the
        :doc:`Tenable Attack Path Analysis APA Findings APIs <findings>`.
        """
        return FindingsAPI(self)

    @property
    def vectors(self):
        """
        The interface object for the
        :doc:`Tenable Attack Path Analysis APA Findings APIs <findings>`.
        """
        return VectorsAPI(self)
