'''
Users
=====

The following methods allow for interaction into the Tenable.io
:devportal:`users <users>` API endpoints.

Methods available on ``tio.v3.vm.users``:

.. rst-class:: hide-signature
.. autoclass:: UsersAPI
    :members:
'''
from typing import Dict, Optional, Union
from uuid import UUID

from requests import Response
from restfly.utils import dict_clean

from tenable.io.v3.base.endpoints.explore import ExploreBaseEndpoint
from tenable.io.v3.base.iterators.explore_iterator import (CSVChunkIterator,
                                                           SearchIterator)
from tenable.io.v3.users.schema import (UserEditSchema, UsersCommonSchema,
                                        UsersCreateSchema)
from tenable.utils import dict_merge


class UsersAPI(ExploreBaseEndpoint):
    '''
    This will contain all methods related to Users
    '''

    _path = 'api/v3/users'
    _conv_json = True
    _schema = UsersCommonSchema()

    def create(self,
               username: str,
               password: str,
               permissions: int,
               name: Optional[str] = None,
               email: Optional[str] = None,
               account_type: Optional[str] = None,
               ) -> Dict:
        '''
        Create a new user.

        :devportal:`users: create <users-create>`

        Args:
            username (str):
                The username for the new user.
            password (str):
                The password for the new user.
            permissions (int):
                The permissions role for the user.  The permissions integer
                is derived based on the desired role of the user.  For details
                describing what permissions values mean what roles, please
                refer to the
                `User Roles <https://cloud.tenable.com/api#/authorization>`_
                table to see what permissions are accepted.
            name (str, optional):
                The human-readable name of the user.
            email (str, optional):
                The email address of the user.
            account_type (str, optional):
                The account type for the user. The default is `local`.

        Returns:
            :obj:`dict`:
                The resource record of the new user.

        Examples:
            Create a standard user:

            >>> user = tio.v3.vm.users.create('jsmith@company.com',
            ...     'password1', 32)

            Create an admin user and add the email and name:

            >>> user = tio.v3.vm.users.create('jdoe@company.com', 'password',
            ...     64, name='Jane Doe', email='jdoe@company.com')
        '''
        payload = dict_clean(
            dict(
                username=username,
                password=password,
                permissions=permissions,
                name=name,
                email=email,
                type=account_type,
            )
        )
        schema = UsersCreateSchema()
        payload = schema.dump(schema.load(payload))
        return self._post(json=payload)

    def delete(self, user_id: UUID) -> None:
        '''
        Removes a user from Tenable.io.

        :devportal:`users: delete <users-delete>`

        Args:
            user_id (uuid.UUID):
            The unique identifier of the user.

        Returns:
            :obj:`None`

        Examples:
            >>> tio.v3.vm.users.delete('60f73e4f-8983-41c2-a13c-39074cbb6229')
        '''
        self._delete(f'{user_id}')

    def details(self, user_id: UUID) -> Dict:
        '''
        Retrieve the details of a user.

        :devportal:`users: details <users-details>`

        Args:
            user_id (uuid.UUID):
                The unique identifier for the user.

        Returns:
            :obj:`dict`:
                The resource record for the user.

        Examples:
            >>> user = tio.v3.vm.users.details(
            ...  '60f73e4f-8983-41c2-a13c-39074cbb6229')
        '''
        return super()._details(user_id)

    def edit(self,
             user_id: UUID,
             permissions: Optional[int] = None,
             name: Optional[str] = None,
             email: Optional[str] = None,
             enabled: Optional[bool] = None,
             ) -> Dict:
        '''
        Modify an existing user.

        :devportal:`users: edit <users-edit>`

        Args:
            user_id (uuid.UUID):
                The unique identifier for the user.
            permissions (int, optional):
                The permissions role for the user.  The permissions integer
                is derived based on the desired role of the user.  For details
                describing what permissions values mean what roles, please
                refer to the
                `User Roles <https://cloud.tenable.com/api#/authorization>`_
                table to see what permissions are accepted.
            name (str, optional):
                The human-readable name of the user.
            email (str, optional):
                The email address of the user.
            enabled (bool, optional):
                Is the user account enabled?

        Returns:
            :obj:`dict`:
                The modified user resource record.

        Examples:
            >>> tio.v3.vm.users.edit(
            ...  '60f73e4f-8983-41c2-a13c-39074cbb6229', name='New Full Name')
        '''
        payload = dict_clean(
            dict(
                permissions=permissions,
                name=name,
                email=email,
                enabled=enabled
            )
        )
        schema = UserEditSchema()
        payload = schema.dump(schema.load(payload))

        # Merge the data that we build with the payload with the user details.
        user = self.details(user_id)
        payload = dict_merge(
            {
                'permissions': user['permissions'],
                'enabled': user['enabled'],
                'email': user['email'],
                'name': user.get('name', None),
            },
            payload,
        )
        return self._put(f'{user_id}', json=payload)

    def enabled(self, user_id: UUID, enabled: bool) -> Dict:
        '''
        Enable the user account.

        :devportal:`users: enabled <users-enabled>`

        Args:
            user_id (uuid.UUID):
                The unique identifier for the user.
            enabled (bool):
            Is the user enabled?

        Returns:
            :obj:`dict`:
                The modified user resource record.

        Examples:
            Enable a user:

            >>> tio.v3.vm.users.enabled(
            ...  '60f73e4f-8983-41c2-a13c-39074cbb6229', True)

            Disable a user:

            >>> tio.v3.vm.users.enabled(
            ...  '60f73e4f-8983-41c2-a13c-39074cbb6229', False)
        '''
        return self._put(f'{user_id}/enabled', json={'enabled': enabled})

    def two_factor(self,
                   user_id: UUID,
                   email: bool,
                   sms: bool,
                   phone: Optional[str] = None
                   ) -> None:
        '''
        Configure two-factor authorization for a specific user.

        :devportal:`users: two-factor <users-two-factor>`

        Args:
            user_id (uuid.UUID):
                The unique identifier for the user.
            email (bool):
                Whether two-factor should be additionally sent as an email.
            sms (bool):
                Whether two-factor should be enabled. This will send SMS codes.
            phone (str, optional):
                The phone number to use for two-factor authentication.
                Required when sms is set to `True`.

        Returns:
            :obj:`None`

        Examples:
            Enable email authorization for a user:

            >>> tio.v3.vm.users.two_factor(
            ...  '60f73e4f-8983-41c2-a13c-39074cbb6229', True, False)

            Enable SMS authorization for a user:

            >>> tio.v3.vm.users.two_factor(
            ...  '60f73e4f-8983-41c2-a13c-39074cbb6229', False, True,
            ...  '9998887766')
        '''
        payload = {'email_enabled': email, 'sms_enabled': sms}
        if phone:
            payload['sms_phone'] = phone
        payload = self._schema.dump(self._schema.load(payload))
        self._put(f'{user_id}/two-factor', json=payload)

    def enable_two_factor(self,
                          user_id: UUID,
                          phone: str,
                          password: str
                          ) -> None:
        '''
        Enable phone-based two-factor authorization for a specific user.

        :devportal:`users: two-factor-enable <users-two-factor-enable>`

        Args:
            user_id (uuid.UUID):
                The user id
            phone (str):
                The phone number to use for two-factor auth.
            password (str):
                The user password.

        Returns:
            :obj:`None`

        Examples:
            >>> tio.v3.vm.users.enable_two_factor(
            ...  '60f73e4f-8983-41c2-a13c-39074cbb6229', '9998887766',
            ...  'password')
        '''
        payload = {'sms_phone': phone, 'password': password}
        payload = self._schema.dump(self._schema.load(payload))
        self._post(
            f'{user_id}/two-factor/send-verification',
            json=payload
        )

    def verify_two_factor(self, user_id: UUID, code: str) -> None:
        '''
        Send the verification code for two-factor authorization.

        :devportal:`users: two-factor-enable-verify
        <users-two-factor-enable-verify>`

        Args:
            user_id (uuid.UUID):
                The user id
            code (str):
                The verification code that was sent to the device.

        Returns:
            :obj:`None`

        Examples:
            >>> tio.v3.vm.users.verify_two_factor(
            ...  '60f73e4f-8983-41c2-a13c-39074cbb6229', 'abc123')
        '''
        self._post(
            f'{user_id}/two-factor/verify-code',
            json={'verification_code': code}
        )

    def search(self,
               **kw
               ) -> Union[SearchIterator, CSVChunkIterator, Response]:
        '''
        Search a list of users.
         Args:
            fields (list, optional):
                The list of field names to return from the Tenable API.
                Example:
                    >>> ['field1', 'field2']
            filter (tuple, dict, optional):
                A nestable filter object detailing how to filter the results
                down to the desired subset.
                Examples:
                    >>> ('or', ('and', ('test', 'oper', '1'),
                    ...                 ('test', 'oper', '2')
                    ...             ),
                    ...     'and', ('test', 'oper', 3)
                    ... )
                    >>> {
                    ...  'or': [{
                    ...      'and': [{
                    ...              'value': '1',
                    ...              'operator': 'oper',
                    ...              'property': '1'
                    ...          },
                    ...          {
                    ...              'value': '2',
                    ...              'operator': 'oper',
                    ...              'property': '2'
                    ...          }
                    ...      ]
                    ...  }],
                    ...  'and': [{
                    ...      'value': '3',
                    ...      'operator': 'oper',
                    ...      'property': 3
                    ...  }]
                    ... }
                As the filters may change and sortable fields may change over
                time, it's highly recommended that you look at the output of
                the :py:meth: `tio.v3.definitions.users()` endpoint to
                get more details.
            sort (list[tuple], optional):
                sort is a list of tuples in the form of
                ('FIELD', 'ORDER').
                It describes how to sort the data
                that is to be returned.
                Examples:
                    >>> [('field_name_1', 'asc'),
                    ...      ('field_name_2', 'desc')]
            limit (int, optional):
                Number of objects to be returned in each request.
                Default and max_limit is 200.
            next (str, optional):
                The pagination token to use when requesting the next page of
                results. This token is presented in the previous response.
            return_resp (bool, optional):
                If set to true, will override the default behavior to return
                a requests.Response Object to the user.
            return_csv (bool, optional):
                If set to true, it will return the CSV response or
                iterable (based on return_resp flag). Iterator returns all
                rows in text/csv format for each call with row headers.
        Returns:
            Iterable:
                The iterable that handles the pagination for the job.
            requests.Response:
                If ``return_resp`` is set to ``True``, then a response
                object is returned instead of an iterable.
        Examples:
            >>> tio.v3.users.search(
            ...     filter=('name','eq','SCCM'),
            ...     fields=['name', 'field_one', 'field_two'],
            ...     limit=2,
            ...     sort=[('last_observed', 'asc')]
            ... )
        '''
        iclass = SearchIterator
        if kw.get('return_csv', False):
            iclass = CSVChunkIterator
        return super()._search(resource='users',
                               iterator_cls=iclass,
                               api_path=f'{self._path}/search',
                               **kw
                               )

    def change_password(self,
                        user_id: UUID,
                        old_password: str,
                        new_password: str
                        ) -> None:
        '''
        Change the password for a specific user.

        :devportal:`users: password <users-password>`

        Args:
            user_id (uuid.UUID):
                The unique identifier for the user.
            old_password (str):
                The current password.
            new_password (str):
                The new password.

        Returns:
            :obj:`None`:
                The password has been successfully changed.

        Examples:
            >>> tio.v3.vm.users.change_password(
            ...  '60f73e4f-8983-41c2-a13c-39074cbb6229', 'old_pass', 'newpass')
        '''
        payload = {'password': new_password, 'current_password': old_password}
        payload = self._schema.dump(self._schema.load(payload))
        self._put(
            f'{user_id}/chpasswd',
            json=payload
        )

    def gen_api_keys(self, user_id: UUID) -> Dict:
        '''
        Generate the API keys for a specific user.

        :devportal:`users: keys <user-keys>`

        Args:
            user_id (uuid.UUID): The unique identifier for the user.

        Returns:
            :obj:`dict`:
                A dictionary containing the new API Key-pair.

        Examples:
            >>> keys = tio.v3.vm.users.gen_api_keys(
            ...  '60f73e4f-8983-41c2-a13c-39074cbb6229')
        '''
        return self._put(f'{user_id}/keys')

    def list_auths(self, user_id: UUID) -> Dict:
        '''
        list user authorizations for accessing a Tenable.io instance.

        :devportal:`users: list-auths <users-list-auths>`

        Args:
            user_id (uuid.UUID): The unique identifier for the user.

        Returns:
            :obj:`dict`:
                Returns authorizations for the user.

        Examples:
            >>> auth = tio.v3.vm.users.list_auths(
            ...  '60f73e4f-8983-41c2-a13c-39074cbb6229')
        '''
        return self._get(f'{user_id}/authorizations')

    def edit_auths(self,
                   user_id: UUID,
                   api_permitted: Optional[bool] = None,
                   password_permitted: Optional[bool] = None,
                   saml_permitted: Optional[bool] = None,
                   ) -> None:
        '''
        update user authorizations for accessing a Tenable.io instance.

        :devportal:`users: edit-auths <users-update-auths>`

        Args:
            user_id (uuid.UUID):
                The unique identifier for the user.
            api_permitted (bool):
                Indicates whether API access is authorized for the user.
            password_permitted (bool):
                Indicates whether user name and password login is authorized
                for the user.
            saml_permitted (bool):
                Indicates whether SSO with SAML is authorized for the user.

        Returns:
            :obj:`None`:
                Returned if Tenable.io successfully updates the user's
                authorizations.

        Examples:
            >>> tio.v3.vm.users.edit_auths(
            ...  '60f73e4f-8983-41c2-a13c-39074cbb6229', True, True, False)
        '''
        # get current settings
        current = self.list_auths(user_id)
        api_permitted = (
            api_permitted if api_permitted is not None else
            current['api_permitted']
        )
        password_permitted = (
            password_permitted
            if password_permitted is not None
            else current['password_permitted']
        )
        saml_permitted = (
            saml_permitted if saml_permitted is not None else
            current['saml_permitted']
        )
        # update payload with new settings
        payload = {
            'api_permitted': api_permitted,
            'password_permitted': password_permitted,
            'saml_permitted': saml_permitted,
        }
        return self._put(f'{user_id}/authorizations', json=payload)
