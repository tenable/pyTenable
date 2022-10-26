'''
Assets V3 endpoints
===================

The following methods allow for interaction into the Tenable.io
:devportal:`assets <io-v3-uw-assets-search>` API endpoints.

Methods available on ``tio.v3.assets``:

.. rst-class:: hide-signature
.. autoclass:: AssetsAPI
    :members:
'''
from typing import Union

from requests import Response
from restfly.errors import ForbiddenError

from tenable.io.v3.base.endpoints.explore import ExploreBaseEndpoint
from tenable.io.v3.base.iterators.explore_iterator import (CSVChunkIterator, SearchIterator)


class AssetsAPI(ExploreBaseEndpoint):
    '''
    This will contain methods related to Explore -> Assets V3 API endpoints.
    '''
    _path = 'api/v3/assets'
    _conv_json = True

    def get_asset_uuids(self, **kw):
        items = []
        try:
            iterator = self.search_all(**kw)
            for item in iterator:
                items.append(item['id'])
        except ForbiddenError:
            print('please check kw arg(s) or uuids passed')
        return items


    def search_all(self, **kw) -> Union[SearchIterator, CSVChunkIterator, Response]:
        '''
        Retrieves all the assets.

        Args:
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
        Returns:
            Iterable:
                The iterable that handles the pagination for the job.
            requests.Response:
                If ``return_resp`` is set to ``True``, then a response
                object is returned instead of an iterable.

        Examples:
            >>> tio.v3.assets.search_all(filter=('netbios_name', 'eq', 'SCCM'),
            ...  limit=2, sort=[('last_observed', 'asc')])
        '''
        iclass = SearchIterator
        if kw.get('return_csv', False):
            iclass = CSVChunkIterator
        return super()._search(resource='assets',
                               iterator_cls=iclass,
                               api_path=f'{self._path}/search',
                               **kw)
