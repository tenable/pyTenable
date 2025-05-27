from restfly import APIEndpoint

from tenable.exposuremanagement.exposure_view.cards.api import CardsAPI


class ExposureViewAPI(APIEndpoint):
    @property
    def cards(self):
        """
        The interface object for the
        :doc:`Tenable Exposure Management Exposure view Cards APIs <cards/index>`.
        """
        return CardsAPI(self._api)
