from tenable.base import APIEndpoint

class AgentGroupsAPI(APIEndpoint):
    def add_agent(self, group_id, agent_id, scanner_id=1):
        '''
        agent-groups: add-agent
        https://cloud.tenable.com/api#/resources/agent-groups/add-agent

        Args:
            scanner_id (int): The id of the scanner
            group_id (int): The id of the group
            agent_id (int): The id of the agent

        Returns:
            None: Agent added successfully
        '''
        return self._api.put(
            'scanners/{}/agent-groups/{}/agents/{}'.format(
                self._check('scanner_id', scanner_id, int),
                self._check('group_id', group_id, int),
                self._check('agent_id', agent_id, int)
            )).json()

    def configure(self, scanner_id, group_id, name):
        '''
        agent-groups: configure
        https://cloud.tenable.com/api#/resources/agent-groups/configure

        Args:
            scanner_id (int): The id of the scanner
            group_id (int): The id of the group
            name (str): The new name for the agent group

        Returns:
            None: Agent group updated successfully
        '''
        return self._api.put(
            'scanners/{}/agent-groups/{}'.format(
                self._check('scanner_id', scanner_id, int),
                self._check('group_id', group_id, int)
            ), json={'name': self_check('name', name, str)})

    def create(self, name, scanner_id=1):
        '''
        agent-groups: create
        https://cloud.tenable.com/api#/resources/agent-groups/create

        Args:
            scanner_id (int): The id of the scanner to add the agent group to
            name (str): The name of the agent group

        Returns:
            None: Agent group created successfully
        '''
        return self._api.post(
            'scanners/{}/agent-groups'.format(
                self._check('scanner_id', scanner_id, int)
            ), json={'name': self_check('name', name, str)})

    def delete(self, group_id, scanner_id=1):
        '''
        agent-groups: delete
        https://cloud.tenable.com/api#/resources/agent-groups/delete

        Args:
            scanner_id (int): The id of the scanner
            group_id (int): The id of the agent group to delete

        Returns:
            None: Agent group deleted successfully
        '''
        return self._api.delete(
            'scanners/{}/agent-groups/{}'.format(
                self._check('scanner_id', scanner_id, int),
                self._check('group_id', group_id, int)
            ))

    def delete_agent(self, group_id, agent_id, scanner_id=1):
        '''
        agent-groups: delete-agent
        https://cloud.tenable.com/api#/resources/agent-groups/delete-agent

        Args:
            scanner_id (int): The id of the scanner
            group_id (int): The id of the agent group to remove the agent from
            agent_id (int): The id of the agent to be removed

        Returns:
            None
        '''
        return self._api.delete(
            'scanners/{}/agent-groups/{}/agents/{}'.format(
                self._check('scanner_id', scanner_id, int),
                self._check('group_id', group_id, int),
                self._check('agent_id', agent_id, int)
            ))

    def details(self, group_id, scanner_id=1):
        '''
        agent-groups: details
        https://cloud.tenable.com/api#/resources/agent-groups/details

        Args:
            
        '''
        pass