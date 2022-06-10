'''
Agents
======

Methods described in this section relate to the the agents API.
These methods can be accessed at ``Nessus.agents``.

.. rst-class:: hide-signature
.. autoclass:: AgentsAPI
    :members:
'''
from typing import List, Dict, Optional, Union, Tuple
from typing_extensions import Literal
from tenable.base.endpoint import APIEndpoint
from .schema.pagination import ListSchema
from .iterators.pagination import PaginationIterator

class AgentsAPI(APIEndpoint):
    _path = 'agents'

    def delete(self, agent_id: int) -> None:
        '''
        Deletes an agent

        Args:
            agent_id (int): Id of the agent to delete

        Example:

            >>> nessus.agents.delete(agent_id)
        '''
        self._delete(f'{agent_id}')

    def delete_many(self, agent_ids: List[int]) -> None:
        '''
        Deletes multiple agents.

        Args:
            agent_ids (list[int]): List of agent ids to delete

        Example:

            >>> nessus.agents.delete_many([agent1, agent2, agent3])
        '''
        self._delete(json={'ids': agent_ids})

    def unlink(self, agent_id: int) -> None:
        '''
        Unlinks an agent.

        Args:
            agent_id (int): Id of the agent to unlink

        Example:

            >>> nessus.agents.unlink(agent_id)
        '''
        self._delete(f'{agent_id}/unlink')

    def unlink_many(self, agent_ids: List[int]) -> None:
        '''
        Unlinks multiple agents.

        Args:
            agent_ids (list[int]): List of agent ids to unlink

        Example:

            >>> nessus.agents.unlink_many([agent1, agent2, agent3])
        '''
        self._delete('unlink', json={'ids': agent_ids})

    def details(self, agent_id: int) -> Dict:
        '''
        Returns the details for an agent.

        Args:
            agent_id (int): Id of the agent to retreive

        Example:

            >>> agent = nessus.agents.details(agent_id)
        '''
        return self._get(f'{agent_id}')['agents'][0]

    def list(self,
             limit: int = 1000,
             offset: int = 0,
             sort_by: Optional[str] = None,
             sort_order: Optional[Literal['asc', 'desc']] = None,
             search_type: Optional[Literal['and', 'or']] = None,
             filters: Optional[Union[Dict, Tuple]] = None,
             return_json: bool = False
             ) -> Union[PaginationIterator, List[Dict]]:
        '''
        Returns a list of agents.

        Args:
            filters (list[tuple], optional):
                List of filters.
            sort_by (str, optional):
                Field to sort by
            sort_order (str, optional):
                Is the sort ascending (``asc``) or descending (``desc``)?
            limit (int, optional):
                Number of records per page
            offset (int, optional):
                How many records to skip before starting to return data
            return_json (bool, optional):
                Should a JSON object be returned instead of an iterator?

        Example:

            >>> for agent in nessus.agents.list():
            ...     print(agent)

            Example with filtering:

            >>> for agent in nessus.agents.list(
            ...     filters=[('name', 'match', 'lin')]
            ... ):
            ...     print(agent)

            Example getting the JSON response instead:

            >>> agents = nessus.agents.list(return_json=True)
        '''
        schema = ListSchema()
        query = schema.dump(schema.load({
            'limit': limit,
            'offset': offset,
            'sort_by': sort_by,
            'sort_order': sort_order,
            'search_type': search_type,
            'filters': filters
        }))
        if return_json:
            return self._get(params=query)['agents']
        return PaginationIterator(self._api,
                                  limit=limit,
                                  offset=offset,
                                  query=query,
                                  envelope='agents',
                                  path=self._path
                                  )
