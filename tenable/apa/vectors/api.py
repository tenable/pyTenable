"""
Vectors
=============

Methods described in this section relate to the vectors API.
These methods can be accessed at ``TenableAPA.vectors``.

.. rst-class:: hide-signature
.. autoclass:: VectorsAPI
    :members:
"""

import json
from copy import copy
from typing import Dict, Optional, Union

from tenable.base._restfly_v1 import APIIterator

from tenable.apa.vectors.schema import VectorsPageSchema
from tenable.base.endpoint import APIEndpoint


class VectorIterator(APIIterator):
    """
    Vector Iterator
    """

    _next_page: str = None
    _payload: Dict

    def _get_page(self) -> None:
        """
        Request the next page of data
        """
        payload = copy(self._payload)
        if self._next_page is not None:
            payload["page_number"] = self._next_page
        # The API only echoes page_number back when it was sent, so track
        # the page locally.  Pages are 1-based.
        current_page = payload.get("page_number") or 1
        resp = self._api.get("apa/api/discover/v1/vectors",
                             params=payload, box=True)
        self._next_page = current_page + 1
        self.page = resp.data
        self.total = resp.get("total")


class VectorsAPI(APIEndpoint):
    _schema = VectorsPageSchema()

    def list(
            self,
            page_number: Optional[int] = None,
            limit: int = 10,
            filter: Optional[Union[dict, str]] = None,
            sort_field: Optional[str] = None,
            sort_order: Optional[str] = None,
            run_ai_summarization: Optional[bool] = None,
            return_iterator=True,
    ) -> Union[VectorIterator, VectorsPageSchema]:
        """
         Retrieve vectors

         Args:
             page_number (optional, int):
                 For offset-based pagination, the requested page to retrieve.
                 If this parameter is omitted,
                 Tenable uses the default value of 1.

             limit (optional, int):
                 The number of records to retrieve.
                 If this parameter is omitted,
                 Tenable uses the default value of 25.
                 The maximum number of events that can be retrieved is 25.
                 For example: limit=25.

             filter (optional, dict | str):
                 A document as defined by Tenable APA online documentation.
                 A dict is serialized to a JSON string before it is sent, and a
                 string is passed through as-is.
                 Filters to allow the user to get
                 to a specific subset of Findings.
                 For a more detailed listing of what filters are available,
                 please refer to the API documentation
                 linked above, however some examples are as such:

                 - ``{"operator":"==", "key":"name", "value":"nice name"}``
                 - ``{"operator":">", "key":"critical_asset", "value": 10}``

             sort_field (optional, str):
                 The field you want to use to sort the results by.
                 Accepted values are ``name``, ``priority``

             run_ai_summarization (optional, bool):
                Indicates whether or not to run the AI summarization for missing paths.
                Note that enabling the AI summarization results in slower response times.
                Tenable uses the default value of false.

             return_iterator (optional, bool):
                 Should we return the response instead of iterable?


        Returns:
             :obj:`VectorsIterator`:
                 List of vectors records

         Examples:
             >>> vectors = tapa.vectors.list()
             >>> for f in vectors:
             ...     pprint(f)

         Examples:
             >>> tapa.vectors.list(
             ...     limit='10',
             ...     sort_field='name',
             ...     sort_order='desc',
             ...     filter={"operator":"==", "key":"name", "value":"nice name"},
             ...     return_iterator=False
             ...     )
        """
        payload = {
            "page_number": page_number,
            "limit": limit,
            "filter": json.dumps(filter) if isinstance(filter, dict) else filter,
            "sort_field": sort_field,
            "sort_order": sort_order}
        if run_ai_summarization:
            payload["run_ai_summarization"] = 'true'
        if return_iterator:
            return VectorIterator(self._api, _payload=payload)
        return self._schema.load(
            self._get(path="apa/api/discover/v1/vectors", params=payload)
        )
