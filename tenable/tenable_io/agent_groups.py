from tenable.tenable_io.base import TIOEndpoint

class AgentGroupsAPI(TIOEndpoint):
    def add_agent(self, group_id, agent_id, scanner_id=1):
        '''
        `agent-groups: add-agent <https://cloud.tenable.com/api#/resources/agent-groups/add-agent>`_

        Args:
            group_id (int): The id of the group
            agent_id (int): The id of the agent
            scanner_id (int, optional): The id of the scanner

        Returns:
            None: Agent added successfully
        '''
        self._api.put('scanners/{}/agent-groups/{}/agents/{}'.format(
            self._check('scanner_id', scanner_id, int),
            self._check('group_id', group_id, int),
            self._check('agent_id', agent_id, int)
        ))

    def bulk_add_agent(self, group_id, agent_ids, scanner_id=1):
        '''
        `bulk-operations: bulk-add-agent <https://cloud.tenable.com/api#/resources/bulk-operations/bulk-add-agent>`_

        Args:
            group_id (int): The id of the group
            agent_id (int): The id of the agent
            scanner_id (int, optional): The id of the scanner

        Returns:
            dict: Task resource
        '''
        self._api.post('scanners/{}/agent-groups/{}/agents/_bulk/add'.format(
            self._check('scanner_id', scanner_id, int),
            self._check('group_id', group_id, int)),
            json={'items': self._check('agent_ids', agent_ids, list)})


    def configure(self, group_id, name, scanner_id=1):
        '''
        `agent-groups: configure <https://cloud.tenable.com/api#/resources/agent-groups/configure>`_

        Args:
            group_id (int): The id of the group
            name (str): The new name for the agent group
            scanner_id (int, optional): The id of the scanner

        Returns:
            None: Agent group updated successfully
        '''
        self._api.put('scanners/{}/agent-groups/{}'.format(
            self._check('scanner_id', scanner_id, int),
            self._check('group_id', group_id, int)
        ), json={'name': self._check('name', name, str)}).json()

    def create(self, name, scanner_id=1):
        '''
        `agent-groups: create <https://cloud.tenable.com/api#/resources/agent-groups/create>`_

        Args:
            name (str): The name of the agent group
            scanner_id (int, optional): 
                The id of the scanner to add the agent group to

        Returns:
            dict: 
                The dictionary object representing the newly minted agent group 
        '''
        return self._api.post(
            'scanners/{}/agent-groups'.format(
                self._check('scanner_id', scanner_id, int)
            ), json={'name': self. _check('name', name, str)}).json()

    def delete(self, group_id, scanner_id=1):
        '''
        `agent-groups: delete <https://cloud.tenable.com/api#/resources/agent-groups/delete>`_

        Args:
            group_id (int): The id of the agent group to delete
            scanner_id (int, optional): The id of the scanner

        Returns:
            None: Agent group deleted successfully
        '''
        self._api.delete('scanners/{}/agent-groups/{}'.format(
            self._check('scanner_id', scanner_id, int),
            self._check('group_id', group_id, int)
        ))

    def delete_agent(self, group_id, agent_id, scanner_id=1):
        '''
        `agent-groups: delete-agent <https://cloud.tenable.com/api#/resources/agent-groups/delete-agent>`_

        Args:
            group_id (int): The id of the agent group to remove the agent from
            agent_id (int): The id of the agent to be removed
            scanner_id (int, optional): The id of the scanner

        Returns:
            None: The agent was deleted from the group successfully.
        '''
        self._api.delete('scanners/{}/agent-groups/{}/agents/{}'.format(
            self._check('scanner_id', scanner_id, int),
            self._check('group_id', group_id, int),
            self._check('agent_id', agent_id, int)
        ))

    def bulk_delete_agent(self, group_id, agent_ids, scanner_id=1):
        '''
        `bulk-operations: bulk-add-agent <https://cloud.tenable.com/api#/resources/bulk-operations/bulk-remove-agent>`_

        Args:
            group_id (int): The id of the group
            agent_id (int): The id of the agent
            scanner_id (int, optional): The id of the scanner

        Returns:
            dict: Task resource
        '''
        self._api.post('scanners/{}/agent-groups/{}/agents/_bulk/add'.format(
            self._check('scanner_id', scanner_id, int),
            self._check('group_id', group_id, int)),
            json={'items': self._check('agent_ids', agent_ids, list)})

    def details(self, group_id, scanner_id=1):
        '''
        `agent-groups: details <https://cloud.tenable.com/api#/resources/agent-groups/details>`_

        Args:
            group_id (int): The id of the agent group to remove the agent from
            scanner_id (int, optional): The id of the scanner

        Returns:
            dict:
                The dictionary object representing the requested agent group
        '''
        return self._api.get(
            'scanners/{}/agent-groups/{}'.format(
                self._check('scanner_id', scanner_id, int),
                self._check('group_id', group_id, int)
            )).json()

    def bulk_status(self, group_id, task_uuid, scanner_id=1):
        '''
        `bulk-operations: bulk-agent-group-status <https://cloud.tenable.com/api#/resources/bulk-operations/bulk-agent-group-status>`_

        Args:
            group_id (int): The id of the group
            task_uuid (str): The id of the agent
            scanner_id (int, optional): The id of the scanner

        Returns:
            dict: Task resource
        '''
        return self._api.get(
            'scanners/{}/agent-groups/{}/agents/_bulk/{}'.format(
                self._check('scanner_id', scanner_id, int),
                self._check('group_id', group_id, int),
                self._check('task_uuid', task_uuid, 'uuid')
            )).json()