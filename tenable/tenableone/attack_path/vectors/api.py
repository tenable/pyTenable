"""
Vectors
=======

Methods described in this section relate to the vectors API.
These methods can be accessed at ``TenableOne.attack_path``.

.. rst-class:: hide-signature
.. autoclass:: VectorsAPI
    :members:

.. toctree::
    :hidden:
    :glob:

    findings/index
    vectors/index
"""

from copy import copy
from typing import Dict, Optional, Union

from restfly import APIIterator

from tenable.base.endpoint import APIEndpoint
from tenable.tenableone.attack_path.vectors.schema import (
    DiscoverPageTableResponse,
    PublicVectorFilterType,
    VectorsPageSchema,
)


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
        payload['page_number'] = self._next_page

        resp = self._api.get('api/v1/t1/apa/vectors', params=payload, box=True)
        self._next_page = resp.get('page_number') + 1
        self.page = resp.data
        self.total = resp.get('total')


class VectorsAPI(APIEndpoint):
    _schema = VectorsPageSchema

    def list(
        self,
        page_number: Optional[int] = None,
        limit: int = 10,
        filter: Optional[dict] = None,
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

            filter (optional, dict):
                A document as defined by Tenable APA online documentation.
                Filters to allow the user to get
                to a specific subset of Findings.
                For a more detailed listing of what filters are available,
                please refer to the API documentation
                linked above, however some examples are:

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
            List all of the available vectors:

            >>> vectors = tapa.vectors.list()
            >>> for f in vectors:
            ...     pprint(f)

            Filtering for a specific subset of vectors:

            >>> tapa.vectors.list(
            ...     limit='10',
            ...     sort_field='name',
            ...     sort_order='desc',
            ...     filter={"operator":"==", "key":"name", "value":"nice name"},
            ...     return_iterator=False
            ...     )
        """
        payload = {
            'page_number': page_number,
            'limit': limit,
            'filter': filter,
            'sort_field': sort_field,
            'sort_order': sort_order,
        }
        if run_ai_summarization:
            payload['run_ai_summarization'] = 'true'
        if return_iterator:
            return VectorIterator(self._api, _payload=payload)
        return self._schema(**self._get(path='api/v1/t1/apa/vectors', params=payload))

    def top_attack_paths_search(
        self,
        limit: int = 1000,
        sort: Optional[str] = None,
        run_ai_summarization: Optional[str] = None,
        filter: Optional[PublicVectorFilterType] = None,
    ) -> DiscoverPageTableResponse:
        """
        Search top attack paths leading to critical assets.

        This endpoint provides comprehensive search capabilities for attack paths with
        advanced filtering, sorting, and pagination options. The response includes
        detailed information about each attack path, including techniques, nodes, and metadata.

        Args:
            limit (optional, int):
                Number of items per page (default: 1000, min: 100, max: 10000)

            sort (optional, str):
                Sort parameter in format "{sort_field}:{sort_order}" (e.g., "name:asc", "priority:desc")

            run_ai_summarization (optional, str):
                Whether to run AI summarization (default: "false"). Enabling AI summarization
                provides additional insights but results in slower response times.
                Valid values: "true", "false"

            filter (optional, PublicVectorFilterType):
                Filter criteria for the search. The filter is passed as a JSON object
                in the request body. Supports complex filtering with AND/OR operators.

        Returns:
            :obj:`DiscoverPageTableResponse`:
                Response containing attack paths data with pagination information

        Examples:
            Search for high priority attack paths leading to critical assets

            >>> filter_data = {
            ...     "operator": "AND",
            ...     "value": [
            ...         {"property": "priority", "operator": "gte", "value": 8},
            ...         {"property": "critical_asset", "operator": "eq", "value": True}
            ...     ]
            ... }
            >>> response = t1.attack_path.vectors.top_attack_paths_search(
            ...     limit=500,
            ...     sort="priority:desc",
            ...     filter=filter_data
            ... )
            >>> for attack_path in response.data:
            ...     print(f"Attack Path: {attack_path.name}, Priority: {attack_path.priority}")

            Simple search with default parameters

            >>> response = t1.attack_path.vectors.top_attack_paths_search()
            >>> print(f"Found {response.total} attack paths")
        """
        payload = {
            'limit': limit,
        }

        if sort:
            payload['sort'] = sort
        if run_ai_summarization:
            payload['run_ai_summarization'] = run_ai_summarization

        # For POST request with filter in body
        if filter:
            # Handle both PublicVectorFilterType objects and plain dictionaries
            if hasattr(filter, 'dict'):
                filter_json = filter.model_dump()
            else:
                filter_json = filter

            return DiscoverPageTableResponse(
                **self._api.post(
                    'api/v1/t1/top-attack-paths/search',
                    params=payload,
                    json=filter_json,
                )
            )
        else:
            return DiscoverPageTableResponse(
                **self._api.post('api/v1/t1/top-attack-paths/search', params=payload)
            )
