'''
users
=====

The following methods allow for interaction into the Tenable.io 
`users <https://cloud.tenable.com/api#/resources/users>`_ API endpoints.

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
'''
from.base import TIOEndpoint
from tenable.errors import UnknownError, PasswordComplexityError
from tenable.utils import dict_merge

class UsersAPI(TIOEndpoint):
    def create(self, username, password, permissions, 
            name=None, email=None, account_type=None):
        '''
        Create a new user.

        `users: create <https://cloud.tenable.com/api#/resources/users/create>`_

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
            dict: The resorce record fo the new user.

        Examples:
            Create a standard user:

            >>> user = tio.users.create('jsmith@company.com', 'password1', 32)

            Create an admin user and add the email and name:

            >>> user = tio.create.users('jdoe@company.com', 'password', 64,
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

    def delete(self, id):
        '''
        Removes a user from Tenable.io.

        `users: delete <https://cloud.tenable.com/api#/resources/users/delete>`_

        Args:
            id (int): The unique identifier of the user.

        Returns:
            None: The user was successfully deleted.

        Examples:
            >>> tio.users.delete(1)
        '''
        self._api.delete('users/{}'.format(self._check('id', id, int)))

    def details(self, id):
        '''
        Retrieve the details of a user.

        `users: details <https://cloud.tenable.com/api#/resources/users/details>`_

        Args:
            id (int): THe unique identifier for the user.

        Returns:
            dict: The resource record for the user.

        Examples:
            >>> user = tio.users.details(1)
        '''
        return self._api.get('users/{}'.format(self._check('id', id, int))).json()

    def edit(self, id, permissions=None, name=None, email=None, enabled=None):
        '''
        Modify an existing user.

        `users: edit <https://cloud.tenable.com/api#/resources/users/edit>`_

        Args:
            id (int): The unique identifier for the user.
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
            dict: The modified user resource record.

        Examples:
            >>> user = tio.users.edit(1, name='New Full Name')
        '''
        payload = dict()

        if permissions:
            payload['permisions'] = self._check('permissions', permissions, int)
        if enabled is not None:
            payload['enabled'] = self._check('enabled', enabled, bool)
        if email:
            payload['email'] = self._check('email', email, str)
        if name:
            payload['name'] = self._check('name', name, str)

        # Merge the data that we build with the payload with the user details.
        user = self.details(self._check('id', id, int))
        payload = dict_merge({
            'permissions': user['permissions'],
            'enabled': user['enabled'],
            'email': user['email'],
            'name': user['name'],
        }, payload)
        return self._api.put('users/{}'.format(id), json=payload).json()

    def enabled(self, id, enabled):
        '''
        Enable the user account.

        users: enabled <https://cloud.tenable.com/api#/resources/users/enabled>`_

        Args:
            id (int): The unique identifier for the user.
            enabled (bool): Is the user enabled?

        Returns:
            dict: The modified user resource record.

        Examples:
            Enable a user:

            >>> tio.users.enabled(1, True)

            Disable a user:

            >>> tio.users.enabled(1, False)
        '''
        return self._api.put('users/{}/enabled'.format(
            self._check('id', id, int)), json={
                'enabled': self._check('enabled', enabled, bool)}).json()

    def two_factor(self, id, email, sms, phone=None):
        '''
        Configure two-factor authorization for a specific user.

        `users: two-factor <https://cloud.tenable.com/api#/resources/users/two-factor>`_

        Args:
            id (int): The unique identifier for the user.
            email (bool): 
                Whether two-factor should be additionally sent as an email.
            sms (bool):
                Whether two-factor should be enabled.  This will send SMS codes.
            phone (str, optional):
                The phone number to use for two-factor authentication.  Required
                when sms is set to `True`.
        
        Returns:
            None: Setting changes were successfully updated.

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
            self._check('id', id, int)), json=payload)

    def enable_two_factor(self, id, phone):
        '''
        Enable phone-based two-factor authorization for a specific user.

        `users: two-factor-enable <https://cloud.tenable.com/api#/resources/users/two-factor-enable>`_

        Args:
            phone (str): The phone number to use for two-factor auth.

        Returns:
            None: One-time activation code sent to the provided phone number.

        Examples:
            >>> tio.users.enable_two_factor(1, '9998887766')
        '''
        self._api.post('users/{}/two-factor/send-verification'.format(
            self._check('id', id, int)), json={
                'sms_phone': self._check('phone', phone, str)})

    def verify_two_factor(self, id, code):
        '''
        Send the verification code for two-factor authorization.

        `users: two-factor-enable-verify <https://cloud.tenable.com/api#/resources/users/two-factor-enable-verify>`_

        Args:
            code (str): The verification code that was sent to the device.

        Returns:
            None: The verification code was valid and two-factor is enabled.

        Examples:
            >>> tio.users.verify_two_factor(1, 'abc123')
        '''
        self._api.post('users/{}/two-factor/verify-code'.format(
            self._check('id', id, int)), json={
                'verification_code': self._check('code', code, str)})

    def impersonate(self, name):
        '''
        Impersonate as a specific user.

        `users: impersonate <https://cloud.tenable.com/api#/resources/users/impersonate>`_

        Args:
            name (str): The user-name of the user to impersonate.

        Returns:
            None: Impersonation successful.

        Examples:
            >>> tio.users.impersonate('jdoe@company.com')
        '''
        self._api._session.headers.update({
            'X-Impersonate': 'username={}'.format(self._check('name', name, str))
        })

    def list(self):
        '''
        Retrieves a list of users.

        `users: list <https://cloud.tenable.com/api#/resources/users/list>`_

        Returns:
            list: List of user resource records.

        Examples:
            >>> for user in tio.users.list():
            ...     pprint(user)
        '''
        return self._api.get('users').json()['users']

    def change_password(self, id, old_password, new_password):
        '''
        Change the password for a specific user.

        `users: password <https://cloud.tenable.com/api#/resources/users/password>`_

        Args:
            id (int): The unique identifier for the user.
            old_password (str): The current password.
            new_password (str): The new password.

        Returns:
            None: The password has been successfully changed.

        Examples:
            >>> tio.users.change_password(1, 'old_pass', 'new_pass')
        '''
        self._api.put('users/{}/chpasswd'.format(self._check('id', id, int)), json={
            'password': self._check('new_password', new_password, str),
            'current_password': self._check('old_password', old_password, str)
        })

    def gen_api_keys(self, id):
        '''
        Generate the API keys for a specific user.

        `users: keys <https://cloud.tenable.com/api#/resources/user/keys>`_

        Args:
            id (int): The unique identifier for the user.

        Returns:
            dict: A dictionary containing the new API Key-pair.

        Examples:
            >>> keys = tio.users.gen_api_keys(1)
        '''
        return self._api.put('users/{}/keys'.format(
            self._check('id', id, int))).json()




