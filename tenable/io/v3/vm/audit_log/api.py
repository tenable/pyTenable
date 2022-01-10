'''
Audit Log
=========

The following methods allow for interaction into the Tenable.io
:devportal:`audit log <audit-log>` API endpoints.

Methods available on ``tio.v3.vm.audit_log``:

.. rst-class:: hide-signature
.. autoclass:: AuditLogAPI
    :members:
'''
from typing import Union

from requests import Response

from tenable.io.v3.base.endpoints.explore import ExploreBaseEndpoint
from tenable.io.v3.vm.audit_log.iterator import (AuditLogCSVIterator,
                                                 AuditLogSearchIterator)


class AuditLogAPI(ExploreBaseEndpoint):
    '''
    This class contains all methods related to AuditLog
    '''
    _path = 'api/v3/audit-log/events'
    _conv_json = True

    def search(self,
               **kwargs
               ) -> Union[AuditLogSearchIterator,
                          AuditLogCSVIterator,
                          Response
                          ]:
        '''
        Search and retrieve the audit logs based on supported conditions.

        Args:
            fields (list, optional):
                The list of field names to return from the Tenable API.

                Example:
                    - ``['field1', 'field2']``
            filter (tuple, Dict, optional):
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
                the :py:meth:`tio.v3.vm.filters.audit_log_filters()`
                endpoint to get more details.
            sort (list[tuple], optional):
                A list of dictionaries describing how to sort the data
                that is to be returned.

                Examples:
                    - ``[('field_name_1', 'asc'),
                             ('field_name_2', 'desc')]``
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
            Iterable:
                The iterable that handles the pagination for the job.
            requests.Response:
                If ``return_json`` was set to ``True``, then a response
                object is instead returned instead of an iterable.

        Examples:
            >>> tio.v3.audit_log.search(filter=('netbios_name', 'eq',
            ...  'SCCM'), fields=['id', 'action', 'description'],
            ...    limit=2, sort=[('received': 'desc)])
        '''
        iclass = AuditLogSearchIterator
        if kwargs.get('return_csv', False):
            iclass = AuditLogCSVIterator
        return super().search(iterator_cls=iclass,
                              is_sort_with_prop=False,
                              api_path=f'{self._path}/search',
                              resource='events',
                              **kwargs
                              )
