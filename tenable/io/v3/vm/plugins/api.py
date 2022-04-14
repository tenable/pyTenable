'''
Plugins
=======

The following methods allow for interaction into the Tenable.io
:devportal:`plugins <plugins>` API endpoints.

Methods available on ``tio.v3.vm.plugins``:

.. rst-class:: hide-signature
.. autoclass:: PluginsAPI
    :members:
'''
from typing import Dict, Union

from requests import Response

from tenable.io.v3.base.endpoints.explore import ExploreBaseEndpoint
from tenable.io.v3.base.iterators.explore_iterator import (CSVChunkIterator,
                                                           SearchIterator)


class PluginsAPI(ExploreBaseEndpoint):
    '''
    This will contain all methods related to plugins
    '''
    _path = 'api/v3/plugins'
    _conv_json = True

    def family_details(self, family_id: int) -> Dict:
        '''
        Retrieve the details for a specific plugin family.

        :devportal:`plugins: family-details plugins-family-details>`

        Args:
            family_id (int):
                The plugin family unique identifier.

        Returns:
            :obj:`dict`:
                Returns a dictionary stating the id, name, and plugins that are
                housed within the plugin family.

        Examples:
            >>> family = tio.v3.vm.plugins.family_details(1)
        '''
        return super()._details(f'families/{family_id}')

    def plugin_details(self, plugin_id: int) -> Dict:
        '''
        Retrieve the details for a specific plugin.

        :devportal:`plugins: plugin-details <plugins-plugin-details>`

        Args:
            plugin_id (int): The plugin id for the requested plugin.

        Returns:
            :obj:`dict`:
                A dictionary stating the id, name, family, and any other
                relevant attributes associated to the plugin.

        Examples:
            >>> plugin = tio.v3.vm.plugins.plugin_details(19506)
            >>> pprint(plugin)
        '''
        return super()._details(f'plugin/{plugin_id}')

    def search(self, **kwargs) -> Union[CSVChunkIterator,
                                        SearchIterator,
                                        Response]:
        '''
        Search and retrieve the plugins based on supported conditions.
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
                the :py:meth:`tio.v3.definitions.vm.plugins()`
                endpoint to get more details.
            sort (list[tuple], optional):
                sort is a list of tuples in the form of
                ('FIELD', 'ORDER').
                It describes how to sort the data
                that is to be returned.
                Examples:
                    >>> [('field_name_1', 'asc'),
                    ...      ('field_name_2', 'desc')]
            limit (int, optional):
                Number of objects to be returned in each request.
                Default and max_limit is 200.
            next (str, optional):
                The pagination token to use when requesting the next page of
                results. This token is presented in the previous response.
            return_resp (bool, optional):
                If set to true, will override the default behavior to return
                a requests.Response Object to the user.
            return_csv (bool, optional):
                If set to true, it will return the CSV response or
                iterable (based on return_resp flag). Iterator returns all
                rows in text/csv format for each call with row headers.
        :Returns:
            - iterable:
                The iterable that handles the pagination for the job.
            - requests.Response:
                If ``return_resp`` is set to ``True``, then a response
                object is returned instead of an iterable.
        Examples:
            >>> tio.v3.vm.plugins.search(filter=('exploited_by_malware', 'eq',
            ...  False), fields=['id', 'name', 'description'],
            ...    limit=2, sort=[('name': 'desc)])
        '''
        iclass = SearchIterator
        if kwargs.get('return_csv', False):
            iclass = CSVChunkIterator
        return super()._search(iterator_cls=iclass,
                               api_path=f'{self._path}/search',
                               resource='plugins',
                               **kwargs
                               )

    def search_families(self, **kwargs) -> Union[CSVChunkIterator,
                                                 SearchIterator,
                                                 Response]:
        '''
        Search and retrieve the families based on supported conditions.
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
                the :py:meth:`tio.v3.definition.vm.plugin_families()`
                endpoint to get more details.
            sort (list[tuple], optional):
                sort is a list of tuples in the form of
                ('FIELD', 'ORDER').
                It describes how to sort the data
                that is to be returned.
                Examples:
                    >>> [('field_name_1', 'asc'),
                    ...      ('field_name_2', 'desc')]
            limit (int, optional):
                Number of objects to be returned in each request.
                Default and max_limit is 200.
            next (str, optional):
                The pagination token to use when requesting the next page of
                results. This token is presented in the previous response.
            return_resp (bool, optional):
                If set to true, will override the default behavior to return
                a requests.Response Object to the user.
            return_csv (bool, optional):
                If set to true, it will return the CSV response or
                iterable (based on return_resp flag). Iterator returns all
                rows in text/csv format for each call with row headers.
        :Returns:
            - iterable:
                The iterable that handles the pagination for the job.
            - requests.Response:
                If ``return_resp`` is set to ``True``, then a response
                object is returned instead of an iterable.
        Examples:
            >>> tio.v3.vm.plugins.search_families(filter=('name', 'eq',
            ...  'Amazon'), fields=['id', 'name', 'count'],
            ...    limit=2, sort=[('count': 'desc)])
        '''
        iclass = SearchIterator
        if kwargs.get('return_csv', False):
            iclass = CSVChunkIterator
        return super()._search(iterator_cls=iclass,
                               api_path=f'{self._path}/families/search',
                               resource='families',
                               **kwargs
                               )
