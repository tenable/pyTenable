'''
exclusions
==========

The following methods allow for interaction into the Tenable.io
:devportal:`exclusions <exclusions>`
API endpoints.

Methods available on ``tio.exclusions``:

.. rst-class:: hide-signature
.. autoclass:: ExclusionsAPI

    .. automethod:: create
    .. automethod:: delete
    .. automethod:: details
    .. automethod:: edit
    .. automethod:: list
'''
from .base import TIOEndpoint
from datetime import datetime

class ExclusionsAPI(TIOEndpoint):
    def create(self, name, members, start_time=None, end_time=None,
               timezone=None, description=None, frequency=None,
               interval=None, weekdays=None, day_of_month=None,
               enabled=True):
        '''
        Create a scan target exclusion.

        :devportal:`exclusions: create <exclusions-create>`

        Args:
            name (str): The name of the exclusion to create.
            members (list):
                The exclusions members.  Each member should be a string with
                either a FQDN, IP Address, IP Range, or CIDR.
            description (str, optional):
                Some further detail about the exclusion.
            start_time (datetime): When the exclusion should start.
            end_time (datetime): When the exclusion should end.
            timezone (str, optional):
                The timezone to use for the exclusion.  The default if none is
                specified is to use UTC.  For the list of usable timezones,
                please refer to :devportal:`scans-timezones`
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
            :obj:`dict`:
                Dictionary of the newly minted exclusion.

        Examples:
            Creating a one-time exclusion:

            >>> from datetime import datetime, timedelta
            >>> exclusion = tio.exclusions.create(
            ...     'Example One-Time Exclusion',
            ...     ['127.0.0.1'],
            ...     start_time=datetime.utcnow(),
            ...     end_time=datetime.utcnow() + timedelta(hours=1))

            Creating a daily exclusion:

            >>> exclusion = tio.exclusions.create(
            ...     'Example Daily Exclusion',
            ...     ['127.0.0.1'],
            ...     frequency='daily',
            ...     start_time=datetime.utcnow(),
            ...     end_time=datetime.utcnow() + timedelta(hours=1))

            Creating a weekly exclusion:

            >>> exclusion = tio.exclusions.create(
            ...     'Example Weekly Exclusion',
            ...     ['127.0.0.1'],
            ...     frequency='weekly',
            ...     weekdays=['mo', 'we', 'fr'],
            ...     start_time=datetime.utcnow(),
            ...     end_time=datetime.utcnow() + timedelta(hours=1))

            Creating a monthly esxclusion:

            >>> exclusion = tio.exclusions.create(
            ...     'Example Monthly Exclusion',
            ...     ['127.0.0.1'],
            ...     frequency='monthly',
            ...     day_of_month=1,
            ...     start_time=datetime.utcnow(),
            ...     end_time=datetime.utcnow() + timedelta(hours=1))

            Creating a yearly exclusion:

            >>> exclusion = tio.exclusions.create(
            ...     'Example Yearly Exclusion',
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
            'members': ','.join(self._check('members', members, list)),
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

        # And now to make the call and return the data.
        return self._api.post('exclusions', json=payload).json()

    def delete(self, id):
        '''
        Delete a scan target exclusion.

        :devportal:`exclusions: delete <exclusions-delete>`

        Args:
            id (int): The exclusion identifier to delete

        Returns:
            :obj:`None`:
                The exclusion was successfully deleted.

        Examples:
            >>> tio.exclusions.delete(1)
        '''
        self._api.delete('exclusions/{}'.format(self._check('id', id, int)))

    def details(self, id):
        '''
        Retrieve the details for a specific scan target exclusion.

        :devportal:`exclusions: details <exclusions-details>`

        Args:
            id (int): The exclusion identifier.

        Returns:
            :obj:`dict`:
                The exclusion record requested.

        Examples:
            >>> exclusion = tio.exclusions.details(1)
            >>> pprint(exclusion)
        '''
        return self._api.get(
            'exclusions/{}'.format(self._check('id', id, int))).json()

    def edit(self, id, name=None, members=None, start_time=None,
             end_time=None, timezone=None, description=None, frequency=None,
             interval=None, weekdays=None, day_of_month=None, enabled=None):
        '''
        Edit an existing scan target exclusion.

        :devportal:`exclusions: edit <exclusions-edit>`

        The edit function will first gather the details of the exclusion that
        will be edited and will overlay the changes on top.  The result will
        then be pushed back to the API to modify the exclusion.

        Args:
            id (int): The id of the exclusion object in Tenable.io

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
                The frequency of the rule. The string inputted will be upcased.
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
            :obj:`dict`:
                Dictionary of the newly minted exclusion.

        Examples:
            Modifying the name of an exclusion:

            >>> exclusion = tio.exclusions.edit(1, name='New Name')
        '''

        # Lets start constructing the payload to be sent to the API...
        payload = self.details(id)

        if name:
            payload['name'] = self._check('name', name, str)

        if members:
            payload['members'] = ','.join(self._check('members', members, list))

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
            'exclusions/{}'.format(
                self._check('id', id, int)
            ), json=payload).json()

    def list(self):
        '''
        List the currently configured scan target exclusions.

        :devportal:`exclusions: list <exclusions-list>`

        Returns:
            :obj:`list`:
                List of exclusion resource records.

        Examples:
            >>> for exclusion in tio.exclusions.list():
            ...     pprint(exclusion)
        '''
        return self._api.get('exclusions').json()['exclusions']