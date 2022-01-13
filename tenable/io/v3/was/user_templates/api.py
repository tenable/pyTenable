'''
User-Templates
==============

The following methods allow for interaction into the Tenable.io
:devportal:`Web Application Scanning v3 user-templates <was-v2-templates>` API.

Methods available on ``tio.v3.was.user_templates``:

.. rst-class:: hide-signature
.. autoclass:: UserTemplatesAPI
    :members:
'''
from typing import Dict, Union
from uuid import UUID

from requests import Response

from tenable.io.v3.base.endpoints.explore import ExploreBaseEndpoint
from tenable.io.v3.base.iterators.explore_iterator import (CSVChunkIterator,
                                                           SearchIterator)
from tenable.io.v3.was.user_templates.schema import UserTemplateSchema
from tenable.utils import dict_clean, dict_merge


class UserTemplatesAPI(ExploreBaseEndpoint):
    '''
    This class contains all methods related to UserTemplates
    '''
    _path = 'api/v3/was/user-templates'
    _conv_json = True

    def delete(self, user_template_id: UUID) -> None:
        '''
        Deletes the specified user-defined template.

        :devportal:`was templates: Get user-defined template details
        <was-v2-user-templates-details>`
        Note:
            You cannot delete a user-defined template if scan configurations
            currently use the template. You must delete any scan configuration
            using the template prior to deleting the template. You can delete
            scan configurations with the DELETE /was/v2/configs/{config_id}
            endpoint.

        Args:
            user_template_id (UUID): The UUID of the user-defined template.

        Returns:
            :obj:`None`

        Examples:
            >>> (tio.v3.was.user_templates.
            ...     delete('d5b3cb1c-9c72-4974-a936-3dfbd2e2835e'))
        '''
        self._delete(f'{user_template_id}')

    def details(self, user_template_id: UUID) -> Dict:
        '''
        Returns details for a user-defined template. User-defined templates can
        be used to define scan configurations.

        :devportal:`was templates: Get user-defined template details
        <was-v2-user-templates-details>`

        Args:
            user_template_id (UUID): The UUID of the user-defined template.

        Returns:
            :obj:`dict`: The resource record of the user-defined template.

        Examples:
            >>> template = (tio.v3.was.user_templates.
            ...     details('d5b3cb1c-9c72-4974-a936-3dfbd2e2835e'))
            >>> pprint(template)
        '''
        return super()._details(user_template_id)

    def search(self, **kwargs) -> Union[SearchIterator,
                                        CSVChunkIterator,
                                        Response]:
        '''
        Search and retrieve the user templates based on supported conditions.

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
                the :py:meth:`tio.v3.was.user_templates.audit_log_filters()`
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
            >>> tio.v3.was.user_templates.search(filter=('netbios_name', 'eq',
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

    def update(self,
               user_template_id: UUID,
               **kwargs
               ) -> Dict:
        '''
        Updates the specified user-defined template.

        :devportal:`was templates: Update user-defined template
        <was-v2-user-templates-update>`

        Args:
            user_template_id (UUID): The UUID of the user-defined template.
            name (str, optional): The name of the user-defined template.
            owner_id (UUID, optional):
                The UUID of the owner of the user-defined template.
            default_permissions (str, optional):
                The scan permissions level, as described in Permissions.
            results_visibility (str, optional):
                The visibility of the results (private or dashboard).
            permissions (list, optional):
                The permissions for the user-defined template.
            description (str, optional):
                The description for the user-defined template.

        Returns:
            :obj:`dict`: The resource record of the user-defined template.

        Examples:
            >>> template = tio.v3.was.user_templates.update(
            ...     user_template_id = 'd5b3cb1c-9c72-4974-a936-3dfbd2e2835e',
            ...     name = 'template_1',
            ...     owner_id = '3fa85f64-5717-4562-b3fc-2c963f66afa6',
            ...     default_permissions = 'no_access',
            ...     results_visibility = 'dashboard',
            ...     permissions = [
            ...         {
            ...             'entity': 'user',
            ...             'entity_id':
            ...                 '3fa85f64-5717-4562-b3fc-2c963f66afa6',
            ...             'permissions_id':
            ...                 '3fa85f64-5717-4562-b3fc-2c963f66afa6',
            ...             'level': 'no_access'
            ...         }
            ...     ]
            ...     description = 'Template for containing threat'
            ... )
            >>> pprint(template)
        '''
        schema = UserTemplateSchema()
        payload = dict_clean(kwargs)
        payload = schema.dump(schema.load(payload))
        current_template = schema.dump(self.details(user_template_id))
        payload = dict_merge(current_template, payload)
        return self._put(f'{user_template_id}', json=payload)
