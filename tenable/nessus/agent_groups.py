'''
Agent Groups
============

Methods described in this section relate to the the agent groups API.
These methods can be accessed at ``Nessus.agent_groups``.

.. rst-class:: hide-signature
.. autoclass:: AgentGroupsAPI
    :members:
'''
from tenable.base.endpoint import APIEndpoint
from typing import List, Dict


class AgentGroupsAPI(APIEndpoint):
    _path = 'agent-groups'

    def add_agent(self, group_id: int, agent_id: int) -> None:
        '''
        Adds a singular agent to an agent group.

        Args:
            group_id (int): The agent group id to modify
            agent_id (int): The agent id

        Example:

            >>> nessus.agent_groups.add_agent(group_id, agent_id)
        '''
        self._put(f'{group_id}/agents/{agent_id}')

    def add_agents(self, group_id: int, agents: List[int]) -> None:
        '''
        Adds multiple agents to an agent group.

        Args:
            group_id (int): The agent group id to modify
            agents (list[int]): A list opf agent ids to add to the group.

        Example:

            >>> nessus.agent_groups.add_agents(group_id, [agent1, agent2])
        '''
        self._put(f'{group_id}/agents', json={'ids': agents})

    def configure(self, group_id: int, name: str) -> None:
        '''
        Changes the name of the given agent group.

        Args:
            group_id (int): The agent group id to modify
            name (str): The name of the agent group

        Example:

            >>> nessus.agent_groups.configure(group_id, 'Example name')
        '''
        self._put(f'{group_id}', json={'name': name})

    def create(self, name: str) -> Dict:
        '''
        Creates an agent group.

        Args:
            name (str): The name of the agent group

        Example:

            >>> group = nessus.agent_groups.create('Example agent group')
        '''
        return self._post(json={'name': name})

    def delete_group(self, group_id: int) -> None:
        '''
        Deletes an agent group.

        Args:
            group_id (int): The agent group id to be deleted.

        Example:

            >>> nessus.agent_groups.delete_group(group_id)
        '''
        self._delete(f'{group_id}')

    def delete_groups(self, group_ids: List[int]) -> None:
        '''
        Deleted multiple agent groups.

        Args:
            group_ids (list[int]): A list of agent group ids to delete

        Example:

            >>> nessus.agent_groups.delete_groups([group1, group2, group3])
        '''
        self._delete(json={'ids': group_ids})

    def delete_agent(self, group_id: int, agent_id: int) -> None:
        '''
        Deletes an agent from the agent group.

        Args:
            group_id (int): The agent group id to modify
            agent_id (int): The agent id to delete from the group

        Example:

            >>> nessus.agent_groups.delete_agent(group_id, agent_id)
        '''
        self._delete(f'{group_id}/agents/{agent_id}')

    def delete_agents(self, group_id: int, agents: List[int]) -> None:
        '''
        Deletes multiple agents from the agent group.

        Args:
            group_id (int): The agent group to modify
            agents (list[int]): A list of agent ids to remove fromt he group

        Example:

            >>> nessus.agent_groups.delete_agents(group_id, [agent1, agent2])
        '''
        self._delete(f'{group_id}/agents', json={'ids': agents})

    def details(self, group_id: int) -> Dict:
        '''
        Returns details for the given agent group

        Args:
            group_id (int): The agent group id to retrieve

        Example:

            >>> group = nessus.agent_groups.details(group_id)
        '''
        return self._get(f'{group_id}')

    def list(self) -> List[Dict]:
        '''
        Returns a listing of the agent groups

        Example:

            >>> groups = nessus.agent_groups.list()
        '''
        return self._get()['groups']
