'''
analysis
========

The following methods allow for interaction into the Tenable.sc 
`analysis <https://docs.tenable.com/sccv/api/Analysis.html>`_ API.

Methods available on ``sc.analysis``:

.. rst-class:: hide-signature
.. autoclass:: AnalysisAPI

    .. automethod:: console
    .. automethod:: events
    .. automethod:: mobile
    .. automethod:: scan
    .. automethod:: user
    .. automethod:: vulns
'''
from .base import SCEndpoint, SCResultsIterator
from tenable.utils import dict_merge
from tenable.errors import *

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

        # sadly the totalRecords attribute isn't always returned.  If it is
        # returned, then we will simply update our total with the value of
        # totalRecords.  In the absense of a totalRecords, we will simply want
        # to check to see if the number of records equalled the page limiter.
        # if it did, then we will assume that therte is likely another page
        # ahead of this one and set the total count to be the limit + count + 1.
        # If the page size is less than the page limit, then we can likely
        # assume that this is the last page, and just set the total to be the
        # count + size of the page.
        if 'totalRecords' in resp['response']:
            self.total = int(resp['response']['totalRecords'])
        else:
            if len(resp['response']['results']) < self._limit:
                self.total = self.count + len(resp['response']['results'])
            else:
                self.total = self.count + self._limit + 1


