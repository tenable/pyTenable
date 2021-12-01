'''
users
=====

The following methods allow for interaction into the Tenable.io
:devportal:`users <users>` API endpoints.

Methods available on ``tio.v3.vm.users``:

.. rst-class:: hide-signature
.. autoclass:: UsersAPI
    :members:
'''
from typing import Dict

from restfly.utils import dict_clean

from tenable.io.v3.base.endpoints.explore import ExploreBaseEndpoint
from tenable.io.v3.base.schema.explore.filters import FilterSchema
from tenable.io.v3.base.schema.explore.search import SearchSchema
from tenable.io.v3.schema import UserEditSchema, UsersCreateSchema
from tenable.utils import dict_merge


class UsersAPI(ExploreBaseEndpoint):
    '''
    This will contain all methods related to Users
    '''

    _path = 'v3/users'
    _conv_json = True

    def create(
        self,
        username: str,
        password: str,
        permissions: int,
        name: str = None,
        email: str = None,
        account_type: str = None,
    ) -> Dict:
        '''
        Create a new user.

        :devportal:`users: create <users-create>`

        Args:
            username (str): The username for the new user.
            password (str): The password for the new user.
            permissions (int):
                The permissions role for the user.  The permissions integer
                is derived based on the desired role of the user.  For details
                describing what permissions values mean what roles, please
                refer to the
                `User Roles <https://cloud.tenable.com/api#/authorization>`_
                table to see what permissions are accepted.
            name (str, optional): The human-readable name of the user.
            email (str, optional): The email address of the user.
            account_type (str, optional):
                The account type for the user.  The default is `local`.

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

    def delete(self, user_id: int) -> None:
        '''
        Removes a user from Tenable.io.

        :devportal:`users: delete <users-delete>`

        Args:
            user_id (int): The unique identifier of the user.

        Returns:
            :obj:`None`:
                The user was successfully deleted.

        Examples:
            >>> tio.v3.vm.users.delete(1)
        '''
        self._delete(str(user_id))

    def details(self, user_id: int) -> Dict:
        '''
        Retrieve the details of a user.

        :devportal:`users: details <users-details>`

        Args:
            user_id (int): The unique identifier for the user.

        Returns:
            :obj:`dict`:
                The resource record for the user.

        Examples:
            >>> user = tio.v3.vm.users.details(1)
        '''
        return self._get(str(user_id))

    def edit(
        self,
        user_id: int,
        permissions: int = None,
        name: str = None,
        email: str = None,
        enabled: bool = None,
    ) -> Dict:
        '''
        Modify an existing user.

        :devportal:`users: edit <users-edit>`

        Args:
            user_id (int): The unique identifier for the user.
            permissions (int, optional):
                The permissions role for the user.  The permissions integer
                is derived based on the desired role of the user.  For details
                describing what permissions values mean what roles, please
                refer to the
                `User Roles <https://cloud.tenable.com/api#/authorization>`_
                table to see what permissions are accepted.
            name (str, optional): The human-readable name of the user.
            email (str, optional): The email address of the user.
            enabled (bool, optional): Is the user account enabled?

        Returns:
            :obj:`dict`:
                The modified user resource record.

        Examples:
            >>> user = tio.v3.vm.users.edit(1, name='New Full Name')
        '''
        payload = dict_clean(
            dict(
                permissions=permissions,
                name=name, email=email,
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
        return self._put(str(user_id), json=payload)

    def enabled(self, user_id: int, enabled: bool) -> Dict:
        '''
        Enable the user account.

        :devportal:`users: enabled <users-enabled>`

        Args:
            user_id (int): The unique identifier for the user.
            enabled (bool): Is the user enabled?

        Returns:
            :obj:`dict`:
                The modified user resource record.

        Examples:
            Enable a user:

            >>> tio.v3.vm.users.enabled(1, True)

            Disable a user:

            >>> tio.v3.vm.users.enabled(1, False)
        '''
        return self._put(f'{user_id}/enabled', json={'enabled': enabled})

    def two_factor(
        self, user_id: int, email: bool, sms: bool, phone: str = None
    ) -> None:
        '''
        Configure two-factor authorization for a specific user.

        :devportal:`users: two-factor <users-two-factor>`

        Args:
            user_id (int): The unique identifier for the user.
            email (bool):
                Whether two-factor should be additionally sent as an email.
            sms (bool):
                Whether two-factor should be enabled. This will send SMS codes.
            phone (str, optional):
                The phone number to use for two-factor authentication.
                Required when sms is set to `True`.

        Returns:
            :obj:`None`:
                Setting changes were successfully updated.

        Examples:
            Enable email authorization for a user:

            >>> tio.v3.vm.users.two_factor(1, True, False)

            Enable SMS authorization for a user:

            >>> tio.v3.vm.users.two_factor(1, False, True, '9998887766')
        '''
        payload = {'email_enabled': email, 'sms_enabled': sms}
        if phone:
            payload['sms_phone'] = phone
        self._put(f'{user_id}/two-factor', json=payload)

    def enable_two_factor(
            self, user_id: int, phone: str, password: str
    ) -> None:
        '''
        Enable phone-based two-factor authorization for a specific user.

        :devportal:`users: two-factor-enable <users-two-factor-enable>`

        Args:
            user_id (int): The user id
            phone (str): The phone number to use for two-factor auth.
            password (str): The user password.

        Returns:
            :obj:`None`:
                One-time activation code sent to the provided phone number.

        Examples:
            >>> tio.v3.vm.users.enable_two_factor(1, '9998887766', 'password')
        '''
        self._post(
            f'{user_id}/two-factor/send-verification',
            json={'sms_phone': phone, 'password': password},
        )

    def verify_two_factor(self, user_id: int, code: str) -> None:
        '''
        Send the verification code for two-factor authorization.

        :devportal:`users:
            two-factor-enable-verify <users-two-factor-enable-verify>`

        Args:
            user_id (int): The user id
            code (str): The verification code that was sent to the device.

        Returns:
            :obj:`None`:
                The verification code was valid and two-factor is enabled.

        Examples:
            >>> tio.v3.vm.users.verify_two_factor(1, 'abc123')
        '''
        self._post(
            f'{user_id}/two-factor/verify-code',
            json={'verification_code': code}
        )

    # todo -> this method is still in progress
    def search_users(self, *filters, **kw):
        '''
        Retrieves the users.

        Requires -
            fields -- list of string = ['field1', 'field2']
            filter -- tuple
                ('field_name', 'operator', 'value') --
                ('and', ('test', 'oper', '1'),
                ('test', 'oper', '2'))
            sort -- list of dictionary
                    [{'property': 'field_name', 'order': 'asc'}]
                 -- sort is not supported by search api for now.
            limit -- integer = (10)
            next -- integer = (10)
        '''

        filterSchema = FilterSchema()
        search_schema = SearchSchema()
        # sort_schema = SortSchema()
        query = filterSchema.dump(filterSchema.load(filters[0]))
        # todo try with multiple dict for sorting.
        # sr = dict(property='name', order='asc')
        # srl = sort_schema.load(sr)
        # making a dictionary which will consists of all the key value pairs.
        kw.update({'filter': query})

        sed = search_schema.dump(search_schema.load(kw))
        print(sed)

    def change_password(
        self, user_id: int, old_password: str, new_password: str
    ) -> None:
        '''
        Change the password for a specific user.

        :devportal:`users: password <users-password>`

        Args:
            user_id (int): The unique identifier for the user.
            old_password (str): The current password.
            new_password (str): The new password.

        Returns:
            :obj:`None`:
                The password has been successfully changed.

        Examples:
            >>> tio.v3.vm.users.change_password(1, 'old_pass', 'new_pass')
        '''
        self._put(
            f'{user_id}/chpasswd',
            json={'password': new_password, 'current_password': old_password},
        )

    def gen_api_keys(self, user_id: int) -> Dict:
        '''
        Generate the API keys for a specific user.

        :devportal:`users: keys <user-keys>`

        Args:
            user_id (int): The unique identifier for the user.

        Returns:
            :obj:`dict`:
                A dictionary containing the new API Key-pair.

        Examples:
            >>> keys = tio.v3.vm.users.gen_api_keys(1)
        '''
        return self._put(f'{user_id}/keys')

    def list_auths(self, user_id: int) -> Dict:
        '''
        list user authorizations for accessing a Tenable.io instance.

        :devportal:`users: list-auths <users-list-auths>`

        Args:
            user_id (int): The unique identifier for the user.

        Returns:
            :obj:`dict`:
                Returns authorizations for the user.

        Examples:
            >>> auth = tio.v3.vm.users.list_auths(1)
        '''
        return self._get(f'{user_id}/authorizations')

    def edit_auths(
        self,
        user_id: int,
        api_permitted: bool = None,
        password_permitted: bool = None,
        saml_permitted: bool = None,
    ) -> None:
        '''
        update user authorizations for accessing a Tenable.io instance.

        :devportal:`users: edit-auths <users-update-auths>`

        Args:
            user_id (int):
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
            >>> tio.v3.vm.users.edit_auths(1, True, True, False)
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
