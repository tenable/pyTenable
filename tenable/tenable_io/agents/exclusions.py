from tenable.base import APIEndpoint
from datetime import date, datetime

class AgentExclusionsAPI(APIEndpoint):
    def create(self, scanner_id, name, start_time=None, end_time=None, 
               timezone=None, description=None, frequency=None, 
               interval=None, weekdays=None, dayofmonth=None,
               enabled=True):
        '''
        agent-exclusions: create
        https://cloud.tenable.com/api#/resources/agent-exclusions/create

        Args:
            name (str): The name of the exclusion to create.
            scanner_id (int, optional): The scanner id.
            description (str, optional): 
                Some further detail about the exclusion.
            start_time (datetime, optional): When the exclusion should start.
            end_time (datetime, optional): When the exclusion should end.
            timezone (str, optional): 
                The timezone to use for the exclusion.  The default if none is 
                specified is to use UTC.  For the list of usable timezones,
                please refer to:
                https://cloud.tenable.com/api#/resources/scans/timezones
            frequency (str, optional):
                The frequency of the rule. The string inputted will be upcased.
                Valid values are: *ONETIME, DAILY, WEEKLY, MONTHLY, YEARLY*.
            interval (int, optional): The interval of the rule.
            weekdays (list, optional):
                List of 2-character representations of the days of the week to
                repeate the frequency rule on.  Valied values are:
                *SU, MO, TU, WE, TH, FR, SA*
                Default values: ``['SU', 'MO', 'TU', 'WE', 'TH', 'FR', 'SA']``
            dayofmonth (int, optional):
                The day of the month to repeat a **MONTHLY** frequency rule on.

        Returns:
            dict: Dictionary of the newly minted exclusion. 
        '''
        # Starting with the innermost part of the payload, lets construct the
        # rrules dictionary.
        frequency = frequency.upper()
        rrules = {
            'freq': self._check('frequency', frequency, str, 
                choices=['ONETIME', 'DAILY', 'WEEKLY', 'MONTHLY', 'YEARLY'],
                default='ONETIME'),
            'interval': self._check('interval', interval, int, default=1)
        }

        # if the frequency is a weekly one, then we will need to specify the
        # days of the week that the exclusion is run on.
        if frequency == 'WEEKLY':
            rrules['byweekday'] = ','.join(self._check('weekdays', weekdays, list,
                choices=['SU', 'MO', 'TU', 'WE', 'TH', 'FR', 'SA'],
                default=['SU', 'MO', 'TU', 'WE', 'TH', 'FR', 'SA']))

        # if the requency is monthly, then we will need to specify the day of
        # the month that the rule will run on.
        if frequency == 'MONTHLY':
            rrules['bymonthday'] = self._check('dayofmonth', dayofmonth, int,
                choices=range(1,32))

        # Next we need to construct the rest of the payload
        payload = {
            'name': self._check('name', name, str),
            'description': self._check('description', description, str, default=''),
            'schedule': {
                'enabled': self._check('enabled', enabled, bool),
                'starttime': self._check('start_time'. start_time, datetime).strftime('%Y-%m-%d %H:%M:%S'),
                'endtime': self._check('end_time'. end_time, datetime).strftime('%Y-%m-%d %H:%M:%S'),
                'timezone': self._check('timezone', timezone, str, default='Etc/UTC'),
                'rrules': rrules
            }
        }

        # Lests check to make sure that the scanner_id is an integer as the API
        # documentation requests and if we don't raise an error, then lets make
        # the call.
        return self._api.post(
            'scanners/{}/agents/exclusions'.format(
                self._check('scanner_id', scanner_id, int)
            ), json=payload).json()

    def delete(self, scanner_id, exclusion_id):
        '''
        agent-exclusions: delete
        https://cloud.tenable.com/api#/resources/agent-exclusions/delete

        Args:
            exclusion_id (int): The id of the exclusion object in Tenable.io
            scanner_id (int, optional): The id of the scanner

        Returns:
            Unknown.
        '''
        return self._api.delete(
            'scanners/{}/agents/exclusions/{}'.format(
                self._check('scanner_id', scanner_id, int),
                self._check('exclusion_id', exclusion_id, int)
            ))

    def details(self, scanner_id, exclusion_id):
        '''
        agent-exclusion: details
        https://cloud.tenable.com/api#/resources/agent-exclusions/details

        Args:
            scanner_id (int): The id of the scanner
            exclusion_id (int): The id of the exclusion object in Tenable.io

        Returns:
            dict: The exclusion resource dictionary.
        '''
        return self._api.delete(
            'scanners/{}/agents/exclusions/{}'.format(
                self._check('scanner_id', scanner_id, int),
                self._check('exclusion_id', exclusion_id, int)
            )).json()

    def edit(self, scanner_id, exclusion_id, name=None, starttime=None, 
            endtime=None, timezone=None, description=None, freq=None, 
            interval=None, weekdays=None, dayofmonth=None, enabled=None, 
            sched_obj=None):
        '''
        Args:
            scanner_id (int): The scanner id.
            exclusion_id (int): The id of the exclusion object in Tenable.io
            name (str, optional): The name of the exclusion to create.
            description (str, optional): 
                Some further detail about the exclusion.
            starttime (datetime, optional): When the exclusion should start.
            endtime (datetime, optional): When the exclusion should end.
            timezone (str, optional): 
                The timezone to use for the exclusion.  The default if none is 
                specified is to use UTC.
            freq (str, optional):
                The frequency of the rule. The string inputted will be upcased.
                Valid values are: *ONETIME, DAILY, WEEKLY, MONTHLY, YEARLY*.
            interval (int, optional): The interval of the rule.
            weekdays (list, optional):
                List of 2-character representations of the days of the week to
                repeate the frequency rule on.  Valied values are:
                *SU, MO, TU, WE, TH, FR, SA*
                Default values: ``['SU', 'MO', 'TU', 'WE', 'TH', 'FR', 'SA']``
            dayofmonth (int, optional):
                The day of the month to repeat a **MONTHLY** frequency rule on.

        Returns:
            dict: Dictionary of the newly minted exclusion. 
        '''

        # If an ExclusionSchedule object was not passed in, then we will have to
        # construct one using all of the available parameters.
        if not sched_obj and (starttime or endtime or timezone or freq 
          or interval or weekdays or dayofmonth or enabled):
            sched_obj = ExclusionSchedule(
                starttime=starttime, 
                endtime=endtime,
                timezone=timezone,
                enabled=enabled,
                freq=freq,
                interval=interval,
                weekdays=weekdays,
                dayofmonth=dayofmonth
            )

        # Lets start constructing the payload to be sent to the API...
        payload = {}

        # As the description, name, and schedule are optional, we will only add 
        # them into the payload if one was specified.
        if self._check('description', description, str):
            payload['description'] = description
        if self._check('name', name, str):
            payload['name'] = name
        if sched_obj:
            payload['schedule'] = sched_obj.json()

        # Lests check to make sure that the scanner_id  and exclusion_id are 
        # integers as the API documentation requests and if we don't raise an 
        # error, then lets make the call.
        return self._api.put(
            'scanners/{}/agents/exclusions/{}'.format(
                self._check('scanner_id', scanner_id, int),
                self._check('exclusion_id', exclusion_id, int)
        ), json=payload).json()

    def list(self, scanner_id):
        '''
        agent-exclusions: list
        https://cloud.tenable.com/api#/resources/agent-exclusions/list

        Args:
            scanner_id (int): The scanner identifier to be used.

        Returns:
            list: List of agent exclusions.
        '''
        return self._api.get(
            'scanners/{}/agent/exclusions'.format(
                self._check('scanner_id', scanner_id, int)
            )).json()['exclusions']
