"""
Findings
=============

Methods described in this section relate to the findings API.
These methods can be accessed at ``TenableAPA.findings``.

.. rst-class:: hide-signature
.. autoclass:: FindingsAPI
    :members:
"""

from copy import copy
from typing import Dict, Optional, Union

from restfly import APIIterator

from tenable.apa.findings.schema import FindingsPageSchema, AttackTechniquesSearchResponseSchema
from tenable.base.endpoint import APIEndpoint


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
        print(self._next_token)
        payload["next"] = self._next_token

        resp = self._api.get("apa/findings-api/v1/findings",
                             params=payload, box=True)
        self._next_token = resp.get("next")
        self.page = resp.data
        self.total = resp.total


class AttackTechniqueIterator(APIIterator):
    """
    Attack Technique Iterator for offset-based pagination
    """

    _offset: int = 0
    _payload: Dict
    _filters: Optional[Dict]
    _limit: int = 1000

    def _get_page(self) -> None:
        """
        Request the next page of data
        """
        payload = copy(self._payload)
        payload["offset"] = self._offset
        payload["limit"] = self._limit

        if self._filters:
            resp = self._api.post("apa/findings-api/v1/attack-techniques/search",
                                 json=self._filters, params=payload, box=True)
        else:
            resp = self._api.post("apa/findings-api/v1/attack-techniques/search",
                                 params=payload, box=True)
        
        self.page = resp.data
        self.total = resp.pagination.get("total", 0)
        
        # Update offset for next page
        self._offset += len(self.page)
        
        # Stop iteration if we got fewer items than requested (end of data)
        # or if we've reached the total count
        if len(self.page) < self._limit or self._offset >= self.total:
            self._exhausted = True


class FindingsAPI(APIEndpoint):
    _schema = FindingsPageSchema()
    _attack_techniques_schema = AttackTechniquesSearchResponseSchema()

    def list(
        self,
        page_number: Optional[int] = None,
        next_token: Optional[str] = None,
        limit: int = 50,
        filter: Optional[dict] = None,
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

             filter (optional, dict):
                 A document as defined by Tenable APA online documentation.
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
             ...     filter='value',
             ...     return_iterator=False
             ...     )
        """

        payload = {
            "page_number": page_number,
            "next": next_token,
            "limit": limit,
            "filter": filter,
            "sort_filed": sort_filed,
            "sort_order": sort_order,
        }
        if return_iterator:
            return FindingIterator(self._api, _payload=payload,
                                   _next_token=next_token)
        return self._schema.load(
            self._get(path="apa/findings-api/v1/findings", params=payload)
        )

    def search_attack_techniques(
        self,
        filters: Optional[dict] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        sort: Optional[str] = None,
        return_iterator: bool = True,
    ) -> Union[AttackTechniqueIterator, dict]:
        """
        Search attack techniques

        Args:
            filters (optional, dict):
                Filter conditions for searching attack techniques.
                Supports complex filtering with AND/OR operators.
                Examples:
                - ``{"operator":"==", "property":"priority", "value":"high"}``
                - ``{"operator":"and", "value":[{"operator":"==", "property":"priority", "value":"high"}, {"operator":"==", "property":"state", "value":"open"}]}``

            offset (optional, int):
                Number of items to skip for pagination.
                If omitted, the default value is 0.

            limit (optional, int):
                Number of items per page.
                If omitted, the default value is 1000.
                The minimum value is 100 and the maximum value is 10000.

            sort (optional, str):
                Sort parameter in format "{sort_field}:{sort_order}" with multiple variations:
                - Ascending: "asc", "ASC", "ascending", "ASCENDING", "Ascending"
                - Descending: "desc", "DESC", "descending", "DESCENDING", "Descending"
                - Examples: "priority:desc", "name:asc", "last_updated_at:ASCENDING", "state:DESCENDING"
                
                Supported sort fields: last_updated_at, priority, mitre_id, name, 
                procedureName, status, state, vectorCount

            return_iterator (bool, optional):
                Should we return the response instead of iterable?

        Returns:
            :obj:`FindingIterator` or :obj:`dict`:
                List of attack technique records

        Examples:
            >>> attack_techniques = tapa.findings.search_attack_techniques()
            >>> for technique in attack_techniques:
            ...     pprint(technique)

        Examples:
            >>> tapa.findings.search_attack_techniques(
            ...     limit=100,
            ...     sort='priority:desc',
            ...     filters={'operator': '==', 'property': 'priority', 'value': 'high'},
            ...     return_iterator=False
            ... )
        """
        payload = {
            "offset": offset,
            "limit": limit,
            "sort": sort,
        }
        
        # Add filters to request body if provided
        if filters:
            # For POST request with body, we need to handle this differently
            # The filters go in the request body, not as query parameters
            if return_iterator:
                return AttackTechniqueIterator(self._api, _payload=payload, _filters=filters, _limit=limit or 1000)
            else:
                response = self._api.post("apa/findings-api/v1/attack-techniques/search", 
                                        json=filters, params=payload, box=True)
                return self._attack_techniques_schema.load(response)
        else:
            if return_iterator:
                return AttackTechniqueIterator(self._api, _payload=payload, _filters=None, _limit=limit or 1000)
            else:
                response = self._api.post("apa/findings-api/v1/attack-techniques/search", 
                                        params=payload, box=True)
                return self._attack_techniques_schema.load(response)
