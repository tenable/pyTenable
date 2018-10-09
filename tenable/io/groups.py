from tenable.tenable_io.base import TIOEndpoint

class GroupsAPI(TIOEndpoint):
    def add_user(self, group_id, user_id):
        '''
        `groups: add-user <https://cloud.tenable.com/api#/resources/groups/add-user>`_

        Args:
            group_id (int):
                The unique identifier of the group to add the user to.
            user_id (int):
                The unique identifier of the user to add.

        Returns:
            None: The user was successfully added to the group.
        '''
        self._api.post('groups/{}/users/{}'.format(
            self._check('group_id', group_id, int),
            self._check('user_id', user_id, int)
        ))

    def create(self, name):
        '''
        `groups: create <https://cloud.tenable.com/api#/resources/groups/create>`_

        Args:
            name (str):
                The name of the group that will be created.

        Returns:
            dict: The group resource record of the newly minted group.
        '''
        return self._api.post('groups', json={
            'name': self._check('name', name, str)
        }).json()

    def delete(self, id):
        '''
        `groups: delete <https://cloud.tenable.com/api#/resources/groups/delete>`_

        Args:
            id (int): The unique identifier for the group to be deleted.

        Returns:
            None: The group was successfully deleted.
        '''
        self._api.delete('groups/{}'.format(self._check('id', id, int)))

    def delete_user(self, group_id, user_id):
        '''
        `groups: delete-user <https://cloud.tenable.com/api#/resources/groups/delete-user>`_

        Args:
            group_id (int): 
                The unique identifier for the group to be modified.
            user_id (int): 
                The unique identifier for the user to be removed from the group.

        Returns:
            None: The user was successfully removed from the group.
        '''
        self._api.delete('groups/{}/users/{}'.format(
            self._check('group_id', group_id, int),
            self._check('user_id', user_id, int)
        ))

    def edit(self, id, name):
        '''
        groups: edit <https://cloud.tenable.com/api#/resources/groups/edit>`_

        Args:
            id (int):
                The unique identifier for the group to be modified.
            name (str):
                The new name for the group.

        Returns:
            dict: The group resource record.
        '''
        return self._api.put('groups/{}'.format(self._check('id', id, int), 
            json={'name': self._check('name', name, str)})).json()

    def list(self):
        '''
        groups: list <https://cloud.tenable.com/api#/resources/groups/list>`_

        Returns:
            list: List of the group resource records
        '''
        return self._api.get('groups').json()['groups']

    def list_users(self, id):
        '''
        `groups: list-users <https://cloud.tenable.com/api#/resources/groups/list-users>`_

        Args:
            id (int): The unique identifier of the group requested.

        Returns:
            list: 
                List of user resource records based on membership to the
                specified group.
        '''
        return self._api.get('groups/{}/users'.format(
            self._check('id', id, int))).json()['users']

    