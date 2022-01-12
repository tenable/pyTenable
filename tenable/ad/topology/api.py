'''
Topology
========

Methods described in this section relate to the the topology API.
These methods can be accessed at ``TenableAD.topology``.

.. rst-class:: hide-signature
.. autoclass:: TopologyAPI
    :members:
'''
from typing import Dict
from tenable.ad.topology.schema import TopologySchema
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
            >>> tad.topology.details(profile_id='1')
        '''
        return self._schema.load(self._api.get(
            f'profiles/{profile_id}/topology'))
