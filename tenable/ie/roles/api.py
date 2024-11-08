'''
Roles
=============

Methods described in this section relate to the roles API.
These methods can be accessed at ``TenableIE.roles``.

.. rst-class:: hide-signature
.. autoclass:: RolesAPI
    :members:
'''
from typing import List, Dict
from marshmallow import ValidationError
from tenable.base.endpoint import APIEndpoint
from .schema import RoleSchema, RolePermissionsSchema


class RolesAPI(APIEndpoint):
    _path = 'roles'
    _schema = RoleSchema()

    def list(self) -> List[Dict]:
        '''
        Retrieve all roles

        Returns:
            list[dict]:
                The list of roles objects

        Examples:
            >>> tie.roles.list()
        '''
        return self._schema.load(self._get(), many=True)

    def create(self,
               name: str,
               description: int
               ) -> List[Dict]:
        '''
        Create a new role

        Args:
            name (str):
                The name of role.
            description (str):
               The description of role.

        Returns:
            list[dict]:
                The created role object.

        Examples:
            >>> tie.roles.create(
            ...     name='Admin',
            ...     description="all privileges"
            ...     )
        '''
        payload = [
            self._schema.dump(self._schema.load({
                'name': name,
                'description': description
            }))
        ]

        return self._schema.load(self._post(json=payload), many=True)

    def default_roles(self) -> List[Dict]:
        '''
        Return the default roles for user creation

        Returns:
            list[dict]:
                The default roles object.

        Examples:
            >>> tie.roles.default_roles()
        '''
        return self._schema.load(
            self._get('user-creation-defaults'), many=True)

    def details(self, role_id: str) -> Dict:
        '''
        Retrieves the details of a specific role.

        Args:
            role_id (str):
                The role instance identifier.

        Returns:
            dict:
                the role object.

        Examples:
            >>> tie.roles.details(
            ...     role_id='1'
            ...     )
        '''
        return self._schema.load(self._get(f"{role_id}"))

    def update(self,
               role_id: str,
               **kwargs
               ) -> Dict:
        '''
        Update an existing role

        Args:
            role_id (str):
                The role instance identifier.
            name (optional, str):
                The name of role.
            description (optional, str):
               The description of role.

        Returns:
            dict:
                The updated widget object.

        Examples:
            >>> tie.roles.update(
            ...     role_id='1',
            ...     name='Basic'
            ...     )
        '''
        payload = self._schema.dump(self._schema.load(kwargs))
        return self._schema.load(self._patch(f"{role_id}", json=payload))

    def delete(self, role_id: str) -> None:
        '''
        Delete an existing role

        Args:
            role_id (str):
                The role instance identifier.

        Returns:
            None:

        Examples:
            >>> tie.roles.delete(
            ...     role_id='1',
            ...     )
        '''
        self._delete(f"{role_id}")

    def copy_role(self,
                  from_id: str,
                  name: str
                  ) -> Dict:
        '''
        Creates a new role from another role

        Args:
            from_id (str):
                The role instance identifier user wants to copy.
            name (str):
                The name of new role.

        Returns:
            dict:
                the copied role object.

        Examples:
            >>> tie.roles.copy_role(
            ...     from_id='1',
            ...     name='Copied name'
            ...     )
        '''
        payload = self._schema.dump(self._schema.load({
            'name': name
        }))
        return self._schema.load(self._post(f'from/{from_id}', json=payload))

    def replace_role_permissions(self,
                                 role_id: str,
                                 permissions: List[Dict]
                                 ) -> Dict:
        '''
        Replace permission list for a role

        Args:
            role_id (str):
                The role instance identifier.
            permissions (List[Dict]) :
                The list of permissions dictionaries.
                Below are the values expected in dictionaries
            entity_name (str):
                The name of entity.
            action (str):
                The code of action to perform.
            entity_ids (List[int]):
                The list of entity identifiers.
            dynamic_id (optional, str):
                The dynamicId to use associated with the action.

        Returns:
            dict:
                the update permissions role object.

        Examples:
            >>> tie.roles.replace_role_permissions(
            ...     role_id='1',
            ...     permissions=[{
            ...         'entity_name':'dashboard',
            ...         'action':'action',
            ...         'entity_ids':[1, 2],
            ...         'dynamic_id': None
            ...     }]
            ... )
        '''
        schema = RolePermissionsSchema()
        payload = schema.dump(schema.load(permissions, many=True), many=True)
        return self._schema.load(
            self._put(f'{role_id}/permissions', json=payload))
