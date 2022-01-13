'''
Templates
=========

The following methods allow for interaction into the Tenable.io
:devportal:`Web Application Scanning v3 templates <was-v2-templates>` API.

Methods available on ``tio.v3.was.templates``:

.. rst-class:: hide-signature
.. autoclass:: TemplatesAPI
    :members:
'''
from typing import Dict, Union
from uuid import UUID

from requests import Response

from tenable.io.v3.base.endpoints.explore import ExploreBaseEndpoint
from tenable.io.v3.base.iterators.explore_iterator import (CSVChunkIterator,
                                                           SearchIterator)


class TemplatesAPI(ExploreBaseEndpoint):
    '''
    This class contains all methods related to Templates
    '''
    _path = 'api/v3/was/templates'
    _conv_json = True

    def details(self, template_id: UUID) -> Dict:
        '''
        Returns the details for a Tenable-provided template. Tenable-provided
        templates can be used to define scan configurations.

        :devportal:`was templates: Get Tenable-provided template details
        <was-v2-templates-details>`

        Args:
            template_id (UUID):
                The UUID of the Tenable-provided template resource.

        Returns:
            :obj:`dict`: The resource record of the template.

        Examples:
            >>> template = (tio.v3.was.templates.
            ...     details('d5b3cb1c-9c72-4974-a936-3dfbd2e2835e'))
            >>> pprint(template)
        '''
        return super()._details(template_id)

    def search(self, **kwargs) -> Union[SearchIterator,
                                        CSVChunkIterator,
                                        Response]:
        '''
        Search and retrieve the templates based on supported conditions.
        Args:
            fields (list, optional):
                The list of field names to return from the Tenable API.
                Example:
                    >>> ['field1', 'field2']
            filter (tuple, Dict, optional):
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
                the :py:meth:`tio.v3.was.filters.templates_filters()`
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
                an iterable and will instead return the results for the
                specific page of data.
            return_csv (bool, optional):
                If set to true, it will return the CSV response or
                iterable (based on return_resp flag). Iterator returns all
                rows in text/csv format for each call with row headers.
        Returns:
            iterable:
                The iterable that handles the pagination for the job.
            requests.Response:
                If ``return_json`` was set to ``True``, then a response
                object is instead returned instead of an iterable.
        Examples:
            >>> tio.v3.was.templates.search(filter=('netbios_name', 'eq',
            ...  'SCCM'), fields=['id', 'action', 'description'],
            ...    limit=2, sort=[('received': 'desc)])
        '''
        iclass = SearchIterator
        if kwargs.get('return_csv', False):
            iclass = CSVChunkIterator
        return super()._search(iterator_cls=iclass,
                               is_sort_with_prop=False,
                               api_path=f'{self._path}/search',
                               resource='items',
                               **kwargs
                               )
