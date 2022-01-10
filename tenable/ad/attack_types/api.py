'''
Attack Type
=============

Methods described in this section relate to the the attack type API.
These methods can be accessed at ``TenableAD.attack_types``.

.. rst-class:: hide-signature
.. autoclass:: AttackTypesAPI
    :members:

'''
from typing import List, Dict
from tenable.ad.attack_types.schema import AttackTypesSchema
from tenable.base.endpoint import APIEndpoint


class AttackTypesAPI(APIEndpoint):
    _schema = AttackTypesSchema()

    def list(self) -> List[Dict]:
        '''
        Retrieve all attack types

        Returns:
            list:
                The list of attack types objects

        Examples:
            >>> tad.attack_types.list()
        '''
        return self._schema.load(self._get('attack-types'), many=True)
