'''
The following methods in classes allow for page iteration
and centralized data processing utility
'''

from copy import copy
from typing import Dict

from requests import Response

from tenable.io.v3.base.iterators.iterator import APIResultIterator


class ExploreIteratorWas(APIResultIterator):
    '''
    The following methods allows us to iterate through pages and get data
    This class is specially created for WAS APIs
    '''
    _path = None
    _resource = None
    _size = 100
    _page_num = 0
    _offset = 0
    _limit = None
    _query = None

    # The number of pages that may be requested before bailing.  If set to
    # None, then there is no limitation to the number of pages that may be
    # requested.
    _pages_total = None
    _pages_requested = 0

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

        return payload

    def _process_response(self, response: Response) -> None:
        '''
        Processes the API response
        '''
        pass

    def _get_data(self):
        '''
        Request the next page of data
        '''
        # The first thing that we need to do is construct the query with the
        # current offset and limits
        payload = self._construct_payload()
        headers = self._construct_headers()
        query = self._query

        self._limit = query['limit']
        self._offset = query['offset']

        # Lets make the actual call at this point.
        resp = self._api.post(self._path,
                              params=query,
                              json=payload,
                              headers=headers
                              )

        self._offset += self._limit

        return resp

    def _get_page(self):
        '''
        Get the next page of records
        '''
        # First we need to see if there is a page limit and if there is, have
        # we run into that limit.  If we have, then return a StopIteration
        # exception.
        if self._pages_total and self._pages_requested >= self._pages_total:
            raise StopIteration()

        # Lets make the actual call at this point.
        resp = self._get_data()

        # Now that we have the response, lets reset any counters we need to,
        # and increment things like the page counter, offset, etc.
        self.page_count = 0
        self._pages_requested += 1
        self._process_response(resp)


class SearchIterator(ExploreIteratorWas):
    '''
    Search Iterator for explore
    '''
    def _process_response(self, response: Response) -> None:
        '''
        Process the API Response
        '''
        body = response.json()
        # Lastly we want to refresh the page data and the total based on the
        # most recent data we have.

        self.page = body[self._resource]
        self.total = body['pagination']['total']


class CSVChunkIterator(ExploreIteratorWas):
    '''
    CSV Iterator for explore
    '''
    _headers = {'Accept': 'text/csv'}
    row_headers: str = None

    def _process_response(self, response: Response) -> None:
        '''
        Process the API Response
        '''
        self.total = int(response.headers.get('total'))
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
