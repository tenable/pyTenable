'''
Accounts
========

The following methods allow for interaction into the Tenable.io
:devportal:`Managed Security Service Provider v3 accounts
<io-mssp-accounts>` API endpoints.

Methods available on ``tio.v3.mssp.accounts``:

.. rst-class:: hide-signature
.. autoclass:: AccountsAPI
    :members:
'''
from typing import Union

from requests import Response

from tenable.io.v3.base.endpoints.explore import ExploreBaseEndpoint
from tenable.io.v3.base.iterators.explore_iterator import (CSVChunkIterator,
                                                           SearchIterator)


class AccountsAPI(ExploreBaseEndpoint):
    '''
    This class contains methods related to Accounts API
    '''
    _path = 'api/v3/mssp/accounts'
    _conv_json = True

    def search(self, **kwargs) -> Union[CSVChunkIterator,
                                        Response,
                                        SearchIterator]:
        '''
        Search and retrieve the accounts based on supported conditions.
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
                the :py:meth:`tio.v3.definitions.mssp.accounts()`
                endpoint to get more details.
            sort (list[tuple], optional):
                A list of dictionaries describing how to sort the data
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
            - Iterable:
                The iterable that handles the pagination for the job.
            - requests.Response:
                If ``return_resp`` is set to ``True``, then a response
                object is returned instead of an iterable.
        Examples:
            >>> tio.v3.mssp.accounts.search(filter=('container_name', 'eq',
            ...     'Example'), fields=['id', 'container_name', 'region'],
            ...     limit=2, sort=[('container_name', 'desc')])
        '''
        iclass = SearchIterator
        if kwargs.get('return_csv', False):
            iclass = CSVChunkIterator
        return super()._search(resource='accounts',
                               iterator_cls=iclass,
                               sort_type=self._sort_type.property_based,
                               api_path=f'{self._path}/search',
                               **kwargs
                               )
