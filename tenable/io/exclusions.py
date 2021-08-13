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
    .. automethod:: exclusions_import
'''
from datetime import datetime
from typing import Dict, Any, ClassVar, List, IO
from restfly.utils import dict_merge, dict_clean
from tenable.io.base import TIOEndpoint
from tenable.io.schema.exclusion_schema import ExclusionSchema


class ExclusionsAPI(TIOEndpoint):
    '''
    This class contain all methods related to exclusions
    '''
    _path: ClassVar[str] = 'exclusions'

    def _validate(
            self,
            data: Dict[Any, Any],
            validator=ExclusionSchema
    ) -> Dict:
        return validator().load(data)

    def create(
            self,
            name: str,
            members: List[str],
            **kwargs
    ) -> Dict:
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
                If enabled is true, the exclusion schedule is active.
                If enabled is false, the exclusion is "Always Active"
                The default value is ``True``
            network_id (uuid, optional):
                The ID of the network object associated with scanners
                where Tenable.io applies the exclusion.

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
        # validate user inputs
        kwargs = self._validate(kwargs)

        # Starting with the innermost part of the payload, lets construct the
        # rrules dictionary.
        frequency = kwargs.get('frequency', 'ONETIME')

        rrules = {
            'freq': frequency,
            'interval': kwargs.get('interval', 1)
        }

        # if the frequency is a weekly one, then we will need to specify the
        # days of the week that the exclusion is run on.
        if frequency == 'WEEKLY':
            rrules['byweekday'] = kwargs.get('weekdays', ['SU', 'MO', 'TU', 'WE', 'TH', 'FR', 'SA'])
            # In the same vein as the frequency check, we're accepting
            # case-insensitive input, comparing it to our known list of
            # acceptable responses, then joining them all together into a
            # comma-separated string.

        # if the frequency is monthly, then we will need to specify the day of
        # the month that the rule will run on.
        if frequency == 'MONTHLY':
            rrules['bymonthday'] = kwargs.get('day_of_month', datetime.today().day)

        # construct payload schedule based on enable
        kwargs['enabled'] = kwargs.get('enabled', True)
        if kwargs.get('enabled') is True:
            schedule = {
                'enabled': True,
                'starttime': kwargs.get('start_time').strftime('%Y-%m-%d %H:%M:%S'),
                'endtime': kwargs.get('end_time').strftime('%Y-%m-%d %H:%M:%S'),
                'timezone': kwargs.get('timezone', 'Etc/UTC'),
                'rrules': rrules
            }
        elif kwargs.get('enabled') is False:
            schedule = {'enabled': False}
        else:
            raise TypeError('enabled must be a boolean value.')

        # Next we need to construct the rest of the payload
        payload = {
            'name': self._check('name', name, str),
            'members': ','.join(self._check('members', members, list)),
            'description': kwargs.get('description', ''),
            'network_id': kwargs.get('network_id', '00000000-0000-0000-0000-000000000000'),
            'schedule': schedule
        }

        # And now to make the call and return the data.
        return self._api.post(f'{self._path}', json=payload).json()

    def delete(
            self,
            exclusion_id: int
    ) -> None:
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
        self._check('exclusion_id', exclusion_id, int)
        self._api.delete(f'{self._path}/{exclusion_id}')

    def details(
            self,
            exclusion_id: int
    ) -> Dict:
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
        self._check('exclusion_id', exclusion_id, int)
        return self._api.get(f'{self._path}/{exclusion_id}').json()

    def edit(
            self,
            exclusion_id: int,
            **kwargs
    ) -> Dict[Any, Any]:
        '''
        Edit an existing scan target exclusion.

        :devportal:`exclusions: edit <exclusions-edit>`

        The edit function will first gather the details of the exclusion that
        will be edited and will overlay the changes on top.  The result will
        then be pushed back to the API to modify the exclusion.

        Args:
            exclusion_id (int): The id of the exclusion object in Tenable.io
            name (str, optional): The name of the exclusion to create.
            members (list, optional):
                The exclusions members.  Each member should be a string with
                either a FQDN, IP Address, IP Range, or CIDR.
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
                where Tenable.io applies the exclusion.

        Returns:
            :obj:`dict`:
                Dictionary of the newly minted exclusion.

        Examples:
            Modifying the name of an exclusion:

            >>> exclusion = tio.exclusions.edit(1, name='New Name')
        '''

        # Lets start constructing the payload to be sent to the API...
        payload = self.details(self._check('exclusion_id', exclusion_id, int))
        payload['schedule'] = dict_clean(payload['schedule'])

        # validate user inputs
        kwargs = self._validate(kwargs)

        if kwargs.get('name'):
            payload['name'] = kwargs.get('name')

        if kwargs.get('members'):
            payload['members'] = kwargs.get('members')

        if kwargs.get('description'):
            payload['description'] = kwargs.get('description')

        if kwargs.get('enabled'):
            payload['schedule']['enabled'] = kwargs.get('enabled')

        if payload['schedule']['enabled']:
            # we will create a dict of default values from existing payload or
            # set individually if not existing schedule exist
            if payload['schedule'].get('rrules') is not None:
                default_rrule_values = {
                    'frequency': payload['schedule']['rrules'].get('freq'),
                    'interval': payload['schedule']['rrules'].get('interval', 1),
                    'weekdays': payload['schedule']['rrules'].get(
                        'byweekday', ','.join(['SU', 'MO', 'TU', 'WE', 'TH', 'FR', 'SA'])),
                    'day_of_month': payload['schedule']['rrules'].get(
                        'bymonthday', datetime.today().day),
                }
            else:
                default_rrule_values = {
                    'frequency': 'ONETIME',
                    'interval': 1,
                    'weekdays': ','.join(['SU', 'MO', 'TU', 'WE', 'TH', 'FR', 'SA']),
                    'day_of_month': datetime.today().day,
                }

            frequency = kwargs.get('frequency', default_rrule_values.get('frequency'))

            # interval needs to be handled in schedule enabled exclusion
            rrules = {
                'freq': frequency,
                'interval': default_rrule_values.get('interval')
            }

            if frequency == 'WEEKLY':
                rrules['byweekday'] = kwargs.get('weekdays', default_rrule_values.get('weekdays'))

            if frequency == 'MONTHLY':
                rrules['bymonthday'] = kwargs.get(
                    'day_of_month', default_rrule_values.get('day_of_month'))

            # update new rrules in existing payload
            if payload['schedule'].get('rrules') is not None:
                dict_merge(payload['schedule']['rrules'], rrules)
            else:
                payload['schedule']['rrules'] = rrules

            if kwargs.get('start_time'):
                payload['schedule']['starttime'] = kwargs.get('start_time').strftime('%Y-%m-%d %H:%M:%S')

            if kwargs.get('end_time'):
                payload['schedule']['endtime'] = kwargs.get('end_time').strftime('%Y-%m-%d %H:%M:%S')

            if kwargs.get('interval'):
                payload['schedule']['rrules']['interval'] = kwargs.get('interval')

            payload['schedule']['timezone'] = kwargs.get(
                'timezone', payload['schedule'].get('timezone', 'Etc/UTC'))

        if kwargs.get('network_id'):
            payload['network_id'] = kwargs.get('network_id')

        # Lets check to make sure that the scanner_id  and exclusion_id are
        # integers as the API documentation requests and if we don't raise an
        # error, then lets make the call.
        return self._api.put(f'{self._path}/{exclusion_id}', json=payload).json()

    def list(self) -> List[Dict]:
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
        return self._api.get(f'{self._path}').json()['exclusions']

    def exclusions_import(
            self,
            fobj: IO
    ) -> None:
        '''
        Import exclusions into Tenable.io.

        :devportal:`exclusions: import <exclusions-import>`

        Args:
            fobj (FileObject):
                The file object of the exclusion(s) you wish to import.

        Returns:
            :obj:`None`:
                Returned if Tenable.io successfully imports the exclusion file.

        Examples:
            >>> with open('import_example.csv') as exclusion:
            ...     tio.exclusions.exclusions_import(exclusion)
        '''
        fid = self._api.files.upload(fobj)
        return self._api.post(f'{self._path}/import', json={'file': fid})
