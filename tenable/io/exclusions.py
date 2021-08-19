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
from typing import Dict, Any, ClassVar, List, IO, Callable
from marshmallow import EXCLUDE
from restfly.utils import dict_merge, dict_clean
from tenable.io.base import TIOEndpoint
from tenable.io.schemas.exclusion_schema import ExclusionSchema


class ExclusionsAPI(TIOEndpoint):
    '''
    This class contain all methods related to exclusions
    '''
    _path: ClassVar[str] = 'exclusions'

    def _validate(
            self,
            data: Dict[Any, Any],
            validator: Callable = ExclusionSchema,
            exclude: bool = False
    ) -> Dict:
        if exclude:
            return validator(unknown=EXCLUDE).load(data)
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
        # create a payload required for API
        payload = {
            'name': self._check('name', name, str),
            'members': self._check('members', members, list),
            'description': kwargs.get('description'),
            'network_id': kwargs.get('network_id'),
            'schedule': {
                'enabled': kwargs.get('enabled'),
                'starttime': kwargs.get('start_time'),
                'endtime': kwargs.get('end_time'),
                'timezone': kwargs.get('timezone'),
                'rrules': {
                    'freq': kwargs.get('frequency'),
                    'interval': kwargs.get('interval'),
                    'byweekday': kwargs.get('weekdays'),
                    'bymonthday': kwargs.get('day_of_month')
                }
            }
        }

        payload = self._validate(payload)

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
        # get the existing values
        existing_payload = self.details(self._check('exclusion_id', exclusion_id, int))

        # create updated payload template
        updated_payload = {
            'name': kwargs.get('name'),
            'members': kwargs.get('members'),
            'description': kwargs.get('description'),
            'network_id': kwargs.get('network_id'),
            'schedule': {
                'enabled': kwargs.get('enabled'),
                'starttime': kwargs.get('start_time'),
                'endtime': kwargs.get('end_time'),
                'timezone': kwargs.get('timezone'),
                'rrules': {
                    'freq': kwargs.get('frequency'),
                    'interval': kwargs.get('interval'),
                    'byweekday': kwargs.get('weekdays'),
                    'bymonthday': kwargs.get('day_of_month')
                }
            }
        }

        # filter all None values from updated payload
        updated_payload = dict_clean(updated_payload)

        # merge new values to existing payload
        dict_merge(existing_payload, updated_payload)

        # validate payload
        payload = self._validate(existing_payload, exclude=True)

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
