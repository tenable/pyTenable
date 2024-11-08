'''
AD Object
=============

Methods described in this section relate to the ad object API.
These methods can be accessed at ``TenableIE.ad_object``.

.. rst-class:: hide-signature
.. autoclass:: ADObjectAPI
    :members:
'''
from typing import List, Dict, Mapping
from restfly.utils import dict_clean
from tenable.ie.ad_object.schema import ADObjectSchema, ADObjectChangesSchema
from tenable.ie.base.iterator import ADIterator
from tenable.base.endpoint import APIEndpoint


class ADObjectIterator(ADIterator):
    '''
    The ad object iterator provides a scalable way to work through alert list
    result sets of any size. The iterator will walk through each page of data,
    returning one record at a time. If it reaches the end of a page of
    records, then it will request the next page of information and then
    continue to return records from the next page (and the next, and the next)
    until the counter reaches the total number of records that the API has
    reported.
    '''


class ADObjectAPI(APIEndpoint):
    _schema = ADObjectSchema()

    def details(self,
                directory_id: str,
                infrastructure_id: str,
                ad_object_id: str
                ) -> Dict:
        '''
        Retrieves the details of a specific AD object.

        Args:
            directory_id (str):
                The directory instance identifier.
            infrastructure_id (str):
                The infrastructure instance identifier.
            ad_object_id (str):
                The AD Object identifier.

        Returns:
            dict:
                The AD object.

        Examples:
            >>> tie.ad_object.details(
            ...     directory_id='1',
            ...     infrastructure_id='1',
            ...     ad_object_id='1'
            ...     )
        '''
        return self._schema.load(
            self._api.get(f"infrastructures/{infrastructure_id}/"
                          f"directories/{directory_id}/"
                          f"ad-objects/{ad_object_id}"))

    def details_by_profile_and_checker(self,
                                       profile_id: str,
                                       checker_id: str,
                                       ad_object_id: str
                                       ) -> Dict:
        '''
        Retrieves an AD object details by id that have deviances for a
        specific profile and checker

        Args:
            profile_id (str):
                The profile instance identifier.
            checker_id (str):
                The checker instance identifier.
            ad_object_id (str):
                The AD Object identifier.

        Returns:
            dict:
                The AD object.

        Examples:
            >>> tie.ad_object.details_by_profile_and_checker(
            ...     profile_id='1',
            ...     checker_id='1',
            ...     ad_object_id='1'
            ...     )
        '''
        return self._schema.load(
            self._api.get(f"profiles/{profile_id}/"
                          f"checkers/{checker_id}/"
                          f"ad-objects/{ad_object_id}"))

    def details_by_event(self,
                         directory_id: str,
                         infrastructure_id: str,
                         ad_object_id: str,
                         event_id: str
                         ) -> Dict:
        '''
        Retrieves the details of a specific AD object.

        Args:
            directory_id (str):
                The directory instance identifier.
            infrastructure_id (str):
                The infrastructure instance identifier.
            ad_object_id (str):
                The AD Object identifier.
            event_id (str):
                The event identifier.

        Returns:
            dict:
                The AD object.

        Examples:
            >>> tie.ad_object.details_by_event(
            ...     directory_id='1',
            ...     infrastructure_id='1',
            ...     ad_object_id='1',
            ...     event_id='1'
            ...     )
        '''
        return self._schema.load(
            self._api.get(f"infrastructures/{infrastructure_id}/"
                          f"directories/{directory_id}/"
                          f"events/{event_id}/"
                          f"ad-objects/{ad_object_id}"))

    def get_changes(self,
                    directory_id: str,
                    infrastructure_id: str,
                    ad_object_id: str,
                    event_id: str,
                    **kwargs
                    ) -> List[Dict]:
        '''
        Get the AD object changes between a given event and event which
        precedes it.

        Args:
            directory_id (str):
                The directory instance identifier.
            infrastructure_id (str):
                The infrastructure instance identifier.
            ad_object_id (str):
                The AD Object identifier.
            event_id (str):
                The event identifier.
            wanted_values (optional, list[str]):
                Which values user wants to include. ``before`` to include the
                values just before the event, ``after`` to include the values
                just after the event or ``current`` to include the current
                values.

        Returns:
            list[dict]:
                The list of AD objects.

        Examples:
            >>> tie.ad_object.get_changes(
            ...     directory_id='1',
            ...     infrastructure_id='1',
            ...     ad_object_id='1',
            ...     event_id='1',
            ...     wanted_values=['current', 'after']
            ...     )
        '''
        schema = ADObjectChangesSchema()
        params = self._schema.dump(self._schema.load(kwargs))
        return schema.load(
            self._api.get(f"infrastructures/{infrastructure_id}/"
                          f"directories/{directory_id}/"
                          f"events/{event_id}/"
                          f"ad-objects/{ad_object_id}/changes", params=params),
            many=True)

    def search_all(self,
                   profile_id: str,
                   checker_id: str,
                   expression: Mapping,
                   directories: List[int],
                   reasons: List[int],
                   show_ignored: bool,
                   **kwargs
                   ) -> ADObjectIterator:
        '''
        Search all AD objects having deviances by profile by checker

        Args:
            profile_id (str):
                The profile instance identifier.
            checker_id (str):
                The checker instance identifier.
            expression (mapping):
                An object describing a filter for searched items.
            directories (list[int]):
                The list of directory instance identifiers.
            reasons (list[int]):
                The list of reasons identifiers.
            show_ignored (bool):
                Whether AD Object that only have ignored deviances should be
                included?
            date_start (optional, str):
                The date after which the AD object deviances should have been
                emitted.
            date_end (optional, str):
                The date before which the AD object deviances should have been
                emitted.
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
            :obj:`ADObjectIterator`:
                An iterator that handles the page management of the requested
                records.

        Examples:
            >>> for ado in tie.ad_object.search_all(
            ...     profile_id='1',
            ...     checker_id='1',
            ...     show_ignored=False,
            ...     reasons=[1, 2],
            ...     directories=[1],
            ...     expression={'OR': [{
            ...         'whencreated': '2021-07-29T12:27:50.0000000Z'
            ...     }]},
            ...     date_end='2022-12-31T18:30:00.000Z',
            ...     date_start='2021-12-31T18:30:00.000Z',
            ...     page=1,
            ...     per_page=20,
            ...     max_pages=10,
            ...     max_items=200
            ...     ):
            ...     pprint(ado)
        '''
        params = self._schema.dump(self._schema.load({
            'page': kwargs.get('page') or 1,
            'perPage': kwargs.get('per_page'),
            'maxItems': kwargs.get('max_items'),
            'maxPages': kwargs.get('max_pages')
        }))

        payload = self._schema.dump(self._schema.load(
            dict_clean({
                'expression': expression,
                'directories': directories,
                'reasons': reasons,
                'dateStart': kwargs.get('date_start'),
                'dateEnd': kwargs.get('date_end'),
                'showIgnored': show_ignored
            })
        ))

        return ADObjectIterator(
            api=self._api,
            _path=f'profiles/{profile_id}/'
                  f'checkers/{checker_id}/'
                  f'ad-objects/search',
            _method='post',
            num_pages=params.get('page'),
            _per_page=params.get('perPage'),
            _query=params,
            _payload=payload,
            _schema=self._schema,
            max_pages=params.pop('maxPages', None),
            max_items=params.pop('maxItems', None)
        )
