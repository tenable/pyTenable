'''
LDAP Configuration
==================

Methods described in this section relate to the ldap configuration API.
These methods can be accessed at ``TenableIE.ldap_configuration``.

.. rst-class:: hide-signature
.. autoclass:: LDAPConfigurationAPI
    :members:
'''
from typing import Dict
from tenable.ie.ldap_configuration.schema import LDAPConfigurationSchema
from tenable.base.endpoint import APIEndpoint


class LDAPConfigurationAPI(APIEndpoint):
    _path = 'ldap-configuration'
    _schema = LDAPConfigurationSchema()

    def details(self) -> Dict:
        '''
        Get LDAP configuration singleton

        Returns:
            dict:
                The LDAP configuration object

        Examples:
            >>> tie.ldap_configuration.details()
        '''
        return self._schema.load(self._get())

    def update(self,
               **kwargs
               ) -> Dict:
        '''
        Update LDAP configuration singleton

        Args:
            enabled (optional, bool):
                Whether the ldap configuration enabled?
            url (optional, str):
                The URL of authentication provider server.
            search_user_dn (optional, str):
                The DN of service account to use to authenticate the user.
            search_user_password (optional, str):
                The password of the service account used for authentication.
            user_search_base (optional, str):
                The DN of the param object for items in LDAP server.
            user_search_filter (optional, str):
                Used to change on what attribute the LDAP query is made to
                authenticate the user.
            allowed_groups (optional, List[Dict]):
                The LDAP group a member need to be a member of so he can
                authenticate. The below listed params are expected in
                allowed groups dict.
            name (required, str):
                The name of group.
            default_role_ids (required, List[int]):
                The list default role identifiers.
            default_profile_id (required, int):
                The default profile identifier.

        Return:
            The LDAP configuration object

        Example:
            >>> tie.ldap_configuration.update(
            ...     enabled=True,
            ...     allowed_groups=[{
            ...         'name': 'group name',
            ...         'default_role_ids': [1, 2],
            ...         'default_profile_id': 1
            ...     }]
            ... )
        '''
        payload = self._schema.dump(self._schema.load(kwargs))
        return self._schema.load(self._patch(json=payload))
