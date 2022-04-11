'''
Groups
======

The following methods allow for interaction into the Tenable.io
:devportal:`groups <groups>` API.

Methods available on ``tio.v3.platform.groups``:

.. rst-class:: hide-signature
.. autoclass:: GroupsAPI
    :members:
'''
from typing import Dict, List, Union
from uuid import UUID

from requests import Response

from tenable.io.v3.base.endpoints.explore import ExploreBaseEndpoint
from tenable.io.v3.base.iterators.explore_iterator import (CSVChunkIterator,
                                                           SearchIterator)
from tenable.io.v3.platform.groups.schema import PlatformGroupSchema

class GroupsAPI(ExploreBaseEndpoint):
    '''
    This will contain all methods related to Groups
    '''

    _path = 'api/v3/groups'
    _conv_json = True

    def add_user(self, group_id: UUID, user_id: UUID) -> List:
        '''
        Add a user to a user group.

        :devportal:`groups: add-user <groups-add-user>`

        Args:
            group_id (uuid.UUID):
                The unique identifier of the group to add the user to.
            user_id (uuid.UUID):
                The unique identifier of the user to add.

        Returns:
            :obj:`list`:
                List of user resource records based on membership to the
                specified group.

        Examples:
            >>> tio.v3.platform.groups.add_user(
            ...     '00000000-0000-0000-0000-000000000000',
            ...     '00000000-0000-0000-0000-000000000000'
            ... )
        '''
        schema = PlatformGroupSchema()
        schema.dump(schema.load({"group_id": group_id, "user_id": user_id}))
        self._post(f'{group_id}/users/{user_id}')
        return self.list_users(group_id)

    def create(self, name: str) -> Dict:
        '''
        Create a new user group.

        :devportal:`groups: create <groups-create>`

        Args:
            name (str):
                The name of the group that will be created.

        Returns:
            :obj:`dict`:
                The group resource record of the newly minted group.

        Examples:
            >>> group = tio.v3.platform.groups.create('Group Name')
        '''
        schema = PlatformGroupSchema()
        schema.dump(schema.load({'name': name}))
        return self._post(json={'name': name})

    def delete(self, group_id: UUID) -> None:
        '''
        Delete a user group.

        :devportal:`groups: delete <groups-delete>`

        Args:
            group_id (uuid.UUID): The unique identifier for the group to be deleted.

        Returns:
            :obj:`None`

        Examples:
            >>> tio.v3.platform.groups.delete(
            ...     '00000000-0000-0000-0000-000000000000'
            ... )
        '''
        schema = PlatformGroupSchema()
        schema.dump(schema.load({'group_id': group_id}))
        self._delete(group_id)

    def delete_user(self, group_id: UUID, user_id: UUID) -> None:
        '''
        Delete a user from a user group.

        :devportal:`groups: delete-user <groups-delete-user>`

        Args:
            group_id (uuid.UUID):
                The unique identifier for the group to be modified.
            user_id (uuid.UUID):
                The unique identifier for the user to be removed
                from the group.

        Returns:
            :obj:`None`

        Examples:
            >>> tio.v3.platform.groups.delete_user(
            ...     '00000000-0000-0000-0000-000000000000',
            ...     '00000000-0000-0000-0000-000000000000'
            ... )
        '''
        schema = PlatformGroupSchema()
        schema.dump(schema.load({"group_id": group_id, "user_id": user_id}))
        self._delete(f'{group_id}/users/{user_id}')

    def edit(self, group_id: UUID, name: str) -> Dict:
        '''
        Edit a user group.

        :devportal:`groups: edit <groups/edit>`

        Args:
            group_id (uuid.UUID):
                The unique identifier for the group to be modified.
            name (str):
                The new name for the group.

        Returns:
            :obj:`dict`:
                The group resource record.

        Examples:
            >>> tio.v3.platform.groups.edit(
            ...     '00000000-0000-0000-0000-000000000000',
            ...     'Updated name'
            ... )
        '''
        schema = PlatformGroupSchema()
        schema.dump(schema.load({"group_id": group_id, "name": name}))
        return self._put(group_id, json={'name': name})

    def list_users(self, group_id: UUID) -> List:
        '''
        List the user memberships within a specific user group.

        :devportal:`groups: list-users <groups-list-users>`

        Args:
            group_id (uuid.UUID): The unique identifier of the group requested.

        Returns:
            :obj:`list`:
                List of user resource records based on membership to the
                specified group.

        Example:
            >>> group_id = '00000000-0000-0000-0000-000000000000'
            >>> for user in tio.v3.platform.groups.list_users(group_id):
            ...     pprint(user)
        '''
        return self._get(f'{group_id}/users')['users']

    def search(self,
               **kwargs
               ) -> Union[CSVChunkIterator,
                          SearchIterator,
                          Response]:
        '''
        Search and retrieve the user groups based on supported conditions.

        :devportal:`groups: search <groups-list>`

        Args:
            fields (list):
                The list of field names to return from the Tenable API.
                Example:
                    - ['field1', 'field2']
            filter (tuple, dict):
                A nestable filter object detailing how to filter the results
                down to the desired subset.
                Examples:
                    >>> ('or', ('and', ('test', 'oper', '1'),
                    ...            ('test', 'oper', '2')
                    ...     ),
                    ... 'and', ('test', 'oper', 3)
                    ... )
                    >>> {'or': [
                    ...         {'and': [
                    ...                 {
                    ...                     'value': '1',
                    ...                     'operator': 'oper',
                    ...                     'property': '1'
                    ...                 },
                    ...                 {
                    ...                     'value': '2',
                    ...                     'operator': 'oper',
                    ...                     'property': '2'
                    ...                 }
                    ...             ]
                    ...         }
                    ...     ],
                    ... 'and': [
                    ...         {
                    ...             'value': '3',
                    ...             'operator': 'oper',
                    ...             'property': 3
                    ...         }
                    ...     ]
                    ... }
                As the filters may change and sortable fields may change over
                time, it's highly recommended that you look at the output of
                the :py:meth:`tio.v3.platform.definitions.groups()`
                endpoint to get more details.
            limit (int):
                Number of objects to be returned in each request.
                Default is 200.
            next (str):
                The pagination token to use when requesting the next page of
                results.  This token is obtained from the previous response.
            return_resp (bool):If set to true, will override the default behavior to return
                a requests. Response Object to the user.
            return_csv (bool):
                If set to true, It wil return the CSV Iterable. Returns all
                data in text/csv format on each next call with row headers
                on each page.
        Returns:
            Iterable:
                The iterable that handles the pagination and potentially
                async requests for the job.
            requests.Response:
                If ``return_resp`` is set to ``True``, then a response
                object is returned instead of an iterable.
        Examples:
            >>> for group in tio.v3.platform.groups.search():
            ...     print(group)
        '''
        iclass = SearchIterator
        if kwargs.get('return_csv', False):
            iclass = CSVChunkIterator
        return super()._search(resource='groups',
                               iterator_cls=iclass,
                               api_path=f'{self._path}/search',
                               **kwargs
                               )
