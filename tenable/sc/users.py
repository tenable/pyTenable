'''
users
=====

The following methods allow for interaction into the Tenable.sc
:sc-api:`User <User.html>` API.  These items are typically seen under the
**Users** section of Tenable.sc.

Methods available on ``sc.users``:

.. rst-class:: hide-signature
.. autoclass:: UserAPI

    .. automethod:: create
    .. automethod:: delete
    .. automethod:: details
    .. automethod:: edit
    .. automethod:: list
'''
from .base import SCEndpoint

class UserAPI(SCEndpoint):
    def _constructor(self, **kw):
        '''
        Handles parsing the keywords and returns a user definition document
        '''
        if 'role' in kw:
            # Validate role as int and pass to roleID
            kw['roleID'] = self._check('role', kw['role'], int)
            del(kw['role'])

        if 'group' in kw:
            # Validate group asd int and pass to groupID
            kw['groupID'] = self._check('group', kw['group'], int)
            del(kw['group'])

        if 'org' in kw:
            # Validate org as int and pass to orgID
            kw['orgID'] = self._check('org', kw['org'], int)
            del(kw['org'])

        if 'responsibility' in kw:
            # Validate responsibility as an int and pass to responsibleAssetID
            kw['responsibleAssetID'] = self._check(
                'responsibility', kw['responsibility'], int)
            del(kw['responsibility'])

        # all of the following keys are string values and do not require any
        # case conversion.  We will simply iterate through them and verify that
        # they are in-fact strings.
        keys = [
            'ldapUsername', 'username', 'firstname', 'lastname', 'title',
            'email', 'address', 'city', 'state', 'country', 'phone', 'fax',
            'fingerprint', 'status'
        ]
        for k in keys:
            if k in kw:
                self._check(k, kw[k], str)

        if 'is_locked' in kw:
            # Convert the is_locked keyword from a boolean value into a string
            # interpretation of that value.
            kw['locked'] = str(self._check(
                'is_locked', kw['is_locked'], bool)).lower()
            del(kw['is_locked'])

        if 'auth_type' in kw:
            # Verify that auth_type is one of the correct possible values and
            # store it within the camelCased version of the parameter.
            kw['authType'] = self._check('auth_type', kw['auth_type'], str,
                choices=['ldap', 'legacy', 'saml', 'tns'])
            del(kw['auth_type'])

        if 'email_notice' in kw:
            # Verify that email_notice is one of the correct possible values and
            # store it within the camelCased version of the parameter.
            kw['emailNotice'] = self._check(
                'email_notice', kw['email_notice'], str, choices=[
                    'both', 'id', 'none', 'password'])
            del(kw['email_notice'])

        if 'timezone' in kw:
            # Convert the timezone parameter into the preference dictionary
            # item thats expected by the API.
            kw['preferences'] = [{
                'name': 'timezone',
                'tag': 'system',
                'value': self._check('timezone', kw['timezone'], str)
            }]
            del(kw['timezone'])

        if 'update_password' in kw:
            # Convert the update_password keyword from a boolean value into a
            # string interpretation of that value.
            kw['mustChangePassword'] = str(self._check(
                'update_password', kw['update_password'], bool)).lower()
            del(kw['update_password'])

        if 'managed_usergroups' in kw:
            # Convert the managed_groups list into a listing of dictionaries
            # with an id parameter.
            kw['managedUsersGroups'] = [{'id': self._check('group:id', i, int)}
                for i in self._check(
                    'managed_usergroups', kw['managed_usergroups'], list)]
            del(kw['managed_usergroups'])

        if 'managed_userobjs' in kw:
            # Convert the managed_groups list into a listing of dictionaries
            # with an id parameter.
            kw['managedObjectsGroups'] = [{'id': self._check('group:id', i, int)}
                for i in self._check(
                    'managed_userobjs', kw['managed_userobjs'], list)]
            del(kw['managed_userobjs'])

        if 'default_reports' in kw:
            # Should the default user reports be built as part of the user
            # creation?
            kw['importReports'] = str(self._check(
                'default_reports', kw['default_reports'], bool)).lower()
            del(kw['default_reports'])

        if 'default_dashboards' in kw:
            # Should the default user dashboards be built as part of the user
            # creation?
            kw['importDashboards'] = str(self._check(
                'default_dashboards', kw['default_dashboards'], bool)).lower()
            del(kw['default_dashboards'])

        if 'default_reportcards' in kw:
            # Should the default user dashboards be built as part of the user
            # creation?
            kw['importARCs'] = str(self._check(
                'default_reportcards', kw['default_reportcards'], bool)).lower()
            del(kw['default_reportcards'])

        if 'ldap_id' in kw:
            # Convert the ldap_id attribute to a subdocument of "ldap"
            kw['ldap'] = {'id': self._check('ldap_id', kw['ldap_id'], int)}
            del(kw['ldap_id'])

        return kw

    def create(self, username, password, role, **kw):
        '''
        Creates a user.

        :sc-api:`user: create <User.html#user_POST>`

        Args:
            username (str):
                The username for the account
            password (str):
                The password for the user to create
            role (int):
                The role that should be assigned to this user.
            address (str, optional):
                Optional street address information to associate to the user.
            auth_type (str, optional):
                The Authentication type to use for the user.  Valid options are
                ``ldap``, ``legacy``, ``saml``, and ``tns``.  If left unspecified
                the default is ``tns``.
            city (str, optional):
                Optional city information to associate to the user.
            country (str, optional):
                Optional country information to associate to the user.
            default_dashboards (bool, optional):
                Should the default dashboards be created for the user?  If left
                unspecified, the default is True.
            default_reportcards (bool, optional):
                Should the default report cards be created for the user?  If
                left unspecified, the default is True.
            default_reports (bool, optional):
                Should the default reports be created fro the user?  If left
                unspecified, the default is True.
            email (str, optional):
                The email address to associate to the user.
            email_notice (str, optional):
                What type of events should generate an email notification?
                Valid types are ``id``, ``password``, ``both``, ``none``.
            fax (str, optional):
                A fax number to associate to the user.
            fingerprint (str, optional):
                A fingerprint to associate to the user.
            firstname (str, optional):
                A first name to associate to the user.
            group (int, optional):
                A group to associate to the user.  This parameter is required
                for users that are not Administrators.
            is_locked (bool, optional):
                If the account locked?  If left unspecified the default is False.
            ldap_id (int, optional):
                If specifying an LDAP auth type, this is the numeric identifier
                for the LDAP configuration to use.
            managed_usergroups (list, optional):
                A list of group ids that the user is allowed to manage users
                within.
            managed_userobjs (list, optional):
                A list of group ids that the user is allowed to manage objects
                within.  This includes asset lists, reports, etc.
            org (int, optional):
                If logged in as an administrator, and creating a security
                manager account, the organization id must be passed in order to
                inform Tenable.sc which organization to create the security
                manager within.
            phone (str, optional):
                A phone number to associate to the user.
            responsibility (int, optional):
                The asset list detailing what assets the user is responsible
                for.  A value of ``0`` denotes all assets, any other non-zero
                integer must be the id of the asset list to associate to the
                user.
            state (str, optional):
                The state to associate to the user.
            timezone (str, optional):
                A timezone other than the system timezone to associate to the
                user.  This will impact all times displayed within the user
                interface.
            title (str, optional):
                A title to associate to the user.
            update_password (bool, optional):
                Should the user be forced to update their password next login?
                If left unspecified, the default is False.

        Returns:
            :obj:`dict`:
                The newly created user.

        Examples:
            >>> user = sc.users.create('username', 'password', 1, group=1)
        '''
        kw['username'] = username
        kw['password'] = password
        kw['role'] = role
        kw['auth_type'] = kw.get('auth_type', 'tns')
        kw['responsibleAssetID'] = -1
        payload = self._constructor(**kw)
        return self._api.post('user', json=payload).json()['response']

    def details(self, id, fields=None):
        '''
        Returns the details for a specific user.

        :sc-api:`user: details <User.html#UserRESTReference-/user/{id}>`

        Args:
            id (int): The identifier for the user.
            fields (list, optional): A list of attributes to return.

        Returns:
            :obj:`dict`:
                The user resource record.

        Examples:
            >>> user = sc.users.details(1)
            >>> pprint(user)
        '''
        params = dict()
        if fields:
            params['fields'] = ','.join([self._check('field', f, str) for f in fields])

        return self._api.get('user/{}'.format(self._check('id', id, int)),
            params=params).json()['response']

    def edit(self, id, **kw):
        '''
        Edits a user.

        :sc-api:`user: edit <User.html#user_id_PATCH>`

        Args:
            address (str, optional):
                Optional street address information to associate to the user.
            auth_type (str, optional):
                The Authentication type to use for the user.  Valid options are
                ``ldap``, ``legacy``, ``saml``, and ``tns``.  If left unspecified
                the default is ``tns``.
            city (str, optional):
                Optional city information to associate to the user.
            country (str, optional):
                Optional country information to associate to the user.
            default_dashboards (bool, optional):
                Should the default dashboards be created for the user?  If left
                unspecified, the default is True.
            default_reportcards (bool, optional):
                Should the default report cards be created for the user?  If
                left unspecified, the default is True.
            default_reports (bool, optional):
                Should the default reports be created fro the user?  If left
                unspecified, the default is True.
            email (str, optional):
                The email address to associate to the user.
            email_notice (str, optional):
                What type of events should generate an email notification?
                Valid types are ``id``, ``password``, ``both``, ``none``.
            fax (str, optional):
                A fax number to associate to the user.
            fingerprint (str, optional):
                A fingerprint to associate to the user.
            firstname (str, optional):
                A first name to associate to the user.
            group (int, optional):
                A group to associate to the user.  This parameter is required
                for users that are not Administrators.
            is_locked (bool, optional):
                If the account locked?  If left unspecified the default is False.
            ldap_id (int, optional):
                If specifying an LDAP auth type, this is the numeric identifier
                for the LDAP configuration to use.
            managed_usergroups (list, optional):
                A list of group ids that the user is allowed to manage users
                within.
            managed_userobjs (list, optional):
                A list of group ids that the user is allowed to manage objects
                within.  This includes asset lists, reports, etc.
            org (int, optional):
                If logged in as an administrator, and creating a security
                manager account, the organization id must be passed in order to
                inform Tenable.sc which organization to create the security
                manager within.
            password (str, optional):
                The user password
            phone (str, optional):
                A phone number to associate to the user.
            responsibility (int, optional):
                The asset list detailing what assets the user is responsible
                for.  A value of ``0`` denotes all assets, any other non-zero
                integer must be the id of the asset list to associate to the
                user.
            role (int, optional):
                The role that should be assigned to this user.
            state (str, optional):
                The state to associate to the user.
            timezone (str, optional):
                A timezone other than the system timezone to associate to the
                user.  This will impact all times displayed within the user
                interface.
            title (str, optional):
                A title to associate to the user.
            update_password (bool, optional):
                Should the user be forced to update their password next login?
                If left unspecified, the default is False.
            username (str, optional):
                The username for the account

        Returns:
            :obj:`dict`:
                The newly updated user.

        Examples:
            >>> user = sc.users.edit(1, username='newusername')
        '''
        payload = self._constructor(**kw)
        return self._api.patch('user/{}'.format(
            self._check('id', id, int)), json=payload).json()['response']

    def delete(self, id):
        '''
        Removes a user.

        :sc-api:`user: delete <User.html#user_id_DELETE>`

        Args:
            id (int): The numeric identifier for the user to remove.

        Returns:
            :obj:`str`:
                An empty response.

        Examples:
            >>> sc.users.delete(1)
        '''
        return self._api.delete('user/{}'.format(
            self._check('id', id, int))).json()['response']

    def list(self, fields=None):
        '''
        Retrieves the list of scan zone definitions.

        :sc-api:`user: list <User.html#user_GET>`

        Args:
            fields (list, optional):
                A list of attributes to return for each user.

        Returns:
            :obj:`list`:
                A list of user resources.

        Examples:
            >>> for user in sc.users.list():
            ...     pprint(user)
        '''
        params = dict()
        if fields:
            params['fields'] = ','.join([self._check('field', f, str)
                for f in fields])

        return self._api.get('user', params=params).json()['response']
