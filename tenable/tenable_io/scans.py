from tenable.base import APIEndpoint
from datetime import datetime
import time

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

class ScansAPI(APIEndpoint):
    def attachment(self, scan_id, attachment_id, key, fobj=None):
        '''
        `scans: attachments <https://cloud.tenable.com/api#/resources/scans/attachments>`_

        Args:
            scan_id (int): The unique identifier for the scan.
            attachment_id (int): The unique identifier for the attachement
            key (str): The attachement access token.
            fobj (FileObject, optional): a file-like object you wish for the
                attachement to be written to.  If none is specified, a StringIO
                object will be returned with the contents of the attachment.

        Returns:
            FileObject: A file-like object with the attachement written into it.
        '''
        if not fobj:
            # if no file-like object is specified, then assign a StringIO object
            # to the variable.
            fobj = StringIO()

        # Make the HTTP call and stream the data into the file object.
        resp = self._api.get('scans/{}/attachments/{}'.format(
            self._check('scan_id', scan_id, int),
            self._check('attachment_id', attachment_id, int)
            ), params={'key': self._check('key', key, str)}, stream=True)
        for chunk in resp.iter_content(chunk_size=1024):
            if chunk:
                fobj.write(chunk)
        fobj.seek(0)

        # Return the file object to the ccaller.
        return fobj

