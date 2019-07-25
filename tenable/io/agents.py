'''
agents
======

The following methods allow for interaction into the Tenable.io
:devportal:`agents <agents>` API endpoints.

Methods available on ``tio.agents``:

.. rst-class:: hide-signature
.. autoclass:: AgentsAPI

    .. automethod:: details
    .. automethod:: list
    .. automethod:: unlink
    .. automethod:: task_status

'''
from .base import TIOIterator, TIOEndpoint

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
    pass


class AgentsAPI(TIOEndpoint):
    def list(self, *filters, **kw):
        '''
        Get the listing of configured agents from Tenable.io.

        :devportal:`agents: list <agents-list>`

        Args:
            *filters (tuple, optional):
                Filters are tuples in the form of ('NAME', 'OPERATOR', 'VALUE').
                Multiple filters can be used and will filter down the data being
                returned from the API.

                Examples:
                    - ``('distro', 'match', 'win')``
                    - ``('name', 'nmatch', 'home')``

                As the filters may change and sortable fields may change over
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
                A list of fields to optionally restrict the wild-card matching
                to.

        Returns:
            :obj:`AgentsIterator`:
                An iterator that handles the page management of the requested
                records.

        Examples:
            Getting the listing of all agents:

            >>> for agent in tio.agents.list():
            ...     pprint(agent)

            Retrieving all of the windows agents:

            >>> for agent in tio.agents.list(('distro', 'match', 'win')):
            ...     pprint(agent)
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

        # The wild-card filter text refers to how the API will pattern match
        # within all fields, or specific fields using the wildcard_fields param.
        if 'wildcard' in kw and self._check('wildcard', kw['wildcard'], str):
            query['w'] = kw['wildcard']

        # The wildcard_fields parameter allows the user to restrict the fields
        # that the wild-card pattern match pertains to.
        if 'wildcard_fields' in kw and self._check(
            'wildcard_fields', kw['wildcard_fields'], list):
            query['wf'] = ','.join(kw['wildcard_fields'])

        # Return the Iterator.
        return AgentsIterator(self._api,
            _limit=limit,
            _offset=offset,
            _pages_total=pages,
            _query=query,
            _path='scanners/{}/agents'.format(scanner_id),
            _resource='agents'
        )

    def details(self, agent_id, scanner_id=1):
        '''
        Retrieves the details of an agent.

        :devportal:`agents: get <agents-get>`

        Args:
            agent_id (int):
                The identifier of the agent.
            scanner_id (int, optional):
                The identifier of the scanner.  Default is 1.

        Returns:
            :obj:`dict`:
                The agent dictionary record.

        Examples:
            >>> agent = tio.agents.details(1)
            >>> pprint(agent)
        '''
        return self._api.get(
            'scanners/{}/agents/{}'.format(
                self._check('scanner_id', scanner_id, int),
                self._check('agent_id', agent_id, int)
            )).json()

    def unlink(self, *agent_ids, **kw):
        '''
        Unlink one or multiple agents from the Tenable.io instance.

        :devportal:`agents: delete <agents-delete>`

        Args:
            *agent_ids (int):
                The ID of the agent to delete
            scanner_id (int, optional):
                The identifier the scanner that the agent communicates to.

        Returns:
            :obj:`dict` or :obj:`None`:
                If unlinking a singular agent, a :obj:`None` response will be
                returned.  If unlinking multiple agents, a :obj:`dict` response
                will be returned with a task record.

        Examples:
            Unlink a singular agent:

            >>> tio.agents.unlink(1)

            Unlink many agents:

            >>> tio.agents.unlink(1, 2, 3)
        '''
        scanner_id = 1
        if 'scanner_id' in kw:
            scanner_id = kw['scanner_id']

        if len(agent_ids) <= 1:
            # as only a singular agent_id was sent over, we can call the delete
            # API
            self._api.delete('scanners/{}/agents/{}'.format(
                self._check('scanner_id', scanner_id, int),
                self._check('agent_id', agent_ids[0], int)
            ))
        else:
            return self._api.post('scanners/{}/agents/_bulk/unlink'.format(
                self._check('scanner_id', scanner_id, int)),
                json={'items': [self._check('agent_ids', i, int) for i in agent_ids]}).json()

    def task_status(self, task_uuid, scanner_id=1):
        '''
        Retrieves the current status of the task requested.

        :devportal:`bulk-operations: bulk-agent-status <bulk-task-agent-status>`

        Args:
            task_uuid (str): The id of the agent
            scanner_id (int, optional): The id of the scanner

        Returns:
            :obj:`dict`:
                Task resource

        Examples:
            >>> item = tio.agents.unlink(21, 22, 23)
            >>> task = tio.agent.task_status(item['task_uuid'])
            >>> pprint(task)
        '''
        return self._api.get(
            'scanners/{}/agents/_bulk/{}'.format(
                self._check('scanner_id', scanner_id, int),
                self._check('task_uuid', task_uuid, 'uuid')
            )).json()
