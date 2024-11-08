'''
Scans
=====

The following methods allow for interaction into the Tenable Vulnerability Management
:devportal:`scans <scans>` API endpoints.

Methods available on ``tio.scans``:

.. rst-class:: hide-signature
.. autoclass:: ScansAPI
    :members:
'''
import time
import warnings
from typing import Union, Optional, List, Dict, Tuple, Callable
from uuid import UUID
from datetime import datetime, timedelta
from io import BytesIO
from restfly.utils import dict_clean
from tenable.constants import IOConstants
from tenable.utils import dict_merge
from tenable.errors import UnexpectedValueError
from tenable.io.base import TIOEndpoint, TIOIterator


class ScanHistoryIterator(TIOIterator):
    '''
    The agents iterator provides a scalable way to work through scan history
    result sets of any size.  The iterator will walk through each page of data,
    returning one record at a time.  If it reaches the end of a page of
    records, then it will request the next page of information and then continue
    to return records from the next page (and the next, and the next) until the
    counter reaches the total number of records that the API has reported.

    Attributes:
        count (int): The current number of records that have been returned
        page (list):
            The current page of data being walked through.  pages will be
            cycled through as the iterator requests more information from the
            API.
        page_count (int): The number of record returned from the current page.
        total (int):
            The total number of records that exist for the current request.
    '''
    pass


