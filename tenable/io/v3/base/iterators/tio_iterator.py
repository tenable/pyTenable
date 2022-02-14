'''
The following methods in classes allow for page iteration
and centralized data processing utility
'''

from tenable.io.v3.base.iterators.iterator import APIResultIterator


class TIOIterator(APIResultIterator):
    '''
    The following methods allows us to iterate through pages and get data
    '''
    _path = None
    _resource = None
    _size = 100
    _page_num = 0
    _api_version = 1
    _offset = None
    _limit = None
    _query = None

    # The number of pages that may be requested before bailing.  If set to
    # None, then there is no limitation to the number of pages that may be
    # requested.
    _pages_total = None
    _pages_requested = 0

    def _get_data(self):
        '''
        Request the next page of data
        '''
        # The first thing that we need to do is construct the query with the
        # current offset and limits
        query = self._query

        if self._api_version == 2:
            query['size'] = self._size
            query['page'] = self._page_num
        else:
            query['limit'] = self._limit
            query['offset'] = self._offset

        # Lets make the actual call at this point.
        resp = self._api.get(self._path, params=query).json()

        if self._api_version == 2:
            self._page_num += 1
        else:
            self._offset += self._limit

        # Lastly we need to return the data from the response and the data key
        # so that _get_page() knows where the information is stored.
        return resp, self._resource

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
        resp, key = self._get_data()

        # Now that we have the response, lets reset any counters we need to,
        # and increment things like the page counter, offset, etc.
        self.page_count = 0
        self._pages_requested += 1

        # Lastly we want to refresh the page data and the total based on the
        # most recent data we have.
        if self._api_version == 2:
            self.page = resp['data'][key]
            self.total = resp['total_count']
        else:
            self.page = resp[key]
            self.total = resp['pagination']['total']
