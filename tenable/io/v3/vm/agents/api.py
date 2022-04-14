'''
Agents
======

The following methods allow for interaction into the Tenable.io
:devportal:`agents <agents>` API endpoints.

Methods available on ``tio.v3.vm.agents``:

.. rst-class:: hide-signature
.. autoclass:: AgentsAPI
    :members:
'''
from typing import Dict, Union
from uuid import UUID

from requests import Response

from tenable.io.v3.base.endpoints.explore import ExploreBaseEndpoint
from tenable.io.v3.base.iterators.explore_iterator import (CSVChunkIterator,
                                                           SearchIterator)
from tenable.io.v3.base.iterators.tio_iterator import TIOIterator
from tenable.io.v3.vm.agents.schema import AgentFilterSchema, AgentSchema
from tenable.utils import dict_clean


class AgentsAPI(ExploreBaseEndpoint):
    '''
    This class contains methods related to Agents API
    '''
    _path: str = 'api/v3/agents'
    _conv_json: bool = True
    _schema = AgentSchema()

    def details(self, agent_id: UUID) -> Dict:
        '''
        Retrieves the details of an agent.

        :devportal:`agents: get <agents-get>`

        Args:
            agent_id (uuid.UUID): The unique identifier of the agent.

        Returns:
            :obj:`dict`:
                The agent dictionary record.

        Examples:
            >>> agent = tio.v3.vm.agents.details(
            ...     '00000000-0000-0000-0000-000000000000'
            ... )
            >>> pprint(agent)
        '''
        return super()._details(agent_id)

    def list_agents_from_group(self, group_id: int, **kwargs) -> Dict:
        '''
        List all the agents for the specified agent group.

        :devportal:`agents: list-agents-from-group <agent-group-list-agents>`

        Args:
            group_id (int):
                The unique identifier of the agent group.
            filters (list, optional):
                Filters are list of tuples in the form of
                ('NAME', 'OPERATOR', 'VALUE'). Multiple filters can be used
                and will filter down the data being returned from the API.

                Examples:
                    - ``[('distro', 'match', 'win'),
                    ('name', 'nmatch', 'home')]``

                As the filters may change and sortable fields may change over
                time, it's highly recommended that you look at the output of
                the `filters:agents-filters <https://developer.tenable.com/
                reference/io-filters-agents-list>`
                endpoint to get more details.
            filter_type (str, optional):
                The filter_type operator determines how the filters are
                combined together.  ``and`` will inform the API that all of
                the filter conditions must be met for an agent to be returned,
                whereas ``or`` would mean that if any of the conditions are
                met, the agent record will be returned.
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
                A string to pattern match against all available fields.
            wildcard_fields (list, optional):
                A list of fields to optionally restrict the wild-card matching
                to.
        Returns:
            :obj:`dict`:
                Returns a list of agents for an agent group.

        Examples:
            >>> agent = tio.v3.vm.agents.list_agents_from_group(
            ...     group_id=469892,
            ...     filters = [('platform', 'match', ['window'])],
            ...     filter_type = 'and',
            ...     limit = 100,
            ...     offset = 0,
            ...     sort = [('name','asc'),('platform', 'asc')],
            ...     wildcard = "IYKKQIGOBWXUXOZIBURFENPNMGZOSWBUKVCD",
            ...     wildcard_fields = ['name']
            ... )
            >>> pprint(agent)
        '''
        payload: dict = dict_clean(kwargs)

        # Let's fetch all the available filters for scan agent
        if payload.get('filters') is not None:
            AgentFilterSchema.populate_filters(
                self._api, path='api/v3/definitions/scans/agents'
            )

        # Let's validate schema using marshmallow
        payload = self._schema.dump(self._schema.load(payload))

        # Let's build the query params
        query: dict = {}
        if 'filters' in payload:
            query['f'] = []
            for item in payload.get('filters'):
                field = item['field']
                oper = item['operator']
                value = ','.join(item['value'])
                query['f'].append(f'{field}:{oper}:{value}')

        if 'sort' in payload:
            query['sort'] = [f'{i[0]}:{i[1]}' for i in payload.get('sort')]

        if 'filter_type' in payload:
            query['ft'] = payload.get('filter_type')

        if 'wildcard' in payload:
            query['w'] = payload.get('wildcard')

        if 'wildcard_fields' in payload:
            query['wf'] = ','.join(payload.get('wildcard_fields'))

        api_path = f'api/v3/agent-groups/{group_id}/agents'

        return TIOIterator(
            self._api,
            _limit=payload.get('limit', 50),
            _offset=payload.get('offset', 0),
            _pages_total=None,
            _query=query,
            _path=api_path,
            _resource='agents'
        )

    def search(self,
               **kwargs) -> Union[SearchIterator, CSVChunkIterator, Response]:
        '''
        Search and retrieve the agents based on supported conditions.
        Args:
            fields (list, optional):
                The list of field names to return from the Tenable API.

                Example:
                    >>> ['field1', 'field2']

            filter (tuple, dict, optional):
                A nestable filter object detailing how to filter the results
                down to the desired subset.
                Examples:
                    >>> ('or', ('and', ('test', 'oper', '1'),
                    ...                 ('test', 'oper', '2')
                    ...             ),
                    ...     'and', ('test', 'oper', 3)
                    ... )
                    >>> {
                    ...  'or': [{
                    ...      'and': [{
                    ...              'value': '1',
                    ...              'operator': 'oper',
                    ...              'property': '1'
                    ...          },
                    ...          {
                    ...              'value': '2',
                    ...              'operator': 'oper',
                    ...              'property': '2'
                    ...          }
                    ...      ]
                    ...  }],
                    ...  'and': [{
                    ...      'value': '3',
                    ...      'operator': 'oper',
                    ...      'property': 3
                    ...  }]
                    ... }
                As the filters may change and sortable fields may change over
                time, it's highly recommended that you look at the output of
                the :py:meth:`tio.v3.definitions.vm.agents()`
                endpoint to get more details.
            sort (list[tuple], optional):
                A list of dictionaries describing how to sort the data
                that is to be returned.
                Examples:
                    >>> [('field_name_1', 'asc'),
                    ...      ('field_name_2', 'desc')]
            limit (int, optional):
                Number of objects to be returned in each request.
                Default and max_limit is 200.
            next (str, optional):
                The pagination token to use when requesting the next page of
                results. This token is presented in the previous response.
            return_resp (bool, optional):
                If set to true, will override the default behavior to return
                a requests.Response Object to the user.
            return_csv (bool, optional):
                If set to true, it will return the CSV response or
                iterable (based on return_resp flag). Iterator returns all
                rows in text/csv format for each call with row headers.
        :Returns:
            - Iterable:
                The iterable that handles the pagination for the job.
            - requests.Response:
                If ``return_resp`` is set to ``True``, then a response
                object is returned instead of an iterable.

        Examples:
            >>> tio.v3.vm.agents.search(
            ... filter=('id', 'eq', '00089a45-44a5-4620-bf9f-75ebedc6cc6c'),
            ... fields=['id'], limit=2)
        '''
        iclass = SearchIterator
        if kwargs.get('return_csv', False):
            iclass = CSVChunkIterator
        return super()._search(
            iterator_cls=iclass,
            sort_type=self._sort_type.default,
            api_path=f'{self._path}/search',
            resource='agents',
            **kwargs
        )

    def task_status(self, task_id: UUID) -> Dict:
        '''
        Retrieves the current status of the task requested.

        :devportal:`bulk-operations: bulk-agent-status
        <bulk-task-agent-status>`

        Args:
            task_id (uuid.UUID): The unique identifier of the agent.

        Returns:
            :obj:`dict`:
                Task resource

        Examples:
            >>> item = tio.v3.vm.agents.unlink(
            ...     '00000000-0000-0000-0000-000000000000',
            ...     '00000000-0000-0000-0000-000000000001',
            ...     '00000000-0000-0000-0000-000000000002'
            ... )
            >>> task = tio.v3.vm.agent.task_status(item['task_id'])
            >>> pprint(task)
        '''
        return self._get(f'_bulk/{task_id}')

    def unlink(self, *agent_ids: UUID) -> Union[Dict, None]:
        '''
        Unlink one or multiple agents from the Tenable.io instance.

        :devportal:`agents: delete <agents-delete>`

        Args:
            *agent_ids (uuid.UUID): The unique identifier of the agent to delete

        Returns:
            :obj:`dict` or :obj:`None`:
                If unlinking a singular agent, a :obj:`None` response will be
                returned.  If unlinking multiple agents, a :obj:`dict` response
                will be returned with a task record.

        Examples:
            Unlink a singular agent:

            >>> tio.v3.vm.agents.unlink(
            ...     '00000000-0000-0000-0000-000000000000'
            ... )

            Unlink many agents:

            >>> tio.v3.vm.agents.unlink(
            ...     '00000000-0000-0000-0000-000000000000',
            ...     '00000000-0000-0000-0000-000000000001',
            ...     '00000000-0000-0000-0000-000000000002'
            ... )
        '''

        if len(agent_ids) <= 1:
            # For singular agent_id was sent over, we can call the delete API
            self._delete(f'{agent_ids[0]}')
        else:
            # For bulk agent id we call agent bulk operation API endpoint
            payload: dict = {'items': [i for i in agent_ids]}
            payload = self._schema.dump(self._schema.load(payload))
            return self._post('_bulk/unlink', json=payload)

    def add_agents_to_network(self, *agent_ids: UUID, **kwargs) -> Dict:
        '''
        Creates a bulk operation task to add agents to a custom network.

        :devportal:`bulk-operations: add-agents-to-network
        <io-agent-bulk-operations-add-to-network>`

        Args:
            *agent_ids (uuid.UUID): The unique identifier of the agent to add
            all_agents (bool, optional):
                Indicates whether or not to match against all agents.
            wildcard (str, optional):
                A string used to match against all string-like attributes
                of an agent.
            filters (list, optional):
                An array of string or numeric operations to match against
                agents.
                For Example:
                    - ``['field:operator:value', 'name:match:laptop']``
            filter_type (str, optional):
                Indicates how to combine the filters conditions.
                Possible values are ``and`` or ``or``.
            hardcoded_filters (list, optional):
                Additional filters that will always be added as
                ``and`` conditions.
            not_items (list, optional):
                An array of agent IDs or UUIDs to exclude from the criteria
                filter.
        Returns:
            :obj:`dict`:
                Returned dict object if Tenable.io successfully creates
                the bulk operation task.

        Examples:
            Adding multiple agent to custom network:

            >>> tio.v3.vm.agents.add_agents_to_network(
            ...     '00000000-0000-0000-0000-000000000000',
            ...     '00000000-0000-0000-0000-000000000001'
            ... )
        '''
        payload: dict = {
            'criteria': {
                'all_agents': kwargs.get('all_agents'),
                'wildcard': kwargs.get('wildcard'),
                'filters': kwargs.get('filters'),
                'filter_type': kwargs.get('filter_type'),
                'hardcoded_filters': kwargs.get('hardcoded_filters')
            },
            'items': [item for item in agent_ids] or None,
            'not_items': kwargs.get('not_items'),
        }
        payload = dict_clean(payload)
        # Let's validate the schema using marshmallow
        payload = self._schema.dump(self._schema.load(payload))

        return self._post('_bulk/addToNetwork', json=payload)

    def remove_agent_from_network(self, *agent_ids: UUID, **kwargs) -> Dict:
        '''
        Creates a bulk operation task to remove agents from a custom network.

        :devportal:`bulk-operations: remove-agents-from-network
        <io-agent-bulk-operations-remove-from-network>`

        Args:
            *agent_ids (uuid.UUID): The unique identifier of the agent to remove
            all_agents (bool, optional):
                Indicates whether or not to match against all agents.
            wildcard (str, optional):
                A string used to match against all string-like attributes
                of an agent.
            filters (list, optional):
                An array of string or numeric operations to match against
                agents.
                For Example:
                    - ``['field:operator:value', 'name:match:laptop']``
            filter_type (str, optional):
                Indicates how to combine the filters conditions.
                Possible values are ``and`` or ``or``.
            hardcoded_filters (list, optional):
                Additional filters that will always be added as
                ``and`` conditions.
            not_items (list, optional):
                An array of agent IDs or UUIDs to exclude from the criteria
                filter.
        Returns:
            :obj:`dict`:
                Returned dict object if Tenable.io successfully creates
                the bulk operation task.

        Examples:
            Removing multiple agent to network:

            >>> tio.v3.vm.agents.remove_agent_from_network(
            ...     '00000000-0000-0000-0000-000000000000',
            ...     '00000000-0000-0000-0000-000000000001'
            ... )
        '''
        payload: dict = {
            'criteria': {
                'all_agents': kwargs.get('all_agents'),
                'wildcard': kwargs.get('wildcard'),
                'filters': kwargs.get('filters'),
                'filter_type': kwargs.get('filter_type'),
                'hardcoded_filters': kwargs.get('hardcoded_filters')
            },
            'items': [item for item in agent_ids] or None,
            'not_items': kwargs.get('not_items'),
        }
        payload = dict_clean(payload)

        # Let's validate the schema using marshmallow
        payload = self._schema.dump(self._schema.load(payload))

        return self._post('_bulk/removeFromNetwork', json=payload)

    def send_instructuion_to_agent(self,
                                   *agent_ids,
                                   directive_type: str,
                                   **kwargs) -> Dict:
        '''
        Create instructions for agents to perform. Instructions include
        restarting or changing local product settings.

        :devportal:`bulk-operations: send-instructions-to-agent
        <io-agent-bulk-operations-directive>`

        Args:
            *agent_ids (uuid.UUID):
                The unique identifier of the agent to remove
            directive_type (str):
                The type of instruction to perform.
                Possible instructions are ``restart`` and ``settings``.
            all_agents (bool, optional):
                Indicates whether or not to match against all agents.
            wildcard (str, optional):
                A string used to match against all string-like attributes
                of an agent.
            filters (list, optional):
                An array of string or numeric operations to match against
                agents.
                For Example:
                    - ``['field:operator:value', 'name:match:laptop']``
            filter_type (str, optional):
                Indicates how to combine the filters conditions.
                Possible values are ``and`` or ``or``.
            hardcoded_filters (list, optional):
                Additional filters that will always be added as
                ``and`` conditions.
            not_items (list, optional):
                An array of agent IDs or UUIDs to exclude from the criteria
                filter.
            options (dict, optional):
                Additional information about the instruction to perform.
                For example:
                    if the type is ``restart`` you can use the options
                    ``'hard': true`` or ``'idle': true``.
        Returns:
            :obj:`dict`:
                Returned dict if Tenable.io successfully creates
                the bulk operation task.

        Examples:
            Sending instruction to multiple agents:

            >>> tio.v3.vm.agents.send_instructuion_to_agent(
            ...     '334b962a-ac03-4336-9ebb-a06b169576e0',
            ...     directive_type = 'restart')
        '''
        payload: dict = {
            'criteria': {
                'all_agents': kwargs.get('all_agents'),
                'wildcard': kwargs.get('wildcard'),
                'filters': kwargs.get('filters'),
                'filter_type': kwargs.get('filter_type'),
                'hardcoded_filters': kwargs.get('hardcoded_filters')
            },
            'items': [item for item in agent_ids] or None,
            'not_items': kwargs.get('not_items'),
            'directive': {
                'type': directive_type,
                'options': kwargs.get('options')
            }
        }
        payload = dict_clean(payload)

        # Let's validate the schema using marshmallow
        payload = self._schema.dump(self._schema.load(payload))

        return self._post('_bulk/directive', json=payload)
