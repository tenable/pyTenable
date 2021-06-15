'''
users
=====

The following methods allow for interaction into the Tenable.io
:devportal:`users <users>` API endpoints.

Methods available on ``tio.users``:

.. rst-class:: hide-signature
.. autoclass:: UsersAPI

    .. automethod:: create
    .. automethod:: change_password
    .. automethod:: delete
    .. automethod:: details
    .. automethod:: edit
    .. automethod:: enabled
    .. automethod:: gen_api_keys
    .. automethod:: two_factor
    .. automethod:: enable_two_factor
    .. automethod:: verify_two_factor
    .. automethod:: impersonate
    .. automethod:: list
    .. automethod:: list_auths
    .. automethod:: edit_auths
'''
from tenable.utils import dict_merge
from tenable.io.base import TIOEndpoint

class UsersAPI(TIOEndpoint):
    '''
    This will contain all methods related to Users
    '''
    def create(self, username, password, permissions,
            name=None, email=None, account_type=None):
        '''
        Create a new user.

        :devportal:`users: create <users-create>`

        Args:
            username (str): The username for the new user.
            password (str): The password for the new user.
            permissions (int):
                The permissions role for the user.  The permissions integer
                is derived based on the desired role of the user.  For details
                describing what permissions values mean what roles, please refer
                to the `User Roles <https://cloud.tenable.com/api#/authorization>`_
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

            >>> user = tio.users.create('jsmith@company.com', 'password1', 32)

            Create an admin user and add the email and name:

            >>> user = tio.users.create('jdoe@company.com', 'password', 64,
            ...     name='Jane Doe', email='jdoe@company.com')

        '''
        payload = {
            'username': self._check('username', username, str),
            'password': self._check('password', password, str),
            'permissions': self._check('permissions', permissions, int),
            'type': self._check('account_type', account_type, str, default='local'),
        }

        if name:
            payload['name'] = self._check('name', name, str)
        if email:
            payload['email'] = self._check('email', email, str)

        return self._api.post('users', json=payload).json()

    def delete(self, user_id):
        '''
        Removes a user from Tenable.io.

        :devportal:`users: delete <users-delete>`

        Args:
            user_id (int): The unique identifier of the user.

        Returns:
            :obj:`None`:
                The user was successfully deleted.

        Examples:
            >>> tio.users.delete(1)
        '''
        self._api.delete('users/{}'.format(self._check('user_id', user_id, int)))

    def details(self, user_id):
        '''
        Retrieve the details of a user.

        :devportal:`users: details <users-details>`

        Args:
            user_id (int): The unique identifier for the user.

        Returns:
            :obj:`dict`:
                The resource record for the user.

        Examples:
            >>> user = tio.users.details(1)
        '''
        return self._api.get('users/{}'.format(self._check('user_id', user_id, int))).json()

    def edit(self, user_id, permissions=None, name=None, email=None, enabled=None):
        '''
        Modify an existing user.

        :devportal:`users: edit <users-edit>`

        Args:
            user_id (int): The unique identifier for the user.
            permissions (int, optional):
                The permissions role for the user.  The permissions integer
                is derived based on the desired role of the user.  For details
                describing what permissions values mean what roles, please refer
                to the `User Roles <https://cloud.tenable.com/api#/authorization>`_
                table to see what permissions are accepted.
            name (str, optional): The human-readable name of the user.
            email (str, optional): The email address of the user.
            enabled (bool, optional): Is the user account enabled?

        Returns:
            :obj:`dict`:
                The modified user resource record.

        Examples:
            >>> user = tio.users.edit(1, name='New Full Name')
        '''
        payload = dict()

        if permissions:
            payload['permissions'] = self._check('permissions', permissions,
                                                 int)
        if enabled is not None:
            payload['enabled'] = self._check('enabled', enabled, bool)
        if email:
            payload['email'] = self._check('email', email, str)
        if name:
            payload['name'] = self._check('name', name, str)

        # Merge the data that we build with the payload with the user details.
        user = self.details(self._check('user_id', user_id, int))
        payload = dict_merge({
            'permissions': user['permissions'],
            'enabled': user['enabled'],
            'email': user['email'],
            'name': user.get('name', None),
        }, payload)
        return self._api.put('users/{}'.format(user_id), json=payload).json()

    def enabled(self, user_id, enabled):
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

            >>> tio.users.enabled(1, True)

            Disable a user:

            >>> tio.users.enabled(1, False)
        '''
        return self._api.put('users/{}/enabled'.format(
            self._check('user_id', user_id, int)), json={
                'enabled': self._check('enabled', enabled, bool)}).json()

    def two_factor(self, user_id, email, sms, phone=None):
        '''
        Configure two-factor authorization for a specific user.

        :devportal:`users: two-factor <users-two-factor>`

        Args:
            user_id (int): The unique identifier for the user.
            email (bool):
                Whether two-factor should be additionally sent as an email.
            sms (bool):
                Whether two-factor should be enabled.  This will send SMS codes.
            phone (str, optional):
                The phone number to use for two-factor authentication.  Required
                when sms is set to `True`.

        Returns:
            :obj:`None`:
                Setting changes were successfully updated.

        Examples:
            Enable email authorization for a user:

            >>> tio.users.two_factor(1, True, False)

            Enable SMS authorization for a user:

            >>> tio.users.two_factor(1, False, True, '9998887766')
        '''
        payload = {
            'email_enabled': self._check('email', email, bool),
            'sms_enabled': self._check('sms', sms, bool)
        }
        if phone:
            payload['sms_phone'] = self._check('phone', phone, str)
        self._api.put('users/{}/two-factor'.format(
            self._check('user_id', user_id, int)), json=payload)

    def enable_two_factor(self, user_id, phone):
        '''
        Enable phone-based two-factor authorization for a specific user.

        :devportal:`users: two-factor-enable <users-two-factor-enable>`

        Args:
            phone (str): The phone number to use for two-factor auth.

        Returns:
            :obj:`None`:
                One-time activation code sent to the provided phone number.

        Examples:
            >>> tio.users.enable_two_factor(1, '9998887766')
        '''
        self._api.post('users/{}/two-factor/send-verification'.format(
            self._check('user_id', user_id, int)), json={
                'sms_phone': self._check('phone', phone, str)})

    def verify_two_factor(self, user_id, code):
        '''
        Send the verification code for two-factor authorization.

        :devportal:`users: two-factor-enable-verify <users-two-factor-enable-verify>`

        Args:
            code (str): The verification code that was sent to the device.

        Returns:
            :obj:`None`:
                The verification code was valid and two-factor is enabled.

        Examples:
            >>> tio.users.verify_two_factor(1, 'abc123')
        '''
        self._api.post('users/{}/two-factor/verify-code'.format(
            self._check('user_id', user_id, int)), json={
                'verification_code': self._check('code', code, str)})

    def impersonate(self, name):
        '''
        Impersonate as a specific user.

        :devportal:`users: impersonate <users/impersonate>`

        Args:
            name (str): The user-name of the user to impersonate.

        Returns:
            :obj:`None`:
                Impersonation successful.

        Examples:
            >>> tio.users.impersonate('jdoe@company.com')
        '''
        self._api._session.headers.update({
            'X-Impersonate': 'username={}'.format(self._check('name', name, str))
        })

    def list(self):
        '''
        Retrieves a list of users.

        :devportal:`users: list <users-list>`

        Returns:
            :obj:`list`:
                List of user resource records.

        Examples:
            >>> for user in tio.users.list():
            ...     pprint(user)
        '''
        return self._api.get('users').json()['users']

    def change_password(self, user_id, old_password, new_password):
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
            >>> tio.users.change_password(1, 'old_pass', 'new_pass')
        '''
        self._api.put('users/{}/chpasswd'.format(self._check('user_id', user_id, int)), json={
            'password': self._check('new_password', new_password, str),
            'current_password': self._check('old_password', old_password, str)
        })

    def gen_api_keys(self, user_id):
        '''
        Generate the API keys for a specific user.

        :devportal:`users: keys <user-keys>`

        Args:
            user_id (int): The unique identifier for the user.

        Returns:
            :obj:`dict`:
                A dictionary containing the new API Key-pair.

        Examples:
            >>> keys = tio.users.gen_api_keys(1)
        '''
        return self._api.put('users/{}/keys'.format(
            self._check('user_id', user_id, int))).json()

    def list_auths(self, user_id):
        '''
        list user authorizations for accessing a Tenable.io instance.

        :devportal:`users: list-auths <users-list-auths>`

        Args:
            user_id (int): The unique identifier for the user.

        Returns:
            :obj:`dict`:
                Returns authorizations for the user.

        Examples:
            >>> auth = tio.users.list_auths(1)
        '''
        return self._api.get('users/{}/authorizations'.format(
            self._check('user_id', user_id, int))).json()

    def edit_auths(self, user_id, api_permitted=None, password_permitted=None, saml_permitted=None):
        '''
        update user authorizations for accessing a Tenable.io instance.

        :devportal:`users: edit-auths <users-update-auths>`

        Args:
            user_id (int):
                The unique identifier for the user.
            api_permitted (bool):
                Indicates whether API access is authorized for the user.
            password_permitted (bool):
                Indicates whether user name and password login is authorized for the user.
            saml_permitted (bool):
                Indicates whether SSO with SAML is authorized for the user.

        Returns:
            :obj:`None`:
                Returned if Tenable.io successfully updates the user's authorizations.

        Examples:
            >>> tio.users.edit_auths(1, True, True, False)
        '''
        # get current settings
        current = self.list_auths(self._check('user_id', user_id, int))

        # update payload with new settings
        payload = {
            'api_permitted': self._check('api_permitted', api_permitted, bool,
                default=current['api_permitted']),
            'password_permitted': self._check('password_permitted', password_permitted, bool,
                default=current['password_permitted']),
            'saml_permitted': self._check('saml_permitted', saml_permitted, bool,
                default=current['saml_permitted'])
        }

        return self._api.put('users/{}/authorizations'.format(
            self._check('user_id', user_id, int)), json=payload)
