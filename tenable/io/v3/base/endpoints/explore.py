'''
Base Explore Endpoint Class
'''
import time
from enum import Enum
from typing import Dict, Union
from uuid import UUID

from requests import Response

from tenable.base.endpoint import APIEndpoint
from tenable.io.v3.base.iterators.explore_iterator import (ExploreIterator,
                                                           SearchIterator)
from tenable.io.v3.base.iterators.was_iterator import ExploreIteratorWas
from tenable.io.v3.base.iterators.was_iterator import \
    SearchIterator as SearchIteratorWAS
from tenable.io.v3.base.schema.explore.search import (SearchSchema,
                                                      SearchWASSchema,
                                                      SortType)
from tenable.utils import dict_clean


class ExploreBaseEndpoint(APIEndpoint):
    _conv_json = False
    _sort_type = SortType

    def _parse_filters(self, finput, filterset=None, rtype='sjson'):
        '''
        A centralized method to parse and munge the filter tuples into the
        anticipated response.
        Args:
            finput (list): The list of filter tuples
            filterset (dict): The response of the allowed filters
            rtype (str, optional):
                The filter format.  Allowed types are 'json', 'sjson',
                'accessgroup', and 'colon'.  JSON is just a simple JSON list of
                dictionaries. SJSON format is effectively serialized JSON into
                the query params. COLON format denotes a colon-delimited format.

        Returns:
            dict:
                The query parameters in the anticipated dictionary format to
                feed to requests.
        '''
        resp = dict()

        for f in finput:
            # First we need to validate the inputs are correct.  We will do that
            # by comparing the filter to the filterset data we have and compare
            # the operators and values to make sure that the input is expected.
            fname = self._check('filter_name', f[0], str)

            foper = self._check('filter_operator', f[1], str,
                                choices=filterset.get(f[0], dict()).get('operators'))

            if isinstance(f[2], str):
                rval = f[2].split(',')
            elif isinstance(f[2], list):
                rval = f[2]
            else:
                raise TypeError('filter_value is not a valid type.')

            fval = self._check('filter_value', rval, list,
                               choices=filterset.get(f[0], dict()).get('choices'),
                               pattern=filterset.get(f[0], dict()).get('pattern'))
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
                # for the colon-delimited format, we simply need to generate the
                # filter as NAME:OPER:VAL and dump it all into a field named f.
                if 'f' not in resp:
                    resp['f'] = list()
                resp['f'].append('{}:{}:{}'.format(fname, foper, fval))
            elif rtype == 'accessgroup':
                # For the access group format, we will instead use the format of
                # "terms", "type", and "operator".  Further all terms must be a
                # list of strings.
                if 'rules' not in resp:
                    resp['rules'] = list()
                resp['rules'].append({
                    'operator': foper,
                    'terms': fval,
                    'type': fname
                })
            elif rtype == 'assets':
                # For the asset format, we will instead use the format of
                # "field", "operator", and "value".  Further all terms must be a
                # list of strings.
                if 'asset' not in resp:
                    resp['asset'] = list()
                resp['asset'].append({
                    'field': fname,
                    'operator': foper,
                    'value': fval
                })

        return resp

    def _details(self, obj_id: Union[str, UUID], **kwargs) -> Dict:
        '''
        Gets the details for the specified id.

        Args:
            obj_id (str, uuid.UUID):
                The unique identifier for the records to be retrieved.
            **kwargs (dict):
                return_csv (bool):
                    Provide this boolean to get the response in form of
                    text or csv.

        Returns:
            :obj:`dict`:
                The requested object

        Example:

            >>> tio.{PATHWAY}.details('00000000-0000-0000-0000-000000000000')
        '''
        headers: dict = {}
        if kwargs.get('return_csv', False):
            headers = {'Accept': 'text/csv'}
            self._conv_json = True

        return self._get(obj_id, headers=headers, conv_json=self._conv_json)

    def _search(self,
                *,
                resource: str,
                api_path: str,
                sort_type: Enum = _sort_type.default,
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

    def _search_was(self,
                    *,
                    resource: str,
                    api_path: str,
                    sort_type: Enum = _sort_type.default,
                    return_resp: bool = False,
                    iterator_cls: ExploreIteratorWas = SearchIteratorWAS,
                    schema_cls: SearchWASSchema = SearchWASSchema,
                    **kwargs
                    ) -> Union[Response, ExploreIteratorWas]:
        '''
        Initiate a search for was API

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
            offset (int, optional):
                The pagination offset to use when requesting the next page of
                results.
            num_pages (int, optional):
                The total number of pages to request before stopping the
                iterator.
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
        num_pages = payload.pop('num_pages', None)
        query = {}
        payload, query = self._update_payload(payload, query)

        if return_resp:
            headers = {}
            if return_csv:
                headers = {'Accept': 'text/csv'}
            return self._api.post(
                api_path,
                json=payload,
                params=query,
                headers=headers
            )
        return iterator_cls(self._api,
                            _path=api_path,
                            _resource=resource,
                            _payload=payload,
                            _query=query,
                            _pages_total=num_pages
                            )

    def _update_payload(self, payload, query):
        query['limit'] = payload.pop('limit')
        query['sort'] = payload.pop('sort', None)
        query['offset'] = payload.pop('offset')
        query = dict_clean(query)

        return payload, query

    def _search_results(self, search_id: str, wait_for_results: bool = True):
        '''
        '''
        resp = self._get(f'search/{search_id}')
        if resp.status_code == 202:
            retry_after = resp.headers.get('retry-after', 10)
            search_id = resp.headers.get('request-result-id', search_id)
        if wait_for_results:
            time.sleep(retry_after)
            return self._search_results(search_id, wait_for_results=True)
        return resp
