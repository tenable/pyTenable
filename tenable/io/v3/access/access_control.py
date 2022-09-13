"""
Access-Control
===============

The following methods allow for interaction into the Tenable.io
:devportal:`access-control <access-control>` API endpoints.

Methods available on ``tio.v3.access_control``:

.. rst-class:: hide-signature
.. autoclass:: AccessControl
    :members:
"""
from tenable.io.base import TIOEndpoint


class AccessControl(TIOEndpoint):
    _path = 'api/v3/access-control'
    '''
        This will contain methods related to AccessControl -> Access control V3 API endpoints.
    '''

    def details(self, uuid):
        """
        Retrieves permission details

        Args:
            uuid (str):
                the uuid of the permission

        Returns:
            :obj:`dict`:
                The resource record for the permission
        """
        return self._api.get(f'{self._path}/permissions/' + uuid).json()

    def get_user_permission(self, user_uuid):
        """
        Retrieves user permission details

        Args:
            user_uuid (str):
                the uuid of the user

        Returns:
            :obj:`dict`:
                The resource record for the user permission
        """
        return self._api.get(f'{self._path}/permissions/users/' + user_uuid).json()

    def get_user_group_permission(self, user_group_uuid):
        """
        Retrieves user permission details

        Args:
            user_group_uuid (str):
                the uuid of the user-group

        Returns:
            :obj:`dict`:
                The resource record for the user permission
        """
        return self._api.get(f'{self._path}/permissions/user-groups/' + user_group_uuid).json()

    def get_current_user_permission(self):
        """
        Retrieves current user permission details

        Args:

        Returns:
            :obj:`dict`:

        """
        return self._api.get(f'{self._path}/permissions/users/me').json()

    def delete(self, permission_uuid):
        """
               Retrieves current user permission details

               Args:
                   permission_uuid (str):
                        the uuid of the permission

               Returns:
                   :obj:`dict`:

               """
        return self._api.delete(f'{self._path}/permissions/' + permission_uuid).json()

    def create(self, permission):
        """

        """
        return self._api.post(f'{self._path}/permissions/', json=permission).json()

    def update(self, permission_uuid, permission):
        """

        """
        response = self._api.put(f'{self._path}/permissions/' + permission_uuid, json=permission)
        if response.status_code == 200:
            return {
                "status": "success",
                "permission_uuid": permission_uuid
            }

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
