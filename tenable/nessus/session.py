'''
Session
=======

Methods described in this section relate to the session API.
These methods can be accessed at ``Nessus.session``.

.. rst-class:: hide-signature
.. autoclass:: SessionAPI
    :members:
'''
from typing import Dict, Optional
from restfly.utils import dict_clean
from tenable.base.endpoint import APIEndpoint


class SessionAPI(APIEndpoint):
    _path = 'session'

    def get(self) -> Dict:
        '''
        Returns the current user's session data

        Returns:
            Dict:
                The session details dictionary

        Example:

            >>> nessus.session.get()
        '''
        return self._get()

    def chpasswd(self, current_password, new_password) -> None:
        '''
        Updated the current user's password.

        Args:
            current_password (str): The user's current password
            new_password (str): The new password for the user

        Example:

            >>> nessus.session.chpasswd('old_pass', 'new_pass')
        '''
        self._put('chpasswd', json={'password': new_password,
                                    'current_password': current_password
                                    })

    def api_keys(self) -> Dict:
        '''
        Generates a new API key pair for the current user.  The API Keys for
        the current session will also be updated if the auth mechanism is api
        keys

        Returns:
            Dict:
                The newly generated keypair for the user.

        Example:

            >>> nessus.session.api_keys()
        '''
        keys = self._put('keys')
        if self._api._auth_mech == 'keys':
            self._api._key_auth(keys['accessKey'], keys['secretKey'])
        return keys

    def edit(self, name: Optional[str] = None,
             email: Optional[str] = None
             ) -> None:
        '''
        Updates the current user's settings.

        Args:
            name (str, optional): Updated name for the user
            email (str, optional): Updated email for the user

        Example:

            >>> nessus.session.edit(email='user@name.com')
        '''
        self._put(json=dict_clean({
            'name': name,
            'email': email
        }))
