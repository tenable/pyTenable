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

from tenable.io.v3.base.endpoints.explore import ExploreBaseEndpoint
from tenable.io.v3.vm.agent_groups.schema import AgentGroupSchema


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
            group_id (UUID): The unique identifier of the group
            agent_ids (UUID): The unique identifier of the agent

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
            group_id (UUID): The unique identifier of the group
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
            group_id (UUID): The unique identifier of the agent group

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
            group_id (UUID): The unique identifier of the agent group to
                             remove the agent from
            *agent_ids (UUID): The unique identifier of the agent to be removed

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

    def details(self):
        raise NotImplementedError('This method will be updated later'
                                  'once the filter API will develop')

    def search(self):
        raise NotImplementedError('Search and Filter functionality '
                                  'will be updated later.')

    def task_status(self, group_id: UUID, task_id: UUID) -> Dict:
        '''
        Retrieves the current status of a bulk task.

        :devportal:`bulk-operations: bulk-agent-group-status
        <bulk-task-agent-group-status>`

        Args:
            group_id (UUID): The unique identifier of the group
            task_id (UUID): The unique identifier of the task

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
