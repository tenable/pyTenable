'''
groups
======

The following methods allow for interaction into the Tenable.io 
`groups <https://cloud.tenable.com/api#/resources/groups>`_ API.

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
from .base import TIOEndpoint

class GroupsAPI(TIOEndpoint):
    def add_user(self, group_id, user_id):
        '''
        Add a user to a user group.

        `groups: add-user <https://cloud.tenable.com/api#/resources/groups/add-user>`_

        Args:
            group_id (int):
                The unique identifier of the group to add the user to.
            user_id (int):
                The unique identifier of the user to add.

        Returns:
            None: The user was successfully added to the group.

        Examples:
            >>> tio.groups.add_user(1, 1)
        '''
        self._api.post('groups/{}/users/{}'.format(
            self._check('group_id', group_id, int),
            self._check('user_id', user_id, int), json={}
        ))

    def create(self, name):
        '''
        Create a new user group.

        `groups: create <https://cloud.tenable.com/api#/resources/groups/create>`_

        Args:
            name (str):
                The name of the group that will be created.

        Returns:
            dict: The group resource record of the newly minted group.

        Examples:
            >>> group = tio.groups.create('Group Name')
        '''
        return self._api.post('groups', json={
            'name': self._check('name', name, str)
        }).json()

    def delete(self, id):
        '''
        Delete a user group.

        `groups: delete <https://cloud.tenable.com/api#/resources/groups/delete>`_

        Args:
            id (int): The unique identifier for the group to be deleted.

        Returns:
            None: The group was successfully deleted.

        Examples:
            >>> tio.groups.delete(1)
        '''
        self._api.delete('groups/{}'.format(self._check('id', id, int)))

    def delete_user(self, group_id, user_id):
        '''
        Delete a user from a user group.

        `groups: delete-user <https://cloud.tenable.com/api#/resources/groups/delete-user>`_

        Args:
            group_id (int): 
                The unique identifier for the group to be modified.
            user_id (int): 
                The unique identifier for the user to be removed from the group.

        Returns:
            None: The user was successfully removed from the group.

        Examples:
            >>> tio.groups.delete_user(1, 1)
        '''
        self._api.delete('groups/{}/users/{}'.format(
            self._check('group_id', group_id, int),
            self._check('user_id', user_id, int)
        ))

    def edit(self, id, name):
        '''
        Edit a user group.

        groups: edit <https://cloud.tenable.com/api#/resources/groups/edit>`_

        Args:
            id (int):
                The unique identifier for the group to be modified.
            name (str):
                The new name for the group.

        Returns:
            dict: The group resource record.

        Examples:
            >>> tio.groups.edit(1, 'Updated name')
        '''
        return self._api.put('groups/{}'.format(self._check('id', id, int)), 
            json={'name': self._check('name', name, str)}).json()

    def list(self):
        '''
        Lists all of the available user groups.

        groups: list <https://cloud.tenable.com/api#/resources/groups/list>`_

        Returns:
            list: List of the group resource records

        Examples:
            >>> for group in tio.groups.list():
            ...     pprint(group)
        '''
        return self._api.get('groups').json()['groups']

    def list_users(self, id):
        '''
        List the user memberships within a specific user group.

        `groups: list-users <https://cloud.tenable.com/api#/resources/groups/list-users>`_

        Args:
            id (int): The unique identifier of the group requested.

        Returns:
            list: 
                List of user resource records based on membership to the
                specified group.

        Example:
            >>> for user in tio.groups.list_users(1):
            ...     pprint(user)
        '''
        return self._api.get('groups/{}/users'.format(
            self._check('id', id, int))).json()['users']

    