from tenable.tenable_io.base import TIOEndpoint
from tenable.errors import ImpersonationError, UnknownError

class SessionAPI(TIOEndpoint):
    def edit(self, name, email):
        '''
        `session: edit <https://cloud.tenable.com/api#/resources/session/edit>`_

        Args:
            name (str): The full name of the user.
            email (str): The email address of the user.

        Returns:
            dict: The session data for the current user.
        '''
        return self._api.put('session', json={
            'name': self._check('name', name, str),
            'email': self._check('email', email, str)
            }).json()

    def get(self):
        '''
        `session: get <https://cloud.tenable.com/api#/resources/session/get>`_

        Returns:
            dict: The user's session resource record.
        '''
        return self._api.get('session').json()

    def change_password(self, old_password, new_password):
        '''
        `session: password <https://cloud.tenable.com/api#/resources/session/password>`_

        Args:
            old_password (str): The current password.
            new_password (str): The new password.

        Returns:
            None: The password has been successfully changed.
        '''
        self._api.put('session/chpasswd', json={
            'password': self._check('new_password', new_password, str),
            'current_password': self._check('old_password', old_password, str)
        })

    def gen_api_keys(self):
        '''
        `session: keys <https://cloud.tenable.com/api#/resources/session/keys>`_

        Returns:
            dict: A dictionary containing the new API Keypair.
        '''
        return self._api.put('session/keys').json()

    def two_factor(self, email, sms, phone=None):
        '''
        `session: two-factor <https://cloud.tenable.com/api#/resources/session/two-factor>`_

        Args:
            email (bool): 
                Whether two-factor should be additionally sent as an email.
            sms (bool):
                Whether two-factor should be enabled.  This will send SMS codes.
            phone (str, optional):
                The phone number to use for two-factor authentication.  Required
                when sms is set to `True`.
        
        Returns:
            None: Setting changes were successfully updated.
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
        `session: two-factor-enable <https://cloud.tenable.com/api#/resources/session/two-factor-enable>`_

        Args:
            phone (str): The phone number to use for two-factor auth.

        Returns:
            None: One-time activation code sent to the provided phone number.
        '''
        self._api.post('session/two-factor/send-verification', json={
            'sms_phone': self._check('phone', phone, str)
        })

    def verify_two_factor(self, code):
        '''
        `session: two-factor-enable-verify <https://cloud.tenable.com/api#/resources/session/two-factor-enable-verify>`_

        Args:
            code (str): The verification code that was sent to the device.

        Returns:
            None: The verification code was valid and two-factor is enabled.
        '''
        self._api.post('session/two-factor/verify-code', json={
            'verification_code': self._check('code', code, str)
        })

    def restore(self):
        '''
        `session: restore <https://cloud.tenable.com/api#/resources/session/restore>`_

        Returns:
            None: The session has properly been restored to the original user.
        '''
        self._api._session.headers.update({
            'X-Impersonate': None
        })
        