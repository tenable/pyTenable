'''
agent_groups
============

The following methods allow for interaction into the Tenable.io 
`agent groups <https://cloud.tenable.com/api#/resources/agent-groups>`_ 
API endpoints.

Methods available on ``tio.agent_groups``:

.. rst-class:: hide-signature
.. autoclass:: AgentGroupsAPI

    .. automethod:: add_agent
    .. automethod:: configure
    .. automethod:: create
    .. automethod:: delete
    .. automethod:: delete_agent
    .. automethod:: details
    .. automethod:: task_status
'''
from .base import TIOEndpoint


class AgentGroupsAPI(TIOEndpoint):
    def add_agent(self, group_id, *agent_ids, **kw):
        '''
        Adds an agent or multiple agents to the agent group specified.

        `agent-groups: add-agent <https://cloud.tenable.com/api#/resources/agent-groups/add-agent>`_

        Args:
            group_id (int): The id of the group
            *agent_ids (int): The id of the agent
            scanner_id (int, optional): The id of the scanner

        Returns:
            None: Single Agent added successfully
            dict: Task resource if multiple Agents were added.

        Examples:
            Adding a singular agent:

            >>> tio.agent_groups.add_agent(1, 1)

            Adding multiple agents:

            >>> tio.agent_groups.add_agent(1, 1, 2, 3)
        '''
        scanner_id = 1
        if 'scanner_id' in kw:
            scanner_id = kw['scanner_id']

        if len(agent_ids) <= 1:
            # if there is only 1 agent id, we will perform a singular add.
            self._api.put('scanners/{}/agent-groups/{}/agents/{}'.format(
                self._check('scanner_id', scanner_id, int),
                self._check('group_id', group_id, int),
                self._check('agent_id', agent_ids[0], int)
            ))
        else:
            # If there are many agent_ids, then we will want to perform a bulk
            # operation.
            return self._api.post(
                'scanners/{}/agent-groups/{}/agents/_bulk/add'.format(
                    self._check('scanner_id', scanner_id, int),
                    self._check('group_id', group_id, int)),
                json={'items': [self._check('agent_id', i, int) for i in agent_ids]}).json()

    def configure(self, group_id, name, scanner_id=1):
        '''
        Renames an existing agent group.

        `agent-groups: configure <https://cloud.tenable.com/api#/resources/agent-groups/configure>`_

        Args:
            group_id (int): The id of the group
            name (str): The new name for the agent group
            scanner_id (int, optional): The id of the scanner

        Returns:
            None: Agent group updated successfully

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

        `agent-groups: create <https://cloud.tenable.com/api#/resources/agent-groups/create>`_

        Args:
            name (str): The name of the agent group
            scanner_id (int, optional): 
                The id of the scanner to add the agent group to

        Returns:
            dict: 
                The dictionary object representing the newly minted agent group

        Examples:
            >>> group = tio.agent_groups.create('New Agent Group')
        '''
        return self._api.post(
            'scanners/{}/agent-groups'.format(
                self._check('scanner_id', scanner_id, int)
            ), json={'name': self. _check('name', name, str)}).json()

    def delete(self, group_id, scanner_id=1):
        '''
        Delete an agent group.

        `agent-groups: delete <https://cloud.tenable.com/api#/resources/agent-groups/delete>`_

        Args:
            group_id (int): The id of the agent group to delete
            scanner_id (int, optional): The id of the scanner

        Returns:
            None: Agent group deleted successfully

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

        `agent-groups: delete-agent <https://cloud.tenable.com/api#/resources/agent-groups/delete-agent>`_

        Args:
            group_id (int): The id of the agent group to remove the agent from
            *agent_ids (int): The id of the agent to be removed
            scanner_id (int, optional): The id of the scanner

        Returns:
            None: A singular agent was deleted from the group successfully.
            dict: Task resource if multiple agents were requested to be deleted.

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

    def details(self, group_id, scanner_id=1):
        '''
        Retrieve the details about the specified agent group.

        `agent-groups: details <https://cloud.tenable.com/api#/resources/agent-groups/details>`_

        Args:
            group_id (int): The id of the agent group to remove the agent from
            scanner_id (int, optional): The id of the scanner

        Returns:
            dict:
                The dictionary object representing the requested agent group

        Examples:
            >>> group = tio.agent_groups.details(1)
            >>> pprint(group)
        '''
        return self._api.get(
            'scanners/{}/agent-groups/{}'.format(
                self._check('scanner_id', scanner_id, int),
                self._check('group_id', group_id, int)
            )).json()

    def list(self, scanner_id=1):
        '''
        Retrieves the list of agent groups configured

        Args:
            scanner_id (int, optional): The id of the scanner

        Returns:
             list: Listing of agent group resource records

        Examples:
            >>>> for agent_group in tio.agent_groups.list():
            ...     pprint(agent_group)

        '''
        return self._api.get('scanners/{}/agent-groups'.format(
            self._check('scanner_id', scanner_id, int))).json()['groups']

    def task_status(self, group_id, task_uuid, scanner_id=1):
        '''
        Retrieves the current status of a bulk task.

        `bulk-operations: bulk-agent-group-status <https://cloud.tenable.com/api#/resources/bulk-operations/bulk-agent-group-status>`_

        Args:
            group_id (int): The id of the group
            task_uuid (str): The id of the task
            scanner_id (int, optional): The id of the scanner

        Returns:
            dict: Task resource

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
