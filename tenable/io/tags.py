'''
Tags
====

The following methods allow for interaction into the Tenable Vulnerability Management
:devportal:`tagging <tags>` API endpoints.

Methods available on ``tio.tags``:

.. rst-class:: hide-signature
.. autoclass:: TagsAPI
    :members:
'''
import json
import re

from tenable.utils import dict_merge
from tenable.io.base import TIOEndpoint, TIOIterator


class TagsIterator(TIOIterator):
    '''
    The tags iterator provides a scalable way to work through tag list result
    sets of any size.  The iterator will walk through each page of data,
    returning one record at a time.  If it reaches the end of a page of
    records, then it will request the next page of information and then continue
    to return records from the next page (and the next, and the next) until the
    counter reaches the total number of records that the API has reported.

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


class TagsAPI(TIOEndpoint):
    '''
    This will contain all methods related to tags
    '''
    _filterset_tags = {
        'value': {
            'operators': ['eq', 'match'], 'pattern': None, 'choices': None
        },
        'category_name': {
            'operators': ['eq', 'match'], 'pattern': None, 'choices': None
        },
        'category_uuid': {
            'operators': ['eq'], 'pattern': r'^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12,32}$', 'choices': None
        },
        'description': {
            'operators': ['eq', 'match'], 'pattern': None, 'choices': None
        },
        'updated_at': {
            'operators': ['date-eq', 'date-gt', 'date-lt'], 'pattern': '\\d+', 'choices': None
        },
        'updated_by': {
            'operators': ['eq'], 'pattern': None
        }  # Add UUID regex here
    }
    _filterset_categories = {
        'name': {
            'operators': ['eq', 'match'], 'pattern': None, 'choices': None
        },
        'description': {
            'operators': ['eq', 'match'], 'pattern': None, 'choices': None
        },
        'created_at': {
            'operators': ['date-eq', 'date-gt', 'date-lt'], 'pattern': '\\d+', 'choices': None
        },
        'updated_at': {
            'operators': ['date-eq', 'date-gt', 'date-lt'], 'pattern': '\\d+', 'choices': None
        },
        'updated_by': {
            'operators': ['eq'], 'pattern': None, 'choices': None
        }  # Add UUID regex here
    }

    def _permission_constructor(self, items):
        '''
        Simple current_domain_permission tuple expander. Also supports validation of values
        '''
        resp = list()
        for item in items:
            self._check('item', item, (tuple, dict))
            if isinstance(item, tuple):
                if len(item) == 3:
                    item = item + ([],)
                resp.append({
                    'id': self._check('id', item[0], 'uuid'),
                    "name": self._check('name', item[1], str),
                    "type": self._check('type', item[2], str,
                                        choices=['user', 'group'], case='upper'),
                    "permissions": [
                        self._check('i', i, str,
                                    choices=['ALL', 'CAN_EDIT', 'CAN_SET_PERMISSIONS'], case='upper')
                        for i in self._check('permissions', item[3], list)],
                })
            else:
                data = dict()
                data['id'] = self._check('id', item['id'], 'uuid')
                data['name'] = self._check('name', item['name'], str)
                data['type'] = self._check('type', item['type'], str,
                                           choices=['user', 'group'], case='upper')
                data['permissions'] = [
                    self._check('i', i, str,
                                choices=['ALL', 'CAN_EDIT', 'CAN_SET_PERMISSIONS'], case='upper')
                    for i in self._check('permissions', item['permissions']
                    if 'permissions' in item else None, list,
                                         default=list())]
                resp.append(data)

        return resp

    def _tag_value_constructor(self, filters, filterdefs, filter_type):
        '''
        A simple constructor to handle constructing the filter parameters for the
        create and edit tag value.
        '''
        filter_type = self._check('filter_type', filter_type, str,
                                  choices=['and', 'or'], default='and', case='lower')

        # created default dictionary for payload filters key
        payload_filters = dict({
            'asset': dict({
                filter_type: list()
            })
        })

        if len(filters) > 0:
            # run the filters through the filter parser and update payload_filters
            parsed_filters = self._parse_filters(filters, filterdefs, rtype='assets')['asset']
            payload_filters['asset'][filter_type] = parsed_filters

        return payload_filters

    def create(self, category, value, description=None, category_description=None,
               filters=None, filter_type=None, all_users_permissions=None,
               current_domain_permissions=None):
        '''
        Create a tag category/value pair

        :devportal:`tags: create-tag-value <tags-create-tag-value-1>`

        Args:
            category (str):
                The category name, or the category UUID.  If the category does
                not exist, then it will be created along with the new value.
            value (str):
                The value for the tag.
            category_description (str, optional):
                If the category is to be created, a description can be
                optionally provided.
            description (str, optional):
                A description for the Category/Value pair.
            filters (list, optional):
                Filters are list of tuples in the form of ('FIELD', 'OPERATOR', 'VALUE').
                Multiple filters can be used and will filter down the data
                for automatically applying the tag to asset.

                Examples:
                    - ``('operating_system', 'match', ['Linux'])``
                    - ``('name', 'nmatch', 'home')``

                Note that multiple values can be passed in list of string format
            filter_type (str, optional):
                The filter_type operator determines how the filters are combined
                together.  ``and`` will inform the API that all of the filter
                conditions must be met whereas ``or`` would mean that if any of the
                conditions are met. Default is ``and``
            all_users_permissions (list, optional):
                List of the minimum set of permissions all users have on the current tag.
                Possible values are ALL, CAN_EDIT, and CAN_SET_PERMISSIONS.
            current_domain_permissions (list, optional):
                List of user and group-specific permissions for the current tag
                current_domain_permissions are list of tuples in the form of
                ('ID', 'NAME', 'TYPE', 'PERMISSIONS')
                the TYPE can be either `USER` or `GROUP` and
                the PERMISSIONS can be `ALL`, `CAN_EDIT` or `CAN_SET_PERMISSIONS`
                any one or all in list

                Examples:
                    - ``(uuid , 'user@company.com', 'USER', ['CAN_EDIT'])``

        Returns:
            :obj:`dict`:
                Tag value resource record

        Examples:
            Creating a new tag & Category:

            >>> tio.tags.create('Location', 'Chicago')

            Creating a new Tag value in the existing Location Category:

            >>> tio.tags.create('Location', 'New York')

            Creating a new Tag value in the existing Location Category
            and apply to assets dynamically:

            >>> tio.tags.create('Location', 'San Francisco',
            ...     filters=[('operating_system', 'match', ['Linux'])])

            Creating a new Tag value in the existing Location Category
            and set permissions for users:

            >>> tio.tags.create('Location', 'Washington',
            ...     all_users_permissions=['CAN_EDIT'],
            ...     current_domain_permissions=[('c2f2d080-ac2b-4278-914b-29f148682ee1',
            ...         'user@company.com', 'USER', ['CAN_EDIT'])
            ...     ])

            Creating a new Tag Value within a Category by UUID:

            >>> tio.tags.create('00000000-0000-0000-0000-000000000000', 'Madison')
        '''
        all_permissions = ['ALL', 'CAN_EDIT', 'CAN_SET_PERMISSIONS']
        payload = dict()

        # First lets see if the category is a UUID or a general string.  If its
        # a UUID, then we will pass the value of category into the category_uuid
        # parameter, if not (but is still a string), then we will pass into
        # category_name

        uuid_pattern = re.compile(r'^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$')

        if uuid_pattern.search(category):
            payload['category_uuid'] = self._check('category', category, 'uuid')
        else:
            payload['category_name'] = self._check('category', category, str)

        payload['value'] = self._check('value', value, str)

        if description:
            payload['description'] = self._check('description', description, str)
        if category_description:
            payload['category_description'] = self._check(
                'category_description', category_description, str)
        if not current_domain_permissions:
            current_domain_permissions = list()

        payload['access_control'] = {
            # setting default current_user_permissions to all
            'current_user_permissions': all_permissions,

            # check and assign all_users_permissions
            'all_users_permissions': [
                self._check('i', i, str, choices=['ALL', 'CAN_EDIT', 'CAN_SET_PERMISSIONS'])
                for i in self._check('all_users_permissions', all_users_permissions, list,
                                     default=list(), case='upper')],

            # run the current_domain_permissions through the permission_constructor
            'current_domain_permissions': self._permission_constructor(
                self._check('current_domain_permissions', current_domain_permissions, list)),
        }

        # if filters are defined, run the filters through the filter parser...
        if self._check('filters', filters, list):
            payload['filters'] = self._tag_value_constructor(
                filters, self._api.filters.asset_tag_filters(), filter_type)

        return self._api.post('tags/values', json=payload).json()

    def create_category(self, name, description=None):
        '''
        Creates a new category

        :devportal:`tags: create-category <tags-create-tag-category>`

        Args:
            name (str): The name of the category to create
            description (str, optional): Description for the category to create.

        Returns:
            :obj:`dict`:
                Tag category resource record

        Examples:
            >>> tio.tags.create_category('Location')
        '''
        payload = dict()
        payload['name'] = self._check('name', name, str)
        if description:
            payload['description'] = self._check('description', description, str)
        return self._api.post('tags/categories', json=payload).json()

    def delete(self, *tag_value_uuids):
        '''
        Deletes tag value(s).

        :devportal:`tag: delete tag value <tags-delete-tag-value>`

        Args:
            *tag_value_uuid (str):
                The unique identifier for the tag value to be deleted.

        Returns:
            :obj:`None`

        Examples:
            Deleting a single tag value:

            >>> tio.tags.delete('00000000-0000-0000-0000-000000000000')

            Deleting multiple tag values:

            >>> tio.tags.delete('00000000-0000-0000-0000-000000000000',
            ...     '10000000-0000-0000-0000-000000000001')
        '''
        if len(tag_value_uuids) <= 1:
            self._api.delete('tags/values/{}'.format(
                self._check('tag_value_uuid', tag_value_uuids[0], 'uuid')))
        else:
            self._api.post('tags/values/delete-requests',
                           json={'values': [
                               self._check('tag_value_uuid', i, 'uuid') for i in tag_value_uuids
                           ]})

    def delete_category(self, tag_category_uuid):
        '''
        Deletes a tag category.

        :devportal:`tag: delete tag category <tags-delete-tag-category>`

        Args:
            tag_category_uuid (str):
                The unique identifier for the tag category to be deleted.

        Returns:
            :obj:`None`

        Examples:
            >>> tio.tags.delete('00000000-0000-0000-0000-000000000000')
        '''
        self._api.delete('tags/categories/{}'.format(
            self._check('tag_category_uuid', tag_category_uuid, 'uuid')))

    def details(self, tag_value_uuid):
        '''
        Retrieves the details for a specific tag category/value pair.

        :devportal:`tag: tag details <tags-tag-value-details>`

        Args:
            tag_value_uuid (str):
                The unique identifier for the c/v pair

        Returns:
            :obj:`dict`:
                Tag value resource record

        Examples:
            >>> tio.tags.details('00000000-0000-0000-0000-000000000000')
        '''
        return self._api.get('tags/values/{}'.format(self._check(
            'tag_value_uuid', tag_value_uuid, 'uuid'))).json()

    def details_category(self, tag_category_uuid):
        '''
        Retrieves the details for a specific tag category.

        :devportal:`tag: tag category details <tags-tag-category-details>`

        Args:
            tag_category_uuid (str):
                The unique identifier for the category

        Returns:
            :obj:`dict`:
                Tag category resource record

        Examples:
            >>> tio.tags.details_category('00000000-0000-0000-0000-000000000000')
        '''
        return self._api.get('tags/categories/{}'.format(self._check(
            'tag_category_uuid', tag_category_uuid, 'uuid'))).json()

    def edit(self, tag_value_uuid, value=None, description=None, filters=None, filter_type=None,
             all_users_permissions=None, current_domain_permissions=None):
        '''
        Updates Tag category/value pair information.

        :devportal:`tag: edit tag value <tags-update-tag-value>`

        Args:
            tag_value_uuid (str):
                The unique identifier for the c/v pair to be edited.
            value (str, optional):
                The new name for the category value.
            description (str, optional):
                New description for the category value.
            filters (list, optional):
                Filters are list of tuples in the form of ('FIELD', 'OPERATOR', 'VALUE').
                Multiple filters can be used and will filter down the data
                for automatically applying the tag to asset.

                Examples::
                    - ``('operating_system', 'match', ['Linux'])``
                    - ``('name', 'nmatch', 'home')``

                Note that multiple values can be passed in list of string format
            filter_type (str, optional):
                The filter_type operator determines how the filters are combined
                together.  ``and`` will inform the API that all of the filter
                conditions must be met whereas ``or`` would mean that if any of the
                conditions are met. Default is ``and``
            all_users_permissions (list, optional):
                List of the minimum set of permissions all users have on the current tag.
                Possible values are ALL, CAN_EDIT, and CAN_SET_PERMISSIONS.
            current_domain_permissions (list, optional):
                List of user and group-specific permissions for the current tag
                current_domain_permissions are list of tuples in the form of
                ('ID', 'NAME', 'TYPE', 'PERMISSIONS')
                the TYPE can be either `USER` or `GROUP` and
                the PERMISSIONS can be `ALL`, `CAN_EDIT` or `CAN_SET_PERMISSIONS`
                any one or all in list

                Examples::
                    - ``(uuid, 'user@company.com', 'USER', ['CAN_EDIT'])``

        Returns:
            :obj:`dict`:
                Tag value resource record.

        Examples:
            >>> tio.tags.edit('00000000-0000-0000-0000-000000000000',
            ...     name='NewValueName')
        '''
        payload = dict()
        payload['value'] = self._check('value', value, str)
        if description:
            payload['description'] = self._check('description', description, str)

        # get existing values of tag
        current = self.details(self._check('tag_value_uuid', tag_value_uuid, 'uuid'))
        current_access_control = current['access_control']

        # created copy of current access control which will be used
        # to compare any changes done in permissions
        access_control = current_access_control.copy()

        # initialize access controls
        payload['access_control'] = dict()

        # Set all users permission
        if all_users_permissions is not None:
            current_access_control['all_users_permissions'] = [
                self._check('i', i, str, choices=['ALL', 'CAN_EDIT', 'CAN_SET_PERMISSIONS'])
                for i in self._check('all_users_permissions', all_users_permissions, list,
                                     case='upper')]

        # run current_domain_permissions through permission parser
        if current_domain_permissions is not None:
            current_access_control['current_domain_permissions'] = self._permission_constructor(
                current_domain_permissions)

        # update payload access control with new values
        payload['access_control'] = dict_merge(payload['access_control'], current_access_control)

        # We need to pick current value of version if available or set default value to 0
        # this value will be incremented when permissions are updated
        if 'version' in current['access_control']:
            current_version = current['access_control']['version']
        else:
            current_version = 0

        # version value must be incremented each time the permissions are updated
        if not payload['access_control'] == access_control:
            payload['access_control']['version'] = current_version + 1

        # if filters are defined, run the filters through the filter parser...
        # or else apply the filters that are available in current payload
        if filters is not None:
            self._check('filters', filters, list)
            payload['filters'] = self._tag_value_constructor(
                filters, self._api.filters.asset_tag_filters(), filter_type)
        elif 'filters' in current and current['filters']:
            # current value in filters are in form of string.
            # we have to first convert it into dict() form before applying
            current['filters']['asset'] = json.loads(current['filters']['asset'])
            payload['filters'] = current['filters']

        return self._api.put('tags/values/{}'.format(self._check(
            'tag_value_uuid', tag_value_uuid, 'uuid')), json=payload).json()

    def edit_category(self, tag_category_uuid, name=None, description=None):
        '''
        Updates Tag category information.

        :devportal:`tag: edit tag category <tags-edit-tag-category>`

        Args:
            tag_category_uuid (str):
                The unique identifier for the category to be edited.
            name (str, optional):
                The new name for the category.
            description (str, optional):
                New description for the category.

        Returns:
            :obj:`dict`:
                Tag category resource record.

        Examples:
            >>> tio.tags.edit_category('00000000-0000-0000-0000-000000000000',
            ...     name='NewValueName')
        '''
        payload = dict()
        payload['name'] = self._check('name', name, str)
        if description:
            payload['description'] = self._check('description', description, str)
        return self._api.put('tags/categories/{}'.format(self._check(
            'tag_category_uuid', tag_category_uuid, 'uuid')), json=payload).json()

    def _tag_list_constructor(self, filters, filterdefs, filter_type, sort):
        '''
        A simple constructor to handle constructing the query parameters for the
        list and list_category methods.
        '''
        query = self._parse_filters(filters, filterdefs, rtype='colon')
        if filter_type:
            query['ft'] = self._check('filter_type', filter_type, str,
                                      choices=['AND', 'OR'], case='upper')
        if sort and self._check('sort', sort, tuple):
            query['sort'] = ','.join(['{}:{}'.format(
                self._check('sort_field', i[0], str, choices=[k for k in filterdefs.keys()]),
                self._check('sort_direction', i[1], str, choices=['asc', 'desc'])
            ) for i in sort])
        return query

    def list(self, *filters, **kw):
        '''
        Retrieves a list of tag category/value pairs based off of the filters
        defined within the query.

        :devportal:`tags: list tags <tags-list-tag-values>`

        Args:
            *filters (tuple, optional):
                A defined filter tuple consisting of the name, operator, and
                value.  Example: ``('category_name', 'eq', 'Location')``.
            filter_type (str, optional):
                If multiple filters are defined, the filter_type toggles the
                behavior as to how these filters are used.  Either all of the
                filters have to match (``AND``) or any of the filters have to
                match (``OR``).  If not specified, the default behavior is to
                assume filter_type is ``AND``.
            limit (int, optional):
                How many records should be returned in a given page.  If nothing
                is set, it will default to 1000 records.
            pages (int, optional):
                How many pages of data would you like to request?
            offset (int, optional):
                How many records to skip before returning results.  If nothing
                is set, it will default to 0.
            sort (tuple, optional):
                A tuple of tuples identifying the the field and sort order of
                the field.

        Returns:
            :obj:`TagIterator`:
                An iterator that handles the pagination of the results

        Examples:
            Return all of the Tag Values:

            >>> for tag in tio.tags.list():
            ...     pprint(tag)

            Return all of the Tags of the Location category:

            >>> for tag in tio.tags.list(('category_name', 'eq', 'Location')):
            ...     pprint(tag)
        '''
        query = self._tag_list_constructor(filters, self._filterset_tags,
                                           kw['filter_type'] if 'filter_type' in kw else None,
                                           kw['sort'] if 'sort' in kw else None)
        return TagsIterator(self._api,
                            _limit=self._check('limit', kw.get('limit', 1000), int),
                            _offset=self._check('offset', kw.get('offset', 0), int),
                            _pages_total=self._check('pages', kw.get('pages'), int),
                            _query=query,
                            _path='tags/values',
                            _resource='values'
                            )

    def list_categories(self, *filters, **kw):
        '''
        Retrieves a list of tag categories based off of the filters defined
        within the query.

        :devportal:`tags: list categories <tags-list-tag-categories>`

        Args:
            *filters (tuple, optional):
                A defined filter tuple consisting of the name, operator, and
                value.  Example: ``('name', 'eq', 'Location')``.
            filter_type (str, optional):
                If multiple filters are defined, the filter_type toggles the
                behavior as to how these filters are used.  Either all of the
                filters have to match (``AND``) or any of the filters have to
                match (``OR``).  If not specified, the default behavior is to
                assume filter_type is ``AND``.
            limit (int, optional):
                How many records should be returned in a given page.  If nothing
                is set, it will default to 1000 records.
            pages (int, optional):
                How many pages of data would you like to request?
            offset (int, optional):
                How many records to skip before returning results.  If nothing
                is set, it will default to 0.
            sort (tuple, optional):
                A tuple of tuples identifying the the field and sort order of
                the field.

        Returns:
            :obj:`TagIterator`:
                An iterator that handles the pagination of the results

        Examples:
            Return all of the Tag Categories:

            >>> for tag in tio.tags.list_categories():
            ...     pprint(tag)

            Return all of the Tags of the Location category:

            >>> for tag in tio.tags.list_categories(
            ...   ('name', 'eq', 'Location')):
            ...     pprint(tag)
        '''
        query = self._tag_list_constructor(filters, self._filterset_categories,
                                           kw['filter_type'] if 'filter_type' in kw else None,
                                           kw['sort'] if 'sort' in kw else None)
        return TagsIterator(self._api,
                            _limit=self._check('limit', kw.get('limit', 1000), int),
                            _offset=self._check('offset', kw.get('offset', 0), int),
                            _pages_total=self._check('pages', kw.get('pages'), int),
                            _query=query,
                            _path='tags/categories',
                            _resource='categories'
                            )

    def assign(self, assets, tags):
        '''
        Assigns the tag category/value pairs defined to the assets defined.

        :devportal:`tags: assign tags <tags-assign-asset-tags>`

        Args:
            assets (list):
                A list of Asset UUIDs.
            tags (list):
                A list of tag category/value pair UUIDs.

        Returns:
            :obj:`str`:
                Job UUID of the assignment job.

        Examples:
            >>> tio.tags.assign(
            ...     assets=['00000000-0000-0000-0000-000000000000'],
            ...     tags=['00000000-0000-0000-0000-000000000000'])
        '''
        self._check('assets', assets, list)
        self._check('tags', tags, list)
        return self._api.post('tags/assets/assignments', json={
            'action': 'add',
            'assets': [self._check('asset', a, 'uuid') for a in assets],
            'tags': [self._check('tag', t, 'uuid') for t in tags],
        }).json()['job_uuid']

    def unassign(self, assets, tags):
        '''
        Un-assigns the tag category/value pairs defined to the assets defined.

        :devportal:`tags: assign tags <tags-assign-asset-tags>`

        Args:
            assets (list):
                A list of Asset UUIDs.
            tags (list):
                A list of tag category/value pair UUIDs.

        Returns:
            :obj:`str`:
                Job UUID of the un-assignment job.

        Examples:
            >>> tio.tags.unassign(
            ...     assets=['00000000-0000-0000-0000-000000000000'],
            ...     tags=['00000000-0000-0000-0000-000000000000'])
        '''
        self._check('assets', assets, list)
        self._check('tags', tags, list)
        return self._api.post('tags/assets/assignments', json={
            'action': 'remove',
            'assets': [self._check('asset', a, 'uuid') for a in assets],
            'tags': [self._check('tag', t, 'uuid') for t in tags],
        }).json()['job_uuid']

    def get_tag_uuid(self, category, value):
        """
        Fetches tag UUID using category/value pairs.

        Args:
            category (str):
                The category name for the tag.
            value (str):
                The value for the tag.

        Returns:
            :obj:`str`:
                Tag UUID.

        Examples:
            >>> tio.tags.get_tag_uuid('test_category','test_value')
        """
        response = self._api.get('tags/categories/filter-categories')
        tag_uuid = None

        for cat in response.json()['categories']:
            if cat['name'].casefold() == category.casefold():
                for val in cat['values']:
                    if val['value'].casefold() == value.casefold():
                        tag_uuid = val['uuid']

        return tag_uuid
