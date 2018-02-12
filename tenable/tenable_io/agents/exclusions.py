from tenable.base import APIEndpoint
from tenable.tenable_io.models import ExclusionSchedule

class AgentExclusionsAPI(APIEndpoint):
    def create(self, scanner_id, name, starttime=None, endtime=None, 
               timezone=None, description=None, freq=None, 
               interval=None, weekdays=None, dayofmonth=None,
               enabled=None, sched_obj=None):
        '''
        agent-exclusions: create
        https://cloud.tenable.com/api#/resources/agent-exclusions/create

        Args:
            scanner_id (int): The scanner id.
            name (str): The name of the exclusion to create.
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
            sched_obj (obj:`ExclusionSchedule`, optional):
                Instead of supplying *any* of the optional parameters, a
                ExclusionSchedule object with the appropriate values may instead 
                be passed.  This will bypass interpretation of any of the other
                paramters and use the object instead.

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
        payload = {'name': self._check('name', name, str)}

        # As the description and schedule are optional, we will only add 
        # them into the payload if one was specified.
        if self._check('description', description, str):
            payload['description'] = description
        if sched_obj:
            payload['schedule'] = sched_obj.json()

        # Lests check to make sure that the scanner_id is an integer as the API
        # documentation requests and if we don't raise an error, then lets make
        # the call.
        return self._api.post(
            'scanners/{}/agents/exclusions'.format(
                self._check('scanner_id', scanner_id, int)), json=payload)

    def delete(self, scanner_id, exclusion_id):
        '''
        agent-exclusions: delete
        https://cloud.tenable.com/api#/resources/agent-exclusions/delete

        Args:
            scanner_id (int): The id of the scanner
            exclusion_id (int): The id of the exclusion object in Tenable.io

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
            ))

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
            sched_obj (obj:`ExclusionSchedule`, optional):
                Instead of supplying *any* of the optional parameters, a
                ExclusionSchedule object with the appropriate values may instead 
                be passed.  This will bypass interpretation of any of the other
                paramters and use the object instead.

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
        ), json=payload)

    def list(self, scanner_id):
        '''
        agent-exclusions: list
        https://cloud.tenable.com/api#/resources/agent-exclusions/list

        Args:
            scanner_id (int): The scanner identifier to be used.

        Returns:
            list: List of agent exclusions.
        '''
        return self._api.get('scanners/{}/agent/exclusions'.format(
            self._check('scanner_id', scanner_id, int)))['exclusions']
