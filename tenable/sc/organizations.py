'''
organization
============

The following methods allow for interaction with the Tenable.sc
:sc-api:`Organization <Organization.html>` API. These items are typically seen
under the **Organization** section of Tenable.sc.

Methods available on ``sc.organizations``:

.. rst-class:: hide-signature
.. autoclass:: OrganizationAPI

    .. automethod:: create
    .. automethod:: list
    .. automethod:: details
    .. automethod:: edit
    .. automethod:: delete
    .. automethod:: accept_risk_rules
    .. automethod:: recast_risk_rules
    .. automethod:: manager_create
    .. automethod:: manager_delete
    .. automethod:: manager_details
    .. automethod:: manager_edit
    .. automethod:: managers_list
'''
from tenable.sc.base import SCEndpoint


class OrganizationAPI(SCEndpoint):
    def _constructor(self, **kw):
        '''
        Organization document constructor
        '''
        if 'name' in kw:
            # Validate the the name attribute is a string value
            self._check('name', kw['name'], str)

        if 'description' in kw:
            # validate that the description is a string value
            self._check('description', kw['description'], str)

        if 'address' in kw:
            # validate that the address field is a string value
            self._check('address', kw['address'], str)

        if 'city' in kw:
            # validate that the city is a string value
            self._check('city', kw['city'], str)

        if 'state' in kw:
            # validate that the state is a string value
            self._check('state', kw['state'], str)

        if 'country' in kw:
            # validate that the country is a streing value.
            self._check('country', kw['country'], str)

        if 'phone' in kw:
            # validate that the phone is a string value.
            self._check('phone', kw['phone'], str)

        if 'lce_ids' in kw:
            # validate that the lce_ids is a list of integers and transform them
            # into a list of dictionaries with id attributes.
            kw['lces'] = [{'id': self._check('lce:id', i, int)}
                for i in self._check('lce_ids', kw['lce_ids'], list)]
            del(kw['lce_ids'])

        if 'zone_selection' in kw:
            # validate that zone_selection is a string value of one of the
            # expected types and store it in the camelCase equiv.
            kw['zoneSelection'] = self._check('zone_selection',
                kw['zone_selection'], str, choices=[
                    'auto_only', 'locked', 'selectable', 'selectable+auto',
                    'selectable+auto_restricted'])
            del(kw['zone_selection'])

        if 'restricted_ips' in kw:
            # ensure that restricted_ips is a list of items and return it as a
            # comma-seperated string in the camelCase variant of the param.
            kw['restrictedIPs'] = ','.join(self._check(
                'restricted_ips', kw['restricted_ips'], list))
            del(kw['restricted_ips'])

        if 'repos' in kw:
            # convert the list of numeric ids for repos into a list of
            # dictionaries with the id attribute.
            kw['repositories'] = [{'id': self._check('repo:id', r, int)}
                for r in self._check('repos', kw['repos'], list)]
            del(kw['repos'])

        if 'pub_sites' in kw:
            # convert the list of numeric ids for pub_sites into a list of
            # dictionaries with the id attribute.
            kw["pubSites"] = [{'id': self._check('site:id', p, int)}
                for p in self._check('pub_sites', kw['pub_sites'], list)]
            del(kw["pub_sites"])

        if 'ldap_ids' in kw:
            # convert the list of numeric ids for ldap_ids into a list of
            # dictionaries with the id attribute.
            kw['ldaps'] = [{'id': self._check('ldap:id', p, int)}
                for p in self._check('ldap_ids', kw['ldap_ids'], list)]
            del(kw['ldap_ids'])

        if 'nessus_managers' in kw:
            # convert the list of numeric ids for nessus managers into a list of
            # dictionaries with the id attribute.
            kw['nessusManagers'] = [{'id': self._check('nessus_manager:id', n, int)}
                for n in self._check('nessus_managers', kw['nessus_managers'], list)]
            del(kw['nessus_managers'])

        if 'info_links' in kw:
            # convert the info_links
            kw['ipInfoLinks'] = [{
                    'name': self._check('link:name', i[0], str),
                    'link': self._check('link:link', i[1], str)}
                for i in self._check('info_links', kw['info_links'], list)]
            del(kw['info_links'])

        if 'vuln_score_low' in kw:
            kw['vulnScoreLow'] = self._check(
                'vuln_score_low', kw['vuln_score_low'], int)
            del(kw['vuln_score_low'])

        if 'vuln_score_medium' in kw:
            kw['vulnScoreMedium'] = self._check(
                'vuln_score_medium', kw['vuln_score_medium'], int)
            del(kw['vuln_score_medium'])

        if 'vuln_score_high' in kw:
            kw['vulnScoreHigh'] = self._check(
                'vuln_score_high', kw['vuln_score_high'], int)
            del(kw['vuln_score_high'])

        if 'vuln_score_critical' in kw:
            kw['vulnScoreCritical'] = self._check(
                'vuln_score_critical', kw['vuln_score_critical'], int)
            del(kw['vuln_score_critical'])

        return kw

    def create(self, name, **kw):
        '''
        Create a new organization

        :sc-api:`SC Organization Create <Organization.html#organization_POST>`

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
                ``locked``, ``selectable+auto``, ``selectable+auto_restricted``.
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

            >>> org = sc.organization.create(Sample Organization', info_links=[
            ...     ('SANS', 'https://isc.sans.edu/ipinfo.html?ip=%IP%)])
        '''
        kw['name'] = name
        kw['zone_selection'] = kw.get('zone_selection', 'auto_only')
        kw = self._constructor(**kw)
        return self._api.post('organization', json=kw).json()['response']

    def list(self, fields=None):
        '''
        Retrieves a list of organizations.

        :sc-api:`SC organization List <Organization.html#OrganizationRESTReference-/organization>`

        Args:
            fields (list, optional):
                The list of fields that are desired to be returned.  For details
                on what fields are available, please refer to the details on the
                request within the organization list API doc.

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

    def details(self, id, fields=None):
        '''
        Retrieves the details for the specified organization.

        :sc-api:`SC Organization Details <Organization.html#organization_id_GET>`

        Args:
            id (int): The numeric id of the organization.
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
            params['fields'] = ','.join([self._check('field', f, str) for f in fields])

        return self._api.get('organization/{}'.format(
            self._check('id', id, int)), params=params).json()['response']

    def edit(self, id, **kw):
        '''Updates an existing organization

        Edits the Organization associated with {id}, changing only the passed
        in fields.

        :sc-api:`SC Organization Edit <Organization.html#organization_id_PATCH>`

        Args:
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
        kw = self._constructor(**kw)
        return self._api.patch('organization/{}'.format(
            self._check('id', id, int)), json=kw).json()['response']

    def delete(self, id):
        '''
        Remove the specified organization from Tenable.sc

        :sc-api:`SC organization Delete <Organization.html#organization_id_DELETE>`

        Args:
            id (int): The numeric id of the organization to delete.

        Returns:
            :obj:`str`:
                Empty response string

        Examples:
            >>> sc.organization.delete(1)
        '''
        return self._api.delete('organization/{}'.format(
            self._check('id', id, int))).json()['response']

    def accept_risk_rules(self, id, repos=None, plugin=None, port=None):
        '''
        Retrieves the accepted risk rules for the organization and optionally
        will filter based on the paramaters specified.

        :sc-api:`organization: accept-risk-rule <Organization.html#OrganizationRESTReference-/organization/{id}/acceptRiskRule>`

        Args:
            id (int): The organization id.
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
            self._check('id', id, int)), params=params).json()['response']

    def recast_risk_rules(self, id, repos=None, plugin=None, port=None):
        '''
        Retrieves the recasted risk rules for the organization and optionally
        will filter based on the paramaters specified.

        :sc-api:`organization: recast-risk-rule <Organization.html#OrganizationRESTReference-/organization/{id}/recastRiskRule>`

        Args:
            id (int): The organization id.
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
        return self._api.get('organization/{}/acceptRiskRule'.format(
            self._check('id', id, int)), params=params).json()['response']

    def managers_list(self, org_id, fields=None):
        '''
        Retrieves a list of security managers.

        :sc-api:`organization-security-manager: list <Organization-Security-Manager.html#OrganizationSecurityManagerRESTReference-/organization/{orgID}/securityManager>`

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

    def manager_create(self, org_id, username, password, role, **kw):
        '''
        Creates a new security manager for the given org.  For a complete list
        of parameters that are supported for this call, please refer to
        :py:meth:`tio.users.create() <UserAPI.create>` for more details.

        :sc-api:`organization-security-manager: create <Organization-Security-Manager.html#organization_orgID_securityManager_POST>`

        Args:
            org_id: (int):
                The numeric identifier for the organization.
            username (str):
                The username for the account
            password (str):
                The password for the user to create
            role (int):
                The role that should be assigned to this user.
            **kw (dict):
                The keyword args to pass to the user constructor.

        Returns:
            :obj:`dict`:
                The newly created security manager.

        Examples:
            >>> secmngr = sc.organizations.manager_create(1,
            ...     'username', 'password', 1)
        '''
        kw['username'] = username
        kw['password'] = password
        kw['role'] = role
        kw['auth_type'] = kw.get('auth_type', 'tns')
        kw['responsibleAssetID'] = -1
        payload = self._api.users._constructor(**kw)
        return self._api.post('organization/{}/securityManager'.format(
            self._check('org_id', org_id, int)), json=payload).json()['response']

    def manager_details(self, org_id, user_id, fields=None):
        '''
        Retrieves the details of a specified security manager within a
        specified organization.

        :sc-api:`organization-security-manager: details <Organization-Security-Manager.html#OrganizationSecurityManagerRESTReference-/organization/{orgID}/securityManager/{id}>`

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

    def manager_edit(self, org_id, user_id, **kw):
        '''
        Edits the specified security manager within the specified organization.
        For details on the supported arguments that may be passed, please refer
        to :py:meth:`tio.users.edit() <UserAPI.edit>` for more details.

        :sc-api:`organization-security-manager: edit <Organization-Security-Manager.html#organization_orgID_securityManager_id_PATCH>`

        Args:
            org_id: (int):
                The numeric identifier for the organization.
            user_id: (int):
                The numeric identifier for the user.
            **kw (dict):
                The keyword args to pass to the user constructor.

        Returns:
            :obj:`dict`:
                The updated user record.

        Examples:
            >>> secmngr = sc.organizations.manager_edit(1, 1,
            ...     username='updated')
        '''
        payload = self._api.users._constructor(**kw)
        return self._api.get('organization/{}/securityManager/{}'.format(
            self._check('org_id', org_id, int),
            self._check('user_id', user_id, int)
            ), json=payload).json()['response']

    def manager_delete(self, org_id, user_id, migrate_to=None):
        '''
        Removes the user specified.

        :sc-api:`organization-security-manager: delete <Organization-Security-Manager.html#organization_orgID_securityManager_id_DELETE>`

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

        self._api.get('organization/{}/securityManager/{}'.format(
            self._check('org_id', org_id, int),
            self._check('user_id', user_id, int)
            ), json=payload)