'''

'''
from tenable.base import APIResultsIterator, APIEndpoint, FileDownloadError
from tenable.errors import UnexpectedValueError
import time

class TIOEndpoint(APIEndpoint):
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

class TIOIterator(APIResultsIterator):
    _path = None
    _resource = None
    _size = 100
    _page_num = 0
    _api_version = 1

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