'''
assets
======

The following methods allow for interaction into the Tenable.io 
`assets <https://cloud.tenable.com/api#/resources/assets>`_ 
API endpoints.

Methods available on ``tio.assets``:

.. rst-class:: hide-signature
.. autoclass:: AssetsAPI

    .. automethod:: asset_import
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

        `assets: list-assets <https://cloud.tenable.com/api#/resources/assets/list-assets>`_

        Returns:
            list: List of asset records.

        Examples:
            >>> for asset in tio.assets.list():
            ...     pprint(asset)
        '''
        return self._api.get('assets').json()['assets']

    def details(self, uuid):
        '''
        Retrieves the details about a specific asset.

        `assets: asset-info <https://cloud.tenable.com/api#/resources/assets/asset-info>`_

        Args:
            uuid (str):
                The UUID (unique identifier) for the asset.

        Returns:
            dict: Asset resource definition.

        Examples:
            >>> asset = tio.assets.details('00000000-0000-0000-0000-000000000000')
        '''
        return self._api.get(
            'assets/{}'.format(
                self._check('uuid', uuid, str)
            )).json()

    def tags(self, uuid):
        '''
        Retrieves the details about a specific asset.

        `tags: asset-tags <https://developer.tenable.com/tenableio/reference#tags-list-asset-tags-1>`_

        Args:
            uuid (str):
                The UUID (unique identifier) for the asset.

        Returns:
            dict: Asset resource definition.

        Examples:
            >>> asset = tio.assets.tags('00000000-0000-0000-0000-000000000000')
        '''
        return self._api.get(
            'tags/assets/{}/assignments'.format(
                self._check('uuid', uuid, 'uuid')
            )).json()

    def asset_import(self, source, *assets):
        '''
        Imports asset information into Tenable.io from an external source.

        `assets: import <https://cloud.tenable.com/api#/resources/assets/import>`_

        Imports a list of asset definition dictionaries.  Each asset record must
        contain at least one of the following attributes: ``fqdn``, ``ipv4``,
        ``netbios_name``, ``mac_address``.  Each record may also contain
        additional properties as mentioned in the `asset resource`_
        documentation.

        Args:
            *assets (list):
                The list of asset dictionaries
            source (str):
                An identifier to be used to upload the assets.

        Returns:
            str: The job UUID.

        Examples:
            >>> tio.assets.asset_import('example_source', {
            ...     'fqdn': ['example.py.test'], 
            ...     'ipv4': ['192.168.254.1'], 
            ...     'netbios_name': 'example', 
            ...     'mac_address': ['00:00:00:00:00:00']
            ... })

        .. _asset resource:
            https://cloud.tenable.com/api#/resources/assets
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

        `assets: list-import-jobs <https://cloud.tenable.com/api#/resources/assets/list-import-jobs>`_

        Returns:
            list: list of job records.

        Examples:
            >>> for job in tio.assets.list_import_jobs():
            ...     pprint(job)
        '''
        return self._api.get('import/asset-jobs').json()['asset_import_jobs']

    def import_job_details(self, uuid):
        '''
        Returns the details about a specific asset import job.

        `assets: import-job-info <https://cloud.tenable.com/api#/resources/assets/import-job-info>`_

        uuid (str):
            The UUID (unique identifier) for the job.

        Returns:
            dict: The job Resource record.

        Examples:
            >>> job = tio.assets.import_job_details('00000000-0000-0000-0000-000000000000')
            >>> pprint(job)
        '''
        return self._api.get(
            'import/asset-jobs/{}'.format(
                self._check('uuid', uuid, str)
            )).json()

