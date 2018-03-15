from tenable.base import APIEndpoint

class FiltersAPI(APIEndpoint):
    def agents_filters(self):
        '''
        `filters: agents-filters <https://cloud.tenable.com/api#/resources/filters/agents-filters>`_

        Returns:
            dict: Filter resource dictionary
        '''
        return self._api.get('filters/scans/agents').json()['filters']