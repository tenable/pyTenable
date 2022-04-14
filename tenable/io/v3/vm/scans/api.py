'''
Scans
=====

The following methods allow for interaction into the Tenable.io
:devportal:`scans <scans>` API endpoints.

Methods available on ``tio.v3.vm.scans``:

.. rst-class:: hide-signature
.. autoclass:: ScansAPI
    :members:
'''
import time
from datetime import datetime
from io import BytesIO
from typing import BinaryIO, Callable, Dict, Optional, Union
from uuid import UUID

import pytest
from requests import Response
from restfly.utils import dict_clean

from tenable.constants import IOConstants
from tenable.errors import UnexpectedValueError
from tenable.io.v3.base.endpoints.explore import ExploreBaseEndpoint
from tenable.io.v3.base.iterators.explore_iterator import (CSVChunkIterator,
                                                           SearchIterator)
from tenable.io.v3.vm.scans.schema import (ScanCheckAutoTargetSchema,
                                           ScanConfigureScheduleSchema,
                                           ScanConvertCredSchema,
                                           ScanDocumentCreateSchema,
                                           ScanExportSchema, ScanSchema)
from tenable.utils import dict_merge


class ScansAPI(ExploreBaseEndpoint):
    '''
    This will contain all methods related to scans
    '''
    schedule_const = IOConstants.ScanScheduleConst
    case_const = IOConstants.CaseConst
    _path = 'api/v3/scans'
    _conv_json = True
    _schema = ScanSchema()

    def _block_while_running(self, scan_id: UUID, sleeper: int = 5) -> None:
        '''
        A simple function to block while the scan_id specified is still in a
        running state.
        '''
        running = True
        while running:
            status = self.results(scan_id)['info']['status']
            if status[-2:].lower() == 'ed':
                running = False
            if running:
                time.sleep(sleeper)

    def _update_policy(self, kwargs: Dict, scan: Dict) -> None:
        policies = self._api.policies.list()
        match = False

        # Here we iterate over each policy in the list, looking
        # to see if we see a match in either the name or the id.  If we do
        # find a match, then we will use the first one that matches, pull
        # the editor config, and then use the policy id and scan policy
        # template uuid.
        for item in policies:
            if kwargs['policy'] in [item['name'],
                                    item['id']] and not match:
                policy_tmpl = self._api.editor.details(
                    'scan/policy', item['id']
                )
                scan['id'] = policy_tmpl['uuid']
                scan['settings']['policy_id'] = item['id']
                match = True

        # if no match was discovered, then raise an invalid warning.
        if not match:
            raise UnexpectedValueError('policy setting is invalid.')

    def _update_sub_doc_data(self, kwargs: Dict, scan: Dict) -> None:
        if 'scanner' in kwargs:
            scan['settings']['scanner_id'] = kwargs['scanner']
            del kwargs['scanner']

        # If the targets parameter is specified, then we will need to convert
        # the list of targets to a comma-delimited string and then set the
        # text_targets parameter with the result.
        if 'targets' in kwargs:
            scan['settings']['text_targets'] = kwargs['targets']
            del kwargs['targets']

        # The uploaded file, can be given in file targets,
        # then give the file name directly in the file target parameter
        if 'file_targets' in kwargs:
            scan['settings']['file_targets'] = kwargs['file_targets']

        # For credentials, we will simply push the dictionary as-is into the
        # the credentials.add sub-document.
        if 'credentials' in kwargs:
            scan['credentials'] = {'add': {}}
            scan['credentials']['add'] = kwargs['credentials']
            del kwargs['credentials']

        # Just like with credentials, we push the dictionary as-is into the
        # correct sub-document of the scan definition.
        if 'compliance' in kwargs:
            scan['audits'] = kwargs['compliance']
            del kwargs['compliance']

        if 'plugins' in kwargs:
            scan['plugins'] = kwargs['plugins']
            del kwargs['plugins']

    def _create_scan_document(self, kwargs: Dict) -> Dict:
        '''
        Takes the key-word arguments and will provide a scan settings document
        based on the values inputted.

        Args:
            kwargs (dict):
                The keyword dict passed from the user

        Returns:
            :obj:`dict`:
                The resulting scan document based on the kwargs provided.
        '''
        scan = {
            'settings': dict(),
        }
        # collection of run-time data from different APIs for schema validation
        context_data = dict()

        # If template is specified, then we will pull the listing of available
        # templates and set the policy UUID to match the template name given.
        templates = dict()
        if 'template' in kwargs:
            templates = self._api.policies.templates()
            templates_choices = list(templates.keys())
            context_data['templates_choices'] = templates_choices

        # If a policy UUID is sent, then we will set the scan template UUID to
        # be the UUID that was specified.
        if 'policy' in kwargs:
            self._update_policy(kwargs, scan)
            del kwargs['policy']

        # if the scanner attribute was set, then we will attempt to figure out
        # what scanner to use.
        if 'scanner' in kwargs:
            scanners = self._api.scanners.allowed_scanners()

            # We will want to attempt to enumerate the scanner list and if
            # we see a name match, replace the scanner name with the UUID
            # of the scanner instead.
            for item in scanners:
                if item['name'] == kwargs['scanner']:
                    kwargs['scanner'] = item['id']

            # we will always want to attempt to use the UUID first as it's
            # the cheapest check that we can run.
            scanners_choices = [s['id'] for s in scanners]
            context_data['scanners_choices'] = scanners_choices

        schema = ScanDocumentCreateSchema(context=context_data)
        kwargs = schema.dump(schema.load(kwargs))

        if 'template' in kwargs:
            scan['id'] = templates[kwargs['template']]
            del kwargs['template']

        self._update_sub_doc_data(kwargs, scan)
        # if the schedule_scan attribute was set, then we will apply fields
        # required for scheduling a scan
        if 'schedule_scan' in kwargs:
            if kwargs['schedule_scan']['enabled']:
                keys = [
                    self.schedule_const.enabled,
                    self.schedule_const.launch,
                    self.schedule_const.rrules,
                    self.schedule_const.schedule_scan,
                    self.schedule_const.start_time,
                    self.schedule_const.timezone,
                ]
            else:
                keys = [
                    self.schedule_const.enabled,
                    self.schedule_const.schedule_scan,
                ]

            # update schedule values in scan settings based on enable parameter
            for k in keys:
                scan['settings'][k] = kwargs['schedule_scan'][k]

            del kwargs['schedule_scan']

        # any remaining keyword arguments will be passed into the settings
        # sub-document. The bulk of the data should go here...
        scan['settings'] = dict_merge(scan['settings'], kwargs)
        return scan

    def _get_schedule_details(self, details: Dict) -> Dict:
        '''
        Existing schedule contains combined string of frequency, interval and
        BYDAY or BYMONTHDAY in rrules. we will Split existing schedule details
        to distributed schedule dictionary

        Args:
            details (dict):
                Dictionary of existing schedule

        Returns:
            :obj:`dict`:
                Distributed dictionary of the keys required for scan schedule.
        '''
        schedule = {}
        if details[self.schedule_const.rrules] is not None:
            rrules = dict(
                rules.split('=')
                for rules in details[self.schedule_const.rrules].split(';')
            )
            schedule = {
                self.schedule_const.frequency: rrules['FREQ'],
                self.schedule_const.interval: rrules['INTERVAL'],
                self.schedule_const.weekdays: rrules.get('BYDAY', '').split(),
                self.schedule_const.day_of_month: rrules.get(
                    'BYMONTHDAY', None
                ),
                self.schedule_const.start_time: datetime.strptime(
                    details[self.schedule_const.start_time],
                    self.schedule_const.time_format,
                )
                if details[self.schedule_const.start_time] is not None
                else None,
                self.schedule_const.timezone: details[
                    self.schedule_const.timezone
                ]
                if details[self.schedule_const.timezone] is not None
                else None,
            }
        return schedule

    def create_scan_schedule(self,
                             enabled: Optional[bool] = False,
                             frequency: Optional[str] = None,
                             interval: Optional[int] = None,
                             weekdays: Optional[list] = None,
                             day_of_month: Optional[int] = None,
                             starttime: Optional[datetime] = None,
                             timezone: Optional[str] = None,
                             ) -> Dict:
        '''
        Create dictionary of keys required for scan schedule

        Args:
            enabled (bool, optional):
                To enable/disable scan schedule
            frequency (str, optional):
                The frequency of the rule. The string input will be up-cased.
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
            starttime (datetime, optional):
                When the scan should start.
            timezone (str, optional):
                The timezone to use for the scan.  The default if none is
                specified is to use UTC.  For the list of usable timezones,
                please refer to :devportal:`scans-timezones`

        Returns:
            :obj:`dict`:
                Dictionary of the keys required for scan schedule.

        '''
        self._schema.load(dict(enabled=enabled))
        schedule = {}
        context_data = dict()
        kwargs = dict(
            frequency=frequency,
            interval=interval,
            weekdays=weekdays,
            day_of_month=day_of_month,
            starttime=starttime,
            timezone=timezone
        )

        context_data['existing_rules'] = {}  # only for schema structure
        context_data['timezone_choices'] = self._api._tz
        schema = ScanConfigureScheduleSchema(context=context_data)
        kwargs = schema.dump(schema.load(kwargs))
        if enabled is True:
            launch = kwargs['frequency']
            frequency = self.schedule_const.ffrequency.format(launch)
            rrules = {
                self.schedule_const.frequency: frequency,
                self.schedule_const.interval:
                    self.schedule_const.finterval.format(
                        kwargs['interval']
                    ),
                self.schedule_const.weekdays: None,
                self.schedule_const.day_of_month: None,
            }

            # if frequency is a weekly one, then we will need to specify the
            # days of the week that the exclusion is run on.
            if frequency == self.schedule_const.weekly_frequency:
                rrules[
                    self.schedule_const.weekdays
                ] = self.schedule_const.fbyweekday.format(
                    kwargs['weekdays']
                )
                # In the same vein as the frequency check, we're accepting
                # case-insensitive input, comparing it to our known list of
                # acceptable responses, then joining them all together into a
                # comma-separated string.

            # if the frequency is monthly, then we will need to specify
            # the day of
            # the month that the rule will run on.
            if frequency == self.schedule_const.monthly_frequency:
                rrules[
                    self.schedule_const.day_of_month
                ] = self.schedule_const.fbymonthday.format(
                    kwargs['day_of_month']
                )

            # Now we have to remove unused keys from rrules and create rrules
            # structure required by scan
            # 'FREQ=ONETIME;INTERVAL=1',FREQ=WEEKLY;INTERVAL=1;BYDAY=MO,TH,FR',
            # 'FREQ=MONTHLY;INTERVAL=1;BYMONTHDAY=22'
            schedule[self.schedule_const.rrules] = ';'.join(
                dict_clean(rrules).values()
            )

            # Set enable and launch key for schedule
            schedule[self.schedule_const.enabled] = True
            schedule[self.schedule_const.launch] = launch

            schedule[self.schedule_const.start_time] = kwargs['starttime']

            schedule[self.schedule_const.timezone] = kwargs['timezone']

            schedule[self.schedule_const.schedule_scan] = 'yes'

        if enabled is False:
            # Set enable and schedule_scan key for schedule
            schedule[self.schedule_const.enabled] = False
            schedule[self.schedule_const.schedule_scan] = 'no'

        return schedule

    def configure_scan_schedule(self,
                                scan_id: UUID,
                                enabled: Optional[bool] = None,
                                frequency: Optional[str] = None,
                                interval: Optional[int] = None,
                                weekdays: Optional[list] = None,
                                day_of_month: Optional[int] = None,
                                starttime: Optional[datetime] = None,
                                timezone: Optional[str] = None,
                                ) -> Dict:
        '''
        Create dictionary of keys required for scan schedule

        Args:
            scan_id (uuid): The id of the Scan object in Tenable.io
            enabled (bool, optional): To enable/disable scan schedule
            frequency (str, optional):
                The frequency of the rule. The string input will be up-cased.
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
            starttime (datetime, optional):
                When the scan should start.
            timezone (str, optional):
                The timezone to use for the scan.  The default if none is
                specified is to use UTC.  For the list of usable timezones,
                please refer to :devportal:`scans-timezones`

        Returns:
            :obj:`dict`:
                Dictionary of the keys required for scan schedule.

        '''
        self._schema.load(dict(enabled=enabled))
        kwargs = dict(
            frequency=frequency,
            interval=interval,
            weekdays=weekdays,
            day_of_month=day_of_month,
            starttime=starttime,
            timezone=timezone
        )
        context_data = dict()
        current = self.details(scan_id)['settings']
        if enabled in [True, False]:
            current[self.schedule_const.enabled] = enabled
        schedule = {}
        if current[self.schedule_const.enabled] is True:
            if current[self.schedule_const.rrules] is not None:
                # create existing schedule dictionary
                existing_rrules = {
                    self.schedule_const.enabled: current[
                        self.schedule_const.enabled
                    ],
                    self.schedule_const.schedule_scan: 'yes'
                    if current[self.schedule_const.enabled] is True
                    else 'no',
                    self.schedule_const.rrules: current[
                        self.schedule_const.rrules
                    ],
                    self.schedule_const.start_time: current[
                        self.schedule_const.start_time
                    ],
                    self.schedule_const.timezone: current[
                        self.schedule_const.timezone
                    ],
                }

                # Restructure existing_rrule with distributed values
                existing_rrules = self._get_schedule_details(existing_rrules)
            else:
                existing_rrules = {}
            context_data['existing_rules'] = existing_rrules
            context_data['timezone_choices'] = self._api._tz
            schema = ScanConfigureScheduleSchema(context=context_data)
            kwargs = schema.dump(schema.load(kwargs))
            launch = kwargs['frequency']

            frequency = self.schedule_const.ffrequency.format(launch)

            rrules = {
                self.schedule_const.frequency: frequency,
                self.schedule_const.interval:
                    self.schedule_const.finterval.format(kwargs['interval']),
                self.schedule_const.weekdays: None,
                self.schedule_const.day_of_month: None,
            }

            # if the frequency is weekly one, then we will need to specify the
            # days of the week that the exclusion is run on.
            if frequency == self.schedule_const.weekly_frequency:
                rrules[
                    self.schedule_const.weekdays
                ] = self.schedule_const.fbyweekday.format(kwargs['weekdays'])
                # In the same vein as the frequency check, we're accepting
                # case-insensitive input, comparing it to our known list of
                # acceptable responses, then joining them all together into a
                # comma-separated string.

            # if the frequency is monthly, then we will need to specify the
            # day of
            # the month that the rule will run on.
            if frequency == self.schedule_const.monthly_frequency:
                rrules[
                    self.schedule_const.day_of_month
                ] = self.schedule_const.fbymonthday.format(
                    kwargs['day_of_month'])

            # Now we have to remove unused keys from rrules and create rrules
            # structure required by scan
            # 'FREQ=ONETIME;INTERVAL=1',FREQ=WEEKLY;INTERVAL=1;BYDAY=MO,TH,FR',
            # 'FREQ=MONTHLY;INTERVAL=1;BYMONTHDAY=22'
            schedule[self.schedule_const.rrules] = ';'.join(
                dict_clean(rrules).values()
            )

            # Set enable and launch key for schedule
            schedule[self.schedule_const.enabled] = True
            schedule[self.schedule_const.launch] = launch

            schedule[self.schedule_const.start_time] = kwargs['starttime']

            schedule[self.schedule_const.timezone] = kwargs['timezone']
            schedule[self.schedule_const.schedule_scan] = 'yes'

            # merge updated schedule values to existing schedule
            dict_merge(existing_rrules, schedule)

            # remove extra keys after merge
            keys = [
                self.schedule_const.frequency,
                self.schedule_const.interval,
                self.schedule_const.weekdays,
                self.schedule_const.day_of_month,
            ]
            for k in keys:
                if k in existing_rrules:
                    del existing_rrules[k]

            return existing_rrules

        if current[self.schedule_const.enabled] is False:
            # Set enable and launch key for schedule
            schedule[self.schedule_const.enabled] = False
            schedule[self.schedule_const.schedule_scan] = 'no'
            return schedule

    def attachment(self,
                   scan_id: UUID,
                   attachment_id: UUID,
                   key: str,
                   fobj: Optional[BinaryIO] = None
                   ) -> BinaryIO:
        '''
        Retrieve an attachment  associated to a scan.

        :devportal:`scans: attachments <scans-attachments>`

        Args:
            scan_id (uuid.UUID):
                The unique identifier for the scan.
            attachment_id (uuid.UUID):
                The unique identifier for the attachment
            key (str):
                The attachment access token.
            fobj (FileObject, optional):
                a file-like object you wish for the
                attachment to be written to.  If none is specified, a BytesIO
                object will be returned with the contents of the attachment.

        Returns:
            :obj:`FileObject`:
                A file-like object with the attachment written into it.

        Examples:
            >>> with open('example.file', 'wb') as fobj:
            ...     tio.v3.vm.scans.attachment(
            ...     'aa57ae93-45e5-4316-8e16-501ebce4ecb7',
            ...     'aa57ae93-45e5-4316-8e16-501ebce4ecb7',
            ...     'abc',
            ...     fobj
            ...     )
        '''
        if not fobj:
            # if no file-like object is specified, then assign a BytesIO object
            # to the variable.
            fobj = BytesIO()
        params = dict(key=key)
        params = self._schema.dump(self._schema.load(params))

        # Make the HTTP call and stream the data into the file object.
        resp = self._get(
            f'{scan_id}/attachments/{attachment_id}',
            params=params,
            stream=True,
        )
        for chunk in resp.iter_content(chunk_size=1024):
            if chunk:
                fobj.write(chunk)
        fobj.seek(0)
        resp.close()

        # Return the file object to the caller.
        return fobj

    def configure(self, scan_id: UUID, **kw: Dict) -> Dict:
        '''
        Overwrite the parameters specified on top of the existing scan record.

        :devportal:`scans: configure <scans-configure>`

        Args:
            scan_id (uuid.UUID):
                The unique identifier for the scan.
            template (str, optional):
                The scan policy template to use.  If no template is specified
                then the default of `basic` will be used.
            policy (uuid, optional):
                The id or title of the scan policy to use (if not using one of
                the pre-defined templates).  Specifying a a policy id will
                override the the template parameter.
            targets (list, optional):
                If defined, then a list of targets can be specified and will
                be formatted to an appropriate text_target attribute.
            credentials (dict, optional):
                A list of credentials to use.
            compliance (dict, optional):
                A list of compliance audiots to use.
            scanner (str, optional):
                Define the scanner or scanner group uuid or name.
            schedule_scan (dict, optional):
                Define updated schedule for scan
            **kw (dict, optional):
                The various parameters that can be passed to the scan creation
                API.  Examples would be `name`, `email`, `scanner_id`, etc. For
                more detailed info, please refer to the API documentation
                linked above.  Further, any keyword arguments passed that are
                not explicitly documented will be automatically appended to the
                settings document.  There is no need to pass settings directly.

        Returns:
            :obj:`dict`:
                The scan resource record.

        Examples:
            >>>  tio.v3.vm.scans.configure(
            ...   '59042c90-5379-43a2-8cf4-87d97f7cb68f', name='New Scan Name')

            # configure a schedule for existing scan

            >>> configure_schedule = api.scans.configure_scan_schedule(
            ... '59042c90-5379-43a2-8cf4-87d97f7cb68f', interval=2)
            >>>  tio.v3.vm.scans.configure(
            ...  '59042c90-5379-43a2-8cf4-87d97f7cb68f',
            ...     schedule_scan=configure_schedule)
        '''

        # We will get the current scan record, generate the new parameters in
        # the correct format, and then merge them together to create the new
        # :func:`~.tenable.tenable_io.ScansAPI.details` method, however is not
        # scan record that we will be pushing to the API.
        current = self.details(scan_id)
        updated = self._create_scan_document(kw)
        scan = dict_merge(current, updated)
        scan = self.upsert_aws_credentials(scan)
        # Performing the actual call to the API with the updated scan record.
        return self._put(f'{scan_id}', json=scan)

    def upsert_aws_credentials(self, scan: Dict) -> Dict:
        '''
        Checks the credential dict of scan dict to derive operation add or edit
        This function assumes there are no edit credentials in the
        credentials dict.
        If there is any edit credentials,it would override the same.
        Args:
            scan (dict):
                scan object to update edit credential if it matches criteria
        Returns:
            :obj:`dict`:
                The scan with updated credentials.
        '''
        if 'credentials' in scan:
            aws_existing_credential_id = None
            if (
                    'current' in scan['credentials']
                    and 'Cloud Services' in scan['credentials']['current']
                    and 'Amazon AWS'
                    in scan['credentials']['current']['Cloud Services']
            ):
                aws_existing_credential = scan['credentials']['current'][
                    'Cloud Services'
                ]['Amazon AWS']
                if len(aws_existing_credential) == 1:
                    aws_existing_credential_id = aws_existing_credential[0][
                        'id'
                    ]
            if (
                    'add' in scan['credentials']
                    and 'Cloud Services' in scan['credentials']['add']
                    and 'Amazon AWS' in
                    scan['credentials']['add']['Cloud Services']
            ):
                aws_new_credential = scan['credentials']['add'][
                    'Cloud Services'
                ]['Amazon AWS']
                aws_new_credential_id = None
                if len(aws_new_credential) == 1:
                    aws_new_credential_id = aws_new_credential[0]['id']
                if (
                        aws_existing_credential_id is not None
                        and aws_existing_credential_id != aws_new_credential_id
                ):
                    scan['credentials']['edit'] = {
                        'Cloud Services': {
                            'Amazon AWS': scan['credentials']['add'][
                                'Cloud Services'
                            ]['Amazon AWS']
                        }
                    }
                    del scan['credentials']['add']['Cloud Services'][
                        'Amazon AWS'
                    ]
        return scan

    def copy(self,
             scan_id: UUID,
             folder_id: Optional[UUID] = None,
             name: Optional[str] = None
             ) -> Dict:
        '''
        Duplicates a scan and returns the details of the copy.

        :devportal:`scans: copy <scans-copy>`

        Args:
            scan_id (uuid):
                The unique identifier for the scan.
            folder_id (uuid, optional):
                The unique identifier for the folder.
            name (str, optional):
                The name for the copied scan.

        Returns:
            :obj:`dict`:
                The scan resource record for the copied scan.

        Examples:
            >>> new_scan =  tio.v3.vm.scans.copy(
            ...  '59042c90-5379-43a2-8cf4-87d97f7cb68f', 'New Scan Name')
        '''

        payload = dict_clean(dict(
            folder_id=folder_id,
            name=name
        ))
        payload = self._schema.dump(self._schema.load(payload))

        # make the call and return the resulting JSON document to the caller.
        return self._post(f'{scan_id}/copy', json=payload)

    def create(self, **kw: Dict) -> Dict:
        '''
        Create a new scan.

        :devportal:`scans: create <scans-create>`

        Args:
            name (str):
                The name of the scan to create.
            template (str, optional):
                The scan policy template to use.  If no template is specified
                then the default of `basic` will be used.
            policy (int, optional):
                The id or title of the scan policy to use (if not using one of
                the pre-defined templates).  Specifying a a policy id will
                override the the template parameter.
            targets (list, optional):
                If defined, then a list of targets can be specified and will
                be formatted to an appropriate text_target attribute.
            credentials (dict, optional):
                A list of credentials to use.
            compliance (dict, optional):
                A list of compliance audits to use.
            scanner (str, optional):
                Define the scanner or scanner group uuid or name.
            schedule_scan (dict, optional):
                Define schedule for scan
            **kw (dict, optional):
                The various parameters that can be passed to the scan creation
                API.  Examples would be `name`, `email`, `scanner_id`, etc. For
                more detailed info, please refer to the API documentation
                linked above.  Further, any keyword arguments passed that are
                not explicitly documented will be automatically appended to the
                settings document.  There is no need to pass settings directly.

        Returns:
            :obj:`dict`:
                The scan resource record of the newly created scan.

        Examples:
            Create an un-credentialed basic scan:

            >>> scan =  tio.v3.vm.scans.create(
            ...     name='Example Scan',
            ...     targets=['127.0.0.1'])

            Creating a scan with a set of managed credentials:

            >>> scan =  tio.v3.vm.scans.create(
            ...     name='Example Managed Cred Scan',
            ...     targets=['127.0.0.1'],
            ...     credentials={'Host': {'SSH': [{'id': 'CREDENTIAL-UUID'}]}}

            Creating a scan with a set of embedded credentials:

            >>> scan =  tio.v3.vm.scans.create(
            ...     name='Example Embedded Cred Scan',
            ...     targets=['127.0.0.1'],
            ...     credentials={'Host': {'Windows': [{
            ...         'domain': '',
            ...         'username': 'Administrator',
            ...         'password': 'sekretsquirrel',
            ...         'auth_method': 'Password'
            ...     }]}}
            ... )

            Create an un-credentialed basic scheduled scan:

            >>> schedule = api.scans.create_scan_schedule(
            ...     enabled=True, frequency='daily', interval=2,
            ... starttime=datetime.utcnow())
            >>> scan =  tio.v3.vm.scans.create(
            ...     name='Example Scan',
            ...     targets=['127.0.0.1']
            ...     schedule_scan=schedule)

            For further information on credentials, what settings to use, etc,
            refer to
            `this doc
             <https://developer.tenable.com/docs/determine-settings-for-credential-type>`_  # noqa E501
            on the developer portal.
        '''
        if 'template' not in kw:
            kw['template'] = 'basic'
        scan = self._create_scan_document(kw)

        # Run the API call and return the result to the caller.
        return self._post(json=scan)['scan']

    def delete(self, scan_id: UUID) -> None:
        '''
        Remove a scan.

        :devportal:`scans: delete <scans-delete>`

        Args:
            scan_id (uuid):
                The unique identifier for the scan.

        Returns:
            :obj:`None`:
                The scan was successfully deleted.

        Examples:
            >>>  tio.v3.vm.scans.delete('59042c90-5379-43a2-8cf4-87d97f7cb68f')
        '''
        self._delete(f'{scan_id}')

    # todo - get back to this once iterator is ready
    @pytest.mark.xfail(raises=NotImplementedError)
    def history(self,
                scan_id,
                limit=None,
                offset=None,
                pages=None,
                sort=None
                ):
        '''
        Get the scan history of a given scan from Tenable.io.

        :devportal:`scans: history <scans-history>`

        Args:
            scan_id (uuid):
                The unique identifier for the scan.
            limit (int, optional):
                The number of records to retrieve.  Default is 50
            offset (int, optional):
                The starting record to retrieve.  Default is 0.
            pages (int, optional):
                The number of pages to retrieve. Default None
            sort (tuple, optional):
                A tuple of tuples identifying the the field and sort order of
                the field.

        Returns:
            :obj:`ScanHistoryIterator`:
                An iterator that handles the page management of the requested
                records.

        Examples:
            >>> for history in  tio.v3.vm.scans.history(
            ...     '59042c90-5379-43a2-8cf4-87d97f7cb68f'):
            ...     pprint(history)
        '''
        # query = dict()
        # if sort and self._check('sort', sort, tuple):
        #     query['sort'] = ','.join(
        #         [
        #             '{}:{}'.format(
        #                 self._check('sort_field', i[0], str),
        #                 self._check(
        #                     'sort_direction',
        #                     i[1],
        #                     str,
        #                     choices=['asc', 'desc'],
        #                 ),
        #             )
        #             for i in sort
        #         ]
        #     )
        #
        # return ScanHistoryIterator(
        #     self._api,
        #     _limit=limit if limit else 50,
        #     _offset=offset if offset else 0,
        #     _pages_total=pages,
        #     _query=query,
        #     _path='scans/{}/history'.format(scan_id),
        #     _resource='history',
        # )
        raise NotImplementedError('This endpoint is not developed')

    def delete_history(self, scan_id: UUID, history_id: UUID) -> None:
        '''
        Remove an instance of a scan from a scan history.

        :devportal:`scans: delete-history <scans-delete-history>`

        Args:
            scan_id (uuid):
                The unique identifier for the scan.
            history_id (uuid):
                The unique identifier for the instance of the scan.

        Returns:
            :obj:`None`:
                Scan history successfully deleted.

        Examples:
            >>>  tio.v3.vm.scans.delete_history(
            ...     '59042c90-5379-43a2-8cf4-87d97f7cb68f',
            ...     '34567c90-5379-43a2-8cf4-87d97f7cb68f')
        '''
        self._delete(f'{scan_id}/history/{history_id}')

    def details(self, scan_id: UUID) -> Dict:
        '''
        Calls the editor API and parses the scan config details to return a
        document that closely matches what API expects to be POSTed or PUTed
        via the create and configure methods.  The compliance audits and
        credentials are populated into the 'current' sub-document for the
        relevant resources.

        .. important::
            Please note that the details method is reverse-engineered from the
            responses from the editor API, and while we're reasonably sure that
            the response should align almost exactly to what the API expects to
            be pushed to it, this method by very nature of what it's doing
            isn't guaranteed to always work.

        .. note::
            If you're looking for the results of the most recent scan, and what
            matches to the ``GET /scans/{id}`` call, then take a look at the
            results method.

        Args:
            scan_id (uuid): The unique identifier for the scan.

        Returns:
            :obj:`dict`:
                The scan configuration resource.

        Examples:
            >>> scan =  tio.v3.vm.scans.details(
            ...     '59042c90-5379-43a2-8cf4-87d97f7cb68f')
            >>> pprint(scan)
        '''
        return self._api.editor.details('scan', scan_id)

    def results(self,
                scan_id: UUID,
                history_id: Optional[UUID] = None
                ) -> Dict:
        '''
        Return the scan results from either the latest scan or a specific scan
        instance in the history.

        :devportal:`scans: details <scans-details>`

        Args:
            scan_id (uuid.UUID):
                The unique identifier for the scan.
            history_id (uuid.UUID, optional):
                The unique identifier for the instance of the scan.

        Returns:
            :obj:`dict`:
                The scan result dictionary.

        Examples:
            Retrieve the latest results:

            >>> results =  tio.v3.vm.scans.results(
            ...  '3bfcfb11-6c12-405b-b7ba-bbc705cd2a6e')

            Retrieve a specific instance of the result set:

            >>> results =  tio.v3.vm.scans.results(
            ...  '3bfcfb11-6c12-405b-b7ba-bbc705cd2a6e',
            ...  'asdcfb11-6c12-405b-b7ba-bbc705cd2a6e')
        '''
        params = dict_clean(dict(
            history_id=history_id
        ))
        params = self._schema.dump(self._schema.load(params))

        return self._get(f'{scan_id}', params=params)

    def export(self,
               scan_id: UUID,
               *filters: Optional[tuple],
               stream_hook: Optional[Callable] = None,
               **kw: Dict
               ) -> BinaryIO:
        '''
        Export the scan report.

        :devportal:`scans: export <scans-export-request>`

        Args:
            scan_id (uuid):
                The unique identifier of the scan.
            *filters (tuple, optional):
                A list of tuples detailing the filters that wish to be applied
                the response data.  Each tuple is constructed as
                ('filter', 'operator', 'value') and would look like the
                following example: `('plugin.id', 'eq', '19506')`.  For a
                complete list of the available filters and options, please
                refer to the API documentation linked above.
            stream_hook (callable, optional):
                If set, send the streaming response to this callable.
                The callable is
                responsible for iterating over the stream but does *not* need
                to close
                the file object. The signature for the callable is:

                .. code-block:: python

                    def f(response: requests.Response,
                          fobj: BytesIO,
                          chunk_size: int) -> BytesIO:

            history_id (uuid, optional):
                The unique identifier for the instance of the scan.
            format (str, optional):
                What format would you like the resulting data to be in.  The
                default would be nessus output. Available options are `nessus`,
                `csv`, `html`, `pdf`, `db`.  Default is `nessus`.
            password (str, optional):
                If the export format is `db`, then what is the password used to
                encrypt the NessusDB file.  This is a require parameter for
                NessusDB exports.
            chapters (list, optional):
                A list of the chapters to write for the report.  The chapters
                list is only required for PDF and HTML exports.  Available
                chapters are `vuln_hosts_summary`, `vuln_by_host`,
                `compliance_exec`, `remediations`, `vuln_by_plugin`, and
                `compliance`.  List order will denote output order.  Default is
                `vuln_by_host`.
            filter_type (str, optional):
                Are the filters exclusive (this AND this AND this) or inclusive
                (this OR this OR this).  Valid values are `and` and `or`.  The
                default setting is `and`.
            scan_type (str, optional):
                This parameter is required only when using the API with
                Web Application Scanning. Available option is 'web-app'.
            fobj (FileObject, optional):
                The file-like object to be returned with the exported data. If
                no object is specified, a BytesIO object is returned with the
                data.  While this is an optional parameter, it is highly
                recommended to use this param as exported files can be quite
                large, and BytesIO objects are stored in memory, not on disk.

        Returns:
            :obj:`FileObject`:
                The file-like object of the requested export.

        Examples:
            Export the full report of the latest instance of the scan:

            >>> with open('example.nessus', 'wb') as reportobj:
            ...      tio.v3.vm.scans.export(1, fobj=reportobj)

            Export a specific instance of the scan:

            >>> with open('example.nessus', 'wb') as reportobj:
            ...      tio.v3.vm.scans.export(1, history_id=1, fobj=reportobj)
        '''
        # todo => integrate the parse filter and wait for download method in
        #  v3 structure
        # initiate the payload and parameters dictionaries.  We are also
        # checking to see if the filters were passed as a keyword argument
        # instead of as an argument list.  As this seems to be a common
        # issue, we should be supporting this methodology.
        filters = self._check(
            'filters', kw.get('filters', filters), (list, tuple)
        )
        payload = self._parse_filters(
            filters, self._api.filters.scan_filters(), rtype='sjson'
        )
        if 'fobj' in kw:
            fobj = kw.pop('fobj')
        else:
            fobj = BytesIO()
        params = {}
        dl_params = {}
        schema = ScanExportSchema()
        kw = schema.dump(schema.load(kw))
        if 'history_id' in kw:
            params['history_id'] = kw['history_id']

        # Enable exporting of Web Application scans.
        if 'scan_type' in kw:
            dl_params['type'] = params['type'] = kw['scan_type']
        if 'password' in kw:
            payload['password'] = kw['password']
        payload['format'] = kw['format']

        # The chapters are sent to us in a list, and we need to collapse that
        # down to a comma-delimited string.
        payload['chapters'] = kw['chapters']
        if 'filter_type' in kw:
            payload['filter.search_type'] = kw['filter_type']

        # Now we need to set the FileObject. If one was passed to us, then lets
        # just use that, otherwise we will need to instantiate a BytesIO object
        # to push the data into.

        # The first thing that we need to do is make the request and get the
        # File id for the job.
        fid = self._post(
            f'{scan_id}/export', params=params, json=payload
        )['file']
        self._api._log.debug(f'Initiated scan export {fid}')

        # Next we will wait for the status of the export request to become
        # ready.
        _ = self._wait_for_download(
            'scans/{}/export/{}/status'.format(scan_id, fid),
            'scans',
            scan_id,
            fid,
            params=dl_params,
        )

        # Now that the status has reported back as "ready", we can actually
        # download the file.
        resp = self._get(
            f'{scan_id}/export/{fid}/download',
            params=dl_params,
            stream=True,
        )

        if stream_hook is not None:
            assert callable(stream_hook)
            # See issue 305 for an example stream_hook callable
            # https://github.com/tenable/pyTenable/issues/305
            stream_hook(resp, fobj, chunk_size=1024)
        else:
            # Lets stream the file into the file-like object...
            for chunk in resp.iter_content(chunk_size=1024):
                if chunk:
                    fobj.write(chunk)

        fobj.seek(0)
        resp.close()

        # Lastly lets return the FileObject to the caller.
        return fobj

    def host_details(self,
                     scan_id: UUID,
                     host_id: UUID,
                     history_id: Optional[UUID] = None,
                     ) -> Dict:
        '''
        Retrieve the host details from a specific scan.

        :devportal:`scans: host-details <scans-host-details>`

        Args:
            scan_id (uuid.UUID):
                The unique identifier for the scan.
            host_id (uuid.UUID):
                The unique identifier for the host within the scan.
            history_id (uuid.UUID, optional):
                The unique identifier for the instance of the scan.

        Returns:
            :obj:`dict`:
                The information related to the host requested.

        Examples:
            >>> host =  tio.v3.vm.scans.host_details(
            ...  '3bfcfb11-6c12-405b-b7ba-bbc705cd2a6e',
            ...  'adscfb11-6c12-405b-b7ba-bbc705cd2a6e')
        '''
        params = dict_clean(dict(
            history_id=history_id
        ))
        params = self._schema.dump(self._schema.load(params))

        return self._get(f'{scan_id}/hosts/{host_id}', params=params)

    def import_scan(self,
                    fobj: BinaryIO,
                    folder_id: Optional[UUID] = None,
                    password: Optional[str] = None,
                    aggregate: Optional[bool] = False
                    ) -> Dict:
        '''
        Import a scan report into Tenable.io.

        :devportal:`scans: import <scans-import>`

        Args:
            fobj (FileObject):
                The File-like object of the scan to import.
            folder_id (int, optional):
                The unique identifier for the folder to place the scan into.
            password (str, optional):
                The password needed to decrypt the file. This is only necessary
                for NessusDB files uploaded.
            aggregate (bool, optional):
                should the Nessus report be aggregated into the aggregate
                results?  The default is True.

        Returns:
            :obj:`dict`:
                The scan resource record for the imported scan.

        Examples:
            Import a .nessusv2 report:

            >>> with open('example.nessus', 'rb') as reportobj:
            ...      tio.v3.vm.scans.import(reportobj)

            Import a NessusDB report.

            >>> with open('example.db', 'rb') as reportobj:
            ...      tio.v3.vm.scans.import(reportobj, password='sekret')
        '''
        # First lets verify that the folder_id and password are typed correctly
        # before initiating any uploads.
        payload = dict_clean(dict(
            folder_id=folder_id,
            password=password,
            aggregate=aggregate
        ))
        payload = self._schema.dump(self._schema.load(payload))
        payload.pop('aggregate', None)

        # Upload the file to the Tenable.io and store the resulting filename in
        # the payload.
        payload['file'] = self._api.files.upload(fobj)

        # make the call to Tenable.io to import and then return the result to
        # the caller.
        return self._post(
            'import',
            json=payload,
            params={'include_aggregate': int(aggregate)},
        )

    def launch(self,
               scan_id: UUID,
               targets: Optional[list] = None
               ) -> str:
        '''
        Launches a scan.

        :devportal:`scans: launch <scans-launch>`

        Args:
            scan_id (uuid):
                The unique identifier for the scan.
            targets (list, optional):
                A list of targets to be scanned instead of the default targets
                in the scan.

        Response:
            :obj:`str`:
                The uuid of the scan instance (history).

        Examples:
            Launch the scan with the configured targets:

            >>>  tio.v3.vm.scans.launch(
            ...  '3bfcfb11-6c12-405b-b7ba-bbc705cd2a6e')

            Launch the scan with some custom targets:

            >>>  tio.v3.vm.scans.launch(
            ...  '3bfcfb11-6c12-405b-b7ba-bbc705cd2a6e', targets=['127.0.0.1'])
        '''
        payload = dict_clean(dict(
            alt_targets=targets
        ))
        payload = self._schema.dump(self._schema.load(payload))
        return self._post(
            f'{scan_id}/launch', json=payload
        )['scan_id']

    def search(self,
               **kw
               ) -> Union[SearchIterator, CSVChunkIterator, Response]:
        '''
        Retrieves the scans.
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
                the :py:meth: `tio.v3.definitions.vm.scans()` endpoint
                to get more details.
            sort (list[tuple], optional):
                sort is a list of tuples in the form of
                ('FIELD', 'ORDER').
                It describes how to sort the data
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
            >>> tio.v3.vm.scans.search(
            ...     filter=('name','eq','SCCM'),
            ...     fields=['name', 'field_one', 'field_two'],
            ...     limit=2,
            ...     sort=[('last_observed', 'asc')]
            ... )
        '''
        iclass = SearchIterator
        if kw.get('return_csv', False):
            iclass = CSVChunkIterator
        return super()._search(resource='scans',
                               iterator_cls=iclass,
                               api_path=f'{self._path}/search',
                               **kw
                               )

    def pause(self, scan_id: UUID, block: Optional[bool] = False) -> None:
        '''
        Pauses a running scan.

        :devportal:`scans: pause <scans-pause>`

        Args:
            scan_id (uuid):
                The unique identifier of the scan to pause.
            block (bool, optional):
                Block until the scan is actually paused.  Default is False.

        Returns:
            :obj:`None`:
                The scan was successfully requested to be paused.

        Examples:
            >>>  tio.v3.vm.scans.pause(
            ...  '3bfcfb11-6c12-405b-b7ba-bbc705cd2a6e')
        '''
        self._post(f'{scan_id}/pause', json={})
        if block:
            self._block_while_running(scan_id)

    def set_read_status(self, scan_id: UUID, read_status: bool) -> None:
        '''
        Sets the read status of the scan.  This is generally used to toggle the
        unread status of the scan within the UI.

        :devportal:`scans: read-status <scans-read-status>`

        Args:
            scan_id (uuid):
                The unique identifier for the scan.
            read_status (bool):
                Is the scan in a read or unread state?  True would denote read,
                whereas False is unread.

        Returns:
            :obj:`None`:
                The status of the scan was updated.

        Examples:
            Set a scan to unread:

            >>>  tio.v3.vm.scans.set_read_status(
            ...  '3bfcfb11-6c12-405b-b7ba-bbc705cd2a6e', False)
        '''
        payload = self._schema.dump(self._schema.load(dict(
            read_status=read_status
        )))
        self._put(
            f'{scan_id}/status',
            json=payload,
        )

    def resume(self, scan_id: UUID) -> None:
        '''
        Resume a paused scan.

        :devportal:`scans: resume <scans-resume>`

        Args:
            scan_id (uuid):
                The unique identifier for the scan.

        Returns:
            :obj:`None`:
                The scan was successfully requested to resume.

        Examples:
            >>>  tio.v3.vm.scans.resume(
            ...  '3bfcfb11-6c12-405b-b7ba-bbc705cd2a6e')
        '''
        self._post(f'{scan_id}/resume')

    def schedule(self, scan_id: UUID, enabled: bool) -> Dict:
        '''
        Enables or disables the scan schedule.

        :devportal:`scans: schedule <scans-schedule>`

        Args:
            scan_id (uuid.UUID):
                The unique identifier for the scan.
            enabled (bool):
                Enables or Disables the scan scheduling.

        Returns:
            :obj:`dict`:
                The schedule resource record for the scan.

        Examples:
            Enable a scan schedule:

            >>>  tio.v3.vm.scans.schedule(
            ...  'aa57ae93-45e5-4316-8e16-501ebce4ecb7',
            ...     True)
        '''
        payload = self._schema.dump(self._schema.load(dict(
            enabled=enabled
        )))
        return self._put(
            f'{scan_id}/schedule',
            json=payload,
        )

    def stop(self, scan_id: UUID, block: bool = False) -> None:
        '''
        Stop a running scan.

        :devportal:`scans: stop <scans-stop>`

        Args:
            scan_id (uuid.UUID):
                The unique identifier for the scan.
            block (bool, optional):
                Block until the scan is actually stopped.  Default is False.

        Returns:
            :obj:`None`:
                The scan was successfully requested to stop.

        Examples:
            Stop the scan asynchronously:

            >>>  tio.v3.vm.scans.stop(
            ...  '3bfcfb11-6c12-405b-b7ba-bbc705cd2a6e')

            Stop the scan and wait for the scan to stop:

            >>>  tio.v3.vm.scans.stop(
            ...  '3bfcfb11-6c12-405b-b7ba-bbc705cd2a6e', True)
        '''
        self._post(f'{scan_id}/stop')
        if block:
            self._block_while_running(scan_id)

    def status(self, scan_id: UUID) -> str:
        '''
        Get the status of the latest instance of the scan.

        :devportal:`scans: get-latest-status <scans-get-latest-status>`

        Args:
            scan_id (int or uuid): The unique identifier for the scan.

        Returns:
            :obj:`str`:
                The current status of the last instance.

        Examples:
            >>>  tio.v3.vm.scans.status(
            ...  '3bfcfb11-6c12-405b-b7ba-bbc705cd2a6e')
            u'completed'
        '''
        return self._get(f'{scan_id}/latest-status')['status']


    def timezones(self) -> list:
        '''
        Retrieves the list of timezones.
        :devportal:`scans: timezones <scans-timezones>`

        Returns:
            :obj:`list`:
                List of allowed timezone strings accepted by Tenable.IO

        Examples:
            >>> for item in  tio.v3.vm.scans.timezones():
            ...     pprint(item)
        '''
        resp = self._get('timezones')['timezones']
        return [i['value'] for i in resp]


    def info(self, scan_id: UUID, history_id: UUID) -> Dict:
        '''
        Retrieves information about the status of the specified instance
        of the scan.

        :devportal:`scan: get-scan-history <scans-history-by-scan-id>`

        Args:
            scan_id (uuid.UUID):
                The unique identifier for the scan.
            history_id (uuid.UUID):
                The unique identifier for the scan instance.

        Returns:
            :obj:`dict`:
                The metadata about the scan instance specified.

        Examples:
            >>> info =  tio.v3.vm.scans.info(
            ... 'aa57ae93-45e5-4316-8e16-501ebce4ecb7',
            ...  'BA0ED610-C27B-4096-A8F4-3189279AFFE7')
        '''
        return self._get(f'{scan_id}/history/{history_id}')

    def check_auto_targets(self,
                           limit: int,
                           matched_resource_limit: int,
                           network_id: Optional[UUID] = None,
                           tags: Optional[list] = None,
                           targets: Optional[list] = None,
                           ) -> Dict:
        '''
        Evaluates a list of targets and/or tags against
        the scan route configuration of scanner groups.

        :devportal:`scan: check-auto-targets <scans-check-auto-targets>`

        Args:
            limit (int):
                Limit the number of missed targets returned in the response.
            matched_resource_limit (int):
                Limit the number of matched resource UUIDs returned in the
                 response.
            network_id (uuid, optional):
                The UUID of the network.
            tags (list, optional):
                A list of asset tags UUIDs.
            targets (list, optional):
                A list of valid targets.

        Returns:
            :obj:`dict`:
                Return the list of missed targets (if any), and
                the list of matched scanner groups (if any).

        Examples:
            >>> scan_routes_info =  tio.v3.vm.scans.check_auto_targets(
            ... '59042c90-5379-43a2-8cf4-87d97f7cb68f',
            ... '65042c90-5379-43a2-8cf4-87d97f7cb68f', targets=['127.0.0.1'])
        '''
        query = {
            'limit': limit,
            'matched_resource_limit': matched_resource_limit,
        }

        query = self._schema.dump(self._schema.load(query))

        payload = dict_clean(dict(
            network_id=network_id,
            tags=tags,
            target_list=targets
        ))
        schema = ScanCheckAutoTargetSchema()
        payload = schema.dump(schema.load(payload))

        return self._post(
            'check-auto-targets', params=query, json=payload
        )

    def convert_credentials(self,
                            cred_id: UUID,
                            scan_id: UUID,
                            cred_name: Optional[str] = None,
                            cred_type: Optional[str] = None,
                            permissions: Optional[list] = None,
                            ad_hoc: Optional[bool] = None,
                            category: Optional[str] = None,
                            **settings: Optional[dict]
                            ) -> str:
        '''
        Convert the Credentials.

        :devportal:`credentials: create <credentials-create>`

        Args:
            cred_id (uuid.UUID):
                Credentials uuid
            scan_id (uuid.UUID):
                Scan uuid
            ad_hoc (bool, optional):
                Determines whether the credential is managed (``False``) or an
                embedded credential in a scan or policy (``True``).
            cred_name (str, optional):
                The name of the credential.
            category (str, optional):
                The name of the category

                Examples: ('host').

            cred_type (str, optional):
                A type for the credential

                Examples: (windows).

            permissions (list, optional):
                A list of permissions (in either tuple or native dict format)
                detailing whom is allowed to use or edit this credential set.
                For the dictionary format, refer to the API docs.  The tuple
                format uses the customary ``(type, perm, uuid)`` format.

                Examples:
                    - ``('user', 32, user_id)``
                    - ``('group', 32, group_id)``
                    - ``('user', 'use', user_id)``
                    - ``('group', 'edit', group_id)``

            **settings (dict, optional):
                Additional keywords passed will be added to the settings dict
                within the API call.  As this dataset can be highly variable,
                it will not be validated and simply passed as-is.

        Returns:
            :obj:`str`:
                The status of the update process.

        Examples:
            >>> cred_id = '00000000-0000-0000-0000-000000000000'
            >>> scan_id = '00000000-0000-0000-0000-000000000000'
            >>> tio.v3.vm.scans.credentials(cred_id)
        '''
        current = self._api.credentials.details(cred_id)

        if not cred_name:
            cred_name = current.get('name')
        if not cred_type:
            cred_type = current.get('type')['name']
        if not ad_hoc:
            ad_hoc = current.get('ad_hoc')
        if not category:
            category = current.get('category')['name']

        settings = dict_merge(current.get('settings'), settings)
        schema = ScanConvertCredSchema()
        payload = dict_clean(dict(
            name=cred_name,
            ad_hoc=ad_hoc,
            permissions=permissions,
            category=category,
            type=cred_type,
            settings=settings
        ))
        payload = schema.dump(schema.load(payload))
        return self._post(f'{scan_id}/credentials/{cred_id}/upgrade',
                          json=payload)['id']

