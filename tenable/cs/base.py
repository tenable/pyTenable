from tenable.base import APIResultsIterator, APIEndpoint

class CSEndpoint(APIEndpoint):
    pass

class CSIterator(APIResultsIterator):
    def _get_data(self):
        '''
        Performs the actual page action and returns the response.
        '''
        return None

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
        self._offset += self._limit

        # Lastly we want to refresh the page data and the total based on the
        # most recent data we have.
        self.page = resp['items']
        self.total = resp['pagination']['total']