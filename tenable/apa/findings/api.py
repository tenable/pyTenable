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

from tenable.apa.findings.schema import FindingsPageSchema
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


class FindingsAPI(APIEndpoint):
    _schema = FindingsPageSchema()

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
