'''
exports
=======
The following methods allow for interaction into the Tenable.io 
`exports <https://cloud.tenable.com/api#/resources/exports>`_ 
API endpoints.

Methods available on ``tio.exports``:

.. rst-class:: hide-signature
.. autoclass:: ExportsAPI

    .. automethod:: vulns
    .. automethod:: assets
'''
from .base import TIOEndpoint, APIResultsIterator
import time

class ExportsIterator(APIResultsIterator):
    '''
    The exports iterator handles the chunk status and retrieval management
    functions in order to provide a simplistic iterator that can be used with
    minimal effort in the calling application.
    '''
    _type = None
    _uuid = None
    _chunks = list()
    _processed = list()

    def _get_page(self):
        '''
        Get the next chunk
        '''
        def get_status():       
            # Query the API for the status of the export.
            status = self._api.get('{}/export/{}/status'.format(self._type, self._uuid)).json()

            # We need to get the list of chunks that we haven't completed yet and are
            # available for download.
            unfinished = [c for c in status['chunks_available'] if c not in self._processed]
            
            # Add the chunks_unfinished key with the unfinished list as the
            # associated value and then return the status to the caller.
            status['chunks_unfinished'] = unfinished

            # if there are no more chunks to process and the export status is 
            # set to finished, then we will break the iteration.
            if (status['status'] == 'FINISHED' 
                    and len(status['chunks_unfinished']) < 1):
                raise StopIteration()

            return status

        # If there are no chunks in our local queue, then we will need to query
        # the status API for more chunks to to work on.
        if len(self._chunks) < 1:
            status = get_status()

            # if the export is still processing, but there aren't any chunks for 
            # us to process yet, then we will wait here in a loop and call for 
            # status once a second until we get something else to work on.
            while len(status['chunks_unfinished']) < 1:
                time.sleep(1)   # wait 1 second
                status = get_status()

            # now that we have some chunks to work on, lets refresh the local
            # chunk cache and continue.
            self._chunks = status['chunks_unfinished']

        # now to take the first chunk off the local queue, move it to the 
        # processed list, and then set store the results to the page attribute.
        chunk_id = self._chunks[0]
        self._chunks.pop(0)
        self._processed.append(chunk_id)
        self.page = self._api.get('{}/export/{}/chunks/{}'.format(
            self._type, self._uuid, chunk_id)).json()

    def next(self):
        '''
        Ask for the next object
        '''
        # If we have worked through the current page of records then we should
        # query the next page of records.
        if self.page_count >= len(self.page):
            self.page_count = 0
            self._get_page()

        # Get the relevant record, increment the counters, and return the
        # record.
        item = self.page[self.page_count]
        self.count += 1
        self.page_count += 1
        return item


