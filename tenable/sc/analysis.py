from .base import SCEndpoint, SCResultsIterator
from tenable.utils import dict_merge


class AnalysisResultsIterator(SCResultsIterator):
    def _get_page(self):
        '''
        Retreives the next page of results when the current page has been
        exhausted.
        '''
        # First we need to see if there is a page limit and if there is, have
        # we run into that limit.  If we have, then return a StopIteration
        # exception.
        if self._pages_total and self._pages_requested >= self._pages_total:
            raise StopIteration()

        # Now we need to do is construct the query with the current offset 
        # and limits
        query = self._query
        query['query']['startOffset'] = self._offset
        query['query']['endOffset'] = self._limit + self._offset

        # Lets actually call the API for the data at this point.
        resp = self._api.post('analysis', json=query).json()

        # Now that we have the response, lets reset any counters we need to, 
        # and increment things like the page counter, offset, etc.
        self.page_count = 0
        self._pages_requested += 1
        self._offset += self._limit
        self._raw = resp
        self.page = resp['response']['results']
        self.total = int(resp['response']['totalRecords'])


class AnalysisAPI(SCEndpoint):
    '''
    '''


    def _analysis(self, *filters, **kw):
        '''
        The base wrapper function handling the calls to the analysis API 
        endpoint.  As this singular endpopint is used as the common API for all
        data export, much of the common handling can be centrally handled and
        only the unique elements for a given sub-type is handled by the
        individual methods.
        '''
        offset = 0
        limit = 200

        if 'query' not in kw:
            kw['query'] = {
                'tool': kw['tool'],
                'type': kw['analysis_type'],
                'filters': [{
                    'filterName': f[0],
                    'operator': f[1],
                    'value': f[2],
                    'type': kw['type'],
                } for f in filters]
            }

        payload = kw['payload'] if 'payload' in kw else dict()
        payload['query'] = kw['query']

        if 'sort_field' in kw:
            payload['sortField'] = self._check(
                'sort_field', kw['sort_field'], str)

        if 'sort_direction' in kw:
            payload['sortDir'] = self._check(
                'sort_direction', kw['sort_direction'], str, 
                choices=['ASC', 'DESC'], case='upper')

        if 'offset' in kw:
            skip = self._check('offset', kw['offset'], int, default=0)

        if 'limit' in kw:
            limit = self._check('limit', kw['limit'], int, default=200)

        return AnalysisResultsIterator(self._api,
            _offset=offset,
            _limit=limit,
            _query=payload
        )

    def vulns(self, *filters, **kw):
        '''
        Args:
            filters (tuple, optional):
                The analysis module provides a more compact way to write filters
                to the analysis endpoint.  The purpose here is to aid in more
                readable code and reduce the amount of boilerplate that must be
                written to support a filtered call to analysis.  The format is
                simply a list of tuples.  Each tuple is broken down into
                (field, operator, value).
            pages (int, optional):
                The number of pages to query.  Default is all.
            limit (int, optional):
                How many entries should be in each page?  Default is 200.
            offset (int, optional):
                How many entries to skip before processing.  Default is 0.
            source (str, optional):
                The data source location.  Allowed sources are ``cumulative`` 
                and ``patched``.  Defaults to ``cumulative``.
            scan_id (int, optional):
                If a scan id is specified, then the results fetched will be from
                the scan specified and not from the cumulative result set.
            sort_field (str, optional):
                The field to sort the results on.
            sort_direction (str, optional):
                The direction in which to sort the results.  Valid settings are
                ``asc`` and ``desc``.  The default is ``asc``.
            tool (str, optional):
                The analysis tool for formatting and returning a specific view
                into the information.  If no tool is specified, the default will
                be ``vulndetails``.  Available tools are:
                ``cceipdetail``, ``cveipdetail``, ``iavmipdetail``, 
                ``iplist``, ``listmailclients``, ``listservices``, 
                ``listos``, ``listsoftware``, ``listsshservers``,
                ``listvuln``, ``listwebclients``, ``listwebservers``,
                ``popcount``, ``sumasset``, ``sumcce``, ``sumclassa``,
                ``sumclassb``, ``sumclassc``, ``sumcve``, ``sumdnsname``,
                ``sumfamily``, ``sumiavm``, ``sumid``, ``sumip``,
                ``summsbulletin``, ``sumprotocol``, ``sumremediation``,
                ``sumseverity``, ``sumuserresponsibility``, ``sumport``,
                ``trend``, ``vulndetails``, ``vulnipdetail``, ``vulnipsummary``
        '''
        payload = {
            'type': 'vuln', 
            'sourceType': 'cumulative',
        }

        if 'source' in kw:
            payload['sourceType'] = self._check('source', kw['source'], str, 
                choices=['cumulative', 'patched'], case='lower')

        if 'tool' in kw:
            self._check('tool', kw['tool'], str, choices=[
                'cceipdetail',
                'cveipdetail',
                'iavmipdetail',
                'iplist', 
                'listmailclients',
                'listservices',
                'listos',
                'listsoftware',
                'listsshservers',
                'listvuln',
                'listwebclients',
                'listwebservers',
                'popcount',
                'sumasset',
                'sumcce',
                'sumclassa',
                'sumclassb',
                'sumclassc',
                'sumcve',
                'sumdnsname',
                'sumfamily',
                'sumiavm',
                'sumid', 
                'sumip',
                'summsbulletin',
                'sumport',
                'sumprotocol',
                'sumremediation',
                'sumseverity',
                'sumuserresponsibility',
                'trend',
                'vulndetails',
                'vulnipdetail',
                'vulnipsummary',
            ], case='lower')
        else:
            kw['tool'] = 'vulndetails'

        if 'scan_id' in kw:
            payload['sourceType'] = 'individual'
            payload['scanID'] = kw['scan_id']

        kw['payload'] = payload
        kw['analysis_type'] = 'vuln'

        return self._analysis(*filters, **kw)

    def scan(self, scan_id, *filters, **kw):
        '''
        '''
        kw['scan_id'] = self._check('scan_id', scan_id, int)
        return self.vuln(*filters, **kw)

    def events(self, *filters, **kw):
        '''
        '''
        payload = {'type': 'event', 'sourceType': 'lce'}

        if 'source' in kw:
            payload['sourceType'] = self._check('source', kw['source'], str, 
                choices=['lce', 'archive'], case='lower')
            if kw['source'] == 'archive':
                if 'silo_id' in kw:
                    payload['view'] = self._check('silo_id', kw['silo_id'], str)
                else:
                    raise UnexpectedValueError(
                        'silo_id is required for archive source')

        if 'tool' in kw:
            self._check('tool', kw['tool'], str, choices=[
                'listdata',
                'sumasset',
                'sumclassa',
                'sumclassb',
                'sumclassc',
                'sumconns',
                'sumdate',
                'sumdstip',
                'sumevent',
                'sumevent2',
                'sumip',
                'sumport',
                'sumprotocol',
                'sumsrcip',
                'sumtime',
                'sumtype',
                'sumuser',
                'syslog',
                'timedist',
            ], case='lower')
        else:
            kw['tool'] = 'syslog'

        kw['payload'] = payload
        kw['analysis_type'] = 'event'

        return self._analysis(*filters, **kw)


    def user(self, *filters, **kw):
        '''
        '''
        pass

    def console(self, *filters, **kw):
        '''
        '''
        pass

    def mobile(self, *filters, **kw):
        '''
        '''
        payload = {'type': 'mobile', 'sourceType': 'cumulative'}

        if 'tool' in kw:
            self._check('tool', kw['tool'], str, choices=[
                'listmodel',
                'listoscpe',
                'listvuln',
                'sumdeviceid',
                'summdmuser',
                'summodel',
                'sumoscpe',
                'sumpluginid',
                'sumprotocol',
                'sumseverity',
                'support',
                'vulndetails'
            ],  case='lower')
        else:
            kw['tool'] = 'vulndetails'
        
        kw['payload'] = payload
        kw['analysis_type'] = 'mobile'

        return self._analysis(*filters, **kw)