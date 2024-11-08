'''
Attacks
=============

Methods described in this section relate to the attacks API.
These methods can be accessed at ``TenableIE.attacks``.

.. rst-class:: hide-signature
.. autoclass:: AttacksAPI
    :members:
'''
from typing import List, Dict
from tenable.ie.attacks.schema import AttackSchema
from tenable.base.endpoint import APIEndpoint


class AttacksAPI(APIEndpoint):
    _schema = AttackSchema()

    def list(self,
             profile_id: str,
             **kwargs
             ) -> List[Dict]:
        '''
        Retrieve all attacks

        Args:
            profile_id (str):
                The attack profile identifier.
            resource_type (str):
                The type of resource. possible values are ``infrastructure``,
                ``directory``, ``hostname``, ``ip``.
            resource_value (str):
                The value of resource.
            attack_type_ids (optional, list[str]):
                The list of attack type ids.
            date_end (optional, str):
                The date before which the attack occurence should be
                considered.
            date_start (optional, str):
                The date after which the attack occurence should be
                considered.
            include_closed (optional, str):
                Whether closed attacks should be included?
                Accepted values are ``true`` or ``false``
            limit (optional, str):
                The number of records user wants to return.
            order (optional, str):
                The order of response. Accepted values are
                ``asc`` or ``desc``.
            search (optional, str):
                Search a value in response.

        Returns:
            list:
                The list of attacks objects

        Examples:
            >>> tie.attacks.list(
            ...     profile_id='1',
            ...     resource_type='infrastructure',
            ...     resource_value='1',
            ...     attack_type_ids=[1, 2],
            ...     include_closed='false',
            ...     limit='10',
            ...     order='asc',
            ...     search='value',
            ...     date_end='2022-12-31T18:30:00.000Z',
            ...     date_start='2021-12-31T18:30:00.000Z'
            ...     )
        '''
        params = self._schema.dump(self._schema.load(kwargs))
        return self._schema.load(
            self._api.get(f'profiles/{profile_id}/attacks', params=params),
            many=True, partial=True)