class ExportsAPI(TIOEndpoint):
    def vulns(self, **kw):
        '''
        Initiate an vulnerability export.

        `exports: vulns-request-export <https://cloud.tenable.com/api#/resources/exports/vulns-request-export>`_

        Args:
            cidr_range (str, optional):
                Restrict the export to only vulns assigned to assets within the
                CIDR range specified.
            first_found (int, optional):
                Specifies the earliest time for a vulnerability to have been
                discovered.  Format is a unix timestamp integer.
            last_fixed (int, optional):
                Specifies the earliest time that vulnerabilitis may have been
                fixed.  Format is a unix timestamp integer.
            last_found (int, optional):
                Specifies the earliest time that a vulnerability may have been
                last seen.  Format is a unix timestamp integer.
            num_assets (int, optional):
                Specifies the number of assets returned per-chunk.  If nothing is
                specified, it will default to 50 assets.
            plugin_family (list, optional):
                list of plugin families to restrict the export to.  values are
                interpreted with an insensitivity to case.
            severity (list, optional):
                list of severities to include as part of the export.  Supported
                values are `info`, `low`, `medium`, `high`, and `critical`.
            since (int, optional):
                Returned results will be bounded to only respond with objects
                that are new or updated between this specified value and current.
                If no since filter is specified, then the results will be unbounded
                and return all results.
            state (list, optional):
                list of object states to be returned.  Supported values are
                `open`, `reopened`, and `fixed`.
            tags (list, optional):
                List of tag key-value pairs that must be associated to the
                vulnerability data to be returned.  Key-value pairs are tuples
                if ``('key', 'value')`` and are case-sensitive.

        Returns:
            ExportIterator: an iterator to walk through the results.

        Examples:
            Export all of the vulnerability data:

            >>> vulns = tio.exports.vulns()
            >>> for vuln in vulns:
            ...     pprint(vuln)

            Export only the critical vulnerabilities:

            >>> for vuln in tio.exports.vulns(severity=['critical']):
            ...     pprint(vuln)
        '''
        payload = {'filters': dict()}

        payload['num_assets'] = str(self._check('num_assets', 
            kw['num_assets'] if 'num_assets' in kw else None, int, default=50))

        if 'severity' in kw and self._check('severity', kw['severity'], list, 
                choices=['info', 'low', 'medium', 'high', 'critical'], case='lower'):
            payload['filters']['severity'] = kw['severity']

        if 'state' in kw and self._check('state', kw['state'], list, 
                choices=['OPEN', 'REOPENED', 'FIXED'], case='upper'):
            payload['filters']['state'] = kw['state']

        if 'plugin_family' in kw and self._check(
                'plugin_family', kw['plugin_family'], list):
            payload['filters']['plugin_family'] = kw['plugin_family']

        if 'since' in kw and self._check('since', kw['since'], int):
            payload['filters']['since'] = kw['since']

        if 'cidr_range' in kw and self._check('cidr_range', kw['cidr_range'], str):
            payload['filters']['cidr_range'] = kw['cidr_range']

        if 'first_found' in kw and self._check('first_found', kw['first_found'], int):
            payload['filters']['first_found'] = kw['first_found']

        if 'last_found' in kw and self._check('last_found', kw['last_found'], int):
            payload['filters']['last_found'] = kw['last_found']

        if 'last_fixed' in kw and self._check('last_fixed', kw['last_fixed'], int):
            payload['filters']['last_fixed'] = kw['last_fixed']

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

        return ExportsIterator(self._api,
            _type='vulns',
            _uuid=self._api.post('vulns/export', json=payload).json()['export_uuid']
        )

    def assets(self, **kw):
        '''
        Export asset data from Tenable.io.

        `exports: assets-request-export <https://cloud.tenable.com/api#/resources/exports/assets-request-export>`_

        Args:
            chunk_size (int, optional):
                Specifies the number of objects returned per-chunk.  If nothing is
                specified, it will default to 50 objects.
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
            sources (list, optional):
                Returns assets that have the specified source.  If multiple
                sources are listed, then the results will be assets that have
                been observed by any of the sources listed.
            has_plugin_results (bool, optional):
                If True, returns only assets that have plugin results.  If False,
                returns only assets that do not have any plugin results.  Assets
                thats would not have plugin results would be assets created from
                a connector, or a discovery scan.

        Returns:
            ExportIterator: an iterator to walk through the results.

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
        payload = {'filters': dict()}
        payload['chunk_size'] = self._check('chunk_size', 
            kw['chunk_size'] if 'chunk_size' in kw else None,
            int, default=100)

        
        # Instead of a long and drawn-out series of if statements for all of
        # these integer filters, lets instead just loop through all of them
        # instead.  As they all have the same logic, there isn't any reason
        # not to shorten up the madness.
        for option in ['created_at', 'updated_at', 'terminated_at', 
                       'deleted_at', 'first_scan_time', 
                       'last_authenticated_scan_time', 'last_assessed']:
            if option in kw and self._check(option, kw[option], int):
                payload['filters'][option] = kw[option]

        # Lets to the same thing we did above for integer checks for the boolean
        # ones as well.
        for option in ['servicenow_sysid', 'has_plugin_results']:
            if option in kw:
                payload['filters'][option] = self._check(option, kw[option], bool)

        if 'sources' in kw and self._check('sources', kw['sources'], list):
            payload['filters']['sources'] = kw['sources']

        return ExportsIterator(self._api,
            _type='assets',
            _uuid=self._api.post('assets/export', json=payload).json()['export_uuid']
        )
