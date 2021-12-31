'''
Base Explore Endpoint Class
'''
import time
from typing import Dict, List, Optional, Type, Union
from uuid import UUID

from tenable.base.endpoint import APIEndpoint
from tenable.io.v3.base.schema.explore.search import SearchSchema
from tenable.errors import UnexpectedValueError, FileDownloadError


class ExploreBaseEndpoint(APIEndpoint):
    _conv_json = False

    def details(self, obj_id: Union[str, UUID]):
        '''
        Gets the details for the specified id.

        Args:
            obj_id:
                The unique identifier for the records to be retrieved.

        Returns:
            Dict:
                The requested object

        Example:

            >>> tio.{PATHWAY}.details('00000000-0000-0000-0000-000000000000')
        '''
        return self._get(obj_id, conv_json=self._conv_json)

    def search(
            self,
            *,
            fields: Optional[List[str]] = None,
            sort: Optional[List[Dict]] = None,
            filter: Optional[Dict] = None, limit: int = 1000,
            next: Optional[str] = None, return_resp: bool = False,
            iterator_cls=None,
            schema_cls: Optional[Type[SearchSchema]] = None,
            **kwargs
    ):
        '''
        Initiate a search

        Args:
            fields:
                The list of field names to return.
            sort:
                A list of dictionaries describing how to sort the data
                that is to be returned.
            filter:
                A nestable filter object detailing how to filter the results
                down to the desired subset.
            limit:
                How many objects should be returned in each request.
            next:
                The pagination token to use when requesting the next page of
                results.  This token is presented in the previous response.
            return_resp:
                If set to true, will override the default behavior to return
                an iterable and will instead return the results for the
                specific page of data.
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

        Examples:

            >>>
        '''
        kwargs['fields'] = fields
        kwargs['sort'] = sort
        kwargs['filter'] = filter
        kwargs['limit'] = limit
        kwargs['next'] = next
        if not schema_cls:
            schema_cls = SearchSchema
        if not iterator_cls:
            # todo - commenting this temporarily
            # iterator_cls = ExploreSearchIterator
            pass
        schema = schema_cls()
        payload = schema.dump(schema.load(kwargs))
        if return_resp:
            return self._post('search', json=payload)
        return iterator_cls(
            self._api,
            _path=f'{self._path}/search',
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

    def _parse_filters(self, finput, filterset=None, rtype='sjson'):
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
                the query params.COLON format denotes a colon-delimited format.

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
            fname = self._check('filter_name', f[0], str)
            if f[0] not in filterset:
                raise UnexpectedValueError(
                    '{} is not a filterable option'.format(f[0]))

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
                # for the colon-delimited format, we simply need to generate
                # thefilter as NAME:OPER:VAL and dump it all into a field named
                # f.
                if 'f' not in resp:
                    resp['f'] = list()
                resp['f'].append('{}:{}:{}'.format(fname, foper, fval))
            elif rtype == 'accessgroup':
                # For the access group format, we will instead use the format
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

    def _wait_for_download(self, path, resource, resource_id, file_id, **kw):
        '''
        A simple method to centralize waiting for an export to enter a
        completed state.  The initial request will be made and then we will
        recheck every two and a half seconds after that.  Once the status
        returns one of the completed states, we will return the status.
        '''
        status = self._api.get(path, **kw).json()['status']
        while status not in ['error', 'ready']:
            time.sleep(2.5)
            status = self._api.get(path, **kw).json()['status']

        # If the status that has been reported back is "error", then we will
        # need to throw the appropriate error back to the user.
        if status == 'error':
            raise FileDownloadError(resource, resource_id, file_id)

        # Return the status to the caller.
        return status
