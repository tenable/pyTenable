'''
assets
======

The following methods allow for interaction into the Tenable.io
:devportal:`assets <assets>` API endpoints.

Methods available on ``tio.assets``:

.. rst-class:: hide-signature
.. autoclass:: AssetsAPI

    .. automethod:: asset_import
    .. automethod:: delete
    .. automethod:: details
    .. automethod:: import_job_details
    .. automethod:: list
    .. automethod:: list_import_jobs
    .. automethod:: tags
'''
from .base import TIOEndpoint

class AssetsAPI(TIOEndpoint):
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
            ...     'add', ['00000000-0000-0000-0000-000000000000'], ['00000000-0000-0000-0000-000000000000'])
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
        Imports asset information into Tenable.io from an external source.

        :devportal:`assets: import <assets-import>`

        Imports a list of asset definition dictionaries.  Each asset record must
        contain at least one of the following attributes: ``fqdn``, ``ipv4``,
        ``netbios_name``, ``mac_address``.  Each record may also contain
        additional properties.

        Args:
            *assets (list):
                The list of asset dictionaries
            source (str):
                An identifier to be used to upload the assets.

        Returns:
            :obj:`str`:
                The job UUID.

        Examples:
            >>> tio.assets.asset_import('example_source', {
            ...     'fqdn': ['example.py.test'],
            ...     'ipv4': ['192.168.254.1'],
            ...     'netbios_name': 'example',
            ...     'mac_address': ['00:00:00:00:00:00']
            ... })
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