#    def configure(self, id, json=None, **params):
#        '''
#        `scans: configure <https://cloud.tenable.com/api#/resources/scans/configure>`_
#
#        Args:
#            id (int): The unique identifier for the scan.
#            json (dict, optional):
#                A raw dictionary to push to the 
#            **params (dict, optional): 
#                The various parameters that can be passed to the scan 
#                configuration.  Examples would include `name`, `emails`, etc.
#                Please refer to the API documentation linked above for more
#                details.
#
#        Returns:
#            dict: The scan resource record.
#        '''
#        return self._api.put('scans/{}'.format(self._check('id', id, int)),
#                    json=params).json()

    def copy(self, scan_id, folder_id=None, name=None):
        '''
        `scans: copy <https://cloud.tenable.com/api#/resources/scans/copy>`_

        Args:
            scan_id (int): The unique identifier for the scan.
            folder_id (int, optional): The unique identifier for the folder.
            name (str, optional): The name for the copied scan.

        Returns:
            dict: The scan resource record for the copied scan.
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

#    def create(self, uuid, *credentials, **settings):
#        '''
#        `scans: create <https://cloud.tenable.com/api#/resources/scans/create>`_
#
#        Args:
#            **params (dict):
#                The various parameters that can be passed to the scan creation
#                API.  Examples would be `name`, `email`, `scanner_id`, etc.  For
#                more detailed informatiom, please refer to the API documentation
#                linked above.
#
#        Returns:
#            dict: The scan resource record of the newly created scan.
#        '''
#        self._api.post('scans', json=params).json()

    def delete(self, scan_id):
        '''
        `scans: delete <https://cloud.tenable.com/api#/resources/scans/delete>`_

        Args:
            scan_id (int): The unique identifier for the scan.

        Returns:
            None: scan successfully deleted.
        '''
        self._api.delete('scans/{}'.format(self._check('scan_id', scan_id, int)))

    def delete_history(self, scan_id, history_id):
        '''
        `scans: delete-history <https://cloud.tenable.com/api#/resources/scans/delete-history>`_

        Args:
            scan_id (int): The unique identifier for the scan.
            history_id (int): The unique identifier for the instance of the scan.

        Returns:
            None: Scan history successfully deleted.
        '''
        self._api.delete('scans/{}/hostory/{}'.format(
            self._check('scan_id', scan_id, int),
            self._check('history_id', history_id, int)))

    def details(self, scan_id, history_id=None):
        '''
        `scans: details <https://cloud.tenable.com/api#/resources/scans/details>`_

        Args:
            scan_id (int): The unique identifier for the scan.
            history_id (int, optional): 
                The unique identifier for the instance of the scan.

        Returns:
            dict: The scan result dictionary.
        '''
        params = dict()
        if history_id:
            params['history_id'] = self._check('history_id', history_id, int)

        self._api.get('scans/{}'.format(self._check('scan_id', scan_id, int)),
            params=params).json()


    def export(self, scan_id, *filters, **kw):
        '''
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
                `csv`, `html`, `pdf`, `db`.
            password (str, optional):
                If the export format is `db`, then what is the password used to
                encrypt the NessusDB file.  This is a require parameter for
                NessusDB exports.
            chapters (list, optional):
                A list of the chapters to write for the report.  The chapters
                list is only required for PDF and HTML exports.  Available
                chapters are `vuln_hosts_summary`, `vuln_by_host`, 
                `compliance_exec`, `remediations`, `vuln_by_plugin`, and
                `compliance`.  List order will denote output order.
            filter_type (str, optional):
                Are the filters exclusive (this AND this AND this) or inclusive
                (this OR this OR this).  Valid values are `and` and `or`.  The
                default setting is `and`.
            fobj (FileObject, optional):
                The file-like object to be returned with the exported data.  If
                no object is specified, a StringIO object is returned with the
                data.  While this is an optional parameter, it is highly
                recommended to use this paramater as exported files can be quite
                large, and StringIO objects are stored in memory, not on disk.

        Returns:
            FileObject: The file-like object of the requested export.
        '''

        # initiate the payload and parameters dictionaries.
        payload = dict()
        params = dict()


        # Interpret the filters into their native format.  The API docs are a
        # little off base here, as the filter format is actually filter.N.Y
        # instead of a list of dictionaries like the documentation states.
        if len(filters) > 0:
            payload['filters'] = []
            for f in filters:
                i = filters.index(f)
                payload['filter.{}.filter'.format(i)] = self._check(
                    'filter_name', f[0], str)
                payload['filter.{}.quality'.format(i)] = self._check(
                    'filter_quality', f[1], str)
                payload['filter.{}.value'.format(i)] = self._check(
                    'filter_value', f[2], str)

        if 'history_id' in kw:
            params['history_id'] = self._check(
                'history_id', kw['history_id'], int)

        if 'password' in kw:
            payload['password'] = self._check('password', kw['password'], str)

        if 'chapters' in kw:
            # The chapters are sent to us in a list, and we need to collapse
            # that down to a comma-delimited string.
            payload['chapters'] = ','.join(
                self._check('chapters', kw['chapters'], list, choices=[
                    'vuln_hosts_summary', 'vuln_by_host', 'vuln_by_plugin',
                    'compliance_exec', 'compliance', 'remediations'
                ]))

        if 'filter_type' in kw:
            payload['filter.search_type'] = self._check(
                    'filter_type', kw['filter_type'], str)

        # Now we need to set the FileObject.  If one was passed to us, then lets
        # just use that, otherwise we will need to instantiate a StingIO object
        # to push the data into.
        if 'fobj' in kw:
            fobj = kw['fobj']
        else:
            fobj = StringIO()

        # The first thing that we need to do is make the request and get the
        # File id for the job.
        fid = self._api.post('scans/{}/export'.format(
            self._check('scan_id', scan_id, int))).json()['file']

        # Next we will wait for the statif of the export request to become
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
        `scans: host-details <https://cloud.tenable.com/api#/resources/scans/host-details>`_

        Args:
            scan_id (int): The unique identifier for the scan.
            host_id (int): THe unique identifier for the host within the scan.
            histort_id (int, optional):
                The unique identifier for the instance of the scan.

        Returns:
            dict: The information related to the host requested.
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
        payload['file'] = self._api.file.upload(fobj)

        # make the call to Tenable.io to import and then return the result to
        # the caller.
        return self._api.post('scans/import', json=payload).json()

    def launch(self, scan_id, targets=None):
        '''
        `scans: launch <https://cloud.tenable.com/api#/resources/scans/launch>`_

        Args:
            scan_id (int): The unique identifier for the scan.
            targets (list, optional): 
                A list of targets to be scanned instead of the default targets
                in the scan.

        Response:
            str: The uuid of the scan instance (history).
        '''
        payload = dict()
        if targets:
            payload['alt_targets'] = ','.join(
                self._check('targets', targets, list))

        return self._api.post('scans/{}/launch'.format(
                self._check('scan_id', scan_id, int)), 
            json=payload).json()['scan_uuid']

    def list(self, folder_id=None, last_modified=None):
        '''
        `scans: list <https://cloud.tenable.com/api#/resources/scans/list>`_

        Args:
            folder_id (int, optional): Only return scans within this folder.
            last_modified (datetime, optional):
                Only return scans that have been modified since the time
                specified.

        Returns:
            dict: A dictionary containing the folder list and the scan list
        '''
        params = dict()
        if folder_id:
            params['folder_id'] = self._check('folder_id', folder_id, int)
        if last_modified:
            # for the last_modified datetime attribute, we will want to convert
            # that into a timestamp integer before passing it to the API.
            params['last_modified'] = int(time.mktime(self._check(
                'last_modified', last_modified, datetime)))

        return self._api.get('scans', params=params).json()

    def pause(self, scan_id):
        '''
        `scans: pause <https://cloud.tenable.com/api#/resources/scans/pause>`_

        Args:  
            scan_id (int): The unique identifier fo the scan to pause.

        Returns:
            None: The scan was successfully requested to be paused.
        '''
        self._api.post('scans/{}/pause'.format(
            self._check('scan_id', scan_id, int)), json={})

    def plugin_output(self, scan_id, host_id, plugin_id, history_id=None):
        '''
        `scans: plugin-output <https://cloud.tenable.com/api#/resources/scans/plugin-output>`_

        Args:
            scan_id (int): The unique identifier of the scan.
            host_id (int): The unique identifier of the scanned host.
            plugin_id (int): The plugin id.
            history_id (int, optional): 
                The unique identifier of the scan instance.

        Returns:
            dict: The plugin resource record for that plugin on that host.
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
        `scans: read-status <https://cloud.tenable.com/api#/resources/scans/read-status>`_

        Args:
            scan_id (int): The unique identifier for the scan.
            read_status (bool): 
                Is the scan in a read or unread state?  True would denote read,
                whereas False is unread.

        Returns:
            None: The status of the scan was updated.
        '''
        self._api.put('scans/{}/status'.format(
                self._check('scan_id', scan_id, int)), json={
            'read': self._check('read_status', read_status, bool)
        })

    def resume(self, scan_id):
        '''
        `scans: resume <https://cloud.tenable.com/api#/resources/scans/resume>`_

        Args:
            scan_id (int): The unique identifier for the scan.

        Returns:
            None: The scan was successfully requested to resume.
        '''
        self._api.post('scans/{}/resume'.format(
            self._check('scan_id', scan_id, int)))

    def schedule(self, scan_id, enabled):
        '''
        `scans: schedule <https://cloud.tenable.com/api#/resources/scans/schedule>`_

        Args:
            scan_id (int): The unique identifier for the scan.
            enabled (bool): Enables or Disables the scan scheduling.

        Returns:
            dict: The schedule resource record for the scan.
        '''
        return self._api.put('scans/{}/schedule'.format(
                self._check('scan_id', scan_id, int)), json={
            'enabled': self._check('enabled', enabled, bool)}).json()

    def stop(self, scan_id):
        '''
        `scans: stop <https://cloud.tenable.com/api#/resources/scans/stop>`_

        Args:
            scan_id (int): The unique identifier for the scan.

        Returns:
            None: The scan was successfully requested to stop.
        '''
        self._api.post('scans/{}/stop'.format(
            self._check('scan_id', scan_id, int)))

    def timezones(self):
        '''
        `scans: timezones <https://cloud.tenable.com/api#/resources/scans/timezones>`_

        Returns:
            list: List of allowed timezone strings accepted by Tenable.IO
        '''
        resp = self._api.get('scans/timezones').json()['timezones']
        return [i['value'] for i in resp]

