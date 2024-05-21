'''
Session
=======

The following methods allow for interaction into the Tenable Vulnerability Management
:devportal:`session <session>` API endpoints.

Methods available on ``tio.session``:

.. rst-class:: hide-signature
.. autoclass:: SessionAPI
    :members:
'''
from .base import TIOEndpoint


class SessionAPI(TIOEndpoint):
    '''
    Tenable Vulnerability Management session API is deprecated.
    it is recommended to use ``users`` endpoint instead
    '''

    def edit(self, name, email):
        '''
        Modify the currently logged-in user.

        :devportal:`session: edit <session-edit>`

        Args:
            name (str): The full name of the user.
            email (str): The email address of the user.

        Returns:
            :obj:`dict`:
                The session data for the current user.

        Examples:
            >>> tio.session.edit('John Doe', 'joe@company.com')
        '''
        return self._api.put('session', json={
            'name': self._check('name', name, str),
            'email': self._check('email', email, str)
            }).json()

    def details(self):
        '''
        Retrieve the current users resource record.

        :devportal:`session: get <session-get>`

        Returns:
            :obj:`dict`:
                The user's session resource record.

        Examples:
            >>> user = tio.session.details()
            >>> pprint(user)
        '''
        return self._api.get('session').json()

    def change_password(self, old_password, new_password):
        '''
        Change the password of the current user.

        :devportal:`session: password <session-password>`

        Args:
            old_password (str): The current password.
            new_password (str): The new password.

        Returns:
            :obj:`None`:
                The password has been successfully changed.

        Examples:
            >>> tio.session.change_password('old_pass', 'new_pass')
        '''
        self._api.put('session/chpasswd', json={
            'password': self._check('new_password', new_password, str),
            'current_password': self._check('old_password', old_password, str)
        })

    def gen_api_keys(self):
        '''
        Generate new API keys for the current user.

        :devportal:`session: keys <session-keys>`

        Returns:
            :obj:`dict`:
                A dictionary containing the new API Keypair.

        Examples:
            >>> keys = tio.session.gen_api_keys()
        '''
        return self._api.put('session/keys').json()

    def two_factor(self, email, sms, phone=None):
        '''
        Configure two-factor authorization.

        :devportal:`session: two-factor <session-two-factor-settings>`

        Args:
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

        Example:
            Configure email multi-factor auth:

            >>> tio.session.two_factor(True, False)

            Configure SMS multi-factor auth:

            >>> tio.session.two_factor(False, True, '9998887766')
        '''
        payload = {
            'email_enabled': self._check('email', email, bool),
            'sms_enabled': self._check('sms', sms, bool)
        }
        if phone:
            payload['sms_phone'] = self._check('phone', phone, str)
        self._api.put('session/two-factor', json=payload)

    def enable_two_factor(self, phone):
        '''
        Initiate the phone-based two-factor authorization verification process.

        :devportal:`session: two-factor-enable <session-send-code>`

        Args:
            phone (str): The phone number to use for two-factor auth.

        Returns:
            :obj:`None`:
                One-time activation code sent to the provided phone number.

        Examples:
            >>> tio.session.enable_two_factor('9998887766')
        '''
        self._api.post('session/two-factor/send-verification', json={
            'sms_phone': self._check('phone', phone, str)
        })

    def verify_two_factor(self, code):
        '''
        Send the verification code for two-factor authorization.

        :devportal:`session: verify-code <session-verify-code>`

        Args:
            code (str): The verification code that was sent to the device.

        Returns:
            :obj:`None`:
                The verification code was valid and two-factor is enabled.

        Examples:
            >>> tio.session.verify_two_factor('abc123')
        '''
        self._api.post('session/two-factor/verify-code', json={
            'verification_code': self._check('code', code, str)
        })

    def restore(self):
        '''
        Restore the session to the logged-in user.  This will remove any user
        impersonation setting that have been set.

        :devportal:`session: restore <session-restore>`

        Returns:
            :obj:`None`:
                The session has properly been restored to the original user.

        Example:
            >>> tio.session.restore()
        '''
        self._api._session.headers.update({
            'X-Impersonate': None
        })
