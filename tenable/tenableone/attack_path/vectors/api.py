"""
Vectors
=======

Methods described in this section relate to the vectors API.
These methods can be accessed at ``TenableOne.attack_path``.

.. rst-class:: hide-signature
.. autoclass:: VectorsAPI
    :members:
"""

import json
import warnings
from copy import copy
from typing import Dict, Optional, Union

from pydantic import BaseModel

from tenable.base._restfly_v1 import APIIterator

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
        if self._next_page is not None:
            payload['page_number'] = self._next_page
        # The API only echoes page_number back when it was sent, so track
        # the page locally.  Pages are 1-based.
        current_page = payload.get('page_number') or 1
        resp = self._api.get('api/v1/t1/apa/vectors', params=payload, box=True)
        self._next_page = current_page + 1
        self.page = resp.data
        self.total = resp.get('total')


class VectorsAPI(APIEndpoint):
    _schema = VectorsPageSchema

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

        .. warning::
            Deprecated.  This method calls the attack path list endpoint, which
            Tenable deprecated on 2025-10-30.  Use :meth:`top_attack_paths_search`
            instead.

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
        warnings.warn(
            'attack_path.vectors.list() calls an endpoint that Tenable deprecated on '
            '2025-10-30.  Use attack_path.vectors.top_attack_paths_search() instead.',
            DeprecationWarning,
            stacklevel=2,
        )
        payload = {
            'page_number': page_number,
            'limit': limit,
            'filter': json.dumps(filter) if isinstance(filter, dict) else filter,
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
        exclude_resolved: bool = True,
        *,
        offset: Optional[int] = None,
    ) -> DiscoverPageTableResponse:
        """
        Search top attack paths leading to critical assets.

        This endpoint provides comprehensive search capabilities for attack paths with
        advanced filtering, sorting, and pagination options. The response includes
        detailed information about each attack path, including techniques, nodes, and metadata.

        Note: Attack Paths now inherit their status from the underlying techniques. Paths
        marked as "Chain Prevented" (partially fixed), "Accepted" or "Done" are excluded by
        default to prioritize active threats. Set exclude_resolved=False to include all paths.

        Args:
            limit (optional, int):
                Number of items per page (default: 1000, min: 100, max: 10000)

            sort (optional, str):
                Sort parameter in format "{sort_field}:{sort_order}"
                (e.g., "name:asc", "priority:desc", "path_status:asc")

            run_ai_summarization (optional, str):
                Whether to run AI summarization (default: "false"). Enabling AI summarization
                provides additional insights but results in slower response times.
                Valid values: "true", "false"

            filter (optional, PublicVectorFilterType):
                Filter criteria for the search. The filter is passed as a JSON object
                in the request body. Supports complex filtering with AND/OR operators.
                The API accepts the comparison operators ``==``, ``!=``, ``eq``,
                ``neq``, ``contains``, ``excludes``, ``includes``, ``>``, ``>=``,
                ``<`` and ``<=``, and rejects others with a 400 error.

            exclude_resolved (bool, optional):
                When True (default), excludes paths with path_status 'done',
                'chain_prevented', or 'accepted'. Set to False to include all paths.

            offset (optional, int):
                The number of records to skip, for paging through results with
                ``limit``.  If omitted, the API starts at the first record.

        Returns:
            :obj:`DiscoverPageTableResponse`:
                Response containing the attack paths in ``data``, and the
                ``pagination`` details (``total``, ``offset``, ``limit`` and
                ``sort``).  ``total`` is also available directly on the response.

        Examples:
            Search for high priority attack paths that are still to do

            >>> filter_data = {
            ...     "operator": "AND",
            ...     "value": [
            ...         {"property": "priority", "operator": ">=", "value": 8},
            ...         {"property": "path_status", "operator": "eq", "value": "to_do"}
            ...     ]
            ... }
            >>> response = t1.attack_path.vectors.top_attack_paths_search(
            ...     limit=500,
            ...     sort="priority:desc",
            ...     filter=filter_data
            ... )
            >>> for attack_path in response.data:
            ...     print(f"Attack Path: {attack_path.name}, Priority: {attack_path.priority}")

            Filter by path_status to get only the paths in review

            >>> filter_data = {
            ...     "property": "path_status",
            ...     "operator": "eq",
            ...     "value": "in_review"
            ... }
            >>> response = t1.attack_path.vectors.top_attack_paths_search(
            ...     filter=filter_data
            ... )

            Include resolved paths

            >>> response = t1.attack_path.vectors.top_attack_paths_search(
            ...     exclude_resolved=False
            ... )

            Page through all attack paths, 1000 at a time

            >>> offset = 0
            >>> while True:
            ...     page = t1.attack_path.vectors.top_attack_paths_search(offset=offset)
            ...     for attack_path in page.data:
            ...         print(attack_path.name)
            ...     offset += len(page.data)
            ...     if not page.data or offset >= page.total:
            ...         break

            Simple search with default parameters

            >>> response = t1.attack_path.vectors.top_attack_paths_search()
            >>> print(f"Found {response.total} attack paths")
        """
        payload = {
            'limit': limit,
            'exclude_resolved': exclude_resolved,
        }

        if offset is not None:
            payload['offset'] = offset
        if sort:
            payload['sort'] = sort
        if run_ai_summarization:
            payload['run_ai_summarization'] = run_ai_summarization

        # For POST request with filter in body
        if filter:
            # Handle both PublicVectorFilterType objects and plain dictionaries
            if isinstance(filter, BaseModel):
                filter_json = filter.model_dump(mode='json')
            else:
                filter_json = filter

            return DiscoverPageTableResponse(
                **self._api.post(
                    'api/v1/t1/apa/top-attack-paths/search',
                    params=payload,
                    json=filter_json,
                )
            )
        else:
            return DiscoverPageTableResponse(
                **self._api.post(
                    'api/v1/t1/apa/top-attack-paths/search', params=payload
                )
            )
