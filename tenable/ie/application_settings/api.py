'''
Application Settings
====================

Methods described in this section relate to the application settings API.
These methods can be accessed at ``TenableIE.application_settings``.

.. rst-class:: hide-signature
.. autoclass:: ApplicationSettingsAPI
    :members:
'''
from typing import Dict
from tenable.ie.application_settings.schema import ApplicationSettingsSchema
from tenable.base.endpoint import APIEndpoint


class ApplicationSettingsAPI(APIEndpoint):
    _path = 'application-settings'
    _schema = ApplicationSettingsSchema()

    def details(self) -> Dict:
        '''
        Get the application settings

        Returns:
            dict:
                The application settings objects

        Examples:
            >>> tie.application_settings.get_settings()
        '''
        return self._schema.load(self._get())

    def update(self,
               **kwargs
               ) -> Dict:
        '''
        Update the application settings

        Args:
            smtp_server_address (optional, str):
                The IP address of the SMTP server to use to send mails.
            smtp_server_port (optional, int):
                The port of SMTP server to use to send mails.
            smtp_account (optional, str):
                The login to use to authenticate against SMTP server.
            smtp_account_password (optional, str):
                The password to use to authenticate against SMTP server.
            smtp_use_start_tls (optional, bool):
                Whether the startTLS SMTP command should be used to secure
                the connection to the SMTP server?
            tls (optional, bool):
                Whether the configured server should connect using TLS?
            email_sender (optional, str):
                The email address to display as the sender in the emails sent.
            default_role_ids (optional, list[int]):
                The default role identifiers.
            default_profile_id (optional, int):
                The default profile identifier.
            internal_certificate (optional, str):
                The certificate chain to use to verify certificates on TLS
                connections.

        Return:
            dict:
                The application settings objects

        Example:
            >>> tie.application_settings.update_settings(
            ...     smtp_use_start_tls=True,
            ...     tls=False,
            ...     default_profile_id=1,
            ...     )
        '''
        payload = self._schema.dump(self._schema.load(kwargs))
        return self._schema.load(self._patch(json=payload))
