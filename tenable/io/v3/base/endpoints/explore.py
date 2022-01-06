'''
Base Explore Endpoint Class
'''
import time
from typing import Dict, List, Union
from uuid import UUID

from requests import Response

from tenable.base.endpoint import APIEndpoint
from tenable.io.v3.base.iterators.explore_iterator import (ExploreIterator,
                                                           SearchIterator)
from tenable.io.v3.base.schema.explore.filters import ParseFilterSchema
from tenable.io.v3.base.schema.explore.search import SearchSchema


class ExploreBaseEndpoint(APIEndpoint):
    _conv_json = False

    @staticmethod
    def _parse_filters(finput: List,
                       filterset: Dict = None,
                       rtype: str = 'sjson') -> Dict:
        '''
        A centralized method to parse and munge the filter tuples into the
        anticipates response.

        Args:
            finput (list): The list of filter tuples
            filterset (dict): The response of the allowed filters
            rtype (str, optional):
                The filter format.  Allowed types are 'json', 'sjson',
                'accessgroup', and 'colon'.  JSON is just a simple JSON list of
                dictionaries. SJSON format is effectively serialized JSON into
                the query params. COLON format denotes a colon-delimited
                format.

        Returns:
            dict:
                The query parameters in the anticipated dictionary format to
                feed to requests.
        '''
        resp = dict()

        for f in finput:
            # First we need to validate the inputs are correct. We will do that
            # by comparing the filter to the filterset data we have and compare
            # the operators and values to make sure that the input is expected.
            schema = ParseFilterSchema(
                context={
                    'filter_set': filterset
                }
            )
            data = schema.dump(schema.load({
                'filter_name': f[0],
                'filter_operator': f[1],
                'filter_value': f[2]
            }))

            fname = data['filter_name']
            foper = data['filter_operator']
            fval = data['filter_value']

            if rtype not in ['accessgroup']:
                fval = ','.join(fval)

            if rtype == 'sjson':
                # For the serialized JSON format, we will need to generate the
                # expanded input for each filter
                i = finput.index(f)
                resp['filter.{}.filter'.format(i)] = fname
                resp['filter.{}.quality'.format(i)] = foper
                resp['filter.{}.value'.format(i)] = fval
            elif rtype == 'json':
                # for standard JSON formats, we will simply build a 'filters'
                # list and store the information there.
                if 'filters' not in resp:
                    resp['filters'] = list()
                resp['filters'].append({
                    'filter': fname,
                    'quality': foper,
                    'value': fval
                })
            elif rtype == 'colon':
                # for the colon-delimited format, we simply need to generate
                # the filter as NAME:OPER:VAL and dump it all into a field
                # named f.
                if 'f' not in resp:
                    resp['f'] = list()
                resp['f'].append('{}:{}:{}'.format(fname, foper, fval))
            elif rtype == 'accessgroup':
                # For the access group format, we will instead use the format
                # of "terms", "type", and "operator".  Further all terms must
                # be a list of strings.
                if 'rules' not in resp:
                    resp['rules'] = list()
                resp['rules'].append({
                    'operator': foper,
                    'terms': fval,
                    'type': fname
                })
            elif rtype == 'assets':
                # For the asset format, we will instead use the format of
                # "field", "operator", and "value". Further all terms must be a
                # list of strings.
                if 'asset' not in resp:
                    resp['asset'] = list()
                resp['asset'].append({
                    'field': fname,
                    'operator': foper,
                    'value': fval
                })
        return resp

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
