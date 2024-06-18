'''
SAML Configuration
==================

Methods described in this section relate to the SAML Configuration API.
These methods can be accessed at ``TenableIE.saml_configuration``.

.. rst-class:: hide-signature
.. autoclass:: SAMLConfigurationAPI
    :members:
'''
from typing import Dict
from tenable.ie.saml_configuration.schema import SAMLConfigurationSchema
from tenable.base.endpoint import APIEndpoint


class SAMLConfigurationAPI(APIEndpoint):
    _path = 'saml-configuration'
    _schema = SAMLConfigurationSchema()

    def details(self) -> Dict:
        '''
        Retrieves the details of the SAML-configuration singleton.

        Returns:
            dict:
                The details of saml configuration singleton.

        Examples:
            >>> tie.saml_configuration.details()
        '''
        return self._schema.load(self._get())

    def update(self,
               **kwargs
               ) -> Dict:
        '''
        Updates the SAML-configuration.

        Args:
            enabled (optional, bool):
                Whether the SAML configuration is enabled or not.
            provider_login_url (optional, str):
                The URL of the identity provider to reach for
                SAML authentication.
            signature_certificate (optional, str):
                The certificate used to sign the SAML authentication.
            activate_created_users (optional, bool):
                Whether the created users through SAML authentication should be
                activated. If false, created users will be disabled until an
                admin comes and activate them.
            allowed_groups (optional, List[Dict]):
                The group names from the identity provider whose members are
                allowed to use tenable.ie. The below listed params are
                expected in allowed_groups dict.
            name (required, str):
                The name of SAML Configuration.
            default_profile_id (required, int):
                The default profile instance identifier of SAML Configuration.
            default_role_ids (required, list(int)):
                The default role instance identifier of SAML Configuration.

        Returns:
            dict:
                The updated saml-configuration.

        Examples:
            >>> tie.saml_configuration.update(
            ...     enabled=True,
            ...     allowed_groups=[{
            ...         'name': 'updated_name',
            ...         'default_profile_id': 1,
            ...         'default_role_ids': [1, 2]
            ...     }]
            ...     )
        '''
        payload = self._schema.dump(self._schema.load(kwargs))
        return self._schema.load(self._patch(json=payload))

    def generate_saml_certificate(self) -> Dict:
        '''
        Generates a SAML certificate.

        Returns:
            dict:
                Generated certificate.

        Examples:
            >>> tie.saml_configuration.generate_saml_certificate()
        '''
        return self._schema.load(self._get(f'generate-certificate'))
