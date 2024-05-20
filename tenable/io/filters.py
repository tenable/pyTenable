'''
Filters
=======

The following methods allow for interaction into the Tenable Vulnerability Management
:devportal:`filters <filters-1>` API endpoints.

Methods available on ``tio.filters``:

.. rst-class:: hide-signature
.. autoclass:: FiltersAPI
    :members:
'''
from tenable.io.base import TIOEndpoint

class FiltersAPI(TIOEndpoint):
    '''
    This will contain all methods related to filters
    '''
    _cache = dict()

    def _normalize(self, filterset):
        '''
        Converts the filters into an easily pars-able dictionary
        '''
        filters = dict()
        for item in filterset:
            datablock = {
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
                    datablock['choices'] = [str(i[key]) for i in item['control']['list']]
                elif isinstance(item['control']['list'], list):
                    datablock['choices'] = [str(i) for i in item['control']['list']]
            if 'regex' in item['control']:
                datablock['pattern'] = item['control']['regex']
            filters[item['name']] = datablock
        return filters

    def _use_cache(self, name, path, field_name='filters', normalize=True):
        '''
        Leverages the filter cache and will return the results as expected.
        '''
        if name not in self._cache:
            self._cache[name] = self._api.get(path).json()[field_name]

        if normalize:
            return self._normalize(self._cache[name])

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

    def access_group_filters_v2(self, normalize=True):
        '''
        Returns access group filters v2.

        :devportal:`filters: access_group_filters_v2 <v2-access-groups-list-filters>`

        Returns:
            :obj:`dict`:
                Filter resource dictionary

        Examples:
            >>> filters = tio.filters.access_group_filters_v2()
        '''
        return self._use_cache('access_groups_v2',
            'v2/access-groups/filters', normalize=normalize)

    def access_group_asset_rules_filters_v2(self, normalize=True):
        '''
        Returns access group rules filters v2.

        :devportal:`filters: access_group_asset_rules_filters_v2 <v2-access-groups-list-rule-filters>`

        Returns:
            :obj:`dict`:
                Filter resource dictionary

        Examples:
            >>> filters = tio.filters.access_group_rules_filters_v2()
        '''
        return self._use_cache('access_group_asset_filters_v2',
            'v2/access-groups/rules/filters',
            field_name='rules', normalize=normalize)

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

    def asset_tag_filters(self):
        '''
        Returns a list of filters that you can use to create the rules for applying dynamic tags.

        :devportal:`tag: list asset tag filters <tags-list-asset-filters>`

        Returns:
            :obj:`dict`:
                Filter resource dictionary

        Examples:
            >>> tio.filters.asset_tag_filters()
        '''
        return self._use_cache('tags', 'tags/assets/filters')
