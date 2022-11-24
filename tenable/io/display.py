from tenable.base.endpoint import APIEndpoint


class DisplayAPI(APIEndpoint):
    """
    This will contain methods related to display
    """
    def get_licensed(self):
        """
        Returns a list of licenced scanned assets.

        :devportal:`assets: list-assets <assets-list-assets>`

        Returns:
            :obj:`list`:
                List of scanned licensed asset records.

        Examples:
            >>> tio.display.get_licensed()
        """

        return self._api.get('workbenches/asset-stats?date_range=90'
                             '&filter.0.filter=is_licensed'
                             '&filter.0.quality=eq'
                             '&filter.0.value=true').json()['scanned']
