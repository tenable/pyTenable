'''
Users
=============

Methods described in this section relate to the users API.
These methods can be accessed at ``TenableIE.users``.

.. rst-class:: hide-signature
.. autoclass:: UsersAPI
    :members:
'''
from typing import List, Dict
from restfly.utils import dict_merge
from tenable.base.endpoint import APIEndpoint
from .schema import UserSchema, UserInfoSchema


class UsersAPI(APIEndpoint):
    _path = 'users'
    _schema = UserSchema()

    def list(self) -> List[Dict]:
        '''
        Retrieve all users

        Returns:
            list:
                The list of users objects

        Examples:
            >>> tie.users.list()
        '''
        return self._schema.load(self._get(), many=True)

    def create(self,
               name: str,
               email: str,
               password: str,
               **kwargs
               ) -> List[Dict]:
        '''
        Create users

        Args:
            name (str):
                The name of new user.
            email (str):
                The email address of the user.
            password (str):
                The password for the new user.
            surname (optional, str):
                The surname of new user.
            department (optional, str):
                The department of user.
            biography (optional, str):
                The biography of user.
            active (optional, bool):
                is the user active?
            picture (optional, List[int]):
                The list of picture numbers

        Return:
            list[dict]:
                The created user objects

        Example:
            >>> tie.users.create(
            ...     name='username',
            ...     email='test@domain.com',
            ...     password='user_password',
            ...     active=True
            ...     )
        '''
        payload = [
            self._schema.dump(self._schema.load(
                dict_merge({
                    'name': name,
                    'email': email,
                    'password': password
                }, kwargs)
            ))
        ]

        return self._schema.load(
            self._post(json=payload),
            many=True)

    def info(self) -> Dict:
        '''
        Gets user information

        Return:
            dict:
                The user info object

        Example:
            >>> tie.users.info()
        '''
        schema = UserInfoSchema()
        return schema.load(self._get('whoami'))

    def details(self, user_id: str) -> Dict:
        '''
        Retrieves the details for a specific user

        Args:
            user_id (str):
                The user instance identifier.

        Returns:
            dict:
                the user object.

        Examples:
            >>> tie.users.details('1')
        '''
        return self._schema.load(self._get(f'{user_id}'))

    def update(self,
               user_id: str,
               **kwargs
               ) -> Dict:
        '''
        Update an existing user

        Args:
            user_id (str):
                The user instance identifier.
            name (optional, str):
                The name of new user.
            email (optional, str):
                The email address of the user.
            password (optional, str):
                The password for the new user.
            surname (optional, str):
                The surname of new user.
            department (optional, str):
                The department of user.
            biography (optional, str):
                The biography of user.
            active (optional, bool):
                is the user active?
            picture (optional, List[int]):
                The list of picture numbers

        Returns:
            dict:
                The updated user object.

        Examples:
            >>> tie.users.update(
            ...     user_id='1',
            ...     name='EDITED'
            ...     )
        '''
        payload = self._schema.dump(self._schema.load(kwargs))
        return self._schema.load(
            self._patch(f"{user_id}", json=payload))

    def delete(self, user_id: str) -> None:
        '''
        Delete an existing user

        Args:
            user_id (str):
                The user instance identifier.

        Returns:
            None:

        Examples:
            >>> tie.users.delete(user_id='1')
        '''
        self._delete(f"{user_id}")

    def create_password(self, email: str) -> None:
        '''
        Sends an email to create new password

        Args:
            email (str):
                The email address of the user.

        Returns:
            None:

        Examples:
            >>> tie.users.create_password(email='test@domain.com')
        '''
        payload = self._schema.dump(self._schema.load({
            'email': email
        }))
        self._post('forgotten-password', json=payload)

    def retrieve_password(self,
                          token: str,
                          new_password: str
                          ) -> None:
        '''
        Retrieves a user password

        Args:
            token (str):
                user token.
            new_password (str):
                new password for user.

        Returns:
            None:

        Examples:
            >>> tie.users.retrieve_password(
            ...     token='token',
            ...     new_password='new_password'
            ...     )
        '''
        payload = self._schema.dump(self._schema.load({
            'token': token,
            'newPassword': new_password
        }))
        self._post('retrieve-password', json=payload)

    def change_password(self,
                        old_password: str,
                        new_password: str
                        ) -> None:
        '''
        Update a user password

        Args:
            old_password (str):
                old password of user.
            new_password (str):
                new password of user.

        Returns:
            None:

        Examples:
            >>> tie.users.change_password(
            ...     old_password='old_password',
            ...     new_password='new_password'
            ...     )
        '''
        payload = self._schema.dump(self._schema.load({
            'oldPassword': old_password,
            'newPassword': new_password
        }))
        self._patch("password", json=payload)

    def update_user_roles(self,
                          user_id: str,
                          roles: List[int]
                          ) -> Dict:
        '''
        Replace role list for user

        Args:
            user_id (str):
                The user instance identifier.
            roles (List[int]):
                The list of user role identifiers.

        Returns:
            dict:
                updated user roles object

        Examples:
            >>> tie.users.update_user_roles(
            ...     user_id='1',
            ...     roles=[1, 2, 3]
            ...     )
        '''
        payload = self._schema.dump(self._schema.load({
            'roles': roles
        }))
        return self._schema.load(self._put(f'{user_id}/roles', json=payload))
