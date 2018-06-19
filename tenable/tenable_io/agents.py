from tenable.tenable_io.base import TIOIterator, TIOEndpoint

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
            

class AgentsAPI(TIOEndpoint):
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
        self._api.delete('scanners/{}/agents/{}'.format(
            self._check('scanner_id', scanner_id, int),
            self._check('agent_id', agent_id, int)    
        ))

    def list(self, *filters, **kw):
        '''
        `agents: list <https://cloud.tenable.com/api#/resources/agents/list>`_

        Args:
            *filters (tuple, optional):
                Filters are tuples in the form of ('NAME', 'OPERATOR', 'VALUE').
                Multiple filters can be used and will filter down the data being
                returned from the API.

                Examples:
                    - ``('distro', 'match', 'win')``
                    - ``('name', 'nmatch', 'home')``

                As the filters mat change and sortable fields mat change over
                time, it's highly recommended that you look at the output of
                the `filters:agents-filters <https://cloud.tenable.com/api#/resources/filters/agents-filters>`_
                endpoint to get more details.
            filter_type (str, optional):
                The filter_type operator determines how the filters are combined
                together.  ``and`` will inform the API that all of the filter
                conditions must be met for an agent to be returned, whereas 
                ``or`` would mean that if any of the conditions are met, the
                agent record will be returned.
            limit (int, optional):
                The number of records to retrieve.  Default is 50
            offset (int, optional):
                The starting record to retrieve.  Default is 0.
            scanner_id (int, optional):
                The identifier the scanner that the agent communicates to.
            sort (tuple, optional):
                A tuple of tuples identifying the the field and sort order of
                the field.
            wildcard (str, optional):
                A string to pattern match against all available fields returned.
            wildcard_fields (list, optional):
                A list of fields to optionally restrict the wildcard matching
                to.

        Returns:
            AgentsIterator: 
                An iterator that handles the page management of the requested
                records.
        '''
        scanner_id = 1
        limit = 50
        offset = 0
        pages = None
        query = self._parse_filters(filters,
            self._api.filters.agents_filters(), rtype='colon')

        # Overload the scanner_id with a new value if it has been requested
        # to do so.
        if 'scanner_id' in kw:
            scanner_id = self._check('scanner_id', kw['scanner_id'], int)

        # If the offset was set to something other than the default starting
        # point of 0, then we will update offset to reflect that.
        if 'offset' in kw and self._check('offset', kw['offset'], int):
            offset = kw['offset']

        # The limit parameter affects how many records at a time we will pull
        # from the API.  The default in the API is set to 50, however we can
        # pull any variable amount.
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
            query['sort'] = ','.join(['{}:{}'.format(
                self._check('sort_field', i[0], str),
                self._check('sort_direction', i[1], str, choices=['asc', 'desc'])
            ) for i in kw['sort']])

        # The filter_type determines how the filters are combined together.
        # The default is 'and', however you can always explicitly define 'and'
        # or 'or'.
        if 'filter_type' in kw and self._check(
            'filter_type', kw['filter_type'], str, choices=['and', 'or']):
            query['ft'] = kw['filter_type']

        # The wildcard filter text refers to how the API will pattern match
        # within all fields, or specific fields using the wildcard_fields param.
        if 'wildcard' in kw and self._check('wildcard', kw['wildcard'], str):
            query['w'] = kw['wildcard']

        # The wildcard_fields parameter allows the user to restrict the fields
        # that the wildcard pattern match pertains to.
        if 'wildcard_fields' in kw and self._check(
            'wildcard_fields', kw['wildcard_fields'], list):
            query['wf'] = ','.join(kw['wildcard_fields'])

        # Return the Iterator.
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
        return self._api.get(
            'scanners/{}/agents/{}'.format(
                self._check('scanner_id', scanner_id, int),
                self._check('agent_id', agent_id, int)
            )).json()

    def bulk_unlink(self, agent_ids, scanner_id=1):
        '''
        `bulk-operations: bulk-unlink-agent <https://cloud.tenable.com/api#/resources/bulk-operations/bulk-unlink-agent>`_

        Args:
            agent_id (int): The id of the agent
            scanner_id (int, optional): The id of the scanner

        Returns:
            dict: Task resource
        '''
        self._api.post('scanners/{}/agents/_bulk/unlink'.format(
            self._check('scanner_id', scanner_id, int)),
            json={'items': self._check('agent_ids', agent_ids, list)})

    def bulk_status(self, task_uuid, scanner_id=1):
        '''
        `bulk-operations: bulk-agent-status <https://cloud.tenable.com/api#/resources/bulk-operations/bulk-agent-status>`_

        Args:
            task_uuid (str): The id of the agent
            scanner_id (int, optional): The id of the scanner

        Returns:
            dict: Task resource
        '''
        return self._api.get(
            'scanners/{}/agents/_bulk/{}'.format(
                self._check('scanner_id', scanner_id, int),
                self._check('task_uuid', task_uuid, 'uuid')
            )).json()
