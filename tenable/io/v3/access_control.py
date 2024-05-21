"""
Access-Control
==============

The following methods allow for interaction into the Tenable Vulnerability Management API endpoints.

Methods available on ``tio.v3.access_control``:

.. rst-class:: hide-signature
.. autoclass:: AccessControlAPI
    :members:
"""
from tenable.io.base import TIOEndpoint


class AccessControlAPI(TIOEndpoint):
    _path = 'api/v3/access-control'
    '''
        This will contain methods related to AccessControl -> Access control V3 API endpoints.
    '''

    def details(self, uuid):
        """
        Retrieves the details of the specified permission.

        :devportal:`access-control: details <io-v3-access-control-permissions-details>`
        Args:
            uuid (str):
                the uuid of the permission to retrieve

        Returns:
            :obj:`dict`:
                The resource record for the specified permission

        Examples:
            Get specific permission details:
                >>> tio.v3.access_control.details('4f948c22-ae2c-4d0b-bab4-0fc1088a85bd')
                ...
        """
        return self._api.get(f'{self._path}/permissions/' + uuid).json()

    def get_user_permission(self, user_uuid):
        """
        Retrieves user permission details

        :devportal:`access-control: user permission <io-v3-access-control-permissions-user-list>`

        Args:
            user_uuid (str):
                the uuid of the user to retrieve

        Returns:
            :obj:`dict`:
                The resource record for the user permissions
        Examples:
            Get specific user permission details:
                >>> tio.v3.access_control.get_user_permission('4f948c22-ae2c-4d0b-bab4-0fc1088a85bd')
        """
        return self._api.get(f'{self._path}/permissions/users/' + user_uuid).json()

    def get_user_group_permission(self, user_group_uuid):
        """
        Retrieves user group permission details

        :devportal:`access-control : user group permission <io-v3-access-control-permissions-user-group-list>`

        Args:
            user_group_uuid (str):
                the uuid of the user-group to retrieve

        Returns:
            :obj:`dict`:
                The resource record for the user-group permission

        Examples:
            Get specific user-group permission details:
                >>> tio.v3.access_control.get_user_group_permission('4f948c22-ae2c-4d0b-bab4-0fc1088a85bd')
        """
        return self._api.get(f'{self._path}/permissions/user-groups/' + user_group_uuid).json()

    def get_current_user_permission(self):
        """
        Retrieves current user permission details

        :devportal:`access-control : current user permission <io-v3-access-control-permissions-current-user-list>`


        Returns:
            :obj:`dict`:
                The resource record for the current user permission.

        Examples:
            Get specific user-group permission details:
                >>> tio.v3.access_control.get_current_user_permission('4f948c22-ae2c-4d0b-bab4-0fc1088a85bd')

        """
        return self._api.get(f'{self._path}/permissions/users/me').json()

    def delete(self, permission_uuid):
        """
        Delete the specified permission

        :devportal:`access-control: delete <io-v3-access-control-permission-delete>`

        Args:
            permission_uuid (str):
                the uuid of the permission to remove

        Returns:
            :obj:`dict`:

        Examples:
            delete permission:
                >>> tio.v3.access_control.delete('4f948c22-ae2c-4d0b-bab4-0fc1088a85bd')
        """
        return self._api.delete(f'{self._path}/permissions/' + permission_uuid).json()

    def create(self, permission):
        """
        Creates a new permission

        :devportal:`access-control: create <io-v3-access-control-permission-create>`

        Args:
             permission(dict):
                    the permission details object that needs to be created,
        Returns:
            :obj:`dict`:
                The resource record for the new permission.

        Example::
            create permission:
              >>>        payload = {
              ...            "actions": ["CanView","CanEdit"],
              ...            "objects": [
              ...                {
              ...                    "type": "Tag",
              ...                    "uuid": "10bd7477-2961-402c-92fb-d7f6a8dc9399",
              ...                    "name": "TGG,DE"
              ...               }
              ...            ],
              ...            "subjects": [
              ...                 {
              ...                   "name": "dummy_user@tenable.com",
              ...                   "type": "User",
              ...                   "uuid": "4f948c212-ae2c-4d0b-bab4-0fc1088a85bd"
              ...                }
              ...            ],
              ...            "name": "permission name"
              ...         }
              ...
              ...  tio.v3.access_control.create(payload)
        """
        return self._api.post(f'{self._path}/permissions/', json=permission).json()

    def update(self, permission_uuid, permission):
        """
        update permission

        :devportal:`access-control : update <io-v3-access-control-permission-update>`

        Args:
            permission_uuid(str):
                permission uuid to be updated

            permission(dict):
                the permission details object that needs to be updated,
                permission details object example :

        Returns:
            :obj:`None`: Update successfully requested.

        Example:
            update permission:
              >>>        payload = {
              ...            "actions": ["CanView","CanEdit"],
              ...            "objects": [
              ...                {
              ...                    "type": "Tag",
              ...                    "uuid": "10bd7477-2961-402c-92fb-d7f6a8dc9399",
              ...                    "name": "TGG,DE"
              ...               }
              ...            ],
              ...            "subjects": [
              ...                 {
              ...                   "name": "dummy_user@tenable.com",
              ...                   "type": "User",
              ...                   "uuid": "4f948c212-ae2c-4d0b-bab4-0fc1088a85bd"
              ...                }
              ...            ],
              ...            "name": "permission name"
              ...         }
              ...
              ...  permission_uuid_val = "212-ae2c-4d0b-bab4-0fc1088a85bd"
              ...
              ...  tio.v3.access_control.update(permission_uuid_val, payload)
        """
        self._api.put(f'{self._path}/permissions/' + permission_uuid, json=permission)

    def list(self) -> list:
        """
        Returns a list of permissions in your container.

        Returns:
            :obj:`list`:
                List of permissions.

        Examples:
            >>> for permission in tio.access_control.list():
            ...     pprint(permission)
        """
        return self._api.get(f"{self._path}/permissions").json()["permissions"]
