'''
Exclusions
==========

The following methods allow for interaction into the Tenable Vulnerability
Management :devportal:`exclusions <exclusions>` API endpoints.

Methods available on ``tio.exclusions``:

.. rst-class:: hide-signature
.. autoclass:: ExclusionsAPI
    :members:
'''
from datetime import datetime
from restfly.utils import dict_merge
from tenable.io.base import TIOEndpoint

class ExclusionsAPI(TIOEndpoint):
    '''
    This will contain all methods related to exclusions
    '''

    def create(self, name, members, start_time=None, end_time=None,
               timezone=None, description=None, frequency=None,
               interval=None, weekdays=None, day_of_month=None,
               enabled=True, network_id=None):
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
                please refer to :devportal:`scans: timezones <scans-timezones>`
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
                If enabled is true, the exclusion schedule is active.
                If enabled is false, the exclusion is "Always Active".
                The default value is ``True``
            network_id (uuid, optional):
                The ID of the network object associated with scanners
                where Tenable Vulnerability Management applies the exclusion.

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

        # construct payload schedule based on enable
        if enabled is True:
            schedule = {
                'enabled': True,
                'starttime':
                    self._check('start_time', start_time, datetime).strftime('%Y-%m-%d %H:%M:%S'),
                'endtime':
                    self._check('end_time', end_time, datetime).strftime('%Y-%m-%d %H:%M:%S'),
                'timezone': self._check('timezone', timezone, str,
                    choices=self._api._tz, default='Etc/UTC'),
                'rrules': rrules
            }
        elif enabled is False:
            schedule = {'enabled': False}
        else:
            raise TypeError('enabled must be a boolean value.')

        # Next we need to construct the rest of the payload
        payload = {
            'name': self._check('name', name, str),
            'members': ','.join(self._check('members', members, list)),
            'description': self._check('description', description, str, default=''),
            'network_id': self._check('network_id', network_id, 'uuid',
                                      default='00000000-0000-0000-0000-000000000000'),
            'schedule': schedule
        }

        # And now to make the call and return the data.
        return self._api.post('exclusions', json=payload).json()

    def delete(self, exclusion_id):
        '''
        Delete a scan target exclusion.

        :devportal:`exclusions: delete <exclusions-delete>`

        Args:
            exclusion_id (int): The exclusion identifier to delete

        Returns:
            :obj:`None`:
                The exclusion was successfully deleted.

        Examples:
            >>> tio.exclusions.delete(1)
        '''
        self._api.delete('exclusions/{}'.format(self._check('exclusion_id', exclusion_id, int)))

    def details(self, exclusion_id):
        '''
        Retrieve the details for a specific scan target exclusion.

        :devportal:`exclusions: details <exclusions-details>`

        Args:
            exclusion_id (int): The exclusion identifier.

        Returns:
            :obj:`dict`:
                The exclusion record requested.

        Examples:
            >>> exclusion = tio.exclusions.details(1)
            >>> pprint(exclusion)
        '''
        return self._api.get(
            'exclusions/{}'.format(self._check('exclusion_id', exclusion_id, int))).json()

    def edit(self, exclusion_id, name=None, members=None, start_time=None,
             end_time=None, timezone=None, description=None, frequency=None,
             interval=None, weekdays=None, day_of_month=None, enabled=None, network_id=None):
        '''
        Edit an existing scan target exclusion.

        :devportal:`exclusions: edit <exclusions-edit>`

        The edit function will first gather the details of the exclusion that
        will be edited and will overlay the changes on top.  The result will
        then be pushed back to the API to modify the exclusion.

        Args:
            exclusion_id (int): The id of the exclusion object in
                Tenable Vulnerability Management
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
            enabled (bool, optional):
                enable/disable exclusion.
            network_id (uuid, optional):
                The ID of the network object associated with scanners
                where Tenable Vulnerability Management applies the exclusion.

        Returns:
            :obj:`dict`:
                Dictionary of the newly minted exclusion.

        Examples:
            Modifying the name of an exclusion:

            >>> exclusion = tio.exclusions.edit(1, name='New Name')
        '''

        # Lets start constructing the payload to be sent to the API...
        payload = self.details(exclusion_id)

        if name:
            payload['name'] = self._check('name', name, str)

        if members:
            payload['members'] = ','.join(self._check('members', members, list))

        if description:
            payload['description'] = self._check('description', description, str)

        if enabled is not None:
            payload['schedule']['enabled'] = self._check('enabled', enabled, bool)

        if payload['schedule']['enabled']:
            frequency = self._check('frequency', frequency, str,
                                    choices=['ONETIME', 'DAILY', 'WEEKLY', 'MONTHLY', 'YEARLY'],
                                    default=payload['schedule']['rrules'].get('freq')
                                    if payload['schedule']['rrules'] is not None else 'ONETIME',
                                    case='upper')

            # interval needs to be handled in schedule enabled excusion
            rrules = {
                'freq': frequency,
                'interval': payload['schedule']['rrules'].get('interval', None) or 1
                if payload['schedule']['rrules'] is not None else 1
            }

            # frequency default value is designed for weekly and monthly based on below conditions
            # - if schedule rrules is None and not defined in edit params, assign default values
            # - if schedule rrules is not None and not defined in edit params, assign old values
            # - if schedule rrules is not None and not defined in edit params
            # and byweekday/bymonthday key not already exist, assign default values
            # - if schedule rrules is not None and defined in edit params, assign new values
            if frequency == 'WEEKLY':
                rrules['byweekday'] = ','.join(self._check(
                    'weekdays', weekdays, list,
                    choices=['SU', 'MO', 'TU', 'WE', 'TH', 'FR', 'SA'],
                    default=payload['schedule']['rrules'].get('byweekday', '').split()
                            or ['SU', 'MO', 'TU', 'WE', 'TH', 'FR', 'SA']
                    if payload['schedule']['rrules'] is not None else
                    ['SU', 'MO', 'TU', 'WE', 'TH', 'FR', 'SA'],
                    case='upper'))
                # In the same vein as the frequency check, we're accepting
                # case-insensitive input, comparing it to our known list of
                # acceptable responses, then joining them all together into a
                # comma-separated string.

            if frequency == 'MONTHLY':
                rrules['bymonthday'] = self._check(
                    'day_of_month', day_of_month, int, choices=list(range(1, 32)),
                    default=payload['schedule']['rrules'].get('bymonthday', datetime.today().day)
                    if payload['schedule']['rrules'] is not None else datetime.today().day)

            # update new rrules in existing payload
            if payload['schedule']['rrules'] is not None:
                dict_merge(payload['schedule']['rrules'], rrules)
            else:
                payload['schedule']['rrules'] = rrules

            if start_time:
                payload['schedule']['starttime'] = self._check(
                    'start_time', start_time, datetime).strftime('%Y-%m-%d %H:%M:%S')

            if end_time:
                payload['schedule']['endtime'] = self._check(
                    'end_time', end_time, datetime).strftime('%Y-%m-%d %H:%M:%S')

            if interval:
                payload['schedule']['rrules']['interval'] = self._check(
                    'interval', interval, int)

            payload['schedule']['timezone'] = self._check(
                'timezone', timezone, str, choices=self._api._tz, default='Etc/UTC')

        if network_id:
            payload['network_id'] = self._check('network_id', network_id, 'uuid')

        # Lets check to make sure that the scanner_id  and exclusion_id are
        # integers as the API documentation requests and if we don't raise an
        # error, then lets make the call.
        return self._api.put(
            'exclusions/{}'.format(
                self._check('exclusion_id', exclusion_id, int)
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

    def exclusions_import(self, fobj):
        '''
        Import exclusions into Tenable Vulnerability Management.

        :devportal:`exclusions: import <exclusions-import>`

        Args:
            fobj (FileObject):
                The file object of the exclusion(s) you wish to import.

        Returns:
            :obj:`None`:
                Returned if Tenable Vulnerability Management successfully
                imports the exclusion file.

        Examples:
            >>> with open('import_example.csv') as exclusion:
            ...     tio.exclusions.exclusions_import(exclusion)
        '''
        fid = self._api.files.upload(fobj)
        return self._api.post('exclusions/import', json={'file': fid})
