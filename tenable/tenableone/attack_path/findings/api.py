"""
Findings
========

Methods described in this section relate to the findings API.
These methods can be accessed at ``TenableOne.attack_path.findings``.

.. rst-class:: hide-signature
.. autoclass:: FindingsAPI
    :members:

"""

import json
from copy import copy
from typing import Dict, Optional, Union

from pydantic import BaseModel

from tenable.base._restfly_v1 import APIIterator

from tenable.base.endpoint import APIEndpoint
from tenable.tenableone.attack_path.findings.schema import (
    FindingsPageSchema,
    TopAttackTechniquesSearchResponse,
)


class FindingIterator(APIIterator):
    """
    Finding Iterator
    """

    _next_token: str = None
    _payload: Dict

    def _get_page(self) -> None:
        """
        Request the next page of data
        """
        payload = copy(self._payload)
        payload['next'] = self._next_token

        resp = self._api.get('api/v1/t1/apa/findings', params=payload, box=True)
        self._next_token = resp.get('next')
        self.page = resp.data
        self.total = resp.total


class FindingsAPI(APIEndpoint):
    _schema = FindingsPageSchema

    def list(
        self,
        page_number: Optional[int] = None,
        next_token: Optional[str] = None,
        limit: int = 50,
        filter: Optional[Union[dict, str]] = None,
        sort_filed: Optional[str] = None,
        sort_order: Optional[str] = None,
        return_iterator=True,
    ) -> Union[FindingIterator, FindingsPageSchema]:
        """
        Retrieve findings

        Args:
            page_number (optional, int):
                For offset-based pagination, the requested page to retrieve.
                If this parameter is omitted,
                Tenable uses the default value of 1.

            next_token (optional, str):
                For cusrsor-based pagination,
                the cursor position for the next page.
                For the initial request, don't populate.
                For subsequent requests, set this parameter to the value found
                in the next property of the previous response.
                When getting null without specify a page number
                it means there are no more pages.

            limit (optional, int):
                The number of records to retrieve.
                If this parameter is omitted,
                Tenable uses the default value of 50.
                The maximum number of events that can be retrieved is 10,000.
                For example: limit=10000.

            filter (optional, dict | str):
                A document as defined by Tenable APA online documentation.
                A dict is serialized to a JSON string before it is sent, and a
                string is passed through as-is.
                Filters to allow the user to get
                to a specific subset of Findings.
                For a more detailed listing of what filters are available,
                please refer to the API documentation
                linked above, however some examples are as such:

                - ``{"operator":"==", "key":"state", "value":"open"}``
                - ``{"operator":">", "key":"last_updated_at", "value":"2024-05-30T12:28:11.528118"}``

            sort_filed (optional, str):
                The field you want to use to sort the results by.
                Accepted values are ``last_updated_at``, ``state``,
                ``vectorCount``, ``status``, ``name``,
                ``procedureName``, ``priority``, and ``mitre_id``.

            sort_order (optional, str):
                The sort order
                Accepted values are ``desc`` or ``acs``

            return_iterator (bool, optional):
                Should we return the response instead of iterable?


        Returns:
            :obj:`FindingIterator`:
                List of findings records

         Examples:
            >>> findings = tapa.findings.list()
            >>> for f in findings:
            ...     pprint(f)

         Examples:
            >>> tapa.findings.list(
            ...     limit='10',
            ...     sort_filed='last_updated_at',
            ...     sort_order='desc',
            ...     filter={'operator': '==', 'key': 'state', 'value': 'open'},
            ...     return_iterator=False
            ...     )
        """

        payload = {
            'page_number': page_number,
            'next': next_token,
            'limit': limit,
            'filter': json.dumps(filter) if isinstance(filter, dict) else filter,
            'sort_filed': sort_filed,
            'sort_order': sort_order,
        }
        if return_iterator:
            return FindingIterator(self._api, _payload=payload, _next_token=next_token)
        return self._schema(**self._get(path='api/v1/t1/apa/findings', params=payload))

    def top_attack_techniques_search(
        self,
        *,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        sort: Optional[str] = None,
        filter: Optional[Union[Dict, BaseModel]] = None,
        exclude_resolved: Optional[bool] = None,
    ) -> TopAttackTechniquesSearchResponse:
        """
        Search the top attack techniques in your organization.

        :devportal:`attack-path: search attack techniques <apa-attack-techniques-search>`

        This is the replacement for the deprecated ``list()`` endpoint.  By default, the
        API excludes resolved techniques: those with a status of ``done`` or
        ``accepted``, or a state of ``archive``.

        Args:
            limit (optional, int):
                The number of techniques to return, from 100 to 10000.  If omitted,
                the API returns 1000.
            offset (optional, int):
                The number of records to skip, for paging through results with
                ``limit``.  If omitted, the API starts at the first record.
            sort (optional, str):
                The sort order, in the format ``property:direction``, such as
                ``priority:desc``.  The API accepts the properties
                ``last_updated_at``, ``priority``, ``mitre_id``, ``name``,
                ``procedure_name``, ``status``, ``state``, ``vector_count`` and
                ``external_id``.
            filter (optional, dict):
                The filter, sent as the JSON request body.  A condition has the
                form ``{"property": ..., "operator": ..., "value": ...}``, using
                the operators ``eq``, ``neq``, ``gt``, ``gte``, ``lt``, ``lte``
                or ``contains``.  Conditions are combined with
                ``{"operator": "and", "value": [...]}`` or ``"or"``, in
                lowercase.  A pydantic model is serialized with ``model_dump``.
            exclude_resolved (optional, bool):
                If False, resolved techniques are included.  If omitted, the API
                excludes them.

        Returns:
            :obj:`TopAttackTechniquesSearchResponse`:
                The techniques in ``data``, and the ``pagination`` details
                (``total``, ``offset``, ``limit`` and ``sort``).  ``total`` is
                also available directly on the response.

        Examples:
            Search the top attack techniques with the default settings:

            >>> response = t1.attack_path.findings.top_attack_techniques_search()
            >>> print(f"Found {response.total} attack techniques")

            High priority techniques that are still to do, highest priority
            first:

            >>> response = t1.attack_path.findings.top_attack_techniques_search(
            ...     sort='priority:desc',
            ...     filter={
            ...         'operator': 'and',
            ...         'value': [
            ...             {'property': 'priority', 'operator': 'eq', 'value': 'high'},
            ...             {'property': 'status', 'operator': 'eq', 'value': 'to_do'},
            ...         ],
            ...     },
            ... )
            >>> for technique in response.data:
            ...     print(technique.mitre_id, technique.name)

            Page through every technique, including resolved ones:

            >>> offset = 0
            >>> while True:
            ...     page = t1.attack_path.findings.top_attack_techniques_search(
            ...         offset=offset, exclude_resolved=False
            ...     )
            ...     offset += len(page.data)
            ...     if not page.data or offset >= page.total:
            ...         break
        """
        params = {}
        if limit is not None:
            params['limit'] = limit
        if offset is not None:
            params['offset'] = offset
        if sort is not None:
            params['sort'] = sort
        if exclude_resolved is not None:
            if not isinstance(exclude_resolved, bool):
                raise TypeError(
                    'exclude_resolved is of type '
                    f'{exclude_resolved.__class__.__name__}.  Expected bool'
                )
            params['exclude_resolved'] = str(exclude_resolved).lower()
        kwargs = {'params': params}
        if filter:
            if isinstance(filter, BaseModel):
                filter = filter.model_dump(mode='json')
            kwargs['json'] = filter
        return TopAttackTechniquesSearchResponse(
            **self._api.post('api/v1/t1/apa/top-attack-techniques/search', **kwargs)
        )