class ScansAPI(TIOEndpoint):
    '''
    This will contain all methods related to scans
    '''
    _box = True
    _path = 'scans'
    schedule_const = IOConstants.ScanScheduleConst
    case_const = IOConstants.CaseConst

    def _block_while_running(self, scan_id, sleeper=5):
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

    def _create_scan_document(self, kwargs):
        '''
        Takes the key-worded arguments and will provide a scan settings document
        based on the values inputted.

        Args:
            kwargs (dict): The keyword dict passed from the user

        Returns:
            :obj:`dict`:
                The resulting scan document based on the kwargs provided.
        '''
        scan = {
            'settings': dict(),
        }

        # If a template is specified, then we will pull the listing of available
        # templates and set the policy UUID to match the template name given.
        if 'template' in kwargs:
            templates = self._api.policies.templates()
            scan['uuid'] = templates[self._check(
                'template', kwargs['template'], str,
                default='basic',
                choices=list(templates.keys())
            )]
            del kwargs['template']

        # If a policy UUID is sent, then we will set the scan template UUID to
        # be the UUID that was specified.
        if 'policy' in kwargs:
            policies = self._api.policies.list()
            match = False

            # Here we are going to iterate over each policy in the list, looking
            # to see if we see a match in either the name or the id.  If we do
            # find a match, then we will use the first one that matches, pull
            # the editor config, and then use the policy id and scan policy
            # template uuid.
            for item in policies:
                if kwargs['policy'] in [item['name'], item['id']] and not match:
                    policy_tmpl = self._api.editor.details('scan/policy', item['id'])
                    scan['uuid'] = policy_tmpl['uuid']
                    scan['settings']['policy_id'] = item['id']
                    match = True

            # if no match was discovered, then raise an invalid warning.
            if not match:
                raise UnexpectedValueError('policy setting is invalid.')
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
            scan['settings']['scanner_id'] = self._check(
                'scanner', kwargs['scanner'], 'scanner-uuid',
                choices=[s['id'] for s in scanners])
            del kwargs['scanner']

        # If the targets parameter is specified, then we will need to convert
        # the list of targets to a comma-delimited string and then set the
        # text_targets parameter with the result.
        if 'targets' in kwargs:
            scan['settings']['text_targets'] = ','.join(self._check(
                'targets', kwargs['targets'], list))
            del kwargs['targets']

        # The uploaded file, can be given in file targets,
        # then give the file name directly in the file target parameter
        if 'file_targets' in kwargs:
            scan['settings']['file_targets'] = self._check('file_targets', kwargs['file_targets'],str)

        # For credentials, we will simply push the dictionary as-is into the
        # the credentials.add sub-document.
        if 'credentials' in kwargs:
            scan['credentials'] = {'add': dict()}
            scan['credentials']['add'] = self._check(
                'credentials', kwargs['credentials'], dict)
            del kwargs['credentials']

        # Just like with credentials, we will push the dictionary as-is into the
        # correct sub-document of the scan definition.
        if 'compliance' in kwargs:
            scan['audits'] = self._check('compliance', kwargs['compliance'], dict)
            del kwargs['compliance']

        if 'plugins' in kwargs:
            scan['plugins'] = self._check('plugins', kwargs['plugins'], dict)
            del kwargs['plugins']

        # if the schedule_scan attribute was set, then we will apply fields
        # required for scheduling a scan
        if 'schedule_scan' in kwargs:
            self._check('schedule_scan', kwargs['schedule_scan'], dict)
            if kwargs['schedule_scan']['enabled']:
                keys = [self.schedule_const.enabled, self.schedule_const.launch, self.schedule_const.rrules,
                        self.schedule_const.schedule_scan, self.schedule_const.start_time, self.schedule_const.timezone]
            else:
                keys = [self.schedule_const.enabled, self.schedule_const.schedule_scan]

            # update schedule values in scan settings based on enable parameter
            for k in keys:
                scan['settings'][k] = kwargs['schedule_scan'][k]

            del (kwargs['schedule_scan'])

        # any other remaining keyword arguments will be passed into the settings
        # sub-document.  The bulk of the data should go here...
        scan['settings'] = dict_merge(scan['settings'], kwargs)
        return scan

    def _get_schedule_details(self, details):
        '''
        Existing schedule contains combined string of frequency, interval and
        BYDAY or BYMONTHDAY in rrules. we will Split existing schedule details to
        distributed schedule dictionary

        Args:
            details (dict): Dictionary of existing schedule

        Returns:
            :obj:`dict`:
                Distributed dictionary of the keys required for scan schedule.
        '''
        schedule = {}
        if details[self.schedule_const.rrules] is not None:
            rrules = dict(rules.split('=') for rules in details[self.schedule_const.rrules].split(';'))
            schedule = {
                self.schedule_const.frequency: rrules['FREQ'],
                self.schedule_const.interval: rrules['INTERVAL'],
                self.schedule_const.weekdays: rrules.get('BYDAY', '').split(),
                self.schedule_const.day_of_month: rrules.get('BYMONTHDAY', None),
                self.schedule_const.start_time: datetime.strptime(
                    details[self.schedule_const.start_time], self.schedule_const.time_format)
                if details[self.schedule_const.start_time] is not None else None,
                self.schedule_const.timezone: details[self.schedule_const.timezone]
                if details[self.schedule_const.timezone] is not None else None,
            }
        return schedule

    def create_scan_schedule(self, enabled=False, frequency=None, interval=None,
                             weekdays=None, day_of_month=None, starttime=None, timezone=None):
        '''
        Create dictionary of keys required for scan schedule

        Args:
            enabled (bool, optional): To enable/disable scan schedule
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
            starttime (datetime, optional): When the scan should start.
            timezone (str, optional):
                The timezone to use for the scan.  The default if none is
                specified is to use UTC.  For the list of usable timezones,
                please refer to :devportal:`scans-timezones <scans-timezones>`

        Returns:
            :obj:`dict`:
                Dictionary of the keys required for scan schedule.

        '''
        self._check(self.schedule_const.enabled, enabled, bool)
        schedule = {}

        if enabled is True:
            launch = self._check(self.schedule_const.frequency, frequency, str,
                                 choices=self.schedule_const.frequency_choice,
                                 default=self.schedule_const.frequency_default,
                                 case=self.case_const.uppercase)
            frequency = self.schedule_const.ffrequency.format(launch)
            rrules = {
                self.schedule_const.frequency: frequency,
                self.schedule_const.interval: self.schedule_const.finterval.format(
                    self._check(self.schedule_const.interval, interval, int,
                                default=self.schedule_const.interval_default)),
                self.schedule_const.weekdays: None,
                self.schedule_const.day_of_month: None
            }

            # if the frequency is a weekly one, then we will need to specify the
            # days of the week that the exclusion is run on.
            if frequency == self.schedule_const.weekly_frequency:
                rrules[self.schedule_const.weekdays] = self.schedule_const.fbyweekday.format(','.join(self._check(
                    self.schedule_const.weekdays, weekdays, list,
                    choices=self.schedule_const.weekdays_default,
                    default=self.schedule_const.weekdays_default,
                    case=self.case_const.uppercase)))
                # In the same vein as the frequency check, we're accepting
                # case-insensitive input, comparing it to our known list of
                # acceptable responses, then joining them all together into a
                # comma-separated string.

            # if the frequency is monthly, then we will need to specify the day of
            # the month that the rule will run on.
            if frequency == self.schedule_const.monthly_frequency:
                rrules[self.schedule_const.day_of_month] = self.schedule_const.fbymonthday.format(
                    self._check(self.schedule_const.day_of_month, day_of_month, int,
                                choices=self.schedule_const.day_of_month_choice,
                                default=self.schedule_const.day_of_month_default))

            # Now we have to remove unused keys from rrules and create rrules structure required by scan
            # 'FREQ=ONETIME;INTERVAL=1', FREQ=WEEKLY;INTERVAL=1;BYDAY=MO,TH,FR', 'FREQ=MONTHLY;INTERVAL=1;BYMONTHDAY=22'
            schedule[self.schedule_const.rrules] = ';'.join(dict_clean(rrules).values())

            # Set enable and launch key for schedule
            schedule[self.schedule_const.enabled] = True
            schedule[self.schedule_const.launch] = launch

            # starttime is rounded-off to 30 min schedule to match with values used in UI
            # will assign schedule datetime in (19700101T013000) format
            starttime = self._check(self.schedule_const.start_time, starttime, datetime,
                                    default=self.schedule_const.start_time_default)
            secs = timedelta(minutes=30).total_seconds()
            starttime = datetime.fromtimestamp(starttime.timestamp() + secs - starttime.timestamp() % secs)
            schedule[self.schedule_const.start_time] = starttime.strftime(self.schedule_const.time_format)

            schedule[self.schedule_const.timezone] = self._check(self.schedule_const.timezone, timezone, str,
                                                                 choices=self._api._tz,
                                                                 default=self.schedule_const.timezone_default)

            schedule[self.schedule_const.schedule_scan] = 'yes'

        if enabled is False:
            # Set enable and schedule_scan key for schedule
            schedule[self.schedule_const.enabled] = False
            schedule[self.schedule_const.schedule_scan] = 'no'

        return schedule

    def configure_scan_schedule(self, scan_id, enabled=None, frequency=None, interval=None,
                                weekdays=None, day_of_month=None, starttime=None, timezone=None):
        '''
        Create dictionary of keys required for scan schedule

        Args:
            scan_id (int): The id of the Scan object in Tenable Vulnerability Management
            enabled (bool, optional): To enable/disable scan schedule
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
            starttime (datetime, optional): When the scan should start.
            timezone (str, optional):
                The timezone to use for the scan.  The default if none is
                specified is to use UTC.  For the list of usable timezones,
                please refer to :devportal:`scans-timezones <scans-timezones>`

        Returns:
            :obj:`dict`:
                Dictionary of the keys required for scan schedule.

        '''
        current = self.details(self._check('scan_id', scan_id, int))['settings']
        if enabled in [True, False]:
            current[self.schedule_const.enabled] = self._check(self.schedule_const.enabled, enabled, bool)
        schedule = {}
        if current[self.schedule_const.enabled] is True:
            if current[self.schedule_const.rrules] is not None:
                # create existing schedule dictionary
                existing_rrules = {
                    self.schedule_const.enabled: current[self.schedule_const.enabled],
                    self.schedule_const.schedule_scan: 'yes' if current[self.schedule_const.enabled] is True else 'no',
                    self.schedule_const.rrules: current[self.schedule_const.rrules],
                    self.schedule_const.start_time: current[self.schedule_const.start_time],
                    self.schedule_const.timezone: current[self.schedule_const.timezone]
                }

                # Restructure existing_rrule with distributed values
                existing_rrules = self._get_schedule_details(existing_rrules)
            else:
                existing_rrules = {}

            launch = self._check(self.schedule_const.frequency, frequency, str,
                                 choices=self.schedule_const.frequency_choice,
                                 default=existing_rrules.get(self.schedule_const.frequency, None) or
                                         self.schedule_const.frequency_default,
                                 case=self.case_const.uppercase)

            frequency = self.schedule_const.ffrequency.format(launch)

            rrules = {
                self.schedule_const.frequency: frequency,
                self.schedule_const.interval: self.schedule_const.finterval.format(
                    self._check(self.schedule_const.interval, interval, int,
                                default=existing_rrules.get(self.schedule_const.interval, None)
                                        or self.schedule_const.interval_default)),
                self.schedule_const.weekdays: None,
                self.schedule_const.day_of_month: None
            }

            # if the frequency is a weekly one, then we will need to specify the
            # days of the week that the exclusion is run on.
            if frequency == self.schedule_const.weekly_frequency:
                rrules[self.schedule_const.weekdays] = self.schedule_const.fbyweekday.format(','.join(self._check(
                    self.schedule_const.weekdays, weekdays, list,
                    choices=self.schedule_const.weekdays_default,
                    default=existing_rrules.get(self.schedule_const.weekdays, '') or
                            self.schedule_const.weekdays_default,
                    case=self.case_const.uppercase)))
                # In the same vein as the frequency check, we're accepting
                # case-insensitive input, comparing it to our known list of
                # acceptable responses, then joining them all together into a
                # comma-separated string.

            # if the frequency is monthly, then we will need to specify the day of
            # the month that the rule will run on.
            if frequency == self.schedule_const.monthly_frequency:
                rrules[self.schedule_const.day_of_month] = self.schedule_const.fbymonthday.format(
                    self._check(self.schedule_const.day_of_month, day_of_month, int,
                                choices=self.schedule_const.day_of_month_choice,
                                default=existing_rrules.get(self.schedule_const.day_of_month, None)
                                        or self.schedule_const.day_of_month_default))

            # Now we have to remove unused keys from rrules and create rrules structure required by scan
            # 'FREQ=ONETIME;INTERVAL=1', FREQ=WEEKLY;INTERVAL=1;BYDAY=MO,TH,FR', 'FREQ=MONTHLY;INTERVAL=1;BYMONTHDAY=22'
            schedule[self.schedule_const.rrules] = ';'.join(dict_clean(rrules).values())

            # Set enable and launch key for schedule
            schedule[self.schedule_const.enabled] = True
            schedule[self.schedule_const.launch] = launch

            # starttime is rounded-off to 30 min schedule and
            # will assign schedule datetime in (19700101T011223) manner
            starttime = self._check(self.schedule_const.start_time, starttime, datetime,
                                    default=existing_rrules.get(self.schedule_const.start_time, None)
                                            or self.schedule_const.start_time_default)
            secs = timedelta(minutes=30).total_seconds()
            starttime = datetime.fromtimestamp(starttime.timestamp() + secs - starttime.timestamp() % secs)
            schedule[self.schedule_const.start_time] = starttime.strftime(self.schedule_const.time_format)

            schedule[self.schedule_const.timezone] = self._check(self.schedule_const.timezone, timezone, str,
                                                                 choices=self._api._tz, default=existing_rrules.get(
                    self.schedule_const.timezone, None)
                                                                                                or self.schedule_const.timezone_default)

            schedule[self.schedule_const.schedule_scan] = 'yes'

            # merge updated schedule values to existing schedule
            dict_merge(existing_rrules, schedule)

            # remove extra keys after merge
            keys = [self.schedule_const.frequency, self.schedule_const.interval,
                    self.schedule_const.weekdays, self.schedule_const.day_of_month]
            for k in keys:
                if k in existing_rrules:
                    del (existing_rrules[k])

            return existing_rrules

        if current[self.schedule_const.enabled] is False:
            # Set enable and launch key for schedule
            schedule[self.schedule_const.enabled] = False
            schedule[self.schedule_const.schedule_scan] = 'no'
            return schedule

    def attachment(self,
                   scan_id: Union[int, UUID],
                   attachment_id: int,
                   key: str,
                   fobj: Optional[BytesIO] = None
                   ) -> BytesIO:
        '''
        Retrieve an attachment  associated to a scan.

        :devportal:`scans: attachments <scans-attachments>`

        Args:
            scan_id (int): The unique identifier for the scan.
            attachment_id (int): The unique identifier for the attachment
            key (str): The attachment access token.
            fobj (FileObject, optional): a file-like object you wish for the
                attachment to be written to.  If none is specified, a BytesIO
                object will be returned with the contents of the attachment.

        Returns:
            :obj:`FileObject`:
                A file-like object with the attachment written into it.

        Examples:
            >>> with open('example.file', 'wb') as fobj:
            ...     tio.scans.attachment(1, 1, 'abc', fobj)
        '''
        if not fobj:
            # if no file-like object is specified, then assign a BytesIO object
            # to the variable.
            fobj = BytesIO()

        # Make the HTTP call and stream the data into the file object.
        resp = self._get(f'{scan_id}/attachments/{attachment_id}',
                         params={'key': key},
                         stream=True
                         )
        for chunk in resp.iter_content(chunk_size=1024):
            if chunk:
                fobj.write(chunk)
        fobj.seek(0)
        resp.close()

        # Return the file object to the caller.
        return fobj

    def configure(self, scan_id: Union[int, UUID], **kw) -> Dict:
        '''
        Overwrite the parameters specified on top of the existing scan record.

        :devportal:`scans: configure <scans-configure>`

        Args:
            scan_id (int): The unique identifier for the scan.
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
                A list of compliance audiots to use.
            scanner (str, optional):
                Define the scanner or scanner group uuid or name.
            schedule_scan (dict, optional):
                Define updated schedule for scan
            **kw (dict, optional):
                The various parameters that can be passed to the scan creation
                API.  Examples would be `name`, `email`, `scanner_id`, etc.  For
                more detailed information, please refer to the API documentation
                linked above.  Further, any keyword arguments passed that are
                not explicitly documented will be automatically appended to the
                settings document.  There is no need to pass settings directly.

        Returns:
            :obj:`dict`:
                The scan resource record.

        Examples:
            >>> tio.scans.configure(1, name='New Scan Name')

            # configure a schedule for existing scan

            >>> configure_schedule = api.scans.configure_scan_schedule(1, interval=2)
            >>> tio.scans.configure(1, schedule_scan=configure_schedule)
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

    def upsert_aws_credentials(self, scan):
        '''
        Checks the credential dict of scan dict to derive operation add or edit.
        This function assumes there are no edit credentials in the credentials dict.
        If there is any edit credentials,it would override the same.
        Args:
            scan: scan object to update edit credential if it matches criteria
        Returns:
            :obj:`dict`:
                The scan with updated credentials.
        '''
        if 'credentials' in scan:
            aws_existing_credential_id = None
            if 'current' in scan['credentials'] \
                    and 'Cloud Services' in scan['credentials']['current'] \
                    and 'Amazon AWS' in scan['credentials']['current']['Cloud Services']:
                aws_existing_credential = scan['credentials']['current']['Cloud Services']['Amazon AWS']
                if len(aws_existing_credential) == 1:
                    aws_existing_credential_id = aws_existing_credential[0]['id']
            if 'add' in scan['credentials'] \
                    and 'Cloud Services' in scan['credentials']['add'] \
                    and 'Amazon AWS' in scan['credentials']['add']['Cloud Services']:
                aws_new_credential = scan['credentials']['add']['Cloud Services']['Amazon AWS']
                aws_new_credential_id = None
                if len(aws_new_credential) == 1:
                    aws_new_credential_id = aws_new_credential[0]['id']
                if aws_existing_credential_id is not None and aws_existing_credential_id != aws_new_credential_id:
                    scan['credentials']['edit'] = \
                        {'Cloud Services': {'Amazon AWS': scan['credentials']['add']['Cloud Services']['Amazon AWS']}}
                    del scan['credentials']['add']['Cloud Services']['Amazon AWS']
        return scan

    def copy(self, scan_id, folder_id=None, name=None):
        '''
        Duplicates a scan and returns the details of the copy.

        :devportal:`scans: copy <scans-copy>`

        Args:
            scan_id (int): The unique identifier for the scan.
            folder_id (int, optional): The unique identifier for the folder.
            name (str, optional): The name for the copied scan.

        Returns:
            :obj:`dict`:
                The scan resource record for the copied scan.

        Examples:
            >>> new_scan = tio.scans.copy(1, 'New Scan Name')
        '''

        # Construct the request payload.
        payload = dict()
        if folder_id:
            payload['folder_id'] = self._check('folder_id', folder_id, int)
        if name:
            payload['name'] = self._check('name', name, str)

        # make the call and return the resulting JSON document to the caller.
        return self._api.post('scans/{}/copy'.format(scan_id),
                              json=payload).json()

    def create(self, **kw):
        '''
        Create a new scan.

        :devportal:`scans: create <scans-create>`

        Args:
            name (str): The name of the scan to create.
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
                API.  Examples would be `name`, `email`, `scanner_id`, etc.  For
                more detailed information, please refer to the API documentation
                linked above.  Further, any keyword arguments passed that are
                not explicitly documented will be automatically appended to the
                settings document.  There is no need to pass settings directly.

        Returns:
            :obj:`dict`:
                The scan resource record of the newly created scan.

        Examples:
            Create an un-credentialed basic scan:

            >>> scan = tio.scans.create(
            ...     name='Example Scan',
            ...     targets=['127.0.0.1'])

            Creating a scan with a set of managed credentials:

            >>> scan = tio.scans.create(
            ...     name='Example Managed Cred Scan',
            ...     targets=['127.0.0.1'],
            ...     credentials={'Host': {'SSH': [{'id': 'CREDENTIAL-UUID'}]}}

            Creating a scan with a set of embedded credentials:

            >>> scan = tio.scans.create(
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
            ...     enabled=True, frequency='daily', interval=2, starttime=datetime.utcnow())
            >>> scan = tio.scans.create(
            ...     name='Example Scan',
            ...     targets=['127.0.0.1']
            ...     schedule_scan=schedule)

            For further information on credentials, what settings to use, etc,
            refer to
            `this doc <https://developer.tenable.com/docs/determine-settings-for-credential-type>`_
            on the developer portal.
        '''
        if 'template' not in kw:
            kw['template'] = 'basic'
        scan = self._create_scan_document(kw)

        # Run the API call and return the result to the caller.
        return self._post(json=scan).scan

    def delete(self, scan_id: Union[int, UUID]):
        '''
        Remove a scan.

        :devportal:`scans: delete <scans-delete>`

        Args:
            scan_id (int or uuid): The unique identifier for the scan.

        Returns:
            :obj:`None`:
                The scan was successfully deleted.

        Examples:
            >>> tio.scans.delete(1)
        '''
        self._delete(f'{scan_id}')

    def history(self,
                scan_id: Union[int, UUID],
                limit: int = 50,
                offset: int = 0,
                pages: Optional[int] = None,
                sort: Tuple[str, str] = None
                ) -> ScanHistoryIterator:
        '''
        Get the scan history of a given scan from Tenable Vulnerability Management.

        :devportal:`scans: history <scans-history>`

        Args:
            scan_id (int or uuid):
                The unique identifier for the scan.
            limit (int, optional):
                The number of records to retrieve.  Default is 50
            offset (int, optional):
                The starting record to retrieve.  Default is 0.
            sort (tuple, optional):
                A tuple of tuples identifying the the field and sort order of
                the field.

        Returns:
            :obj:`ScanHistoryIterator`:
                An iterator that handles the page management of the requested
                records.

        Examples:
            >>> for history in tio.scans.history(1):
            ...     pprint(history)
        '''
        query = {}
        if sort:
            query['sort'] = ','.join([f'{i[0]}:{i[1]}' for i in sort])

        return ScanHistoryIterator(self._api,
                                   _limit=limit if limit else 50,
                                   _offset=offset if offset else 0,
                                   _pages_total=pages,
                                   _query=query,
                                   _path=f'scans/{scan_id}/history',
                                   _resource='history'
                                   )

    def delete_history(self,
                       scan_id: Union[int, UUID],
                       history_id: Union[int, UUID]
                       ):
        '''
        Remove an instance of a scan from a scan history.

        :devportal:`scans: delete-history <scans-delete-history>`

        Args:
            scan_id (int or uuid):
                The unique identifier for the scan.
            history_id (int or uuid):
                The unique identifier for the instance of the scan.

        Returns:
            :obj:`None`:
                Scan history successfully deleted.

        Examples:
            >>> tio.scans.delete_history(1, 1)
        '''
        self._delete(f'{scan_id}/history/{history_id}')

    def details(self, scan_id: Union[int, UUID]) -> Dict:
        '''
        Calls the editor API and parses the scan config details to return a
        document that closely matches what the API expects to be POSTed or PUTed
        via the create and configure methods.  The compliance audits and
        credentials are populated into the 'current' sub-document for the
        relevant resources.

        .. important::
            Please note that the details method is reverse-engineered from the
            responses from the editor API, and while we are reasonably sure that
            the response should align almost exactly to what the API expects to
            be pushed to it, this method by very nature of what it's doing isn't
            guaranteed to always work.

        .. note::
            If you're looking for the results of the most recent scan, and what
            matches to the ``GET /scans/{id}`` call, then take a look at the
            results method.

        Args:
            scan_id (int or uuid): The unique identifier for the scan.

        Returns:
            :obj:`dict`:
                The scan configuration resource.

        Examples:
            >>> scan = tio.scans.details(1)
            >>> pprint(scan)
        '''
        return self._api.editor.details('scan', scan_id)

    def results(self,
                scan_id: Union[int, UUID],
                history_id: Optional[Union[int, UUID]] = None,
                history_uuid: Optional[UUID] = None
                ):
        '''
        Return the scan results from either the latest scan or a specific scan
        instance in the history.

        :devportal:`scans: details <scans-details>`

        Args:
            scan_id (int or uuid): The unique identifier for the scan.
            history_id (int, optional):
                The unique identifier for the instance of the scan.
            history_uuid (uuid, optional)
                The UUID for the instance of the scan.

        Returns:
            :obj:`dict`:
                The scan result dictionary.

        Examples:
            Retrieve the latest results:

            >>> results = tio.scans.results(419)

            Retrieve a specific instance of the result set using history_id:

            >>> results = tio.scans.results(419, history_id=15184619)

            Retrieve a specific instance of the result set using history_uuid:

            >>> results = tio.scans.results(419, history_uuid="123e4567-e89b-12d3-a456-426614174000")

        '''
        params = dict()

        if history_id:
            params['history_id'] = history_id
        if history_uuid:
            warnings.warn('The history_uuid parameter is deprecated, '
                          'use history_id instead', DeprecationWarning)
            params['history_id'] = history_uuid

        return self._api.get('scans/{}'.format(
            scan_id), params=params).json()

    def export(self,
               scan_id: Union[int, UUID],
               *filters: Tuple[str, str, str],
               stream_hook: Optional[Callable] = None,
               **kw
               ):
        '''
        Export the scan report.

        :devportal:`scans: export <scans-export-request>`

        Args:
            scan_id (int or uuid): The unique identifier of the scan.
            *filters (tuple, optional):
                A list of tuples detailing the filters that wish to be applied
                the response data.  Each tuple is constructed as
                ('filter', 'operator', 'value') and would look like the
                following example: `('plugin.id', 'eq', '19506')`.  For a
                complete list of the available filters and options, please
                refer to the API documentation linked above.
            stream_hook (callable, optional):
                If set, send the streaming response to this callable. The callable is
                responsible for iterating over the stream but does *not* need to close
                the file object. The signature for the callable is:

                .. code-block:: python

                    def f(response: requests.Response,
                          fobj: BytesIO,
                          chunk_size: int) -> BytesIO:

            history_id (int, optional):
                The unique identifier for the instance of the scan.
            history_uuid (uuid, optional):
                The UUID for the instance of the scan.
            format (str, optional):
                What format would you like the resulting data to be in.  The
                default would be nessus output.  Available options are `nessus`,
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
                The file-like object to be returned with the exported data.  If
                no object is specified, a BytesIO object is returned with the
                data.  While this is an optional parameter, it is highly
                recommended to use this parameter as exported files can be quite
                large, and BytesIO objects are stored in memory, not on disk.

        Returns:
            :obj:`FileObject`:
                The file-like object of the requested export.

        Examples:
            Export the full report of the latest instance of the scan:

            >>> with open('example.nessus', 'wb') as reportobj:
            ...     tio.scans.export(1, fobj=reportobj)

            Export a specific instance of the scan:

            >>> with open('example.nessus', 'wb') as reportobj:
            ...     tio.scans.export(1, history_id=1, fobj=reportobj)
        '''

        # initiate the payload and parameters dictionaries.  We are also
        # checking to see if the filters were passed as a keyword argument
        # instead of as an argument list.  As this seems to be a common
        # issue, we should be supporting this methodology.
        filters = self._check('filters',
                              kw.get('filters', filters), (list, tuple))
        payload = self._parse_filters(filters,
                                      self._api.filters.scan_filters(), rtype='sjson')
        params = dict()
        dl_params = dict()

        if 'history_id' in kw:
            params['history_id'] = self._check(
                'history_id', kw['history_id'], int)

        if kw.get('history_uuid'):
            params['history_uuid'] = self._check(
                'history_uuid', kw['history_uuid'], 'scanner-uuid')

        # Enable exporting of Web Application scans.
        if 'scan_type' in kw:
            dl_params['type'] = params['type'] = self._check(
                'type', kw['scan_type'], str, choices=['web-app'])

        if 'password' in kw:
            payload['password'] = self._check('password', kw['password'], str)

        payload['format'] = self._check('format',
                                        kw['format'] if 'format' in kw else None,
                                        str, choices=['nessus', 'html', 'pdf', 'csv', 'db'],
                                        default='nessus')

        # The chapters are sent to us in a list, and we need to collapse that
        # down to a comma-delimited string.
        payload['chapters'] = ';'.join(
            self._check('chapters',
                        kw['chapters'] if 'chapters' in kw else None,
                        list,
                        choices=['vuln_hosts_summary', 'vuln_by_host', 'vuln_by_plugin',
                                 'compliance_exec', 'compliance', 'remediations'],
                        default=['vuln_by_host']))

        if 'filter_type' in kw:
            payload['filter.search_type'] = self._check(
                'filter_type', kw['filter_type'], str, choices=['and', 'or'])

        # Now we need to set the FileObject.  If one was passed to us, then lets
        # just use that, otherwise we will need to instantiate a BytesIO object
        # to push the data into.
        if 'fobj' in kw:
            fobj = kw['fobj']
        else:
            fobj = BytesIO()

        # The first thing that we need to do is make the request and get the
        # File id for the job.
        fid = self._api.post('scans/{}/export'.format(scan_id),
                             params=params, json=payload).json()['file']
        self._api._log.debug('Initiated scan export {}'.format(fid))

        # Next we will wait for the status of the export request to become
        # ready.
        _ = self._wait_for_download(
            'scans/{}/export/{}/status'.format(scan_id, fid),
            'scans', scan_id, fid, params=dl_params)

        # Now that the status has reported back as "ready", we can actually
        # download the file.
        resp = self._api.get('scans/{}/export/{}/download'.format(
            scan_id, fid), params=dl_params, stream=True)

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
                     scan_id: Union[int, UUID],
                     host_id: int,
                     history_id: Optional[int] = None,
                     history_uuid: Optional[UUID] = None
                     ) -> Dict:
        '''
        Retrieve the host details from a specific scan.

        :devportal:`scans: host-details <scans-host-details>`

        Args:
            scan_id (int): The unique identifier for the scan.
            host_id (int): The unique identifier for the host within the scan.
            history_id (int, optional):
                The unique identifier for the instance of the scan.
            history_uuid (str, optional):
                The unique identifier for the scan instance.

        Returns:
            :obj:`dict`:
                The information related to the host requested.

        Examples:
            >>> host = tio.scans.host_details(1, 1)
        '''
        params = dict()
        if history_id:
            params['history_id'] = self._check('history_id', history_id, int)

        if history_uuid:
            params['history_uuid'] = self._check(
                'history_uuid', history_uuid, 'scanner-uuid')

        return self._api.get('scans/{}/hosts/{}'.format(
            scan_id,
            self._check('host_id', host_id, int)),
            params=params).json()

    def import_scan(self,
                    fobj: BytesIO,
                    folder_id: Optional[int] = None,
                    password: Optional[str] = None,
                    aggregate: bool = True):
        '''
        Import a scan report into Tenable Vulnerability Management.

        :devportal:`scans: import <scans-import>`

        Args:
            fobj (FileObject): The File-like object of the scan to import.
            folder_id (int, optional):
                The unique identifier for the folder to place the scan into.
            password (str, optional):
                The password needed to decrypt the file.  This is only necessary
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
            ...     tio.scans.import(reportobj)

            Import a NessusDB report.

            >>> with open('example.db', 'rb') as reportobj:
            ...     tio.scans.import(reportobj, password='sekret')
        '''
        # First lets verify that the folder_id and password are typed correctly
        # before initiating any uploads.
        payload = {}
        if folder_id:
            payload['folder_id'] = self._check('folder_id', folder_id, int)
        if password:
            payload['password'] = self._check('password', password, str)

        # Upload the file to the Tenable Vulnerability Management and store
        # the resulting filename in the payload.
        payload['file'] = self._api.files.upload(fobj,
                                                 encrypted=bool(password))

        # make the call to Tenable Vulnerability Management to import and
        # then return the result to the caller.
        return self._post('import',
                          json=payload,
                          params={'include_aggregate': int(aggregate)}
                          )

    def launch(self,
               scan_id: Union[int, UUID],
               targets: Optional[List[str]] = None
               ):
        '''
        Launches a scan.

        :devportal:`scans: launch <scans-launch>`

        Args:
            scan_id (int or uuid): The unique identifier for the scan.
            targets (list, optional):
                A list of targets to be scanned instead of the default targets
                in the scan.

        Response:
            :obj:`str`:
                The uuid of the scan instance (history).

        Examples:
            Launch the scan with the configured targets:

            >>> tio.scans.launch(1)

            Launch the scan with some custom targets:

            >>> tio.scans.launch(1, targets=['127.0.0.1'])
        '''
        payload = {}
        if targets:
            payload['alt_targets'] = targets

        return self._post(f'{scan_id}/launch', json=payload).scan_uuid

    def list(self,
             folder_id: Optional[int] = None,
             last_modified: Optional[datetime] = None
             ) -> List[Dict]:
        '''
        Retrieve the list of configured scans.

        :devportal:`scans: list <scans-list>`

        Args:
            folder_id (int, optional): Only return scans within this folder.
            last_modified (datetime, optional):
                Only return scans that have been modified since the time
                specified.

        Returns:
            :obj:`list`:
                A list containing the list of scan resource records.

        Examples:
            >>> for scan in tio.scans.list():
            ...     pprint(scan)
        '''
        params = {}
        if folder_id:
            params['folder_id'] = folder_id
        if last_modified and isinstance(last_modified, datetime):
            # for the last_modified datetime attribute, we will want to convert
            # that into a timestamp integer before passing it to the API.
            lm = int(time.mktime(last_modified.timetuple()))
            params['last_modification_date'] = lm
        if last_modified and isinstance(last_modified, int):
            params['last_modification_date'] = last_modified

        return self._get(params=params).scans

    def pause(self, scan_id: Union[int, UUID], block: bool = False):
        '''
        Pauses a running scan.

        :devportal:`scans: pause <scans-pause>`

        Args:
            scan_id (int or uuid): The unique identifier of the scan to pause.
            block (bool, optional):
                Block until the scan is actually paused.  Default is False.

        Returns:
            :obj:`None`:
                The scan was successfully requested to be paused.

        Examples:
            >>> tio.scans.pause(1)
        '''
        self._post(f'{scan_id}/pause', json={})
        if block:
            self._block_while_running(scan_id)

    def plugin_output(self,
                      scan_id: Union[int, UUID],
                      host_id: int,
                      plugin_id: int,
                      history_id: Optional[int] = None,
                      history_uuid: Optional[UUID] = None
                      ) -> Dict:
        '''
        Retrieve the plugin output for a specific instance of a vulnerability
        on a host.

        :devportal:`scans: plugin-output <scans-plugin-output>`

        Args:
            scan_id (int or uuid): The unique identifier of the scan.
            host_id (int): The unique identifier of the scanned host.
            plugin_id (int): The plugin id.
            history_id (int, optional):
                The unique identifier of the scan instance.

        Returns:
            :obj:`dict`:
                The plugin resource record for that plugin on that host.

        Examples:
            >>> output = tio.scans.plugin_output(1, 1, 1)
            >>> pprint(output)
        '''
        params = {}
        if history_id:
            params['history_id'] = history_id
        if history_uuid:
            params['history_uuid'] = history_uuid

        return self._get(f'{scan_id}/hosts/{host_id}/plugins/{plugin_id}',
                         params=params
                         )

    def set_read_status(self, scan_id: Union[str, UUID], read_status: bool):
        '''
        Sets the read status of the scan.  This is generally used to toggle the
        unread status of the scan within the UI.

        :devportal:`scans: read-status <scans-read-status>`

        Args:
            scan_id (int or uuid): The unique identifier for the scan.
            read_status (bool):
                Is the scan in a read or unread state?  True would denote read,
                whereas False is unread.

        Returns:
            :obj:`None`:
                The status of the scan was updated.

        Examples:
            Set a scan to unread:

            >>> tio.scans.set_read_status(1, False)
        '''
        self._put(f'{scan_id}/status', json={'read': read_status})

    def resume(self, scan_id: Union[str, UUID]):
        '''
        Resume a paused scan.

        :devportal:`scans: resume <scans-resume>`

        Args:
            scan_id (int or uuid): The unique identifier for the scan.

        Returns:
            :obj:`None`:
                The scan was successfully requested to resume.

        Examples:
            >>> tio.scans.resume(1)
        '''
        self._post(f'{scan_id}/resume')

    def schedule(self, scan_id: Union[str, UUID], enabled: bool) -> dict:
        '''
        Enables or disables the scan schedule.

        :devportal:`scans: schedule <scans-schedule>`

        Args:
            scan_id (int): The unique identifier for the scan.
            enabled (bool): Enables or Disables the scan scheduling.

        Returns:
            :obj:`dict`:
                The schedule resource record for the scan.

        Examples:
            Enable a scan schedule:

            >>> tio.scans.schedule(1, True)
        '''
        return self._put(f'{scan_id}/schedule', json={'enabled': enabled})

    def stop(self, scan_id: Union[str, UUID], block: bool = False):
        '''
        Stop a running scan.

        :devportal:`scans: stop <scans-stop>`

        Args:
            scan_id (int): The unique identifier for the scan.
            block (bool, optional):
                Block until the scan is actually stopped.  Default is False.

        Returns:
            :obj:`None`:
                The scan was successfully requested to stop.

        Examples:
            Stop the scan asynchronously:

            >>> tio.scans.stop(1)

            Stop the scan and wait for the scan to stop:

            >>> tio.scans.stop(1, True)
        '''
        self._post(f'{scan_id}/stop')
        if block:
            self._block_while_running(scan_id)

    def status(self, scan_id: Union[str, UUID]) -> str:
        '''
        Get the status of the latest instance of the scan.

        :devportal:`scans: get-latest-status <scans-get-latest-status>`

        Args:
            scan_id (int or uuid): The unique identifier for the scan.

        Returns:
            :obj:`str`:
                The current status of the last instance.

        Examples:
            >>> tio.scans.status(1)
            u'completed'
        '''
        return self._get(f'{scan_id}/latest-status').status

    def progress(self,
                 scan_id: Union[int, UUID],
                 history_id: Optional[int] = None,
                 history_uuid: Optional[UUID] = None,
                 ) -> int:
        """
        Get the progress of the specified scan.

        :devportal:`scans: get-scan-progress <io-vm-scans-progress-get>`

        Args:
            scan_id (int | UUID): The
        """
        params = {}
        if history_id:
            params['history_id'] = history_id
        if history_uuid:
            params['history_uuid'] = history_uuid
        return self._get(f'{scan_id}/progress').progress


    def timezones(self) -> List[str]:
        '''
        Retrieves the list of timezones.

        :devportal:`scans: timezones <scans-timezones>`

        Returns:
            :obj:`list`:
                List of allowed timezone strings accepted by Tenable.IO

        Examples:
            >>> for item in tio.scans.timezones():
            ...     pprint(item)
        '''
        resp = self._get('timezones').timezones
        return [i.value for i in resp]

    def info(self, scan_id: Union[int, UUID], history_uuid: UUID) -> Dict:
        '''
        Retrieves information about the status of the specified instance
        of the scan.

        :devportal:`scan: get-scan-history <scans-history-by-scan-id>`

        Args:
            scan_id (int or uuid): The unique identifier for the scan.
            history_uuid (str): The unique identifier for the scan instance.

        Returns:
            :obj:`dict`:
                The metadata about the scan instance specified.

        Examples:
            >>> info = tio.scans.info(1, 'BA0ED610-C27B-4096-A8F4-3189279AFFE7')
        '''
        return self._api.get('scans/{}/history/{}'.format(
            scan_id,
            self._check('history_uuid', history_uuid, 'scanner-uuid'))).json()

    def check_auto_targets(
        self,
        limit: int,
        matched_resource_limit: int,
        network_uuid: Optional[UUID] = '00000000-0000-0000-0000-000000000000',
        tags: Optional[List[UUID]] = None,
        targets: Optional[List[str]] = None
    ) -> Dict:
        '''
        Evaluates a list of targets and/or tags against
        the scan route configuration of scanner groups.

        :devportal:`scan: check-auto-targets <scans-check-auto-targets>`

        Args:
            limit (int):
                Limit the number of missed targets returned in the response.
            matched_resource_limit (int):
                Limit the number of matched resource UUIDs returned
                in the response.
            network_uuid (uuid, optional):
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
            >>> scan_routes_info = tio.scans.check_auto_targets(10, 5, targets=['127.0.0.1'])
        '''
        payload = {}
        query = {
            "limit": limit,
            "matched_resource_limit": matched_resource_limit
        }
        if tags:
            payload['tags'] = [str(t) for t in tags]
        if targets:
            payload['target_list'] = ','.join([str(t) for t in targets])
        return self._post('check-auto-targets', params=query, json=payload)
