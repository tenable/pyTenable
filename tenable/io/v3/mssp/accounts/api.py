'''
Accounts
========

The following methods allow for interaction into the Tenable.io
:devportal:`Managed Security Service Provider v3 accounts
<io-mssp-accounts>` API.

Methods available on ``tio.v3.mssp.accounts``:

.. rst-class:: hide-signature
.. autoclass:: AccountsAPI
    :members:
'''
from typing import List

from tenable.io.v3.base.endpoints.explore import ExploreBaseEndpoint
from tenable.io.v3.base.iterators.explore_iterator import (CSVChunkIterator,
                                                           SearchIterator)


class AccountsAPI(ExploreBaseEndpoint):
    _path = 'api/v3/mssp/accounts'
    _conv_json = True

    def search(self, **kwargs) -> List:
        '''
        Retrieves the assets.

        Args:
            fields (list):
                The list of field names to return from the Tenable API.

                Example:
                    - ``['field1', 'field2']``
            filter (tuple, Dict):
                A nestable filter object detailing how to filter the results
                down to the desired subset.

                Examples:
                    >>> ('or', ('and', ('test', 'oper', '1'),
                                   ('test', 'oper', '2')
                            ),
                    'and', ('test', 'oper', 3)
                   )
                    >>> {'or': [
                    {'and': [
                        {'value': '1', 'operator': 'oper', 'property': '1'},
                        {'value': '2', 'operator': 'oper', 'property': '2'}
                        ]
                    }],
                    'and': [
                        {'value': '3', 'operator': 'oper', 'property': 3}
                        ]
                    }

                As the filters may change and sortable fields may change over
                time, it's highly recommended that you look at the output of
                the :py:meth:`tio.v3.vm.filters.asset_filters()`
                endpoint to get more details.
            sort list(tuple, Dict):
                A list of dictionaries describing how to sort the data
                that is to be returned.

                Examples:
                    - ``[('field_name_1', 'asc'),
                             ('field_name_2', 'desc')]``
                    - ``[{'property': 'last_observed', 'order': 'desc'}]``
            limit (int):
                Number of objects to be returned in each request.
                Default is 1000.
            next (str):
                The pagination token to use when requesting the next page of
                results.  This token is presented in the previous response.
            return_resp (bool):
                If set to true, will override the default behavior to return
                an iterable and will instead return the results for the
                specific page of data.
            return_csv (bool):
                If set to true, It wil return the CSV Iterable. Returns all
                data in text/csv format on each next call with row headers
                on each page.

        Returns:
            Returns:
                Iterable:
                    The iterable that handles the pagination and potentially
                    async requests for the job.
                requests.Response:
                    If ``return_json`` was set to ``True``, then a response
                    object is instead returned instead of an iterable.

        Examples:
            >>> tio.v3.mssp.accounts.search(filter=('netbios_name', 'eq',
            ...  'SCCM'), fields=['name', 'netbios_name', 'last_login'],
            ...    limit=2, sort=[('last_observed', 'asc')])
        '''
        iclass = SearchIterator
        if kwargs.get('return_csv', False):
            iclass = CSVChunkIterator
        return super().search(resource='accounts',
                              iterator_cls=iclass,
                              is_sort_with_prop=False,
                              api_path=f'{self._path}/search',
                              **kwargs
                              )
