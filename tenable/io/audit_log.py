'''
Audit Log
=========

The following methods allow for interaction into the Tenable Vulnerability
Management :devportal:`audit log <audit-log>` API endpoints.

Methods available on ``io.audit_log``:

.. rst-class:: hide-signature
.. autoclass:: AuditLogAPI
    :members:
'''
from typing_extensions import Literal
from typing import Tuple, Optional, Dict
from copy import copy
from .base import TIOEndpoint
from restfly.iterator import APIIterator


class AuditLogIterator(APIIterator):
    '''
    AuditLog Iterator
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
        resp = self._api.get('audit-log/v1/events', params=payload, box=True)
        self._next_token = resp.pagination.get('next')
        self.page = resp.events
        self.total = resp.pagination.total


class AuditLogAPI(TIOEndpoint):
    _box = True
    _path = 'audit-log/v1/events'

    def events(self,
               *filters: Tuple[str, str, str],
               limit: int = 1000,
               filter_type: Literal['and', 'or'] = 'and',
               sort: Optional[str] = None,
               token: Optional[str] = '0',
               return_json: bool = False
               ):
        '''
        Retrieve audit logs from Tenable Vulnerability Management.

        :devportal:`audit-log: events <audit-log-events>`

        Args:
            *filters (tuple, optional):
                Filters to allow the user to get to a specific subset of data
                within the audit log.  For a more detailed listing of what
                filters are available, please refer to the API documentation
                linked above, however some examples are as such:

                - ``('date', 'gt', '2017-07-05')``
                - ``('date', 'lt', '2017-07-07')``
                - ``('actor_id', 'match', '6000a811-8422-4096-83d3-e4d44f7d')``
                - ``('target_id', 'match', '6000a811-8422-4096-83d3-e4d447d')``

            limit (int, optional):
                The limit of how many events to return.  The API will default
                to 50 unless otherwise specified.

            filter_type (str, optional):
                if multiple filters are present, how should we combine the
                filters?  Supported values are `and` or `or`.  If left
                unspecified, the default is `and`.

            sort (str, optional):
                Should any soerting be performed on the resulting data?  The
                format is `FIELD_NAME:DIRECTION`.  For example, supplying
                `received:desc` would sort the results by the received field in
                descencing order.

            token (str, optional):
                The `next` token to request the next page.

            return_json (bool, optional):
                Should we return the JSON response instead of iterable?

        Returns:
            :obj:`AuditLogIterator`:
                List of event records

        Examples:
            >>> events = tio.audit_log.events(('date', 'gt', '2018-01-01'))
            >>> for e in events:
            ...     pprint(e)
        '''
        payload = {
            'f': [f'{f[0]}.{f[1]}:{f[2]}' for f in filters],
            'ft': filter_type,
            'limit': limit,
            'next': token,
            'sort': sort
        }
        if return_json:
            return self._get(params=payload)
        return AuditLogIterator(self._api,
                                _payload=payload,
                                _next_token=token
                                )
