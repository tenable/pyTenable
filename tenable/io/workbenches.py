'''
Workbenches
===========

The following methods allow for interaction into the Tenable Vulnerability Management
:devportal:`workbenches <workbenches>` API endpoints.

.. note::

    Workbenches API endpoints have an upper bound on the amount of data that
    they will return, so for larger result sets, it may make more sense to use
    the exports API.

Methods available on ``tio.workbenches``:

.. rst-class:: hide-signature
.. autoclass:: WorkbenchesAPI
    :members:
'''
from io import BytesIO
from .base import TIOEndpoint
from tenable.errors import UnexpectedValueError


class WorkbenchesAPI(TIOEndpoint):
    def _workbench_query(self, filters, kw, filterdefs):
        '''
        '''
        # Initiate the query dictionary with the filters parser.
        query = self._parse_filters(filters, filterdefs)

        if 'age' in kw:
            # The age parameter is converted into the "date_range" parameter
            # for the endpoint.  The name was simply changed to be more
            # understandable.
            query['date_range'] = self._check('age', kw['age'], int)

        if 'filter_type' in kw:
            # The scans & workbenches endpoints use a serialized JSON format for
            # query parameters, hence the x.y notation.
            query['filter.search_type'] = self._check(
                'filter_type', kw['filter_type'], str, choices=['and', 'or'])

        # Return the query to the caller
        return query


    def assets(self, *filters, **kw):
        '''
        The assets workbench allows for filtering and interactively querying the
        asset data stored within Tenable Vulnerability Management.  There are a wide variety of
        filtering options available to find specific pieces of data.

        :devportal:`workbenches: assets <workbenches-assets>`

        Args:
            age (int, optional):
                The maximum age of the data to be returned.
            *filters (list, optional):
                 A list of tuples detailing the filters that wish to be applied
                the response data.  Each tuple is constructed as
                ('filter', 'operator', 'value') and would look like the
                following example: `('host.hostname', 'match', 'asset.com')`.
                For a complete list of the available filters and options, please
                refer to the API documentation linked above.
            filter_type (str, optional):
                Are the filters exclusive (this AND this AND this) or inclusive
                (this OR this OR this).  Valid values are `and` and `or`.  The
                default setting is `and`.
            all_fields (bool, optional):
                Should all of the available fields be returned for each returned
                asset, or just the default fields represented in the UI.  The
                default is set to `True` which will return the same level of
                detail as the workbenches: asset-info endpoint.

        Returns:
            :obj:`list`:
                List of asset resource records.

        Examples:
            Query for all of the asset information:

            >>> for asset in tio.workbenches.assets():
            ...     pprint(asset)

            Query for just the windows assets:

            >>> for asset in tio.workbenches.assets(
            ...     ('operating_system', 'match', 'Windows')):
            ...     pprint(asset)
        '''
        # Call the query builder to handle construction
        query = self._workbench_query(filters, kw,
            self._api.filters.workbench_asset_filters())

        # If all_fields is set to true or is unspecified, then we will set the
        # all_fields parameter to "full".
        if 'all_fields' in kw:
            if self._check('all_fields', kw['all_fields'], bool):
                query['all_fields'] = 'full'
        else:
            query['all_fields'] = 'full'

        return self._api.get('workbenches/assets', params=query).json()['assets']

    def asset_activity(self, uuid):
        '''
        Query for the asset activity (when was the asset was seen, were there
        changes, etc.).

        :devportal:`workbenches: asset-activity <workbenches-assets-activity>`

        Args:
            uuid (str): The asset unique identifier.

        Returns:
            :obj:`list`:
                The activity list of the asset specified.

        Examples:
            >>> asset_id = '00000000-0000-0000-0000-000000000000'
            >>> for entry in tio.workbenches.asset_activity(asset_id):
            ...     pprint(entry)
        '''
        return self._api.get('workbenches/assets/{}/activity'.format(
            self._check('uuid', uuid, 'uuid'))).json()['activity']

    def asset_info(self, uuid, all_fields=True):
        '''
        Query for the information for a specific asset within the asset
        workbench.

        :devportal:`workbenches: asset-info </workbenches-asset-info>`

        Args:
            id (str): The unique identifier (UUID) of the asset.
            all_fields (bool, optional):
                If all_fields is set to true (the default state), then an
                expanded dataset is returned as defined by the API
                documentation (linked above).

        Returns:
            :obj:`dict`:
                The resource record for the asset.

        Examples:
            >>> asset = tio.workbenches.asset_info('00000000-0000-0000-0000-000000000000')
        '''
        query = {'all_fields': 'full'}

        if not self._check('all_fields', all_fields, bool):
            # if the caller chooses to get a reduced list of attributes for the
            # response, then we simply want to remove the key from from the
            # query dictionary.  The documentation states that the existence of
            # the parameter is what triggers the expanded dataset, which we
            # are returning by default.
            del(query['all_fields'])

        return self._api.get('workbenches/assets/{}/info'.format(
            self._check('uuid', uuid, 'uuid')), params=query).json()['info']

    def asset_vulns(self, uuid, *filters, **kw):
        '''
        Return the vulnerabilities for a specific asset.

        :devportal:`workbenches: asset-vulnerabilities <workbenches-asset-vulnerabilities>`

        Args:
            uuid (str):
                The unique identifier of the asset to query.
            age (int, optional):
                The maximum age of the data to be returned.
            *filters (list, optional):
                 A list of tuples detailing the filters that wish to be applied
                the response data.  Each tuple is constructed as
                ('filter', 'operator', 'value') and would look like the
                following example: `('host.hostname', 'match', 'asset.com')`.
                For a complete list of the available filters and options, please
                refer to the API documentation linked above.
            filter_type (str, optional):
                Are the filters exclusive (this AND this AND this) or inclusive
                (this OR this OR this).  Valid values are `and` and `or`.  The
                default setting is `and`.

        Returns:
            :obj:`list`:
                List of vulnerability resource records.

        Examples:
            >>> asset_id = '00000000-0000-0000-0000-000000000000'
            >>> for vuln in tio.workbenches.asset_vulns(asset_id):
            ...     pprint(vuln)
        '''
        # Call the query builder to handle construction
        query = self._workbench_query(filters, kw,
            self._api.filters.workbench_vuln_filters())

        return self._api.get(
            'workbenches/assets/{}/vulnerabilities'.format(
                self._check('uuid', uuid, 'uuid')), params=query).json()['vulnerabilities']

    def asset_vuln_info(self, uuid, plugin_id, *filters, **kw):
        '''
        Retrieves the vulnerability information for a specific plugin on a
        specific asset within Tenable Vulnerability Management.

        :devportal:`workbenches: asset-vulnerability-info <workbenches-asset-vulnerability-info>`

        Args:
            uuid (str):
                The unique identifier of the asset to query.
            plugin_id (int):
                The unique identifier of the plugin.
            age (int, optional):
                The maximum age of the data to be returned.
            *filters (list, optional):
                 A list of tuples detailing the filters that wish to be applied
                the response data.  Each tuple is constructed as
                ('filter', 'operator', 'value') and would look like the
                following example: `('host.hostname', 'match', 'asset.com')`.
                For a complete list of the available filters and options, please
                refer to the API documentation linked above.
            filter_type (str, optional):
                Are the filters exclusive (this AND this AND this) or inclusive
                (this OR this OR this).  Valid values are `and` and `or`.  The
                default setting is `and`.

        Returns:
            :obj:`list`:
                List of vulnerability resource records.

        Examples:
            >>> asset_id = '00000000-0000-0000-0000-000000000000'
            >>> vuln = tio.workbenches.asset_vuln_info(asset_id, 19506)
            >>> pprint(vuln)
        '''
        # Call the query builder to handle construction
        query = self._workbench_query(filters, kw,
            self._api.filters.workbench_vuln_filters())

        return self._api.get(
            'workbenches/assets/{}/vulnerabilities/{}/info'.format(
                self._check('uuid', uuid, 'uuid'),
                self._check('plugin_id', plugin_id, int)), params=query).json()['info']

    def asset_vuln_output(self, uuid, plugin_id, *filters, **kw):
        '''
        Retrieves the vulnerability output for a specific vulnerability on a
        specific asset within Tenable Vulnerability Management.

        :devportal:`workbenches: asset-vulnerability-output <workbenches-asset-vulnerability-output>`

        Args:
            uuid (str):
                The unique identifier of the asset to query.
            plugin_id (int):
                The unique identifier of the plugin.
            age (int, optional):
                The maximum age of the data to be returned.
            *filters (list, optional):
                 A list of tuples detailing the filters that wish to be applied
                the response data.  Each tuple is constructed as
                ('filter', 'operator', 'value') and would look like the
                following example: `('host.hostname', 'match', 'asset.com')`.
                For a complete list of the available filters and options, please
                refer to the API documentation linked above.
            filter_type (str, optional):
                Are the filters exclusive (this AND this AND this) or inclusive
                (this OR this OR this).  Valid values are `and` and `or`.  The
                default setting is `and`.

        Returns:
            :obj:`list`:
                List of vulnerability resource records.

        Examples:
            >>> asset_id = '00000000-0000-0000-0000-000000000000'
            >>> output = tio.workbenches.asset_vuln_output(asset_id, 19506)
            >>> pprint(output)
        '''
        # Call the query builder to handle construction
        query = self._workbench_query(filters, kw,
            self._api.filters.workbench_vuln_filters())

        return self._api.get(
            'workbenches/assets/{}/vulnerabilities/{}/outputs'.format(
                self._check('uuid', uuid, 'uuid'),
                self._check('plugin_id', plugin_id, int)), params=query).json()['outputs']

    def asset_delete(self, asset_uuid):
        '''
        Deletes the asset.

        :devportal:`workbenches: asset-delete <workbenches-asset-delete>`

        Args:
            asset_uuid (str): The unique identifier for the asset.

        Returns:
            :obj:`None`:

        Examples:
            >>> asset_id = '00000000-0000-0000-0000-000000000000'
            >>> tio.workbenches.asset_delete(asset_id)
        '''
        self._api.delete('workbenches/assets/{}'.format(
            self._check('asset_uuid', asset_uuid, 'uuid')))

    def vuln_assets(self, *filters, **kw):
        '''
        Retrieve assets based on the vulnerability data.

        :devportal:`workbenches: assets-vulnerabilities <workbenches-assets-vulnerabilities>`

        Args:
            age (int, optional):
                The maximum age of the data to be returned.
            *filters (list, optional):
                 A list of tuples detailing the filters that wish to be applied
                the response data.  Each tuple is constructed as
                ('filter', 'operator', 'value') and would look like the
                following example: `('host.hostname', 'match', 'asset.com')`.
                For a complete list of the available filters and options, please
                refer to the API documentation linked above.
            filter_type (str, optional):
                Are the filters exclusive (this AND this AND this) or inclusive
                (this OR this OR this).  Valid values are `and` and `or`.  The
                default setting is `and`.

        Returns:
            :obj:`list`:
                List of asset resource records.

        Examples:
            >>> for asset in tio.workbenches.vuln_assets():
            ...     pprint(asset)
        '''
        # Call the query builder to handle construction
        query = self._workbench_query(filters, kw,
            self._api.filters.workbench_vuln_filters())

        return self._api.get(
            'workbenches/assets/vulnerabilities', params=query).json()['assets']

    def export(self, *filters, **kw):
        '''
        Export data from the vulnerability workbench.  These exports can be in
        a number of different formats, however the defaults are set to export
        a Nessusv2 report.

        :devportal:`workbenches: export <workbenches-export-request>`

        Args:
            *filters (tuple, optional):
                A list of tuples detailing the filters that wish to be applied
                the response data.  Each tuple is constructed as
                ('filter', 'operator', 'value') and would look like the
                following example: `('plugin.id', 'eq', '19506')`.  For a
                complete list of the available filters and options, please
                refer to the API documentation linked above.
            asset_uuid (uuid, optional):
                Restrict the output to the asset identifier specified.
            plugin_id (int, optional):
                Restrict the output to the plugin identifier specified.
            format (str, optional):
                What format would you like the resulting data to be in.  The
                default would be nessus output.  Available options are `nessus`,
                `csv`, `html`, `pdf`.  Default is 'nessus'
            chapters (list, optional):
                A list of the chapters to write for the report.  The chapters
                list is only required for PDF, CSV, and HTML exports.  Available
                chapters are ``vuln_hosts_summary``, ``vuln_by_host``,
                ``vuln_by_plugin``, and ``vuln_by_asset``. List order will denote
                output order.  In the case of CSV reports, only
                ``vuln_by_asset`` and ``vuln_by_plugin`` are available and only
                a singular chapter can be specified.
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
            :obj:`FileObject`:
                The file-like object of the requested export.

        Examples:
            >>> with open('example.nessus', 'wb') as exportobj:
            ...     tio.workbenches.export(fobj=exportobj)
        '''

        # initiate the payload and parameters dictionaries.
        params = self._parse_filters(filters,
            self._api.filters.workbench_vuln_filters())
        params['report'] = 'vulnerabilities'
        params['chapter'] = 'vuln_by_asset'
        params['format'] = 'nessus'

        if 'plugin_id' in kw:
            params['plugin_id'] = self._check(
                'plugin_id', kw['plugin_id'], int)

        if 'asset_uuid' in kw:
            params['asset_id'] = self._check(
                'asset_uuid', kw['asset_uuid'], 'uuid')

        if 'format' in kw:
            params['format'] = self._check('format', kw['format'], str,
                default='nessus',
                choices=[
                'nessus', 'csv', 'html', 'pdf'
            ])
            if kw['format'] not in ['nessus',]:
                # The chapters are sent to us in a list, and we need to collapse
                # that down to a comma-delimited string.  Note that if the nessus
                # format is specified, we must use the vuln_by_asset report, so
                # will ignore the chapters attribute in those cases.
                if 'chapters' not in kw:
                    raise UnexpectedValueError('no chapters were specified')
                else:
                    params['chapter'] = ';'.join(
                        self._check('chapters', kw['chapters'], list,
                            default='vuln_by_asset',
                            choices=[
                                'diff',
                                'exec_summary',
                                'vuln_by_host',
                                'vuln_by_plugin',
                                'vuln_hosts_summary',
                                'vuln_by_asset',
                        ]))

        if 'filter_type' in kw:
            params['filter.search_type'] = self._check(
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
        fid = self._api.get('workbenches/export',
            params=params).json()['file']
        self._api._log.debug('Initiated workbench export {}'.format(fid))

        # Next we will wait for the state of the export request to become
        # ready.  We will query the API every half a second until we get the
        # response we're looking for.
        self._wait_for_download(
            'workbenches/export/{}/status'.format(fid),
            'workbenches', 'export', fid)

        # Now that the status has reported back as "ready", we can actually
        # download the file.
        resp = self._api.get('workbenches/export/{}/download'.format(
            fid), stream=True)

        # Lets stream the file into the file-like object...
        for chunk in resp.iter_content(chunk_size=1024):
            if chunk:
                fobj.write(chunk)
        fobj.seek(0)
        resp.close()
        return fobj

    def vulns(self, *filters, **kw):
        '''
        The vulnerability workbench allows for filtering and interactively
        querying the vulnerability data stored within Tenable Vulnerability Management.  There are a
        wide variety of filtering options available to find specific pieces
        of data.

        :devportal:`workbenches: vulnerability-info <workbenches-vulnerability-info>`

        Args:
            age (int, optional):
                The maximum age of the data to be returned.
            authenticated (bool, optional):
                If set to true will only return authenticated vulnerabilities.
            exploitable (bool, optional):
                If set to true will only return exploitable vulnerabilities.
            *filters (list, optional):
                 A list of tuples detailing the filters that wish to be applied
                the response data.  Each tuple is constructed as
                ('filter', 'operator', 'value') and would look like the
                following example: `('host.hostname', 'match', 'asset.com')`.
                For a complete list of the available filters and options, please
                refer to the API documentation linked above.
            filter_type (str, optional):
                Are the filters exclusive (this AND this AND this) or inclusive
                (this OR this OR this).  Valid values are `and` and `or`.  The
                default setting is `and`.
            resolvable (bool, optional):
                If set to true will only return vulnerabilities with a
                remediation path.
            severity (str, optional):
                Only return results of a specific severity
                (critical, high, medium, or low).

        Returns:
            :obj:`dict`:
                Vulnerability info resource
        '''
        # Call the query builder to handle construction
        query = self._workbench_query(filters, kw,
            self._api.filters.workbench_vuln_filters())

        if 'authenticated' in kw and self._check('authenticated', kw['authenticated'], bool):
            query['authenticated'] = True
        if 'exploitable' in kw and self._check('exploitable', kw['exploitable'], bool):
            query['exploitable'] = True
        if 'resolvable' in kw and self._check('resolvable', kw['resolvable'], bool):
            query['resolvable'] = True
        if 'severity' in kw and self._check('severity', kw['severity'], str,
                choices=['critical', 'high', 'medium', 'low']):
            query['severity'] = kw['severity']

        return self._api.get(
            'workbenches/vulnerabilities', params=query).json()['vulnerabilities']

    def vuln_info(self, plugin_id, *filters, **kw):
        '''
        Retrieve the vulnerability information for a specific vulnerability.

        :devportal:`workbenches: vulnerability-info <workbenches-vulnerability-info>`

        Args:
            age (int, optional):
                The maximum age of the data to be returned.
            *filters (list, optional):
                 A list of tuples detailing the filters that wish to be applied
                the response data.  Each tuple is constructed as
                ('filter', 'operator', 'value') and would look like the
                following example: `('host.hostname', 'match', 'asset.com')`.
                For a complete list of the available filters and options, please
                refer to the API documentation linked above.
            filter_type (str, optional):
                Are the filters exclusive (this AND this AND this) or inclusive
                (this OR this OR this).  Valid values are `and` and `or`.  The
                default setting is `and`.

        Returns:
            :obj:`dict`:
                Vulnerability info resource

        Examples:
            >>> info = tio.workbenches.vuln_info(19506)
            >>> pprint(info)
        '''
        # Call the query builder to handle construction
        query = self._workbench_query(filters, kw,
            self._api.filters.workbench_vuln_filters())

        return self._api.get(
            'workbenches/vulnerabilities/{}/info'.format(
                self._check('plugin_id', plugin_id, int)), params=query).json()['info']

    def vuln_outputs(self, plugin_id, *filters, **kw):
        '''
        Retrieve the vulnerability output for a given vulnerability.

        :devportal:`workbenches: vulnerability-output <workbenches-vulnerability-output>`

        Args:
            age (int, optional):
                The maximum age of the data to be returned.
            *filters (list, optional):
                 A list of tuples detailing the filters that wish to be applied
                the response data.  Each tuple is constructed as
                ('filter', 'operator', 'value') and would look like the
                following example: `('host.hostname', 'match', 'asset.com')`.
                For a complete list of the available filters and options, please
                refer to the API documentation linked above.
            filter_type (str, optional):
                Are the filters exclusive (this AND this AND this) or inclusive
                (this OR this OR this).  Valid values are `and` and `or`.  The
                default setting is `and`.

        Returns:
            :obj:`dict`:
                Vulnerability outputs resource

        Examples:
            >>> outputs = tio.workbenches.vuln_outputs(19506)
            >>> pprint(outputs)
        '''
        # Call the query builder to handle construction
        query = self._workbench_query(filters, kw,
            self._api.filters.workbench_vuln_filters())

        return self._api.get(
            'workbenches/vulnerabilities/{}/outputs'.format(
                self._check('plugin_id', plugin_id, int)), params=query).json()['outputs']
