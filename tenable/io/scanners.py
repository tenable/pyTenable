'''
Scanners
========

The following methods allow for interaction into the Tenable Vulnerability Management
:devportal:`scanners <scanners>` API.

Methods available on ``tio.scanners``:

.. rst-class:: hide-signature
.. autoclass:: ScannersAPI
    :members:
'''
from .base import TIOEndpoint

SCANNERS_ = 'scanners/{}'


class ScannersAPI(TIOEndpoint):

    def linking_key(self):
        '''
        The linking key for the Tenable Vulnerability Management instance.

        Returns:
            :obj:`str`:
                The linking key

        Examples:
            >>> print(tio.scanners.linking_key())
        '''
        scanners = self.list()
        for scanner in scanners:
            if scanner['uuid'] == '00000000-0000-0000-0000-00000000000000000000000000001':
                return scanner['key']

    def allowed_scanners(self):
        '''
        A simple convenience function that returns the list of scanners that the
        current user is allowed to use.

        Returns:
            :obj:`list`:
                List of scanner documents.

        Examples:
            >>> for scanner in tio.scanners.allowed_scanners():
            ...     pprint(scanner)
        '''
        # We want to get the scanners that are available for scanning.  To do so,
        # we will want to pull the information from the scan template.  This
        # isn't the prettiest way to handle this, however it will consistently
        # return the results that we are looking for.
        def get_scanners(tmpl):
            for item in tmpl['settings']['basic']['inputs']:
                if item['id'] == 'scanner_id':
                    return item['options']
            return []

        vm_tmpl = self._api.policies.templates().get('advanced', None)
        was_tmpl = self._api.policies.templates().get('was_scan', None)
        scanners = get_scanners(self._api.editor.template_details('scan', vm_tmpl))
        if was_tmpl is not None:
            scanners.extend(get_scanners(self._api.editor.template_details('scan', was_tmpl)))
        return scanners

    def control_scan(self, scanner_id, scan_uuid, action):
        '''
        Perform actions against scans on a given scanner.

        :devportal:`scanners: control-scans <scanners-control-scans>`

        Args:
            scanner_id (int):
                The unique identifier for the scanner.
            scan_uuid (uuid):
                The unique identifier for the scan.
            action (str):
                The action to take upon the scan.  Valid actions are `stop`,
                `pause`, and `resume`.

        Returns:
            :obj:`None`:
                The action was sent to the scan successfully.

        Examples:
            Stop a scan running on the scanner:

            >>> tio.scanners.control_scan(1, '00000000-0000-0000-0000-000000000000', 'stop')
        '''
        self._api.post('scanners/{}/scans/{}/control'.format(
            self._check('scanner_id', scanner_id, int),
            self._check('scan_uuid', scan_uuid, str),
            ), json={'action': self._check('action', action, str,
                                        choices=['stop', 'pause', 'resume'])})

    def delete(self, id):
        '''
        Delete a scanner from Tenable Vulnerability Management.

        :devportal:`scanners: delete <scanners-delete>`

        Args:
            id (int):
                The unique identifier for the scanner to delete.

        Returns:
            :obj:`None`:
                The scanner was successfully deleted.

        Examples:
            >>> tio.scanners.delete(1)
        '''
        self._api.delete(SCANNERS_.format(self._check('id', id, int)))

    def details(self, id):
        '''
        Retrieve the details for a specified scanner.

        :devportal:`scanners: details <scanners-details>`

        Args:
            id (int):
                The unique identifier for the scanner

        Returns:
            :obj:`dict`:
                The scanner resource record.

        Examples:
            >>> scanner = tio.scanners.details(1)
            >>> pprint(scanner)
        '''
        return self._api.get(SCANNERS_.format(
            self._check('id', id, int))).json()

    def edit(self, id, **kwargs):
        '''
        Modify the scanner.

        :devportal:`scanners: edit <scanners-edit>`

        Args:
            id (int):
                The unique identifier for the scanner.
            force_plugin_update (bool, optional):
                Force the scanner to perform a plugin update .
            force_ui_update (bool, optional):
                Force the scanner to perform a UI update.
            finish_update (bool, optional):
                Force the scanner to reboot to complete the update process.
                This action is only valid when automatic updates are disabled.
            registration_code (str, optional):
                Sets the registration code for the scanner.
            aws_update_interval (int, optional):
                For AWS scanners this will inform the scanner how often to check
                into Tenable Vulnerability Management.

        Returns:
            :obj:`None`:
                The operation was requested successfully.

        Examples:
            Force a plugin update on a scanner:

            >>> tio.scanners.edit(1, force_plugin_update=True)
        '''
        payload = dict()
        if ('force_plugin_update' in kwargs
            and self._check('force_plugin_update', kwargs['force_plugin_update'], bool)):
            payload['force_plugin_update'] = 1
        if ('force_ui_update' in kwargs
            and self._check('force_ui_update', kwargs['force_ui_update'], bool)):
            payload['force_ui_update'] = 1
        if ('finish_update' in kwargs
            and self._check('finish_update', kwargs['finish_update'], bool)):
            payload['finish_update'] = 1
        if ('registration_code' in kwargs
            and self._check('registration_code', kwargs['registration_code'], str)):
            payload['registration_code'] = kwargs['registration_code']
        if ('aws_update_interval' in kwargs
            and self._check('aws_update_interval', kwargs['aws_update_interval'], int)):
            payload['aws_update_interval'] = kwargs['aws_update_interval']

        self._api.put(SCANNERS_.format(self._check('id', id, int)),
                      json=payload)

    def get_aws_targets(self, id):
        '''
        Returns the list of AWS targets the scanner can reach.

        :devportal:`scanners: get-aws-targets <scanners-get-aws-targets>`

        Args:
            id (int): The unique identifier for the scanner.

        Returns:
            :obj:`list`:
                List of aws target resource records.

        Examples:
            >>> for target in tio.scanners.get_aws_targets(1):
            ...      pprint(target)
        '''
        return self._api.get('scanners/{}/aws-targets'.format(
                    self._check('id', id, int))).json()['targets']

    def get_scanner_key(self, id):
        '''
        Return the key associated with the scanner.

        :devportal:`scanners: get-scanner-key <scanners-get-scanner-key>`

        Args:
            id (int): The unique identifier for the scanner.

        Returns:
            :obj:`str`:
                The scanner key

        Examples:
            >>> print(tio.scanners.get_scanner_key(1))
        '''
        return str(self._api.get('scanners/{}/key'.format(
            self._check('id', id, int))).json()['key'])

    def get_scans(self, id):
        '''
        Retrieves the scans associated to the scanner.

        :devportal:`scanners: get-scans <scanners-get-scans>`

        Args:
            id (int): The unique identifier for the scanner.

        Returns:
            :obj:`list`:
                List of scan resource records associated to the scanner.

        Examples:
            >>> for scan in tio.scanners.get_scans(1):
            ...     pprint(scan)
        '''
        return self._api.get('scanners/{}/scans'.format(
            self._check('id', id, int))).json()['scans']

    def list(self):
        '''
        Retrieves the list of scanners.

        :devportal:`scanners: list <scanners-list>`

        Returns:
            :obj:`list`:
                List of scanner resource records.

        Examples:
            >>> for scanner in tio.scanners.list():
            ...     pprint(scanner)
        '''
        return self._api.get('scanners').json()['scanners']

    def toggle_link_state(self, id, linked):
        '''
        Toggles the scanner's activated state.

        :devportal:`scanners: toggle-link-state <scanners-toggle-link-state>`

        Args:
            id (int): The unique identifier for the scanner
            linked (bool):
                The link status of the scanner.  Setting to `False` will disable
                the link, whereas setting to `True` will enable the link.

        Returns:
            :obj:`None`:
                The status change was successful.

        Examples:
            to deactivate a linked scanner:

            >>> tio.scanners.toggle_link_state(1, False)
        '''
        self._api.put('scanners/{}/link'.format(self._check('id', id, int)),
            json={'link': int(self._check('linked', linked, bool))})

    def get_permissions(self, id):
        '''
        Returns the permission list for a given scanner.

        Args:
            id (int): The unique identifier for the scanner.

        Returns:
            :obj:`dict`:
                The permissions resource for the scanner

        Examples:
            >>> tio.scanners.get_permissions(1)
        '''
        return self._api.permissions.list('scanner', self._check('id', id, int))

    def edit_permissions(self, id, *acls):
        '''
        Modifies the permissions list for the given scanner.

        Args:
            id (int):The unique identifier for the scanner.
            *acls (dict): The permissions record(s) for the scanner.

        Returns:
            :obj:`None`:
                The permissions have been updated successfully.

        Examples:
            >>> tio.scanners.edit_permissions(1,
            ...     {'type': 'default, 'permissions': 16},
            ...     {'type': 'user', 'id': 2, 'permissions': 16})
        '''
        self._api.permissions.change('scanner', self._check('id', id, int), *acls)
