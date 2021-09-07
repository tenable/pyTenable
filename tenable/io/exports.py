'''
exports
=======

The following methods allow for interaction into the Tenable.io
:devportal:`exports <exports>` API endpoints.

Methods available on ``tio.exports``:

.. rst-class:: hide-signature
.. autoclass:: ExportsAPI

    .. automethod:: assets
    .. automethod:: vulns
    .. automethod:: compliance
'''
import time
import sys
from ipaddress import IPv4Network
from tenable.errors import TioExportsError, TioExportsTimeout
from tenable.io.base import TIOEndpoint, APIResultsIterator, UnexpectedValueError
try:
    from json.decoder import JSONDecodeError
except ImportError:
    JSONDecodeError = ValueError

class ExportsIterator(APIResultsIterator):
    '''
    The exports iterator handles the chunk status and retrieval management
    functions in order to provide a simplistic iterator that can be used with
    minimal effort in the calling application.

     Attributes:
        count (int): The current number of records that have been returned
        page (list):
            The current page of data being walked through.  pages will be
            cycled through as the iterator requests more information from the
            API.
        page_count (int): The number of record returned from the current page.
        total (int):
            The total number of records that exist for the current request.
    '''
    def __init__(self, api, **kw):
        self.type = None
        self.uuid = None
        self.chunk_id = None
        self.timeout = None
        self.chunks = list()
        self.processed = list()
        self._wait_for_complete = False
        APIResultsIterator.__init__(self, api, **kw)

    def _process_page(self, page_data):
        '''
        Processes a page of data
        '''
        self.page = page_data

    def _get_page(self):
        '''
        Get the next chunk
        '''
        def get_status():
            # Query the API for the status of the export.
            status = self._api.get('{}/export/{}/status'.format(self.type, self.uuid)).json()
            log_message = f'EXPORT {self.type} {self.uuid} is status {status.get("status")}'
            self._log.debug(log_message)

            # We need to get the list of chunks that we haven't completed yet and are
            # available for download.
            unfinished = [c for c in status.get('chunks_available', list()) if c not in self.processed]

            # Add the chunks_unfinished key with the unfinished list as the
            # associated value and then return the status to the caller.
            status['chunks_unfinished'] = unfinished

            # if there are no more chunks to process and the export status is
            # set to finished, then we will break the iteration.
            if (status['status'] == 'FINISHED'
              and len(status['chunks_unfinished']) < 1):
                raise StopIteration()

            if status['status'] != 'FINISHED' and self._wait_for_complete:
                status['chunks_unfinished'] = list()

            if status['status'] == 'ERROR':
                raise TioExportsError(self.type, self.uuid)

            if (status['status'] == 'QUEUED' and self.timeout
              and time.time() > self.timeout):
                self.cancel()
                raise TioExportsTimeout(self.type, self.uuid)

            return status

        # If there are no chunks in our local queue, then we will need to query
        # the status API for more chunks to to work on.
        if len(self.chunks) < 1:
            status = get_status()

            backoff_counter = 1
            # if the export is still processing, but there aren't any chunks for
            # us to process yet, then we will wait here in a loop and call for
            # status once a second until we get something else to work on.
            while len(status['chunks_unfinished']) < 1:
                backoff_counter += 1
                time.sleep(backoff_counter if backoff_counter < 30 else 30)
                status = get_status()

            # now that we have some chunks to work on, lets refresh the local
            # chunk cache and continue.
            self.chunks = status['chunks_unfinished']

        # now to take the first chunk off the local queue, move it to the
        # processed list, and then set store the results to the page attribute.
        self.chunk_id = self.chunks[0]
        self.chunks.pop(0)
        self.processed.append(self.chunk_id)

        # We will attempt to download a chunk of data and convert it into JSON.
        # If the conversion fails, then we will increment our own retry counter
        # and attempt to download the chunk again.  After 3 attempts, we will
        # assume that the chunk is dead and simply expire the chunk id.
        downloaded = False
        counter = 0
        while not downloaded and counter <= 3:
            try:
                self.page = self._api.get('{}/export/{}/chunks/{}'.format(
                    self.type, self.uuid, self.chunk_id)).json()
                downloaded = True
            except JSONDecodeError:
                log_message = 'Invalid Chunk {} on export {}'.format(
                               str(self.chunk_id), str(self.uuid))
                self._log.warning(log_message)
                self.page = list()
                counter += 1

        # If the chunk of data is empty, then we will call ourselves to get the
        # next page of data.  This allows us to properly handle empty chunks of
        # data.
        if len(self.page) < 1:
            log_message = 'Empty Chunk {} on Export {}'.format(
                           str(self.chunk_id), str(self.uuid))
            self._log.warning(log_message)
            self._get_page()

    def next(self):
        '''
        Ask for the next object
        '''
        # If we have worked through the current page of records then we should
        # query the next page of records.
        if self.page_count >= len(self.page):
            self._get_page()
            self.page_count = 0

        # Get the relevant record, increment the counters, and return the
        # record.
        item = self.page[self.page_count]
        self.count += 1
        self.page_count += 1
        return item

    def cancel(self):
        '''
        Cancels the export.
        '''
        self._api.get('{}/export/{}/cancel'.format(self.type, self.uuid)).json()


