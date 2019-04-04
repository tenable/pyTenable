'''
scan_instances
==============

The following methods allow for interaction into the Tenable.sc 
`Scan Result <https://docs.tenable.com/sccv/api/Scan-Result.html>`_ API.  While
the Tenable.sc API refers to the model these endpoints interact with as 
*ScanResult*, were actually interacting with an instance of a scan definition
stored within the *Scan* API endpoints.  These scan instances could be running
scans, stopped scans, errored scans, or completed scans.  These items are
typically seen under the **Scan Results** section of Tenable.sc.

Methods available on ``sc.scan_instances``:

.. rst-class:: hide-signature
.. autoclass:: ScanResultAPI

    .. automethod:: copy
    .. automethod:: delete
    .. automethod:: details
    .. automethod:: email
    .. automethod:: export_scan
    .. automethod:: import_scan
    .. automethod:: list
    .. automethod:: pause
    .. automethod:: reimport_scan
    .. automethod:: resume
    .. automethod:: stop
'''
from .base import SCEndpoint
from tenable.utils import dict_merge
from io import BytesIO

class ScanResultAPI(SCEndpoint):
    def copy(self, id, *users):
        '''
        Clones the scan instance.

        + `SC ScanResult Copy <https://docs.tenable.com/sccv/api/Scan-Result.html#ScanResultRESTReference-/scanResult/{id}/copy>`_

        Args:
            id (int): The identifier of the scan instance to clone.
            *users (int): 
                A user id to associate to the scan instance.

        Returns:
            dict

        Examples:
            >>> sc.scan_instances.copy(1)
        '''
        payload = dict()
        if users:
            payload['users'] = [{'id': self._check('user:id', u, int)} for u in users]
        return self._api.post('scanResult/{}/copy'.format(
            self._check('id', id, int)), json=payload).json()['response']

    def delete(self, id):
        '''
        Removes the scan instance from TenableSC.

        + `SC ScanResult Delete <https://docs.tenable.com/sccv/api/Scan-Result.html#scanResult_id_DELETE>`_

        Args:
            id (int): The identifier of the scan instance to delete.

        Returns:
            dict

        Examples:
            >>> sc.scan_instances.delete(1)
        '''
        return self._api.delete('scanResult/{}'.format(
            self._check('id', id, int))).json()['response']

    def details(self, id, fields=None):
        '''
        Retreives the details for the specified scan instance.

        + `SC ScanResult <https://docs.tenable.com/sccv/api/Scan-Result.html#scanResult_id_GET>`_

        Args:
            id (int): The identifier for the scan instance to be retrieved.
            fields (list, optional): 
                List of fields to return.  Refer to the API documentation
                referenced above for a list of available fields.

        Returns:
            dict: The scan instance resource record.

        Examples:
            Getting the details of a scan instance with just the 
            default parameters:

            >>> scan = sc.scan_instances.details(1)
            >>> pprint(scan)

            Specifying what fields you'd like to be returned:

            >>> scan = sc.scan_instances.details(1, 
            ...     fields=['name', 'status', 'scannedIPs', 'startTime', 'finishTime'])
            >>> pprint(scan)
        '''
        params = dict()
        if fields:
            params['fields'] = ','.join([self._check('field', f, str) 
                for f in self._check('fields', fields, list)])
        return self._api.get('scanResult/{}'.format(self._check('id', id, int)),
            params=params).json()['response']

    def email(self, id, *emails):
        '''
        Emails the scan results of the requested scan to the email addresses
        defined.

        + `SC ScanResult Email <https://docs.tenable.com/sccv/api/Scan-Result.html#ScanResultRESTReference-/scanResult/{id}/email>`_

        Args:
            id (int): The identifier for the specified scan instance.
            *emails (str): Valid email address.

        Returns:
            str: Empty string response.

        Examples:
            >>> sc.scan_instances.email(1, 'email@company.tld')
        '''
        return self._api.post('scanResult/{}/email'.format(
            self._check('id', id, int)), json={'email': ','.join(
                [self._check('address', e, str) for e in emails])}).json()['response']

    def export_scan(self, id, fobj=None, export_format=None):
        '''
        Downloads the results of the scan.

        + `SC ScanResult Download <https://docs.tenable.com/sccv/api/Scan-Result.html#ScanResultRESTReference-/scanResult/{id}/download>`_

        Args:
            id (int): The scan instance identifier.
            export_format (str, optional):
                The format of the resulting data.  Allowable values are
                ``scap1_2`` and ``v2``.  ``v2`` is the default value if none
                are specified.
            fobj (FileObject, optional):
                The file-like object to write the resulting file into.  If
                no file-like object is provided, a BytesIO objects with the
                downloaded file will be returned.  Be aware that the default
                option of using a BytesIO object means that the file will be
                stored in memory, and it's generally recommended to pass an
                actual file-object to write to instead.

        Returns:
            FileObject: The file-like object with the resulting zipped report.

        Examples:
            >>> with open('example.zip', 'wb') as fobj:
            ...     sc.scan_instances.export_scan(1, fobj)
        '''
        resp = self._api.post('scanResult/{}/download'.format(
            self._check('id', id, int)), stream=True, json={
                'downloadType': self._check('export_format', export_format, str,
                    choices=['scap1_2', 'v2'], default='v2')})

        # if no file-like object was passed, then we will instantiate a BytesIO
        # object to push the file into.
        if not fobj:
            fobj = BytesIO()

        # Lets stream the file into the file-like object...
        for chunk in resp.iter_content(chunk_size=1024):
            if chunk:
                fobj.write(chunk)
        fobj.seek(0)
        return fobj

    def import_scan(self, fobj, repo, **kw):
        '''
        Imports a nessus file into Tenable.sc.

        + `SC Scan Import <https://docs.tenable.com/sccv/api/Scan-Result.html#ScanResultRESTReference-/scanResult/import>`_

        Args:
            fobj (FileObject):
                The file-like object containing the Nessus file to import.
            repo (int):
                The repository id for the scan.
            auto_mitigation (int, optional):
                How many days to hold on to data before mitigating it?  The 
                default value is 0.
            host_tracking (bool, optional):
                Should DHCP host tracking be enabled?  The default is False.
            vhosts (bool, optional):
                Should virtual host logic be enabled for the scan?  The default
                is ``False``.

        Returns:
            str: An empty string response.

        Examples:
            >>> with open('example.nessus') as fobj:
            ...     sc.scan_instances.import_scan(fobj, 1)
        '''
        kw['repo'] = repo
        payload = self._api.scans._constructor(**kw)
        payload['filename'] = self._api.files.upload(fobj)
        return self._api.post(
            'scanResult/import', json=payload).json()['response']

    def reimport_scan(self, id, **kw):
        '''
        Re-imports an existing scan into the cumulative repository.

        + `SC Scan Re-Import <https://docs.tenable.com/sccv/api/Scan-Result.html#ScanResultRESTReference-/scanResult/{id}/import>`_

        Args:
            id (int):
                The scan instance identifier.
            auto_mitigation (int, optional):
                How many days to hold on to data before mitigating it?  The 
                default value is 0.
            host_tracking (bool, optional):
                Should DHCP host tracking be enabled?  The default is False.
            vhosts (bool, optional):
                Should virtual host logic be enabled for the scan?  The default
                is ``False``.

        Returns:
            str: An emty string response.

        Examples:
            >>> sc.scan_instances.reimport_scan(1)
        '''
        payload = self._api.scans._constructor(**kw)
        return self._api.post('scanResult/{}/import'.format(self._check(
            'id', id, int)), json=payload).json()['response']

    def list(self, fields=None):
        '''
        Retreives the list of scan instances.

        + `SC ScanResult List <https://docs.tenable.com/sccv/api/Scan-Result.html#ScanResultRESTReference-/scanResult>`_

        Args:
            fields (list, optional): 
                A list of attributes to return.

        Returns:
            dict: A list of scan instance resources.

        Examples:
            * Retreiving all of the manageable scans instances:

            >>> for scan in sc.scan_instances.list()['manageable']:
            ...     pprint(scan)
        '''
        params = dict()
        if fields:
            params['fields'] = ','.join([self._check('field', f, str) 
                for f in fields])

        return self._api.get('scanResult', params=params).json()['response']

    def pause(self, id):
        '''
        Pauses a running scan instance.  Note that this will not impact agent
        scan instances.

        + SC Scan Pause <https://docs.tenable.com/sccv/api/Scan-Result.html#ScanResultRESTReference-/scanResult/{id}/pause>`_

        Args:
            id (int): The unique identifier for the scan instance.

        Returns:
            dict: The Scan instance state

        Examples:
            >>> sc.scan_instances.pause(1)
        '''
        return self._api.post('scanResult/{}/pause'.format(self._check(
            'id', id, int))).json()['response']

    def resume(self, id):
        '''
        Resumes a paused scan instance.  Note that this will not impact agent
        scan instances.

        + SC Scan Resume <https://docs.tenable.com/sccv/api/Scan-Result.html#ScanResultRESTReference-/scanResult/{id}/resume>`_

        Args:
            id (int): The unique identifier for the scan instance.

        Returns:
            dict: The Scan instance state

        Examples:
            >>> sc.scan_instances.resume(1)
        '''
        return self._api.post('scanResult/{}/resume'.format(self._check(
            'id', id, int))).json()['response']

    def stop(self, id):
        '''
        Stops a running scan instance.  Note that this will not impact agent
        scan instances.

        + SC Scan Stop <https://docs.tenable.com/sccv/api/Scan-Result.html#ScanResultRESTReference-/scanResult/{id}/stop>`_

        Args:
            id (int): The unique identifier for the scan instance.

        Returns:
            dict: The Scan instance state

        Examples:
            >>> sc.scan_instances.stop(1)
        '''
        return self._api.post('scanResult/{}/stop'.format(self._check(
            'id', id, int))).json()['response']
