'''
Base explore class for V3 endpoints
'''
from enum import Enum
from typing import Union

from requests import Response

from tenable.base.endpoint import APIEndpoint
from tenable.io.v3.base.iterators.explore_iterator import (ExploreIterator,
                                                           SearchIterator)

from tenable.io.v3.base.schema.explore.search import (SearchSchemaV3,
                                                      SortType)


class ExploreBaseEndpoint(APIEndpoint):
    _conv_json = False
    _sort_type = SortType

    def _search(self,
                *,
                resource: str,
                api_path: str,
                sort_type: Enum = _sort_type.default,
                return_resp: bool = False,
                iterator_cls: ExploreIterator = SearchIterator,
                schema_cls: SearchSchemaV3 = SearchSchemaV3,
                **kwargs
                ) -> Union[Response, ExploreIterator]:
        '''
        Initiate a search

        Args:
            resource (str):
                The json key to fetch the data from response
            api_path (str):
                API path for search endpoint
            sort_type (enum):
                Select format of sort expected by API. All the
                supported formats are present in SortType Enumeration Class.
            fields (list, optional):
                The list of field names to return from the Tenable API.
                Example:
                    >>> ['field1', 'field2']
            sort (list[tuple], optional):
                sort is a list of tuples in the form of
                ('FIELD', 'ORDER').
                It describes how to sort the data
                that is to be returned.
                Examples:
                    >>> [('field_name_1', 'asc'),
                    ...      ('field_name_2', 'desc')]
            filter (tuple, dict, optional):
                A nestable filter object detailing how to filter the results
                down to the desired subset.
                Examples:
                    >>> ('or', ('and', ('test', 'oper', '1'),
                    ...                 ('test', 'oper', '2')
                    ...             ),
                    ...     'and', ('test', 'oper', 3)
                    ... )
                    >>> {
                    ...  'or': [{
                    ...      'and': [{
                    ...              'value': '1',
                    ...              'operator': 'oper',
                    ...              'property': '1'
                    ...          },
                    ...          {
                    ...              'value': '2',
                    ...              'operator': 'oper',
                    ...              'property': '2'
                    ...          }
                    ...      ]
                    ...  }],
                    ...  'and': [{
                    ...      'value': '3',
                    ...      'operator': 'oper',
                    ...      'property': 3
                    ...  }]
                    ... }
            limit (int, optional):
                Number of objects to be returned in each request.
                Default and maximum limit is 200.
            next (str, optional):
                The pagination token to use when requesting the next page of
                results. This token is presented in the previous response.
            return_resp (bool, optional):
                If set to true, will override the default behavior to return
                a requests.Response Object to the user.
            return_csv (bool, optional):
                If set to true, it will return the CSV response or
                iterable (based on return_resp flag). Iterator returns all
                rows in text/csv format for each call with row headers.
            iterator_cls:
                If specified, will override the default iterator class that
                will be used for instantiating the iterator.
            schema_cls:
                If specified, will override the default Search schema class
                that will be used for validation.

        :Returns:
            - Iterable:
                The iterable that handles the pagination for the job.
            - requests.Response:
                If ``return_resp`` is set to ``True``, then a response
                object is returned instead of an iterable.

        '''
        schema = schema_cls(
            context={'sort_type': sort_type})
        return_csv = kwargs.pop('return_csv', False)
        payload = schema.dump(schema.load(kwargs))

        if return_resp:
            headers = {}
            if return_csv:
                headers = {'Accept': 'text/csv'}
            return self._api.post(
                api_path,
                json=payload,
                headers=headers
            )
        return iterator_cls(
            self._api,
            _path=api_path,
            _resource=resource,
            _payload=payload
        )
