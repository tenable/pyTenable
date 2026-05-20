"""
Permissions
===========

The following methods allow for interaction into the Tenable Vulnerability Management
:devportal`permissions <permissions-1>` API endpoints.

Methods available on ``tio.permissions``:

.. rst-class:: hide-signature
.. autoclass:: PermissionsAPI
    :members:
"""

from tenable.utils import scrub

from .base import TIOEndpoint


class PermissionsAPI(TIOEndpoint):
    def change(self, otype, id, *acls):
        """
        Modify the permission of a specific object.

        :devportal:`permissions: change <permissions-change>`

        Args:
            otype (str):
                The type of object to change.
            id (int):
                The unique identifier of the object.
            *acls (dict):
                ACL dictionaries inform Tenable Vulnerability Management how to handle permissions of
                the various objects within Tenable Vulnerability Management.  Please refer to the
                `permissions documentation`_ for more details.

        Returns:
            :obj:`None`:
                The object permissions were successfully changed.

        .. _permissions documentation:
            https://developer.tenable.com/docs/permissions
        """
        # Check to make sure all of the ACLs are dictionaries.
        for item in acls:
            self._check('acl', item, dict)

        # Make the API call.
        self._api.put(f'permissions/{scrub(otype)}/{scrub(id)}', json={'acls': acls})

    def list(self, otype, id):
        """
        List the permissions of a specific object.

        :devportal:`permissions: list <permissions-list>`

        Args:
            otype (str):
                The type of object being queried.
            id (int):
                The unique identifier of the object.

        Returns:
            :obj:`list`:
                The permission recourse record listings for the specified object.
        """
        return self._api.get(f'permissions/{scrub(otype)}/{scrub(id)}').json()['acls']
