'''
scans
=====

The following methods allow for interaction into the Tenable.io 
`scans <https://cloud.tenable.com/api#/resources/scans>`_ API endpoints.

Methods available on ``tio.scans``:

.. rst-class:: hide-signature
.. autoclass:: ScansAPI

    .. automethod:: attachment
    .. automethod:: configure
    .. automethod:: copy
    .. automethod:: create
    .. automethod:: delete
    .. automethod:: delete_history
    .. automethod:: details
    .. automethod:: results
    .. automethod:: export
    .. automethod:: host_details
    .. automethod:: import_scan
    .. automethod:: launch
    .. automethod:: list
    .. automethod:: pause
    .. automethod:: plugin_output
    .. automethod:: set_read_status
    .. automethod:: resume
    .. automethod:: schedule
    .. automethod:: status
    .. automethod:: stop
    .. automethod:: timezones
'''
from .base import TIOEndpoint
from tenable.utils import dict_merge
from tenable.errors import UnexpectedValueError
from datetime import datetime, timedelta
from io import BytesIO
import time

class ScansAPI(TIOEndpoint):
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

    def _create_scan_document(self, kw):
        '''
        Takes the key-worded arguments and will provide a scan settings document
        based on the values inputted.

        Args:
            kw (dict): The keyword dict passed from the user

        Returns:
            scan (dict): The resulting scan document based on the kw provided.
        '''
        scan = {
            'settings': dict(),
        }

        # If a template is specified, then we will pull the listing of available
        # templates and set the policy UUID to match the template name given.
        if 'template' in kw:
            templates = self._api.policies.templates()
            scan['uuid'] = templates[self._check(
                'template', kw['template'], str, 
                default='basic',
                choices=list(templates.keys())
            )]
            del(kw['template'])

        # If a policy UUID is sent, then we will set the scan template UUID to
        # be the UUID that was specified.
        if 'policy' in kw:
            try:
                # at first we are going to assume that the information that was
                # relayed to use for the scan policy was the policy ID.  As
                # this is the least expensive thing to check for, it's a logical
                # starting point.
                scan['settings']['policy_id'] = self._check(
                    'policy', kw['policy'], int)

            except (UnexpectedValueError, TypeError):
                # Now we are going to attempt to find the scan policy based on
                # the title of the policy before giving up and throwing. an
                # UnexpectedValueError
                policies = self._api.policies.list()
                match = False
                for item in policies:
                    if kw['policy'] == item['name']:
                        scan['uuid'] = item['template_uuid']
                        scan['settings']['policy_id'] = item['id']
                        match = True
                if not match:
                    raise UnexpectedValueError('policy setting is invalid.')
            del(kw['policy'])

        # if the scanner attribute was set, then we will attempt to figure out
        # what scanner to use.
        if 'scanner' in kw:
            scanners = self._api.scanners.allowed_scanners()
            try:
                # we will always want to attempt to use the UUID first as it's
                # the cheapest check that we can run.
                scan['settings']['scanner_id'] = self._check(
                    'scanner', kw['scanner'], 'scanner-uuid', 
                    choices=[s['id'] for s in scanners])

            except (UnexpectedValueError, TypeError):
                # as an UnexpectedValueError was raised, the data may just be
                # the name of a scanner.  If this is the case, then we will want
                # to attempt to enumerate the scanner list and if we see a match,
                # use that scanner's UUID instead.
                for item in scanners:
                    if item['name'] == kw['scanner']:
                        scan['settings']['scanner_id'] = item['id']

                if 'scanner_id' not in scan['settings']:
                    raise UnexpectedValueError('scanner setting is invalid.')
            del(kw['scanner'])

        # If the targets parameter is specified, then we will need to convert
        # the list of targets to a comma-delimited string and then set the
        # text_targets parameter with the result.
        if 'targets' in kw:
            scan['settings']['text_targets'] = ','.join(self._check(
                'targets', kw['targets'], list))
            del(kw['targets'])

        # For credentials, we will simply push the dictionary as-is into the
        # the credentials.add sub-document.
        if 'credentials' in kw:
            scan['credentials'] = {'add': dict()}
            scan['credentials']['add'] = self._check(
                'credentials', kw['credentials'], dict)
            del(kw['credentials'])

        # Just like with credentials, we will push the dictionary as-is into the
        # correct sub-document of the scan definition.
        if 'compliance' in kw:
            scan['audits'] = self._check('compliance', kw['compliance'], dict)
            del(kw['compliance'])

        if 'plugins' in kw:
            scan['plugins'] = self._check('plugins', kw['plugins'], dict)
            del(kw['plugins'])

        # any other remaining keyword arguments will be passed into the settings
        # sub-document.  The bulk of the data should go here...
        scan['settings'] = dict_merge(scan['settings'], kw)
        return scan

    def attachment(self, scan_id, attachment_id, key, fobj=None):
        '''
        Retrieve an attachment  associated to a scan.

        `scans: attachments <https://cloud.tenable.com/api#/resources/scans/attachments>`_

        Args:
            scan_id (int): The unique identifier for the scan.
            attachment_id (int): The unique identifier for the attachement
            key (str): The attachement access token.
            fobj (FileObject, optional): a file-like object you wish for the
                attachement to be written to.  If none is specified, a BytesIO
                object will be returned with the contents of the attachment.

        Returns:
            FileObject: A file-like object with the attachement written into it.

        Examples:
            >>> with open('example.file', 'wb') as fobj:
            ...     tio.scans.attachement(1, 1, 'abc', fobj)
        '''
        if not fobj:
            # if no file-like object is specified, then assign a BytesIO object
            # to the variable.
            fobj = BytesIO()

        # Make the HTTP call and stream the data into the file object.
        resp = self._api.get('scans/{}/attachments/{}'.format(
            self._check('scan_id', scan_id, int),
            self._check('attachment_id', attachment_id, int)
            ), params={'key': self._check('key', key, str)}, stream=True)
        for chunk in resp.iter_content(chunk_size=1024):
            if chunk:
                fobj.write(chunk)
        fobj.seek(0)

        # Return the file object to the caller.
        return fobj

    def configure(self, id, **kw):
        '''
        Overwrite the parameters specified on top of the existing scan record.

        `scans: configure <https://cloud.tenable.com/api#/resources/scans/configure>`_

        Args:
            id (int): The unique identifier for the scan.
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
            **kw (dict, optional):
                The various parameters that can be passed to the scan creation
                API.  Examples would be `name`, `email`, `scanner_id`, etc.  For
                more detailed information, please refer to the API documentation
                linked above.            

        Returns:
            dict: The scan resource record.

        Examples:
            >>> tio.scans.configure(1, name='New Scan Name')
        '''

        # We will get the current scan record, generate the new parameters in
        # the correct format, and then merge them together to create the new
        # :func:`~.tenable.tenable_io.ScansAPI.details` method, however is not 
        # scan record that we will be pushing to the API.
        current = self.details(id)
        updated = self._create_scan_document(kw)
        scan = dict_merge(current, updated)

        # Performing the actual call to the API with the updated scan record.
        return self._api.put('scans/{}'.format(self._check('id', id, int)),
                    json=scan).json()

    def copy(self, scan_id, folder_id=None, name=None):
        '''
        Duplicates a scan and returns the details of the copy.

        `scans: copy <https://cloud.tenable.com/api#/resources/scans/copy>`_

        Args:
            scan_id (int): The unique identifier for the scan.
            folder_id (int, optional): The unique identifier for the folder.
            name (str, optional): The name for the copied scan.

        Returns:
            dict: The scan resource record for the copied scan.

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
        return self._api.post('scans/{}/copy'.format(self._check('scan_id', scan_id, int)),
            json=payload).json()

    def create(self, **kw):
        '''
        Create a new scan.

        `scans: create <https://cloud.tenable.com/api#/resources/scans/create>`_

        Args:
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
            **kw (dict, optional):
                The various parameters that can be passed to the scan creation
                API.  Examples would be `name`, `email`, `scanner_id`, etc.  For
                more detailed information, please refer to the API documentation
                linked above.

        Returns:
            dict: The scan resource record of the newly created scan.

        Examples:
            Create an un-credentialed basic scan:

            >>> scan = tio.scans.create(targets=['127.0.0.1'])
        '''
        if 'template' not in kw:
            kw['template'] = 'basic'
        scan = self._create_scan_document(kw)

        # Run the API call and return the result to the caller.
        return self._api.post('scans', json=scan).json()['scan']

    def delete(self, scan_id):
        '''
        Remove a scan.

        `scans: delete <https://cloud.tenable.com/api#/resources/scans/delete>`_

        Args:
            scan_id (int): The unique identifier for the scan.

        Returns:
            None: scan successfully deleted.

        Examples:
            >>> tio.scans.delete(1)
        '''
        self._api.delete('scans/{}'.format(self._check('scan_id', scan_id, int)))

    def delete_history(self, scan_id, history_id):
        '''
        Remove an instance of a scan from a scan history.

        `scans: delete-history <https://cloud.tenable.com/api#/resources/scans/delete-history>`_

        Args:
            scan_id (int): The unique identifier for the scan.
            history_id (int): The unique identifier for the instance of the scan.

        Returns:
            None: Scan history successfully deleted.

        Examples:
            >>> tio.scans.delete_history(1, 1)
        '''
        self._api.delete('scans/{}/hostory/{}'.format(
            self._check('scan_id', scan_id, int),
            self._check('history_id', history_id, int)))

    def details(self, scan_id):
        '''
        Calls the editor API and parses the scan config details to return a
        document that closely matches what the API expects to be POSTed or PUTed
        via the create and configure methods.  The compliance audits and
        credentials are populated into the 'current' sub-document for the
        relevant resources.

        Args:
            scan_id (int): The unique identifier for the scan.

        Returns:
            dict: The scan configuration resource.

        Examples:
            >>> scan = tio.scans.details(1)
            >>> pprint(scan)

        Please note that flatten_scan is reverse-engineered from the responses
        from the editor API and isn't guaranteed to work. 
        '''

        # Get the editor object
        editor = self._api.get('editor/scan/{}'.format(
            self._check('scan_id', scan_id, int))).json()

        # define the initial skeleton of the scan object
        scan = {
            'settings': self._api.editor.parse_vals(editor['settings']),
            'uuid': editor['uuid']
        }

        # graft on the basic settings that aren't stored in any input sections.
        for item in editor['settings']['basic']['groups']:
            for setting in item.keys():
                if setting not in ['name', 'title', 'inputs']:
                    scan['settings'][setting] = item[setting]

        if 'credentials' in editor:
            # if the credentials sub-document exists, then lets walk down the
            # credentials dataset
            scan['credentials'] = {
                'current': self._api.editor.parse_creds(
                    editor['credentials']['data'])
            }

            # We also need to gather the settings from the various credential
            # settings that are unique to the scan.
            for ctype in editor['credentials']['data']:
                for citem in ctype['types']:
                    if 'settings' in citem and citem['settings']:
                        scan['settings'] = dict_merge(
                            scan['settings'], self._api.editor.parse_vals(
                                citem['settings']))

        if 'compliance' in editor:
            # if the audits sub-document exists, then lets walk down the
            # audits dataset.
            scan['compliance'] = {
                'current': self._api.editor.parse_audits(
                    editor['compliance']['data'])
            }

            # We also need to add in the "compliance" settings into the scan
            # settings.
            for item in editor['compliance']['data']:
                if 'settings' in item:
                    scan['settings'] = dict_merge(
                        scan['settings'], self._api.editor.parse_vals(
                            item['settings']))

        if 'plugins' in editor:
            # if the plugins sub-document exists, then lets walk down the
            # plugins dataset.
            scan['plugins'] = self._api.editor.parse_plugins(
                editor['plugins']['families'], scan_id)

        # We next need to do a little post-parsing of the ACLs to find the
        # owner and put ownder_id attribute into the appropriate location.
        for acl in scan['settings']['acls']:
            if acl['owner'] == 1:
                scan['settings']['owner_id'] = acl['id']

        # return the scan document to the caller.
        return scan

    def results(self, scan_id, history_id=None):
        '''
        Return the scan results from either the latest scan or a specific scan
        instance in the history.

        `scans: details <https://cloud.tenable.com/api#/resources/scans/details>`_

        Args:
            scan_id (int): The unique identifier for the scan.
            history_id (int, optional): 
                The unique identifier for the instance of the scan.

        Returns:
            dict: The scan result dictionary.

        Examples:
            Retrieve the latest results:

            >>> results = tio.scans.results(1)

            Retrieve a specific instance of the result set:

            >>> results = tio.scans.results(1, 1)
        '''
        params = dict()
        if history_id:
            params['history_id'] = self._check('history_id', history_id, int)

        return self._api.get('scans/{}'.format(
            self._check('scan_id', scan_id, int)), params=params).json()


    def export(self, scan_id, *filters, **kw):
        '''
        Export the scan report.

        `scans: export <https://cloud.tenable.com/api#/resources/scans/export-request>`_

        Args:
            scan_id (int): The unique identifier of the scan.
            *filters (tuple, optional):
                A list of tuples detailing the filters that wish to be applied
                the response data.  Each tuple is constructed as 
                ('filter', 'operator', 'value') and would look like the 
                following example: `('plugin.id', 'eq', '19506')`.  For a
                complete list of the available filters and options, please
                refer to the API documentation linked above.
            history_id (int, optional): 
                The unique identifier for the instance of the scan.
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
            fobj (FileObject, optional):
                The file-like object to be returned with the exported data.  If
                no object is specified, a BytesIO object is returned with the
                data.  While this is an optional parameter, it is highly
                recommended to use this parameter as exported files can be quite
                large, and BytesIO objects are stored in memory, not on disk.

        Returns:
            FileObject: The file-like object of the requested export.

        Examples:
            Export the full report of the latest instance of the scan:

            >>> with open('example.nessus', 'wb') as reportobj:
            ...     tio.scans.export(1, fobj=reportobj)

            Export a specific instance of the scan:

            >>> with open('example.nessus', 'wb') as reportobj:
            ...     tio.scans.export(1, history_id=1, fobj=reportobj)
        '''

        # initiate the payload and parameters dictionaries.
        payload = self._parse_filters(filters,
            self._api.filters.scan_filters(), rtype='sjson')
        params = dict()

        if 'history_id' in kw:
            params['history_id'] = self._check(
                'history_id', kw['history_id'], int)

        if 'password' in kw:
            payload['password'] = self._check('password', kw['password'], str)

        payload['format'] = self._check('format', 
            kw['format'] if 'format' in kw else None,
            str, choices=['nessus', 'html', 'pdf', 'csv', 'db'],
            default='nessus')

        # The chapters are sent to us in a list, and we need to collapse that
        # down to a comma-delimited string.
        payload['chapters'] = ','.join(
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
        fid = self._api.post('scans/{}/export'.format(
            self._check('scan_id', scan_id, int)), 
            params=params, json=payload).json()['file']
        self._api._log.debug('Initiated scan export {}'.format(fid))

        # Next we will wait for the status of the export request to become
        # ready.  We will query the API every half a second until we get the
        # response we're looking for.
        while 'ready' != self._api.get('scans/{}/export/{}/status'.format(
                                        scan_id, fid)).json()['status']:
            time.sleep(0.5)

        # Now that the status has reported back as "ready", we can actually
        # download the file.
        resp = self._api.get('scans/{}/export/{}/download'.format(
            scan_id, fid), stream=True)

        # Lets stream the file into the file-like object...
        for chunk in resp.iter_content(chunk_size=1024):
            if chunk:
                fobj.write(chunk)
        fobj.seek(0)

        # Lastly lets return the FileObject to the caller.
        return fobj

    def host_details(self, scan_id, host_id, history_id=None):
        '''
        Retrieve the host details from a specific scan.

        `scans: host-details <https://cloud.tenable.com/api#/resources/scans/host-details>`_

        Args:
            scan_id (int): The unique identifier for the scan.
            host_id (int): The unique identifier for the host within the scan.
            histort_id (int, optional):
                The unique identifier for the instance of the scan.

        Returns:
            dict: The information related to the host requested.

        Examples:
            >>> host = tio.scans.host_details(1, 1)
        '''
        params = dict()
        if history_id:
            params['history_id'] = self._check('history_id', history_id, int)

        return self._api.get('scans/{}/hosts/{}'.format(
                self._check('scan_id', scan_id, int),
                self._check('host_id', host_id, int)),
            params=params).json()


    def import_scan(self, fobj, folder_id=None, password=None):
        '''
        Import a scan report into Tenable.io.

        `scans: import <https://cloud.tenable.com/api#/resources/scans/import>`_

        Args:
            fobj (FileObject): The File-like object of the scan to import.
            folder_id (int, optional): 
                The unique identifier for the folder to place the scan into.
            password (str, optional):
                The password needed to decrypt the file.  This is only necessary
                for NessusDB files uploaded.

        Returns:
            dict: The scan resource record for the imported scan.

        Examples:
            Import a .nessusv2 report:

            >>> with open('example.nessus') as reportobj:
            ...     tio.scans.import(reportobj)

            Import a NessusDB report.

            >>> with open('example.db') as reportobj:
            ...     tio.scans.import(reportobj, password='sekret')
        '''
        # First lets verify that the folder_id and password are typed correctly
        # before initiating any uploads.
        payload = dict()
        if folder_id:
            payload['folder_id'] = self._check('folder_id', folder_id, int)
        if password:
            payload['password'] = self._check('password', password, str)

        # Upload the file to the Tenable.io and store the resulting filename in
        # the payload.
        payload['file'] = self._api.files.upload(fobj)

        # make the call to Tenable.io to import and then return the result to
        # the caller.
        return self._api.post('scans/import', json=payload).json()

    def launch(self, scan_id, targets=None):
        '''
        Launches a scan.

        `scans: launch <https://cloud.tenable.com/api#/resources/scans/launch>`_

        Args:
            scan_id (int): The unique identifier for the scan.
            targets (list, optional): 
                A list of targets to be scanned instead of the default targets
                in the scan.

        Response:
            str: The uuid of the scan instance (history).

        Examples:
            Launch the scan with the configured targets:

            >>> tio.scans.launch(1)

            Launch the scan with some custom targets:

            >>> tio.scans.launch(1, targets=['127.0.0.1'])
        '''
        payload = dict()
        if targets:
            payload['alt_targets'] = self._check('targets', targets, list)

        return self._api.post('scans/{}/launch'.format(
                self._check('scan_id', scan_id, int)), 
            json=payload).json()['scan_uuid']

    def list(self, folder_id=None, last_modified=None):
        '''
        Retrieve the list of configured scans.

        `scans: list <https://cloud.tenable.com/api#/resources/scans/list>`_

        Args:
            folder_id (int, optional): Only return scans within this folder.
            last_modified (datetime, optional):
                Only return scans that have been modified since the time
                specified.

        Returns:
            list: A list containing the list of scan resource records.

        Examples:
            >>> for scan in tio.scans.list():
            ...     pprint(scan)
        '''
        params = dict()
        if folder_id:
            params['folder_id'] = self._check('folder_id', folder_id, int)
        if last_modified:
            # for the last_modified datetime attribute, we will want to convert
            # that into a timestamp integer before passing it to the API.
            params['last_modification_date'] = int(time.mktime(self._check(
                'last_modified', last_modified, datetime).timetuple()))

        return self._api.get('scans', params=params).json()['scans']

    def pause(self, scan_id, block=False):
        '''
        Pauses a running scan.

        `scans: pause <https://cloud.tenable.com/api#/resources/scans/pause>`_

        Args:  
            scan_id (int): The unique identifier fo the scan to pause.
            block (bool, optional): 
                Block until the scan is actually paused.  Default is False.

        Returns:
            None: The scan was successfully requested to be paused.

        Examples:
            >>> tio.scans.pause(1)
        '''
        self._api.post('scans/{}/pause'.format(
            self._check('scan_id', scan_id, int)), json={})
        if block:
            self._block_while_running(scan_id)

    def plugin_output(self, scan_id, host_id, plugin_id, history_id=None):
        '''
        Retrieve the plugin output for a specific instance of a vulnerability
        on a host.

        `scans: plugin-output <https://cloud.tenable.com/api#/resources/scans/plugin-output>`_

        Args:
            scan_id (int): The unique identifier of the scan.
            host_id (int): The unique identifier of the scanned host.
            plugin_id (int): The plugin id.
            history_id (int, optional): 
                The unique identifier of the scan instance.

        Returns:
            dict: The plugin resource record for that plugin on that host.

        Examples:
            >>> output = tio.scans.plugin_output(1, 1, 1)
            >>> pprint(output)
        '''
        params = dict()
        if history_id:
            params['history_id'] = self._check('history_id', history_id, int)

        return self._api.get('scans/{}/hosts/{}/plugins/{}'.format(
            self._check('scan_id', scan_id, int),
            self._check('host_id', host_id, int),
            self._check('plugin_id', plugin_id, int)), params=params).json()

    def set_read_status(self, scan_id, read_status):
        '''
        Sets the read status of the scan.  This is generally used to toggle the
        unread status of the scan within the UI.

        `scans: read-status <https://cloud.tenable.com/api#/resources/scans/read-status>`_

        Args:
            scan_id (int): The unique identifier for the scan.
            read_status (bool): 
                Is the scan in a read or unread state?  True would denote read,
                whereas False is unread.

        Returns:
            None: The status of the scan was updated.

        Examples:
            Set a scan to unread:

            >>> tio.scans.set_read_status(1, False)
        '''
        self._api.put('scans/{}/status'.format(
                self._check('scan_id', scan_id, int)), json={
            'read': self._check('read_status', read_status, bool)
        })

    def resume(self, scan_id):
        '''
        Resume a paused scan.

        `scans: resume <https://cloud.tenable.com/api#/resources/scans/resume>`_

        Args:
            scan_id (int): The unique identifier for the scan.

        Returns:
            None: The scan was successfully requested to resume.

        Examples:
            >>> tio.scans.resume(1)
        '''
        self._api.post('scans/{}/resume'.format(
            self._check('scan_id', scan_id, int)))

    def schedule(self, scan_id, enabled):
        '''
        Enables or disables the scan schedule.

        `scans: schedule <https://cloud.tenable.com/api#/resources/scans/schedule>`_

        Args:
            scan_id (int): The unique identifier for the scan.
            enabled (bool): Enables or Disables the scan scheduling.

        Returns:
            dict: The schedule resource record for the scan.

        Examples:
            Enable a scan schedule:

            >>> tio.scans.schedule(1, True)
        '''
        return self._api.put('scans/{}/schedule'.format(
                self._check('scan_id', scan_id, int)), json={
            'enabled': self._check('enabled', enabled, bool)}).json()

    def stop(self, scan_id, block=False):
        '''
        Stop a running scan.

        `scans: stop <https://cloud.tenable.com/api#/resources/scans/stop>`_

        Args:
            scan_id (int): The unique identifier for the scan.
            block (bool, optional):
                Block until the scan is actually stopped.  Default is False.

        Returns:
            None: The scan was successfully requested to stop.

        Examples:
            Stop the scan asynchronously:

            >>> tio.scans.stop(1)

            Stop the scan and wait for the scan to stop:

            >>> tio.scans.stop(1, True)
        '''
        self._api.post('scans/{}/stop'.format(
            self._check('scan_id', scan_id, int)))
        if block:
            self._block_while_running(scan_id)

    def status(self, scan_id):
        '''
        Get the status of the latest instance of the scan.

        Args:
            scan_id (int): The unique identifier for the scan.

        Returns:
            str: The current status of the last instance.

        Examples:
            >>> tio.scans.status(1)
            u'completed'
        '''
        return self._api.get('scans/{}/latest-status'.format(
            self._check('scan_id', scan_id, int))).json()['status']

    def timezones(self):
        '''
        Retrieves the list of timezones.

        `scans: timezones <https://cloud.tenable.com/api#/resources/scans/timezones>`_

        Returns:
            list: List of allowed timezone strings accepted by Tenable.IO

        Examples:
            >>> for item in tio.scans.timezones():
            ...     pprint(item)
        '''
        resp = self._api.get('scans/timezones').json()['timezones']
        return [i['value'] for i in resp]

