'''
Profiles
=============

Methods described in this section relate to the profiles API.
These methods can be accessed at ``TenableIE.profiles``.

.. rst-class:: hide-signature
.. autoclass:: ProfilesAPI
    :members:
'''
from typing import List, Dict
from tenable.base.endpoint import APIEndpoint
from .schema import ProfileSchema


class ProfilesAPI(APIEndpoint):
    _path = 'profiles'
    _schema = ProfileSchema()

    def list(self) -> List[Dict]:
        '''
        Retrieve all profiles

        Returns:
            list[dict]:
                The list of profile objects

        Examples:
            >>> tie.profiles.list()
        '''
        return self._schema.load(self._get(), many=True)

    def create(self,
               name: str,
               directories: List[int]
               ) -> List[Dict]:
        '''
        Create a profile

        Args:
            name (str):
                The name of new profile.
            directories (List[int]):
                The list of directory identifiers.

        Return:
            list[dict]:
                The created profile objects

        Example:
            >>> tie.profiles.create(
            ...     name='ExampleProfile',
            ...     directories=[1, 2]
            ...     )
        '''
        payload = [
            self._schema.dump(self._schema.load({
                'name': name,
                'directories': directories
            }))
        ]

        return self._schema.load(self._post(json=payload), many=True)

    def details(self,
                profile_id: str
                ) -> Dict:
        '''
        Retrieves the details for a specific profile

        Args:
            profile_id (str):
                The profile instance identifier.

        Returns:
            dict:
                The profile object.

        Examples:
            >>> tie.profiles.details('1')
        '''
        return self._schema.load(self._get(f'{profile_id}'))

    def update(self,
               profile_id: str,
               **kwargs
               ) -> Dict:
        '''
        Update an existing profile

        Args:
            profile_id (str):
                The profile instance identifier.
            name (optional, str):
                The name of profile.
            deleted (optional, bool):
                is the profile deleted?
            directories (optional, List[int]):
                The list of directory ids.

        Returns:
            dict:
                The updated profile object.

        Examples:
            >>> tie.profiles.update(
            ...     profile_id='1',
            ...     name='EDITED'
            ...     )
        '''
        payload = self._schema.dump(self._schema.load(kwargs))
        return self._schema.load(self._patch(f"{profile_id}", json=payload))

    def delete(self, profile_id: str) -> None:
        '''
        Delete an existing profile

        Args:
            profile_id (str):
                The profile instance identifier.

        Returns:
            None:

        Examples:
            >>> tie.profiles.delete(profile_id='1')
        '''
        self._delete(f"{profile_id}")

    def copy_profile(self,
                     from_id: str,
                     name: str,
                     directories: List[int]
                     ) -> Dict:
        '''
        Creates a new profile from another profile

        Args:
            from_id (str):
                The profile instance identifier user wants to copy.
            name (str):
                The name of new profile.
            directories (List[int]):
                The list of directory ids.

        Returns:
            dict:
                The copied role object.

        Examples:
            >>> tie.profiles.copy_profile(
            ...     from_id='1',
            ...     name='Copied name',
            ...     directories=[1, 2]
            ...     )
        '''
        payload = self._schema.dump(self._schema.load({
            'name': name,
            'directories': directories
        }))
        return self._schema.load(self._post(f'from/{from_id}', json=payload))

    def commit(self,
               profile_id: str
               ) -> None:
        '''
        Commits change of the related profile

        Args:
            profile_id (str):
                The profile instance identifier.

        Return:
            None

        Example:
            >>> tie.profiles.commit('1')
        '''
        self._post(f'{profile_id}/commit')

    def unstage(self,
                profile_id: str
                ) -> None:
        '''
        Unstages changes of the related profile

        Args:
            profile_id (str):
                The profile instance identifier.

        Return:
            None

        Example:
            >>> tie.profiles.unstage('1')
        '''
        self._post(f'{profile_id}/unstage')
