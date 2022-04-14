'''
Agent Groups
============

The following methods allow for interaction into the Tenable.io
:devportal:`agent groups <agent-groups>` API endpoints.

Methods available on ``tio.v3.vm.agent_groups``:

.. rst-class:: hide-signature
.. autoclass:: AgentGroupsAPI
    :members:
'''
from typing import Dict, Union
from uuid import UUID

from requests import Response

from tenable.io.v3.base.endpoints.explore import ExploreBaseEndpoint
from tenable.io.v3.base.iterators.explore_iterator import (CSVChunkIterator,
                                                           SearchIterator)
from tenable.io.v3.vm.agent_groups.schema import (AgentGroupFilterSchema,
                                                  AgentGroupSchema)
from tenable.utils import dict_clean


class AgentGroupsAPI(ExploreBaseEndpoint):
    '''
    This class contain all methods related to Agent Groups
    '''
    _path: str = 'api/v3/agent-groups'
    _conv_json: bool = True
    _schema = AgentGroupSchema()

    def add_agent(self, group_id: UUID, *agent_ids: UUID) -> Union[None, Dict]:
        '''
        Adds an agent or multiple agents to the agent group specified.

        :devportal:`agent-groups: add-agent <agent-groups-add-agent>`

        Args:
            group_id (uuid.UUID): The unique identifier of the group
            agent_ids (uuid.UUID): The unique identifier of the agent

        Returns:
            :obj:`dict` or :obj:`None`:
                If adding a singular agent, a :obj:`None` response will be
                returned.  If adding multiple agents, a :obj:`dict` response
                will be returned with a task record.

        Examples:
            Adding a singular agent:

            >>> tio.v3.vm.agent_groups.add_agent(
            ...    'ef62870e-fe2f-4ba9-98b7-43d3a53ffe85',
            ...    '1bd703af-b2aa-4a82-ad8d-b883381a873f'
            ... )

            Adding multiple agents:

            >>> tio.v3.vm.agent_groups.add_agent(
            ...    'ef62870e-fe2f-4ba9-98b7-43d3a53ffe85',
            ...    '1drge3af-b2aa-4a81-ad8d-b883381a873f',
            ...    '1bgfdgaf-b2aa-4a82-ad8d-b834581a873f',
            ...    'bsbsbbdf-b2aa-4a83-ad8d-b867581a873f'
            ... )
        '''
        if len(agent_ids) <= 1:
            # if there is only 1 agent id, we will perform a singular add.
            self._put(f'{group_id}/agents/{agent_ids[0]}')
        else:
            # If there are many agent_ids, then we will want to perform a
            # bulk operation.
            payload: dict = {'items': [i for i in agent_ids]}
            payload = self._schema.dump(self._schema.load(payload))
            return self._post(
                f'{group_id}/agents/_bulk/add',
                json=payload
            )

    def configure(self, group_id: UUID, name: str) -> Dict:
        '''
        Renames an existing agent group.

        :devportal:`agent-groups: configure <agent-groups-configure>`

        Args:
            group_id (uuid.UUID): The unique identifier of the group
            name (str): The new name for the agent group

        Returns:
            :obj:`dict`

        Examples:
            >>> tio.v3.vm.agent_groups.configure(
            ...    'ef62870e-fe2f-4ba9-98b7-43d3a53ffe85',
            ...    'New Name'
            ... )
        '''
        payload: dict = {'name': name}
        payload = self._schema.dump(self._schema.load(payload))
        return self._put(f'{group_id}', json=payload)

    def create(self, name: str) -> Dict:
        '''
        Creates a new agent group.

        :devportal:`agent-groups: create <agent-groups-create>`

        Args:
            name (str): The name of the agent group

        Returns:
            :obj:`dict`:
                The dictionary object representing the newly minted agent group

        Examples:
            >>> group = tio.v3.vm.agent_groups.create('New Agent Group')
        '''
        payload: dict = {'name': name}
        payload = self._schema.dump(self._schema.load(payload))
        return self._post(json=payload)

    def delete(self, group_id: UUID) -> None:
        '''
        Delete an agent group.

        :devportal:`agent-groups: delete <agent-groups-delete>`

        Args:
            group_id (uuid.UUID): The unique identifier of the agent group

        Returns:
            :obj:`None`

        Examples:
            >>> tio.v3.vm.agent_groups.delete(
            ...     'ef62870e-fe2f-4ba9-98b7-43d3a53ffe85'
            ... )
        '''
        self._delete(f'{group_id}')

    def delete_agent(self,
                     group_id: UUID,
                     *agent_ids: UUID
                     ) -> Union[None, Dict]:
        '''
        Delete one or many agents from an agent group.

        :devportal:`agent-groups: delete-agent <agent-groups-delete-agent>`

        Args:
            group_id (uuid.UUID): The unique identifier of the agent group to
                             remove the agent from
            *agent_ids (uuid.UUID): The unique identifier of the agent to be removed

        Returns:
            :obj:`dict` or :obj:`None`:
                If deleting a singular agent, a :obj:`None` response will be
                returned.  If deleting multiple agents, a :obj:`dict` response
                will be returned with a Job resource record.

        Examples:
            Delete a singular agent from an agent group:

            >>> tio.v3.vm.agent_groups.delete_agent(
            ...     'ef62870e-fe2f-4ba9-98b7-43d3a53ffe85',
            ...     'bytsbg56-fe2f-4ba9-98b7-vrt23tert453'
            ... )

            Delete multiple agents from an agent group:

            >>> tio.v3.vm.agent_groups.delete_agent(
            ...     'ef62870e-fe2f-4ba9-98b7-43d3a53ffe85',
            ...     'fdbd563f-gr45-45gf-98b7-65fghgdfgrt5',
            ...     'ythtbf56-fe2f-4ba9-98b7-hfghr345353f',
            ...     'dfgdfd43-fe2f-4ba9-98b7-bdf43fgghf34'
            ... )
        '''
        if len(agent_ids) <= 1:
            # if only a singular agent_id was passed, then we will want to
            self._delete(f'{group_id}/agents/{agent_ids[0]}')
        else:
            # if multiple agent ids were requested to be deleted, then we will
            # call the bulk deletion API.
            payload: dict = {'items': [i for i in agent_ids]}
            payload = self._schema.dump(self._schema.load(payload))
            return self._post(
                f'{group_id}/agents/_bulk/remove',
                json=payload
            )

    def details(self, group_id: UUID, *filters, **kwargs) -> Dict:
        '''
        Retrieve the details about the specified agent group.

        :devportal:`agent-groups: details <agent-groups-details>`

        Args:
            group_id (uuid.UUID): The unique identifier of the agent group.
            *filters (tuple, optional):
                Filters are tuples in the form of
                ('NAME', 'OPERATOR', 'VALUE').
                Multiple filters can be used and will filter down
                the data being returned from the API.

                Examples:
                    - ``('distro', 'match', 'win')``
                    - ``('name', 'nmatch', 'home')``

                As the filters may change and sortable fields may change over
                time, it's highly recommended that you look at the output of
                the `filters:agents-filters <https://cloud.tenable.com/api#/
                resources/filters/agents-filters>`_
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
                A string to pattern match against all available fields returned
            wildcard_fields (list, optional):
                A list of fields to optionally restrict the wild-card matching
                to.

        Returns:
            :obj:`dict`:
                The dictionary object representing the requested agent group

        Examples:
            >>> group = tio.v3.vm.agent_groups.details(
            ...     'ea81c0e9-a041-45d6-a654-80570d6bee97'
            ... )
            >>> pprint(group)
        '''
        payload: dict = dict_clean(kwargs)

        # Let's fetch all the available filters for scan agent
        if filters:
            payload['filters'] = list(filters)
            AgentGroupFilterSchema.populate_filters(
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

        return self._get(f'{group_id}', params=query)

    def search(self,
               **kwargs) -> Union[SearchIterator, CSVChunkIterator, Response]:
        '''
        Search agent groups based on supported conditions.
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
                the :py:meth:`tio.v3.definitions.vm.agent_groups()`
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
            >>> tio.v3.vm.agent_groups.search(
            ...     fields=['id', 'name'],
            ...     filter=('id', 'eq', [1,2]),
            ...     sort=[('id', 'asc')],
            ...     limit=10
            ... )
        '''
        iclass = SearchIterator

        if kwargs.get('return_csv', False):
            iclass = CSVChunkIterator

        return super()._search(
            iterator_cls=iclass,
            sort_type=self._sort_type.default,
            api_path=f'{self._path}/search',
            resource='agent_groups',
            **kwargs
        )

    def task_status(self, group_id: UUID, task_id: UUID) -> Dict:
        '''
        Retrieves the current status of a bulk task.

        :devportal:`bulk-operations: bulk-agent-group-status
        <bulk-task-agent-group-status>`

        Args:
            group_id (uuid.UUID): The unique identifier of the group
            task_id (uuid.UUID): The unique identifier of the task

        Returns:
            :obj:`dict`:
                Task resource

        Examples:
            >>> item = tio.v3.vm.agent_groups.add_agent(
            ...      'ef62870e-fe2f-4ba9-98b7-43d3a53ffe85',
            ...      'fdbd563f-gr45-45gf-98b7-65fghgdfgrt5',
            ...      'ythtbf56-fe2f-4ba9-98b7-hfghr345353f',
            ...      'dfgdfd43-fe2f-4ba9-98b7-bdf43fgghf34'
            ... )
            >>> task = tio.v3.vm.agent_groups.task_status(item['task_id'])
            >>> pprint(task)
        '''
        return self._get(f'{group_id}/agents/_bulk/{task_id}')

    def send_instruction_to_agents_in_group(self,
                                            group_id: UUID,
                                            *agent_ids: UUID,
                                            directive_type: str,
                                            **kwargs) -> Dict:
        '''
        Create instructions for agents in an agent group to perform.

        :devportal:`bulk-operations: send-instructions-to-agent
        <io-agent-bulk-operations-directive>`

        Args:
            group_id (uuid.UUID):
                The unique identifier of the agent_group
            *agent_ids (uuid.UUID):
                The unique identifier of the agent
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

            >>> tio.v3.vm.agent_groups.send_instruction_to_agents_in_group(
            ...     '00000000-0000-0000-0000-000000000000',
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

        return self._post(f'{group_id}/agents/_bulk/directive', json=payload)
