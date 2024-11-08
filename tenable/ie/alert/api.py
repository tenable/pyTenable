'''
Alerts
=============

Methods described in this section relate to the alerts API.
These methods can be accessed at ``TenableIE.alerts``.

.. rst-class:: hide-signature
.. autoclass:: AlertsAPI
    :members:
'''
from typing import List, Dict
from tenable.ie.alert.schema import AlertSchema, AlertParamsSchema
from tenable.ie.base.iterator import ADIterator
from tenable.base.endpoint import APIEndpoint


class AlertIterator(ADIterator):
    '''
    The alert iterator provides a scalable way to work through alert list
    result sets of any size. The iterator will walk through each page of data,
    returning one record at a time. If it reaches the end of a page of
    records, then it will request the next page of information and then
    continue to return records from the next page (and the next, and the next)
    until the counter reaches the total number of records that the API has
    reported.
    '''


class AlertsAPI(APIEndpoint):
    _path = 'alerts'
    _schema = AlertSchema()

    def list_by_profile(self,
                        profile_id: str,
                        **kwargs
                        ) -> AlertIterator:
        '''
        Retrieve all alert instances

        Args:
            profile_id (str):
                The profile instance identifier.
            archived (optional, bool):
                is alert archived?
            read (optional, bool):
                is alert read?
            page (optional, int):
                The page number user wants to retrieve.
            per_page (optional, int):
                The number of records per page user wants to retrieve.
            max_items (optional, int):
                The maximum number of records to return before
                stopping iteration.
            max_pages (optional, int):
                The maximum number of pages to request before throwing
                stopping iteration.

        Returns:
            :obj:`AlertIterator`:
                An iterator that handles the page management of the requested
                records.

        Examples:
            >>> for alert in tie.alerts.list_by_profile(
            ...     profile_id='1',
            ...     archived=False,
            ...     read=False,
            ...     page=1,
            ...     per_page=20,
            ...     max_pages=10,
            ...     max_items=200
            ...     ):
            ...     pprint(alert)
        '''
        schema = AlertParamsSchema()
        params = schema.dump(self._schema.load(kwargs))

        return AlertIterator(
            api=self._api,
            _path=f'profiles/{profile_id}/alerts',
            num_pages=params.get('page'),
            _per_page=params.get('perPage'),
            _query=params,
            _schema=schema,
            max_pages=params.pop('maxPages', None),
            max_items=params.pop('maxItems', None)
        )

    def details(self,
                alert_id: str
                ) -> Dict:
        '''
        Retrieves the details of a specific alert.

        Args:
            alert_id (str):
                The alert instance identifier.

        Returns:
            dict:
                the alert object.

        Examples:
            >>> tie.alerts.details(
            ...     alert_id='1'
            ...     )
        '''
        return self._schema.load(self._get(f"{alert_id}"))

    def update(self,
               alert_id: str,
               **kwargs
               ) -> Dict:
        '''
        Update alert instance

        Args:
            alert_id (str):
                The alert instance identifier.
            archived (optional, bool):
                is alert archived?
            read (optional, bool):
                is alert read?

        Returns:
            dict:
                The updated alert object.

        Example:
            >>> tie.alerts.update(
            ...     alert_id='1',
            ...     archived=False,
            ...     read=False
            ...     )
        '''
        payload = self._schema.dump(self._schema.load(kwargs))
        return self._schema.load(self._patch(f"{alert_id}", json=payload))

    def update_on_profile(self,
                          profile_id: str,
                          **kwargs
                          ) -> None:
        '''
        Update alerts for one profile

        Args:
            profile_id (str):
                The alert instance identifier.
            archived (optional, bool):
                is alert archived?
            read (optional, bool):
                is alert read?

        Returns:
            None:

        Example:
            >>> tie.alerts.update_on_profile(
            ...     profile_id='1',
            ...     archived=False,
            ...     read=False
            ...     )
        '''
        payload = self._schema.dump(self._schema.load(kwargs))
        self._api.patch(f"profiles/{profile_id}/alerts", json=payload)
