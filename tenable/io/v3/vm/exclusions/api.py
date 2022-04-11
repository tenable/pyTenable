'''
Exclusions
==========

The following methods allow for interaction into the Tenable.io
:devportal:`exclusions <exclusions>`
API endpoints.

Methods available on ``tio.v3.vm.exclusions``:

.. rst-class:: hide-signature
.. autoclass:: ExclusionsAPI
    :members:
'''

from datetime import datetime
from typing import BinaryIO, Dict, List, Optional, Union
from uuid import UUID

from requests import Response

from tenable.io.v3.base.endpoints.explore import ExploreBaseEndpoint
from tenable.io.v3.base.iterators.explore_iterator import (CSVChunkIterator,
                                                           SearchIterator)
from tenable.io.v3.vm.exclusions.schema import ExclusionSchema
from tenable.utils import dict_clean, dict_merge


class ExclusionsAPI(ExploreBaseEndpoint):
    '''
    This class contain all methods related to exclusions
    '''
    _path: str = 'api/v3/exclusions'
    _conv_json: bool = True

    def create(self,
               name: str,
               members: List,
               start_time: Optional[str] = None,
               end_time: Optional[str] = None,
               timezone: Optional[str] = None,
               description: Optional[str] = None,
               frequency: Optional[str] = None,
               interval: Optional[int] = None,
               weekdays: Optional[List] = None,
               day_of_month: Optional[int] = None,
               enabled: Optional[bool] = True,
               network_id: Optional[UUID] = None
               ) -> Dict:
        '''
        Create a scan target exclusion.

        :devportal:`exclusions: create <exclusions-create>`

        Args:
            name (str): The name of the exclusion to create.
            members (list):
                The exclusions members.  Each member should be a string with
                either a FQDN, IP Address, IP Range, or CIDR.
            start_time (str): When the exclusion should start.
            end_time (str): When the exclusion should end.
            timezone (str, optional):
                The timezone to use for the exclusion. The default, if none is
                specified, is to use UTC.  For the list of usable timezones,
                please refer to :devportal:`scans-timezones`
            description (str, optional):
                Some further detail about the exclusion.
            frequency (str, optional):
                The frequency of the rule. The string inputted will be up-cased
                Valid values are: ``ONETIME``, ``DAILY``, ``WEEKLY``,
                ``MONTHLY``, ``YEARLY``.
                Default value is ``ONETIME``.
            interval (int, optional):
                The interval of the rule. The default interval is 1
            weekdays (list, optional):
                List of 2-character representations of the days of the week to
                repeat the frequency rule on. Valid values are:
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
            >>> exclusion = tio.v3.vm.exclusions.create(
            ...     'Example One-Time Exclusion',
            ...     ['127.0.0.1'],
            ...     start_time=datetime.utcnow().strftime(
            ...         '%Y-%m-%d %H:%M:%S'
            ...     ),
            ...     end_time=(
            ...         datetime.utcnow() + timedelta(hours=1)
            ...     ).strftime('%Y-%m-%d %H:%M:%S')
            ... )

            Creating a daily exclusion:

            >>> exclusion = tio.v3.vm.exclusions.create(
            ...     'Example Daily Exclusion',
            ...     ['127.0.0.1'],
            ...     frequency='daily',
            ...     start_time=datetime.utcnow().strftime(
            ...         '%Y-%m-%d %H:%M:%S'
            ...     ),
            ...     end_time=(
            ...         datetime.utcnow() + timedelta(hours=1)
            ...     ).strftime('%Y-%m-%d %H:%M:%S')
            ... )

            Creating a weekly exclusion:

            >>> exclusion = tio.v3.vm.exclusions.create(
            ...     'Example Weekly Exclusion',
            ...     ['127.0.0.1'],
            ...     frequency='weekly',
            ...     weekdays=['mo', 'we', 'fr'],
            ...     start_time=datetime.utcnow().strftime(
            ...         '%Y-%m-%d %H:%M:%S'
            ...     ),
            ...     end_time=(
            ...         datetime.utcnow() + timedelta(hours=1)
            ...     ).strftime('%Y-%m-%d %H:%M:%S')
            ... )

            Creating a monthly esxclusion:

            >>> exclusion = tio.v3.vm.exclusions.create(
            ...     'Example Monthly Exclusion',
            ...     ['127.0.0.1'],
            ...     frequency='monthly',
            ...     day_of_month=1,
            ...     start_time=datetime.utcnow().strftime(
            ...         '%Y-%m-%d %H:%M:%S'
            ...     ),
            ...     end_time=(
            ...         datetime.utcnow() + timedelta(hours=1)
            ...     ).strftime('%Y-%m-%d %H:%M:%S')
            ... )

            Creating a yearly exclusion:

            >>> exclusion = tio.v3.vm.exclusions.create(
            ...     'Example Yearly Exclusion',
            ...     ['127.0.0.1'],
            ...     frequency='yearly',
            ...     start_time=datetime.utcnow().strftime(
            ...         '%Y-%m-%d %H:%M:%S'
            ...     ),
            ...     end_time=(
            ...         datetime.utcnow() + timedelta(hours=1)
            ...     ).strftime('%Y-%m-%d %H:%M:%S')
            ... )
        '''

        # construct schedule payload based on enable
        if enabled is True:
            schedule: dict = {
                'enabled': True,
                'starttime': start_time,
                'endtime': end_time,
                'timezone': timezone or 'Etc/UTC',
                'rrules': {
                    'freq': frequency or 'ONETIME',
                    'interval': interval or 1,
                    'byweekday': weekdays,
                    'bymonthday': day_of_month
                }
            }

        elif enabled is False:
            schedule = {'enabled': False}
        else:
            raise TypeError('enabled must be a boolean value.')

        # Next we need to construct the rest of the payload
        payload = {
            'name': name,
            'members': members,
            'description': description,
            'network_id': network_id,
            'schedule': schedule
        }
        payload = dict_clean(payload)

        # Let's validate the payload using Mershmallow schema
        schema = ExclusionSchema(
            context={'timezones': self._api._tz}
        )
        payload = schema.dump(schema.load(payload))

        # And now to make the call and return the data.
        return self._post(json=payload)

    def delete(self, exclusion_id: int) -> None:
        '''
        Delete a scan target exclusion.

        :devportal:`exclusions: delete <exclusions-delete>`

        Args:
            exclusion_id (int): The exclusion identifier to delete

        Returns:
            :obj:`None`:
                The exclusion was successfully deleted.

        Examples:
            >>> tio.v3.vm.exclusions.delete(1)
        '''
        self._delete(f'{exclusion_id}')

    def details(self, exclusion_id: int) -> Dict:
        '''
        Retrieve the details for a specific scan target exclusion.

        :devportal:`exclusions: details <exclusions-details>`

        Args:
            exclusion_id (int): The exclusion identifier.

        Returns:
            :obj:`dict`:
                The exclusion record requested.

        Examples:
            >>> exclusion = tio.v3.vm.exclusions.details(1)
            >>> pprint(exclusion)
        '''
        return super()._details(str(exclusion_id))

    def edit(self,
             exclusion_id: int,
             name: Optional[str] = None,
             members: Optional[List] = None,
             start_time: Optional[str] = None,
             end_time: Optional[str] = None,
             timezone: Optional[str] = None,
             description: Optional[str] = None,
             frequency: Optional[str] = None,
             interval: Optional[int] = None,
             weekdays: Optional[List] = None,
             day_of_month: Optional[int] = None,
             enabled: Optional[bool] = None,
             network_id: Optional[UUID] = None
             ) -> Dict:
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
            start_time (str, optional): When the exclusion should start.
            end_time (str, optional): When the exclusion should end.
            timezone (str, optional):
                The timezone to use for the exclusion.  The default if none is
                specified is to use UTC.  For the list of usable timezones,
                please refer to :devportal:`scans-timezones`
            description (str, optional):
                Some further detail about the exclusion.
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

            >>> exclusion = tio.v3.vm.exclusions.edit(1, name='New Name')
        '''

        # Lets start constructing the payload to be sent to the API...
        res_dict = self.details(exclusion_id=exclusion_id)

        if res_dict['schedule']['rrules'] is None:
            res_dict['schedule']['rrules'] = {}

        if enabled is None:
            enabled = res_dict['schedule']['enabled']

        payload: dict = {
            'name': name or res_dict['name'],
            'members': members or str(res_dict['members']).split(','),
            'description': description or res_dict['description'],
            'network_id': network_id or res_dict['network_id'],
            'schedule': {
                'enabled': enabled
            }
        }

        if payload['schedule']['enabled']:
            rrules: dict = res_dict['schedule']['rrules']
            schedule: dict = {
                'starttime': start_time or res_dict['schedule']['starttime'],
                'endtime': end_time or res_dict['schedule']['endtime'],
                'timezone': timezone or res_dict['schedule'].get(
                    'timezone', 'Etc/UTC'
                ),
                'rrules': {
                    'freq': frequency or rrules.get('freq', 'ONETIME'),
                    'interval': interval or rrules.get('interval', 1),
                    'byweekday': weekdays or rrules.get(
                        'byweekday', 'SU,MO,TU,WE,TH,FR,SA').split(','),
                    'bymonthday': day_of_month or rrules.get(
                        'bymonthday', datetime.today().day)
                }
            }
            # let's merge new schedule dict to payload
            dict_merge(payload['schedule'], schedule)

        # Let's validate the payload using Mershmallow schema
        schema = ExclusionSchema(
            context={'timezones': self._api._tz}
        )
        payload = schema.dump(schema.load(payload))

        return self._put(f'{exclusion_id}', json=payload)

    def exclusions_import(self, fobj: BinaryIO) -> None:
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
            ...     tio.v3.vm.exclusions.exclusions_import(exclusion)
        '''
        fid = self._api.v3.vm.files.upload(fobj)

        self._post('import', json={'file': fid})

    def search(self,
               **kwargs) -> Union[SearchIterator, CSVChunkIterator, Response]:
        '''
        Search exclusions based on supported conditions.
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
                the :py:meth:`tio.v3.definitions.vm.exclusions()`
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
            >>> tio.v3.vm.exclusions.search(
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
            sort_type=self._sort_type.property_based,
            api_path=f'{self._path}/search',
            resource='exclusions',
            **kwargs
        )
