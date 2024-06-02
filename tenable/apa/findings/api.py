'''
Findings
=============

Methods described in this section relate to the findings API.
These methods can be accessed at ``TenableAPA.findings``.

.. rst-class:: hide-signature
.. autoclass:: FindingsAPI
    :members:
'''
from copy import copy
from typing import List, Dict, Optional

from restfly import APIIterator

from tenable.apa.findings.schema import FindingSchema, FindingPageSchema
from tenable.base.endpoint import APIEndpoint


class FindingIterator(APIIterator):
    '''
    Finding Iterator
    '''
    _next_token: str = None
    _payload: Dict

    def _get_page(self) -> None:
        '''
        Request the next page of data
        '''
        payload = copy(self._payload)
        print(self._next_token)
        payload['next'] = self._next_token

        if self.num_pages >= 1 and self._next_token is None:
            raise StopIteration()
        resp = self._api.get('apa/findings-api/v1/findings', params=payload, box=True)
        self._next_token = resp.get('next')
        self.page = resp.data
        self.total = resp.total


class FindingsAPI(APIEndpoint):
    _schema = FindingPageSchema()

    def list(self,
             page_number: int,
             next: str,
             limit: int = 50,
             filter: Optional[dict],
             sort_filed: Optional[]
             return_iterator=True, **kwargs) -> List[Dict]:
        '''
        Retrieve findings

        Args:
            procedure_name (str):
                The finding identifier.
            resource_type (str):
                The type of resource. possible values are ``infrastructure``,
                ``directory``, ``hostname``, ``ip``.
            resource_value (str):
                The value of resource.
            attack_type_ids (optional, list[str]):
                The list of attack type ids.
            date_end (optional, str):
                The date before which the attack occurence should be
                considered.
            date_start (optional, str):
                The date after which the attack occurence should be
                considered.
            include_closed (optional, str):
                Whether closed attacks should be included?
                Accepted values are ``true`` or ``false``
            limit (optional, str):
                The number of records user wants to return.
            order (optional, str):
                The order of response. Accepted values are
                ``asc`` or ``desc``.
            search (optional, str):
                Search a value in response.

        Returns:
            list:
                The list of attacks objects

        Examples:
            >>> tad.findings.list(
            ...     profile_id='1',
            ...     resource_type='infrastructure',
            ...     resource_value='1',
            ...     attack_type_ids=[1, 2],
            ...     include_closed='false',
            ...     limit='10',
            ...     order='asc',
            ...     search='value',
            ...     date_end='2022-12-31T18:30:00.000Z',
            ...     date_start='2021-12-31T18:30:00.000Z'
            ...     )
        '''
        params = self._schema.dump(self._schema.load(kwargs))
        return self._schema.load(
            self._api.get(f'apa/findings-api/v1/findnigs', params=params),
            many=True, partial=True)
