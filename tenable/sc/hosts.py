'''
Hosts
=====

The following methods allow for interaction with the Tenable Security Center
:sc-api:`Hosts <Hosts.htm>` API.  These items are typically seen under the
**Hosts** section of Tenable Security Center.

Methods available on ``sc.hosts``:

.. rst-class:: hide-signature
.. autoclass:: HostsAPI
    :members:
'''
from typing import List, Union, Dict, Optional, Tuple
from .base import SCEndpoint, SCResultsIterator
from tenable.errors import UnexpectedValueError


class HostsResultsIterator(SCResultsIterator):
    pass


class HostsAPI(SCEndpoint):
    _path = 'hosts'
    _box = True

    def list(self,
             fields: List[str],
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
        params = {
            'fields': ','.join(fields),
            'limit': limit,
            'startOffset': offset,
            'endOffset': limit + offset,
            'pagination': str(pagination).lower(),
        }
        if return_json:
            return self._get(params=params).response
        return HostsResultsIterator(self._api,
                                    _resource='hosts'
                                    _params=params,
                                    _limit=limit,
                                    _offset=offset
                                    _pages_total=pages
                                    )

    def search(self,
               filters: List[Tuple[str, str, str]],
               fields: List[str],
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
        params = {
            'fields': ','.join(fields),
            'limit': limit,
            'startOffset': offset,
            'endOffset': limit + offset,
            'pagination': str(pagination).lower(),
        }
        if return_json:
            return self._get(params=params).response
        return HostsResultsIterator(self._api,
                                    _resource='hosts'
                                    _params=params,
                                    _limit=limit,
                                    _offset=offset
                                    _pages_total=pages
                                    )
