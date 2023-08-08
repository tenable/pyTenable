'''
Access Groups v2
================

The following methods allow for interaction into the Tenable Vulnerability Management
:devportal:`access-groups-v2 <v2-access-groups>` API endpoints.

Methods available on ``tio.access_groups_v2``:

.. rst-class:: hide-signature
.. autoclass:: AccessGroupsV2API
    :members:
'''
from restfly.utils import dict_merge
from tenable.errors import UnexpectedValueError
from tenable.io.base import TIOEndpoint, TIOIterator

class AccessGroupsIteratorV2(TIOIterator):
    '''
    The access groups v2 iterator provides a scalable way to work through
    access groups result sets of any size.  The iterator will walk through each
    page of data, returning one record at a time.  If it reaches the end of a
    page of records, then it will request the next page of information and then
    continue to return records from the next page (and the next, and the next)
    until the counter reaches the total number of records that the API has
    reported.

    Attributes:
        count (int): The current number of records that have been returned
        page (list):
            The current page of data being walked through.  pages will be
            cycled through as the iterator requests more information from the
            API.
        page_count (int): The number of record returned from the current page.
        total (int):
            The total number of records that exist for the current request.
    '''
    pass

class AccessGroupsV2API(TIOEndpoint):
    '''
    This will contain all methods related to access group
    '''
    def _list_clean(self, items):
        '''
        Removes duplicate values from list

        Args:
            items (list): list of items

        Returns:
            :obj:`list`:
                Returns list of distinct values
        '''
        return list(set(self._check('items', items, list)))

    def _principal_constructor(self, items):
        '''
        Simple principle tuple expander.  Also supports validating principle
        dictionaries for transparent passthrough.
        '''
        resp = list()
        for item in items:
            self._check('principal', item, (tuple, dict))
            if isinstance(item, tuple):
                data = dict()
                if len(item) == 2:
                    item = item + ([],)
                data['type'] = self._check('principal:type', item[0], str,
                    choices=['user', 'group'])

                try:
                    data['principal_id'] = self._check('principal:id', item[1], 'uuid')
                except UnexpectedValueError:
                    data['principal_name'] = self._check('principal:name', item[1], str)

                data['permissions'] = self._list_clean(
                    [self._check('permission', permission, str,
                        choices=['CAN_VIEW', 'CAN_SCAN'], case='upper')
                    for permission in self._check('permissions', item[2], list)])

                # if permissions are empty, we will assign default value to it
                if not data['permissions']:
                    data['permissions'] = ['CAN_VIEW']

                resp.append(data)
            else:
                self._check('principal:type', item['type'], str,
                    choices=['user', 'group'])
                if 'principal_id' in item:
                    self._check('principal_id', item['principal_id'], 'uuid')
                if 'principal_name' in item:
                    self._check('principal_name', item['principal_name'], str)
                item['permissions'] = self._list_clean([
                    self._check('permission', permission, str,
                        choices=['CAN_VIEW', 'CAN_SCAN'], case='upper')
                    for permission in self._check('permissions', item['permissions']
                    if 'permissions' in item and item['permissions']
                    else None, list, default=['CAN_VIEW'])]
                )

                resp.append(item)

        return resp

    def list(self, *filters, **kw):
        '''
        Get the listing of configured access groups from Tenable Vulnerability Management.

        :devportal:`access-groups-v2: list <v2-access-groups-listt>`

        Args:
            *filters (tuple, optional):
                Filters are tuples in the form of ('NAME', 'OPERATOR', 'VALUE').
                Multiple filters can be used and will filter down the data being
                returned from the API.

                Examples:
                    - ``('distro', 'match', 'win')``
                    - ``('name', 'nmatch', 'home')``

                As the filters may change and sortable fields may change over
                time, it's highly recommended that you look at the output of
                the :py:meth:`tio.filters.access_groups_filters_v2()` endpoint to get more details.
            filter_type (str, optional):
                The filter_type operator determines how the filters are combined
                together.  ``and`` will inform the API that all the filter
                conditions must be met for an access group to be returned,
                whereas ``or`` would mean that if any of the conditions are met,
                the access group record will be returned.
            limit (int, optional):
                The number of records to retrieve.  Default is 50
            offset (int, optional):
                The starting record to retrieve.  Default is 0.
            sort (tuple, optional):
                A tuple of tuples identifying the field and sort order of
                the field.
            wildcard (str, optional):
                A string to pattern match against all available fields returned.
            wildcard_fields (list, optional):
                A list of fields to optionally restrict the wild-card matching
                to.

        Returns:
            :obj:`AccessGroupsIterator`:
                An iterator that handles the page management of the requested
                records.

        Examples:
            Getting the listing of all agents:

            >>> for group in tio.access_groups_v2.list():
            ...     pprint(group)

            Retrieving all of the windows agents:

            >>> for group in tio.access_groups_v2.list(('name', 'eq', 'win')):
            ...     pprint(group)
        '''
        limit = 50
        offset = 0
        pages = None
        query = self._parse_filters(filters,
            self._api.filters.access_group_filters_v2(), rtype='colon')

        # If the offset was set to something other than the default starting
        # point of 0, then we will update offset to reflect that.
        if 'offset' in kw and self._check('offset', kw['offset'], int):
            offset = kw['offset']

        # The limit parameter affects how many records at a time we will pull
        # from the API.  The default in the API is set to 50, however we can
        # pull any variable amount.
        if 'limit' in kw and self._check('limit', kw['limit'], int):
            limit = kw['limit']

        # For the sorting fields, we are converting the tuple that has been
        # provided to us and converting it into a comma-delimited string with
        # each field being represented with its sorting order.  e.g. If we are
        # presented with the following:
        #
        #   sort=(('field1', 'asc'), ('field2', 'desc'))
        #
        # we will generate the following string:
        #
        #   sort=field1:asc,field2:desc
        #
        if 'sort' in kw and self._check('sort', kw['sort'], tuple):
            query['sort'] = ','.join(['{}:{}'.format(
                self._check('sort_field', i[0], str),
                self._check('sort_direction', i[1], str, choices=['asc', 'desc'])
            ) for i in kw['sort']])

        # The filter_type determines how the filters are combined together.
        # The default is 'and', however you can always explicitly define 'and'
        # or 'or'.
        if 'filter_type' in kw and self._check(
            'filter_type', kw['filter_type'], str, choices=['and', 'or']):
            query['ft'] = kw['filter_type']

        # The wild-card filter text refers to how the API will pattern match
        # within all fields, or specific fields using the wildcard_fields param.
        if 'wildcard' in kw and self._check('wildcard', kw['wildcard'], str):
            query['w'] = kw['wildcard']

        # The wildcard_fields parameter allows the user to restrict the fields
        # that the wild-card pattern match pertains to.
        if 'wildcard_fields' in kw and self._check(
            'wildcard_fields', kw['wildcard_fields'], list):
            query['wf'] = ','.join(kw['wildcard_fields'])

        # Return the Iterator.
        return AccessGroupsIteratorV2(self._api,
            _limit=limit,
            _offset=offset,
            _pages_total=pages,
            _query=query,
            _path='v2/access-groups',
            _resource='access_groups'
        )

    def create(self, name, rules, principals=None, all_users=False, access_group_type=None):
        '''
        Creates a new access group

        :devportal:`access-groups: create <v2-access-groups-create>`

        Args:
            name (str):
                The name of the access group to create.
            rules (list):
                a list of rule tuples.  Tuples are defined in the standardized
                method of name, operator, value.  For example:

                .. code-block:: python

                    ('operating_system', 'eq', ['Windows NT'])

                Rules will be validated against by the filters before being sent
                to the API.  Note that the value field in this context is a list
                of string values.
            principals (list, optional):
                A list of principal tuples.  Each tuple must contain the type,
                the identifier and the permissions for the principal.
                The identifier can be either a UUID associated to a user/group, or the name of the
                user/group and the permissions can be either a CAN_VIEW or CAN_EDIT or Both in list
                Default permission is ``CAN_VIEW``
                For example:

                .. code-block:: python

                    ('user', '32a0c314-442b-4aed-bbf5-ba9cf5cafbf4', ['CAN_VIEW'])
                    ('user', 'steve@company.tld', ['CAN_SCAN'])
                    ('group', '32a0c314-442b-4aed-bbf5-ba9cf5cafbf4')

            all_users (bool, optional):
                If enabled, the access group will apply to all users and any
                principals defined will be ignored.

            access_group_type (str, optional):
                The type of access group. It can be one of two possible types:
                `MANAGE_ASSETS`, `SCAN_TARGETS`
                The default is `MANAGE_ASSETS`

        Returns:
            :obj:`dict`:
                The resource record for the new access list.

        Examples:
            Allow all users to see 192.168.0.0/24:

            >>> tio.access_groups_v2.create('Example',
            ...     [('ipv4', 'eq', ['192.168.0.0/24'])],
            ...     all_users=True)

            Allow everyone in a specific group id to see specific hosts:

            >>> tio.access_groups_v2.create('Example',
            ...     [('netbios_name', 'eq', ['dc1.company.tld']),
            ...      ('netbios_name', 'eq', ['dc2.company.tld'])],
            ...     principals=[
            ...         ('group', '32a0c314-442b-4aed-bbf5-ba9cf5cafbf4', ['CAN_VIEW'])
            ... ])
        '''
        if not principals:
            principals = list()

        # construct the payload dictionary
        payload = {
            # run the rules through the filter parser...
            'rules': self._parse_filters(rules,
                self._api.filters.access_group_asset_rules_filters_v2(),
                    rtype='accessgroup')['rules'],

            # run the principals through the principal parser...
            'principals': self._principal_constructor(principals),
            'name': self._check('name', name, str),
            'all_users': self._check('all_users', all_users, bool),
            'access_group_type': self._check('access_group_type', access_group_type, str,
                choices=['MANAGE_ASSETS', 'SCAN_TARGETS'],
                default='MANAGE_ASSETS',
                case='upper')
        }

        # call the API endpoint and return the response to the caller.
        return self._api.post('v2/access-groups', json=payload).json()

    def delete(self, group_id):
        '''
        Deletes the specified access group.

        :devportal:`access-groups: delete <v2-access-groups-delete>`

        Args:
            group_id (str): The UUID of the access group to remove.
        '''
        self._api.delete('v2/access-groups/{}'.format(
            self._check('group_id', group_id, 'uuid')))

    def edit(self, group_id, **kw):
        '''
        Edits an access group

        :devportal:`access-groups: edit <v2-access-groups-edit>`

        Args:
            group_id (str):
                The UUID of the access group to edit.
            name (str, optional):
                The name of the access group to edit.
            rules (list, optional):
                a list of rule tuples.  Tuples are defined in the standardized
                method of name, operator, value.  For example:

                .. code-block:: python

                    ('operating_system', 'eq', ['Windows NT'])

                Rules will be validated against by the filters before being sent
                to the API.  Note that the value field in this context is a list
                of string values.
            principals (list, optional):
                A list of principal tuples.  Each tuple must contain the type,
                the identifier and the permissions for the principal.
                The identifier can be either a UUID associated to a user/group, or the name of the
                user/group and the permissions can be either a CAN_VIEW or CAN_SCAN or Both in list
                Default permission is ``CAN_VIEW``
                For example:

                .. code-block:: python

                    ('user', '32a0c314-442b-4aed-bbf5-ba9cf5cafbf4', ['CAN_VIEW'])
                    ('user', 'steve@company.tld', ['CAN_SCAN'])
                    ('group', '32a0c314-442b-4aed-bbf5-ba9cf5cafbf4')

            all_users (bool):
                If enabled, the access group will apply to all users and any
                principals defined will be ignored.
            all_assets (bool, optional):
                Specifies if the access group to modify is the default
                "all assets" group or a user-defined one.
            access_group_type (str, optional):
                The type of access group. It can be one of three possible types:
                `MANAGE_ASSETS`, `SCAN_TARGETS`
                The default is `MANAGE_ASSETS`
        '''

        # If any rules are specified, then run them through the filter parser.
        if 'rules' in kw:
            kw['rules'] = self._parse_filters(kw['rules'],
                self._api.filters.access_group_asset_rules_filters_v2(),
                    rtype='accessgroup')['rules']

        # if any principals are specified, then run them through the principal
        # parser.
        if 'principals' in kw:
            kw['principals'] = self._principal_constructor(kw['principals'])

        # get the details of the access group that we are supposed to be editing
        # and then merge in the keywords specified.
        details = dict_merge(self.details(self._check('group_id', group_id, 'uuid')), kw)

        # construct the payload from the merged details.
        payload = {
            'name': self._check('name', details['name'], str),
            'all_users': self._check('all_users', details['all_users'], bool),
            'all_assets': self._check('all_assets', details['all_assets'], bool),
            'rules': details['rules'],
            'principals': details['principals'],
            'access_group_type': details['access_group_type']
        }

        # call the API endpoint and return the response to the caller.
        return self._api.put('v2/access-groups/{}'.format(group_id), json=payload).json()

    def details(self, group_id):
        '''
        Retrieves the details of the specified access group.

        :devportal:`access-groups: details <v2-access-groups-details>`

        Args:
            group_id (str): The UUID of the access group.
        '''
        return self._api.get('v2/access-groups/{}'.format(
            self._check('group_id', group_id, 'uuid'))).json()
