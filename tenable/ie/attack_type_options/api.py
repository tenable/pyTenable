'''
Attack Type Options
===================

Methods described in this section relate to the attack type options API.
These methods can be accessed at ``TenableIE.attack_type_options``.

.. rst-class:: hide-signature
.. autoclass:: AttackTypeOptionsAPI
    :members:
'''
from typing import List, Dict
from tenable.ie.attack_type_options.schema import AttackTypeOptionsSchema
from tenable.base.endpoint import APIEndpoint


class AttackTypeOptionsAPI(APIEndpoint):
    _schema = AttackTypeOptionsSchema()

    def list(self,
             profile_id: str,
             attack_type_id: str,
             **kwargs
             ) -> List[Dict]:
        '''
        Get all attack type options related to a profile and attack type.

        Args:
            profile_id (str):
                The attack profile identifier.
            attack_type_id (str):
                The attack type identifier.
            staged (optional, bool):
                Get only objects that are staged.
                Accepted values are ``True``, ``False``.

        Returns:
            list:
                The list of attack type options objects

        Examples:
            >>> tie.attack_type_options.list(
            ...     profile_id='1',
            ...     attack_type_id='1',
            ...     staged=False
            ...     )
        '''
        partial = ('codename', 'value', 'value_type', )
        params = self._schema.dump(self._schema.load(kwargs, partial=partial))

        return self._schema.load(
            self._api.get(f'profiles/{profile_id}/'
                          f'attack-types/{attack_type_id}/'
                          f'attack-type-options', params=params),
            many=True)

    def create(self,
               profile_id: str,
               attack_type_id: str,
               **kwargs
               ) -> List:
        '''
        Create attack type options related to a profile and attack type.

        Args:
            profile_id (str):
                The attack profile identifier.
            attack_type_id (str):
                The attack type identifier.
            codename (str):
                The codename of attack type option.
            value (str):
                The new value of the option.
            value_type (str):
                The type of option. possible values are ``string``, ``regex``,
                ``float``, ``integer``, ``boolean``, ``date``, ``object``,
                ``array/string``, ``array/regex``, ``array/integer``,
                ``array/boolean``, ``array/select``, ``array/object``
            directory_id (optional, int):
                The directory identifier.

        Return:
            list:
                The newly created attack type options.

        Example:
            >>> tie.attack_type_options.create(
            ...     profile_id='1',
            ...     attack_type_id='1',
            ...     codename='codename',
            ...     value='Some value',
            ...     value_type='string',
            ...     directory_id=None
            ...     )
        '''
        payload = [self._schema.dump(self._schema.load(kwargs))]

        return self._schema.load(
            self._api.post(f'profiles/{profile_id}/'
                           f'attack-types/{attack_type_id}/'
                           f'attack-type-options', json=payload),
            many=True)
