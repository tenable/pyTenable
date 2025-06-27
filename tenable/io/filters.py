"""
Filters
=======

The following methods allow for interaction into the Tenable Vulnerability Management
:devportal:`filters <filters-1>` API endpoints.

Methods available on ``tio.filters``:

.. rst-class:: hide-signature
.. autoclass:: FiltersAPI
    :members:
"""

import time
from typing import Any

from tenable.io.base import TIOEndpoint


class FiltersAPI(TIOEndpoint):
    """
    This will contain all methods related to filters
    """

    _cache = {}

    def _normalize(self, filterset: list[dict[str, Any]]) -> dict[str, Any]:
        """
        Converts the filters into an easily pars-able dictionary
        """
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
                    datablock['choices'] = [
                        str(i[key]) for i in item['control']['list']
                    ]
                elif isinstance(item['control']['list'], list):
                    datablock['choices'] = [str(i) for i in item['control']['list']]
            if 'regex' in item['control']:
                datablock['pattern'] = item['control']['regex']
            filters[item['name']] = datablock
        return filters

    def _use_cache(
        self,
        name: str,
        path: str,
        field_name: str = 'filters',
        normalize: bool = True,
        expire_age: int = 60,
    ) -> dict[str, Any]:
        """
        Leverages the filter cache and will return the results as expected.
        """
        if name not in self._cache or self._cache[name]['ts'] + expire_age <= int(
            time.time()
        ):
            self._cache[name] = {
                'ts': int(time.time()),
                'data': self._api.get(path).json()[field_name],
            }
        if normalize:
            return self._normalize(self._cache[name]['data'])

        return self._cache[name]['data']

    def access_group_asset_rules_filters(
        self,
        normalize: bool = True,
        expire_age: int = 60,
    ) -> dict[str, Any]:
        """
        Returns access group rules filters.

        :devportal:`filters: access-control-rules-filters <access-groups-list-rule-filters>`

        Args:
            normalize:
                Should the response be converted into the same structure used for the
                filter cache?
            expire_age:
                How many seconds old can the cache be before forcing a refresh?

        Returns:
            :obj:`dict`:
                Filter resource dictionary

        Examples:
            >>> filters = tio.filters.access_group_rules_filters()
        """
        return self._use_cache(
            'access_group_asset_filters',
            'access-groups/rules/filters',
            field_name='rules',
            normalize=normalize,
            expire_age=expire_age,
        )

    def access_group_filters(
        self,
        normalize: bool = True,
        expire_age: int = 60,
    ) -> dict[str, Any]:
        """
        Returns access group filters.

        :devportal:`filters: access-group-filters <access-groups-list-filters>`

        Args:
            normalize:
                Should the response be converted into the same structure used for the
                filter cache?
            expire_age:
                How many seconds old can the cache be before forcing a refresh?

        Returns:
            :obj:`dict`:
                Filter resource dictionary

        Examples:
            >>> filters = tio.filters.access_group_filters()
        """
        return self._use_cache(
            'access_groups',
            'access-groups/filters',
            normalize=normalize,
            expire_age=expire_age,
        )

    def access_group_filters_v2(self, normalize=True):
        """
        Returns access group filters v2.

        :devportal:`filters: access_group_filters_v2 <v2-access-groups-list-filters>`

        Args:
            normalize:
                Should the response be converted into the same structure used for the
                filter cache?
            expire_age:
                How many seconds old can the cache be before forcing a refresh?

        Returns:
            :obj:`dict`:
                Filter resource dictionary

        Examples:
            >>> filters = tio.filters.access_group_filters_v2()
        """
        return self._use_cache(
            'access_groups_v2', 'v2/access-groups/filters', normalize=normalize
        )

    def access_group_asset_rules_filters_v2(
        self,
        normalize: bool = True,
        expire_age: int = 60,
    ) -> dict[str, Any]:
        """
        Returns access group rules filters v2.

        :devportal:`filters: access_group_asset_rules_filters_v2 <v2-access-groups-list-rule-filters>`

        Args:
            normalize:
                Should the response be converted into the same structure used for the
                filter cache?
            expire_age:
                How many seconds old can the cache be before forcing a refresh?

        Returns:
            :obj:`dict`:
                Filter resource dictionary

        Examples:
            >>> filters = tio.filters.access_group_rules_filters_v2()
        """
        return self._use_cache(
            'access_group_asset_filters_v2',
            'v2/access-groups/rules/filters',
            field_name='rules',
            normalize=normalize,
            expire_age=expire_age,
        )

    def agents_filters(
        self,
        normalize: bool = True,
        expire_age: int = 60,
    ) -> dict[str, Any]:
        """
        Returns agent filters.

        :devportal:`filters: agents-filters <filters-agents-filters>`

        Args:
            normalize:
                Should the response be converted into the same structure used for the
                filter cache?
            expire_age:
                How many seconds old can the cache be before forcing a refresh?

        Returns:
            :obj:`dict`:
                Filter resource dictionary

        Examples:
            >>> filters = tio.filters.agents_filters()
        """
        return self._use_cache(
            'agents',
            'filters/scans/agents',
            normalize=normalize,
            expire_age=expire_age,
        )

    def workbench_vuln_filters(
        self,
        normalize: bool = True,
        expire_age: int = 60,
    ) -> dict[str, Any]:
        """
        Returns the vulnerability workbench filters

        :devportal:`workbenches: vulnerabilities-filters <workbenches-vulnerabilities-filters>`

        Args:
            normalize:
                Should the response be converted into the same structure used for the
                filter cache?
            expire_age:
                How many seconds old can the cache be before forcing a refresh?

        Returns:
            :obj:`dict`:
                Filter resource dictionary

        Examples:
            >>> filters = tio.filters.workbench_vuln_filters()
        """
        return self._use_cache(
            'vulns',
            'filters/workbenches/vulnerabilities',
            normalize=normalize,
            expire_age=expire_age,
        )

    def workbench_asset_filters(
        self,
        normalize: bool = True,
        expire_age: int = 60,
    ) -> dict[str, Any]:
        """
        Returns the asset workbench filters.

        :devportal:`workbenches: assets-filters <filters-assets-filter>`

        Args:
            normalize:
                Should the response be converted into the same structure used for the
                filter cache?
            expire_age:
                How many seconds old can the cache be before forcing a refresh?

        Returns:
            :obj:`dict`:
                Filter resource dictionary

        Examples:
            >>> filters = tio.filters.workbench_asset_filters()
        """
        return self._use_cache(
            'asset',
            'filters/workbenches/assets',
            normalize=normalize,
            expire_age=expire_age,
        )

    def scan_filters(
        self,
        normalize: bool = True,
        expire_age: int = 60,
    ) -> dict[str, Any]:
        """
        Returns the individual scan filters.

        Args:
            normalize:
                Should the response be converted into the same structure used for the
                filter cache?
            expire_age:
                How many seconds old can the cache be before forcing a refresh?

        Returns:
            :obj:`dict`:
                Filter resource dictionary

        Examples:
            >>> filters = tio.filters.scan_filters()
        """
        return self._use_cache('scan', 'filters/scans/reports', normalize=normalize)

    def credentials_filters(
        self,
        normalize: bool = True,
        expire_age: int = 60,
    ) -> dict[str, Any]:
        """
        Returns the individual scan filters.

        :devportal:`filters: credentials <credentials-filters>`

        Args:
            normalize:
                Should the response be converted into the same structure used for the
                filter cache?
            expire_age:
                How many seconds old can the cache be before forcing a refresh?

        Returns:
            :obj:`dict`:
                Filter resource dictionary

        Examples:
            >>> filters = tio.filters.scan_filters()
        """
        return self._use_cache(
            'scan',
            'filters/credentials',
            normalize=normalize,
            expire_age=expire_age,
        )

    def networks_filters(self) -> dict[str, Any]:
        """
        Returns the networks filters.

        Returns:
            :obj:`dict`:
                Filter resource dictionary

        Examples:
            >>> filters = tio.filters.network_filters()
        """
        return {
            'name': {
                'operators': ['eq', 'neq', 'match'],
                'choices': None,
                'pattern': None,
            }
        }

    def asset_tag_filters(
        self,
        normalize: bool = True,
        expire_age: int = 60,
    ) -> dict[str, Any]:
        """
        Returns a list of filters that you can use to create the rules for applying dynamic tags.

        :devportal:`tag: list asset tag filters <tags-list-asset-filters>`

        Args:
            normalize:
                Should the response be converted into the same structure used for the
                filter cache?
            expire_age:
                How many seconds old can the cache be before forcing a refresh?

        Returns:
            :obj:`dict`:
                Filter resource dictionary

        Examples:
            >>> tio.filters.asset_tag_filters()
        """
        return self._use_cache(
            'tags',
            'tags/assets/filters',
            normalize=normalize,
            expire_age=expire_age,
        )
