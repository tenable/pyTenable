'''
Scanners
========

The following methods allow for interaction into the Tenable.io
:devportal:`scanners <scanners>` API.

Methods available on ``tio.v3.vm.scanners``:

.. rst-class:: hide-signature
.. autoclass:: ScannersAPI
    :members:
'''

from typing import Dict, List
from uuid import UUID

from tenable.io.v3.base.endpoints.explore import ExploreBaseEndpoint
from typing_extensions import Literal

from .schema import ScannerEditSchema


class ScannersAPI(ExploreBaseEndpoint):

    _path = 'api/v3/scanners'
    _conv_json = True

    def linking_key(self) -> str:
        '''
        The linking key for the Tenable.io instance.

        Returns:
            str:
                The linking key

        Examples:
            >>> print(tio.v3.vm.scanners.linking_key())
        '''
        scanners = self.list()
        for scanner in scanners:
            if (
                scanner['id']
                == '00000000-0000-0000-0000-00000000000000000000000000001'
            ):
                return scanner['key']

    def allowed_scanners(self) -> List:
        '''
        A simple convenience function that returns the list
        of scanners that the current user is allowed to use.

        Returns:
            List:
                List of scanner documents.

        Examples:
            >>> for scanner in tio.v3.vm.scanners.allowed_scanners():
            ...     pprint(scanner)
        '''
        # We want to get the scanners that are available for scanning.
        # To do so, we will want to pull the information from the
        # scan template.  This isn't the prettiest way to handle this,
        # however it will consistently
        # return the results that we are looking for.
        # def get_scanners(tmpl):
        #     for item in tmpl['settings']['basic']['inputs']:
        #         if item['id'] == 'scanner_id':
        #             return item['options']
        #     return []

        # vm_tmpl = self._api.policies.templates().get('advanced', None)
        # was_tmpl = self._api.policies.templates().get('was_scan', None)
        # scanners = get_scanners(
        #    self._api.editor.template_details('scan', vm_tmpl)
        # )
        # if was_tmpl is not None:
        #     scanners.extend(
        #         get_scanners(
        #           self._api.editor.template_details('scan', was_tmpl)
        #         )
        #     )
        # return scanners

        return NotImplementedError(
            'This method will be updated once Policies and Editor APIs\
                are implemented in v3'
        )

    def control_scan(
        self,
        scanner_id: UUID,
        scan_uuid: UUID,
        action: Literal['resume', 'pause', 'stop'],
    ) -> None:
        '''
        Perform actions against scans on a given scanner.

        :devportal:`scanners: control-scans <scanners-control-scans>`

        Args:
            scanner_id: (uuid):
                The unique identifier for the scanner.
            scan_uuid (uuid):
                The unique identifier for the scan.
            action (str):
                The action to take upon the scan.  Valid actions are `stop`,
                `pause`, and `resume`.

        Returns:
            None:
                The action was sent to the scan successfully.

        Examples:
            Stop a scan running on the scanner:

            >>> tio.v3.vm.scanners.control_scan(
                1, '00000000-0000-0000-0000-000000000000',
                'stop'
                )
        '''
        self._post(
            f'{scanner_id}/scans/{scan_uuid}/control',
            json={
                'action': action})

    def delete(self, id: UUID) -> None:
        '''
        Delete a scanner from Tenable.io.

        :devportal:`scanners: delete <scanners-delete>`

        Args:
            id (uuid):
                The unique identifier for the scanner to delete.

        Returns:
            None:
                The scanner was successfully deleted.

        Examples:
            >>> tio.v3.vm.scanners.delete(1)
        '''
        self._delete(f'{id}')

    def details(self, id: UUID) -> Dict:
        '''
        Retrieve the details for a specified scanner.

        :devportal:`scanners: details <scanners-details>`

        Args:
            id: (uuid):
                The unique identifier for the scanner

        Returns:
            Dict:
                The scanner resource record.

        Examples:
            >>> scanner = tio.v3.vm.scanners.details(1)
            >>> pprint(scanner)
        '''
        return self._get(f'{id}')

    def edit(self, id: UUID, **kwargs) -> None:
        '''
        Modify the scanner.

        :devportal:`scanners: edit <scanners-edit>`

        Args:
            id: (uuid):
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
                For AWS scanners this will inform the scanner
                how often to check into Tenable.io.

        Returns:
            None:
                The operation was requested successfully.

        Examples:
            Force a plugin update on a scanner:

            >>> tio.v3.vm.scanners.edit(1, force_plugin_update=True)
        '''
        payload = dict()
        schema = ScannerEditSchema()
        payload = schema.dump(schema.load(kwargs))
        self._api.put(f'settings/{id}', json=payload)

    def get_aws_targets(self, id: UUID) -> List:
        '''
        Returns the list of AWS targets the scanner can reach.

        :devportal:`scanners: get-aws-targets <scanners-get-aws-targets>`

        Args:
            id: (uuid): The unique identifier for the scanner.

        Returns:
            List:
                List of aws target resource records.

        Examples:
            >>> for target in tio.v3.vm.scanners.get_aws_targets(1):
            ...      pprint(target)
        '''
        return self._get(f'{id}/aws-targets')['targets']

    def get_scanner_key(self, id: UUID) -> str:
        '''
        Return the key associated with the scanner.

        :devportal:`scanners: get-scanner-key <scanners-get-scanner-key>`

        Args:
            id: (uuid): The unique identifier for the scanner.

        Returns:
            str:
                The scanner key

        Examples:
            >>> print(tio.v3.vm.scanners.get_scanner_key(1))
        '''
        return str(self._get(f'{id}/key')['key'])

    def get_scans(self, id: UUID) -> List:
        '''
        Retrieves the scans associated to the scanner.

        :devportal:`scanners: get-scans <scanners-get-scans>`

        Args:
            id: (uuid): The unique identifier for the scanner.

        Returns:
            List:
                List of scan resource records associated to the scanner.

        Examples:
            >>> for scan in tio.v3.vm.scanners.get_scans(1):
            ...     pprint(scan)
        '''
        return self._get(f'{id}/scans')['scans']

    def search(self) -> List:
        '''
        Search endpoint introduced in v3.

        :devportal:`scanners: search <scanners-search>`

        Returns:
            List:
                Iterator Class object
                TODO Implementation of base iterator class
                ExploreSearchIterator needs to be updated at v3/base/iterator
        Examples:
            TODO
        '''
        raise NotImplementedError(
            'This method will be updated once ExploreSearchIterator is \
                implemented for v3'
        )

    def list(self) -> List:
        '''
        Retrieves the list of scanners.

        :devportal:`scanners: list <scanners-list>`

        Returns:
            List:
                List of scanner resource records.

        Examples:
            >>> for scanner in tio.scanners.list():
            ...     pprint(scanner)
        '''
        return self._get()['scanners']

    def toggle_link_state(self, id: UUID, linked: bool) -> None:
        '''
        Toggles the scanner's activated state.

        :devportal:`scanners: toggle-link-state <scanners-toggle-link-state>`

        Args:
            id: (uuid): The unique identifier for the scanner
            linked (bool):
                The link status of the scanner.
                Setting to `False` will disable
                the link, whereas setting to `True` will enable the link.

        Returns:
            None:
                The status change was successful.

        Examples:
            to deactivate a linked scanner:

            >>> tio.v3.vm.scanners.toggle_link_state(1, False)
        '''
        self._put(
            f'{id}/link',
            json={'link': int(linked)},
        )

    def get_permissions(self, id: UUID) -> Dict:
        '''
        Returns the permission list for a given scanner.

        Args:
            id: (uuid): The unique identifier for the scanner.

        Returns:
            Dict:
                The permissions resource for the scanner

        Examples:
            >>> tio.v3.vm.scanners.get_permissions(1)
        '''
        # return self._api.permissions.list('scanner', self._check('id', id,
        # int))
        raise NotImplementedError(
            'This method will be updated once Permissions API is \
                migrated to v3'
        )

    def edit_permissions(self, id: UUID, *acls) -> None:
        '''
        Modifies the permissions list for the given scanner.

        Args:
            id: (uuid):The unique identifier for the scanner.
            *acls (dict): The permissions record(s) for the scanner.

        Returns:
            None:
                The permissions have been updated successfully.

        Examples:
            >>> tio.v3.vm.scanners.edit_permissions(1,
            ...     {'type': 'default, 'permissions': 16},
            ...     {'type': 'user', 'id': 2, 'permissions': 16})
        '''
        # self._api.permissions.change('scanner',
        #   self._check('id', id, int),
        #   *acls
        # )
        raise NotImplementedError(
            'This method will be updated once Permissions API is migrated \
                to v3'
        )
