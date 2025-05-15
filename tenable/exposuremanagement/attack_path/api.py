"""
Attack Path
===========

The following sub-package allows for interaction with the Tenable Exposure Management
Attack Path APIs.

.. rst-class:: hide-signature
.. autoclass:: AttackPathAPI
    :members:

.. toctree::
    :hidden:
    :glob:

    findings/index
    vectors/index
"""

from tenable.base.endpoint import APIEndpoint
from tenable.exposuremanagement.attack_path.findings.api import FindingsAPI
from tenable.exposuremanagement.attack_path.vectors.api import VectorsAPI


class AttackPathAPI(APIEndpoint):
    @property
    def findings(self):
        """
        The interface object for the
        :doc:`Tenable Exposure Management Attack Path Findings APIs <findings/index>`.
        """
        return FindingsAPI(self._api)

    @property
    def vectors(self):
        """
        The interface object for the
        :doc:`Tenable Exposure Management Attack Path Vectors APIs <vectors/index>`.
        """
        return VectorsAPI(self._api)
