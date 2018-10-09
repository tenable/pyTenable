from tenable.tenable_io.base import TIOEndpoint

class AssetsAPI(TIOEndpoint):
    def list(self):
        '''
        `assets: list-assets <https://cloud.tenable.com/api#/resources/assets/list-assets>`_

        Returns:
            list: List of asset records.
        '''
        return self._api.get('assets').json()['assets']

    def info(self, uuid):
        '''
        `assets: asset-info <https://cloud.tenable.com/api#/resources/assets/asset-info>`_

        Args:
            uuid (str):
                The UUID (unique identifier) for the asset.

        Returns:
            dict: Asset resource definition.
        '''
        return self._api.get(
            'assets/{}'.format(
                self._check('uuid', uuid, str)
            )).json()

    def asset_import(self, definitions, source):
        '''
        `assets: import <https://cloud.tenable.com/api#/resources/assets/import>`_

        Imports a list of asset definition dictionaries.  Each asset record must
        contain at least one of the following attributes: ``fqdn``, ``ipv4``,
        ``netbios_name``, ``mac_address``.  Each record may also contain
        additional properties as mentioned in the `asset resource`_
        documentation.

        Args:
            definitions (list):
                The list of asset dictionaries
            source (str):
                An identifier to be used to upload the assets.

        Returns:
            str: The job UUID.

        .. _asset resource:
            https://cloud.tenable.com/api#/resources/assets
        '''
        # We will likely want to perform some more stringent checking of the
        # asset resources that are being defined, however a simple type check
        # should suffice for now.
        return self._api.post(
            'import/assets', json={
                'assets': self._check('definitions', definitions, list),
                'source': self._check('source', source, str)
            }).json()['asset_import_job_uuid']

    def import_jobs(self):
        '''
        `assets: list-import-jobs <https://cloud.tenable.com/api#/resources/assets/list-import-jobs>`_

        Returns:
            list: list of job records.
        '''
        return self._api.get('import/asset-jobs').json()['asset_import_jobs']

    def import_job_info(self, uuid):
        '''
        `assets: import-job-info <https://cloud.tenable.com/api#/resources/assets/import-job-info>`_

        uuid (str):
            The UUID (unique identifier) for the job.

        Returns:
            dict: The job Resource record.
        '''
        return self._api.get(
            'import/asset-jobs/{}'.format(
                self._check('uuid', uuid, str)
            )).json()

