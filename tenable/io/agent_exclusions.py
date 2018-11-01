'''
agent_exclusions
================

The following methods allow for interaction into the Tenable.io 
`agent exclusions <https://cloud.tenable.com/api#/resources/agent-exclusions>`_
API endpoints.

Methods available on ``tio.agent_exclusions``:

.. rst-class:: hide-signature
.. autoclass:: AgentExclusionsAPI

    .. automethod:: create
    .. automethod:: delete
    .. automethod:: details
    .. automethod:: edit
    .. automethod:: list
'''
from .base import TIOEndpoint
from datetime import date, datetime

class AgentExclusionsAPI(TIOEndpoint):
    def create(self, name, scanner_id=1, start_time=None, end_time=None, 
               timezone=None, description=None, frequency=None, 
               interval=None, weekdays=None, day_of_month=None,
               enabled=True):
        '''
        Creates a new agent exclusion.

        `agent-exclusions: create <https://cloud.tenable.com/api#/resources/agent-exclusions/create>`_

        Args:
            name (str): The name of the exclusion to create.
            scanner_id (int, optional): The scanner id.
            description (str, optional): 
                Some further detail about the exclusion.
            start_time (datetime): When the exclusion should start.
            end_time (datetime): When the exclusion should end.
            timezone (str, optional): 
                The timezone to use for the exclusion.  The default if none is 
                specified is to use UTC.  For the list of usable timezones,
                please refer to:
                https://cloud.tenable.com/api#/resources/scans/timezones
            frequency (str, optional):
                The frequency of the rule. The string inputted will be up-cased.
                Valid values are: ``ONETIME``, ``DAILY``, ``WEEKLY``, 
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
                Is the exclusion enabled?  The default is ``True``

        Returns:
            dict: Dictionary of the newly minted exclusion.

        Examples:
            Creating a one-time exclusion:

            >>> from datetime import datetime, timedelta
            >>> exclusion = tio.agent_exclusions.create(
            ...     'Example One-Time Agent Exclusion',
            ...     ['127.0.0.1'],
            ...     start_time=datetime.utcnow(),
            ...     end_time=datetime.utcnow() + timedelta(hours=1))

            Creating a daily exclusion:

            >>> exclusion = tio.agent_exclusions.create(
            ...     'Example Daily Agent Exclusion',
            ...     ['127.0.0.1'],
            ...     frequency='daily',
            ...     start_time=datetime.utcnow(),
            ...     end_time=datetime.utcnow() + timedelta(hours=1))

            Creating a weekly exclusion:

            >>> exclusion = tio.agent_exclusions.create(
            ...     'Example Weekly Exclusion',
            ...     ['127.0.0.1'],
            ...     frequency='weekly',
            ...     weekdays=['mo', 'we', 'fr'],
            ...     start_time=datetime.utcnow(),
            ...     end_time=datetime.utcnow() + timedelta(hours=1))

            Creating a monthly esxclusion:

            >>> exclusion = tio.agent_exclusions.create(
            ...     'Example Monthly Agent Exclusion',
            ...     ['127.0.0.1'],
            ...     frequency='monthly',
            ...     day_of_month=1,
            ...     start_time=datetime.utcnow(),
            ...     end_time=datetime.utcnow() + timedelta(hours=1))

            Creating a yearly exclusion:

            >>> exclusion = tio.agent_exclusions.create(
            ...     'Example Yearly Agent Exclusion',
            ...     ['127.0.0.1'],
            ...     frequency='yearly',
            ...     start_time=datetime.utcnow(),
            ...     end_time=datetime.utcnow() + timedelta(hours=1)) 
        '''
        # Starting with the innermost part of the payload, lets construct the
        # rrules dictionary.
        frequency = self._check('frequency', frequency, str, 
            choices=['ONETIME', 'DAILY', 'WEEKLY', 'MONTHLY', 'YEARLY'],
            default='ONETIME', 
            case='upper')

        rrules = {
            'freq': frequency,
            'interval': self._check('interval', interval, int, default=1)
        }

        # if the frequency is a weekly one, then we will need to specify the
        # days of the week that the exclusion is run on.
        if frequency == 'WEEKLY':
            rrules['byweekday'] = ','.join(self._check(
                'weekdays', weekdays, list,
                choices=['SU', 'MO', 'TU', 'WE', 'TH', 'FR', 'SA'],
                default=['SU', 'MO', 'TU', 'WE', 'TH', 'FR', 'SA'],
                case='upper'))
            # In the same vein as the frequency check, we're accepting
            # case-insensitive input, comparing it to our known list of
            # acceptable responses, then joining them all together into a 
            # comma-separated string.

        # if the frequency is monthly, then we will need to specify the day of
        # the month that the rule will run on.
        if frequency == 'MONTHLY':
            rrules['bymonthday'] = self._check('day_of_month', day_of_month, int,
                choices=list(range(1,32)),
                default=datetime.today().day)

        # Next we need to construct the rest of the payload
        payload = {
            'name': self._check('name', name, str),
            'description': self._check('description', description, str, default=''),
            'schedule': {
                'enabled': self._check('enabled', enabled, bool, default=True),
                'starttime': self._check('start_time', start_time, datetime).strftime('%Y-%m-%d %H:%M:%S'),
                'endtime': self._check('end_time', end_time, datetime).strftime('%Y-%m-%d %H:%M:%S'),
                'timezone': self._check('timezone', timezone, str, 
                    choices=self._api._tz,
                    default='Etc/UTC'),
                'rrules': rrules
            }
        }

        # Lets check to make sure that the scanner_id is an integer as the API
        # documentation requests and if we don't raise an error, then lets make
        # the call.
        return self._api.post(
            'scanners/{}/agents/exclusions'.format(
                self._check('scanner_id', scanner_id, int)
            ), json=payload).json()

    def delete(self, exclusion_id, scanner_id=1):
        '''
        Delete an agent exclusion.

        `agent-exclusions: delete <https://cloud.tenable.com/api#/resources/agent-exclusions/delete>`_

        Args:
            exclusion_id (int): The id of the exclusion object in Tenable.io
            scanner_id (int, optional): The id of the scanner

        Returns:
            None: The Exclusion was successfully deleted

        Examples:
            >>> tio.agent_exclusions.delete(1)
        '''
        self._api.delete('scanners/{}/agents/exclusions/{}'.format(
            self._check('scanner_id', scanner_id, int),
            self._check('exclusion_id', exclusion_id, int)
        ))

    def details(self, exclusion_id, scanner_id=1):
        '''
        Retrieve the details for a specific agent exclusion.

        `agent-exclusion: details <https://cloud.tenable.com/api#/resources/agent-exclusions/details>`_

        Args:
            exclusion_id (int): The id of the exclusion object in Tenable.io
            scanner_id (int, optional): The id of the scanner

        Returns:
            dict: The exclusion resource dictionary.

        Examples:
            >>> exclusion = tio.agent_exclusions.details(1)
        '''
        return self._api.get(
            'scanners/{}/agents/exclusions/{}'.format(
                self._check('scanner_id', scanner_id, int),
                self._check('exclusion_id', exclusion_id, int)
            )).json()

    def edit(self, exclusion_id, scanner_id=1, name=None, start_time=None, 
            end_time=None, timezone=None, description=None, frequency=None, 
            interval=None, weekdays=None, day_of_month=None, enabled=None):
        '''
        Edit an existing agent exclusion.

        `agent-exclusions: edit <https://cloud.tenable.com/api#/resources/agent-exclusions/edit>`_

        The edit function will first gather the details of the exclusion that
        will be edited and will overlay the changes on top.  The result will
        then be pushed back to the API to modify the exclusion.

        Args:
            exclusion_id (int): The id of the exclusion object in Tenable.io
            scanner_id (int, optional): The scanner id.
            name (str, optional): The name of the exclusion to create.
            description (str, optional): 
                Some further detail about the exclusion.
            start_time (datetime, optional): When the exclusion should start.
            end_time (datetime, optional): When the exclusion should end.
            timezone (str, optional): 
                The timezone to use for the exclusion.  The default if none is 
                specified is to use UTC.
            frequency (str, optional):
                The frequency of the rule. The string inputted will be up-cased.
                Valid values are: *ONETIME, DAILY, WEEKLY, MONTHLY, YEARLY*.
            interval (int, optional): The interval of the rule.
            weekdays (list, optional):
                List of 2-character representations of the days of the week to
                repeat the frequency rule on.  Valid values are:
                *SU, MO, TU, WE, TH, FR, SA*
                Default values: ``['SU', 'MO', 'TU', 'WE', 'TH', 'FR', 'SA']``
            day_of_month (int, optional):
                The day of the month to repeat a **MONTHLY** frequency rule on.

        Returns:
            dict: Dictionary of the newly minted exclusion.

        Examples:
            >>> exclusion = tio.agent_exclusions.edit(1, name='New Name')
        '''

        # Lets start constructing the payload to be sent to the API...
        payload = self.details(exclusion_id, scanner_id=scanner_id)

        if name:
            payload['name'] = self._check('name', name, str)

        if description:
            payload['description'] = self._check('description', description, str)

        if enabled is not None:
            payload['schedule']['enabled'] = self._check('enabled', enabled, bool)

        if start_time:
            payload['schedule']['starttime'] = self._check(
                'start_time', start_time, datetime).strftime('%Y-%m-%d %H:%M:%S')

        if end_time:
            payload['schedule']['endtime'] = self._check(
                'end_time', end_time, datetime).strftime('%Y-%m-%d %H:%M:%S')

        if timezone:
            payload['schedule']['timezone'] = self._check(
                'timezone', timezone, str, choices=self._api._tz)

        if frequency:
            payload['schedule']['rrules']['freq'] = self._check(
                'frequency', frequency, str, 
                choices=['ONETIME', 'DAILY', 'WEEKLY', 'MONTHLY', 'YEARLY'],
                case='upper')

        if interval:
            payload['schedule']['rrules']['interval'] = self._check(
                'interval', interval, int)

        if weekdays:
            payload['schedule']['rrules']['byweekday'] = ','.join(self._check(
                'weekdays', weekdays, list,
                choices=['SU', 'MO', 'TU', 'WE', 'TH', 'FR', 'SA'],
                case='upper'))
            # In the same vein as the frequency check, we're accepting
            # case-insensitive input, comparing it to our known list of
            # acceptable responses, then joining them all together into a 
            # comma-separated string.
            
        if day_of_month is not None:
            payload['schedule']['rrules']['bymonthday'] = self._check(
                'day_of_month', day_of_month, int, choices=list(range(1,32)))

        # Lets check to make sure that the scanner_id  and exclusion_id are 
        # integers as the API documentation requests and if we don't raise an 
        # error, then lets make the call.
        return self._api.put(
            'scanners/{}/agents/exclusions/{}'.format(
                self._check('scanner_id', scanner_id, int),
                self._check('exclusion_id', exclusion_id, int)
        ), json=payload).json()

    def list(self, scanner_id=1):
        '''
        Lists all of the currently configured agent exclusions.

        `agent-exclusions: list <https://cloud.tenable.com/api#/resources/agent-exclusions/list>`_

        Args:
            scanner_id (int, optional): The scanner identifier to be used.

        Returns:
            list: List of agent exclusions.

        Examples:
            >>> for exclusion in tio.agent_exclusions.list():
            ...     pprint(exclusion)
        '''
        return self._api.get(
            'scanners/{}/agents/exclusions'.format(
                self._check('scanner_id', scanner_id, int)
            )).json()['exclusions']
