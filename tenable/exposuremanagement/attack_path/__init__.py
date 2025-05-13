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
    """

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
