'''
Assets
======

The following methods allow for interaction into the Tenable Vulnerability Management
:devportal:`assets <assets>` API endpoints.

Methods available on ``tio.assets``:

.. rst-class:: hide-signature
.. autoclass:: AssetsAPI
    :members:
'''
from tenable.io.base import TIOEndpoint


class AssetsAPI(TIOEndpoint):
    '''
    This will contain all methods related to Assets
    '''

    def list(self):
        '''
        Returns a list of assets.

        :devportal:`assets: list-assets <assets-list-assets>`

        Returns:
            :obj:`list`:
                List of asset records.

        Examples:
            >>> for asset in tio.assets.list():
            ...     pprint(asset)
        '''
        return self._api.get('assets').json()['assets']

    def delete(self, uuid):
        '''
        Deletes the asset.

        :devportal:`workbenches: asset-delete <workbenches-asset-delete>`

        Args:
            asset_uuid (str): The unique identifier for the asset.

        Returns:
            :obj:`None`:

        Examples:
            >>> asset_id = '00000000-0000-0000-0000-000000000000'
            >>> tio.asset.delete(asset_id)
        '''
        self._api.delete('workbenches/assets/{}'.format(
            self._check('uuid', uuid, 'uuid')))

    def details(self, uuid):
        '''
        Retrieves the details about a specific asset.

        :devportal:`assets: asset-info <assets-asset-info>`

        Args:
            uuid (str):
                The UUID (unique identifier) for the asset.

        Returns:
            :obj:`dict`:
                Asset resource definition.

        Examples:
            >>> asset = tio.assets.details(
            ...     '00000000-0000-0000-0000-000000000000')
        '''
        return self._api.get(
            'assets/{}'.format(
                self._check('uuid', uuid, str)
            )).json()

    def assign_tags(self, action, assets, tags):
        '''
        Add/remove tags for asset(s).

        :devportal:`tags: assign-asset-tags <tags-assign-asset-tags>`

        Args:
            action (str):
                Specifies whether to add or remove tags. Valid values: add, remove.
            assets (List[str]):
                An array of asset UUIDs.
            tags (List[str]):
                An array of tag value UUIDs.

        Returns:
            :obj:`dict`:
                The job Resource record.

        Examples:
            >>> asset = tio.assets.assign_tags(
            ...     'add', ['00000000-0000-0000-0000-000000000000'],
            ...     ['00000000-0000-0000-0000-000000000000'])
        '''
        return self._api.post(
            'tags/assets/assignments', json={
                'action': self._check('action', action, str, choices=['add', 'remove']),
                'assets': [self._check('asset', i, 'uuid') for i in assets],
                'tags': [self._check('source', i, 'uuid') for i in tags]
            }).json()

    def tags(self, uuid):
        '''
        Retrieves the details about a specific asset.

        :devportal:`tags: asset-tags <tags-list-asset-tags>`

        Args:
            uuid (str):
                The UUID (unique identifier) for the asset.

        Returns:
            :obj:`dict`:
                Asset resource definition.

        Examples:
            >>> asset = tio.assets.tags(
            ...     '00000000-0000-0000-0000-000000000000')
        '''
        return self._api.get(
            'tags/assets/{}/assignments'.format(
                self._check('uuid', uuid, 'uuid')
            )).json()

    def asset_import(self, source, *assets):
        '''
        Imports asset information into Tenable Vulnerability Management from an external source.

        :devportal:`assets: import <assets-import>`

        Imports a list of asset definition dictionaries.  Each asset record must
        contain at least one of the following attributes: ``fqdn``, ``ipv4``,
        ``netbios_name``, ``mac_address``.  Each record may also contain
        additional properties.

        Args:
            *assets (dict):
                One or more asset definition dictionaries
            source (str):
                An identifier to be used to upload the assets.

        Returns:
            :obj:`str`:
                The job UUID.

        Examples:
            import single asset:

            >>> tio.assets.asset_import('example_source', {
            ...     'fqdn': ['example.py.test'],
            ...     'ipv4': ['192.168.254.1'],
            ...     'netbios_name': 'example',
            ...     'mac_address': ['00:00:00:00:00:00']
            ... })

            import multiple asset:

            >>> tio.assets.asset_import('multiple_asset_example_source',
            ...     {
            ...         'fqdn': ['example_one.py.test'],
            ...         'ipv4': ['192.168.1.1'],
            ...         'netbios_name': 'example_one',
            ...         'mac_address': ['00:00:00:00:00:00']
            ...     },{
            ...         'fqdn': ['example_two.py.test'],
            ...         'ipv4': ['192.168.255.1'],
            ...         'netbios_name': 'example_two',
            ...         'mac_address': ['00:00:00:00:00:00']
            ...     })
        '''
        # We will likely want to perform some more stringent checking of the
        # asset resources that are being defined, however a simple type check
        # should suffice for now.
        return self._api.post(
            'import/assets', json={
                'assets': [self._check('asset', i, dict) for i in assets],
                'source': self._check('source', source, str)
            }).json()['asset_import_job_uuid']

    def list_import_jobs(self):
        '''
        Returns a list of asset import jobs.

        :devportal:`assets: list-import-jobs <assets-list-import-jobs>`

        Returns:
            :obj:`list`:
                List of job records.

        Examples:
            >>> for job in tio.assets.list_import_jobs():
            ...     pprint(job)
        '''
        return self._api.get('import/asset-jobs').json()['asset_import_jobs']

    def import_job_details(self, uuid):
        '''
        Returns the details about a specific asset import job.

        :devportal:`assets: import-job-info <assets-import-job-info>`

        uuid (str):
            The UUID (unique identifier) for the job.

        Returns:
            :obj:`dict`:
                The job Resource record.

        Examples:
            >>> job = tio.assets.import_job_details(
            ...     '00000000-0000-0000-0000-000000000000')
            >>> pprint(job)
        '''
        return self._api.get(
            'import/asset-jobs/{}'.format(
                self._check('uuid', uuid, str)
            )).json()

    def move_assets(self, source, destination, targets):
        '''
        Moves assets from the specified network to another network.

        :devportal:`assets: move-assets <assets-bulk-move>`

        source (str):
            The UUID of the network currently associated with the assets.
        destination (str):
            The UUID of the network to associate with the specified assets.
        targets (list):
            The IPv4 addresses of the assets to move.

        Returns:
            :obj:`int`:
                Returns the number of moved assets.

        Examples:
            >>> asset = tio.assets.move_assets('00000000-0000-0000-0000-000000000000',
            ...         '10000000-0000-0000-0000-000000000001', ["127.0.0.1"])
            >>> pprint(asset)
        '''
        payload = {
            'source': self._check('source', source, 'uuid'),
            'destination': self._check('destination', destination, 'uuid'),
            'targets': ','.join(self._check('targets', targets, list))
        }

        return self._api.post('api/v2/assets/bulk-jobs/move-to-network', json=payload).json()

    def bulk_delete(self, *filters, hard_delete=None, filter_type=None):
        '''
        Deletes the specified assets.

        :devportal:`assets: bulk_delete <assets-bulk-delete>`

        Args:
             *filters (tuple):
                A defined filter tuple consisting of the name, operator, and
                value.  Example: ``('host.hostname', 'match', 'asset.com')``.
            filter_type (str, optional):
                If multiple filters are defined, the filter_type toggles the
                behavior as to how these filters are used.  Either all the
                filters have to match (``AND``) or any of the filters have to
                match (``OR``).  If not specified, the default behavior is to
                assume filter_type is ``AND``.
            hard_delete (bool, optional):
                Should the assets be completely removed with all related data?

        Returns:
            :obj:`dict`:
                Returns the number of deleted assets.

        Examples:
            >>> asset = tio.assets.bulk_delete(
            ...     ('host.hostname', 'match', 'asset.com'), filter_type='or')
            >>> pprint(asset)
        '''
        payload = dict()

        # run the rules through the filter parser...
        filter_type = self._check('filter_type', filter_type, str,
                                  choices=['and', 'or'], default='and', case='lower')
        parsed = self._parse_filters(
            filters, self._api.filters.workbench_asset_filters(), rtype='assets')['asset']

        if hard_delete:
            payload['hard_delete'] = self._check('hard_delete', hard_delete, bool)
        payload['query'] = {filter_type: parsed}

        return self._api.post('api/v2/assets/bulk-jobs/delete', json=payload).json()

    def update_acr(self, assets_uuid_list, reason, value, note=""):
        """
        Updates ACR for the provided asset UUID's with reason(s).

        Args:
            assets_uuid_list (list):
                Asset UUID's which are being updated.
            reason (list):
                List of reason(s).
            value (str):
                New ACR value for assets, ranging from 1 - 10.
            note (str):
                Additional note if any.

        Returns:
            :obj:`int`:
                Status code for the request.

        Examples:
            >>> tio.assets.update_acr(
            ... ['00000000-0000-0000-0000-000000000000', '00000000-0000-0000-0000-000000000001'],
            ... ['Other'], 1, 'some notes')
        """
        asset_uuids = []

        for asset_uuid in assets_uuid_list:
            asset_uuids.append({"id": asset_uuid})

        note = note + " - pyTenable"
        payload = [{"acr_score": int(value), "reason": reason, "asset": asset_uuids, "note": note}]

        return self._api.post('api/v2/assets/bulk-jobs/acr', json=payload).status_code
