'''
Topology
========

Methods described in this section relate to the topology API.
These methods can be accessed at ``TenableIE.topology``.

.. rst-class:: hide-signature
.. autoclass:: TopologyAPI
    :members:
'''
from typing import Dict
from tenable.ie.topology.schema import TopologySchema
from tenable.base.endpoint import APIEndpoint


class TopologyAPI(APIEndpoint):
    _schema = TopologySchema()

    def details(self, profile_id: str) -> Dict:
        '''
        Gets the representation of AD topology.

        Args:
            profile_id (str): The profile instance identifier.

        Returns:
            dict:
                Representation of AD topology.

        Examples:
            >>> tie.topology.details(profile_id='1')
        '''
        return self._schema.load(self._api.get(
            f'profiles/{profile_id}/topology'))
