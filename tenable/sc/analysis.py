'''
analysis
========

The following methods allow for interaction into the Tenable.sc
:sc-api:`analysis <Analysis.html>` API.  The analysis area in Tenable.sc is
highly complex and allows for a wide range of varied inputs and outputs.  This
single endpoint has been broken down in pyTenable to several methods in order to
apply some defaults to the expected data-types and options most likely to be
returned.  As the filters are dependent on the tool and data-type that is being
referenced, the best solution to understanding what filters are available when
getting started is to simply pass a known bad filter string and use the
resulting error as an indicator of whats available.  For example, you could
perform the following action below while attempting to see the available filters
for the mobile data-type when using the ``vulndetails`` tool:

.. code-block:: python

    >>> x = sc.analysis.mobile(('something', '=', ''))
    >>> x.next()
    Traceback (most recent call last):
      File "<input>", line 1, in <module>
        x.next()
      File "tenable/base.py", line 75, in next
        self._get_page()
      File "tenable/sc/analysis.py", line 43, in _get_page
        resp = self._api.post('analysis', json=query).json()
      File "tenable/base.py", line 436, in post
        return self._request('POST', path, **kwargs)
      File "tenable/base.py", line 379, in _request
        raise self._error_codes[status](resp)
    PermissionError: 00000000-0000-0000-0000-000000000000:403 {"type":"regular",
    "response":"","error_code":146,"error_msg":"Invalid parameters specified for
    mobile vuln query.  The filter 'something' is invalid (valid filters:
    repositoryIDs, port, pluginID, familyID, pluginOutput, lastSeen,
    lastMitigated, severity, protocol, pluginName, baseCVSSScore,
    exploitAvailable, pluginPublished, pluginModified, vulnPublished,
    patchPublished, deviceID, mdmType, deviceModel, serialNumber, deviceUser,
    deviceVersion, osCPE).","warnings":[],"timestamp":1545060739}


The resulting error details specifically what filters can be set.

When it comes to constructing filters, TenableSC uses a common filter structure
for the collapsed filter-set.  This format is in the form of a 3 entry tuple
consisting of ('filtername', 'operator', 'value').  For example, if you're
looking to set the ``pluginID`` filter to ``19506`` the filter would look like
``('pluginID', '=', '19506')``.  Severities are in level of criticality, from 0
(informational) to 4 (critical).  Filters like these can be a string of comma-
separated values to indicate multiple items.  So for high and critical vulns,
``('severity', '=', '3,4')`` would return only what your looking for.

Asset list calculations in filters are a bit more complex, but still shouldn't
be too difficult.  Tenable.sc leverages nested pairs for the asset calculations
combined with a operator to define how that pair are to be combined.  Each of
the elements within the pair can further be nested, allowing for some quite
complex asset list math to happen.

On the simple side, if you just want to look for The the combined results of
asset lists 1 or 2, you would perform:
``('asset', '~', ('or', 1, 2))``.
Note the tilda, informing the filtering engine that it will need to perform some
sort of calculation first.  The tilda is only used when using the asset filter.

Now for a more complex calculation, you could look for the IPs that exist in
both 1 or 2, but not 3:
``('asset', '~', ('and', ('or', 1, 2), ('not', 3)))``
As you can see it's just a matter of nesting out from "1 or 2".  The only new
concept here is the paired tuple for not.  asking for the inverse of an asset
list requires that you wrap it in a tuple with the not operator.

Methods available on ``sc.analysis``:

.. rst-class:: hide-signature
.. autoclass:: AnalysisAPI

    .. automethod:: console
    .. automethod:: events
    .. automethod:: mobile
    .. automethod:: scan
    .. automethod:: vulns
'''
from .base import SCEndpoint, SCResultsIterator
from tenable.utils import dict_merge
from tenable.errors import *

