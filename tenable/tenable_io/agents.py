from tenable.base import APIEndpoint
from tenable.tenable_io.base import TIOIterator

class AgentsIterator(TIOIterator):
    '''
    The agents iterator provides a scalable way to work through agent result
    sets of any size.  The iterator will walk through each page of data,
    returning one record at a time.  If it reaches the end of a page of
    records, then it will request the next page of information and then continue
    to return records from the next page (and the next, and the next) until the
    counter reaches the total number of records that the API has reported.

    Attributes:
        count (int): The current number of records that have been returned
        page (list): 
            The current page of data being walked through.  pages will be
            cycled through as the iterator requests more information from the
            API.
        page_count (int): The number of record returned from the current page.
        total (int): 
            The total number of records that exist for the current request.
    '''
    def _get_data(self):
        '''
        Request the next page of data
        '''
        # The first thing that we need to do is construct the query with the
        # current offset and limits
        query = self._query
        query['limit'] = self._limit
        query['offset'] = self._offset

        # Lets make the actual call at this point.
        resp = self._api.get(
            'scanners/{}/agents'.format(self._scanner_id), params=query).json()

        # Lastly we need to return the data from the response and the data key
        # so that _get_page() knows where the information is stored.
        return resp, 'agents'
            

class AgentsAPI(APIEndpoint):
    def delete(self, agent_id, scanner_id=1):
        '''
        `agents: delete <https://cloud.tenable.com/api#/resources/agents/delete>`_

        Args:
            agent_id (int):
                The ID fo the agent to delete
            scanner_id (int, optional):
                The identifier the scanner that the agent communicates to.

        Returns:
            None
        '''
        return self._api.delete('scanners/{}/agents/{}'.format(
            self._check('scanner_id', scanner_id, int),
            self._check('agent_id', agent_id, int)    
        ))

    def list(self, *filters, **kw):
        '''
        `agents: list <https://cloud.tenable.com/api#/resources/agents/list>`_

        Args:
            *filters (tuple, optional):

            scanner_id (int, optional):
                The identifier the scanner that the agent communicates to.
            offset (int, optional):
                The starting record to retrieve.  Default is 0.
            limit (int, optional):
                The number of records to retrieve.  Default is 50
            sort (tuple, optional):
                A tuple of tuples identifying the the field and sort order of
                the field.
            
        Returns:
            AgentsIterator: 
                An iterator that handles the page management of the requested
                records.
        '''
        scanner_id = 1
        limit = 50
        offset = 0
        pages = None
        query = {'f': []}

        if 'scanner_id' in kw:
            scanner_id = self._check('scanner_id', kw['scanner_id'], int)
        if 'offset' in kw and self._check('offset', kw['limit'], int):
            offset = kw['offset']
        if 'limit' in kw and self._check('limit', kw['limit'], int):
            limit = kw['limit']

        # For the sorting fields, we are converting the tuple that has been
        # provided to us and converting it into a comma-delimited string with
        # each field being represented with its sorting order.  e.g. If we are
        # presented with the following:
        #
        #   sort=(('field1', 'asc'), ('field2', 'desc'))
        #
        # we will generate the following string:
        #
        #   sort=field1:asc,field2:desc
        #
        if 'sort' in kw and self._check('sort', kw['sort'], tuple):
            for item in kw['sort']:
                query['sort'] = ','.join(['{}:{}'.format(
                    self._check('sort_field', i[0], str),
                    self._check('sort_direction', i[1], str, choices=['asc', 'desc'])
                ) for i in kw['sort']])

        # For the filters, we are converting the tuples provided into multiple
        # filter strings.  The filter strings are in the format of name:op:value.
        # Down the road this should likely be refactored to pull the filter
        # options and actually validate the input beyond proving that it's a
        # string, however for now this will do.
        # https://cloud.tenable.com/api#/resources/filters
        #
        # Example filter tuple:
        #
        #    ('distro', 'match', 'win')
        #
        # would generate the following string:
        #
        #    'distro:match:win'
        #
        query['f'] = ['{}:{}:{}'.format(
            self._check('filter_name', f[0], str),
            self._check('filter_operator', f[1], str),
            self._check('filter_value', f[2], str)
        ) for f in filters]

        if 'filter_type' in kw and self._check('filter_type', kw['filter_type'], str, choices=['and', 'or']):
            query['ft'] = kw['filter_type']
        if 'wildcard' in kw and self._check('wildcard', kw['wildcard'], str):
            query['w'] = kw['wildcard']
        if 'wildcard_fields' in kw and self._check('wildcard_fields', kw['wildcard_fields'], list):
            query['wf'] = ','.join(kw['wildcard_fields'])

        return AgentsIterator(self._api,
            _limit=limit,
            _offset=offset,
            _pages_total=pages,
            _scanner_id=scanner_id,
            _query=query
        )

    def get(self, agent_id, scanner_id=1):
        '''
        `agents: get <https://cloud.tenable.com/api#/resources/agents/get>`_

        Args:
            agent_id (int): 
                The identifier of the agent.
            scanner_id (int, optional): 
                The identifier of the scanner.  Default is 1.

        Returns:
            dict: The agent dictionary record.
        '''
        return self._api.get('scanners/{}/agents/{}'.format(
            self._check('scanner_id', scanner_id, int),
            self._check('agent_id', agent_id, int)
        )).json()
