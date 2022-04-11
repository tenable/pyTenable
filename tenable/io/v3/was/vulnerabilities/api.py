'''
Vulnerability
=============

The following methods allow for interaction into the Tenable.io
:devportal:`vulnerabilities <was-v2-vulnerabilities>` API.

Methods available on ``tio.v3.was.vulnerabilities``:

.. rst-class:: hide-signature
.. autoclass:: VulnerabilityAPI
    :members:
'''
from typing import Dict, Union

from requests import Response

from tenable.io.v3.base.endpoints.explore import ExploreBaseEndpoint
from tenable.io.v3.base.iterators.explore_iterator import (CSVChunkIterator,
                                                           SearchIterator)


class VulnerabilityAPI(ExploreBaseEndpoint):
    '''
    API class containing all the methods related to WAS Vulnerability.
    '''
    _path = 'api/v3/findings/vulnerabilities/webapp'
    _conv_json = True

    def get_details(self, id: str) -> Dict:
        '''
        Return details of a particular finding

        Args:
            id: The unique identifier of the finding.

        Returns:
            :obj:`dict`: details of the respective finding id

        Examples:
            >>> tio.v3.was.vulnerabilities.get_details(id)
        '''
        # return super()._details(f'{id}')
        raise NotImplementedError('This method will be implemented later \
                                  once respective endpoint is \
                                  migrated to v3')

    def search(self,
               **kw
               ) -> Union[SearchIterator, CSVChunkIterator, Response]:
        '''
        Search and retrieve the WAS Vulnerabilities based on supported
        conditions.

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
                the :py:meth:`tio.v3.definitions.was.vulnerabilities()`
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
                a requests.Response Object as is to the user.

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
            >>> tio.v3.was.vulnerabilities.search(
            ... fields=['finding_id'], limit=2)
        '''
        iclass = SearchIterator
        if kw.get('return_csv', False):
            iclass = CSVChunkIterator
        return super()._search(iterator_cls=iclass,
                               sort_type=self._sort_type.property_based,
                               resource='findings',
                               api_path=f'{self._path}/search',
                               **kw
                               )
