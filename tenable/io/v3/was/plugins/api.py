'''
Plugins
=======

The following methods allow for interaction into the Tenable.io
:devportal:`Web Application Scanning v3 plugins <was-v2-plugins>` API.

Methods available on ``tio.v3.was.plugins``:

.. rst-class:: hide-signature
.. autoclass:: PluginsAPI
    :members:
'''
from typing import Dict, Union

from requests import Response

from tenable.io.v3.base.endpoints.explore import ExploreBaseEndpoint
from tenable.io.v3.base.iterators.was_iterator import (CSVChunkIterator,
                                                       SearchIterator)


class PluginsAPI(ExploreBaseEndpoint):
    '''
    This will contain all methods for WAS plugins
    '''
    _path = 'api/v3/was/plugins'
    _conv_json = True

    def details(self, id: int) -> Dict:
        '''
        Returns details for the specified Tenable.io
        Web Application Scanning plugin.

        :devportal:`was plugins: plugin details <was-v2-plugins-details>`

        Args:
            id (int):
                The ID of a Tenable.io Web Application Scanning plugin.

        Returns:
            :obj:`dict`:
                The resource record of the was plugin.

        Examples:
            >>> plugin = tio.v3.was.plugins.details(1)
        '''
        return self._details(f'{id}')

    def search(self,
               **kw
               ) -> Union[SearchIterator, CSVChunkIterator, Response]:
        '''
        Retrieves the plugins data

        Args:

            fields (list, optional):
                The list of field names to return from the Tenable API.

                Example:
                    >>> ['field1', 'field2']

            sort (list[tuple], optional):
                sort is a list of tuples in the form of
                ('FIELD', 'ORDER').
                It describes how to sort the data
                that is to be returned.

                Examples:
                    >>> [('field_name_1', 'asc'),
                    ...      ('field_name_2', 'desc')]

            filter (tuple, dict, optional):
                A nestable filter object detailing how to filter the results
                down to the desired subset.

                Examples:
                    >>> ('or', ('and', ('test', 'oper', '1'),
                    ...                 ('test', 'oper', '2')
                    ...             ),
                    ...     'and', ('test', 'oper', 3)
                    ... )
                    >>> {
                    ...  'or': [{
                    ...      'and': [{
                    ...              'value': '1',
                    ...              'operator': 'oper',
                    ...              'property': '1'
                    ...          },
                    ...          {
                    ...              'value': '2',
                    ...              'operator': 'oper',
                    ...              'property': '2'
                    ...          }
                    ...      ]
                    ...  }],
                    ...  'and': [{
                    ...      'value': '3',
                    ...      'operator': 'oper',
                    ...      'property': 3
                    ...  }]
                    ... }

                As the filters may change and sortable fields may change over
                time, it's highly recommended that you look at the output of
                the :py:meth: `tio.v3.definitions.was.plugins()` endpoint
                to get more details.
            limit (int, optional):
                Number of objects to be returned in each request.
                Default and maximum limit is 200.
            offset (int, optional):
                The pagination offset to use when requesting the next page of
                results.
            num_pages (int, optional):
                The total number of pages to request before stopping the
                iterator.
            return_resp (bool, optional):
                If set to true, will override the default behavior to return
                a requests.Response Object to the user.
            return_csv (bool, optional):
                If set to true, it will return the CSV response or
                iterable (based on return_resp flag). Iterator returns all
                rows in text/csv format for each call with row headers.

        Returns:

            Iterable:
                The iterable that handles the pagination for the job.

            requests.Response:
                If ``return_resp`` is set to ``True``, then a response
                object is returned instead of an iterable.

        Examples:
            >>> tio.v3.was.plugins.search(
            ...     filter=('name','eq','value'),
            ...     fields=['name', 'field_one', 'field_two'],
            ...     limit=2,
            ...     sort=[('name', 'asc')]
            ... )
        '''
        iclass = SearchIterator
        if kw.get('return_csv', False):
            iclass = CSVChunkIterator
        return super()._search_was(resource='plugins',
                                   iterator_cls=iclass,
                                   api_path=f'{self._path}/search',
                                   sort_type=self._sort_type.name_based,
                                   **kw
                                   )
