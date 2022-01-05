'''
Base Explore Endpoint Class
'''
import time
from typing import Union
from uuid import UUID

from requests import Response

from tenable.base.endpoint import APIEndpoint
from tenable.io.v3.base.iterators.explore_iterator import (ExploreIterator,
                                                           SearchIterator)
from tenable.io.v3.base.schema.explore.search import SearchSchema


class ExploreBaseEndpoint(APIEndpoint):
    _conv_json = False

    def details(self, obj_id: Union[str, UUID]) -> dict:
        '''
        Gets the details for the specified id.

        Args:
            obj_id:
                The unique identifier for the records to be retrieved.

        Returns:
            dict:
                The requested object

        Example:

            >>> tio.{PATHWAY}.details('00000000-0000-0000-0000-000000000000')
        '''
        return self._get(obj_id, conv_json=self._conv_json)

    def search(self,
               *,
               resource: str,
               api_path: str,
               is_sort_with_prop: bool = True,
               return_resp: bool = False,
               iterator_cls: ExploreIterator = SearchIterator,
               schema_cls: SearchSchema = SearchSchema,
               **kwargs
               ) -> Union[Response, ExploreIterator]:
        '''
        Initiate a search

        Args:
            resource (str):
                The json key to fetch the data from response
            api_path (str):
                API path for search endpoint
            is_sort_with_prop (bool):
                If set to True sort structure will be in form of
                {'property':'field_name','order': 'asc'} else
                {'field_name': 'asc'}
            fields (list):
                The list of field names to return.
                Example:
                    - ``['field1', 'field2']``
            sort (list(tuple)):
                A list of dictionaries describing how to sort the data
                that is to be returned.
                Examples:
                    - ``[{'last_observed': 'desc'}]``
            filter (tuple, dict):
                A nestable filter object detailing how to filter the results
                down to the desired subset.

                Examples:
                    >>> ('or', ('and', ('test', 'oper', '1'),
                                   ('test', 'oper', '2')
                            ),
                    'and', ('test', 'oper', 3)
                   )
                    >>> {'or': [
                    {'and': [
                        {'value': '1', 'operator': 'oper', 'property': '1'},
                        {'value': '2', 'operator': 'oper', 'property': '2'}
                        ]
                    }],
                    'and': [
                        {'value': '3', 'operator': 'oper', 'property': 3}
                        ]
                    }

                As the filters may change and sortable fields may change over
                time, it's highly recommended that you look at the output of
                the :py:meth:`tio.v3.vm.filters.asset_filters()`
                endpoint to get more details.
            limit (int):
                How many objects should be returned in each request.
                 Default is 1000.
            next (str):
                The pagination token to use when requesting the next page of
                results.  This token is presented in the previous response.
            return_resp (bool):
                If set to true, will override the default behavior to return
                an iterable and will instead return the results for the
                specific page of data.
            return_csv (bool):
                If set to true, It wil return the CSV Iteratble
            iterator_cls:
                If specified, will override the default iterator class that
                will be used for instantiating the iterator.
            schema_cls:
                If specified, will override the default schema class that
                will be used to validate the

        Returns:
            Iterable:
                The iterable that handles the pagination and potentially
                async requests for the job.
            requests.Response:
                If ``return_json`` was set to ``True``, then a response
                object is instead returned instead of an iterable.

        '''
        schema = schema_cls(
            context={'is_sort_with_prop': is_sort_with_prop})
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

    def search_results(self, search_id: str, wait_for_results: bool = True):
        '''
        '''
        resp = self._get(f'search/{search_id}')
        if resp.status_code == 202:
            retry_after = resp.headers.get('retry-after', 10)
            search_id = resp.headers.get('request-result-id', search_id)
        if wait_for_results:
            time.sleep(retry_after)
            return self.search_results(search_id, wait_for_results=True)
        return resp
