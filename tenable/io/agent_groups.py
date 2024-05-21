'''
Agent Groups
============

The following methods allow for interaction into the Tenable Vulnerability Management
:devportal:`agent groups <agent-groups>` API endpoints.

Methods available on ``tio.agent_groups``:

.. rst-class:: hide-signature
.. autoclass:: AgentGroupsAPI
    :members:
'''
from .base import TIOEndpoint


class AgentGroupsAPI(TIOEndpoint):
    def add_agent(self, group_id, *agent_ids, **kw):
        '''
        Adds an agent or multiple agents to the agent group specified.

        :devportal:`agent-groups: add-agent <agent-groups-add-agent>`

        Args:
            group_id (int): The id of the group
            *agent_ids (int): The id or uuid of the agent.  If passing multiple, they must all be either numeric id or uuid.
            scanner_id (int, optional): The id of the scanner

        Returns:
            :obj:`dict` or :obj:`None`:
                If adding a singular agent, a :obj:`None` response will be
                returned.  If adding multiple agents, a :obj:`dict` response
                will be returned with a task record.

        Examples:
            Adding a singular agent:

            >>> tio.agent_groups.add_agent(1, 1)

            Adding multiple agents:

            >>> tio.agent_groups.add_agent(1, 1, 2, 3)

            Adding multiple agents by uuid:

            >>> tio.agent_groups.add_agent(1, 'uuid-1', 'uuid-2', 'uuid-3')
        '''
        scanner_id = 1
        if 'scanner_id' in kw:
            scanner_id = kw['scanner_id']

        # we can handle either ids or uuids as the list of items.
        useUuids = len(agent_ids) > 0 and isinstance(agent_ids[0], str)

        if len(agent_ids) <= 1:
            # if there is only 1 agent id, we will perform a singular add.
            self._api.put('scanners/{}/agent-groups/{}/agents/{}'.format(
                self._check('scanner_id', scanner_id, int),
                self._check('group_id', group_id, int),
                self._check('agent_id', agent_ids[0], 'uuid' if useUuids else int)
            ))
        else:
            # If there are many agent_ids, then we will want to perform a bulk
            # operation.
            return self._api.post(
                'scanners/{}/agent-groups/{}/agents/_bulk/add'.format(
                    self._check('scanner_id', scanner_id, int),
                    self._check('group_id', group_id, int)),
                json={'items': [self._check('agent_id', i, 'uuid' if useUuids else int) for i in agent_ids]}).json()

    def configure(self, group_id, name, scanner_id=1):
        '''
        Renames an existing agent group.

        :devportal:`agent-groups: configure <agent-groups-configure>`

        Args:
            group_id (int): The id of the group
            name (str): The new name for the agent group
            scanner_id (int, optional): The id of the scanner

        Returns:
            :obj:`None`

        Examples:
            >>> tio.agent_groups.configure(1, 'New Name')
        '''
        self._api.put('scanners/{}/agent-groups/{}'.format(
            self._check('scanner_id', scanner_id, int),
            self._check('group_id', group_id, int)
        ), json={'name': self._check('name', name, str)}).json()

    def create(self, name, scanner_id=1):
        '''
        Creates a new agent group.

        :devportal:`agent-groups: create <agent-groups-create>`

        Args:
            name (str): The name of the agent group
            scanner_id (int, optional):
                The id of the scanner to add the agent group to

        Returns:
            :obj:`dict`:
                The dictionary object representing the newly minted agent group

        Examples:
            >>> group = tio.agent_groups.create('New Agent Group')
        '''
        return self._api.post(
            'scanners/{}/agent-groups'.format(
                self._check('scanner_id', scanner_id, int)
            ), json={'name': self._check('name', name, str)}).json()

    def delete(self, group_id, scanner_id=1):
        '''
        Delete an agent group.

        :devportal:`agent-groups: delete <agent-groups-delete>`

        Args:
            group_id (int): The id of the agent group to delete
            scanner_id (int, optional): The id of the scanner

        Returns:
            :obj:`None`

        Examples:
            >>> tio.agent_groups.delete(1)
        '''
        self._api.delete('scanners/{}/agent-groups/{}'.format(
            self._check('scanner_id', scanner_id, int),
            self._check('group_id', group_id, int)
        ))

    def delete_agent(self, group_id, *agent_ids, **kw):
        '''
        Delete one or many agents from an agent group.

        :devportal:`agent-groups: delete-agent <agent-groups-delete-agent>`

        Args:
            group_id (int): The id of the agent group to remove the agent from
            *agent_ids (int): The id of the agent to be removed
            scanner_id (int, optional): The id of the scanner

        Returns:
            :obj:`dict` or :obj:`None`:
                If deleting a singular agent, a :obj:`None` response will be
                returned.  If deleting multiple agents, a :obj:`dict` response
                will be returned with a Job resource record.

        Examples:
            Delete a singular agent from an agent group:

            >>> tio.agent_groups.delete_agent(1, 1)

            Delete multiple agents from an agent group:

            >>> tio.agent_groups.delete_agent(1, 1, 2, 3)
        '''
        scanner_id = 1
        if 'scanner_id' in kw:
            scanner_id = kw['scanner_id']

        if len(agent_ids) <= 1:
            # if only a singular agent_id was passed, then we will want to
            self._api.delete('scanners/{}/agent-groups/{}/agents/{}'.format(
                self._check('scanner_id', scanner_id, int),
                self._check('group_id', group_id, int),
                self._check('agent_id', agent_ids[0], int)
            ))
        else:
            # if multiple agent ids were requested to be deleted, then we will
            # call the bulk deletion API.
            return self._api.post(
                'scanners/{}/agent-groups/{}/agents/_bulk/remove'.format(
                    self._check('scanner_id', scanner_id, int),
                    self._check('group_id', group_id, int)),
                json={'items': [self._check('agent_ids', i, int) for i in agent_ids]}).json()

    def details(self, group_id, *filters, **kw):
        '''
        Retrieve the details about the specified agent group.

        :devportal:`agent-groups: details <agent-groups-details>`

        Args:
            group_id (int): The id of the agent group.
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
                together.  ``and`` will inform the API that all the filter
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
                A tuple of tuples identifying the field and sort order of
                the field.
            wildcard (str, optional):
                A string to pattern match against all available fields returned.
            wildcard_fields (list, optional):
                A list of fields to optionally restrict the wild-card matching
                to.

        Returns:
            :obj:`dict`:
                The dictionary object representing the requested agent group

        Examples:
            >>> group = tio.agent_groups.details(1)
            >>> pprint(group)
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

        # If the offset was set to something other than the default starting
        # point of 0, then we will update offset to reflect that.
        if 'offset' in kw and self._check('offset', kw['offset'], int):
            query['offset'] = kw['offset']

        # The limit parameter affects how many records at a time we will pull
        # from the API.  The default in the API is set to 50, however we can
        # pull any variable amount.
        if 'limit' in kw and self._check('limit', kw['limit'], int):
            query['limit'] = kw['limit']

        return self._api.get(
            'scanners/{}/agent-groups/{}'.format(
                self._check('scanner_id', scanner_id, int),
                self._check('group_id', group_id, int)
            ), params=query
        ).json()

    def list(self, scanner_id=1):
        '''
        Retrieves the list of agent groups configured

        :devportal:`agent-groups: list <agent-groups-list>`

        Args:
            scanner_id (int, optional): The id of the scanner

        Returns:
            :obj:`list`:
                Listing of agent group resource records

        Examples:
            >>>> for agent_group in tio.agent_groups.list():
            ...     pprint(agent_group)

        '''
        return self._api.get('scanners/{}/agent-groups'.format(
            self._check('scanner_id', scanner_id, int))).json()['groups']

    def task_status(self, group_id, task_uuid, scanner_id=1):
        '''
        Retrieves the current status of a bulk task.

        :devportal:`bulk-operations: bulk-agent-group-status <bulk-task-agent-group-status>`

        Args:
            group_id (int): The id of the group
            task_uuid (str): The id of the task
            scanner_id (int, optional): The id of the scanner

        Returns:
            :obj:`dict`:
                Task resource

        Examples:
            >>> item = tio.agent_groups.add_agent(1, 21, 22, 23)
            >>> task = tio.agent_groups.task_status(item['task_uuid'])
            >>> pprint(task)
        '''
        return self._api.get(
            'scanners/{}/agent-groups/{}/agents/_bulk/{}'.format(
                self._check('scanner_id', scanner_id, int),
                self._check('group_id', group_id, int),
                self._check('task_uuid', task_uuid, 'uuid')
            )).json()
