'''
permissions
===========

The following methods allow for interaction into the Tenable.io 
`permissions <https://cloud.tenable.com/api#/resources/permissions>`_ 
API endpoints.

Methods available on ``tio.permissions``:

.. rst-class:: hide-signature
.. autoclass:: PermissionsAPI

    .. automethod:: change
    .. automethod:: list
'''
from .base import TIOEndpoint

class PermissionsAPI(TIOEndpoint):
    def change(self, otype, id, *acls):
        '''
        Modify the permission of a specific object.

        `permissions: change <https://cloud.tenable.com/api#/resources/permissions/change>`_

        Args:
            otype (str):
                The type of object to change.
            id (int):
                The unique identifier fo the object.
            *acls (dict):
                ACL dictionaries inform Tenable.io how to handle permissions of
                the various objects within Tenable.io.  The permissions dict is
                described on the `permissions resource`_ page.  Further the
                integer values that represent the permissions granted are
                detailed on the `authorization page`_ within the documentation.

        Returns:
            None: The object permissions were successfully changed.

        .. _permissions resource:
            https://cloud.tenable.com/api#/resources/permissions
        .. _authorization page:
            https://cloud.tenable.com/api#/authorization
        '''
        # Check to make sure all of the ACLs are dictionaries.
        for item in acls:
            self._check('acl', item, dict)

        # Make the API call.
        self._api.put('permissions/{}/{}'.format(
            self._check('otype', otype, str),
            self._check('id', id, int)
        ), json={'acls': acls})

    def list(self, otype, id):
        '''
        List the permissions of a specific object.

        `permissions: list <https://cloud.tenable.com/api#/resources/permissions/list>`_

        Args:
            otype (str):
                The type of object being queried.
            id (int):
                The unique identifier of the object.

        Returns:
            list: 
                The permission recourse record listings for the specified object.
        '''
        return self._api.get(
            'permissions/{}/{}'.format(
                self._check('otype', otype, str),
                self._check('id', id, int)
            )).json()['acls']