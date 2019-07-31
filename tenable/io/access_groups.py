'''
access_groups
=============

The following methods allow for interaction into the Tenable.io
:devportal:`access-groups <access-groups>` API endpoints.

Methods available on ``tio.access_groups``:

.. rst-class:: hide-signature
.. autoclass:: AccessGroupsAPI

    .. automethod:: create
    .. automethod:: delete
    .. automethod:: details
    .. automethod:: edit
    .. automethod:: list
'''
from tenable.errors import UnexpectedValueError
from tenable.utils import dict_merge
from .base import TIOEndpoint, TIOIterator

class AccessGroupsIterator(TIOIterator):
    '''
    The access groups iterator provides a scalable way to work through
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

class AccessGroupsAPI(TIOEndpoint):
    def _principal_constructor(self, items):
        '''
        Simple principle tuple expander.  Also supports validating principle
        dictionaries for transparent passthrough.
        '''
        resp = list()
        for item in items:
            self._check('principal', item, (tuple, dict))
            if isinstance(item, tuple):
                self._check('principal:type', item[0], str,
                    choices=['user', 'group'])
                try:
                    resp.append({
                        'type': item[0],
                        'principal_id': self._check(
                            'principal:id', item[1], 'uuid')
                    })
                except UnexpectedValueError as err:
                    resp.append({
                        'type': item[0],
                        'principal_name': self._check(
                            'principal:name', item[1], str)
                    })
            else:
                self._check('principal:type', item['type'], str,
                    choices=['user', 'group'])
                if 'principal_id' in item:
                    self._check('principal_id', item['principal_id'], 'uuid')
                if 'principal_name' in item:
                    self._check('principal_name', item['principal_name'], str)
                resp.append(item)
        return resp

    def create(self, name, rules, principals=None, all_users=False):
        '''
        Creates a new access group

        :devportal:`access-groups: create <access-groups-create>`

        Args:
            name (str):
                The name of the access group to create.
            rules (list):
                a list of rule tuples.  Tuples are defined in the standardized
                method of name, operator, value.  For example:

                .. code-block:: python

                    ('operating_system', 'eq', ['Windows NT'])

                Rules will be validate against by the filters before being sent
                to the API.  Note that the value field in this context is a list
                of string values.
            principals (list, optional):
                A list of principal tuples.  Each tuple must contain both the
                type and the identifier for the principal.  The identifier can
                be either a UUID associated to a user/group, or the name of the
                user/group.  For example:

                .. code-block:: python

                    ('user', '32a0c314-442b-4aed-bbf5-ba9cf5cafbf4')
                    ('user', 'steve@company.tld')
                    ('group', '32a0c314-442b-4aed-bbf5-ba9cf5cafbf4')

            all_users (bool, optional):
                If enabled, the access group will apply to all users and any
                principals defined will be ignored.

        Returns:
            :obj:`dict`:
                The resource record for the new access list.

        Examples:
            Allow all users to see 192.168.0.0/24:

            >>> tio.access_groups.create('Example',
            ...     [('ipv4', 'eq', ['192.168.0.0/24'])],
            ...     all_users=True)

            Allow everyone in a specific group id to see specific hosts:

            >>> tio.access_groups.create('Example',
            ...     [('netbios_name', 'eq', ['dc1.company.tld']),
            ...      ('netbios_name', 'eq', ['dc2.company.tld'])],
            ...     principals=[
            ...         ('group', '32a0c314-442b-4aed-bbf5-ba9cf5cafbf4')
            ... ])
        '''
        if not principals:
            principals = list()

        # construct the payload dictionary
        payload = {
            # run the rules through the filter parser...
            'rules': self._parse_filters(rules,
                self._api.filters.access_group_asset_rules_filters(),
                    rtype='accessgroup')['rules'],

            # run the principals through the principal parser...
            'principals': self._principal_constructor(principals),
            'name': self._check('name', name, str),
            'all_users': self._check('all_users', all_users, bool),
        }

        # call the API endpoint and return the response to the caller.
        return self._api.post('access-groups', json=payload).json()

    def edit(self, id, **kw):
        '''
        Edits an access group

        :devportal:`access-groups: update <access-groups-edit>`

        Args:
            id (str):
                The UUID of the access group to edit.
            name (str, optional):
                The name of the access group to create.
            rules (list, optional):
                a list of rule tuples.  Tuples are defined in the standardized
                method of name, operator, value.  For example:

                .. code-block:: python

                    ('operating_system', 'eq', ['Windows NT'])

                Rules will be validate against by the filters before being sent
                to the API.  Note that the value field in this context is a list
                of string values.
            principals (list, optional):
                A list of principal tuples.  Each tuple must contain both the
                type and the identifier for the principal.  The identifier can
                be either a UUID associated to a user/group, or the name of the
                user/group.  For example:

                .. code-block:: python

                    ('user', '32a0c314-442b-4aed-bbf5-ba9cf5cafbf4')
                    ('user', 'steve@company.tld')
                    ('group', '32a0c314-442b-4aed-bbf5-ba9cf5cafbf4')

            all_users (bool, optional):
                If enabled, the access group will apply to all users and any
                principals defined will be ignored.
            all_assets (bool, optional):
                Specifies if the access group to modify is the default
                "all assets" group or a user-defined one.
        '''

        # If any rules are specified, then run them through the filter parser.
        if 'rules' in kw:
            kw['rules'] = self._parse_filters(kw['rules'],
                self._api.filters.access_group_asset_rules_filters(),
                    rtype='accessgroup')['rules']

        # if any principals are specified, then run them through the principal
        # parser.
        if 'principals' in kw:
            kw['principals'] = self._principal_constructor(kw['principals'])

        # get the details of the access group that we are supposed to be editing
        # and then merge in the keywords specified.
        g = dict_merge(self.details(self._check('id', id, 'uuid')), kw)

        # construct the payload from the merged details.
        payload = {
            'name': self._check('name', g['name'], str),
            'all_users': self._check('all_users', g['all_users'], bool),
            'all_assets': self._check('all_assets', g['all_assets'], bool),
            'rules': g['rules'],
            'principals': g['principals']
        }

        # call the API endpoint and return the response to the caller.
        return self._api.put('access-groups/{}'.format(id),
            json=payload).json()

    def delete(self, id):
        '''
        Deletes the specified access group.

        :devportal:`access-groups: delete <access-groups-delete>`

        Args:
            id (str): The UUID of the access group to remove.
        '''
        self._api.delete('access-groups/{}'.format(
            self._check('id', id, 'uuid')))

    def details(self, id):
        '''
        Retrieves the details of the specified access group.

        :devportal:`access-groups: details <access-groups-details>`

        Args:
            id (str): The UUID of the access group.
        '''
        return self._api.get('access-groups/{}'.format(
            self._check('id', id, 'uuid'))).json()

    def list(self, *filters, **kw):
        '''
        Get the listing of configured access groups from Tenable.io.

        :devportal:`access-groups: list <access-groups-list>`

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
                the :py:meth:`tio.filters.access_groups_filters() <FiltersAPI.access_groups_filters>`
                endpoint to get more details.
            filter_type (str, optional):
                The filter_type operator determines how the filters are combined
                together.  ``and`` will inform the API that all of the filter
                conditions must be met for an access group to be returned,
                whereas ``or`` would mean that if any of the conditions are met,
                the access group record will be returned.
            limit (int, optional):
                The number of records to retrieve.  Default is 50
            offset (int, optional):
                The starting record to retrieve.  Default is 0.
            sort (tuple, optional):
                A tuple of tuples identifying the the field and sort order of
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

            >>> for group in tio.access_groups.list():
            ...     pprint(group)

            Retrieving all of the windows agents:

            >>> for group in tio.access_groups.list(('name', 'eq', 'win')):
            ...     pprint(group)
        '''
        limit = 50
        offset = 0
        pages = None
        query = self._parse_filters(filters,
            self._api.filters.access_group_filters(), rtype='colon')

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
        return AccessGroupsIterator(self._api,
            _limit=limit,
            _offset=offset,
            _pages_total=pages,
            _query=query,
            _path='access-groups',
            _resource='access_groups'
        )

