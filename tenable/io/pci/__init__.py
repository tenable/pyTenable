"""
PCI-ASV
=======

The following methods allow for interaction into the TVM PCI-ASV API endpoints.

Methods available on ``tio.pci``:

.. rst-class:: hide-signature
.. autoclass:: PCIASVAPI
    :members:

"""

from typing import Any, Literal, Type

from ..base import TIOEndpoint
from .attestations import AttestationsAPI
from .scans import ScansAPI


class PCIASVAPI(TIOEndpoint):
    @property
    def attestations(self) -> AttestationsAPI:
        """
        The interface for :doc:`TVM PCI-ASV Attestations APIs <attestations>`.
        """
        return AttestationsAPI(self._api)

    @property
    def scans(self) -> ScansAPI:
        """
        The interface for :doc:`TVM PCI-ASV Scans APIs <scans>`.
        """
        return ScansAPI(self._api)
