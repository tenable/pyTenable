from tenable.base import APIEndpoint

class FiltersAPI(APIEndpoint):
    def _filter_conversion(self, filterset):
        return filterset

    def agents_filters(self):
        '''
        `filters: agents-filters <https://cloud.tenable.com/api#/resources/filters/agents-filters>`_

        Returns:
            dict: Filter resource dictionary
        '''
        return self._filter_conversion(
            self._api.get('filters/scans/agents').json()['filters'])

    def workbench_vuln_filters(self):
        '''
        `workbenches: vulnerabilities-filters <https://cloud.tenable.com/api#/resources/workbenches/vulnerabilities-filters>`_

        Returns:
            dict: Filter resource dictionary
        '''
        return self._filter_conversion(
            self._api.get('filters/workbench/vulnerabilities').json()['filters'])

    def workbench_asset_filters(self):
        '''
        `workbenches: assets-filters <https://cloud.tenable.com/api#/resources/workbenches/assets-filters>`_

        Returns:
            dict: Filter resource dictionary
        '''
        return self._filter_conversion(
            self._api.get('filters/workbench/assets').json()['filters'])

    def scan_filters(self):
        '''
        Returns:
            dict: Filter resource dictionary
        '''
        return self._filter_conversion(
            self._api.get('filters/scans/reports').json()['filters'])