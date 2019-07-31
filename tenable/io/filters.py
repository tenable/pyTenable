'''
filters
=======

The following methods allow for interaction into the Tenable.io
:devportal:`filters <filters-1>` API endpoints.

Methods available on ``tio.filters``:

.. rst-class:: hide-signature
.. autoclass:: FiltersAPI

    .. automethod:: agents_filters
    .. automethod:: scan_filters
    .. automethod:: networks_filters
    .. automethod:: workbench_asset_filters
    .. automethod:: workbench_vuln_filters
'''
from .base import TIOEndpoint

class FiltersAPI(TIOEndpoint):
    _cache = dict()

    def _normalize(self, filterset):
        '''
        Converts the filters into an easily pars-able dictionary
        '''
        filters = dict()
        for item in filterset:
            f = {
                'operators': item['operators'],
                'choices': None,
                'pattern': None,
            }

            # If there is a list of choices available, then we need to parse
            # them out and only pull back the usable values as a list
            if 'list' in item['control']:
                # There is a lack of consistency here.  In some cases the "list"
                # is a list of dictionary items, and in other cases the "list"
                # is a list of string values.
                if isinstance(item['control']['list'][0], dict):
                    key = 'value' if 'value' in item['control']['list'][0] else 'id'
                    f['choices'] = [str(i[key]) for i in item['control']['list']]
                elif isinstance(item['control']['list'], list):
                    f['choices'] = [str(i) for i in item['control']['list']]
            if 'regex' in item['control']:
                f['pattern'] = item['control']['regex']
            filters[item['name']] = f
        return filters

    def _use_cache(self, name, path, field_name='filters', normalize=True):
        '''
        Leverages the filter cache and will return the results as expected.
        '''
        if name not in self._cache:
            self._cache[name] = self._api.get(path).json()[field_name]

        if normalize:
            return self._normalize(self._cache[name])
        else:
            return self._cache[name]

    def access_group_asset_rules_filters(self, normalize=True):
        '''
        Returns access group rules filters.

        :devportal:`filters: access-control-rules-filters <access-groups-list-rule-filters>`

        Returns:
            :obj:`dict`:
                Filter resource dictionary

        Examples:
            >>> filters = tio.filters.access_group_rules_filters()
        '''
        return self._use_cache('access_group_asset_filters',
            'access-groups/rules/filters',
            field_name='rules', normalize=normalize)

    def access_group_filters(self, normalize=True):
        '''
        Returns access group filters.

        :devportal:`filters: access-group-filters <access-groups-list-filters>`

        Returns:
            :obj:`dict`:
                Filter resource dictionary

        Examples:
            >>> filters = tio.filters.access_group_filters()
        '''
        return self._use_cache('access_groups',
            'access-groups/filters', normalize=normalize)

    def agents_filters(self, normalize=True):
        '''
        Returns agent filters.

        :devportal:`filters: agents-filters <filters-agents-filters>`

        Returns:
            :obj:`dict`:
                Filter resource dictionary

        Examples:
            >>> filters = tio.filters.agents_filters()
        '''
        return self._use_cache('agents', 'filters/scans/agents',
                               normalize=normalize)

    def workbench_vuln_filters(self, normalize=True):
        '''
        Returns the vulnerability workbench filters

        :devportal:`workbenches: vulnerabilities-filters <workbenches-vulnerabilities-filters>`

        Returns:
            :obj:`dict`:
                Filter resource dictionary

        Examples:
            >>> filters = tio.filters.workbench_vuln_filters()
        '''
        return self._use_cache('vulns',
            'filters/workbenches/vulnerabilities', normalize=normalize)

    def workbench_asset_filters(self, normalize=True):
        '''
        Returns the asset workbench filters.

        :devportal:`workbenches: assets-filters <filters-assets-filter>`

        Returns:
            :obj:`dict`:
                Filter resource dictionary

        Examples:
            >>> filters = tio.filters.workbench_asset_filters()
        '''
        return self._use_cache('asset', 'filters/workbenches/assets',
                               normalize=normalize)

    def scan_filters(self, normalize=True):
        '''
        Returns the individual scan filters.

        Returns:
            :obj:`dict`:
                Filter resource dictionary

        Examples:
            >>> filters = tio.filters.scan_filters()
        '''
        return self._use_cache('scan', 'filters/scans/reports',
                               normalize=normalize)

    def credentials_filters(self, normalize=True):
        '''
        Returns the individual scan filters.

        :devportal:`filters: credentials <credentials-filters>`

        Returns:
            :obj:`dict`:
                Filter resource dictionary

        Examples:
            >>> filters = tio.filters.scan_filters()
        '''
        return self._use_cache('scan', 'filters/credentials',
                               normalize=normalize)

    def networks_filters(self):
        '''
        Returns the networks filters.

        Returns:
            :obj:`dict`:
                Filter resource dictionary

        Examples:
            >>> filters = tio.filters.network_filters()
        '''
        return {'name': {
            'operators': ['eq', 'neq', 'match'],
            'choices': None,
            'pattern': None
        }}
