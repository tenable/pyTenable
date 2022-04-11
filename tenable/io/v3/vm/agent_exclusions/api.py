'''
Agent Exclusions
================

The following methods allow for interaction into the Tenable.io
:devportal:`agent exclusions <agent-exclusions>` API endpoints.

Methods available on ``tio.v3.vm.agent_exclusions``:

.. rst-class:: hide-signature
.. autoclass:: AgentExclusionsAPI
    :members:
'''
from typing import Dict, Optional, Union
from uuid import UUID

from requests import Response

from tenable.io.v3.base.endpoints.explore import ExploreBaseEndpoint
from tenable.io.v3.base.iterators.explore_iterator import (CSVChunkIterator,
                                                           SearchIterator)
from tenable.io.v3.vm.agent_exclusions.schema import AgentExclusionSchema
from tenable.utils import dict_clean, dict_merge


class AgentExclusionsAPI(ExploreBaseEndpoint):
    '''
    This class contains methods related to Agent Exclusions APIs
    '''
    _path: str = 'api/v3/agents/exclusions'
    _conv_json: bool = True

    def create(self,
               name: str,
               start_time: str,
               end_time: Optional[str] = None,
               timezone: Optional[str] = 'UTC',
               description: Optional[str] = None,
               frequency: Optional[str] = 'ONETIME',
               interval: Optional[int] = 1,
               weekdays: Optional[list] = None,
               day_of_month: Optional[int] = None,
               enabled: Optional[bool] = True,
               ) -> Dict:
        '''
        Creates a new agent exclusion.

        :devportal:`agent-exclusions: create <agent-exclusions-create>`

        Args:
            name (str): The name of the exclusion to create.
            start_time (str): When the exclusion should start.
            end_time (str): When the exclusion should end.
            timezone (str, optional):
                The timezone to use for the exclusion.  The default if none is
                specified is to use UTC.  For the list of usable timezones,
                please refer to:
                https://cloud.tenable.com/api#/resources/scans/timezones
            description (str, optional):
                Some further detail about the exclusion.
            frequency (str, optional):
                The frequency of the rule. The string inputted will be
                up-cased. Valid values are:``ONETIME``, ``DAILY``, ``WEEKLY``,
                ``MONTHLY``, ``YEARLY``.
                Default value is ``ONETIME``.
            interval (int, optional):
                The interval of the rule.  The default interval is 1
            weekdays (list, optional):
                List of 2-character representations of the days of the week to
                repeat the frequency rule on.  Valid values are:
                *SU, MO, TU, WE, TH, FR, SA*
                Default values: ``['SU', 'MO', 'TU', 'WE', 'TH', 'FR', 'SA']``
            day_of_month (int, optional):
                The day of the month to repeat a **MONTHLY** frequency rule on.
                The default is today.
            enabled (bool, optional):
                enable/disable exclusion. The default is ``True``

        Returns:
            dict: Dictionary of the newly minted exclusion.

        Examples:
            Creating a one-time exclusion:

            >>> from datetime import datetime, timedelta
            >>> exclusion = tio.v3.vm.agent_exclusions.create(
            ...     name = 'Example One-Time Agent Exclusion',
            ...     frequency = 'ONETIME',
            ...     start_time=datetime.utcnow(),
            ...     end_time=datetime.utcnow() + timedelta(hours=1))

            Creating a daily exclusion:

            >>> exclusion = tio.v3.vm.agent_exclusions.create(
            ...     name = 'Example Daily Agent Exclusion',
            ...     frequency='DAILY',
            ...     start_time=datetime.utcnow(),
            ...     end_time=datetime.utcnow() + timedelta(hours=1))

            Creating a weekly exclusion:

            >>> exclusion = tio.v3.vm.agent_exclusions.create(
            ...     name = 'Example Weekly Exclusion',
            ...     frequency='WEEKLY',
            ...     weekdays=['mo', 'we', 'fr'],
            ...     start_time=datetime.utcnow(),
            ...     end_time=datetime.utcnow() + timedelta(hours=1))

            Creating a monthly exclusion:

            >>> exclusion = tio.v3.vm.agent_exclusions.create(
            ...     name = 'Example Monthly Agent Exclusion',
            ...     frequency='MONTHLY',
            ...     day_of_month=1,
            ...     start_time=datetime.utcnow(),
            ...     end_time=datetime.utcnow() + timedelta(hours=1))

            Creating a yearly exclusion:

            >>> exclusion = tio.v3.vm.agent_exclusions.create(
            ...     name = 'Example Yearly Agent Exclusion',
            ...     frequency='YEARLY',
            ...     start_time=datetime.utcnow(),
            ...     end_time=datetime.utcnow() + timedelta(hours=1))
        '''
        # Let's create the payload
        payload: dict = {
            'name': name,
            'description': description,
            'schedule': {
                'enabled': enabled,
                'starttime': start_time,
                'endtime': end_time,
                'timezone': timezone,
                'rrules': {
                    'freq': frequency,
                    'interval': interval,
                    'byweekday': weekdays,
                    'bymonthday': day_of_month
                }
            }
        }
        payload = dict_clean(payload)
        # validate payload using marshmallow schema
        schema = AgentExclusionSchema(
            context={'timezones': self._api.v3.vm.scans.timezones()}
        )
        payload = schema.dump(schema.load(payload))
        return self._post(json=payload)

    def delete(self, exclusion_id: UUID) -> None:
        '''
        Delete an agent exclusion.

        :devportal:`agent-exclusions: delete <agent-exclusions-delete>`

        Args:
            exclusion_id (str): The id of the exclusion object in Tenable.io

        Returns:
            None: The Exclusion was successfully deleted

        Examples:
            >>> tio.v3.vm.agent_exclusions.delete(
            ...     exclusion_id = '00000000-0000-0000-0000-000000000000'
            ... )
        '''
        self._delete(f'{exclusion_id}')

    def details(self, exclusion_id: UUID) -> Dict:
        '''
        Retrieve the details for a specific agent exclusion.

        :devportal:`agent-exclusion: details <agent-exclusions-details>`

        Args:
            exclusion_id (int): The id of the exclusion object in Tenable.io

        Returns:
            dict: The exclusion resource dictionary.

        Examples:
            >>> exclusion = tio.v3.vm.agent_exclusions.details(
            ...     exclusion_id = '00000000-0000-0000-0000-000000000000'
            ... )
        '''
        return super()._details(exclusion_id)

    def edit(self,
             exclusion_id: UUID,
             name: Optional[str] = None,
             start_time: Optional[str] = None,
             end_time: Optional[str] = None,
             timezone: Optional[str] = None,
             description: Optional[str] = None,
             frequency: Optional[str] = None,
             interval: Optional[int] = None,
             weekdays: Optional[list] = None,
             day_of_month: Optional[int] = None,
             enabled: Optional[bool] = None,
             ) -> Dict:
        '''
        Edit an existing agent exclusion.

        :devportal:`agent-exclusions: edit <agent-exclusions-edit>`

        The edit function will first gather the details of the exclusion that
        will be edited and will overlay the changes on top.  The result will
        then be pushed back to the API to modify the exclusion.

        Args:
            exclusion_id (uuid.UUID): The id of the exclusion object in Tenable.io
            name (str, optional): The name of the exclusion to create.
            start_time (datetime, optional): When the exclusion should start.
            end_time (datetime, optional): When the exclusion should end.
            timezone (str, optional):
                The timezone to use for the exclusion.  The default if none is
                specified is to use UTC.
            description (str, optional):
                Some further detail about the exclusion.
            frequency (str, optional):
                The frequency of the rule.
                The string inputted will be up-cased.
                Valid values are: *ONETIME, DAILY, WEEKLY, MONTHLY, YEARLY*.
            interval (int, optional): The interval of the rule.
            weekdays (list, optional):
                List of 2-character representations of the days of the week to
                repeat the frequency rule on.  Valid values are:
                *SU, MO, TU, WE, TH, FR, SA*
                Default values: ``['SU', 'MO', 'TU', 'WE', 'TH', 'FR', 'SA']``
            day_of_month (int, optional):
                The day of the month to repeat a **MONTHLY** frequency rule on.
            enabled (bool, optional):
                enable/disable exclusion.

        Returns:
            dict: Dictionary of the newly minted exclusion.

        Examples:
            >>> exclusion = tio.v3.vm.agent_exclusions.edit(
            ...     exclusion_id = '00000000-0000-0000-0000-000000000000',
            ...     name='New Name'
            ... )
        '''

        # Lets start constructing the payload to be sent to the API...
        payload = self.details(exclusion_id=exclusion_id)

        unwanted_keys = [
            'id',
            'creation_date',
            'last_modification_date',
            'core_updates_blocked'
        ]
        for key in unwanted_keys:
            payload.pop(key, None)

        field_dict: dict = {
            'name': name,
            'description': description,
            'schedule': {
                'enabled': enabled,
            }
        }

        # Let's clean and Merge field dict to payload
        field_dict = dict_clean(field_dict)
        dict_merge(payload, field_dict)

        if payload['schedule']['enabled']:
            schedule_dict: dict = {
                'starttime': start_time,
                'endtime': end_time,
                'timezone': timezone,
                'rrules': {
                    'freq': frequency,
                    'interval': interval,
                    'byweekday': weekdays,
                    'bymonthday': day_of_month
                }
            }
            schedule_dict = dict_clean(schedule_dict)
            dict_merge(payload['schedule'], schedule_dict)

        payload['schedule']['starttime'] = (
            payload['schedule']['starttime'].replace('T', ' ')
        ).replace(payload['schedule']['starttime'][-6:], '')

        payload['schedule']['endtime'] = (
            payload['schedule']['endtime'].replace('T', ' ')
        ).replace(payload['schedule']['endtime'][-6:], '')

        # validate payload using marshmallow
        schema = AgentExclusionSchema(
            context={'timezones': self._api.v3.vm.scans.timezones()}
        )
        payload = schema.dump(schema.load(payload))
        return self._put(f'{exclusion_id}', json=payload)

    def search(self,
               **kwargs) -> Union[SearchIterator, CSVChunkIterator, Response]:
        '''
        Search agent exclusions based on supported conditions.
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
                the :py:meth:`tio.v3.definitions.vm.agent_exclusions()`
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
            >>> tio.v3.vm.agent_exclusions.search(
            ...     fields=['id', 'name'],
            ...     filter=('id', 'eq', [1,2]),
            ...     sort=[('id', 'asc')],
            ...     limit=10
            ... )
        '''
        iclass = SearchIterator

        if kwargs.get('return_csv', False):
            iclass = CSVChunkIterator

        return super()._search(
            iterator_cls=iclass,
            sort_type=self._sort_type.default,
            api_path=f'{self._path}/search',
            resource='exclusions',
            **kwargs
        )
