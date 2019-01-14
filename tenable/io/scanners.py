'''
scanners
========

The following methods allow for interaction into the Tenable.io 
`scanners <https://cloud.tenable.com/api#/resources/scanners>`_ API.

Methods available on ``tio.scanners``:

.. rst-class:: hide-signature
.. autoclass:: ScannersAPI

    .. automethod:: control_scan
    .. automethod:: delete
    .. automethod:: details
    .. automethod:: edit
    .. automethod:: get_aws_targets
    .. automethod:: get_scanner_key
    .. automethod:: get_scans
    .. automethod:: linking_key
    .. automethod:: list
    .. automethod:: toggle_link_state
'''
from .base import TIOEndpoint

class ScannersAPI(TIOEndpoint):

    def linking_key(self):
        '''
        The linking key for the Tenable.io instance.

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
            list: List of scanner documents.

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

        vm_tmpl = self._api.policies.templates()['advanced']
        was_tmpl = self._api.policies.templates()['was_scan']
        vm_scanners = get_scanners(self._api.editor.details('scan', vm_tmpl))
        was_scanners = get_scanners(self._api.editor.details('scan', was_tmpl))
        return vm_scanners + was_scanners

    def control_scan(self, scanner_id, scan_uuid, action):
        '''
        Perform actions against scans on a given scanner.

        `scanners: control-scans <https://cloud.tenable.com/api#/resources/scanners/control-scans>`_

        Args:
            scanner_id (int):
                The unique identifier for the scanner.
            scan_uuid (uuid):
                The unique identifier for the scan.
            action (str):
                The action to take upon the scan.  Valid actions are `stop`,
                `pause`, and `resume`.

        Returns:
            None: The action was sent to the scan successfully.

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
        Delete a scanner from Tenable.io.

        `scanners: delete <https://cloud.tenable.com/api#/resources/scanners/delete>`_

        Args:
            id (int):
                The unique identifier for the scanner to delete.

        Returns:
            None: The scanner was successfully deleted.

        Examples:
            >>> tio.scanners.delete(1)
        '''
        self._api.delete('scanners/{}'.format(self._check('id', id, int)))

    def details(self, id):
        '''
        Retrieve the details for a specified scanner.

        `scanners: details <https://cloud.tenable.com/api#/resources/scanners/details>`_

        Args:
            id (int):
                The unique identifier for the scanner

        Returns:
            dict: The scanner resource record.

        Examples:
            >>> scanner = tio.scanners.details(1)
            >>> pprint(scanner)
        '''
        return self._api.get('scanners/{}'.format(
            self._check('id', id, int))).json()

    def edit(self, id, **kwargs):
        '''
        Modify the scanner.

        `scanners: edit <https://cloud.tenable.com/api#/resources/scanners/edit>`_

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
                into Tenable.io.

        Returns:
            None: The operation was requested successfully.

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

        self._api.put('settings/{}'.format(self._check('id', id, int)), 
            json=payload)

    def get_aws_targets(self, id):
        '''
        Returns the list of AWS targets the scanner can reach.

        `scanners: get-aws-targets <https://cloud.tenable.com/api#/resources/scanners/get-aws-targets>`_

        Args:
            id (int): The unique identifier for the scanner.

        Returns:
            list: List of aws target resource records.

        Examples:
            >>> for target in tio.scanners.get_aws_targets(1):
            ...      pprint(target)
        '''
        return self._api.get('scanners/{}/aws-targets'.format(
                    self._check('id', id, int))).json()['targets']

    def get_scanner_key(self, id):
        '''
        Return the key associated with the scanner.

        `scanners: get-scanner-key <https://cloud.tenable.com/api#/resources/scanners/get-scanner-key>`_

        Args:
            id (int): The unique identifier for the scanner.

        Returns:
            str: The scanner key

        Examples:
            >>> print(tio.scanners.get_scanner_key(1))
        '''
        return str(self._api.get('scanners/{}/key'.format(
            self._check('id', id, int))).json()['key'])

    def get_scans(self, id):
        '''
        Retrieves the scans associated to the scanner.

        `scanners: get-scans <https://cloud.tenable.com/api#/resources/scanners/get-scans>`_

        Args:
            id (int): The unique identifier for the scanner.

        Returns:
            list: List of scan resource records associated to the scanner.

        Examples:
            >>> for scan in tio.scanners.get_scans(1):
            ...     pprint(scan)
        '''
        return self._api.get('scanners/{}/scans'.format(
            self._check('id', id, int))).json()['scans']

    def list(self):
        '''
        Retrieves the list of scanners.

        `scanners: list <https://cloud.tenable.com/api#/resources/scanners/list>`_

        Returns:
            list: List of scanner resource records.

        Examples:
            >>> for scanner in tio.scanners.list():
            ...     pprint(scanner)
        '''
        return self._api.get('scanners').json()['scanners']

    def toggle_link_state(self, id, linked):
        '''
        Toggles the scanner's activated state.

        `scanners: toggle-link-state <https://cloud.tenable.com/api#/resources/scanners/toggle-link-state>`_

        Args:
            id (int): The unique identifier for the scanner
            linked (bool): 
                The link status of the scanner.  Setting to `False` will disable
                the link, whereas setting to `True` will enable the link.

        Returns:
            None: The status change was successful.

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
            dict: The permissions resource for the scanner
        
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
            None: The permissions have been updated successfully.
        
        Examples:
            >>> tio.scanners.edit_permissions(1, 
            ...     {'type': 'default, 'permissions': 16},
            ...     {'type': 'user', 'id': 2, 'permissions': 16})
        '''
        self._api.permissions.change('scanner', self._check('id', id, int), *acls)