class ExportsAPI(TIOEndpoint):
    '''
    This class contains all methods related to exports
    '''
    def vulns(self, **kw):
        '''
        Initiate an vulnerability export.

        :devportal:`exports: vulns-request-export <exports-vulns-request-export>`

        Args:
            cidr_range (str, optional):
                Restrict the export to only vulns assigned to assets within the
                CIDR range specified.
            first_found (int, optional):
                Specifies the earliest time for a vulnerability to have been
                discovered.  Format is a unix timestamp integer.
            include_unlicensed (bool, optional):
                Informs the vuln export if it should include vulnerability data
                from assets that are unlicensed.  This is generally required
                when interacting with stale assets (>90 days).
            last_fixed (int, optional):
                Specifies the earliest time that vulnerabilities may have been
                fixed.  Format is a unix timestamp integer.
            last_found (int, optional):
                Specifies the earliest time that a vulnerability may have been
                last seen.  Format is a unix timestamp integer.
            num_assets (int, optional):
                Specifies the number of assets returned per-chunk.  If nothing is
                specified, it will default to 500 assets.
            plugin_family (list[str], optional):
                list of plugin families to restrict the export to.  Please note
                that this parameter's values are case sensitive.
            plugin_ids (list[int], optional):
                A list of plugin id's to explicitly export.
            severity (list[str], optional):
                list of severities to include as part of the export.  Supported
                values are `info`, `low`, `medium`, `high`, and `critical`.
            state (list[str], optional):
                list of object states to be returned.  Supported values are
                `open`, `reopened`, and `fixed`.
            tags (list[tuple], optional):
                List of tag key-value pairs that must be associated to the
                vulnerability data to be returned.  Key-value pairs are tuples
                ``('key', 'value')`` and are case-sensitive.
            timeout (int, optional):
                Number of seconds to wait before timing out the export.  If left
                unspecified the iterator will wait indefinitely for the export to
                complete.
            uuid (str, optional):
                To re-request an iterator based off of an existing export, pass
                the UUID of the export to bypass the initial request and instead
                use the UUID passed to build the export iterator.
            vpr (dict, optional):
                Restricts the results to the export to only vulnerabilities that
                match the VPR criteria specified.  As this supports a range of
                operations which are ``gte`` (for greater than or equal to), ``lte`` (for less than or equal to),
                ``eq`` (for equal to), ``neq`` (for not equal to),
                it's worth detailing a couple of examples.
                (``eq`` and ``neq`` takes the value in list):

                VPR Scores greater than or equal to 7.0:

                >>> vpr={'gte': 7}

                VPR Score less than 7, but not 5:

                >>> vpr={'lt': 7, 'neq': [5]}

                VPR Score equal to 5:

                >>> vpr={'eq': [5]}

                VPR Score less than or equal to 7:

                >>> vpr={'lte': 7.0}

            when_done (bool, optional):
                Wait to start working through the data until the export has finished
                processing.  If left unspecified the default behavior is to download
                chunks as they are available.

        Returns:
            :obj:`ExportIterator`:
                An iterator to walk through the results.

        Examples:
            Export all of the vulnerability data:

            >>> vulns = tio.exports.vulns()
            >>> for vuln in vulns:
            ...     pprint(vuln)

            Export only the critical vulnerabilities:

            >>> for vuln in tio.exports.vulns(severity=['critical']):
            ...     pprint(vuln)
        '''
        uuid = kw.get('uuid')
        payload = {'filters': dict()}

        # Instead of a long and drawn-out series of if statements for all of
        # these integer filters, lets instead just loop through all of them
        # instead.  As they all have the same logic, there isn't any reason
        # not to shorten up the madness.
        for option in ['since', 'first_found', 'last_found',
                       'last_fixed', 'first_scan_time',
                       'last_authenticated_scan_time', 'last_assessed']:
            self._api._log.debug(f'{option}={kw.get(option)}')
            if self._check(option, kw.get(option), int) is not None:
                payload['filters'][option] = kw[option]

        payload['num_assets'] = str(self._check('num_assets',
            kw['num_assets'] if 'num_assets' in kw else None, int, default=500))

        if self._check('include_unlicensed', kw.get('include_unlicensed'), bool):
            payload['include_unlicensed'] = kw.get('include_unlicensed')

        if self._check('plugin_ids', kw.get('plugin_ids'), list):
            payload['filters']['plugin_id'] = [int(p) for p in kw['plugin_ids']]
        if self._check('plugin_id', kw.get('plugin_id'), list):
            payload['filters']['plugin_id'] = [int(p) for p in kw['plugin_id']]

        if 'severity' in kw and self._check('severity', kw['severity'], list,
                choices=['info', 'low', 'medium', 'high', 'critical'], case='lower'):
            payload['filters']['severity'] = kw['severity']

        if 'state' in kw and self._check('state', kw['state'], list,
                choices=['OPEN', 'REOPENED', 'FIXED'], case='upper'):
            payload['filters']['state'] = kw['state']

        if 'plugin_family' in kw and self._check(
                'plugin_family', kw['plugin_family'], list):
            payload['filters']['plugin_family'] = kw['plugin_family']

        if 'cidr_range' in kw and self._check('cidr_range', kw['cidr_range'], str):
            cidr = kw['cidr_range']

            # if the python version is less than 3, then we will need to
            # recast it as a unicode string.
            if sys.version_info < (3, 0):
                cidr = unicode(cidr)

            # Validate the cidr_range attribute as an actual CIDR range.  If it
            # returns an error back to us, then we can safely assume that it's
            # not a valid CIDR and throw a UnexpectedValueError informing the
            # caller of the mistake.
            try:
                network = IPv4Network(cidr)
            except ValueError:
                raise UnexpectedValueError('{} is not a valid CIDR'.format(cidr))

            # Assuming everything has passed, then we will add the filter to the
            # filters dictionary.
            payload['filters']['cidr_range'] = str(network)

        if 'tags' in kw and self._check('tags', kw['tags'], list):
            # if any tags were specified, then we will iterate through the list
            # and handle each
            for tag in kw['tags']:
                # check to see if the tag is a tuple and also construct the
                # filter name.
                self._check('tags:tag', tag, tuple)
                name = 'tag.{}'.format(
                    self._check('tag:name', tag[0], str))

                # If the tag filter doesn't yet exist, then we need to create it
                # and associate an empty list to it.
                if name not in payload['filters']:
                    payload['filters'][name] = list()

                # add the tag value to the tag filter.
                payload['filters'][name].append(
                    self._check('tag:value', tag[1], str))

        if 'vpr' in kw and self._check('vpr', kw['vpr'], dict):
            payload['filters']['vpr_score'] = kw['vpr']

        if not uuid:
            uuid = self._api.post(
                'vulns/export', json=payload).json()['export_uuid']
            self._api._log.debug('Initiated vuln export {}'.format(uuid))

        return ExportsIterator(self._api,
            type='vulns',
            uuid=uuid,
            timeout=self._check('timeout', kw.get('timeout'), int),
            _wait_for_cmplete=self._check('when_done', kw.get('when_done'), bool, default=False)
        )

    def assets(self, **kw):
        '''
        Export asset data from Tenable.io.

        :devportal:`exports: assets-request-export <exports-assets-request-export>`

        Args:
            chunk_size (int, optional):
                Specifies the number of objects returned per-chunk.  If nothing is
                specified, it will default to 1000 objects.
            created_at (int, optional):
                Returns all assets created after the specified unix timestamp.
            updated_at (int, optional):
                Returns all assets updated after the specified unix timestamp.
            terminated_at (int, optional):
                Returns all assets terminated after the specified unix timestamp.
            deleted_at (int, optional):
                Returns all assets deleted after the specified unix timestamp.
            first_scan_time (int, optional):
                Returns all assets first scanned after the specified unix
                timestamp.
            is_deleted (bool, optional):
                Determines whether or not to return assets which have any value
                within the ``deleted_at`` attribute.  If left unspecified, the
                default is ``False``
            is_licensed (bool, optional):
                Determines whether or not to return unlicensed assets as part of
                the export.  If left unspecified, the default is ``True``,
                meaning only licensed assets will be returned.
            is_terminated (bool, optional):
                Determines whether or not to return assets that have any value
                within the ``terminated_at`` attribute.  If left unspecified,
                the default is ``False``.
            last_authenticated_scan_time (int, optional):
                Returns all assets that have completed an authenticated scan
                after the specified unix timestamp.
            last_assessed (int, optional):
                Returns all assets that have been assessed after the specified
                unix timestamp.
            servicenow_sysid (bool, optional):
                If set to True, will return only assets that have a ServiceNow
                Sys ID.  If set to False, then returns only assets that do not
                have a ServiceNow Sys ID.
            sources (list[str], optional):
                Returns assets that have the specified source.  If multiple
                sources are listed, then the results will be assets that have
                been observed by any of the sources listed.
            has_plugin_results (bool, optional):
                If True, returns only assets that have plugin results.  If False,
                returns only assets that do not have any plugin results.  Assets
                that's would not have plugin results would be assets created from
                a connector, or a discovery scan.
            tags (list[tuple], optional):
                List of tag key-value pairs that must be associated to the
                asset data to be returned.  Key-value pairs are tuples
                ``('key', 'value')`` and are case-sensitive.
            timeout (int, optional):
                Number of seconds to wait before timing out the export.  If left
                unspecified the iterator will wait indefinitely for the export to
                complete.
            uuid (str, optional):
                To re-request an iterator based off of an existing export, pass
                the UUID of the export to bypass the initial request and instead
                use the UUID passed to build the export iterator.
            when_done (bool, optional):
                Wait to start working through the data until the export has finished
                processing.  If left unspecified the default behavior is to download
                chunks as they are available.

        Returns:
            :obj:`ExportIterator`:
                An iterator to walk through the results.

        Examples:
            Export all of the asset data within Tenable.io:

            >>> assets = tio.exports.assets()
            >>> for asset in assets:
            ...     pprint(asset)

            Export only the assets updated in the last week:

            >>> import time
            >>> last_week = int(time.time()) - 604800
            >>> for asset in tio.exports.assets(updated_at=last_week):
            ...     pprint(asset)
        '''
        uuid = kw.get('uuid')
        payload = {'filters': dict()}
        payload['chunk_size'] = self._check('chunk_size',
            kw['chunk_size'] if 'chunk_size' in kw else None,
            int, default=1000)


        # Instead of a long and drawn-out series of if statements for all of
        # these integer filters, lets instead just loop through all of them
        # instead.  As they all have the same logic, there isn't any reason
        # not to shorten up the madness.
        for option in ['created_at', 'updated_at', 'terminated_at',
                       'deleted_at', 'first_scan_time',
                       'last_authenticated_scan_time', 'last_assessed']:
            if option in kw:
                payload['filters'][option] = self._check(option, kw[option], int)

        # Lets to the same thing we did above for integer checks for the boolean
        # ones as well.
        for option in ['servicenow_sysid', 'has_plugin_results',
                       'is_terminated', 'is_deleted', 'is_licensed']:
            if option in kw:
                payload['filters'][option] = self._check(option, kw[option], bool)

        if 'sources' in kw and self._check('sources', kw['sources'], list):
            payload['filters']['sources'] = kw['sources']

        if 'tags' in kw and self._check('tags', kw['tags'], list):
            # if any tags were specified, then we will iterate through the list
            # and handle each
            for tag in kw['tags']:
                # check to see if the tag is a tuple and also construct the
                # filter name.
                self._check('tags:tag', tag, tuple)
                name = 'tag.{}'.format(
                    self._check('tag:name', tag[0], str))

                # If the tag filter doesn't yet exist, then we need to create it
                # and associate an empty list to it.
                if name not in payload['filters']:
                    payload['filters'][name] = list()

                # add the tag value to the tag filter.
                payload['filters'][name].append(
                    self._check('tag:value', tag[1], str))

        if not uuid:
            uuid = self._api.post(
                'assets/export', json=payload).json()['export_uuid']
            self._api._log.debug('Initiated asset export {}'.format(uuid))
        return ExportsIterator(
            self._api,
            type='assets',
            uuid=uuid,
            timeout=self._check('timeout', kw.get('timeout'), int),
            _wait_for_cmplete=self._check('when_done', kw.get('when_done'), bool, default=False)
        )

    def compliance(self, **kw):
        '''
        Export all compliance data from Tenable.io.

        :devportal:`exports: export-compliance-data <io-exports-compliance-create>`

        Args:
            num_findings (int, optional):
                Specifies the number of compliance findings per exported chunk.
                The range is 50-5000
            asset (list[uuid], optional):
                A list of asset UUIDs for which you want to return compliance data.
                The list can contain a maximum of 200 asset UUIDs.
            last_seen (int, optional):
                Filters assets that were last seen by a scan between
                the specified date (in Unix time) and now.
            first_seen (int, optional):
                Filters assets that were first seen by a scan between
                the specified date (in Unix time) and now.

                Note: The first_seen filter cannot be used by itself.
                You must use last_seen and first_seen together or only last_seen.
            timeout (int, optional):
                Number of seconds to wait before timing out the export.  If left
                unspecified the iterator will wait indefinitely for the export to
                complete.
            uuid (str, optional):
                To re-request an iterator based off of an existing export, pass
                the UUID of the export to bypass the initial request and instead
                use the UUID passed to build the export iterator.
            when_done (bool, optional):
                Wait to start working through the data until the export has finished
                processing.  If left unspecified the default behavior is to download
                chunks as they are available.

        Returns:
            :obj:`ExportIterator`:
                An iterator to walk through the results.

        Examples:
            Export all of the compliance data within Tenable.io:

            >>> compliance_data = tio.exports.compliance()
            >>> for compliance in compliance_data:
            ...     pprint(compliance)

            Export only the compliance data between last week and now:

            >>> import time
            >>> last_week = int(time.time()) - 604800
            >>> for compliance in tio.exports.compliance(last_seen=last_week):
            ...     pprint(compliance)

        '''
        # initialize payload
        payload=dict()
        uuid = kw.get('uuid')

        # set the number of compliance findings per exported chunk
        if 'num_findings' in kw and self._check('num_findings', kw['num_findings'], int,
                                                choices=list(range(50, 5001))):
            payload['num_findings'] = kw['num_findings']

        # set list of asset UUIDs for which you want to return compliance data
        # the count of asset UUIDs can be maximum of 200 UUID values.
        if 'asset' in kw and self._check('asset', kw['asset'], list):
            if len(kw['asset']) <= 200:
                payload['asset'] = [
                    self._check('asset_value', asset, 'uuid') for asset in kw['asset']]
            else:
                raise UnexpectedValueError("The list can contain a maximum of 200 asset UUIDs")

        # set last seen and first seen filters
        # we are checking first seen filter only if last seen is available
        if 'last_seen' in kw:
            payload['filters'] = dict()
            payload['filters']['last_seen'] = self._check('last_seen', kw['last_seen'], int)

            if 'first_seen' in kw:
                payload['filters']['first_seen'] = self._check('first_seen', kw['first_seen'], int)

        if not uuid:
            uuid = self._api.post(
                'compliance/export', json=payload).json()['export_uuid']
            self._api._log.debug('Initiated compliance export {}'.format(uuid))

        return ExportsIterator(
            self._api,
            type='compliance',
            uuid=uuid,
            timeout=self._check('timeout', kw.get('timeout'), int),
            _wait_for_cmplete=self._check('when_done', kw.get('when_done'), bool, default=False)
        )