class AnalysisAPI(SCEndpoint):
    def _expass(self, item):
        '''
        Expands the asset combination expressions from nested tuples to the
        nested dictionary structure that's expected.
        '''

        # the operator conversion dictionary.  The UI uses "and", "or", and
        # "not" whereas the API uses "intersection", "union", and "compliment".
        # if the user is passing us the tuples, lets assume that they are using
        # the UI definitions and not the API ones.
        oper = {
            'and': 'intersection',
            'or': 'union',
            'not': 'complement'
        }

        # some simple checking to ensure that we are being passed good data
        # before we expand the tuple.
        if len(item) < 2 or len(item) > 3:
            raise TypeError('{} must be exactly 1 operator and 1-2 items'.format(item))
        self._check('operator', item[0], str, choices=oper.keys())
        self._check('operand1', item[1], [int, tuple])
        if len(item) == 3:
            self._check('operand2', item[2], [int, tuple])

        resp = {'operator': oper[item[0].lower()]}

        # we need to expand the operand.  If the item is a nested tuple, then
        # we will call ourselves and pass the tuple.  If not, then we will
        # simply return a dictionary with the id value set to the integer that
        # was passed.
        if isinstance(item[1], tuple):
            resp['operand1'] = self._expass(item[1])
        else:
            resp['operand1'] = {'id': str(item[1])}

        # if there are 2 operators in the tuple, then we will want to expand the
        # second one as well. If the item is a nested tuple, then we will call 
        # ourselves and pass the tuple.  If not, then we will simply return a 
        # dictionary with the id value set to the integer that was passed.
        if len(item) == 3:
            if isinstance(item[2], tuple):
                resp['operand2'] = self._expass(item[2])
            else:
                resp['operand2'] = {'id': str(item[2])}

        # return the response to the caller.
        return resp

    def _query_constructor(self, *filters, **kw):
        '''
        Constructs an analysis query.  This part has been pulled out of the
        _analysis method and placed here so that it can be re-used in other
        part of the library.
        '''
        if 'query' not in kw:
            kw['query'] = {
                'tool': kw['tool'],
                'type': kw['analysis_type'],
                'filters': list()
            }
            for f in filters:
                item = {'filterName': f[0], 'operator': f[1]}

                if isinstance(f[2], tuple) and f[1] == '~' and f[0] == 'asset':
                    # if this is a asset combination, then we will want to
                    # expand the tuple into the expected dictionary struicture
                    # that the API is expecting.
                    item['value'] = self._expass(f[2])
                else:
                    # if we dont have any specific conditions set, then simply
                    # return the value parameter assigned to the "value" attribute
                    item['value'] = f[2]

                # Add the newly expanded filter to the filters list.
                kw['query']['filters'].append(item)
        return kw


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
        pages = None

        # Call the query constructor to build the query if necessary./
        kw = self._query_constructor(*filters, **kw)

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
            offset = self._check('offset', kw['offset'], int, default=0)

        if 'limit' in kw:
            limit = self._check('limit', kw['limit'], int, default=200)

        if 'pages' in kw:
            pages = self._check('pages', kw['pages'], int)

        if 'json_result' in kw and kw['json_result']:
            # if the json_result flag is set, then we do not want to return an
            # iterator, and instead just want to return the results section of
            # the response.
            payload['query']['startOffset'] = offset
            payload['query']['endOffset'] = limit + offset
            return self._api.post(
                'analysis', json=payload).json()['response']
        else:
            # the default option is the return the AnalysisResultsIterator
            return AnalysisResultsIterator(self._api,
                _offset=offset,
                _limit=limit,
                _query=payload,
                _pages_total=pages,
            )

    def vulns(self, *filters, **kw):
        '''
        Query's the analysis API for vulnerability data within the cumulative
        repositories.

        `SC Analysis: Vuln Type <https://docs.tenable.com/sccv/api/Analysis.html#AnalysisRESTReference-VulnType>`_

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

        Returns:
            AnalysisResultsIterator: an iterator object handling data pagination.

        Examples:
            A quick example showing how to get all of the information stored in
            SecurityCenter.  As the default is for the vulns method to return
            data from the vulndetails tool, we can handle this without actually
            doing anything other than calling 

            >>> from pprint import pprint
            >>> for vuln in sc.analysis.vulns():
            ...     pprint(vuln)

            To ask for a specific subset of information (like only critical and
            exploitable vulns) you'd want to pass the filter tuples into the
            query like so:

            >>> vulns = sc.analysis.vulns(
            ...    ('severity', '=', '4'),
            ...    ('exploitAvailable', '=', 'true'))

            To request a different data format (like maybe an IP summary of 
            vulns) you just need to specify the appropriate tool:

            >>> ips = sc.analysis.vulns(
            ...    ('severity', '=', '4'),
            ...    ('exploitAvailable', '=', 'true'), tool='sumip')
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
                'iplist', # not sure if this should be removed...
                'listmailclients',
                'listservices',
                'listos',
                'listsoftware',
                'listsshservers',
                'listvuln',
                'listwebclients',
                'listwebservers',
                'popcount', # not sure if we should remove this...
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

        # DIRTYHACK - If the tool is set to 'iplist', then we will want to make
        #             sure to specify that the json_result flag is set to bypass
        #             the iterator.  The iplist dataset is instead a dictionary
        #             and not a list.
        if kw['tool'] == 'iplist':
            # set the json_result flaf to True and call the _analysis method.
            kw['json_result'] = True
            resp = self._analysis(*filters, **kw)

            # The results attribute always appears to be NoneType, so lets
            # remove it in the interest of trying to keep a clean return.
            del(resp['results'])
            return resp

        # call the _analysis method and return tyhe results to the caller.
        return self._analysis(*filters, **kw)

    def scan(self, scan_id, *filters, **kw):
        '''
        Queries the analysis API for vulnerability data from a specific scan.

        `SC Analysis: Vuln Type <https://docs.tenable.com/sccv/api/Analysis.html#AnalysisRESTReference-VulnType>`_

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

        Returns:
            AnalysisResultsIterator: an iterator object handling data pagination.

        Examples:
            A quick example showing how to get the information for a specific
            scan from SecurityCenter.  As the default is for the scan method to 
            return data from the vulndetails tool, we can handle this without 
            actually doing anything other than calling 

            >>> for vuln in sc.analysis.scan(1):
            ...     pprint(vuln)

            To ask for a specific subset of information (like only critical and
            exploitable vulns) you'd want to pass the filter tuples into the
            query like so:

            >>> vulns = sc.analysis.scan(1
            ...    ('severity', '=', '4'),
            ...    ('exploitAvailable', '=', 'true'))

            To request a different data format (like maybe an IP summary of 
            vulns) you just need to specify the appropriate tool:

            >>> ips = sc.analysis.scan(1
            ...    ('severity', '=', '4'),
            ...    ('exploitAvailable', '=', 'true'), tool='sumip')
        '''
        kw['scan_id'] = self._check('scan_id', scan_id, int)
        return self.vuln(*filters, **kw)

    def events(self, *filters, **kw):
        '''
        Queries the analysis API for event data from the Log Correlation Engine

        `SC Analysis: Event Type <https://docs.tenable.com/sccv/api/Analysis.html#AnalysisRESTReference-EventType>`_

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
                The data source location.  Allowed sources are ``lce`` 
                and ``archive``.  Defaults to ``lce``.
            silo_id (int, optional):
                If a silo id is specified, then the results fetched will be from
                the lce silo specified and not from the cumulative result set.
            sort_field (str, optional):
                The field to sort the results on.
            sort_direction (str, optional):
                The direction in which to sort the results.  Valid settings are
                ``asc`` and ``desc``.  The default is ``asc``.
            tool (str, optional):
                The analysis tool for formatting and returning a specific view
                into the information.  If no tool is specified, the default will
                be ``vulndetails``.  Available tools are:
                ``listdata``, ``sumasset``, ``sumclassa``, ``sumclassb``, 
                ``sumclassc``, ``sumconns``, ``sumdate``, ``sumdstip``, 
                ``sumevent``, ``sumevent2``, ``sumip``, ``sumport``, 
                ``sumprotocol``, ``sumsrcip``, ``sumtime``, ``sumtype``, 
                ``sumuser``, ``syslog``, ``timedist``

        Returns:
            AnalysisResultsIterator: an iterator object handling data pagination.
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
        payload = {'type': 'user'}
        kw['payload'] = payload
        kw['tool'] = 'user'
        kw['analysis_type'] = 'user'
        return self._analysis(*filters, **kw)

    def console(self, *filters, **kw):
        '''
        Queries the analysis API for event data from the Log Correlation Engine

        `SC Analysis: scLog Type <https://docs.tenable.com/sccv/api/Analysis.html#AnalysisRESTReference-SCLogType.1>`_

        Args:
            filters (tuple, optional):
                The analysis module provides a more compact way to write filters
                to the analysis endpoint.  The purpose here is to aid in more
                readable code and reduce the amount of boilerplate that must be
                written to support a filtered call to analysis.  The format is
                simply a list of tuples.  Each tuple is broken down into
                (field, operator, value).
            date (str, optional):
                A date in YYYYMM format.  the default is simply "all".
            pages (int, optional):
                The number of pages to query.  Default is all.
            limit (int, optional):
                How many entries should be in each page?  Default is 200.
            offset (int, optional):
                How many entries to skip before processing.  Default is 0.
            sort_field (str, optional):
                The field to sort the results on.
            sort_direction (str, optional):
                The direction in which to sort the results.  Valid settings are
                ``asc`` and ``desc``.  The default is ``asc``.

        Returns:
            AnalysisResultsIterator: an iterator object handling data pagination.
        '''
        kw['payload'] = {
            'type': 'scLog', 
            'date': 'all' if 'date' not in kw else self._check('date', kw['date'], str)
        }
        kw['tool'] = 'scLog'
        kw['analysis_type'] = 'scLog'
        return self._analysis(*filters, **kw)

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