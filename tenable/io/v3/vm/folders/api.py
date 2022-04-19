'''
Folders
=======

The following methods allow for interaction into the Tenable.io
:devportal:`folders <folders>` API endpoints.

Methods available on ``tio.v3.vm.folders``:

.. rst-class:: hide-signature
.. autoclass:: FoldersAPI
    :members:
'''
from typing import Union

from requests import Response

from tenable.io.v3.base.endpoints.explore import ExploreBaseEndpoint
from tenable.io.v3.base.iterators.explore_iterator import (CSVChunkIterator,
                                                           SearchIterator)
from tenable.io.v3.vm.folders.schema import FolderSchema


class FoldersAPI(ExploreBaseEndpoint):

    _path = 'api/v3/scans/folders'
    _conv_json = True
    _schema = FolderSchema()

    def create(self, name: str) -> int:
        '''
        Create a folder.

        :devportal:`folders: create <folders-create>`

        Args:
            name (str): The name of the new folder.

        Returns:
            :obj:`int`:
                The new folder id.

        Examples:
            >>> folder = tio.v3.vm.folders.create('New Folder Name')
        '''
        payload = self._schema.dump(self._schema.load({'name': name}))
        return self._post(json=payload)['id']

    def delete(self, id: int) -> None:
        '''
        Delete a folder.

        :devportal:`folders: delete <folders-delete>`

        Args:
            id (int): The unique identifier for the folder.

        Returns:
            :obj:`None`

        Examples:
            >>> tio.v3.vm.folders.delete(1)
        '''
        self._delete(f'{id}')

    def edit(self, id: int, name: str) -> None:
        '''
        Edit a folder.

        :devportal:`folders: edit <folders-edit>`

        Args:
            id (int): The unique identifier for the folder.
            name (str): The new name for the folder.

        Returns:
            :obj:`None`

        Examples:
            >>> tio.v3.vm.folders.edit(1, 'Updated Folder Name')
        '''
        payload = self._schema.dump(self._schema.load({'name': name}))
        self._put(f'{id}', json=payload)

    def search(self,
               **kwargs
               ) -> Union[CSVChunkIterator,
                          SearchIterator,
                          Response]:
        '''
        Search and retrieve the folders based on supported conditions.

        :devportal:`folders: search <folders-search>`

        Args:
            
            fields (list, optional):
                The list of field names to return from the Tenable API.
                
                Example:
                    >>> ['field1', 'field2']
            
            filter (tuple, dict, optional):
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
                the :py:meth:`tio.v3.vm.definitions.folders()`
                endpoint to get more details.
            
            sort list(tuple, dict):
                A list of dictionaries describing how to sort the data
                that is to be returned.
            
                Examples:
                    >>> [('field_name_1', 'asc'),
                    ...     ('field_name_2', 'desc')]
                    >>> [{'property': 'last_observed', 'order': 'desc'}]
            
            limit (int):
                Number of objects to be returned in each request.
                Default is 200.
            next (str):
                The pagination token to use when requesting the next page of
                results.  This token is presented in the previous response.
            return_resp (bool, optional):
                If set to true, will override the default behavior to return
                a requests.Response Object to the user.
            return_csv (bool):
                If set to true, It wil return the CSV Iterable. Returns all
                data in text/csv format on each next call with row headers
                on each page.
        
        :Returns:

            - Iterable:
                The iterable that handles the pagination for the job.

            - requests.Response:
                If ``return_resp`` is set to ``True``, then a response
                object is returned instead of an iterable.

        Examples:
            >>> for folder in tio.v3.vm.folders.search():
            ...     print(folder)
        '''
        iclass = SearchIterator
        if kwargs.get('return_csv', False):
            iclass = CSVChunkIterator
        return super()._search(resource='folders',
                               iterator_cls=iclass,
                               sort_type=self._sort_type.default,
                               api_path=f'{self._path}/search',
                               **kwargs
                               )
