'''
Tags
====

The following methods allow for interaction into the Tenable.io
:devportal:`tagging <tags>` API endpoints.

Methods available on ``tio.v3.vm.tags``:

.. rst-class:: hide-signature
.. autoclass:: TagsAPI
    :members:
'''
import json
import re
from typing import Dict, List, Union
from uuid import UUID

from restfly.utils import dict_clean, dict_merge

from tenable.io.v3.base.endpoints.explore import ExploreBaseEndpoint
from tenable.io.v3.vm.tags.schema import (AssetTagSchema, TagCategorySchema,
                                          TagValueSchema)


class TagsAPI(ExploreBaseEndpoint):
    '''
    This will contain all methods related to tags
    '''
    _path = 'tags'
    _conv_json = True

    def _tag_value_constructor(self,
                               filters: list,
                               filterdefs: dict,
                               filter_type: str
                               ) -> Dict:
        '''
        A simple constructor to handle constructing the filter
        parameters for the create and edit tag value.
        '''
        # validate filter_type with marshmallow schema
        schema = TagValueSchema(only=['filter_type'])
        filter_type = schema.dump(schema.load(dict_clean({
            'filter_type': filter_type
        })))['filter_type']

        # created default dictionary for payload filters key
        payload_filters = dict({
            'asset': dict({
                filter_type: list()
            })
        })

        if len(filters) > 0:
            # run the filters through the filter parser
            # and update payload_filters
            parsed_filters = self._parse_filters(
                filters,
                filterdefs,
                rtype='assets'
            )['asset']
            payload_filters['asset'][filter_type] = parsed_filters

        return payload_filters

    def create(self,
               category: Union[str, UUID],
               value: str,
               description: str = None,
               category_description: str = None,
               filters: List = None,
               filter_type: str = None,
               all_users_permissions: List = None,
               current_domain_permissions: List = None,
               ) -> Dict:
        '''
        Create a tag category/value pair

        :devportal:`tags: create-tag-value <tags-create-tag-value-1>`

        Args:
            category (str):
                The category name, or the category UUID.  If the category does
                not exist, then it will be created along with the new value.
            value (str):
                The value for the tag.
            description (str, optional):
                A description for the Category/Value pair.
            category_description (str, optional):
                If the category is to be created, a description can be
                optionally provided.
            filters (list, optional):
                Filters are list of tuples in the form of
                ('FIELD', 'OPERATOR', 'VALUE').
                Multiple filters can be used and will filter down the data
                for automatically applying the tag to asset.

                Examples:
                    - ``('distro', 'match', ['win', 'linux'])``
                    - ``('name', 'nmatch', 'home')``

                Note that multiple values can be passed in list of string
                format
            filter_type (str, optional):
                The filter_type operator determines how the filters are
                combined together. ``and`` will inform the API that all of the
                filter conditions must be met whereas ``or`` would mean that
                if any of the conditions are met. Default is ``and``:
            all_users_permissions (list, optional):
                List of the minimum set of permissions all users have on
                the current tag.
                Possible values are ALL, CAN_EDIT, and CAN_SET_PERMISSIONS.
            current_domain_permissions (list, optional):
                List of user and group-specific permissions for the current tag
                current_domain_permissions are list of tuples in the form of
                ('ID', 'NAME', 'TYPE', 'PERMISSIONS')
                the TYPE can be either `USER` or `GROUP` and
                the PERMISSIONS can be
                `ALL`, `CAN_EDIT` or `CAN_SET_PERMISSIONS`
                any one or all in list

                Examples:
                    - ``(uuid , 'user@company.com', 'USER', ['CAN_EDIT'])``

        Returns:
            :obj:`dict`:
                Tag value resource record

        Examples:
            Creating a new tag & Category:

            >>> tio.v3.vm.tags.create('Location', 'Chicago')

            Creating a new Tag value in the existing Location Category:

            >>> tio.v3.vm.tags.create('Location', 'New York')

            Creating a new Tag value in the existing Location Category
            and apply to assets dynamically:

            >>> tio.v3.vm.tags.create('Location', 'San Francisco',
            ...     filters=[('distro', 'match', ['win', 'linux'])])

            Creating a new Tag value in the existing Location Category
            and set permissions for users:

            >>> tio.v3.vm.tags.create('Location', 'Washington',
            ...     all_users_permissions=['CAN_EDIT'],
            ...     current_domain_permissions=[
            ...         (
            ...             'c2f2d080-ac2b-4278-914b-29f148682ee1',
            ...             'user@company.com',
            ...             'USER',
            ...             ['CAN_EDIT']
            ...         )
            ...     ])

            Creating a new Tag Value within a Category by UUID:

            >>> tio.v3.vm.tags.create(
            ...     '00000000-0000-0000-0000-000000000000',
            ...     'Madison'
            ... )
        '''

        # First lets see if the category is a UUID or a general string.  If its
        # a UUID, then we will pass the value of category into the
        # category_uuid parameter, if not (but is still a string), then we will
        # pass into category_name

        uuid_pattern = re.compile(
            r'^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}'
            r'-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$'
        )

        category_uuid = category_name = None
        if uuid_pattern.search(category):
            category_uuid = category
        else:
            category_name = category

        payload: dict = {
            'category_uuid': category_uuid,
            'category_name': category_name,
            'category_description': category_description,
            'value': value,
            'description': description,
            'access_control': {
                # setting default current_user_permissions to all
                'current_user_permissions': [
                    'ALL', 'CAN_EDIT', 'CAN_SET_PERMISSIONS'
                ],
                # check and assign all_users_permissions
                'all_users_permissions': all_users_permissions or [],
                'current_domain_permissions':
                    current_domain_permissions or [],
            },
            'filters': None
        }

        # if filters are defined, run the filters through the filter parser...
        if filters and isinstance(filters, list):
            payload['filters'] = self._tag_value_constructor(
                filters,
                self._api.filters.asset_tag_filters(),
                filter_type
            )

        # Let's validate the payload using marshmallow schema
        payload = dict_clean(payload)
        schema = TagValueSchema()
        payload = schema.dump(schema.load(payload))

        return self._post('values', json=payload)

    def create_category(self, name: str, description: str = None) -> Dict:
        '''
        Creates a new category

        :devportal:`tags: create-category <tags-create-tag-category>`

        Args:
            name (str):
                The name of the category to create
            description (str, optional):
                Description for the category to create.

        Returns:
            :obj:`dict`:
                Tag category resource record

        Examples:
            >>> tio.v3.vm.tags.create_category('Location')
        '''
        payload: dict = {
            'name': name,
            'description': description
        }
        payload = dict_clean(payload)

        # let's validate payload using marshmallow schema
        schema = TagCategorySchema()
        payload = schema.dump(schema.load(payload))

        return self._post('categories', json=payload)

    def delete(self, *value_ids: UUID) -> None:
        '''
        Deletes tag value(s).

        :devportal:`tag: delete tag value <tags-delete-tag-value>`

        Args:
            *value_ids (str):
                The unique identifier for the tag value to be deleted.

        Returns:
            :obj:`None`

        Examples:
            Deleting a single tag value:

            >>> tio.v3.vm.tags.delete('00000000-0000-0000-0000-000000000000')

            Deleting multiple tag values:

            >>> tio.v3.vm.tags.delete(
            ...     '00000000-0000-0000-0000-000000000000',
            ...     '10000000-0000-0000-0000-000000000001'
            ... )
        '''
        if len(value_ids) == 1:
            self._delete(f'values/{value_ids[0]}')
        else:
            payload: dict = {
                'values': [value_id for value_id in value_ids]
            }
            # Let's validate the payload using marshmallow schema
            schema = TagValueSchema(only=['value_id'])
            payload = schema.dump(schema.load(payload))
            self._post('values/delete-requests', json=payload)

    def delete_category(self, category_id: UUID) -> None:
        '''
        Deletes a tag category.

        :devportal:`tag: delete tag category <tags-delete-tag-category>`

        Args:
            category_id (str):
                The unique identifier for the tag category to be deleted.

        Returns:
            :obj:`None`

        Examples:
            >>> tio.v3.vm.tags..delete('00000000-0000-0000-0000-000000000000')
        '''
        self._delete(f'categories/{category_id}')

    def details(self, value_id: UUID) -> Dict:
        '''
        Retrieves the details for a specific tag category/value pair.

        :devportal:`tag: tag details <tags-tag-value-details>`

        Args:
            value_id (str):
                The unique identifier for the c/v pair

        Returns:
            :obj:`dict`:
                Tag value resource record

        Examples:
            >>> tio.v3.vm.tags.details('00000000-0000-0000-0000-000000000000')
        '''
        return self._get(f'values/{value_id}')

    def details_category(self, category_id: UUID) -> Dict:
        '''
        Retrieves the details for a specific tag category.

        :devportal:`tag: tag category details <tags-tag-category-details>`

        Args:
            category_id (UUID):
                The unique identifier for the category

        Returns:
            :obj:`dict`:
                Tag category resource record

        Examples:
            >>> tio.v3.vm.tags.details_category(
            ...     category_id = '00000000-0000-0000-0000-000000000000'
            ... )
        '''
        return self._get(f'categories/{category_id}')

    def edit(self,
             value_id: UUID,
             value: str = None,
             description: str = None,
             filters: List = None,
             filter_type: str = None,
             all_users_permissions: List = None,
             current_domain_permissions: List = None
             ) -> Dict:
        '''
        Updates Tag category/value pair information.

        :devportal:`tag: edit tag value <tags-update-tag-value>`

        Args:
            value_id (str):
                The unique identifier for the c/v pair to be edited.
            value (str, optional):
                The new name for the category value.
            description (str, optional):
                New description for the category value.
            filters (list, optional):
                Filters are list of tuples in the form of
                ('FIELD', 'OPERATOR', 'VALUE').
                Multiple filters can be used and will filter down the data
                for automatically applying the tag to asset.

                Examples::
                    - ``('distro', 'match', ['win', 'linux'])``
                    - ``('name', 'nmatch', 'home')``

                Note:
                     multiple values can be passed in list of string format
            filter_type (str, optional):
                The filter_type operator determines how the filters are
                combined together.  ``and`` will inform the API that all of
                the filter conditions must be met whereas ``or`` would mean
                that if any of the conditions are met. Default is ``and``
            all_users_permissions (list, optional):
                List of the minimum set of permissions all users have on the
                current tag.
                Possible values are ALL, CAN_EDIT, and CAN_SET_PERMISSIONS.
            current_domain_permissions (list, optional):
                List of user and group-specific permissions for the current tag
                current_domain_permissions are list of tuples in the form of
                ('ID', 'NAME', 'TYPE', 'PERMISSIONS')
                the TYPE can be either `USER` or `GROUP` and the
                PERMISSIONS can be `ALL`, `CAN_EDIT` or `CAN_SET_PERMISSIONS`
                any one or all in list

                Examples::
                    - ``(uuid, 'user@company.com', 'USER', ['CAN_EDIT'])``

        Returns:
            :obj:`dict`:
                Tag value resource record.

        Examples:
            >>> tio.v3.vm.tags.edit('00000000-0000-0000-0000-000000000000',
            ...     value='NewValueName')
        '''

        payload: dict = {
            'value': value,
            'description': description
        }

        # get existing values of tag
        current = self.details(value_id=value_id)
        current_access_control = current['access_control']

        # created copy of current access control which will be used
        # to compare any changes done in permissions
        access_control = current_access_control.copy()

        # initialize access controls
        payload['access_control'] = dict()

        # Set all users permission
        if all_users_permissions is not None:
            current_access_control['all_users_permissions'] = \
                all_users_permissions

        # run current_domain_permissions through permission parser
        if current_domain_permissions is not None:
            current_access_control['current_domain_permissions'] = \
                current_domain_permissions

        # update payload access control with new values
        payload['access_control'] = dict_merge(
            payload['access_control'],
            current_access_control
        )

        # We need to pick current value of version if available or set default
        # value to 0.
        # this value will be incremented when permissions are updated
        if 'version' in current['access_control']:
            current_version = current['access_control']['version']
        else:
            current_version = 0

        # version value must be incremented each time the
        # permissions are updated
        if payload['access_control'] != access_control:
            payload['access_control']['version'] = current_version + 1

        # if filters are defined, run the filters through the filter parser...
        # or else apply the filters that are available in current payload
        if filters is not None:
            payload['filters'] = self._tag_value_constructor(
                filters,
                self._api.filters.asset_tag_filters(),
                filter_type
            )
        elif 'filters' in current and current['filters']:
            # current value in filters are in form of string.
            # we have to first convert it into dict() form before applying
            current['filters']['asset'] = json.loads(
                current['filters']['asset']
            )
            payload['filters'] = current['filters']

        # validate payload using marshmallow schema
        payload = dict_clean(payload)
        schema = TagValueSchema()
        payload = schema.dump(schema.load(payload))

        return self._put(f'values/{value_id}', json=payload)

    def edit_category(self,
                      category_id: UUID,
                      name: str,
                      description: str = None
                      ) -> Dict:
        '''
        Updates Tag category information.

        :devportal:`tag: edit tag category <tags-edit-tag-category>`

        Args:
            category_id (UUID):
                The unique identifier for the category to be edited.
            name (str):
                The new name for the category.
            description (str, optional):
                New description for the category.

        Returns:
            :obj:`dict`:
                Tag category resource record.

        Examples:
            >>> tio.v3.vm.tags.edit_category(
            ...     category_id='00000000-0000-0000-0000-000000000000',
            ...     name='NewValueName'
            ... )
        '''
        payload: dict = {
            'name': name,
            'description': description
        }
        payload = dict_clean(payload)

        # let's validate payload using marshmallow schema
        schema = TagCategorySchema()
        payload = schema.dump(schema.load(payload))

        return self._put(f'categories/{category_id}', json=payload)

    def list_asset_tag(self, asset_id: UUID) -> Dict:
        '''
        Retrieves the details about a specific asset.

        :devportal:`tags: asset-tags <tags-list-asset-tags>`

        Args:
            asset_id (str):
                The UUID (unique identifier) for the asset.

        Returns:
            :obj:`dict`:
                Asset resource definition.

        Examples:
            >>> asset = tio.v3.vm.assets.tags(
            ...     '00000000-0000-0000-0000-000000000000')
        '''
        return self._get(f'assets/{asset_id}/assignments')

    def assign(self, assets: List, tags: List) -> str:
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
            >>> tio.v3.vm.tags.assign(
            ...     assets=['00000000-0000-0000-0000-000000000000'],
            ...     tags=['00000000-0000-0000-0000-000000000000'])
        '''
        payload: dict = {
            'action': 'add',
            'assets': assets,
            'tags': tags
        }

        # Let's validate the payload using marshmallow schema
        schema = AssetTagSchema()
        payload = schema.dump(schema.load(payload))

        return self._post('assets/assignments', json=payload)['job_id']

    def unassign(self, assets: List, tags: List) -> str:
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
            >>> tio.v3.vm.tags.unassign(
            ...     assets=['00000000-0000-0000-0000-000000000000'],
            ...     tags=['00000000-0000-0000-0000-000000000000'])
        '''
        payload: dict = {
            'action': 'remove',
            'assets': assets,
            'tags': tags
        }

        # let's validate the payload using marshmallow schema
        schema = AssetTagSchema()
        payload = schema.dump(schema.load(payload))

        return self._post('assets/assignments', json=payload)['job_id']

    def search(self):
        raise NotImplementedError('This method will be updated letter.')

    def search_categories(self):
        raise NotImplementedError('This method will be updated letter.')
