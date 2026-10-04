"""
Groups
======

The following methods allow for interaction into the Tenable Vulnerability Management
:devportal:`groups <groups-list>` API.

Methods available on ``tio.groups``:

.. rst-class:: hide-signature
.. autoclass:: GroupsAPI
    :members:
"""

from tenable.utils import scrub

from .base import TIOEndpoint


class GroupsAPI(TIOEndpoint):
    def add_user(self, group_id, user_id):
        """
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
        """
        self._api.post(f'groups/{scrub(group_id)}/users/{scrub(user_id)}')

    def create(self, name, *, managed_by_saml=None):
        """
        Create a new user group.

        :devportal:`groups: create <groups-create>`

        Args:
            name (str):
                The name of the group that will be created.
            managed_by_saml (bool, optional):
                If ``True``, SAML single sign-on can add users to and remove
                users from the group.  If ``False``, group membership is
                managed independently of SAML.  If omitted, the API default
                applies.

        Returns:
            :obj:`dict`:
                The group resource record of the newly minted group.  It
                includes ``managed_by_saml`` only if the flag was set.

        Examples:
            >>> group = tio.groups.create('Group Name')

            Create a group whose membership SAML manages:

            >>> group = tio.groups.create('SAML Admins', managed_by_saml=True)
        """
        payload = {'name': self._check('name', name, str)}
        if managed_by_saml is not None:
            payload['managed_by_saml'] = self._check(
                'managed_by_saml', managed_by_saml, bool
            )
        return self._api.post('groups', json=payload).json()

    def delete(self, id):
        """
        Delete a user group.

        :devportal:`groups: delete <groups-delete>`

        Args:
            id (int): The unique identifier for the group to be deleted.

        Returns:
            :obj:`None`:
                The group was successfully deleted.

        Examples:
            >>> tio.groups.delete(1)
        """
        self._api.delete(f'groups/{scrub(id)}')

    def delete_user(self, group_id, user_id):
        """
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
        """
        self._api.delete(f'groups/{scrub(group_id)}/users/{scrub(user_id)}')

    def edit(self, id, name, *, managed_by_saml=None):
        """
        Edit a user group.

        :devportal:`groups: edit <groups-edit>`

        Args:
            id (int):
                The unique identifier for the group to be modified.
            name (str):
                The new name for the group.  The API requires a name on every
                edit, so pass the current name to change only
                ``managed_by_saml``.
            managed_by_saml (bool, optional):
                If ``True``, SAML single sign-on can add users to and remove
                users from the group.  If ``False``, group membership is
                managed independently of SAML.  If omitted, the current
                setting is kept.

        Returns:
            :obj:`dict`:
                The group resource record.

        Examples:
            >>> tio.groups.edit(1, 'Updated name')

            Stop SAML from managing the group's membership:

            >>> tio.groups.edit(1, 'SAML Admins', managed_by_saml=False)
        """
        payload = {'name': self._check('name', name, str)}
        if managed_by_saml is not None:
            payload['managed_by_saml'] = self._check(
                'managed_by_saml', managed_by_saml, bool
            )
        return self._api.put(f'groups/{scrub(id)}', json=payload).json()

    def list(self):
        """
        Lists all of the available user groups.

        :devportal:`groups: list <groups-list>`

        Returns:
            :obj:`list`:
                List of the group resource records

        Examples:
            >>> for group in tio.groups.list():
            ...     pprint(group)
        """
        return self._api.get('groups').json()['groups']

    def list_users(self, id):
        """
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
        """
        return self._api.get(f'groups/{scrub(id)}/users').json()['users']
