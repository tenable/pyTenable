'''
groups
======

The following methods allow for interaction into the Tenable.io
:devportal:`groups <groups>` API.

Methods available on ``tio.groups``:

.. rst-class:: hide-signature
.. autoclass:: GroupsAPI

    .. automethod:: add_user
    .. automethod:: create
    .. automethod:: delete
    .. automethod:: delete_user
    .. automethod:: edit
    .. automethod:: list
    .. automethod:: list_users
'''
from typing import ClassVar, Dict, List
from .base import TIOEndpoint

class GroupsAPI(TIOEndpoint):
    _path: ClassVar[str] = 'groups'

    def add_user(
            self,
            group_id: int,
            user_id: int
    ) -> None:
        '''
        Add a user to a user group.

        :devportal:`groups: add-user <groups-add-user>`

        Args:
            group_id (int):
                The unique identifier of the group to add the user to.
            user_id (int):
                The unique identifier of the user to add.

        Returns:
            :obj:`None`:
                The user was successfully added to the group.

        Examples:
            >>> tio.groups.add_user(1, 1)
        '''
        self._check('group_id', group_id, int)
        self._check('user_id', user_id, int)
        self._api.post(f'{self._path}/{group_id}/users/{user_id}', json={})

    def create(
            self,
            name: str
    ) -> Dict:
        '''
        Create a new user group.

        :devportal:`groups: create <groups-create>`

        Args:
            name (str):
                The name of the group that will be created.

        Returns:
            :obj:`dict`:
                The group resource record of the newly minted group.

        Examples:
            >>> group = tio.groups.create('Group Name')
        '''
        self._check('name', name, str)
        return self._api.post(f'{self._path}', json={'name': name}).json()

    def delete(
            self,
            id: int
    ) -> None:
        '''
        Delete a user group.

        :devportal:`groups: delete <groups-delete>`

        Args:
            id (int): The unique identifier for the group to be deleted.

        Returns:
            :obj:`None`:
                The group was successfully deleted.

        Examples:
            >>> tio.groups.delete(1)
        '''
        self._check('id', id, int)
        self._api.delete(f'{self._path}/{id}')

    def delete_user(
            self,
            group_id: int,
            user_id: int
    ) -> None:
        '''
        Delete a user from a user group.

        :devportal:`groups: delete-user <groups-delete-user>`

        Args:
            group_id (int):
                The unique identifier for the group to be modified.
            user_id (int):
                The unique identifier for the user to be removed from the group.

        Returns:
            :obj:`None`:
                The user was successfully removed from the group.

        Examples:
            >>> tio.groups.delete_user(1, 1)
        '''
        self._check('group_id', group_id, int)
        self._check('user_id', user_id, int)
        self._api.delete(f'{self._path}/{group_id}/users/{user_id}')

    def edit(
            self,
            id: int,
            name: str
    ) -> Dict:
        '''
        Edit a user group.

        :devportal:`groups: edit <groups/edit>`

        Args:
            id (int):
                The unique identifier for the group to be modified.
            name (str):
                The new name for the group.

        Returns:
            :obj:`dict`:
                The group resource record.

        Examples:
            >>> tio.groups.edit(1, 'Updated name')
        '''
        self._check('id', id, int)
        self._check('name', name, str)
        return self._api.put(f'{self._path}/{id}', json={'name': name}).json()

    def list(self) -> List:
        '''
        Lists all of the available user groups.

        :devportal:`groups: list <groups-list>`

        Returns:
            :obj:`list`:
                List of the group resource records

        Examples:
            >>> for group in tio.groups.list():
            ...     pprint(group)
        '''
        return self._api.get(self._path).json()['groups']

    def list_users(
            self,
            id: int
    ) -> List:
        '''
        List the user memberships within a specific user group.

        :devportal:`groups: list-users <groups-list-users>`

        Args:
            id (int): The unique identifier of the group requested.

        Returns:
            :obj:`list`:
                List of user resource records based on membership to the
                specified group.

        Example:
            >>> for user in tio.groups.list_users(1):
            ...     pprint(user)
        '''
        self._check('id', id, int)
        return self._api.get(f'{self._path}/{id}/users').json()['users']
