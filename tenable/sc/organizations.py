'''
Organizations
=============

The following methods allow for interaction with the Tenable Security Center
:sc-api:`Organization <Organization.htm>` API. These items are typically seen
under the **Organization** section of Tenable Security Center.

Methods available on ``sc.organizations``:

.. rst-class:: hide-signature
.. autoclass:: OrganizationAPI
    :members:
'''
from tenable.sc.base import SCEndpoint


class OrganizationAPI(SCEndpoint):
    def _constructor(self, **kwargs):
        '''
        Organization document constructor
        '''
        if 'name' in kwargs:
            # Validate the the name attribute is a string value
            self._check('name', kwargs['name'], str)

        if 'description' in kwargs:
            # validate that the description is a string value
            self._check('description', kwargs['description'], str)

        if 'address' in kwargs:
            # validate that the address field is a string value
            self._check('address', kwargs['address'], str)

        if 'city' in kwargs:
            # validate that the city is a string value
            self._check('city', kwargs['city'], str)

        if 'state' in kwargs:
            # validate that the state is a string value
            self._check('state', kwargs['state'], str)

        if 'country' in kwargs:
            # validate that the country is a streing value.
            self._check('country', kwargs['country'], str)

        if 'phone' in kwargs:
            # validate that the phone is a string value.
            self._check('phone', kwargs['phone'], str)

        if 'lce_ids' in kwargs:
            # validate that the lce_ids is a list of integers and transform them
            # into a list of dictionaries with id attributes.
            kwargs['lces'] = [{'id': self._check('lce:id', i, int)}
                          for i in self._check('lce_ids', kwargs['lce_ids'], list)]
            del kwargs['lce_ids']

        if 'zone_selection' in kwargs:
            # validate that zone_selection is a string value of one of the
            # expected types and store it in the camelCase equiv.
            kwargs['zoneSelection'] = self._check('zone_selection',
                                              kwargs['zone_selection'], str, choices=[
                    'auto_only', 'locked', 'selectable', 'selectable+auto',
                    'selectable+auto_restricted'])
            del kwargs['zone_selection']

        if 'restricted_ips' in kwargs:
            # ensure that restricted_ips is a list of items and return it as a
            # comma-seperated string in the camelCase variant of the param.
            kwargs['restrictedIPs'] = ','.join(self._check(
                'restricted_ips', kwargs['restricted_ips'], list))
            del kwargs['restricted_ips']

        if 'repos' in kwargs:
            # convert the list of numeric ids for repos into a list of
            # dictionaries with the id attribute.
            kwargs['repositories'] = [{'id': self._check('repo:id', r, int)}
                                  for r in self._check('repos', kwargs['repos'], list)]
            del kwargs['repos']

        if 'pub_sites' in kwargs:
            # convert the list of numeric ids for pub_sites into a list of
            # dictionaries with the id attribute.
            kwargs["pubSites"] = [{'id': self._check('site:id', p, int)}
                              for p in self._check('pub_sites', kwargs['pub_sites'], list)]
            del kwargs["pub_sites"]

        if 'ldap_ids' in kwargs:
            # convert the list of numeric ids for ldap_ids into a list of
            # dictionaries with the id attribute.
            kwargs['ldaps'] = [{'id': self._check('ldap:id', p, int)}
                           for p in self._check('ldap_ids', kwargs['ldap_ids'], list)]
            del kwargs['ldap_ids']

        if 'nessus_managers' in kwargs:
            # convert the list of numeric ids for nessus managers into a list of
            # dictionaries with the id attribute.
            kwargs['nessusManagers'] = [{'id': self._check('nessus_manager:id', n, int)}
                                    for n in self._check('nessus_managers', kwargs['nessus_managers'], list)]
            del kwargs['nessus_managers']

        if 'info_links' in kwargs:
            # convert the info_links
            kwargs['ipInfoLinks'] = [{
                'name': self._check('link:name', i[0], str),
                'link': self._check('link:link', i[1], str)}
                for i in self._check('info_links', kwargs['info_links'], list)]
            del kwargs['info_links']

        if 'vuln_score_low' in kwargs:
            kwargs['vulnScoreLow'] = self._check(
                'vuln_score_low', kwargs['vuln_score_low'], int)
            del kwargs['vuln_score_low']

        if 'vuln_score_medium' in kwargs:
            kwargs['vulnScoreMedium'] = self._check(
                'vuln_score_medium', kwargs['vuln_score_medium'], int)
            del kwargs['vuln_score_medium']

        if 'vuln_score_high' in kwargs:
            kwargs['vulnScoreHigh'] = self._check(
                'vuln_score_high', kwargs['vuln_score_high'], int)
            del kwargs['vuln_score_high']

        if 'vuln_score_critical' in kwargs:
            kwargs['vulnScoreCritical'] = self._check(
                'vuln_score_critical', kwargs['vuln_score_critical'], int)
            del kwargs['vuln_score_critical']

        return kwargs

    def create(self, name, **kwargs):
        '''
        Create a new organization

        :sc-api:`SC Organization Create <Organization.htm#organization_POST>`

        Args:
            name (str): The name for organization.
            info_links (list, optional):
                A list of custom analysis links provided to users within the
                host vulnerability details when analyzing data outside of
                SecurityCenter is desired.  Links shall be described in a tuple
                format with ``(name, link)`` format.  For example:
                ``('SANS', 'https://isc.sans.edu/ipinfo.html?ip=%IP%')``
            lce_ids (list, optional):
                What Log Correlation Engines (if any) should this organization
                be allowed to access?  If left unspecified no LCE engined will
                be granted to this organization.
            ldap_ids (list, optional):
                What ldap server configuration ids should be used with this
                organization?
            nessus_managers (list, optional):
                Nessus Manager scanner for Nessus Agent scan imports.
            pub_sites (list, optional):
                A list of publishing site ids to associate this organization.
            repos (list, optional):
                A list of Repository ids to associate to this organization.
            restricted_ips (list, optional):
                A list of IP addresses, CIDRs, and/or IP ranges that should
                never be scanned.
            vuln_score_low (int):
                The vulnerability weighting to apply to low criticality
                vulnerabilities for scoring purposes. (Default: 1)
            vuln_score_medium (int):
                The vulnerability weighting to apply to medium criticality
                vulnerabilities for scoring purposes. (Default: 3)
            vuln_score_high (int):
                The vulnerability weighting to apply to high criticality
                vulnerabilities for scoring purposes. (Default: 10)
            vuln_score_critical (int):
                The vulnerability weighting to apply to critical criticality
                vulnerabilities for scoring purposes.(Default: 40)
            zone_selection (str):
                What type of scan zone selection should be performed?
                Available selection types are as follows: ``auto_only``,
                ``locked``, ``selectable+auto``,
                ``selectable+auto_restricted``.
                If left unspecified, the default is ``auto_only``.
            zones (list, optional):
                When ``zone_selection`` is not ``auto_only``, this field
                must be filled with list of ids from available scan zone(s).

        Returns:
            :obj:`dict`:
                The organization resource record for the newly created Org.

        Examples:

            Creating a new organization with automatic scan zone selection:

            >>> org = sc.organization.create('Sample Organization')

            Creating a new organization with custom analysis links:

            >>> org = sc.organization.create(
            ...     'Sample Organization',
            ...     info_links=[
            ...         ('SANS', 'https://isc.sans.edu/ipinfo.html?ip=%IP%')
            ... ])
        '''
        kwargs['name'] = name
        kwargs['zone_selection'] = kwargs.get('zone_selection', 'auto_only')
        kwargs = self._constructor(**kwargs)
        return self._api.post('organization', json=kwargs).json()['response']

    def list(self, fields=None):
        # noqa: E501
        '''
        Retrieves a list of organizations.

        :sc-api:`SC organization List <Organization.htm#OrganizationRESTReference-/organization>`

        Args:
            fields (list, optional):
                The list of fields that are desired to be returned.  For
                details on what fields are available, please refer to the
                details on the request within the organization list API doc.

        Returns:
            :obj:`list`:
                List of organization definitions.

        Examples:

            Retrieve all of all of the organizations:

            >>> repos = sc.organizations.list()
        '''
        params = dict()
        if fields:
            params['fields'] = ','.join([self._check('field', f, str)
                                         for f in fields])
        return self._api.get('organization', params=params).json()['response']

    def details(self, organization_id, fields=None):
        # noqa: E501
        '''
        Retrieves the details for the specified organization.
        
        :sc-api:`SC Organization Details <Organization.htm#organization_uuid_GET>`

        Args:
            organization_id (int): The numeric id of the organization.
            fields (list, optional):
                The list of fields that are desired to be returned. For details
                on what fields are available, please refer to the details on
                the request within the organization details API doc.

        Returns:
            :obj:`dict`:
                The organization resource record.

        Examples:

            >>> org = sc.organization.details(1)
        '''
        params = dict()
        if fields:
            params['fields'] = ','.join(
                [self._check('field', f, str) for f in fields]
            )

        return self._api.get('organization/{}'.format(
            self._check('organization_id', organization_id, int)),
            params=params).json()['response']

    def edit(self, organization_id, **kwargs):
        # noqa: E501
        '''
        Updates an existing organization

        :sc-api:`SC Organization Edit <Organization.htm#organization_uuid_PATCH>`

        Args:
            organization_id: The numeric id of the organization.
            info_links (list, optional):
                A list of custom analysis links provided to users within the
                host vulnerability details when analyzing data outside of
                SecurityCenter is desired.
            lce_ids (list, optional):
                What Log Correlation Engines (if any) should this organization
                be allowed to access?  If left unspecified no LCE engined will
                be granted to this organization.
            ldap_ids (list, optional):
                What ldap server configuration ids should be used with this
                organization?
            name (str, optional): The name for organization.
            nessus_managers (list, optional):
                Nessus Manager scanner for Nessus Agent scan imports.
            pub_sites (list, optional):
                A list of publishing site ids to associate this organization.
            repos (list, optional):
                A list of Repository ids to associate to this organization.
            restricted_ips (list, optional):
                A list of IP addresses, CIDRs, and/or IP ranges that should
                never be scanned.
            vuln_score_low (int):
                The vulnerability weighting to apply to low criticality
                vulnerabilities for scoring purposes. (Default: 1)
            vuln_score_medium (int):
                The vulnerability weighting to apply to medium criticality
                vulnerabilities for scoring purposes. (Default: 3)
            vuln_score_high (int):
                The vulnerability weighting to apply to high criticality
                vulnerabilities for scoring purposes. (Default: 10)
            vuln_score_critical (int):
                The vulnerability weighting to apply to critical criticality
                vulnerabilities for scoring purposes.(Default: 40)
            zone_selection (str):
                What type of scan zone selection should be performed?
                Available selection types are as follows: ``auto_only``,
                ``locked``, ``selectable+auto``, ``selectable+auto_restricted``.
                If left unspecified, the default is ``auto_only``.
            zones (list, optional):
                When ``zone_selection`` is not ``auto_only``, this field
                must be filled with list of ids from available scan zone(s).

        Returns:
            dict: The updated organization resource record.

        Examples:

            >>> sc.organization.edit(1, name='New Name')
        '''
        kwargs = self._constructor(**kwargs)
        return self._api.patch('organization/{}'.format(
            self._check('organization_id', organization_id, int)), json=kwargs).json()['response']

    def delete(self, organization_id):
        # noqa: E501
        '''
        Remove the specified organization from Tenable Security Center

        :sc-api:`SC organization Delete <Organization.htm#organization_uuid_DELETE>`

        Args:
            organization_id (int): The numeric id of the organization to delete.

        Returns:
            :obj:`str`:
                Empty response string

        Examples:

            >>> sc.organization.delete(1)
        '''
        return self._api.delete('organization/{}'.format(
            self._check('organization_id', organization_id, int))
        ).json()['response']

    def accept_risk_rules(self,
                          organization_id,
                          repos=None,
                          plugin=None,
                          port=None
                          ):
        # noqa: E501
        '''
        Retrieves the accepted risk rules for the organization and optionally
        will filter based on the parameters specified.

        :sc-api:`organization: accept-risk-rule
        <Organization.htm#organization_uuid_acceptRiskRule_GET>`

        Args:
            organization_id (int): The organization id.
            repos (list, optional):
                A list of repository ids to restrict the search to.
            plugin (int, optional):
                A plugin id to restrict the search to.
            port (int, optional):
                A port number to restrict the search to.

        Returns:
            :obj:`list`:
                A list of rules that match the request.

        Examples:

            >>> for rule in sc.organizations.accept_risk_rules(1):
            ...     pprint(rule)
        '''
        params = dict()
        if repos:
            params['repositoryIDs'] = ','.join([self._check('repo:id', i, int)
                                                for i in self._check('repos', repos, list)])
        if plugin:
            params['pluginID'] = self._check('plugin', plugin, int)
        if port:
            params['port'] = self._check('port', port, int)
        return self._api.get('organization/{}/acceptRiskRule'.format(
            self._check('organization_id', organization_id, int)), params=params).json()['response']

    def recast_risk_rules(self, organization_id, repos=None, plugin=None, port=None):
        # noqa: E501
        '''
        Retrieves the recasted risk rules for the organization and optionally
        will filter based on the parameters specified.

        :sc-api:`organization: recast-risk-rule
        <Organization.htm#organization_uuid_recastRiskRule_GET>`

        Args:
            organization_id (int): The organization id.
            repos (list, optional):
                A list of repository ids to restrict the search to.
            plugin (int, optional):
                A plugin id to restrict the search to.
            port (int, optional):
                A port number to restrict the search to.

        Returns:
            :obj:`list`:
                A list of rules that match the request.

        Examples:

            >>> for rule in sc.organizations.recast_risk_rules(1):
            ...     pprint(rule)
        '''
        params = dict()
        if repos:
            params['repositoryIDs'] = ','.join([self._check('repo:id', i, int)
                                                for i in self._check('repos', repos, list)])
        if plugin:
            params['pluginID'] = self._check('plugin', plugin, int)
        if port:
            params['port'] = self._check('port', port, int)
        return self._api.get('organization/{}/recastRiskRule'.format(
            self._check('organization_id', organization_id, int)), params=params).json()['response']

    def managers_list(self, org_id, fields=None):
        # noqa: E501,PLC0301
        '''
        Retrieves a list of security managers.

        :sc-api:`organization-security-manager: list <Organization-Security-Manager.htm#OrganizationSecurityManagerRESTReference-/organization/{orgID}/securityManager>`

        Args:
            org_id: (int):
                The numeric identifier for the organization.
            fields (list, optional):
                The list of fields that are desired to be returned.  For details
                on what fields are available, please refer to the details on the
                request within the organization list API doc.

        Returns:
            :obj:`list`:
                List of user definitions.

        Examples:

            Retrieve all of the security managers for a given org.:
            >>> repos = sc.organizations.managers_list()
        '''
        params = dict()
        if fields:
            params['fields'] = ','.join([self._check('field', f, str)
                                         for f in fields])
        return self._api.get('organization/{}/securityManager'.format(
            self._check('org_id', org_id, int)), params=params).json()['response']

    def manager_create(self, org_id, username, password, role, **kwargs):
        # noqa: E501,PLC0301
        '''
        Creates a new security manager for the given org.  For a complete list
        of parameters that are supported for this call, please refer to
        :py:meth:`tio.users.create() <UserAPI.create>` for more details.

        :sc-api:`organization-security-manager: create <Organization-Security-Manager.htm#organization_orgUUID_securityManager_POST>`

        Args:
            org_id: (int):
                The numeric identifier for the organization.
            username (str):
                The username for the account
            password (str):
                The password for the user to create
            role (int):
                The role that should be assigned to this user.
            **kwargs (dict):
                The keyword args to pass to the user constructor.

        Returns:
            :obj:`dict`:
                The newly created security manager.

        Examples:

            >>> secmngr = sc.organizations.manager_create(1,
            ...     'username', 'password', 1)
        '''
        kwargs['username'] = username
        kwargs['password'] = password
        kwargs['role'] = role
        kwargs['auth_type'] = kwargs.get('auth_type', 'tns')
        kwargs['responsibleAssetID'] = -1
        payload = self._api.users._constructor(**kwargs)
        return self._api.post('organization/{}/securityManager'.format(
            self._check('org_id', org_id, int)), json=payload).json()['response']

    def manager_details(self, org_id, user_id, fields=None):
        # noqa: E501,PLC0301
        '''
        Retrieves the details of a specified security manager within a
        specified organization.

        :sc-api:`organization-security-manager: details <Organization-Security-Manager.htm#OrganizationSecurityManagerRESTReference-/organization/{orgID}/securityManager/{id}>`

        Args:
            org_id: (int):
                The numeric identifier for the organization.
            user_id: (int):
                The numeric identifier for the user.
            fields (list, optional):
                The list of fields that are desired to be returned.  For details
                on what fields are available, please refer to the details on the
                request within the organization list API doc.

        Returns:
            :obj:`dict`:
                The user resource record.

        Examples:

            >>> secmngr = sc.organizations.manager_details(1, 1)
        '''
        params = dict()
        if fields:
            params['fields'] = ','.join([self._check('field', f, str)
                                         for f in fields])
        return self._api.get('organization/{}/securityManager/{}'.format(
            self._check('org_id', org_id, int),
            self._check('user_id', user_id, int)),
            params=params).json()['response']

    def manager_edit(self, org_id, user_id, **kwargs):
        # noqa: E501,PLC0301
        '''
        Edits the specified security manager within the specified organization.
        For details on the supported arguments that may be passed, please refer
        to :py:meth:`tio.users.edit() <UserAPI.edit>` for more details.

        :sc-api:`organization-security-manager: edit <Organization-Security-Manager.htm#organization_orgUUID_securityManager_uuid_PATCH>`

        Args:
            org_id: (int):
                The numeric identifier for the organization.
            user_id: (int):
                The numeric identifier for the user.
            **kwargs (dict):
                The keyword args to pass to the user constructor.

        Returns:
            :obj:`dict`:
                The updated user record.

        Examples:

            >>> secmngr = sc.organizations.manager_edit(1, 1,
            ...     username='updated')
        '''
        payload = self._api.users._constructor(**kwargs)
        return self._api.patch('organization/{}/securityManager/{}'.format(
            self._check('org_id', org_id, int),
            self._check('user_id', user_id, int)
        ), json=payload).json()['response']

    def manager_delete(self, org_id, user_id, migrate_to=None):
        # noqa: E501,PLC0301
        '''
        Removes the user specified.

        :sc-api:`organization-security-manager: delete <Organization-Security-Manager.htm#organization_uuid_DELETE>`

        Args:
            org_id: (int):
                The numeric identifier for the organization.
            user_id: (int):
                The numeric identifier for the user.

        Examples:

            >>> sc.organizations.manager_delete(1, 1)
        '''
        payload = dict()
        if migrate_to:
            payload['migrateUserID'] = self._check('migrate_to', migrate_to, int)

        self._api.delete('organization/{}/securityManager/{}'.format(
            self._check('org_id', org_id, int),
            self._check('user_id', user_id, int)
        ), json=payload)
