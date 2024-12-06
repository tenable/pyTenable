"""
Hosts
=====

The following methods allow for interaction with the Tenable Security Center
:sc-api:`Hosts <Hosts.htm>` API.  These items are typically seen under the
**Hosts** section of Tenable Security Center.

Methods available on ``sc.hosts``:

.. rst-class:: hide-signature
.. autoclass:: HostsAPI
    :members:
"""

from typing import Dict, List, Literal, Optional, Tuple, Union

from .base import SCEndpoint, SCResultsIterator


class HostsResultsIterator(SCResultsIterator):
    pass


class HostsAPI(SCEndpoint):
    _path = 'hosts'
    _box = True

    def list(
        self,
        fields: Optional[List[str]] = None,
        limit: int = 10000,
        offset: int = 0,
        pages: Optional[int] = None,
        pagination: bool = True,
        return_json: bool = False,
    ) -> Union[HostsResultsIterator, Dict]:
        """
        Retreive the list of hosts from the system.

        Args:
            fields (list[str], optional):
                What fields should be returned in the response.
            limit (int, 1000):
                How many hosts should be returned?
            offset (int, 0):
                At what index should
            pages (int, optional):
                The maximum number of pages to return for the iterator.
            pagination (bool, False):
                Should pagination be used?
            return_json (bool, False):
                Should we return the json response instead of an iterator?

        Response:
            The response will be either the HostResultsIterator to handle
            pagination of the data (preferred) or the raw response from the
            api (if return_json is set to `True`).

        Examples:

            >>> for host in sc.hosts.list():
            ...     print(host)
        """
        if not fields:
            fields = [
                'id',
                'uuid',
                'tenableUUID',
                'name',
                'ipAddress',
                'os',
                'firstSeen',
                'lastSeen',
                'macAddress',
                'source',
                'repID',
                'netBios',
                'netBiosWorkgroup',
                'createdTime',
                'modifiedTime',
                'acr',
                'aes',
            ]
        params = {
            'fields': ','.join(fields),
            'limit': limit,
            'startOffset': offset,
            'endOffset': limit + offset,
            'pagination': str(pagination).lower(),
        }
        if return_json:
            return self._get(params=params).response
        return HostsResultsIterator(
            self._api,
            _resource='hosts',
            _query=params,
            _limit=limit,
            _offset=offset,
            _pages_total=pages,
        )

    def search(
        self,
        *filters: Tuple[str, str, str],
        filter_type: Literal['and', 'or'] = 'and',
        fields: Optional[List[str]] = None,
        limit: int = 10000,
        offset: int = 0,
        pages: Optional[int] = None,
        pagination: bool = True,
        return_json: bool = False,
    ) -> Union[HostsResultsIterator, Dict]:
        """
        Retreive the list of hosts from the system.

        Args:
            filters (list[tuple[str, str, str]], optional):
                List of search filter tuples.
            filter_type (Literal['and', 'or'], optional):
                The filtering boolean logic to use for multiple filters.  If left
                unspecified it defaults to `and`.
            fields (list[str], optional):
                What fields should be returned in the response.
            limit (int, 1000):
                How many hosts should be returned?
            offset (int, 0):
                At what index should
            pages (int, optional):
                The maximum number of pages to return for the iterator.
            pagination (bool, False):
                Should pagination be used?
            return_json (bool, False):
                Should we return the json response instead of an iterator?

        Response:
            The response will be either the HostResultsIterator to handle
            pagination of the data (preferred) or the raw response from the
            api (if return_json is set to `True`).

        Examples:

            >>> for host in sc.hosts.search(filters=[('ip', 'eq', '1.2.3.4')]):
            ...     print(host)
        """
        if not fields:
            fields = [
                'id',
                'uuid',
                'tenableUUID',
                'name',
                'ipAddress',
                'os',
                'firstSeen',
                'lastSeen',
                'macAddress',
                'source',
                'repID',
                'netBios',
                'netBiosWorkgroup',
                'createdTime',
                'modifiedTime',
                'acr',
                'aes',
            ]

        params = {
            'fields': ','.join(fields),
            'limit': limit,
            'startOffset': offset,
            'endOffset': limit + offset,
            'pagination': str(pagination).lower(),
        }
        payload = {
            'filters': {
                filter_type: [
                    {'property': p, 'operator': o, 'value': v} for p, o, v in filters
                ]
            }
        }
        if return_json:
            return self._post('search', params=params, json=payload).response
        return HostsResultsIterator(
            self._api,
            _method='POST',
            _resource='hosts/search',
            _body=payload,
            _query=params,
            _limit=limit,
            _offset=offset,
            _pages_total=pages,
        )

    def update_acr(
        self,
        host_uuid: str,
        reasoning: Optional[List[int]] = None,
        score: Optional[int] = None,
        notes: Optional[str] = None,
        overwritten: bool = True,
    ) -> Dict:
        """
        Override the Asset Criticality Rating (ACR) score and the reasons for the
        specified Host

        Args:
            host_uuid (str): The Host UUID to modify
            reasonings (list[int], optional):
                The list of reasoning objects noting why the score was changed
            score (int, optional):
                The updated ACR score
            notes (str, optional):
                Notes detailing why the score was changed
            overwritten (bool):
                Should we use the overwritten score or the default one?

        Returns:
            The updated host object.

        Example:
            >>> sc.host.update_acr(
            ...     host_uuid='12345678-1234-1234-123456789012',
            ...     score=7,
            ...     reasonings=[4],
            ...     notes='Why we changed this score...',
            ... )
        """
        payload = {'overwritten': str(overwritten).lower()}
        if reasoning:
            payload['reasoning'] = [{'id': x} for x in reasoning]
        if score:
            payload['overwrittenScore'] = score
        if notes:
            payload['notes'] = notes
        return self._patch(f'{host_uuid}/acr', json=payload).response