class AnalysisResultsIterator(SCResultsIterator):
    def _get_page(self):
        '''
        Retrieves the next page of results when the current page has been
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
        # totalRecords.  In the absence of a totalRecords, we will simply want
        # to check to see if the number of records equaled the page limiter.
        # if it did, then we will assume that there is likely another page
        # ahead of this one and set the total count to be the limit + count + 1.
        # If the page size is less than the page limit, then we can likely
        # assume that this is the last page, and just set the total to be the
        # count + size of the page.
        total_records = resp['response'].get('totalRecords')
        records = resp['response'].get('returnedRecords')
        page_size = len(resp['response']['results'])

        if page_size == records and total_records:
            self.total = int(total_records)
        else:
            self._log.warning(' '.join([
                'API Recordkeeping error.',
                'api_total={},'.format(str(total_records)),
                'api_count={},'.format(str(records)),
                'page_size={},'.format(str(page_size)),
                'iter_total={}'.format(str(self.total))
            ]))
            if page_size < self._limit:
                self.total = self.count + page_size
            else:
                self.total = self.count + self._limit + 1


class AnalysisAPI(SCEndpoint):
    def _analysis(self, *filters, **kw):
        '''
        The base wrapper function handling the calls to the analysis API
        endpoint.  As this singular endpoint is used as the common API for all
        data export, much of the common handling can be centrally handled and
        only the unique elements for a given sub-type is handled by the
        individual methods.
        '''

        offset = 0
        limit = 1000
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

        if payload.get('sourceType') in ['individual']:
            payload['query']['view'] = self._check(
                'view', kw.get('view', 'all'), str,
                choices=['all', 'new', 'patched'], default='all')

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

        :sc-api:`analysis: vuln-type <Analysis.html#AnalysisRESTReference-VulnType>`

        Args:
            filters (tuple, optional):
                The analysis module provides a more compact way to write filters
                to the analysis endpoint.  The purpose here is to aid in more
                readable code and reduce the amount of boilerplate that must be
                written to support a filtered call to analysis.  The format is
                simply a list of tuples.  Each tuple is broken down into
                (field, operator, value).
            query_id (int, optional):
                The ID number of the SC Query where filters should be pulled from in place of the tuple filters. This is
                mutually exclusive with the tuple filters.
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
                ``sumasset``, ``sumcce``, ``sumclassa``, ``sumclassb``,
                ``sumclassc``, ``sumcve``, ``sumdnsname``,
                ``sumfamily``, ``sumiavm``, ``sumid``, ``sumip``,
                ``summsbulletin``, ``sumprotocol``, ``sumremediation``,
                ``sumseverity``, ``sumuserresponsibility``, ``sumport``,
                ``trend``, ``vulndetails``, ``vulnipdetail``, ``vulnipsummary``

        Returns:
            :obj:`AnalysisResultsIterator`:
                An iterator object handling data pagination.

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
        kw['type'] = 'vuln'

        # DIRTYHACK - If the tool is set to 'iplist', then we will want to make
        #             sure to specify that the json_result flag is set to bypass
        #             the iterator.  The iplist dataset is instead a dictionary
        #             and not a list.
        if kw['tool'] == 'iplist':
            # set the json_result flag to True and call the _analysis method.
            kw['json_result'] = True
            resp = self._analysis(*filters, **kw)

            # The results attribute always appears to be NoneType, so lets
            # remove it in the interest of trying to keep a clean return.
            del(resp['results'])
            return resp

        # call the _analysis method and return the results to the caller.
        return self._analysis(*filters, **kw)

    def scan(self, scan_id, *filters, **kw):
        '''
        Queries the analysis API for vulnerability data from a specific scan.

        :sc-api:`analysis: vuln-type <Analysis.html#AnalysisRESTReference-VulnType>`

        Args:
            scan_id (int):
                If a scan id is specified, then the results fetched will be from
                the scan specified and not from the cumulative result set.
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
                ``sumasset``, ``sumcce``, ``sumclassa``, ``sumclassb``,
                ``sumclassc``, ``sumcve``, ``sumdnsname``,
                ``sumfamily``, ``sumiavm``, ``sumid``, ``sumip``,
                ``summsbulletin``, ``sumprotocol``, ``sumremediation``,
                ``sumseverity``, ``sumuserresponsibility``, ``sumport``,
                ``trend``, ``vulndetails``, ``vulnipdetail``, ``vulnipsummary``
            view (str, optional):
                The type of vulnerability slice you'd like to have returned.
                The returned data can be either ``all``, ``new``, or ``patched``.
                If no view is specified, then the default will be ``all``.

        Returns:
            :obj:`AnalysisResultsIterator`:
                An iterator object handling data pagination.

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
        return self.vulns(*filters, **kw)

    def events(self, *filters, **kw):
        '''
        Queries the analysis API for event data from the Log Correlation Engine

        :sc-api:`analysis: event-type <Analysis.html#AnalysisRESTReference-EventType>`

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
            :obj:`AnalysisResultsIterator`:
                An iterator object handling data pagination.
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
        kw['type'] = 'event'

        return self._analysis(*filters, **kw)


    # not sure what the user datatype is, however I haven't seen any use-cases
    # for this datatype.  leaving the method here, just commented out in-case
    # it needs some love and attention at a later date.
    #def user(self, *filters, **kw):
    #    '''
    #    '''
    #    payload = {'type': 'user'}
    #    kw['payload'] = payload
    #    kw['tool'] = 'user'
    #    kw['type'] = 'user'
    #    return self._analysis(*filters, **kw)

    def console(self, *filters, **kw):
        '''
        Queries the analysis API for log data from the Tenable.sc Console itself.

        :sc-api:`analysis: sclog-type <Analysis.html#AnalysisRESTReference-SCLogType>`

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
            :obj:` AnalysisResultsIterator`:
                An iterator object handling data pagination.
        '''
        kw['payload'] = {
            'type': 'scLog',
            'date': 'all' if 'date' not in kw else self._check('date', kw['date'], str)
        }
        kw['tool'] = 'scLog'
        kw['type'] = 'scLog'
        return self._analysis(*filters, **kw)

    def mobile(self, *filters, **kw):
        '''
        Queries the analysis API for mobile data collected from querying one or
        many MDM solutions.

        :sc-api:`analysis: mobile-type <Analysis.html#AnalysisRESTReference-MobileType>`

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
            sort_field (str, optional):
                The field to sort the results on.
            sort_direction (str, optional):
                The direction in which to sort the results.  Valid settings are
                ``asc`` and ``desc``.  The default is ``asc``.
            tool (str, optional):
                The analysis tool for formatting and returning a specific view
                into the information.  If no tool is specified, the default will
                be ``vulndetails``.  Available tools are:
                ``listvuln``, ``sumdeviceid``, ``summdmuser``, ``summodel``,
                ``sumoscpe``, ``sumpluginid``, ``sumseverity``, ``vulndetails``

        Returns:
            :obj:`AnalysisResultsIterator`:
                An iterator object handling data pagination.
        '''
        payload = {'type': 'mobile', 'sourceType': 'cumulative'}

        if 'tool' in kw:
            self._check('tool', kw['tool'], str, choices=[
                'listvuln',
                'sumdeviceid',
                'summdmuser',
                'summodel',
                'sumoscpe',
                'sumpluginid',
                'sumseverity',
                'vulndetails'
            ],  case='lower')
        else:
            kw['tool'] = 'vulndetails'

        kw['payload'] = payload
        kw['type'] = 'mobile'

        return self._analysis(*filters, **kw)