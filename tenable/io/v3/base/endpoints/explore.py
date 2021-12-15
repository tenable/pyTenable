'''
Base Explore Endpoint Class
'''
import time
from typing import Dict, List, Optional, Type, Union
from uuid import UUID

from tenable.base.endpoint import APIEndpoint
from tenable.io.v3.base.schema.explore.search import SearchSchema


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
        self._get(obj_id, conv_json=self._conv_json)

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
