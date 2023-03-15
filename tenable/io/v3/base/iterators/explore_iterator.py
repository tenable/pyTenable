'''
Iterator for search V3 endpoints
'''
from copy import copy
from typing import Dict

from requests import Response

from tenable.io.v3.base.iterators.iterator import APIResultIterator


class ExploreIterator(APIResultIterator):
    '''
    Base Iterator for explore V3 endpoints
    '''
    _path: str = None
    _next_token: str = None
    _resource: str = None
    _payload: Dict = {}
    _headers: Dict = {}

    def _construct_headers(self) -> Dict:
        '''
        Constructs the headers for API calls
        '''
        return copy(self._headers)

    def _construct_payload(self) -> Dict:
        '''
        Constructs the payload for the API
        '''
        payload = copy(self._payload)
        if self._next_token:
            payload['next'] = self._next_token
        return payload

    def _process_response(self, response: Response) -> None:
        '''
        Processes the API response
        '''
        pass

    def _get_page(self) -> None:
        '''
        Request the next page of data
        '''
        payload = self._construct_payload()
        headers = self._construct_headers()

        # This is to stop the iteration in case of csv_iterator
        # for infinite loop.
        if self.num_pages >= 1 and self._next_token is None:
            raise StopIteration()
        resp = self._api.post(self._path,
                              json=payload,
                              headers=headers
                              )
        self._next_token = resp.headers.get('X-Continuation-Token')
        self._process_response(resp)


class SearchIterator(ExploreIterator):
    '''
    Search Iterator for explore V3 endpoints
    '''

    def _process_response(self, response: Response) -> None:
        '''
        Process the API Response
        '''
        body = response.json()
        # Pagination value can be null in JSON response, we need to make sure
        # a dict is returned
        pagination = body.get('pagination') or {}
        self.page = body[self._resource]
        self.total = pagination.get('total')
        self._next_token = pagination.get('next')


class CSVChunkIterator(ExploreIterator):
    '''
    CSV Iterator for explore V3 endpoints
    '''
    _headers = {'Accept': 'text/csv'}
    row_headers: str = None

    def _process_response(self, response: Response) -> None:
        '''
        Process the API Response
        '''
        if not self.row_headers:
            self.row_headers, _, data = response.text.partition('\n')
            self.page = [data]
        else:
            self.page = [response.text]

    def __getitem__(self, key: int) -> str:
        '''
        Returns the specified item
        '''
        return '\n'.join([self.row_headers, self.page[key]])
