'''
Templates
=========

The following methods allow for interaction into the Tenable.io
:devportal:`Web Application Scanning v3 templates
<was-v2-templates>` API endpoints.

Methods available on ``tio.v3.was.templates``:

.. rst-class:: hide-signature
.. autoclass:: TemplatesAPI
    :members:
'''
from typing import Dict, Union
from uuid import UUID

from requests import Response

from tenable.io.v3.base.endpoints.explore import ExploreBaseEndpoint
from tenable.io.v3.base.iterators.was_iterator import (CSVChunkIterator,
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
            template_id (uuid.UUID):
                The UUID of the Tenable-provided template resource.

        Returns:
            :obj:`dict`: The resource record of the template.

        Examples:
            >>> template = (tio.v3.was.templates.
            ...     details('d5b3cb1c-9c72-4974-a936-3dfbd2e2835e'))
            >>> pprint(template)
        '''
        return super()._details(template_id)

    def search(self, **kwargs) -> Union[CSVChunkIterator,
                                        Response,
                                        SearchIterator]:
        '''
        Search and retrieve the teamplates based on supported conditions.

        Args:
            fields (list, optional):
                The list of field names to return from the Tenable API.
                Examples:
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
                the :py:meth: `tio.v3.definitions.was.configurations()`
                endpoint to get more details.
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
            >>> tio.v3.was.templates.search(
            ...     filter=('type', 'eq','private'),
            ...     fields=['unread_count', 'name', 'id'],
            ...     limit=2,
            ...     sort=[('name', 'desc')]
            ... )
        '''
        iclass = SearchIterator
        if kwargs.get('return_csv', False):
            iclass = CSVChunkIterator
        return super()._search_was(
            resource='items',
            iterator_cls=iclass,
            sort_type=self._sort_type.name_based,
            api_path=f'{self._path}/search',
            **kwargs
        )
