'''
roles
=====

The following methods allow for interaction into the Tenable.sc
:sc-api:`Roles <Role.html>` API.  These items are typically seen under the
**User Roles** section of Tenable.sc.

Methods available on ``sc.roles``:

.. rst-class:: hide-signature
.. autoclass:: RoleAPI

    .. automethod:: create
    .. automethod:: delete
    .. automethod:: details
    .. automethod:: edit
    .. automethod:: list
'''
from .base import SCEndpoint

class RoleAPI(SCEndpoint):
    def _constructor(self, **kw):
        '''
        Handles parsing the keywords and returns a role definition document
        '''
        if 'name' in kw:
            # Validate that the name parameter is a string.
            self._check('name', kw['name'], str)

        if 'description' in kw:
            # Validate that the description parameter is a string.
            self._check('description', kw['description'], str)

        # Snake-cased boolean role mapping to the API attributes.
        mapping = {
            'manage_groups': 'permManageGroups',
            'manage_roles': 'permManageRoles',
            'manage_images': 'permManageImages',
            'manage_relationships': 'permManageGroupRelationships',
            'manage_blackout_windows': 'permManageBlackoutWindows',
            'manage_attributes': 'permManageAttributeSets',
            'create_tickets': 'permCreateTickets',
            'create_alerts': 'permCreateAlerts',
            'create_auditfiles': 'permCreateAuditFiles',
            'create_ldap_assets': 'permCreateLDAPAssets',
            'create_policies': 'permCreatePolicies',
            'purge_tickets': 'permPurgeTickets',
            'purge_scans': 'permPurgeScanResults',
            'purge_reports': 'permPurgeReportResults',
            'can_scan': 'permScan',
            'can_agent_scan': 'permAgentsScan',
            'can_share': 'permShareObjects',
            'can_feed_update': 'permUpdateFeeds',
            'can_import_scan': 'permUploadNessusResults',
            'can_view_logs': 'permViewOrgLogs',
            'manage_accepted_risk_rules': 'permManageAcceptRiskRules',
            'manage_recast_risk_rules': 'permManageRecastRiskRules',
        }

        # iterate through the keys, converting the boolean values to the
        # lowercased strings values that the API expects to see.
        for key in mapping.keys():
            if key in kw:
                kw[mapping[key]] = str(self._check(key, kw[key], bool)).lower()
                del(kw[key])

        return kw

    def create(self, name, **kw):
        '''
        Creates a role.

        :sc-api:`role: create <Role.html#role_POST>`

        Args:
            name (str): The name of the new role to create.
            descrioption (str, optional):
                A description for the role to be created.
            can_agent_scan (bool, optional):
                Are members of this role allowed to perform agent scans? If left
                unspecified the default is ``False``.
            can_feed_update (bool, optional):
                Are members of this role allowed to perform feed updates? If
                left unspecified, the default is ``False``.
            can_import_scan (bool, optional):
                Are members of this role allowed to import scans?  If left
                unspecified, the default is ``False``.
            can_scan (bool, optional):
                Are members of this role allowed to perform scans?  If left
                unspecified, the default is ``False``.
            can_share (bool, optional):
                Are members of this role allowed to share objects with other
                groups?  If left unspecified, the default is ``False``.
            can_view_logs (bool, optional):
                Are members of this role allowed to view the organizational
                logs from Tenable.sc?  If left unspecified, the default is
                ``False``.
            create_alerts (bool, optional):
                Are members of this role allowed to create alerts? If left
                unspecified, the default is ``False``.
            create_auditfiles (bool, optional):
                Are members of this role allowed to create their own audit
                files?  If left unspecified, the default is ``False``.
            create_ldap_assets (bool, optional):
                Are members of this role allowed to create LDAP Query Asset
                Lists?  If left unspecified, the default is ``False``.
            create_policies (bool, optional):
                Are members of this role allowed to create scan policies?
                If left unspecified, the default is ``False``.
            create_tickets (bool, optional):
                Are members of this role allowed to create tickets?  If left
                unspecified, the default is ``False``.
            manage_accepted_risk_rules (bool, optional):
                Are members of this role allowed to manage accepted risk rules?
                If left unspecified, the default is ``False``.
            manage_attributes (bool, optional):
                Are members of this role allowed to manage attribute sets?
                If left unspecified, the default is ``False``.
            manage_blackout_windows (bool, optional):
                Are members of this role allowed to manage scanning blackout
                windows?  If left unspecified, the default is ``False``.
            manage_groups (bool, optional):
                Are members of this role allowed to manage user groups?
                If left unspecified, the default is ``False``.
            manage_images (bool, optional):
                Are members of this role allowed to manage report images?
                If left unspecified, the default is ``False``.
            manage_recast_risk_rules (bool, optional):
                Are members of this role allowed to manage recast risk rules?
                If left unspecified, the default is ``False``.
            manage_relationships (bool, optional):
                Are members of this role allowed to manage the user group
                relationships?  If left unspecified, the default is ``False``.
            manage_roles (bool, optional):
                Are members of this role allowed to manage group role
                configurations?  If left unspecified, the default is ``False``.

        Returns:
            :obj:`dict`:
                The newly created role.

        Examples:
            >>> role = sc.roles.create('Example Role',
            ...     can_scan=True, can_import_scan=True)
        '''
        kw['name'] = name
        payload = self._constructor(**kw)
        return self._api.post('role', json=payload).json()['response']

    def details(self, id, fields=None):
        '''
        Returns the details for a specific role.

        :sc-api:`role: details <Role.html#role_id_GET>`

        Args:
            id (int): The identifier for the role.
            fields (list, optional): A list of attributes to return.

        Returns:
            :obj:`dict`:
                The role resource record.

        Examples:
            >>> role = sc.roles.details(1)
            >>> pprint(role)
        '''
        params = dict()
        if fields:
            params['fields'] = ','.join([self._check('field', f, str) for f in fields])

        return self._api.get('role/{}'.format(self._check('id', id, int)),
            params=params).json()['response']

    def edit(self, id, **kw):
        '''
        Edits a role.

        :sc-api:`role: edit <Role.html#role_id_PATCH>`

        Args:
            id (int): The numeric identifier for the role.
            name (str, optional):
                The name of the new role to create.
            description (str, optional):
                A description for the role to be created.
            can_agent_scan (bool, optional):
                Are members of this role allowed to perform agent scans? If left
                unspecified the default is ``False``.
            can_feed_update (bool, optional):
                Are members of this role allowed to perform feed updates? If
                left unspecified, the default is ``False``.
            can_import_scan (bool, optional):
                Are members of this role allowed to import scans?  If left
                unspecified, the default is ``False``.
            can_scan (bool, optional):
                Are members of this role allowed to perform scans?  If left
                unspecified, the default is ``False``.
            can_share (bool, optional):
                Are members of this role allowed to share objects with other
                groups?  If left unspecified, the default is ``False``.
            can_view_logs (bool, optional):
                Are members of this role allowed to view the organizational
                logs from Tenable.sc?  If left unspecified, the default is
                ``False``.
            create_alerts (bool, optional):
                Are members of this role allowed to create alerts? If left
                unspecified, the default is ``False``.
            create_auditfiles (bool, optional):
                Are members of this role allowed to create their own audit
                files?  If left unspecified, the default is ``False``.
            create_ldap_assets (bool, optional):
                Are members of this role allowed to create LDAP Query Asset
                Lists?  If left unspecified, the default is ``False``.
            create_policies (bool, optional):
                Are members of this role allowed to create scan policies?
                If left unspecified, the default is ``False``.
            create_tickets (bool, optional):
                Are members of this role allowed to create tickets?  If left
                unspecified, the default is ``False``.
            manage_accepted_risk_rules (bool, optional):
                Are members of this role allowed to manage accepted risk rules?
                If left unspecified, the default is ``False``.
            manage_attributes (bool, optional):
                Are members of this role allowed to manage attribute sets?
                If left unspecified, the default is ``False``.
            manage_blackout_windows (bool, optional):
                Are members of this role allowed to manage scanning blackout
                windows?  If left unspecified, the default is ``False``.
            manage_groups (bool, optional):
                Are members of this role allowed to manage user groups?
                If left unspecified, the default is ``False``.
            manage_images (bool, optional):
                Are members of this role allowed to manage report images?
                If left unspecified, the default is ``False``.
            manage_recast_risk_rules (bool, optional):
                Are members of this role allowed to manage recast risk rules?
                If left unspecified, the default is ``False``.
            manage_relationships (bool, optional):
                Are members of this role allowed to manage the user group
                relationships?  If left unspecified, the default is ``False``.
            manage_roles (bool, optional):
                Are members of this role allowed to manage group role
                configurations?  If left unspecified, the default is ``False``.

        Returns:
            :obj:`dict`:
                The newly updated role.

        Examples:
            >>> role = sc.roles.create()
        '''
        payload = self._constructor(**kw)
        return self._api.patch('role/{}'.format(
            self._check('id', id, int)), json=payload).json()['response']

    def delete(self, id):
        '''
        Removes a role.

        :sc-api:`role: delete <Role.html#role_id_DELETE>`

        Args:
            id (int): The numeric identifier for the role to remove.

        Returns:
            :obj:`str`:
                An empty response.

        Examples:
            >>> sc.roles.delete(1)
        '''
        return self._api.delete('role/{}'.format(
            self._check('id', id, int))).json()['response']


    def list(self, fields=None):
        '''
        Retrieves the list of role definitions.

        :sc-api:`role: list <Role.html#role_GET>`

        Args:
            fields (list, optional):
                A list of attributes to return for each role.

        Returns:
            :obj:`list`:
                A list of role resources.

        Examples:
            >>> for role in sc.roles.list():
            ...     pprint(role)
        '''
        params = dict()
        if fields:
            params['fields'] = ','.join([self._check('field', f, str)
                for f in fields])

        return self._api.get('role', params=params).json()['response']
