'''
Event
=====
Methods described in this section relate to the the event API.
These methods can be accessed at ``TenableIE.event``.

.. rst-class:: hide-signature
.. autoclass:: EventAPI
    :members:
'''
from typing import Dict, List, Mapping
from restfly.utils import dict_clean
from tenable.ie.event.schema import EventSchema
from tenable.base.endpoint import APIEndpoint


class EventAPI(APIEndpoint):
    _schema = EventSchema()
    _path = 'events'

    def details(self,
                event_id: str,
                infrastructure_id: str,
                directory_id: str
                ) -> Dict:
        '''
        Retrieves the details of specific event instance.

        Args:
            event_id (str):
                The event instance identifier.
            infrastructure_id (str):
                The infrastructure instance identifier.
            directory_id (str):
                The directory instance identifier.

        Returns:
            dict:
                Details of the event object.

        Examples:
            >>> tie.event.details(
            ...     event_id='1',
            ...     infrastructure_id='1',
            ...     directory_id='1'
            ...     )

        '''
        return self._schema.load(
            self._api.get(f'infrastructures/{infrastructure_id}/directories'
                          f'/{directory_id}/events/{event_id}'))

    def search_events(self,
                      expression: Mapping,
                      profile_id: int,
                      date_start: str,
                      date_end: str,
                      directory_ids: List[int],
                      **kwargs
                      ) -> List[Dict]:
        '''
        Searches the events.

        Args:
            expression (mapping):
                An object describing a filter for searched items.
            profile_id (int):
                The profile instance identifier.
            date_start (str):
                The starting date from where the events are expected.
            date_end (str):
                The date till which the events are expected.
            directory_ids (List[int]):
                List of directory instance identifiers.
            order (optional, str):
                The desired sorting order of the event identifier. Default
                is ``desc``

        Returns:
            list[dict]:
                The search result object.

        Examples:

            >>> tie.event.search_events(
            ...     expression={'AND': [{'systemOnly': 'True'}]},
            ...     profile_id=5,
            ...     date_start='2022-01-05T00:00:00.000Z',
            ...     date_end='2022-01-12T23:59:59.999Z',
            ...     directory_ids=[1,2,3],
            ...     order='asc'
            ...     )

        '''
        payload = self._schema.dump(self._schema.load(
            dict_clean({
                'expression': expression,
                'profileId': profile_id,
                'dateStart': date_start,
                'dateEnd': date_end,
                'directoryIds': directory_ids,
                'order': dict(column='id', direction=kwargs.get('order'))
            })
        ))
        return self._schema.load(self._post('search', json=payload),
                                 many=True)
