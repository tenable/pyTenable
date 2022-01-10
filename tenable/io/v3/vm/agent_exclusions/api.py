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
from datetime import datetime
from typing import Dict, Optional
from uuid import UUID

from restfly.utils import dict_clean, dict_merge

from tenable.io.v3.base.endpoints.explore import ExploreBaseEndpoint
from tenable.io.v3.vm.agent_exclusions.schema import AgentExclusionSchema


class AgentExclusionsAPI(ExploreBaseEndpoint):
    '''
    This class contains methods related to Agent Exclusions APIs
    '''
    _path: str = 'api/v3/agents'
    _conv_json: bool = True

    def create(self,
               name: str,
               start_time: str,
               end_time: Optional[str] = None,
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
            start_time (datetime): When the exclusion should start.
            end_time (datetime): When the exclusion should end.
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
            ...     start_time=(
            ...         datetime.utcnow()
            ...     ).strftime('%Y-%m-%dT%H:%M:%SZ'),
            ...     end_time=(
            ...         datetime.utcnow() + timedelta(hours=1)
            ...     ).strftime('%Y-%m-%dT%H:%M:%SZ')

            Creating a daily exclusion:

            >>> exclusion = tio.v3.vm.agent_exclusions.create(
            ...     name = 'Example Daily Agent Exclusion',
            ...     frequency='DAILY',
            ...     start_time=(
            ...         datetime.utcnow()
            ...     ).strftime('%Y-%m-%dT%H:%M:%SZ'),
            ...     end_time=(
            ...         datetime.utcnow() + timedelta(hours=1)
            ...     ).strftime('%Y-%m-%dT%H:%M:%SZ')

            Creating a weekly exclusion:

            >>> exclusion = tio.v3.vm.agent_exclusions.create(
            ...     name = 'Example Weekly Exclusion',
            ...     frequency='WEEKLY',
            ...     weekdays=['mo', 'we', 'fr'],
            ...     start_time=(
            ...         datetime.utcnow()
            ...     ).strftime('%Y-%m-%dT%H:%M:%SZ'),
            ...     end_time=(
            ...         datetime.utcnow() + timedelta(hours=1)
            ...     ).strftime('%Y-%m-%dT%H:%M:%SZ')

            Creating a monthly exclusion:

            >>> exclusion = tio.v3.vm.agent_exclusions.create(
            ...     name = 'Example Monthly Agent Exclusion',
            ...     frequency='MONTHLY',
            ...     day_of_month=1,
            ...     start_time=(
            ...         datetime.utcnow()
            ...     ).strftime('%Y-%m-%dT%H:%M:%SZ'),
            ...     end_time=(
            ...         datetime.utcnow() + timedelta(hours=1)
            ...     ).strftime('%Y-%m-%dT%H:%M:%SZ')

            Creating a yearly exclusion:

            >>> exclusion = tio.v3.vm.agent_exclusions.create(
            ...     name = 'Example Yearly Agent Exclusion',
            ...     frequency='YEARLY',
            ...     start_time=(
            ...         datetime.utcnow()
            ...     ).strftime('%Y-%m-%dT%H:%M:%SZ'),
            ...     end_time=(
            ...         datetime.utcnow() + timedelta(hours=1)
            ...     ).strftime('%Y-%m-%dT%H:%M:%SZ')
        '''
        payload: dict = {
            'name': name,
            'description': description,
            'schedule': {
                'enabled': enabled,
                'starttime': start_time,
                'endtime': end_time,
                'rrules': {}
            }
        }

        # Starting with the innermost part of the payload, lets construct the
        # rrules dictionary.
        rrules: dict = {
            'freq': frequency.upper(),
            'interval': interval,
        }

        # if the frequency is a weekly one, then we will need to
        # specify the days of the week that the exclusion is run on.
        if rrules['freq'] == 'WEEKLY':
            # In the same vein as the frequency check, we're accepting
            # case-insensitive input, comparing it to our known list of
            # acceptable responses, then joining them all together into a
            # comma-separated string.
            if weekdays is not None:
                rrules['byweekday'] = [
                    item.upper() for item in weekdays
                ]
            else:
                rrules['byweekday'] = [
                    'SU', 'MO', 'TU', 'WE', 'TH', 'FR', 'SA'
                ]

        # if the frequency is monthly, then we will need to specify
        # the day of the month that the rule will run on.
        if rrules['freq'] == 'MONTHLY':
            if day_of_month is not None:
                rrules['bymonthday'] = day_of_month
            else:
                rrules['bymonthday'] = datetime.today().day

        # Let's Add rrules dict to payload dict
        dict_merge(payload['schedule']['rrules'], rrules)

        # validate payload using marshmallow schema
        schema = AgentExclusionSchema()
        payload = schema.dump(schema.load(payload))

        return self._post(f'exclusions', json=payload)

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
        self._delete(f'exclusions/{exclusion_id}')

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
        return self._get(f'exclusions/{exclusion_id}')

    def edit(self,
             exclusion_id: UUID,
             name: Optional[str] = None,
             start_time: Optional[str] = None,
             end_time: Optional[str] = None,
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
            exclusion_id (UUID): The id of the exclusion object in Tenable.io
            name (str, optional): The name of the exclusion to create.
            start_time (datetime, optional): When the exclusion should start.
            end_time (datetime, optional): When the exclusion should end.
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
                'starttime': start_time,
                'endtime': end_time,
                'rrules': {
                    'freq': frequency,
                    'interval': interval
                }
            }
        }

        # Let's clean and Merge field dict to payload
        field_dict = dict_clean(field_dict)
        dict_merge(payload, field_dict)

        if payload['schedule']['enabled']:
            rrules = {
                'freq': payload['schedule']['rrules']['freq'],
                'interval': payload['schedule']['rrules']['interval'],
                'byweekday': None,
                'bymonthday': None,
            }

            rrules['freq'] = rrules['freq'].upper()

            # frequency default value is designed for weekly and
            # monthly based on below conditions
            # - if schedule rrules is not None and not defined in edit params,
            #   and byweekday/bymonthday key already exist, assign old values
            # - if schedule rrules is not None and not defined in edit params
            #   and byweekday/bymonthday key not already exist,
            #   assign default values
            # - if schedule rrules is not None and defined in edit params,
            # assign new values
            if rrules['freq'] == 'WEEKLY':
                if weekdays is not None:
                    rrules['byweekday'] = [
                        item.upper() for item in weekdays
                    ]
                else:
                    rrules['byweekday'] = payload['schedule']['rrules'].get(
                        'byweekday', 'SU,MO,TU,WE,TH,FR,SA'
                    ).split(',')
                # In the same vein as the frequency check, we're accepting
                # case-insensitive input, comparing it to our known list of
                # acceptable responses, then joining them all together into a
                # comma-separated string.
            elif rrules['freq'] == 'MONTHLY':
                if day_of_month is not None:
                    rrules['bymonthday'] = day_of_month
                else:
                    rrules['bymonthday'] = payload['schedule']['rrules'].get(
                        'bymonthday', datetime.today().day
                    )

            # Let's Merge rrules dict to payload
            dict_merge(payload['schedule']['rrules'], rrules)

        # Let's clean the payload
        payload = dict_clean(payload)

        # validate payload using marshmallow
        # let's remove addtional keys from payload
        schema = AgentExclusionSchema()
        payload = schema.dump(schema.load(payload))

        return self._put(f'exclusions/{exclusion_id}', json=payload)

    def search(self):
        raise NotImplementedError(
            'This method will be implemented later.'
        )
