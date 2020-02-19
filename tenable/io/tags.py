'''
tags
====

The following methods allow for interaction into the Tenable.io
:devportal:`tagging <tags>` API endpoints.

Methods available on ``tio.tags``:

.. rst-class:: hide-signature
.. autoclass:: TagsAPI

    .. automethod:: create
    .. automethod:: create_category
    .. automethod:: delete
    .. automethod:: delete_category
    .. automethod:: details
    .. automethod:: details_category
    .. automethod:: edit
    .. automethod:: edit_category
    .. automethod:: list
    .. automethod:: list_categories
'''
from .base import TIOEndpoint, TIOIterator
from tenable.errors import UnexpectedValueError

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
    _filterset_tags = {
        'value': {'operators': ['eq', 'match'], 'pattern': None, 'choices': None},
        'category_name': {'operators': ['eq', 'match'], 'pattern': None, 'choices': None},
        'description': {'operators': ['eq', 'match'], 'pattern': None, 'choices': None},
        'updated_at': {'operators': ['date-eq', 'date-gt', 'date-lt'], 'pattern': '\\d+', 'choices': None},
        'updated_by': {'operators': ['eq'], 'pattern': None} # Add UUID regex here
    }
    _filterset_categories = {
        'name': {'operators': ['eq', 'match'], 'pattern': None, 'choices': None},
        'description': {'operators': ['eq', 'match'], 'pattern': None, 'choices': None},
        'created_at': {'operators': ['date-eq', 'date-gt', 'date-lt'], 'pattern': '\\d+', 'choices': None},
        'updated_at': {'operators': ['date-eq', 'date-gt', 'date-lt'], 'pattern': '\\d+', 'choices': None},
        'updated_by': {'operators': ['eq'], 'pattern': None, 'choices': None} # Add UUID regex here
    }

    def create(self, category, value, description=None, filters=None,
               category_description=None):
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
            filters (dict, optional):
                The filter dictionary as specified within the API documents.

        Returns:
            :obj:`dict`:
                Tag value resource record

        Examples:
            Creating a new tag & Category:

            >>> tio.tags.create('Location', 'Chicago')

            Creating a new Tag value in the existing Location Category:

            >>> tio.tags.create('Location', 'New York')

            Creating a new Tag Value within a Category by UUID:

            >>> tio.tags.create('00000000-0000-0000-0000-000000000000', 'Madison')
        '''
        payload = dict()

        # First lets see if the category is a UUID or a general string.  If its
        # a UUID, then we will pass the value of category into the category_uuid
        # parameter, if not (but is still a string), then we will pass into
        # category_name
        try:
            payload['category_uuid'] = self._check('category', category, 'uuid')
        except UnexpectedValueError:
            payload['category_name'] = self._check('category', category, str)

        payload['value'] = self._check('value', value, str)

        if description:
            payload['description'] = self._check('description', description, str)
        if category_description:
            payload['category_description'] = self._check(
                'category_description', category_description, str)
        if filters:
            payload['filters'] = self._check('filters', filters, dict)

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

    def delete(self, tag_value_uuid):
        '''
        Deletes a tag category/value pair.

        :devportal:`tag: delete tag value <tags-delete-tag-value>`

        Args:
            tag_value_uuid (str):
                The unique identifier for the c/v pair to be deleted.

        Returns:
            :obj:`None`

        Examples:
            >>> tio.tags.delete('00000000-0000-0000-0000-000000000000')
        '''
        self._api.delete('tags/values/{}'.format(
            self._check('tag_value_uuid', tag_value_uuid, 'uuid')))

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

    def edit(self, tag_value_uuid, value=None, description=None, filters=None):
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
            filters (dict, optional):
                The filter dictionary as specified within the API documents.

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
        if filters:
            payload['filters'] = self._check('filters', filters, dict)
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
        if sort:
            query['sort'] = self._check('sort', sort, str,
                choices=[k for k in filterdefs.keys()])
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
            sort (str, optional):
                What field to sort the results on.

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
            sort (str, optional):
                What field to sort the results on.

        Returns:
            :obj:`TagIterator`:
                An iterator that handles the pagination of the results

        Examples:
            Return all of the Tag Categories:

            >>> for tag in tio.tags.list_categories():
            ...     pprint(tag)

            Return all of the Tags of the Location category:

            >>> for tag in tio.tags.list_categories(
            ...   ('category_name', 'eq', 'Location')):
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