"""
Exposure View
=============

The following sub-package allows for interaction with the Tenable Exposure Management
Exposure View APIs.

.. rst-class:: hide-signature
.. autoclass:: ExposureViewAPI
    :members:

.. toctree::
    :hidden:
    :glob:

    cards/index
"""

from restfly import APIEndpoint

from tenable.tenableone.exposure_view.cards.api import CardsAPI


class ExposureViewAPI(APIEndpoint):
    @property
    def cards(self):
        """
        The interface object for the
        :doc:`Tenable Exposure Management Exposure view Cards APIs <cards/index>`.
        """
        return CardsAPI(self._api)
